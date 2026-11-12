---
name: install-anti-slop
description: Install and configure the anti-slop Oxlint plugin in a local TypeScript or JavaScript repository. Use whenever a user asks to add anti-slop lint rules, copy the anti-slop plugin, configure opinionated Oxlint rules, or migrate an existing local anti-slop setup.
disable-model-invocation: true
---
<!-- vendored: dmmulroy/anti-slop@446268e skills/install-anti-slop (MIT). -->

# Install anti-slop

Copy the bundled Oxlint plugin into the current repository and add it to the existing
lint setup.

1. Inspect the repository first. Read its agent instructions, check `git status` so you
   preserve unrelated work, and find the package manager, the Oxlint config, and any
   existing copy of anti-slop.

2. Copy the plugin. Run this from the target repository:

   ```bash
   node <skill-directory>/scripts/install.mjs [relative-destination]
   ```

   The default destination is `tools/oxlint/anti-slop/`. The script refuses to replace an
   existing destination. Compare the two copies first, and pass `--force` only after
   backing up and reviewing the existing files.

3. Install the dependencies. Query the current versions of `oxlint` and
   `@oxlint/plugins`, and install the same version of both as development dependencies
   with the repository's package manager.

4. Register the plugin. Merge these fields into the existing config and keep every entry
   already there:

   ```ts
   ignorePatterns: [
     ".agent/**", ".agents/**", ".claude/**", ".codex/**", ".continue/**",
     ".cursor/**", ".gemini/**", ".opencode/**", ".pi/**", ".roo/**",
     ".windsurf/**", "tools/oxlint/anti-slop/**",
   ],
   jsPlugins: [{ name: "anti-slop", specifier: "./tools/oxlint/anti-slop/index.ts" }],
   ```

   Add any other agent-tool directories the repository has. Never ignore every
   dot-directory, because some hold owned source. For Vite+, merge into
   `lint.ignorePatterns`, `lint.jsPlugins`, and `fmt.ignorePatterns`.

   Enable every bundled `anti-slop/*` rule at `error`.

5. Run the repository's lint and typecheck, or the full `vp check` for Vite+. Report
   findings in owned source, and fix them only if the user asked for a migration or
   cleanup. Never weaken a rule, suppress an error, add an unsafe cast, or rewrite types
   only to make lint pass.

6. Report the destination, the versions installed, the config changes, the checks run,
   and any findings that remain.

When replacing an older local copy, compare its rules and diagnostics before
overwriting, and keep project-specific rules in their own plugin. To resolve findings,
prefer inference, `as const`, `satisfies`, named contracts, and parsing at the boundary.
