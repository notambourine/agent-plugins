# Output contract

The client skills (`intake`, `agenda`, `follow-up`, `tick`) write through these targets.
`shipped` and `weekly-recap` use `deck` only; `share` uses `deck` and `pdf`. Every write
carries a ledger key; see [ledger.md](ledger.md).

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

An invite reaches the client without approval, so never send one to external guests.
`calendar: hold` places a hold on the user's calendar only.

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
is `~/Google Drive`. Drive syncs the files; never upload them. A naming or folder rule in
the context body's conventions overrides this; recurring outputs, like each week's call
deck, keep a dated name in their own folder.

## Decks

A deck is the same content as the Slack draft, shaped for slides. Return the Slack draft
too.

- **Content:** start from the skill's golden example in [examples/](examples/). Keep its
  slide order and section names; swap in this run's content and drop empty sections.
- **Format:** nt-brand's `system` skill owns slide shapes, front matter, and export in its
  `references/decks.md`. Pass `$KIT/deck-standalone.css` to `--theme-set`. The theme carries
  all styling, so never add a `<style>` block.

## Documents

A `pdf` is the same content as the Slack draft, written as a document. Return the Slack
draft too.

- **Format:** nt-brand's `system` skill owns front matter, structure, and the pandoc and
  Chrome export in its `references/documents.md`. Build `ref` from the client code and the
  skill. The template carries styling and page setup, so never add a `<style>` block or
  print flags.

## Slack mrkdwn

Write Slack messages per [recap-format.md](recap-format.md#slack-mrkdwn-not-markdown). Put
the ledger key in a final context line.

## Writing

Write BLUF (bottom line up front): the first line carries the outcome the reader acts on.
Lead with decisions, owners, and results. One bullet per item. No meeting narration, no
"great call". Client-facing outputs leave out internal notes from the context body.
Anything that leaves the client's own channels describes the client by sector, never by
name.

Client-facing decks and documents read as an agency presenting its work:

- **Pyramid:** open with the BLUF as one governing message, then group the support under it by
  audience or outcome. Ask for the message once when the sources do not settle it.
- **Numbers:** use one only when it carries the message and reads as a win. Never frame
  results as error counts or ratios like 998 of 999; state the outcome.
- **Asks:** a topic to align on beats a decision to make. Offer a proposed default the
  client can veto. Never ask the client to pick items out of raw data.
- **Proposals:** mark every date, plan, or readiness claim the sources do not state as the
  agent's proposal, and list them for the user. Confirm each before the output reaches the
  client.
- **Voice:** run `nt-voice:human-voice` on the text before showing the draft.
