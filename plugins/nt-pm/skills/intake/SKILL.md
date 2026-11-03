---
name: intake
description: Gather client context, confirm the connectors it needs, and settle the output target before client work. Use when starting any client deliverable, ticket update, recap, or share, or when another client skill needs context.
---

# Intake

Every other client skill runs this first. It returns a context bundle and writes only to
the client context file.

1. Load the client context per [../../client-config.md](../../client-config.md). Name the
   client when more than one could match. None exists: offer to seed one before going on.
2. Check connectors. Each source the context enables needs a connector tool in this
   session: Slack always, plus Granola, Google Drive, Gmail, Google Calendar, GitHub, and
   Asana when enabled. List every missing one by name and stop. Never skip a source
   silently.
3. Settle the output target, in this order: the invoking prompt ("Slack response", "deck",
   "PDF", "issues"), then `outputs.<phase>`, then `outputs.default`. Still ambiguous in an
   interactive session: ask once, offering the context's targets (AskUserQuestion where
   available). Unattended: use `outputs.default`.
4. Collect, newest first, scoped to the client's `domains` and channels:
   - Slack internal: team threads, open questions, and decisions in progress.
   - Slack external: client asks, approvals, and what the client already knows.
   - Granola: notes from the client's recent calls.
   - Drive: recently changed docs in `sources.drive`.
   - Gmail: only with `sources.email: true`; threads with the client's domains.
   - GitHub: open issues and PRs in `sources.github`.
   - Asana: open and recently changed tickets, plus the board's stages and guide.
   - The body's context map, and the last `follow-up` output, found by its ledger key.
5. Write back. Add each new place that held context to the context map, and any tracker
   stage or convention learned to the body.

Return the client name, the target, any missing context the user must supply, and a terse
source digest with links. Never quote email or Slack verbatim in client-facing output.
