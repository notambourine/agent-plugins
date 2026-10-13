# Deck guidance

Start from `examples/deck.md`. It uses every slide shape below and renders as
is.

Explain the client's system with typographic concept diagrams built from brand
tokens. Do not substitute photography or icons for a chart.

Use this slide grammar: numbered eyebrow, lowercase display headline with one
emphasized word, short body or concept diagram, source sublabel, running footer.
Use `.eyebrow` for both labels and write them in sentence case. The theme
uppercases the first in pink and turns a later one into a muted source note
pinned above the footer. Content slides anchor to the top so headlines hold
their position; only the cover, dividers, and quotes center.

## Render

Export a PDF, standalone HTML, or PPTX with marp-cli and the self-contained
theme:

```bash
npx @marp-team/marp-cli@4.5.1 deck.md --pdf --html --allow-local-files \
  --theme-set node_modules/@notambourine/brand-kit/deck-standalone.css
```

- `deck-standalone.css` carries the faces, every token, and the lockup as data
  URIs, so the file renders with nothing beside it. It is built from `deck.css`;
  correct the source, never the build.
- `--html` lets the `.eyebrow` paragraphs through. `--allow-local-files` loads
  images by relative path.
- marp-cli drives Chrome. A sandboxed agent shell may refuse to launch it; rerun
  the export unsandboxed.
- Marp renders every newline inside a paragraph as a line break. Keep each
  paragraph and bullet on one line, and set Prettier's `proseWrap: preserve` for
  deck files.

On a web page, feed the Markdown through Marpit with `deck.css`, and load
`tokens.css` on the containing page. The theme reads the document root; its
color fallbacks do not provide font faces or logo data. Do not mistake a deck
that renders for one whose assets loaded.

## Structure

Front matter sets `marp: true`, `theme: nt`, `paginate: true`, and a `footer:`
naming the client by sector and the deck's subject. Separate slides with `---`.
Select a shape with `<!-- _class: name -->`.

| Shape  | Class     | Source                                                     |
| ------ | --------- | ---------------------------------------------------------- |
| Cover  | `lead`    | Eyebrow, H1, one-line purpose, date sublabel. Once a deck. |
| Agenda | none      | H2 plus an ordered list of three to five decisions.        |
| Break  | `divider` | Numbered eyebrow and an H1 naming the section.             |
| Point  | none      | Eyebrow, H2, at most two sentences or five bullets.        |
| Stats  | `stats`   | Two to four bullets, each `**figure**` then the label.     |
| List   | `split`   | Five to six short bullets in two columns.                  |
| Table  | none      | A comparison of at most five rows, sourced in a sublabel.  |
| Quote  | `quote`   | One blockquote; an italic last line is the attribution.    |
| Visual | none      | `![bg right:40% contain](path)` beside an eyebrow and H2.  |
| Figure | none      | An image alone in its paragraph; an italic line captions.  |
| Close  | none      | The decisions or asks, then one link.                      |

Never add a deck-local `<style>` block or hand-picked brand values. Shared decks
are immutable artifacts, so embedded overrides cannot receive later brand
corrections. Ask for a theme class here instead.

For print, set `class: theme-light` in the front matter. A `_class` directive
replaces the global class, so write `_class: lead theme-light` on that deck's
cover.

## Content

- Make each headline the slide's takeaway, not its topic.
- Pull numbers from the source with their comparison and measurement window, and
  put the source in the sublabel. Follow the voice rules for anything a client
  sees.
- Use real images only: client screenshots, charts exported from the data, or
  kit artwork. Ask for an asset rather than substituting stock or generated
  imagery. Reference them relative to the deck file.

Keep the running lockup so an exported PDF identifies itself. A full-bleed
`![bg]` slide hides corner furniture, including that lockup; account for the
loss when choosing that layout. Never retype the brand name in display type.
