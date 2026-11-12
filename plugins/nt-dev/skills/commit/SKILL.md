---
name: commit
description: Write and create focused git commits. Use when the user asks to commit or finished work needs committing.
allowed-tools:
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git log:*)
  - Bash(git add:*)
  - Bash(git commit:*)
---

# Commit

Give each commit one coherent scope, and split work that covers more.

Write the subject as `scope: lowercase imperative description`, under 72 characters, in
the repo's vocabulary and with no Conventional Commit type. Nest a scope when that helps,
and join two as `a,b`. The subject is the BLUF (bottom line up front): it states the
outcome, because that is what someone reading `git log --oneline` needs.

Add a body only for rationale the diff does not show, a trap, or an issue the commit
closes.

Stage the paths you touched. Never run `git add -A`.
