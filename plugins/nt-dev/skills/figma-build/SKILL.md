---
name: figma-build
description: Build a multi-section page from Figma frames, from intake to shipped PR.
effort: high
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, AskUserQuestion
argument-hint: "[epic-issue-number]"
---

# Figma page build

Ship one epic of several sections as a page that matches its frames at every breakpoint.
The repo's Figma workflow owns frame-level mechanics; this skill runs the page.

## Resolve the spec

Collect everything before planning: the epic and section issues, frame node IDs at every
project breakpoint, the real breakpoint ramp, themes, launch caveats, and the feature-flag
pattern. Ask for gaps in one round.

Inspect every frame. Record exact copy, typography, layout, spacing, semantic colors,
assets, and what changes per breakpoint. Search the codebase before proposing a component,
then classify each element:

- **REUSE:** use as is.
- **PROMOTE:** move an existing element to a shared layer; name what varies.
- **NEW:** create a primitive or shared local component.
- **NEEDS RULING:** give the options, their costs, and a recommendation.

Send design conflicts and reuse rulings as one batch. Never guess, and never leave an
inline color value.

## Build

Land shared work first: theme-complete tokens, then primitives that leave existing
consumers unchanged, then assets exported from the recorded node IDs in the project's
format.

Build the first section alone; it exposes the missing shared work. Then build the rest in
parallel. Each worker stays inside its section and hands missing tokens or primitives back
to the coordinator.

Follow the repo's server/client split and keep interactive state in small leaves. Copy
frame text verbatim. Flag placeholders and conflicting copy; never invent content.

## Verify

At every breakpoint, compare rendered values and behavior with the recorded spec. Confirm
probe preconditions, such as loaded images and settled animations, before trusting a
failure. Typecheck and lint each commit. A check written for a specific failure must be
shown to fail.

Before shipping, delete scaffolding comments and consolidate only proven duplication.
Rerun the same QA after any refactor.

## Ship

Commit shared dependencies before sections. Get explicit approval before git operations.
Check whether the branch already has a PR. Never force-push a shared branch.

Link the PR from each section issue. Write every open copy, design, or asset decision into
both the PR and the issue that owns it.
