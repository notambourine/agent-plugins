---
name: agenda
description: Draft a default agenda for an upcoming client call from the calendar event, the last follow-up, and open work. Use before a client meeting or when asked for an agenda.
---

# Agenda

An agenda gets each decision made on the call, with an owner.

Run `intake` for phase `agenda`. Resolve the event: the one named, else the client's next
call on Google Calendar. Check the ledger per [../../ledger.md](../../ledger.md); a hit
ends the run.

Build from these, highest priority first:

1. Open action items and unresolved questions from the last follow-up.
2. Standing items from the client config body.
3. What is new since the last call: shipped work, open PRs or issues waiting on the
   client, and Slack threads that need a decision.
4. The event description, when it names a topic.

Fit the agenda to the event length by dropping the lowest priority items first. Each item
names the decision or input wanted and its owner.

```text
🗓️ *<Client>: <Event title> (M/D, h:mm)*

🎯 *Decisions needed*
• *Topic:* Decision wanted. _Owner_

🔄 *Updates*
• *Topic:* One line.

📌 *Carried over*
• *Item:* Status. _Owner_
```

Omit empty sections. Write to the target per [../../outputs.md](../../outputs.md).
