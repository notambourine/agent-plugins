# Ledger contract

Shared by `agenda`, `follow-up`, and `tick`. Makes every run idempotent, so a 15-minute
loop repeats nothing.

## Key

```text
nt:<eventId>:<instanceStartUTC>:<phase>
```

`instanceStartUTC` is the occurrence's start, `YYYYMMDDTHHMMZ`. It separates recurring
instances and re-arms an agenda when a call moves. `phase` is `agenda`, `follow-up`, or
`schedule`. Runs with no calendar event use `nt:manual:<client>:<YYYYMMDD>:<phase>`.

## The destination is the ledger

Write the key in the same write as the output, never as a second step:

- Slack: final context line, in the draft DM or the channel.
- Google Doc: end of the title.
- GitHub issue: `<!-- nt:... -->` in the body.
- Calendar hold: event description.

Before any write, search the first target for the key. Found: skip. Search unavailable or
failed: skip and report; a missed run is cheaper than a duplicate client message.

## Local cache

`${XDG_STATE_HOME:-$HOME/.local/state}/nt-pm/ledger.jsonl`, one
`{"key":"...","at":"..."}` per line, appended after a confirmed write. A hit skips the
destination search. A miss proves nothing; search the destination. Cloud runs have no
cache.

## Manual runs

A key already present means the work exists. Link it and ask before writing another.
