# Output contract

`intake`, `agenda`, `follow-up`, and `tick` write through the targets below. `shipped` and
`weekly-recap` use only `deck`, and `share` uses `deck` and `pdf`. Every write carries a
ledger key; see [ledger.md](ledger.md).

## Targets

| Target           | Write                                                    | Needs                                          |
| ---------------- | -------------------------------------------------------- | ---------------------------------------------- |
| `slack:#channel` | A Slack mrkdwn message                                   | Slack connector                                |
| `drive`          | A Google Doc in `sources.drive`                          | Google Drive connector                         |
| `pdf`            | A branded document PDF; see [Documents](#documents)      | `nt-brand`, `pandoc`, and Chrome               |
| `deck`           | A Marp deck and its PDF; see [Decks](#decks)             | `nt-brand`, marp-cli through `npx`, and Chrome |
| `github`         | One issue per action item in `sources.github`            | `gh` CLI, or the GitHub connector in the cloud |
| `chat`           | The text, returned in the conversation and written nowhere | none                                         |

## Approval

- With `draft`, send every output to the user's own Slack DM under a heading that names
  the intended target. Create no issues; list them in the draft. Without Slack, fall back
  to `chat`.
- With `post`, write to the target. Nothing reaches a client unless the context file says
  `post`.

A calendar invite reaches its guests without any approval step, so never send one to
external guests. `calendar: hold` places a hold on the user's calendar only.

## Brand kit

Decks and documents export from the kit that nt-brand mirrors. Resolve its directory from
this plugin, and use that path wherever nt-brand's guidance says
`node_modules/@notambourine/brand-kit`. The first candidate is the repo layout and the
second is the plugin cache:

```bash
KIT=$(ls -d "${CLAUDE_PLUGIN_ROOT}"/../nt-brand/skills/system \
  "${CLAUDE_PLUGIN_ROOT}"/../../nt-brand/*/skills/system 2>/dev/null | tail -1)
```

Chrome prints both formats. If a sandboxed shell refuses to launch it, rerun the export
unsandboxed.

## Files

Name each export by the rules in nt-brand's `system` skill under "Name shared files". The
file travels without its folder, so the name is its title:

- A client PDF is `NoTambourine · <Client> (<Topic>).pdf`. Work with no client drops the
  client: `NoTambourine (<Topic>).pdf`.
- The topic says what the reader gets: `(Weekly Call)`, `(Call Follow-up)`, `(Deploys)`,
  `(Weekly Recap)`.
- A point-in-time output adds its month, `(Weekly Recap, Oct 2026)`. One that recurs
  within a month adds the day, `(Weekly Call, 14 Oct 2026)`, so two files never share a
  name.
- The Markdown source sits beside the export as a lowercase slug, such as
  `weekly-call-2026-10-14.md`.
- Never write `deck.pdf`, `doc.pdf`, a version suffix, or `final`.

Write both files to `sources.drive_dir` under the Google Drive for desktop mount. Without
that field, use `My Drive/<client>/`, and without a mount use the working directory. On
macOS the mount is `~/Google Drive`. Drive syncs the files, so never upload them. A folder
or naming rule in the context body's conventions overrides this section.

## Decks

A deck holds the same content as the Slack draft, shaped for slides. Return the Slack
draft with it.

- Start from the skill's example in [examples/](examples/). Keep its slide order and
  section names, replace its content with this run's, and drop empty sections.
- nt-brand's `references/decks.md` owns slide shapes, front matter, and export. Pass
  `$KIT/deck-standalone.css` to `--theme-set`. The theme carries all styling, so never add
  a `<style>` block.

## Documents

A `pdf` holds the same content as the Slack draft, written as a document. Return the Slack
draft with it.

nt-brand's `references/documents.md` owns front matter, structure, and the pandoc and
Chrome export. Build `ref` from the client code and the skill. The template carries
styling and page setup, so never add a `<style>` block or print flags.

## Slack mrkdwn

Format Slack messages per [recap-format.md](recap-format.md#slack-mrkdwn). Put the ledger
key in a final context line.

## Writing

Open with the BLUF (bottom line up front): the outcome the reader acts on. Follow it with
decisions, owners, and results, one bullet per item. Leave out any account of how the
meeting went. Keep internal notes from the context body out of client-facing output.
Outside the client's own channels and folders, describe the client by sector and never by
name.

A client-facing deck or document reads as an agency presenting its work:

- **One message.** State the BLUF as a single governing message, then group the support
  under it by audience or outcome. If the sources do not settle the message, ask the user
  for it once.
- **Numbers.** Use a number only when it carries the message and reads as a win. State the
  outcome; never report results as an error count or a ratio such as 998 of 999.
- **Asks.** Prefer a topic to align on, with a proposed default the client can veto, over
  a decision to make. Never ask the client to pick items out of raw data.
- **Proposals.** When the sources do not state a date, plan, or readiness claim, mark it
  as the agent's proposal and list those for the user. Confirm each one before the output
  reaches the client.
- **Voice.** Run `nt-voice:human-voice` on the text before showing the draft.
