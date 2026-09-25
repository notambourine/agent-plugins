# notambourine/agent-plugins

NoTambourine plugins for Claude Code and Codex.

## Install

### Claude Code

```bash
claude plugin marketplace add notambourine/agent-plugins
claude plugin list --available --json |
  jq -r '.available[] | select(.marketplaceName == "notambourine") | .pluginId' |
  while read -r plugin; do claude plugin install "$plugin" --scope user; done
```

Update: `claude plugin marketplace update notambourine`

Auto-update: `/plugin` > Marketplaces > notambourine > Enable auto-update.

### Codex

```bash
codex plugin marketplace add notambourine/agent-plugins
codex plugin list --json --available -m notambourine |
  jq -r '.available[].pluginId' |
  while read -r plugin; do codex plugin add "$plugin"; done
```

Start a new Codex thread after installation. These packages use portable Agent
Plugins manifests and shared Agent Skills. Claude-specific hooks remain available
only through Claude Code.

Portable packages: `nt-brand`, `nt-dev`, `nt-pm`, and `nt-voice`.
`nt-seo-spider`, `nt-shopify`, and `nt-vendor` remain Claude-only until their
MCP, hook, or vendored skill metadata is adapted.

## Plugins

| Plugin | Purpose |
| --- | --- |
| `nt-brand` | Brand tokens, CSS, decks, voice, and audits |
| `nt-dev` | PRs, issues, cleanup, recall, commits, and development workflows |
| `nt-pm` | Shipped updates and weekly recaps |
| `nt-seo-spider` | Screaming Frog MCP, 29 tools, SEO Spider 24+ |
| `nt-shopify` | Blocks live-store writes |
| `nt-voice` | Surgical prose edits and structural rewrites |
| `nt-vendor` | `codebase-design`, `audit-codebase`, `improve-codebase-architecture`, `install-anti-slop`, `eli5` |
| `nt-share` | `/nt-share:share`: branded unguessable URL; token required |
| `wormhook` | Blocks npm/PyPI supply-chain malware |

Enable repo-local plugins:

```bash
claude plugin enable nt-seo-spider@notambourine -s local
claude plugin enable nt-shopify@notambourine -s local
```

Config switches in `.claude/settings.json` `env`:

| Variable | Values |
| --- | --- |
| `NT_DEV_SKILL_NUDGE` | unset: block once; `strict`: block until skill read; `off` |
| `NT_DEV_DASH_GUARD` | unset: block a commit adding Unicode dashes; `strict`: block the write too; `off` |
| `NT_SHOPIFY_GUARD` | unset: block live writes; `off` |

`nt-shopify` allows reads, local app work, theme development, and
`theme push --development`. It blocks live targeting, mutations, deploys, releases,
environment writes, and unknown verbs. Run intentionally blocked commands yourself.

Per-machine control:

```bash
claude plugin install wormhook@notambourine --scope user
claude plugin disable wormhook@notambourine
```

Committed repo control:

```json
{ "enabledPlugins": { "nt-brand@notambourine": true } }
```

Contribute: [CONTRIBUTING.md](CONTRIBUTING.md). License: [MIT](LICENSE). Third-party
notices: [vendor/NOTICE.md](vendor/NOTICE.md).
