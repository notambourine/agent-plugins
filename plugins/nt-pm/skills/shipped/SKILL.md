---
name: shipped
description: Draft plain-English Slack deploy notes for work about to ship or the last observed production push. Use for deploy previews and retrospective release summaries; drafts only, never deployed or posted by the agent.
disable-model-invocation: true
allowed-tools:
  - Bash(git fetch:*)
  - Bash(git reflog:*)
  - Bash(git rev-parse:*)
  - Bash(git rev-list:*)
  - Bash(git symbolic-ref:*)
  - Bash(git log:*)
  - Bash(git show:*)
  - Bash(git merge-base:*)
  - Bash(git remote:*)
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(gh issue view:*)
  - Bash(gh api:*)
  - Bash(date:*)
  - Bash(echo:*)
  - Bash(sed:*)
  - Bash(tr:*)
  - Bash(head:*)
---

# Deploy updates

Draft the note and never deploy. Follow [../../recap-format.md](../../recap-format.md).

## Range

- Pre-deploy, the default: from the remote default branch to the first of `dev`,
  `staging`, `develop`, or `release` that exists, or to `HEAD`.
- Retrospective: from the previous tip to the current tip in the remote default branch's
  reflog.
- Explicit: a reflog entry, SHA, tag, or date the user names. Use a named range as given.

Fetch `origin` and stop if the fetch fails. Resolve the endpoints, short SHAs, dates, and
commit count, then write. Never ask the user to confirm the range.

- With zero commits, say that nothing is pending or shipped.
- With an empty reflog on a retrospective, ask for a range.
- With no `origin`, ask for the deployment repo.

## Read the work

Read the non-merge commits. Find each one's PR from the number or SHA it references. Read
the PR body first, then the linked issues and the diff stat if the body does not explain
the change. Drop work that was already in the range's start. Claim little for a commit
with no PR or issue behind it. Group related work, and fold routine dependency and CI
changes into one line.

## Output

Return only:

```text
🚀 *Deploys: <window> (M/D/YY)*
The release's one result, in one line.

✨ *Features*
• *Label:* Outcome in one short sentence.

🛠️ *Fixes*
• *Label:* Outcome in one short sentence.
```

Word the window for the reader: `Last N Days` for a retrospective, `Pending` for a
pre-deploy.

Keep labels and sentences neutral. Name the surface with a generic noun and say what it
does now. Never suggest that the old behavior was wrong or that someone made a mistake.
That rules out comparatives and corrective wording such as `Smarter Search`,
`Right Order`, `Finally`, or `No Longer Broken`. Write `Search` and `Sort Order`.

Use these sections in this order, and only those that have bullets: ✨ Features, 🛠️ Fixes,
⚡ Performance, 📈 SEO & Marketing, 🗂️ Admin & Internal, ⚙️ Behind the Scenes.

When asked for a deck or PDF, also build one from
[../../examples/shipped.deck.md](../../examples/shipped.deck.md) per
[../../outputs.md](../../outputs.md#decks).
