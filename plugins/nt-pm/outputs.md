# Output contract

The client skills (`intake`, `agenda`, `deck`, `follow-up`, `tick`) write through these
targets. Every write carries a ledger key; see [ledger.md](ledger.md).

## Targets

| Target           | Write                                                                          | Needs                                          |
| ---------------- | ------------------------------------------------------------------------------ | ---------------------------------------------- |
| `slack:#channel` | Slack mrkdwn message                                                           | Slack connector                                |
| `drive`          | Google Doc in `sources.drive`                                                  | Google Drive connector                         |
| `pdf`            | Branded PDF beside the Drive Doc, else in the working directory                | `nt-brand`, plus `typst` or `pandoc`           |
| `deck`           | Marp Markdown and its PDF, beside the Drive Doc, else in the working directory | `nt-brand`, marp-cli via `npx`, and Chrome     |
| `github`         | One issue per action item in `sources.github`                                  | `gh` CLI, or the GitHub connector in the cloud |
| `chat`           | Return the text; write nothing                                                 | none                                           |

## Approval

- `draft` sends every output to the user's own Slack DM, headed with its intended target.
  It creates no issues; it lists them in the draft. Without Slack, fall back to `chat`.
- `post` writes to the target. A target that reaches the client still needs `post`;
  nothing goes to a client by default.

Never send calendar invites to external guests. `calendar: hold` places a hold on the
user's calendar only.

## Slack mrkdwn

Slack strips markdown on paste. Bold is `*one asterisk*`, bullets are a literal `•`, and
there are no headings, tables, or fenced blocks. Put the ledger key in a final context
line.

## Writing

Lead with decisions, owners, and results. Give a result its number, comparison, and window
when the source has them. One bullet per item. No meeting narration, no "great call".
Client-facing outputs leave out internal notes from the config body. Anything that leaves
the client's own channels describes the client by sector, never by name.
