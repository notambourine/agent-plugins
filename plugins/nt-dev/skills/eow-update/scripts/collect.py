#!/usr/bin/env python3
"""Collect one week of GitHub work, and every image and video attached to it, into one folder.

Writes <out>/week.md (the digest to read), <out>/week.json (the same, structured) and
<out>/media/ (downloaded attachments). Needs an authenticated `gh` and `curl`.
"""

import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

MEDIA_EXT = ("png", "jpg", "jpeg", "gif", "webp", "mp4", "mov", "webm", "pdf")
VIDEO_EXT = ("mp4", "mov", "webm")
CONTENT_TYPES = {
    "image/png": "png",
    "image/jpeg": "jpg",
    "image/gif": "gif",
    "image/webp": "webp",
    "video/mp4": "mp4",
    "video/quicktime": "mov",
    "video/webm": "webm",
    "application/pdf": "pdf",
}
BOT = re.compile(r"(\[bot\]$|^github-actions$|^dependabot|^renovate|^shopify$|-bot$)", re.I)
URL = re.compile(r"https?://[^\s<>()\"'\]]+")
GH_ASSET = re.compile(
    r"^https://(github\.com/user-attachments/(assets|files)/"
    r"|github\.com/[^/]+/[^/]+/assets/"
    r"|user-images\.githubusercontent\.com/"
    r"|private-user-images\.githubusercontent\.com/)"
)
GH_BLOB = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/(?:blob|raw)/([^/]+)/([^?#]+)")
BEFORE = re.compile(r"\b(before|old|was|today|current(ly)?|previous(ly)?|prior|on main|live)\b", re.I)
AFTER = re.compile(r"\b(after|new|now|fixed|this pr|with this change|preview|pinned)\b", re.I)
MEDIA_LINE = re.compile(
    r"!\[([^\]]*)\]\([^)]*\)|<(?:img|video)[^>]*?(?:alt=\"([^\"]*)\")?[^>]*>"
    r"|https://github\.com/user-attachments/assets/[\w-]+")
LINK_KINDS = (
    ("preview", re.compile(r"preview_theme_id=|shopifypreview\.com")),
    ("artifact", re.compile(r"claude\.ai/(code/)?artifact")),
    ("video", re.compile(r"loom\.com|youtu\.be|youtube\.com|vimeo\.com")),
    ("doc", re.compile(r"docs\.google\.com|drive\.google\.com|notion\.so|figma\.com")),
)


def run(cmd, stdin=None, binary=False):
    proc = subprocess.run(cmd, input=stdin, capture_output=True, text=not binary)
    if proc.returncode != 0:
        err = proc.stderr if not binary else proc.stderr.decode("utf8", "replace")
        raise RuntimeError(f"{' '.join(cmd[:4])}...: {err.strip()[:400]}")
    return proc.stdout


def gh_json(*args):
    return json.loads(run(["gh", *args]) or "null")


def local_date(iso):
    stamp = dt.datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return stamp.astimezone().date()


def slug(text, limit=40):
    text = re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")
    return text[:limit].strip("-") or "media"


def strip_md(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"<(img|video)[^>]*>", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = URL.sub("", text)
    return re.sub(r"[*_`#>|]+", " ", text).strip(" :-\t")


def sections(body):
    """Split a PR body on its `## ` headings. Text before the first heading is section ''."""
    out, name, lines = [], "", []
    for line in (body or "").splitlines():
        head = re.match(r"^#{1,3}\s+(.*)", line)
        if head:
            out.append((name, lines))
            name, lines = head.group(1).strip(), []
        else:
            lines.append(line)
    out.append((name, lines))
    return [(n, "\n".join(ls).strip()) for n, ls in out if n or "\n".join(ls).strip()]


def trimmed_body(body, full):
    """The parts a client update needs: why, what, caveats, what is still open."""
    body = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    body = re.sub(r"\n.*Generated with \[Claude Code\].*", "", body)
    parts = sections(body)
    if not any(n for n, _ in parts):
        return body.strip()[:1500]
    keep = []
    for name, text in parts:
        low = name.lower()
        if not full and re.search(r"test|validation|verif", low):
            unchecked = [ln for ln in text.splitlines() if re.match(r"\s*- \[ \]", ln)]
            if unchecked:
                keep.append(f"**{name} - still open**\n" + "\n".join(unchecked))
            continue
        if not full and name and not re.search(
                r"goal|summary|screenshot|rollout|release|open|decision|note|why|what", low):
            continue
        text = MEDIA_LINE.sub(lambda m: f"[{m.group(1) or m.group(2) or 'attachment'}]", text)
        keep.append((f"**{name}**\n" if name else "") + text)
    return "\n\n".join(keep).strip()


def find_media(text, source):
    """Every image or video URL in a body, with the caption written around it."""
    found, heading, last_text = [], "", ""
    for line in re.sub(r"<!--.*?-->", "", text or "", flags=re.S).splitlines():
        head = re.match(r"^#{1,4}\s+(.*)", line)
        if head:
            heading, last_text = head.group(1).strip(), ""
            continue
        urls = []
        for url in URL.findall(line):
            url = url.rstrip(".,;:!?")
            bare = url.split("?")[0].lower()
            if GH_ASSET.match(url) or bare.endswith(tuple("." + e for e in MEDIA_EXT)):
                urls.append(url)
        same_line = strip_md(line)
        if not urls:
            if same_line:
                last_text = same_line
            continue
        for url in urls:
            alt = re.search(r"!\[([^\]]*)\]\(" + re.escape(url), line)
            if not alt:
                tag = re.search(r"<(?:img|video)[^>]*" + re.escape(url) + r"[^>]*>", line)
                alt = re.search(r'alt="([^"]*)"', tag.group(0)) if tag else None
            alt = alt.group(1).strip() if alt else ""
            if re.fullmatch(r"(image|screenshot.*|img.*|video|\S+\.(png|jpe?g|gif|mp4|mov))?", alt, re.I):
                alt = ""
            caption = alt or same_line or last_text
            role = "unknown"
            before, after = BEFORE.search(caption), AFTER.search(caption)
            if (before and after) or re.search(r"\bvs\.?\b|\bversus\b|side by side", caption, re.I):
                role = "comparison"
            elif before:
                role = "before"
            elif after:
                role = "after"
            found.append(
                {"url": url, "caption": caption, "section": heading, "role": role, "source": source}
            )
    return found


def find_links(text):
    links = {}
    for url in URL.findall(re.sub(r"<!--.*?-->", "", text or "", flags=re.S)):
        url = url.rstrip(".,;:!?")
        for kind, pattern in LINK_KINDS:
            if pattern.search(url):
                links.setdefault(kind, [])
                if url not in links[kind]:
                    links[kind].append(url)
    return links


def sniff_ext(path):
    with open(path, "rb") as handle:
        head = handle.read(16)
    if head.startswith(b"\x89PNG"):
        return "png"
    if head.startswith(b"\xff\xd8"):
        return "jpg"
    if head.startswith(b"GIF8"):
        return "gif"
    if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    if head[4:8] == b"ftyp":
        return "mov" if head[8:12] == b"qt  " else "mp4"
    if head.startswith(b"\x1a\x45\xdf\xa3"):
        return "webm"
    if head.startswith(b"%PDF"):
        return "pdf"
    return ""


def download(url, stem, token):
    """Fetch one attachment. Returns the final path, or raises."""
    part = pathlib.Path(str(stem) + ".part")
    blob = GH_BLOB.match(url)
    if blob:
        owner, repo, ref, path = blob.groups()
        data = run(
            ["gh", "api", "-H", "Accept: application/vnd.github.raw",
             f"repos/{owner}/{repo}/contents/{path}?ref={ref}"],
            binary=True,
        )
        part.write_bytes(data)
        ctype = ""
    else:
        # The token goes in through stdin so it never shows in the process list.
        config = f'header = "Authorization: Bearer {token}"\n' if GH_ASSET.match(url) and token else ""
        ctype = run(
            ["curl", "-K", "-", "-sSL", "--fail", "--max-time", "900", "--max-filesize", "1000000000",
             "-o", str(part), "-w", "%{content_type}", url],
            stdin=config,
        ).split(";")[0].strip()
    ext = CONTENT_TYPES.get(ctype) or sniff_ext(part) or url.split("?")[0].rsplit(".", 1)[-1].lower()
    if ext not in MEDIA_EXT:
        part.unlink(missing_ok=True)
        raise RuntimeError(f"not an image or video ({ctype or 'unknown type'})")
    final = pathlib.Path(f"{stem}.{ext}")
    part.replace(final)
    return final


def image_size(path):
    try:
        from PIL import Image

        with Image.open(path) as image:
            return list(image.size)
    except Exception:
        return None


def human(size):
    return f"{size / 1e6:.1f} MB" if size >= 1e5 else f"{size / 1e3:.0f} KB"


def local_captures(dirs, start, end):
    """Screenshots and screen recordings saved on this machine inside the window."""
    lo = dt.datetime.combine(start, dt.time.min).timestamp()
    hi = dt.datetime.combine(end, dt.time.max).timestamp()
    seen, out = set(), []
    for root in dirs:
        root = pathlib.Path(root).expanduser()
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if len(path.relative_to(root).parts) > 3 or path in seen:
                continue
            if path.suffix.lower().lstrip(".") not in MEDIA_EXT or not path.is_file():
                continue
            stat = path.stat()
            if lo <= stat.st_mtime <= hi:
                seen.add(path)
                out.append(
                    {"path": str(path), "bytes": stat.st_size,
                     "when": dt.datetime.fromtimestamp(stat.st_mtime).strftime("%a %d %b %H:%M"),
                     "mtime": stat.st_mtime,
                     "kind": "video" if path.suffix.lower().lstrip(".") in VIDEO_EXT
                     else ("file" if path.suffix.lower() == ".pdf" else "image")}
                )
    return sorted(out, key=lambda item: item["mtime"])


PR_FIELDS = (
    "number,title,body,url,mergedAt,updatedAt,baseRefName,headRefName,labels,author,"
    "closingIssuesReferences,additions,deletions,changedFiles,isDraft,reviewDecision"
)


def list_prs(repo, state, query):
    args = ["pr", "list", "--repo", repo, "--state", state, "--search", query, "--limit", "300"]
    try:
        return gh_json(*args, "--json", PR_FIELDS + ",files")
    except RuntimeError:
        return gh_json(*args, "--json", PR_FIELDS)


def areas(pr):
    counts = {}
    for item in pr.get("files") or []:
        parts = item["path"].split("/")
        key = "/".join(parts[:2]) if len(parts) > 2 else parts[0]
        counts[key] = counts.get(key, 0) + 1
    return [k for k, _ in sorted(counts.items(), key=lambda kv: -kv[1])[:4]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="folder to write into")
    parser.add_argument("--repo", help="OWNER/REPO, default: the repo of the current folder")
    parser.add_argument("--from", dest="start", help="first day, YYYY-MM-DD (default: this Monday)")
    parser.add_argument("--to", dest="end", help="last day, YYYY-MM-DD (default: today)")
    parser.add_argument("--week", choices=("this", "last"), default="this")
    parser.add_argument("--scope", choices=("mine", "team"), default="mine")
    parser.add_argument("--author", help="GitHub login, default: the authenticated user")
    parser.add_argument("--client-logins", default="", help="comma list of the client's GitHub logins")
    parser.add_argument("--local-dirs", default="~/Videos,~/Movies,~/Pictures,~/Downloads,~/Desktop",
                        help="comma list of folders searched for this week's screenshots and recordings")
    parser.add_argument("--no-media", action="store_true", help="list attachments, download none")
    parser.add_argument("--full-bodies", action="store_true", help="keep every PR body section")
    args = parser.parse_args()

    today = dt.date.today()
    monday = today - dt.timedelta(days=today.weekday())
    if args.week == "last":
        monday -= dt.timedelta(days=7)
    start = dt.date.fromisoformat(args.start) if args.start else monday
    end = dt.date.fromisoformat(args.end) if args.end else (
        today if args.week == "this" else monday + dt.timedelta(days=6))

    repo_info = gh_json("repo", "view", *([args.repo] if args.repo else []),
                        "--json", "nameWithOwner,defaultBranchRef,url")
    repo = repo_info["nameWithOwner"]
    default_branch = repo_info["defaultBranchRef"]["name"]
    login = args.author or run(["gh", "api", "user", "--jq", ".login"]).strip()
    clients = {name.strip().lower() for name in args.client_logins.split(",") if name.strip()}
    token = run(["gh", "auth", "token"]).strip()

    out = pathlib.Path(args.out).expanduser()
    media_dir = out / "media"
    media_dir.mkdir(parents=True, exist_ok=True)

    # GitHub searches in UTC; ask a day wider on both sides, then filter on the local date.
    wide = f"{start - dt.timedelta(days=1)}..{end + dt.timedelta(days=1)}"
    who = f" author:{login}" if args.scope == "mine" else ""
    merged = [
        pr for pr in list_prs(repo, "merged", f"merged:{wide}{who}")
        if start <= local_date(pr["mergedAt"]) <= end and not BOT.search(pr["author"]["login"])
    ]
    merged.sort(key=lambda pr: pr["mergedAt"])
    open_prs = [
        pr for pr in list_prs(repo, "open", f"updated:>={start} author:{login}")
        if local_date(pr["updatedAt"]) >= start
    ]

    def comments_of(number):
        try:
            return gh_json("api", "--paginate", f"repos/{repo}/issues/{number}/comments") or []
        except RuntimeError:
            return []

    with ThreadPoolExecutor(6) as pool:
        all_comments = dict(zip([pr["number"] for pr in merged],
                                pool.map(comments_of, [pr["number"] for pr in merged])))

    # Issues a PR closes or names up front: who asked, and in what words.
    refs = {}
    for pr in merged:
        numbers = {item["number"] for item in pr.get("closingIssuesReferences") or []}
        lead = pr["title"] + "\n" + re.sub(r"<!--.*?-->", "", pr["body"] or "", flags=re.S)[:700]
        numbers |= {int(n) for n in re.findall(r"(?<![\w/])#(\d{2,6})\b", lead)}
        numbers.discard(pr["number"])
        pr["refs"] = sorted(numbers)
        for number in numbers:
            refs[number] = None

    def issue_of(number):
        try:
            data = gh_json("api", f"repos/{repo}/issues/{number}")
        except RuntimeError:
            return None
        return {
            "number": number,
            "title": data["title"],
            "author": data["user"]["login"],
            "association": (data.get("author_association") or "none").lower(),
            "state": data["state"],
            "is_pr": "pull_request" in data,
            "labels": [label["name"] for label in data.get("labels", [])],
            "url": data["html_url"],
            "body": data.get("body") or "",
            "from_client": data["user"]["login"].lower() in clients,
        }

    with ThreadPoolExecutor(6) as pool:
        for number, data in zip(list(refs), pool.map(issue_of, list(refs))):
            refs[number] = data

    closed_issues = []
    try:
        closed_issues = [
            issue for issue in gh_json(
                "issue", "list", "--repo", repo, "--state", "closed", "--limit", "200",
                "--search", f"closed:{wide} assignee:{login}",
                "--json", "number,title,author,closedAt,labels,url")
            if start <= local_date(issue["closedAt"]) <= end
        ]
    except RuntimeError as error:
        print(f"closed issues skipped: {error}", file=sys.stderr)

    # Attachments: PR body, human comments on it, and the body of an issue it closes.
    jobs, failures = [], []
    for pr in merged:
        found = find_media(pr["body"], f"PR #{pr['number']} body")
        for comment in all_comments.get(pr["number"], []):
            if not BOT.search(comment["user"]["login"]):
                found += find_media(comment["body"], f"PR #{pr['number']} comment by {comment['user']['login']}")
        for number in pr["refs"]:
            issue = refs.get(number)
            if issue and not issue["is_pr"]:
                found += find_media(issue["body"], f"issue #{number} body (the request)")
        seen, unique = set(), []
        for item in found:
            if item["url"] not in seen:
                seen.add(item["url"])
                unique.append(item)
        pr["media"] = unique
        for index, item in enumerate(unique, 1):
            item["stem"] = str(media_dir / f"pr{pr['number']}-{index:02d}-{slug(item['caption'])}")
            jobs.append(item)

    def fetch(item):
        stem = pathlib.Path(item["stem"])
        have = [p for p in stem.parent.glob(stem.name + ".*") if p.suffix != ".part"]
        try:
            path = have[0] if have else download(item["url"], item["stem"], token)
        except Exception as error:  # one broken link must not lose the week
            item["error"] = str(error)[:200]
            return
        item["file"] = str(path)
        item["bytes"] = path.stat().st_size
        ext = path.suffix.lstrip(".")
        item["kind"] = "video" if ext in VIDEO_EXT else ("file" if ext == "pdf" else "image")
        if item["kind"] == "image":
            item["size"] = image_size(path)

    if not args.no_media:
        with ThreadPoolExecutor(4) as pool:
            list(pool.map(fetch, jobs))
        failures = [item for item in jobs if "error" in item]
        wanted = {pathlib.Path(item["file"]) for item in jobs if "file" in item}
        for stale in media_dir.glob("pr[0-9]*-[0-9][0-9]-*"):
            if stale not in wanted:
                stale.unlink()

    local = local_captures([d for d in args.local_dirs.split(",") if d], start, end)

    # ---- week.md -------------------------------------------------------------------------
    lines = [
        f"# Week {start} to {end} - {repo}",
        "",
        f"Scope: {args.scope} ({login}). Live branch: `{default_branch}`. `media/` paths are under {out}.",
        f"{len(merged)} merged PRs, {len(open_prs)} open PRs touched, {len(closed_issues)} issues closed, "
        f"{sum(1 for j in jobs if 'file' in j)} attachments downloaded, {len(local)} local captures.",
        "",
        "## Merged this week",
    ]
    for pr in merged:
        mine = pr["author"]["login"] == login
        live = pr["baseRefName"] == default_branch
        labels = ", ".join(label["name"] for label in pr["labels"]) or "none"
        lines += [
            "",
            f"### #{pr['number']} {pr['title']}",
            f"- merged {local_date(pr['mergedAt']).strftime('%a %d %b')} by {pr['author']['login']}"
            f" | {pr['url']}",
            f"- base `{pr['baseRefName']}`: "
            + ("on the live branch" if live else "NOT the live branch - built, not on the live store yet"),
            f"- labels: {labels} | +{pr['additions']} -{pr['deletions']} in {pr['changedFiles']} files"
            + (f" | mostly {', '.join(areas(pr))}" if areas(pr) else ""),
        ]
        for number in pr["refs"]:
            issue = refs.get(number)
            if not issue:
                continue
            tag = "CLIENT REQUEST " if issue["from_client"] else ""
            kind = "PR" if issue["is_pr"] else "issue"
            lines.append(
                f"- {tag}refers to {kind} #{number} \"{issue['title']}\" by {issue['author']}"
                f" ({issue['association']})"
                f" [{issue['state']}; {', '.join(issue['labels']) or 'no labels'}] {issue['url']}")
            if issue["from_client"]:
                asked = " ".join(strip_md(issue["body"]).split())[:400]
                lines.append(f"  - in the client's words: {asked}")
        for comment in all_comments.get(pr["number"], []):
            if comment["user"]["login"].lower() in clients:
                said = " ".join(strip_md(comment["body"]).split())[:300]
                lines.append(f"- CLIENT COMMENT by {comment['user']['login']}: {said}")
        links = find_links(pr["body"])
        for kind, urls in links.items():
            lines.append(f"- {kind} links: " + " ".join(urls[:4]))
        for item in pr["media"]:
            if "file" in item:
                detail = human(item["bytes"]) + (f", {item['size'][0]}x{item['size'][1]}" if item.get("size") else "")
                lines.append(
                    f"- MEDIA [{item['kind']}, {detail}, role: {item['role']}] `media/{pathlib.Path(item['file']).name}`"
                    f" - \"{item['caption']}\" ({item['source']})")
            else:
                why = item.get("error", "not downloaded")
                lines.append(f"- MEDIA not fetched ({why}): {item['url']} - \"{item['caption']}\"")
        body = trimmed_body(pr["body"], args.full_bodies)
        if not mine and args.scope == "team":
            body = body[:1200]
        lines += ["", body or "_no description_"]

    lines += ["", "## Open PRs touched this week (in progress)"]
    for pr in sorted(open_prs, key=lambda item: item["number"]):
        state = "draft" if pr["isDraft"] else (pr.get("reviewDecision") or "in review").lower()
        goal = next((text for name, text in sections(re.sub(r"<!--.*?-->", "", pr["body"] or "", flags=re.S))
                     if "goal" in name.lower()), "")
        goal = " ".join(strip_md(goal).split())[:320]
        lines.append(f"- #{pr['number']} {pr['title']} [{state}; base `{pr['baseRefName']}`] {pr['url']}")
        if goal:
            lines.append(f"  - {goal}")
    if not open_prs:
        lines.append("_none_")

    lines += ["", "## Issues closed this week (assigned to the author)"]
    for issue in closed_issues:
        tag = "CLIENT REQUEST " if issue["author"]["login"].lower() in clients else ""
        lines.append(f"- {tag}#{issue['number']} {issue['title']} (opened by {issue['author']['login']}) {issue['url']}")
    if not closed_issues:
        lines.append("_none_")

    lines += ["", "## Local captures from this week (originals, not copied)"]
    for item in local:
        lines.append(f"- [{item['kind']}, {human(item['bytes'])}] {item['when']} `{item['path']}`")
    if not local:
        lines.append("_none_")

    if failures:
        lines += ["", "## Attachments that failed to download"]
        lines += [f"- {item['url']} ({item['error']})" for item in failures]

    (out / "week.md").write_text("\n".join(lines) + "\n")
    for pr in merged:
        pr["comments"] = [
            {"author": c["user"]["login"], "body": c["body"][:600], "url": c["html_url"]}
            for c in all_comments.get(pr["number"], []) if not BOT.search(c["user"]["login"])
        ]
    (out / "week.json").write_text(json.dumps(
        {"repo": repo, "default_branch": default_branch, "login": login, "scope": args.scope,
         "from": str(start), "to": str(end), "merged": merged, "open": open_prs,
         "closed_issues": closed_issues, "refs": refs, "local": local}, indent=1, default=str))

    print(f"{out / 'week.md'}")
    print(f"{len(merged)} merged PRs, {len(open_prs)} open, {len(closed_issues)} issues closed")
    print(f"{sum(1 for j in jobs if 'file' in j)}/{len(jobs)} attachments in {media_dir}, {len(local)} local captures")
    if failures:
        print(f"{len(failures)} attachments failed, listed at the end of week.md", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        sys.exit(f"collect: {error}")
