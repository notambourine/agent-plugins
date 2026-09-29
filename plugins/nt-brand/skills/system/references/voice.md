# Voice and copy audit

Lead public pages and introductions with:

> Ship the systems your business needs next.

For existing systems, use:

> Improve the systems that run your business.

Follow with what we will deliver and what the client can do once it ships. Write
plainly and warmly. Use humor only when it makes the point clearer.

## Positioning and offers

Position NoTambourine as senior engineers who join the client's team, use AI
throughout delivery, and own the work from business goal to shipped system. Name
the software, data, or infrastructure needed to reach that goal. Keep the time
between a decision and working software short.

Treat AI as a working capability. Explain where it speeds up delivery, automates
work, improves a product, or helps a team use its information. Name the result,
not the novelty. Do not make broad claims about transformation or intelligence.

Show engineers working with product managers, operators, designers, and domain
experts. Credit clear priorities, sound decisions, and close coordination for
delivery speed. Never claim that eliminating a role, planning, documentation, or
meetings makes a team fast.

Define fit by the result and the responsibility we will take. Mention
private-equity experience when relevant, but keep general positioning open to
any ownership structure. The name means no padding.

Use this introduction:

> Ship the systems your business needs next. NoTambourine brings senior
> engineers into your team to own delivery and build with AI.

For a meta description or short directory listing, use:

> Senior engineers using AI inside your team to ship the systems your business
> needs next.

Give clear reasons to call: launching a product, improving a core system,
automating routine work, or connecting systems and data. Describe the shipped
change in daily terms. A file arrives automatically. An order moves between
systems. A team releases an update. A customer gets a useful answer. Support
claims about growth, time saved, reliability, or delivery speed with client
evidence.

Keep public positioning open to a new ambition or an existing constraint. Ask
what the client wants to accomplish, why now, and what will change after it
ships. In proposals, connect each constraint to its business consequence and the
work required.

Use these offer names:

- **Assessment:** Choose what to build or change next. Review the systems,
  workflows, and priorities, then set the delivery plan.
- **Embedded:** Add senior engineers who build with AI to your team. We own
  delivery and ship the systems your business needs next.

Use "Start a conversation" for the primary invitation. Ask what the reader wants
to ship and when. Discuss fit before asking them to choose an engagement.

## Register and evidence

- Address marketing readers as "you". In client deliverables, use "we" for the
  client's organization with us inside it. Name the parties in proposals and
  SOWs. Never use "I" as the author's voice.
- Keep sales material out of client deliverables. Explain the client's system,
  the decisions to make, and the work to ship.
- Show the objective, what shipped, and what the client can now do. Use client
  numbers when available. Otherwise use a verifiable before and after. Share
  client evidence only with permission.
- Name who joins and owns delivery. Promise direct access to that person. Cover
  our estimating mistakes within the agreed scope.
- Describe constraints without blaming the people who built the system.

## Names and mechanics

Use `NoTambourine` in human-facing sentences. Reserve `notambourine` for
technical slugs, paths, URLs, domains, GitHub organizations, npm names, and CSS
classes. Use `NoTambourine LLC` only in contracts, at most twice: one
Definitions anchor and the signature block. Reject `Notambourine` and
`No Tambourine`. Cite the public `AGENTS.md` for disputed naming flags.

Preserve `Senior engineers. No tambourine.` as a standalone signature: tagline,
slide, sign-off, or footer. The instrument is lowercase. This is the only
permitted spaced form.

Use sentence case for headlines, buttons, navigation, and labels. Reserve
uppercase for pink eyebrows; decks also use it for sublabels. Follow deck
guidance for lowercase display headlines. Vary sentence length. Cut
throat-clearing, superlatives, exclamation marks, and clever phrasing that
delays the point.

Use ASCII punctuation: hyphens and straight quotes/apostrophes. Do not use em/en
dashes, curly quotes, or single-character ellipses. The interpunct may separate
a name, role, and company: `Tom Fuertes · Principal · NoTambourine`.

## Audit before shipping

Audit anything clients or strangers see: pages, email, decks, proposals, SOWs,
READMEs, and release notes. Search for candidates, then judge them in context.

The opening should name the work and our responsibility. Remove assumed pain,
unearned urgency, decorative language, and claims that could describe any
agency. Keep technical constraints when they explain a decision or result.

```sh
rg -n 'notambourine|Notambourine|No\s+Tambourine|NoTambourine LLC' <file>
rg -n '[\x{2014}\x{2013}\x{2018}\x{2019}\x{201C}\x{201D}\x{2026}]' <file>
rg -ni '\b(proven|world-class|battle-tested|results-driven|cutting-edge|best-in-class|seamless|robust|leverage|synergy|holistic|bespoke)\b' <file>
rg -ni ',\s+(ensuring|enabling|allowing|helping|driving|empowering|delivering|providing)\b' <file>
rg -ni "this matters|it's worth noting|it is worth noting|needless to say|at the end of the day|in today's" <file>
rg -n '!(\s|$)|\bI\b' <file>
```

Check legal-name occurrences against the contract limit. Ignore technical slugs
and code when judging wordmark hits. Ignore literal technical uses such as "a
robust error path" and `I` in quotations, identifiers, or names.

Cut puffery and keep evidence. Replace claims of importance with the
consequence. Cut participle tails at the comma. Narrow grand claims to something
a client can verify. If a sentence keeps its meaning after a phrase is cut, cut
the phrase.

Keep three fixtures even when they match a search flag: the signature, factual
lines such as "Two engineers, six weeks, one shipped feature", and one pink
`<em>` in a headline.

Format source documents with the repository's pinned Prettier before sharing or
exporting them. Review the rendered document, especially slide breaks and
tables.
