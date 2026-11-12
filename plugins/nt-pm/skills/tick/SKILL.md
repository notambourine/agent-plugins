---
name: tick
description: One pass of the calendar loop that drafts due agendas and follow-ups across every client and skips anything already done. Run on a schedule.
disable-model-invocation: true
---

# Tick

This skill runs unattended. Never ask a question. Report what was skipped and why.

Run it every 15 minutes with `/loop 15m /nt-pm:tick` or a desktop scheduled task. A cloud
routine runs at most hourly and has no `gh`, Drive mount, or `NT_PM_CLIENT_DIR`, so use
one only for an hourly follow-up sweep.

Take the steps in order, cheapest first, and drop an event at the first step it fails:

1. Read Google Calendar from 4 hours ago to 2 hours ahead. Drop declined, cancelled, and
   all-day events.
2. Match each event to a client context in `$NT_PM_CLIENT_DIR` by attendee domain. Skip an
   event that matches none, which removes internal meetings.
3. Pick the phase:
   - `agenda` when the call starts within `timing.agenda-lead`.
   - `follow-up` when the call has ended and Granola has its notes. If the notes are not
     there yet, skip until a later run. Once `timing.notes-timeout` has passed, report the
     missing notes once.
4. Check the ledger per [../../ledger.md](../../ledger.md). Skip an event whose key is
   written.
5. Run `agenda` or `follow-up` for the event.

Return one line for each event acted on or reported, and nothing for the rest. If nothing
was due, return `nothing due`.
