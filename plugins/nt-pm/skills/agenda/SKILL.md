---
name: agenda
description: Draft a default agenda for an upcoming client call from the calendar event, the last follow-up, and open work. Use before a client meeting or when asked for an agenda; for a report of shipped work with no call, use weekly-recap.
---

# Agenda

Draft an agenda that gets each needed decision made on the call and gives it an owner.

Run `intake` for phase `agenda`. Use the event the user named, or the client's next call
on Google Calendar. Check the ledger per [../../ledger.md](../../ledger.md), and stop if
the key is already written.

Build from these, highest priority first:

1. Open action items and unresolved questions from the last follow-up.
2. Standing items from the client config body.
3. What is new since the last call: shipped work, open PRs or issues waiting on the
   client, and Slack threads that need a decision.
4. The event description, when it names a topic.

Write claims per [../../recap-format.md](../../recap-format.md#claims).

Fit the agenda to the length of the event, dropping the lowest-priority items first. Each
item names the input wanted and who owns it. List an item as a decision only when the
sources show the client has to choose on this call. Otherwise list it as a topic with a
proposed default.

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

Choose Worked through items per
[../../recap-format.md](../../recap-format.md#worked-through). Omit empty sections. When
the agenda will be shown in the meeting, offer a `deck` built from
[../../examples/agenda.deck.md](../../examples/agenda.deck.md). Write to the target per
[../../outputs.md](../../outputs.md).
