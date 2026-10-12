---
paths:
  - "plugins/nt-brand/**"
  - "scripts/brand-kit.mjs"
  - "package.json"
---

# Brand mirror

- Treat `notambourine/brand-kit` as the golden source.
- Never hand-edit `plugins/nt-brand/skills/system/`.
- Fix upstream, release, pin the exact version, run `npm run brand:sync`.
- Sync the mirror on every Dependabot bump.
- Verify with `npm run brand`.
- Read the committed mirror at runtime, never `node_modules`.
- Publish new files upstream before they land here.
