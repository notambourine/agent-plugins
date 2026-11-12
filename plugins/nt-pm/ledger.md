# Ledger contract

`agenda`, `follow-up`, and `tick` record every write under a key, so a loop that runs
every 15 minutes never writes the same output twice.

## Key

```text
nt:<eventId>:<instanceStartUTC>:<phase>
```

`instanceStartUTC` is the occurrence's start time as `YYYYMMDDTHHMMZ`. It separates the
instances of a recurring event, and it changes when a call moves, so a moved call gets a
new agenda. `phase` is `agenda`, `follow-up`, or `schedule`. A run with no calendar event
uses `nt:manual:<client>:<YYYYMMDD>:<phase>`.

## Where the key goes

The key lives in the output itself. Write it in the same call as the output, never as a
second step:

- Slack: the final context line of the draft DM or channel message.
- Google Doc: the end of the title.
- GitHub issue: an `<!-- nt:... -->` comment in the body.
- Calendar hold: the event description.

Before any write, search the first target for the key. If the key is there, skip the
write. If the search is unavailable or fails, also skip, and report it: missing one run
costs less than sending a client the same message twice.

## Local cache

`${XDG_STATE_HOME:-$HOME/.local/state}/nt-pm/ledger.jsonl` holds one
`{"key":"...","at":"..."}` line per confirmed write. A key found there skips the
destination search. A key missing there settles nothing, so search the destination. Cloud
runs have no cache.

## Manual runs

When a manual run finds its key already written, link the existing output and ask before
writing another.
