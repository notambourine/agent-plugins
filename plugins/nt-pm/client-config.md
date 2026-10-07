# Client config contract

Shared by the client skills: `intake`, `agenda`, `follow-up`, `tick`. Client facts never live in this plugin or its repo.

## Location

Read the first that exists:

1. `.claude/refs/nt-pm.md` in the current repo: one client, repo-scoped work.
2. `$NT_PM_CLIENT_DIR/<client>/nt-pm.md`: every client, used by `tick`. Set
   `NT_PM_CLIENT_DIR` in user settings `env`, pointing at a synced folder.

Neither found: stop and offer to write one from the template below. Never write it inside
a plugin directory or this marketplace repo.

## Template

```markdown
---
client: Acme
domains: [acme.com]
sources:
  slack: ["#acme-internal", "#ext-acme"]
  granola: true
  drive: https://drive.google.com/drive/folders/FOLDER_ID
  email: false
  github: acme/web
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
```

## Fields

| Field | Default | Meaning |
| --- | --- | --- |
| `domains` | required | Attendee email domains that map a calendar event to this client |
| `sources.slack` | required | Channels read for context; Slack is always on |
| `sources.granola` | `false` | Read call notes from Granola |
| `sources.drive` | none | Folder read for context and written for Doc outputs |
| `sources.email` | `false` | Opt-in; search Gmail threads with `domains` |
| `sources.github` | none | `owner/repo` read for open work and written for issues |
| `outputs.<phase>` | `outputs.default` | One target or a list; see [outputs.md](outputs.md) |
| `approval` | `draft` | `draft`: send to the user for review; `post`: write to the client-facing target |
| `calendar` | `propose` | `propose`: suggest times; `hold`: also place a guest-free hold on the user's calendar |
| `timing.agenda-lead` | `60m` | How far ahead of a call `tick` drafts the agenda |
| `timing.notes-timeout` | `4h` | How long after a call `tick` waits for notes before reporting |

The body overrides skill defaults where they conflict.
