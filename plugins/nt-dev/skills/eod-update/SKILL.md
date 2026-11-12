---
name: eod-update
description: Draft a Slack end-of-day update on progress against epics and goals. Use when the user asks for an EOD, end-of-day, or daily status note.
allowed-tools:
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(gh issue list:*)
  - Bash(gh issue view:*)
  - Bash(gh api:*)
  - Bash(git log:*)
  - Bash(git config:*)
  - Bash(git remote:*)
  - Bash(date:*)
---

# End-of-day update

Draft a note that tells a lead how far each epic or goal moved today and what is blocking
it. The lead tracks goals. Today's commits, reviews, and comments are the evidence for the
note and stay out of it. Draft only; the user posts it.

## Find the goals

Start from today's record: local commits and the user's GitHub events (authored, reviewed,
commented, merged) whose timestamps fall today.

Trace each piece of work up to the goal it serves: the PR, the issue it closes, then that
issue's `parent`, else its milestone, else its project. A review or comment on a
teammate's PR belongs to the goal that PR serves. Goals the user names in the request
override the tracker.

Read each goal's standing from the tracker: `subIssuesSummary` on a parent issue, or the
open and closed counts and due date on a milestone.

Ask in one round for what the record cannot show: the goal behind any work that traces to
nothing, tomorrow's plan, and blockers. With no repo context, build the note from the
answers.

## Write

Write one entry for each goal that moved today or is blocked, largest movement first.
Leave out the other goals.

- **Standing:** what the tracker shows, such as `5 of 8 issues closed, due 14-11`. Call a
  goal on track, at risk, or a percentage complete only when the user said so; the tracker
  cannot show it.
- **Progress:** what is true of the goal tonight that was not true this morning, one
  bullet per outcome and in the client's terms. "Checkout accepts gift cards (#212)" is
  progress. "Reviewed #212, pushed 4 commits" is activity and does not belong. Cite PR and
  issue numbers, never URLs.
- **Next:** what remains before the goal closes, or the step planned for tomorrow.
- **Blockers:** the blocker, the goal it holds up, and who can clear it.

Work that serves no goal, such as maintenance or an unrelated review, shares one line
under Other.

The line under the header is the BLUF (bottom line up front). Make it the blocker that
needs someone, or failing that the goal that moved furthest.

White-label the note. Epic and milestone titles often carry a client's name, so restate
them by sector and shape.

Return only the note, as bare Slack mrkdwn text with no fence around it. Slack strips
markdown on paste, so bold is `*one asterisk*` and bullets are a literal `•`.

```text
🌇 *EOD Update DD-MM-YYYY*
[BLUF line]

🎯 *[Goal]* · [standing]
• [progress]
• Next: [what remains]

🧹 *Other*
• [work outside any goal]

🚩 *Blockers*
• [blocker, goal, who can clear it; or None]

📝 *Notes*
[optional]
```

Repeat the 🎯 block for each goal. Always include Blockers. Drop Other and Notes when
they are empty.
