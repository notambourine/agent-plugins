---
name: shipped
description: Draft plain-English Slack deploy notes for work about to ship or the last observed production push. Use for deploy previews and retrospective release summaries; drafts only, never deployed or posted by the agent.
disable-model-invocation: true
allowed-tools:
  - Bash(git fetch:*)
  - Bash(git reflog:*)
  - Bash(git rev-parse:*)
  - Bash(git rev-list:*)
  - Bash(git symbolic-ref:*)
  - Bash(git log:*)
  - Bash(git show:*)
  - Bash(git merge-base:*)
  - Bash(git remote:*)
  - Bash(gh pr list:*)
  - Bash(gh pr view:*)
  - Bash(gh issue view:*)
  - Bash(gh api:*)
  - Bash(date:*)
  - Bash(echo:*)
  - Bash(sed:*)
  - Bash(tr:*)
  - Bash(head:*)
---

# Deploy updates

Draft the note. Never deploy. Follow [../../recap-format.md](../../recap-format.md).

## Range

- Pre-deploy (default): remote default branch to the first of `dev`, `staging`, `develop`,
  `release`, else `HEAD`.
- Retrospective: previous to current observed tip in the remote default branch's reflog.
- An explicit range takes a reflog entry, SHA, tag, or date. A range named in the
  invocation is final.

Fetch `origin`; stop if it fails. Resolve the endpoints, short SHAs, dates, and commit
count, then write. Never ask the user to confirm the range.

- Zero commits: say nothing is pending or shipped.
- Empty retrospective reflog: ask for a range.
- No `origin`: ask for the deployment repo.

## Read the work

Read non-merge commits. Resolve each PR from its referenced number or SHA. Read the PR
body first, then linked issues and the diff stat when the body falls short. Drop work
already ancestral to the start. Word commits with no PR or issue behind them
conservatively. Fold related work together and collapse routine dependency and CI noise.

## Output

Return only:

```text
🚀 *Deploys: <window> (M/D/YY)*

✨ *Features*
• *Label:* Outcome in one short sentence.

🛠️ *Fixes*
• *Label:* Outcome in one short sentence.
```

The window uses the reader's terms: `Last N Days` for retrospective, `Pending` for
pre-deploy.

Keep labels and sentences neutral. Name the surface with a generic noun and state what it
does now. Never imply the old behavior was wrong or that someone erred: no comparatives or
corrective framing like `Smarter Search`, `Right Order`, `Finally`, or `No Longer Broken`.
Write `Search`, `Sort Order`.

Use these sections in this order, only the ones with bullets: ✨ Features, 🛠️ Fixes, ⚡
Performance, 📈 SEO & Marketing, 🗂️ Admin & Internal, ⚙️ Behind the Scenes.

When asked for a deck or PDF, also build one from
[../../examples/shipped.deck.md](../../examples/shipped.deck.md) per
[../../outputs.md](../../outputs.md#decks).
