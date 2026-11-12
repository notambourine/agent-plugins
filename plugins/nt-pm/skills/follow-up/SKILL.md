---
name: follow-up
description: Turn a finished client call into a documented follow-up with decisions, action items, and next meeting. Use after a client call or when asked for call notes, a recap, or post-call issues.
---

# Follow-up

Draft a follow-up that records what the call decided, who owns each next step, and when
the team meets next.

Run `intake` for phase `follow-up`. Use the event the user named, or the client's most
recent call that has ended. Check the ledger per [../../ledger.md](../../ledger.md), and
stop if the key is already written.

Take the call from its Granola notes, or from notes the user pastes. With no notes, stop
and say so. Never reconstruct a call from its agenda.

Extract only what the notes support:

- Decisions, each with an owner.
- Action items, each with an owner and its due date if one was stated. Mark the others "no
  date".
- Open questions.
- The next meeting, when one was agreed or implied.

```text
📝 *<Client>: <Event title> (M/D)*
The decision or next step that matters most, in one line.

✅ *Decisions*
• *Topic:* Decision. _Owner_

📋 *Action items*
• *Item:* What, by when. _Owner_

❓ *Open questions*
• *Topic:* Question. _Who answers_

📅 *Next*
• Date, or "To schedule".
```

Write to every target per [../../outputs.md](../../outputs.md). For `deck`, start from
[../../examples/follow-up.deck.md](../../examples/follow-up.deck.md). For `github`, open
one issue per action item NoTambourine owns. Items the client owns stay in the message.

When the next meeting is still to schedule, propose two or three slots in the follow-up,
taken from the user's free time in working hours. With `calendar: hold`, also hold the
first slot under ledger phase `schedule`.
