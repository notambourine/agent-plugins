---
name: human-voice
description: Humanize prose by choosing a surgical voice edit or a structural rewrite. Use for AI-sounding drafts, anti-slop passes, editorial reviews, and requests to preserve an author's voice.
allowed-tools: Read, Edit, Grep
argument-hint: "[<file> | pasted text] [--surgical | --rewrite]"
---

# Human voice

Pick one method and read only that one.

| Method | Choose for | Read |
| --- | --- | --- |
| Surgical | Authored draft, settled structure, review, uncertain touch, PR/commit/technical artifact | [surgical/METHOD.md](surgical/METHOD.md) |
| Rewrite | Machine draft, disposable structure, formulaic architecture, explicit redo/slop request | [rewrite/METHOD.md](rewrite/METHOD.md) |

Flags win. Default to surgical. State the choice in one line, then read the method. Never load both
in one pass. To restore an author's voice after a machine rewrite, run the rewrite, then a separate
surgical pass.

Your choice line and rationale meet the same bar as the draft.

## NoTambourine copy

When the text speaks for NoTambourine, read nt-brand's `references/voice.md` and build from its
golden set. Check claims against `doctrine/SOUL.md` and `doctrine/CULTURE.md`. Cite proof only from
`references/case-studies/`, under its white-label rules.

## Always

User requirements win. Keep claims, identifiers, commands, and paths intact. Hold terms stable. Use
ASCII hyphens unless told otherwise. Delete before adding.
