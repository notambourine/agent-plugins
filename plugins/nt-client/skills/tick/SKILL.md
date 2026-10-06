---
name: tick
description: One pass of the calendar loop that drafts due agendas and follow-ups across every client and skips anything already done. Run on a schedule.
disable-model-invocation: true
---

# Tick

Unattended. Never ask questions; report what was skipped and why.

Run it every 15 minutes with `/loop 15m /nt-client:tick` or a desktop scheduled task.
Cloud routines run at most hourly and have no `gh`, `typst`, or `NT_CLIENT_DIR`, so they
suit an hourly follow-up sweep, not agendas.

Cheapest check first; stop each event at the first miss:

1. Read Google Calendar from 4 hours ago to 2 hours ahead. Drop declined, cancelled, and
   all-day events.
2. Match each event to a client config in `$NT_CLIENT_DIR` by attendee domain. No match:
   skip; that drops internal meetings.
3. Pick the phase:
   - `agenda`: starts within `timing.agenda-lead`.
   - `follow-up`: ended, and Granola has its notes. No notes yet: skip until a later tick.
     Past `timing.notes-timeout`: report once.
4. Check the ledger per [../../ledger.md](../../ledger.md). Hit: skip.
5. Run `agenda` or `follow-up` for that event.

Return one line per event acted on or reported, nothing for silent skips. Nothing due:
return `nothing due`.
