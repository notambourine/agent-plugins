---
name: trim-comments
description: Remove comments that restate code and shorten comments that preserve necessary rationale or traps. Use before committing or when a diff is over-commented.
effort: high
allowed-tools: Bash, Read, Edit, Glob, Grep, AskUserQuestion
argument-hint: "[path-or-glob | --repo]"
disable-model-invocation: true
---

# Trim comments

Leave only comments that stop a wrong change.

## Test

A comment stays only when both hold:

- The surrounding code or config cannot show the fact.
- Without it, a competent editor could make a wrong change.

A survivor explains why a choice wins or warns of a trap. One line when possible, two at
most, and never longer than the code it covers.

Delete comments that describe code, explain well-named values or routine config switches,
narrate a change, repeat another comment or a memory rule, or carry authorship, tags, or
dates. Age earns no exemption.

## Scope

Inspect the union of:

- the path or glob argument;
- files edited, or comments deferred, this session;
- staged, unstaged, and untracked source files.

`--repo` covers every tracked source file. List the resolved files before editing.

Skip generated, vendored, dependency, lock, and prose files. Keep shebangs, licenses,
directives, lint and type suppressions, TODOs and FIXMEs linked to an issue, hook headers,
`FIX RUNBOOK` blocks, and comment-like text inside strings or embedded programs.

## Apply

Read each comment in context. Delete the failures first, then shorten survivors. Keep
traps at their point of use. Ask before moving broader rationale into a commit body, PR,
or repo memory file. Leave edits uncommitted.

Confirm every diff hunk changed only comments:

```bash
git diff -U0 | grep -E '^[+-]' | grep -vE '^(\+\+\+|---)' | grep -vE '^[+-][[:space:]]*(#|//|/\*|\*|--|$)'
```

Output is acceptable only for trailing comments. Skip checks CI already runs.

Report the changed files and counts for deleted, shortened, kept, and skipped.
