# Output contract

The client skills (`intake`, `agenda`, `follow-up`, `tick`) write through these targets.
`shipped` and `weekly-recap` use `deck` only. Every write carries a ledger key; see
[ledger.md](ledger.md).

## Targets

| Target           | Write                                                                  | Needs                                          |
| ---------------- | ---------------------------------------------------------------------- | ---------------------------------------------- |
| `slack:#channel` | Slack mrkdwn message                                                   | Slack connector                                |
| `drive`          | Google Doc in `sources.drive`                                          | Google Drive connector                         |
| `pdf`            | Branded document PDF; see [Documents](#documents)                      | `nt-brand`, `pandoc`, and Chrome               |
| `deck`           | Marp deck and its PDF in the Drive folder on disk; see [Decks](#decks) | `nt-brand`, marp-cli via `npx`, and Chrome     |
| `github`         | One issue per action item in `sources.github`                          | `gh` CLI, or the GitHub connector in the cloud |
| `chat`           | Return the text; write nothing                                         | none                                           |

## Approval

- `draft` sends every output to the user's own Slack DM, headed with its intended target.
  It creates no issues; it lists them in the draft. Without Slack, fall back to `chat`.
- `post` writes to the target. A target that reaches the client still needs `post`;
  nothing goes to a client by default.

Never send calendar invites to external guests. `calendar: hold` places a hold on the
user's calendar only.

## Brand kit

Decks and documents export from nt-brand's mirrored kit. Resolve it from this plugin and
use it wherever nt-brand's guidance says `node_modules/@notambourine/brand-kit`; the first
path is the repo layout, the second the plugin cache:

```bash
KIT=$(ls -d "${CLAUDE_PLUGIN_ROOT}"/../nt-brand/skills/system \
  "${CLAUDE_PLUGIN_ROOT}"/../../nt-brand/*/skills/system 2>/dev/null | tail -1)
```

Chrome prints both. A sandboxed shell may refuse to launch it; rerun the export
unsandboxed.

Write `<date>-<skill>.md` and its PDF to `sources.drive_dir` under the Google Drive for
desktop mount, else `My Drive/<client>/`, else the working directory. On macOS the mount
is `~/Google Drive`. Drive syncs the files; never upload them.

## Decks

A deck is the same content as the Slack draft, shaped for slides. Return the Slack draft
too.

- **Content:** start from the skill's golden example in [examples/](examples/). Keep its
  slide order and section names; swap in this run's content and drop empty sections.
- **Format:** nt-brand's `system` skill owns slide shapes, front matter, and export in its
  `references/decks.md`. Pass `$KIT/deck-standalone.css` to `--theme-set`. Never add a
  `<style>` block.

## Documents

A `pdf` is the same content as the Slack draft, written as a document. Return the Slack
draft too.

- **Format:** nt-brand's `system` skill owns front matter, structure, and the pandoc and
  Chrome export in its `references/documents.md`. Build `ref` from the client code and the
  skill. Never add a `<style>` block or print flags.

## Slack mrkdwn

Slack strips markdown on paste. Bold is `*one asterisk*`, bullets are a literal `•`, and
there are no headings, tables, or fenced blocks. Put the ledger key in a final context
line.

## Writing

Lead with decisions, owners, and results. Give a result its number, comparison, and window
when the source has them. One bullet per item. No meeting narration, no "great call".
Client-facing outputs leave out internal notes from the config body. Anything that leaves
the client's own channels describes the client by sector, never by name.
