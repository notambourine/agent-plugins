---
name: follow-up
description: Turn a finished client call into a documented follow-up with decisions, action items, and next meeting. Use after a client call or when asked for call notes, a recap, or post-call issues.
---

# Follow-up

Run `intake` for phase `follow-up`. Resolve the event: the one named, else the client's most
recent ended call. Check the ledger per [../../ledger.md](../../ledger.md); a hit stops here.

Source the call from Granola notes, else notes the user pastes. No notes: stop and say so;
never reconstruct a call from the agenda.

Extract only what the notes support:

- Decisions, each with its owner.
- Action items, each with owner and due date when stated; mark the rest "no date".
- Open questions.
- Next meeting, when one was agreed or is implied.

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

Write to every target per [../../outputs.md](../../outputs.md). For `github`, one issue per
NoTambourine-owned action item; client-owned items stay in the message.

A next meeting "to schedule": propose two or three slots from the user's free/busy in
working hours, inside the follow-up. With `calendar: hold`, also hold the first slot under
ledger phase `schedule`.
