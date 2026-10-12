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

- Fix the brand upstream, release it, pin the exact version, then sync.
- Never edit the mirror. Never read it from `node_modules` at runtime.
- Style with the semantic `--bg`, `--fg1`, `--accent`, `--sp-*`, and `--r-*` tokens.

## Vendored skills

```bash
node scripts/vendor-skills.mjs check <name>
node scripts/vendor-skills.mjs verify <name>
node scripts/vendor-skills.mjs pull <name>
node scripts/vendor-skills.mjs refs
```

- Give each manifest entry a source, pin, path, and license. A gist uses `gist`, `owner`,
  and `entry`.
- Pull one named skill at a time.
- Vendor whole directories.
- Review the prose diff and every referrer the script names.
- Use `dest` plus `as` for private supporting material.
- Call public skills as `nt-vendor:<name>`.
- Never infer a license.

Rules: [.claude/rules/vendored-skills.md](.claude/rules/vendored-skills.md),
[.claude/rules/portable-shell.md](.claude/rules/portable-shell.md).
