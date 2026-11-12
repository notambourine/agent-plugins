---
name: audit-codebase
description: Read-only whole-codebase audit for simplifications in data structures, state representation, control flow, algorithms, and ownership. Inventories every subsystem as a coverage contract, reviews each one in a bounded subagent, verifies each finding against the repo, then audits its own coverage. Never edits, runs tests, commits, or pushes. Use for "audit this codebase", "find simplifications", or a pre-refactor survey.
disable-model-invocation: true
---
<!-- vendored: aarondfrancis/8735edb@959a2a9 audit-your-codebase.md (unstated). -->

# Codebase audit

Audit the whole codebase for simplifications that matter. This is read-only: do not edit
files, run tests, commit, or push. You are the coordinator, and you continue until every
subsystem is reviewed and the final audit is validated.

## 1. Inventory every subsystem

Give each subsystem a stable ID, an exact ownership boundary, its key implementation
files, its public interfaces, major callers, and tests, and a status of `queued`,
`review`, `recommend`, or `skip`. Include product code, shared infrastructure, platform
bridges, ownership of generated contracts, and test and tooling infrastructure.

Keep one scratchpad that holds the inventory, confirmed findings, skip decisions,
cross-cutting patterns, duplicates, final priorities and dependencies, and a log. The
inventory is the coverage contract. A broad catch-all row does not prove coverage.

## 2. Review each subsystem in a fresh agent

Give each read-only agent one subsystem with a boundary that overlaps no other. Run only
as many at once as you can coordinate. Each agent inspects the implementation, public
interfaces, major callers, and tests, and returns at most two simplifications, or `skip`.

Look for:

- booleans or nullable fields that allow invalid combinations and should be a state
  machine or a discriminated union;
- assumptions about an object's shape repeated in several places;
- branching duplicated where a small map, registry, or reducer would remove it;
- state or behavior with no clear owner;
- repeated scans or lookups that a better collection or index would remove;
- lifecycle or async state that can go stale or contradict itself.

Prefer plain local code that is already clear. Reject a change whose only benefit is
style, hypothetical extensibility, a few fewer lines, or the same branching moved behind
a new type.

Each recommendation gives:

1. the verdict, recommend or skip;
2. evidence with exact file and line references;
3. the current complexity or invalid states;
4. the proposed representation and why it is simpler;
5. the smallest credible scope, with affected files and interfaces;
6. regression and migration risks;
7. the validation that exists and what more is needed;
8. confidence: high, medium, or low.

## 3. Verify and combine

Check every finding against the repository yourself before accepting it. Narrow, demote,
or reject one that is vague, duplicates another, misreads intended behavior, or only
moves complexity. Record each skip as completed coverage. Assign each accepted finding to
one subsystem. Keep opening review batches until every inventory row is closed.

## 4. Audit the audit

Run fresh independent passes for coverage, overlap between findings, materiality, missing
fields, and priority order. If the coverage pass finds an omission, add a row for it and
audit it. Do not widen a finished row to absorb it.

Rank the recommendations by impact, confidence, effort, blast radius, and prerequisites,
and name the best first slices to implement.

The audit is complete when every subsystem has a recommendation or an explicit skip,
every finding has all eight fields, the priorities are consistent, and the repository is
unchanged.
