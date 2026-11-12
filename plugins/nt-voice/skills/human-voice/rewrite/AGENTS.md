# Agent rules

- `METHOD.md` is what runs. `README.md` covers install and lists the patterns.
- Keep the 33 pattern names and version `2.9.1` the same in the method, the README, and
  the manifest.
- Keep the frontmatter portable and the wording neutral across agent harnesses.
- Validate with `uv run scripts/validate-package.py`, `npx skills add . --list`, and
  `claude plugin validate .`.
- When a change fixes a behavior, add a short version note.
