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

One commit, one coherent scope. Split broader work.

Subject: `scope: lowercase imperative description`, under 72 characters, in the repo's
vocabulary. No Conventional Commit type. Nest a scope when it helps; join two with `a,b`.

Add a body only for rationale the diff hides, a trap, or an issue it closes.

Stage the paths you touched. Never `git add -A`.
