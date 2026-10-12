---
paths:
  - "plugins/nt-vendor/**"
  - "plugins/nt-voice/skills/human-voice/**"
  - "vendor/**"
  - "scripts/vendor-skills.mjs"
---

# Vendored skills

- Never hand-edit `vendor/pristine/`, `vendor/NOTICE.md`, or a manifest `sha` or `files`.
- Add the manifest source, pin, path, and license, then run
  `node scripts/vendor-skills.mjs pull <name>`.
- Pull one named skill at a time.
- Give a gist `gist`, `owner`, and `entry`.
- Mark a missing license `unstated`.
- Vendor whole directories.
- Audit every referrer that `check` or `pull` names.
- Give a single-reader source `dest` plus `as`.
- Reference public skills as `nt-vendor:<name>`.
- Reference supporting material by relative path.
- Leave upstream bare sibling calls as they are; wrap them locally when needed.
