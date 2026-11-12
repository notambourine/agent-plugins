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

Update with `claude plugin marketplace update notambourine`. To update automatically, open
`/plugin`, choose Marketplaces, then notambourine, then Enable auto-update.

### Codex

```bash
codex plugin marketplace add notambourine/agent-plugins
codex plugin list --json --available -m notambourine |
  jq -r '.available[].pluginId' |
  while read -r plugin; do codex plugin add "$plugin"; done
```

Start a new Codex thread after installing. Codex gets `nt-brand`, `nt-dev`, `nt-pm`, and
`nt-voice`, and it runs their skills but none of their hooks. `nt-seo-spider`,
`nt-shopify`, and `nt-vendor` depend on a Claude Code MCP server, hook, or skill format
and install only there.

## Plugins

| Plugin          | What it does                                                                                                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------- |
| `nt-brand`      | The brand kit: tokens, components, fonts, logos, deck and document PDF export, voice, doctrine, and case studies     |
| `nt-dev`        | Commits, pull requests, issues, end-of-day notes, session recall, and repo cleanup in house conventions              |
| `nt-pm`         | Client call agendas and follow-ups, deploy notes, weekly recaps, and Drive share links. Client facts stay out of it  |
| `nt-seo-spider` | Screaming Frog's MCP server and a `crawl` skill. Needs SEO Spider 24 or later                                        |
| `nt-shopify`    | Blocks writes to a live Shopify store                                                                                |
| `nt-voice`      | Edits prose so it reads as written by a person                                                                       |
| `nt-vendor`     | Third-party skills: `codebase-design`, `audit-codebase`, `improve-codebase-architecture`, `install-anti-slop`, `eli5` |
| `wormhook`      | Blocks npm and PyPI supply-chain malware before it runs                                                              |

## Turn plugins on per repo

`nt-seo-spider` and `nt-shopify` are off until a repo enables them:

```bash
claude plugin enable nt-seo-spider@notambourine -s local
claude plugin enable nt-shopify@notambourine -s local
```

To keep any other plugin off by default, install it at user scope and disable it:

```bash
claude plugin install wormhook@notambourine --scope user
claude plugin disable wormhook@notambourine
```

Then enable it in each repo that wants it, in the committed `.claude/settings.json`:

```json
{ "enabledPlugins": { "wormhook@notambourine": true } }
```

## Settings

Set these under `env` in `.claude/settings.json`:

| Variable             | Values                                                                                                   |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| `NT_DEV_SKILL_NUDGE` | Unset blocks a PR or issue write once to name the skill. `strict` blocks until the skill is read. `off`  |
| `NT_DEV_DASH_GUARD`  | Unset blocks a commit that adds a Unicode dash. `strict` also blocks the file write. `off`               |
| `NT_DEV_BRIEF`       | Unset lists the `nt-dev` skills at session start. `off`                                                  |
| `NT_SHOPIFY_GUARD`   | Unset blocks live writes. `off`                                                                          |
| `NT_PM_CLIENT_DIR`   | The synced folder that holds `<client>/client-context.md`. Set it in user settings and never commit it   |

`nt-shopify` allows reads, local app work, theme development, and
`theme push --development`. It blocks commands that target a live theme, mutations,
deploys, releases, environment writes, and any verb it does not recognize. To run a
blocked command on purpose, run it yourself outside the agent.

`nt-seo-spider` keeps what it learns about a site in that repo's
`.claude/refs/nt-seo-spider.md`.

## More

- [CONTRIBUTING.md](CONTRIBUTING.md) covers naming, layout, hooks, and the two mirrors.
- The license is [MIT](LICENSE). Third-party notices are in
  [vendor/NOTICE.md](vendor/NOTICE.md).
