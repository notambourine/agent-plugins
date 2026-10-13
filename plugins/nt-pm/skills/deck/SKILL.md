---
name: deck
description: Build a branded client deck (review, agenda or kickoff, proposal) from the client's sources and export it to PDF. Use when asked for a deck, slides, or a presentation for a client.
---

# Deck

A deck makes one argument a slide at a time and ends on the decisions it needs.

This skill owns what goes in the deck. nt-brand's `system` skill owns how it looks: read
its `references/decks.md` and start from its `examples/deck.md`. Never restate its slide
grammar here or add a `<style>` block to the deck.

Run `intake` for phase `deck`. Check the ledger per [../../ledger.md](../../ledger.md); a
hit ends the run.

## Content

Pull from the intake digest, newest first: the last follow-up's decisions and action
items, open issues and PRs waiting on the client, shipped work, and case studies or
results docs in Drive. Give every number its comparison and window, and cite its source in
the slide's sublabel. A number without both stays off the slide; list it as missing
context instead.

One idea per slide. The headline states the takeaway, not the topic.

## Structure

Pick the story by deck type, then fit it to the meeting length by cutting the lowest
priority slides.

- **Client review:** results against the last review's goals, what ships next, and the
  decisions needed today. Open on the result that matters most to the client.
- **Agenda or kickoff:** goals and how success is measured, scope, timeline and owners,
  open questions. Close on the first decisions and who makes them.
- **Proposal:** the client's problem in their numbers, the approach, proof from a case
  study, scope and timeline, the ask.

Every type closes on the decisions or asks, each with an owner.

## Export

Export with the marp-cli command in `references/decks.md`, with `--theme-set "$CSS"` in
place of its `node_modules` path. Resolve it from this plugin's root; the first path is
the repo layout, the second the installed-plugin cache:

```bash
CSS=$(ls -d "${CLAUDE_PLUGIN_ROOT}"/../nt-brand/skills/system/deck-standalone.css \
  "${CLAUDE_PLUGIN_ROOT}"/../../nt-brand/*/skills/system/deck-standalone.css 2>/dev/null | tail -1)
```

marp-cli drives Chrome, so Chrome must be installed. A sandboxed shell may refuse to
launch it; rerun the export unsandboxed.

Write through the `deck` target per [../../outputs.md](../../outputs.md).
