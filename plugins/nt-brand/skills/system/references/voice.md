# Voice and copy audit

Write from `doctrine/SOUL.md` (what we believe) and `doctrine/CULTURE.md` (how
we work). Run `/nt-voice:human-voice` on anything clients or strangers see.

## Golden set

Pick and combine these lines; write new copy in their register. The site owns
where each one lives.

- `NoTambourine · a boutique AI-native engineering agency`, or under the
  wordmark the eyebrow `Boutique AI-native engineering agency`
- `Engineering measured in results, not hours.`
- `We earn continued work with results, not dependency.`
- `Improve the systems that run your business.`
- `Senior engineers inside your team to lead delivery.`
- `Platform migrations, redesigns, site speed, and ongoing engineering.`
- `Launch a product, automate routine work, or connect systems and data.`
- `We plan each project around the business result it should produce.`
- `After our most recent redesign launched, mobile add-to-cart rose 38% and conversion 17%.`
- `Start a conversation`, linked to https://notambourine.com/tom
- The headings in `doctrine/SOUL.md`

## Facts

- `Tom Fuertes · Principal · NoTambourine`: 20 years of organizational-change
  experience across more than 250 engagements.
- Private-equity experience: mention only when relevant.
- Never publish a client list, a named case study, rates, margins, fixed offers,
  deal terms, or scope guarantees. References and terms come through a
  conversation.
- Draw proof from the white-labelled [case studies](case-studies/README.md).

## Rules

- Site copy says "you". A client deliverable's "we" is the client's organization
  with us inside it. A proposal or SOW names the parties. Never write "I".
- Back claims with client numbers, shared with permission. For an unnamed
  client, state the metric, the comparison, and the measurement window.
- Say "platform", not a vendor, unless the reader runs on it.
- Describe constraints without blaming whoever built the system.
- Sentence case; uppercase only for pink eyebrows and deck sublabels. ASCII
  punctuation; the interpunct separates name, role, and company.

## Names

- `NoTambourine` in every human-facing sentence.
- `notambourine` only in a path, URL, domain, GitHub org, npm name, or CSS
  class.
- `NoTambourine LLC` at most twice per contract: the signature block and one
  Definitions anchor.
- Never `Notambourine`, `No Tambourine`, any split form, or wordplay on the
  instrument.

```sh
rg -n 'notambourine|Notambourine|[Nn]o\s+[Tt]ambourine|NoTambourine LLC' <file>
```
