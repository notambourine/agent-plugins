# Recap output contract

`shipped` and `weekly-recap` share this contract. Each skill sets its header line, section
names, and section emoji. Everything below is fixed.

Draft only. Hand the draft to the user; never post it.

## Slack mrkdwn, not markdown

The reader pastes into Slack, which strips markdown. Write mrkdwn:

- Bold with `*one asterisk*`. `**two**` pastes as literal asterisks.
- Italicize with `_underscores_`.
- Start bullets with a literal `•`. Never `-` or `*`.
- Skip headings, tables, links, and fenced blocks. Slack drops them.

Return the block as bare text. A fence makes the reader copy markup instead of the
message.

## Bullets

```text
• *Label:* Outcome in one short sentence.
```

The label is a bold one- or two-word noun for the surface that changed, then a colon. The
sentence states the result for the reader, not the mechanism. When a measured result
exists, give the metric, the comparison, and the window.

## Sections

Bold the header line and each section header with single asterisks. Put bullets on the
line right under their header. Leave one blank line under the header line and one between
sections. Drop empty sections. Use exactly the skill's emoji, in the skill's order.

## Compression

One bullet per theme, never per commit or PR. The block fits one Slack screen. Skip bots,
imports, dependency bumps, and docs that change nothing for the reader.

## Vocabulary

Common shorthand is fine: 9s, 404, RSS, zip. Leave out PRs, hashes, branches, files,
functions, database internals, implementation jargon, attribution, people's names, stock
openings, inflated adjectives, and rhetorical framing. White-label clients per the
nt-brand case-study rules: sector and shape, never a name, domain, or identifying detail.

## Fallbacks

Without `gh`, fall back to git and say so. Apply later wording edits to the whole block.
