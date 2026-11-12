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
milestones, labels, projects, and hierarchy. Labels and milestones are per repo, so never
carry metadata across projects.

Fill the target repo's committed form or template from `.github/ISSUE_TEMPLATE/` or
`.github/issue_template.md`, keeping its headings exactly. Without one, use
[.github/issue_template.md](.github/issue_template.md).

## Body

Write BLUF (bottom line up front): the title and the body's first sentence state the
outcome, so a PM who reads only those can triage. A title that names the activity or the
mechanism fails that test. The body covers the problem, scope, constraints, context, and
an acceptance check someone can observe. Put user behavior and business rules first. Add
implementation only when it is already decided or would be costly to rediscover. Link
decisions instead of repeating them.

A ticket moved from Asana, Jira, Slack, or a meeting carries only what the source and the
user state. Turn every gap into an open question. Never fill one with invented scope,
acceptance, settings, or configurability. The issue's readers cannot open an attachment
behind a login, such as an Asana `get_asset` or Jira link, so never link one. Download it
and upload it per
[../pr/references/github-attachments.md](../pr/references/github-attachments.md), or say
that it is missing.

Design work swaps the headings for four bold leads:

- `**Goal:**` the result in one sentence.
- `**Context:**` the design reference, plus `Replaces:` and `Figma:` URLs when they exist.
- `**Dev Notes:**` the verified component or token to reuse, cited as `path/to/File.tsx`.
  Never empty.
- `**Done when:**` the route, theme, and design result someone can observe.

Engineering work keeps the headings. Open with dated measurements, then the constraint,
then the target state. Cite `file.ts:155` only where the implementer would otherwise
rediscover it. Use at most one table or diagram. Name prerequisites and open questions.

Leave out delivery plans, tutorials, speculative solutions, and recaps. Show hierarchy
with child issues and parent links, and keep it out of the body.

## Submit

Follow [../pr/references/body.md](../pr/references/body.md) for wording and for where the
body file goes.

Set only the milestone, labels, fields, status, and parent the repo uses. Keep duplicated
metadata consistent. A revision folds new facts into the body; a comment records only a
dated decision or result.
