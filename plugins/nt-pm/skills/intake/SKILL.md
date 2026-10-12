---
name: intake
description: Gather client context, confirm the connectors it needs, and settle the output target before client work. Use when starting any client deliverable, or when another client skill needs context.
---

# Intake

Every other client skill runs this first. Return a context bundle; write nothing.

1. Load the client config per [../../client-config.md](../../client-config.md). Name the client when more
   than one could match.
2. Check connectors. Each enabled source in the config needs a connector tool in this
   session: Slack always; Granola, Google Drive, Gmail, Google Calendar, and GitHub when
   enabled. List every missing one by name and stop. Never skip a source silently.
3. Settle the output target, in order: the invoking prompt ("Slack response", "deck",
   "PDF", "issues"), then `outputs.<phase>`, then `outputs.default`. Still ambiguous in an
   interactive session: ask once, offering the config's targets (AskUserQuestion where
   available). Unattended: use `outputs.default`.
4. Collect, newest first, scoped to the client's `domains` and channels:
   - Slack: recent threads in `sources.slack`.
   - Granola: notes from the client's recent calls.
   - Drive: recently changed docs in `sources.drive`.
   - Gmail: only with `sources.email: true`; threads with the client's domains.
   - GitHub: open issues and PRs in `sources.github`.
   - The last `follow-up` output for this client, found by its ledger key.

Return the client name, the target, missing context the user must supply, and a terse
source digest with links. Never quote email or Slack verbatim into client-facing output.
