# Output contract

The client skills (`intake`, `agenda`, `follow-up`, `tick`) write through these targets.
`shipped` and `weekly-recap` use `deck` only. Every write carries a ledger key; see
[ledger.md](ledger.md).

## Targets

| Target           | Write                                                                  | Needs                                          |
| ---------------- | ---------------------------------------------------------------------- | ---------------------------------------------- |
| `slack:#channel` | Slack mrkdwn message                                                   | Slack connector                                |
| `drive`          | Google Doc in `sources.drive`                                          | Google Drive connector                         |
| `pdf`            | Branded PDF beside the Drive Doc, else in the working directory        | `nt-brand`, plus `typst` or `pandoc`           |
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

## Decks

A deck is the same content as the Slack draft, shaped for slides. Return the Slack draft
too.

- **Content:** start from the skill's golden example in [examples/](examples/). Keep its
  slide order and section names; swap in this run's content and drop empty sections.
- **Format:** nt-brand's `system` skill owns slide shapes, front matter, and export in its
  `references/decks.md`. Never add a `<style>` block.
- **Theme:** pass nt-brand's mirrored `deck-standalone.css` to `--theme-set`. Resolve it
  from this plugin; the first path is the repo layout, the second the plugin cache:

  ```bash
  CSS=$(ls -d "${CLAUDE_PLUGIN_ROOT}"/../nt-brand/skills/system/deck-standalone.css \
    "${CLAUDE_PLUGIN_ROOT}"/../../nt-brand/*/skills/system/deck-standalone.css 2>/dev/null | tail -1)
  ```

- **Export:** marp-cli drives Chrome. A sandboxed shell may refuse to launch it; rerun the
  export unsandboxed.
- **Destination:** write `<date>-<skill>.md` and its PDF to `sources.drive_dir` under the
  Google Drive for desktop mount, else `My Drive/<client>/`, else the working directory.
  On macOS the mount is `~/Google Drive`. Drive syncs the files; never upload them.

## Slack mrkdwn

Slack strips markdown on paste. Bold is `*one asterisk*`, bullets are a literal `•`, and
there are no headings, tables, or fenced blocks. Put the ledger key in a final context
line.

## Writing

Lead with decisions, owners, and results. Give a result its number, comparison, and window
when the source has them. One bullet per item. No meeting narration, no "great call".
Client-facing outputs leave out internal notes from the config body. Anything that leaves
the client's own channels describes the client by sector, never by name.
