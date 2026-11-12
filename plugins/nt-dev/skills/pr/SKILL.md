---
name: pr
description: Create or revise a draft pull request.
allowed-tools: Bash, Read, Write, Glob
argument-hint: "[pr-number-to-edit]"
---

# Pull request

Open a draft PR that tells a PM what changed for users and what it moved. Mark it ready
only on request.

## Template

Search the target repo's `.github/`, root, and `docs/` for a committed template. Without
one, use [.github/pull_request_template.md](.github/pull_request_template.md). Keep the
chosen template's headings and markers.

## Body

Work out what changed from the issue, the source, the diff, and the commits. A branch
name or the commit subjects alone are not enough. Write BLUF (bottom line up front):
Goal's first sentence states the outcome and its measured impact, so a PM who stops there
knows what the PR did. Explain behavior and decisions and leave the file list to the
diff.

Summary answers the same three questions for each area the change reaches, even where the
repo's template words its Summary another way. Give each area a bold lead line, then one
sentence each:

- `Problem:` what a user hit or could not do, in their words.
- `Cause:` the mechanism that produced it. Name no files. A new capability has no cause,
  so drop the line.
- `Fix:` the approach that solves it, so a reader knows how without opening the diff.

Keep each of those lines under 20 words. Leave fallbacks, edge cases, test counts, and
file names to the diff. Keep the whole body within the template's word budget, and cut
detail before cutting a section.

For visible changes, add named before/after captures, or a recording for motion and flows.
Upload them as GitHub user attachments per
[references/github-attachments.md](references/github-attachments.md).

## Submit

Follow [references/body.md](references/body.md) for wording and for where the body file
goes. Submit with `gh pr create` or `gh pr edit`, keeping the formatting intact.
