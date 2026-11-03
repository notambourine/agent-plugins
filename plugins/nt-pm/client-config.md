# Client context contract

Every client skill reads client facts from a context file. Client facts never live in this
plugin or its repo.

## Location

Read the first one that exists:

1. `.claude/refs/client-context.md` in the current repo, for one client and repo-scoped
   work.
2. `$NT_PM_CLIENT_DIR/<client>/client-context.md`, for every client; `tick` reads here.
   Set `NT_PM_CLIENT_DIR` in user settings `env` to a synced folder.

Read a legacy `nt-pm.md` at either path when no `client-context.md` exists, and offer to
rename it.

Neither exists: offer to write one. Seed it from what the connectors find: Slack channels
matching the client, the tracker project, the Drive folder, the repo. Never write it
inside a plugin directory or this marketplace repo.

## Template

```markdown
---
client: Acme
domains: [acme.com]
sources:
  slack:
    internal: ["#acme-internal"]
    external: ["#ext-acme"]
  granola: true
  drive: https://drive.google.com/drive/folders/FOLDER_ID
  drive_dir: Shared drives/acme-shared
  email: false
  github: acme/web
  asana: https://app.asana.com/0/PROJECT_ID
outputs:
  default: slack:#acme-internal
  agenda: slack:#acme-internal
  follow-up: [slack:#ext-acme, drive, github]
approval: draft
calendar: propose
timing:
  agenda-lead: 60m
  notes-timeout: 4h
---

Free-form notes: who attends, standing agenda items, tone, what never goes to the client.

## Tracker

Stage field: Stage. Shipped, waiting on client: Client Review. Complete: Done, marked
complete. Board guide: the project description.

## Conventions

- Weekly call decks: `weekly-calls/<YYYY-MM-DD> <name>.pdf`.
- Shipped means live on the production branch.

## Context map

- `#ext-acme`: client asks and approvals.
- Drive `briefs/`: campaign briefs.
```

## Fields

| Field                    | Default           | Meaning                                                                                        |
| ------------------------ | ----------------- | ---------------------------------------------------------------------------------------------- |
| `domains`                | required          | Attendee email domains that tie a calendar event to this client                                |
| `sources.slack.internal` | required          | Team channels about the client; Slack is always on                                             |
| `sources.slack.external` | none              | Shared channels with the client; read for asks, approvals, and tone                            |
| `sources.granola`        | `false`           | Read call notes from Granola                                                                   |
| `sources.drive`          | none              | Folder read for context and written for Doc outputs                                            |
| `sources.drive_dir`      | none              | Folder under the Google Drive for desktop mount where decks land, e.g. `Shared drives/<drive>` |
| `sources.email`          | `false`           | Opt-in Gmail search on `domains`                                                               |
| `sources.github`         | none              | `owner/repo` read for open work and written for issues                                         |
| `sources.asana`          | none              | Tracker project read for tickets and updated on request                                        |
| `outputs.<phase>`        | `outputs.default` | One target or a list; see [outputs.md](outputs.md)                                             |
| `approval`               | `draft`           | `draft` sends to the user for review; `post` writes to the client-facing target                |
| `calendar`               | `propose`         | `propose` suggests times; `hold` also places a guest-free hold on the user's calendar          |
| `timing.agenda-lead`     | `60m`             | How far ahead of a call `tick` drafts the agenda                                               |
| `timing.notes-timeout`   | `4h`              | How long after a call `tick` waits for notes before reporting                                  |

A flat `sources.slack` list counts as `internal`.

## Body

The body is the memory skills write back to. Where it and a skill default conflict, the
body wins.

- **Tracker:** the stage field, what each stage means, and where the board guide lives.
  Read the board and record it before proposing a ticket move. Never name a stage the
  board does not have.
- **Conventions:** naming, folders, and definitions the user corrected. Record each
  correction here so the next session keeps it.
- **Context map:** each channel, doc, board, or thread that held context, with one line on
  what it holds. Add a place the first time it pays off.

Edit the body in place; keep it a map, never a log.
