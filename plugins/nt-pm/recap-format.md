# Recap output contract

`shipped` and `weekly-recap` share this contract. Each skill sets its own header line,
section names, and section emoji. The rest is fixed here.

Draft only. Hand the draft to the user and never post it.

## Slack mrkdwn

The reader pastes the draft into Slack, which uses mrkdwn and drops Markdown:

- Bold with `*one asterisk*`. `**two**` pastes as literal asterisks.
- Italicize with `_underscores_`.
- Start each bullet with a literal `•`, never `-` or `*`.
- Use no headings, tables, links, or fenced blocks.

Return the block as bare text. Inside a fence, the reader copies the fence along with the
message.

## BLUF

Put one plain line directly under the header line: the bottom line up front, the single
result the reader keeps if they read nothing else. It meets the same bar as any other
[claim](#claims).

## Bullets

```text
• *Label:* Outcome in one short sentence.
```

The label is a bold noun of one or two words for the surface that changed, followed by a
colon. The sentence says what changed for the reader and leaves out how it was built. When
a result was measured, give the metric, the comparison, and the window.

## Sections

Bold the header line and each section header with single asterisks. Put bullets on the
line directly under their header. Leave one blank line under the BLUF line and one between
sections. Drop empty sections. Use the skill's emoji exactly, in the skill's order.

## Claims

State what the sources show: merged, in early access, scheduled for a date. Write "live",
"launched", "faster", or "ready" only when a production merge backs it, or a metric with
its comparison and window. When a release state is unclear, ask before drafting. Every
headline option offered to the user must be true.

## Worked through

A skill with a 🧗 *Worked through* section uses this bullet:

```text
• *Label:* What was in the way. What we did. Where it stands.
```

Include an item only when it cost a day or more, moved a date or scope, or needs client
input. Keep at most three. Find them in PR Cause lines, reverts, reopened issues, and
follow-up blockers. Describe the difficulty in facts, with no adjectives about effort.
Name the constraint and never the person or team that built the system.

## Compression

Write one bullet per theme, never one per commit or PR. The whole block fits on one Slack
screen. Skip bots, imports, dependency bumps, and docs that change nothing for the reader.

## Vocabulary

Common shorthand such as 404, RSS, or zip is fine. Leave out PRs, hashes, branches, files,
functions, database internals, implementation jargon, attribution, people's names, stock
openings, inflated adjectives, rhetorical framing, and forecasts. White-label the client
per nt-brand's case-study rules: sector and shape, never a name, domain, or identifying
detail.

## Fallbacks

Without `gh`, fall back to git and say so. When the user edits wording later, apply the
edit across the whole block.
