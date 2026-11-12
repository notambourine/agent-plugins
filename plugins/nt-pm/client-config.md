# Client context contract

Every client skill reads its client facts from a context file. Those facts never live in
this plugin or its repo.

## Location

Read the first of these that exists:

1. `.claude/refs/client-context.md` in the current repo, for work scoped to one client's
   repo.
2. `$NT_PM_CLIENT_DIR/<client>/client-context.md`, which covers every client and is where
   `tick` reads. Set `NT_PM_CLIENT_DIR` to a synced folder in user settings `env`.

When neither path has a `client-context.md` but one has a legacy `nt-pm.md`, read that
and offer to rename it.

When no file exists, offer to write one. Seed it from what the connectors find: the Slack
channels that match the client, the tracker project, the Drive folder, and the repo. Never
write it inside a plugin directory or this marketplace repo.

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

- Weekly call decks land in `weekly-calls/`.
- Shipped means live on the production branch.

## Context map

- `#ext-acme`: client asks and approvals.
- Drive `briefs/`: campaign briefs.
```

## Fields

| Field                    | Default           | Meaning                                                                                        |
| ------------------------ | ----------------- | ---------------------------------------------------------------------------------------------- |
| `domains`                | required          | Attendee email domains that tie a calendar event to this client                                |
| `sources.slack.internal` | required          | Team channels about the client; Slack is always read                                           |
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

Skills write what they learn about the client back to the body. Where the body and a
skill's default disagree, follow the body.

- **Tracker:** the stage field, what each stage means, and where the board guide lives.
  Read the board and record it here before proposing a ticket move. Never name a stage the
  board does not have.
- **Conventions:** the naming, folders, and definitions the user has corrected. Record
  each correction so the next session keeps it.
- **Context map:** each channel, doc, board, or thread that held useful context, with one
  line on what it holds. Add a place the first time it answers a question.

Edit the body in place. It describes the client as they are now and keeps no history.
