---
name: tick
description: One pass of the calendar loop that drafts due agendas and follow-ups across every client and skips anything already done. Run on a schedule.
disable-model-invocation: true
---

# Tick

Runs unattended. Never ask questions; report what was skipped and why.

Run it every 15 minutes with `/loop 15m /nt-pm:tick` or a desktop scheduled task. Cloud
routines run at most hourly and have no `gh`, `typst`, or `NT_PM_CLIENT_DIR`. They suit an
hourly follow-up sweep, not agendas.

Run the cheapest check first, and drop an event at its first miss:

1. Read Google Calendar from 4 hours ago to 2 hours ahead. Drop declined, cancelled, and
   all-day events.
2. Match each event to a client config in `$NT_PM_CLIENT_DIR` by attendee domain. No
   match: skip. This drops internal meetings.
3. Pick the phase:
   - `agenda`: the call starts within `timing.agenda-lead`.
   - `follow-up`: the call ended and Granola has its notes. No notes yet: skip until a
     later tick. Past `timing.notes-timeout`: report once.
4. Check the ledger per [../../ledger.md](../../ledger.md). Hit: skip.
5. Run `agenda` or `follow-up` for that event.

Return one line per event acted on or reported, and nothing for silent skips. Nothing due:
return `nothing due`.
