---
name: system
description:
  Build or review NoTambourine-branded surfaces, slide decks, and copy. Use for
  brand styling, color questions, positioning, deck and document PDF export, and
  copy audits before shipping.
---

# NoTambourine brand

Apply the brand without padding.

## Read only what the task needs

- For visual design or styling, read [visual rules](references/visual.md),
  including locked-surface font and logo traps.
- For writing or auditing anything clients or the public see, read
  [voice and copy audit](references/voice.md) and build from its golden set.
- For proof points or adding a client result, read
  [case studies](references/case-studies/README.md); never name the client.
- For slide authoring or deck export, read [deck guidance](references/decks.md).
  Load visual or voice guidance only when designing slides or writing/reviewing
  their copy.
- For a contract, proposal, report, or any other non-deck PDF, read
  [document guidance](references/documents.md).
- For a color, type, spacing, or component value, inspect the relevant CSS
  directly. Do not load prose references for a value lookup.
- For page or component markup, start from the matching file in `examples/` and
  keep its classes.
- For installation, asset selection, logo regeneration, or consumer integration,
  read the relevant section of [README.md](README.md).

## Name shared files

Name every PDF a client may receive as its title; it travels without its folder.

- Write `NoTambourine · Client (Topic).pdf`, parties joined with `·` as in a
  document H1. Internal work drops the client: `NoTambourine (Topic).pdf`.
- Name the topic by what the reader gets, never the tool: `(SEO Crawl)`, not
  `(Screaming Frog)`.
- Add the month to a point-in-time report: `(SEO Crawl, Oct 2026)`. Never add a
  version suffix or `final`.
- Append a signed document's ref so the file, footer, and DocuSign envelope
  match: `NoTambourine · Client (SOW 2) NTB-CLI-SOW2.pdf`.
- Keep the source a lowercase slug beside its export, dated runs as
  `seo-crawl-2026-10.md`. Never ship `deck.pdf` or `doc.pdf`.

## Source of truth

Treat `notambourine/brand-kit` as canonical. Read values from its CSS and
artwork from its assets. Correct brand values here, never by syncing a
downstream copy back in. Update consumer pins after a correction; a consumer's
limited theme support does not narrow the brand system.

Use semantic CSS aliases. Reach for primitives only when no alias fits or the
consumer integration requires it; consult README for framework exceptions. Never
hardcode colors outside renderer `var()` fallbacks.

Read doctrine only when needed: `doctrine/SOUL.md` holds client-facing beliefs
and `doctrine/CULTURE.md` the team's internal working rules. notambourine.com
publishes edited versions; do not infer internal policy from what they omit.
Keep client material unpublished; `/reports/` and `/pog/` are disallowed to
agents.
