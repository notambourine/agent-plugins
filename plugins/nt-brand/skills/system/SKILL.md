---
name: system
description:
  Build or review NoTambourine-branded surfaces, decks, and copy. Use for brand
  styling, color questions, positioning, and copy audits before shipping.
---

# NoTambourine brand

Apply the brand without padding.

## Read only what the task needs

- For visual design or styling, read [visual rules](references/visual.md),
  including locked-surface font and logo traps.
- For writing or auditing anything clients or the public see, read
  [voice and copy audit](references/voice.md) and build from its golden set.
- For slide authoring or export, read [deck guidance](references/decks.md). Load
  visual or voice guidance only when designing slides or writing/reviewing their
  copy.
- For a color, type, spacing, or component value, inspect the relevant CSS
  directly. Do not load prose references for a value lookup.
- For installation, asset selection, logo regeneration, or consumer integration,
  read the relevant section of [README.md](README.md).

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
