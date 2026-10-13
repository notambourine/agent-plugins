---
name: follow-up
description: Turn a finished client call into a documented follow-up with decisions, action items, and next meeting. Use after a client call or when asked for call notes, a recap, or post-call issues.
---

# Follow-up

A follow-up writes down what the call decided, who owns each next step, and when the team
meets next.

Run `intake` for phase `follow-up`. Resolve the event: the one named, else the client's
most recent ended call. Check the ledger per [../../ledger.md](../../ledger.md); a hit
ends the run.

Source the call from Granola notes, else from notes the user pastes. No notes: stop and
say so. Never rebuild a call from its agenda.

Extract only what the notes support:

- Decisions, each with an owner.
- Action items, each with an owner and the due date when one was stated; mark the rest "no
  date".
- Open questions.
- The next meeting, when one was agreed or implied.

```text
📝 *<Client>: <Event title> (M/D)*

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
one issue per NoTambourine-owned action item; client-owned items stay in the message.

When the next meeting is "to schedule", propose two or three slots from the user's
free/busy in working hours, inside the follow-up. With `calendar: hold`, also hold the
first slot under ledger phase `schedule`.
