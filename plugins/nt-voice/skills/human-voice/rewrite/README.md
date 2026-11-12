# Humanizer

A portable Markdown skill, version `2.9.1`. It removes 33 patterns of AI writing while
keeping the facts and the author's voice, and it works on pasted text, on a file, or as a
step inside another task.

## Install

```bash
npx skills add blader/humanizer --global
npx skills update humanizer --global
npx skills add blader/humanizer --global --agent '*'
```

Omit `--global` to install into one project. In Claude Code:

```text
/plugin marketplace add blader/humanizer
/plugin install humanizer@humanizer
```

## Use

```text
/humanizer
[text]
```

Provide a writing sample to have the rewrite match your voice. Point to a file to edit
its prose in place.

The patterns: significance, notability, `-ing` tails, promotion, vague attribution,
formulaic sections, AI vocabulary, copula avoidance, negative parallelism, forced threes,
synonym cycling, false ranges, passive fragments, dashes, bold, inline headers, title
case, emoji, curly quotes, chatbot artifacts, cutoff disclaimers, flattery, filler,
hedging, generic conclusions, excess hyphens, authority tropes, signposting, fragmented
headers, diff narration, punchlines, aphorisms, rhetorical openers.

The list is based on
[Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
The license is MIT.
