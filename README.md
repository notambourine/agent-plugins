# notambourine/agent-plugins

The plugins NoTambourine engineers use to ship client work in Claude Code and Codex.

## Install

### Claude Code

```bash
claude plugin marketplace add notambourine/agent-plugins
claude plugin list --available --json |
  jq -r '.available[] | select(.marketplaceName == "notambourine") | .pluginId' |
  while read -r plugin; do claude plugin install "$plugin" --scope user; done
```

Update with `claude plugin marketplace update notambourine`. Turn on auto-update under
`/plugin` > Marketplaces > notambourine > Enable auto-update.

### Codex

```bash
codex plugin marketplace add notambourine/agent-plugins
codex plugin list --json --available -m notambourine |
  jq -r '.available[].pluginId' |
  while read -r plugin; do codex plugin add "$plugin"; done
```

Start a new Codex thread after install. Codex reads the portable Agent Plugins manifests
and shared Agent Skills. Hooks run only in Claude Code.

Portable: `nt-brand`, `nt-dev`, `nt-pm`, `nt-voice`. Claude-only until their MCP, hook, or
vendored skill metadata is adapted: `nt-seo-spider`, `nt-shopify`, `nt-vendor`.

## Plugins

| Plugin          | What it does                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `nt-brand`      | Brand tokens (CSS, JSON, Tailwind theme), components, examples, fonts, logos, decks, voice, doctrine, and white-labelled case studies |
| `nt-dev`        | Commits, PRs, issues, cleanup, recall, and daily development workflow                                                                 |
| `nt-pm` | Deploy notes, weekly recaps, client call agendas and follow-ups, and a deduped calendar loop; client configs stay outside this repo |
| `nt-seo-spider` | Screaming Frog MCP and a `crawl` skill; site facts in `.claude/refs/nt-seo-spider.md`. Needs SEO Spider 24+                           |
| `nt-shopify`    | Blocks writes to a live store                                                                                                         |
| `nt-voice`      | Surgical prose edits and structural rewrites                                                                                          |
| `nt-vendor`     | `codebase-design`, `audit-codebase`, `improve-codebase-architecture`, `install-anti-slop`, `eli5`                                     |
| `nt-share`      | `/nt-share:share` returns a branded, unguessable URL; needs a token                                                                   |
| `wormhook`      | Blocks npm and PyPI supply-chain malware                                                                                              |

Turn on the repo-local plugins:

```bash
claude plugin enable nt-seo-spider@notambourine -s local
claude plugin enable nt-shopify@notambourine -s local
```

Set switches in `.claude/settings.json` `env`:

| Variable             | Values                                                                               |
| -------------------- | ------------------------------------------------------------------------------------ |
| `NT_DEV_SKILL_NUDGE` | unset: block once; `strict`: block until the skill is read; `off`                    |
| `NT_DEV_DASH_GUARD`  | unset: block a commit that adds Unicode dashes; `strict`: block the write too; `off` |
| `NT_SHOPIFY_GUARD`   | unset: block live writes; `off`                                                      |
| `NT_PM_CLIENT_DIR` | Synced folder holding `<client>/nt-pm.md`; set in user settings, never committed |

`nt-shopify` allows reads, local app work, theme development, and
`theme push --development`. It blocks live targeting, mutations, deploys, releases,
environment writes, and unknown verbs. Run a blocked command yourself when you mean it.

Per machine:

```bash
claude plugin install wormhook@notambourine --scope user
claude plugin disable wormhook@notambourine
```

Per repo, committed:

```json
{ "enabledPlugins": { "nt-brand@notambourine": true } }
```

Contributing: [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE). Third-party
notices: [vendor/NOTICE.md](vendor/NOTICE.md).
