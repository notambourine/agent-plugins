---
name: human-voice
description: Humanize prose by choosing a surgical voice edit or a structural rewrite. Use for AI-sounding drafts, anti-slop passes, editorial reviews, and requests to preserve an author's voice.
allowed-tools: Read, Edit, Grep
argument-hint: "[<file> | pasted text] [--surgical | --rewrite]"
---

# Human voice

Choose one method and read only that one.

| Method | Choose it when | Read |
| --- | --- | --- |
| Surgical | A person wrote the draft, its structure is settled, it is a PR, commit, or technical document, or you are unsure how much to change | [surgical/METHOD.md](surgical/METHOD.md) |
| Rewrite | A model wrote the draft, its structure is formulaic or can be discarded, or the user asked for a redo | [rewrite/METHOD.md](rewrite/METHOD.md) |

A flag decides the method. Without one, default to surgical. State your choice in one line, then
read the method. Never load both in one pass. To restore an author's voice after a rewrite, run a
separate surgical pass afterward.

Hold your own choice line and any rationale to the same standard as the draft.

## NoTambourine copy

When the text speaks for NoTambourine, read nt-brand's `references/voice.md` and build from its
golden set. Check claims against `doctrine/SOUL.md` and `doctrine/CULTURE.md`. Cite proof only from
`references/case-studies/`, under its white-label rules.

## Always

The user's requirements override both methods. Keep claims, identifiers, commands, and paths
intact, and keep each term the same throughout. Use ASCII hyphens unless told otherwise. Prefer
deleting words to adding them. Keep the BLUF (bottom line up front): the outcome stays in the
first sentence, and if an edit pushes it down, move it back.
