---
name: weekly-recap
description: Summarize a repo's shipped, in-review, and in-progress work for PMs and executives. Use for non-technical weekly recaps; drafts only, never posted by the agent.
allowed-tools:
  - Bash(gh pr list:*)
  - Bash(git log:*)
  - Bash(git for-each-ref:*)
  - Bash(git symbolic-ref:*)
  - Bash(date:*)
  - Bash(echo:*)
---

# Weekly recap

Recap the whole team's work. Follow [../../recap-format.md](../../recap-format.md).

Use the window the user named, or ask for one of 1 to 4 weeks. Compute inclusive dates
with whichever `date` syntax the machine has, BSD or GNU.

When the repo has a client context per [../../client-config.md](../../client-config.md),
run `intake` first and follow its conventions.

Collect merged PRs since the start, all open PRs, recent non-merge commits, and recently
touched branches.

- Shipped: PRs merged to the production branch. Work merged only to an integration branch
  such as `dev` or `staging` goes under In Progress, marked as waiting on release.
- In Review: open PRs on core work that are ready to merge.
- In Progress: active branches that have not merged.

Cover every contributor's merged work, then remove the names. Skip empty PRs.

Return only:

```text
📅 *Weekly Dev Recap: Mon D - Mon D, YYYY*
The week's one result, in one line.

🚀 *Shipped*
• *Label:* Outcome in one short sentence.

🧗 *Worked through*
• *Label:* What was in the way. What we did. Where it stands.

🔨 *In Progress*
• *Label:* Outcome in one short sentence.

👀 *In Review*
• *Label:* Outcome in one short sentence.
```

Use exactly these five emoji, in this order.

When asked for a deck or PDF, also build one from
[../../examples/weekly-recap.deck.md](../../examples/weekly-recap.deck.md) per
[../../outputs.md](../../outputs.md#decks).

Ask for the repo when none is given. Ask when the default branch is unclear.
