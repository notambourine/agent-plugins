---
name: eod-update
description: Draft a Slack end-of-day update. Use when the user asks for an EOD, end-of-day, or daily status note.
allowed-tools:
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(gh api:*)
  - Bash(git log:*)
  - Bash(git config:*)
  - Bash(git remote:*)
  - Bash(date:*)
---

# End-of-day update

Draft the note. Never post it.

## Gather

Pull today's local commits and the user's authenticated GitHub events: authored, reviewed,
commented, merged. Confirm each event's timestamp falls today. Count each PR once.
Collapse commits into the outcome they produced.

For a teammate's PR, state what the user did on it. For the user's own PR, state where it
stands. Ask only about work the record cannot show, tomorrow's plan, and blockers. With no
repo context, build the note from the answers.

## Write

Lead each item with the result. Keep items short. Cite PR numbers, never URLs. Name each
blocker and what it holds up. Write white-labelled: no client names.

Return only this, as bare Slack mrkdwn text, not a fenced block. Slack strips markdown on
paste, so bold is `*one asterisk*` and bullets are a literal `•`.

```text
🌇 *EOD Update DD-MM-YYYY*

✅ *Done*
• [item]

🔨 *Doing*
• [item]

🚩 *Blockers*
• [item or None]

📝 *Notes*
[optional]
```

Always include Blockers. Drop Notes when empty.
