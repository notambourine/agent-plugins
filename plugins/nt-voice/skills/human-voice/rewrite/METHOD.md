<!-- vendored: blader/humanizer@523374d . (MIT). -->

# Rewrite

Keep every claim, fact, name, number, date, quote, citation, identifier, and link target.
Add none that the source or the user did not supply. Preserve the information and feel
free to change the shape: compress dull parts, and merge or split paragraphs. If the
user gave a writing sample, match its habits, including its dashes. Otherwise match the
requested register. Add personality only where the genre has it, such as an essay or a
blog post. Technical, legal, and reference text should stay plain.

## Patterns to remove

Content:

1. Inflated significance ("stands as a testament", "a pivotal moment").
2. Claims of notability, or lists of media coverage with no context.
3. Trailing `-ing` phrases that add analysis with no content ("highlighting its role").
4. Promotional language.
5. Vague attribution ("experts say").
6. Formulaic "challenges" and "future outlook" sections.

Language:

7. AI vocabulary.
8. Avoiding "is" and "has" ("serves as", "boasts").
9. Negative parallelism ("not just X, but Y") and a trailing negation.
10. Lists forced to three items.
11. Cycling through synonyms for one thing.
12. False ranges ("from X to Y" where no scale exists).
13. Passive or subjectless phrasing.

Style:

14. Em and en dashes.
15. Bold on many phrases.
16. Lists whose items open with a bold inline header.
17. Title-case headings.
18. Decorative emoji.
19. Curly quotes.

Communication:

20. Chatbot artifacts ("I hope this helps").
21. Knowledge-cutoff disclaimers and speculation about missing information.
22. Flattery.

Filler and hedging:

23. Filler phrases.
24. Stacked hedges.
25. Generic upbeat conclusions.
26. Hyphens on compounds after the noun ("the tool is well-known").
27. Appeals to authority ("at its core", "the reality is").
28. Signposting ("Let's dive in", "Here's what you need to know").
29. A heading followed by a one-line restatement of it.
30. Narrating the edit ("the revised version now").
31. Manufactured punchlines and runs of short dramatic sentences.
32. Aphorism formulas.
33. Rhetorical question openers.

Look for clusters. One dash, one "however", or one short emphatic sentence is not a
tell. Do not rewrite a flagged phrase inside a quotation, a title, a proper name, or an
example that discusses the phrase.

## What to write instead

Use plain "is", "are", and "has", active sentences with a subject, specific nouns, the
same word for the same thing, sentence-case headings, straight quotes, and sentences of
varied length. Cut unsupported claims, padding, false balance, stock conclusions, and
offers to continue. Unless a writing sample uses them, the final text has no em or en
dash.

Leave these alone: specific and odd details, mixed feelings, asides and
self-corrections, deliberate voice, technical terms, hedges the facts require, lists
that really have three items, and formatting the destination requires.

## Modes

- **Pasted text:** deliver the draft, a short list of what still reads as generated,
  and the final version.
- **File:** run the loop internally and edit the prose in place. Leave code,
  frontmatter, data, and link targets untouched. Report a short summary.
- **Embedded in another task:** run the loop internally and return only the final text.

The loop: find the patterns, write a draft, and read it as if aloud. Ask what still
sounds generated and whether the draft states anything the source did not. Revise, then
scan for dashes.
