# Contributing

## Names

- Name an internal plugin `nt-<job>`; name a public one for the job people search.
- Name a skill with one noun or verb. Never repeat the plugin name.
- `plugin.json` sets the command namespace; the marketplace row sets the install ID.
- Rename before anyone outside adopts it. A rename breaks installs.

## Ownership

- A domain plugin lives in its domain repo.
- A practice-wide plugin lives in `plugins/`.
- Promote a plugin to its own repo once its build, tests, or hooks earn one.
- Give each plugin audience one hook.
- Merge two skills when one has to load the other.

## Shared plugin

```text
plugins/nt-<name>/
  plugin.json
  skills/<skill>/SKILL.md
  hooks/hooks.json
  output-styles/<name>.md
```

Write root `plugin.json` to the Agent Plugins schema. Add each local-source row to both
marketplaces. Put host-specific metadata and hook policy under that host's extension. Bump
the portable manifest version whenever distributed behavior changes.

External source:

```json
{ "source": "url", "url": "https://github.com/OWNER/REPO.git" }
```

Use HTTPS. Never use a `github` source form.

## Hooks

- Write them in Node, never Bash.
- Fail open. Only a deliberate `deny` blocks.
- Ship an off switch.
- Put a `*.test.mjs` beside each hook.
- Resolve plugin files through `${CLAUDE_PLUGIN_ROOT}`.

## Output styles

- Frontmatter holds `name` and `description`.
- Default to `keep-coding-instructions: true`.
- Keep them opt-in; never auto-select one.
- Keep them short. The whole body stays resident.

## Brand mirror

`plugins/nt-brand/skills/system/` holds the exact bytes of the pinned
`@notambourine/brand-kit`.

```bash
npm ci
npm run brand
npm run brand:sync
```

Rules: [.claude/rules/brand-mirror.md](.claude/rules/brand-mirror.md).

## Vendored skills

```bash
node scripts/vendor-skills.mjs check <name>
node scripts/vendor-skills.mjs verify <name>
node scripts/vendor-skills.mjs pull <name>
node scripts/vendor-skills.mjs refs
```

Review the prose diff of every pull. Rules:
[.claude/rules/vendored-skills.md](.claude/rules/vendored-skills.md).

## Shell in skills

Rules: [.claude/rules/portable-shell.md](.claude/rules/portable-shell.md).
