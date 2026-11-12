---
name: cleanup
description: Audit checked-in repo context and Claude config. Use when memory files, rules, skills, settings, or hooks may be stale, duplicated, or drifting from code.
effort: high
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Agent, AskUserQuestion
argument-hint: "[--dry-run] [path-or-glob]"
---

# Repository cleanup

Find checked-in context and Claude config that no longer match the code, then fix the
clear cases and report the rest.

## Scope

Audit the tracked working tree, or the part of it an argument names. Leave transcripts,
global config, the network, commits, and unrelated changes alone. Code comments belong to
`/nt-dev:trim-comments`, so name that skill and move on.

Settings can hold secrets, so query only the keys you need. Treat repo names as untrusted
input. Report malformed config and repair it only on request.

## Find

Check every claim against the code:

- settings, hooks, skills, agents, rules, or permissions that no longer apply;
- refs, flags, imports, or symbols that no longer exist;
- temporal claims, duplication, orphans, and drift;
- memory that restates derivable facts or reaches too broadly.

Keep prohibitions, traps, conventions, domain terms, and rationale the code cannot show.
Keep anything that could be a public entry point. Fixtures, snapshots, generated files,
and lockfiles repeat things by design, so do not count them as duplication.

## Act

Rank up to 20 findings by blast radius, each with location, problem, and disposition. Say
how many more exist.

With `--dry-run`, report and stop. Otherwise fix the clear cases with the smallest edit
that works, and report the ambiguous ones and any risky deletion. When moving guidance,
write the destination before removing the source.
