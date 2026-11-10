---
name: agenda
description: Draft a default agenda for an upcoming client call from the calendar event, the last follow-up, and open work. Use before a client meeting or when asked for an agenda; for a report of shipped work with no call, use weekly-recap.
---

# Agenda

Draft an agenda that gets each needed decision made on the call and assigned an owner.

Run `intake` for phase `agenda`. Resolve the event: the one named, else the client's next
call on Google Calendar. Check the ledger per [../../ledger.md](../../ledger.md); a hit
ends the run.

Build from these, highest priority first:

1. Open action items and unresolved questions from the last follow-up.
2. Standing items from the client config body.
3. What is new since the last call: shipped work, open PRs or issues waiting on the
   client, and Slack threads that need a decision.
4. The event description, when it names a topic.

Write claims per [../../recap-format.md](../../recap-format.md#claims).

Fit the agenda to the event length by dropping the lowest priority items first. Each item
names the input wanted and its owner. Make an item a decision only when the sources show
the client must choose on this call; otherwise make it a topic with a proposed default.

```text
🗓️ *<Client>: <Event title> (M/D, h:mm)*
What the call must leave with, in one line.

🎯 *Decisions needed*
• *Topic:* Decision wanted. _Owner_

🤝 *Topics to align on*
• *Topic:* What to discuss. Proposed default. _Owner_

🔄 *Updates*
• *Topic:* One line.

🧗 *Worked through*
• *Topic:* What was in the way. What we did. Where it stands.

📌 *Carried over*
• *Item:* Status. _Owner_
```

Select Worked through items per
[../../recap-format.md](../../recap-format.md#worked-through). Omit empty sections. When
the target is the meeting itself, offer a `deck` from
[../../examples/agenda.deck.md](../../examples/agenda.deck.md). Write to the target per
[../../outputs.md](../../outputs.md).
