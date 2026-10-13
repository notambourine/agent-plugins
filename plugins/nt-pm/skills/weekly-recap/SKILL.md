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

Use the window the user named. Without one, ask for 1 to 4 weeks. Compute inclusive dates
with whichever BSD or GNU `date` syntax is available.

Collect merged PRs since the start, all open PRs, recent non-merge commits, and recently
touched branches.

- Shipped: merged PRs.
- In Review: open, merge-ready core PRs.
- In Progress: active unmerged branches.

Cover every merged contributor's work, then strip the names. Skip empty PRs.

Return only:

```text
📅 *Weekly Dev Recap: Mon D - Mon D, YYYY*

🚀 *Shipped*
• *Label:* Outcome in one short sentence.

🔨 *In Progress*
• *Label:* Outcome in one short sentence.

👀 *In Review*
• *Label:* Outcome in one short sentence.
```

Use exactly these four emoji, in this order.

When asked for a deck or PDF, also build one from
[../../examples/weekly-recap.deck.md](../../examples/weekly-recap.deck.md) per
[../../outputs.md](../../outputs.md#decks).

Ask for the repo when none is given. Ask when the default branch is unclear.
