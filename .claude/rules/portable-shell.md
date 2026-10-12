---
paths:
  - "plugins/**/*.md"
  - "scripts/*.mjs"
---

# Portable shell

Every command runs on macOS, Linux, and Git Bash. Check with
`node scripts/check-portable.mjs`.

- Write POSIX/MSYS only. Annotate any platform-specific line.
- Never use `pbcopy`, `pbpaste`, `osascript`, `brew`, `gtimeout`, `stat`, `sed -i ''`, or
  `readlink -f`.
- Call `mktemp` bare.
- Never hardcode a machine-absolute path. Derive it from `$PWD`, `$HOME`, the repo root,
  or `${CLAUDE_PLUGIN_ROOT}`.
- Match Claude project dirs by trailing repo name, then verify the recorded `cwd`.
- Key JavaScript manifests with `/`, never the platform separator.
- Name every dependency outside the shell. `jq` is not everywhere.
