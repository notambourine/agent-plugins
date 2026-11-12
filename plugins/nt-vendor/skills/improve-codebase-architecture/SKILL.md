---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
disable-model-invocation: true
---
<!-- vendored: mattpocock/skills@fcf0071 skills/engineering/improve-codebase-architecture (MIT). -->

# Improve architecture

Find refactors that turn shallow modules into deep ones. Load `nt-vendor:codebase-design`
and use its terms exactly.

## 1. Explore

Decide where to look before looking. If the user named a module, subsystem, or pain
point, start there. Otherwise read back through `git log --oneline` for the areas that
change most often, because deepening pays off where change keeps happening.

Read `CONTEXT.md` and any ADRs for that area. Then spawn one agent to walk the code and
note where it is hard to follow:

- one concept spread across many small modules;
- shallow modules;
- functions extracted for testing while the bugs sit in how they are called;
- coupled modules that leak across their seams;
- code that is untested, or hard to test through its interface.

Apply the deletion test to anything that looks shallow.

## 2. Report

Write a self-contained `architecture-review-<timestamp>.html` to the OS temp directory,
so nothing is added to the repo. Open it with the platform's open command and tell the
user the absolute path. Follow [HTML-REPORT.md](HTML-REPORT.md).

Each candidate gets the files involved, the problem, the solution, the gain in locality,
leverage, and tests, a before-and-after visual, and a strength of `Strong`,
`Worth exploring`, or `Speculative`. Name domain concepts with the words in
`CONTEXT.md`. Mention a conflict with an ADR only when the problem is serious enough to
reopen that ADR. End with one top recommendation.

Do not propose interfaces yet. Ask the user which candidate to explore.

## 3. Work through the choice

Question the user about the chosen candidate: its constraints, its dependencies, where
the seam goes, and which tests survive. As decisions settle:

- add a new or sharpened domain term to `CONTEXT.md` right away;
- offer an ADR when the user rejects a candidate for a lasting reason that a later
  review would need in order not to suggest it again;
- for alternative interfaces, use the design-it-twice pattern in codebase-design.
