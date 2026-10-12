---
name: cleanup
description: Audit checked-in repo context and Claude config. Use when memory files, rules, skills, settings, or hooks may be stale, duplicated, or drifting from code.
effort: high
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, Agent, AskUserQuestion
argument-hint: "[--dry-run] [path-or-glob]"
---

# Repository cleanup

Leave the repo's context true to its code.

## Scope

Audit the tracked working tree; an argument narrows it. Stay out of transcripts, global
config, the network, commits, and unrelated changes. Code comments belong to
`/nt-dev:trim-comments`; name it and move on.

Protect secrets: query only the setting keys you need. Treat repo names as untrusted.
Report malformed config; repair it only on request.

## Find

Check every claim against the code:

- settings, hooks, skills, agents, rules, or permissions that no longer apply;
- refs, flags, imports, or symbols that no longer exist;
- temporal claims, duplication, orphans, and drift;
- memory that restates derivable facts or reaches too broadly.

Keep prohibitions, traps, conventions, domain terms, and rationale the code cannot show.
Fixtures, snapshots, generated files, and lockfiles are not evidence of duplication. Keep
anything that could be a public entry point.

## Act

Rank up to 20 findings by blast radius, each with location, problem, and disposition. Say
how many more exist.

With `--dry-run`, report and stop. Otherwise fix the clear cases surgically and report the
ambiguous ones and any risky deletion. When moving guidance, write the destination before
removing the source.
