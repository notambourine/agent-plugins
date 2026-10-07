# Output contract

Shared by the client skills: `intake`, `agenda`, `follow-up`, `tick`. Every write carries a ledger key; see [ledger.md](ledger.md).

## Targets

| Target | Write | Needs |
| --- | --- | --- |
| `slack:#channel` | Slack mrkdwn message | Slack connector |
| `drive` | Google Doc in `sources.drive` | Google Drive connector |
| `pdf` | Branded PDF beside the Drive Doc, else in the working directory | `nt-brand`, plus `typst` or `pandoc` |
| `github` | One issue per action item in `sources.github` | `gh` CLI, or the GitHub connector in the cloud |
| `chat` | Return the text; write nothing | none |

## Approval

- `draft`: send every output to the user's own Slack DM, headed with its intended target.
  Create no issues; list them in the draft. Fall back to `chat` without Slack.
- `post`: write to the target. A target that reaches the client still needs `post`;
  nothing is posted to a client by default.

Never send calendar invites to external guests. `calendar: hold` places a hold on the
user's calendar only.

## Slack mrkdwn

Slack strips markdown on paste. Bold is `*one asterisk*`, bullets are a literal `•`, no
headings, tables, or fenced blocks. Put the ledger key in a final context line.

## Writing

Lead with decisions and owners. One bullet per item. No meeting narration, no "great call".
Client-facing outputs omit internal notes from the config body.
