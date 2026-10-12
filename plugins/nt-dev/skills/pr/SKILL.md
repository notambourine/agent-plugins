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

Build the story from the issue, source, diff, and commits; a branch name or commit
subjects alone are not enough. Open on the outcome and its measured impact. Explain
behavior and decisions, not files. Size the body to the change. Give it a specific title.

Write plainly: concrete nouns, no inflated adjectives, no `not just X but Y`, no closing
flourish. Never name a client; describe them by sector and shape.

For visible changes, add named before/after captures, or a recording for motion and flows.
Upload them as GitHub user attachments per
[references/github-attachments.md](references/github-attachments.md).

## Submit

Write the body file to an absolute session-scratchpad path, never `$TMPDIR`. `gh` runs
unsandboxed, where `$TMPDIR` is shared and `--body-file` can read another session's file.

Submit with `gh pr create` or `gh pr edit`, keeping the formatting intact.
