---
name: issue
description: Create or revise a GitHub issue.
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[issue-number-to-edit]"
---

# GitHub issue

Write an issue a PM can act on: the outcome, what it covers, and how to tell it is done.

## Template

Work in the target repo with authenticated `gh`. Read its recent issues for conventions,
milestones, labels, projects, and hierarchy. Never carry metadata across projects.

Fill the target repo's committed form or template from `.github/ISSUE_TEMPLATE/` or
`.github/issue_template.md`, keeping its headings exactly. Without one, use
[.github/issue_template.md](.github/issue_template.md).

## Body

Title the outcome, not the activity or mechanism. The body covers the problem, scope,
constraints, context, and acceptance someone can observe. Put user behavior and business
rules first. Add implementation only when it is decided or costly to rediscover. Link
decisions instead of repeating them.

Write plainly: concrete nouns, no inflated adjectives, no `not just X but Y`, no closing
flourish. Never name a client; describe them by sector and shape.

A ticket moved from Asana, Jira, Slack, or a meeting carries only what the source and the user
state. Every gap becomes an open question, never scope, acceptance, settings, or
configurability. Never link an attachment behind a login (Asana `get_asset`, Jira). Download it
and upload it per [../pr/references/github-attachments.md](../pr/references/github-attachments.md),
or name it as missing.

Design work swaps the headings for four bold leads:

- `**Goal:**` the result in one sentence.
- `**Context:**` the design reference, plus `Replaces:` and `Figma:` URLs when they exist.
- `**Dev Notes:**` the verified component or token to reuse, cited as `path/to/File.tsx`.
  Never empty.
- `**Done when:**` the route, theme, and design result someone can observe.

Engineering work keeps the headings. Open with dated measurements, then the constraint,
then the target state. Cite `file.ts:155` only where the implementer would otherwise
rediscover it. Use at most one table or diagram. Name prerequisites and open questions.

Leave out delivery plans, tutorials, speculative solutions, recaps, and fake hierarchy.
Use child issues and real parent links.

## Submit

Write the body file to an absolute session-scratchpad path, never `$TMPDIR`. `gh` runs
unsandboxed, where `$TMPDIR` is shared and `--body-file` can read another session's file.

Set only the milestone, labels, fields, status, and parent the repo uses. Keep duplicated
metadata consistent. A revision folds new facts into the body; a comment records only a
dated decision or result.
