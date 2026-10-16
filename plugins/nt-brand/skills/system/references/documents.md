# Document guidance

Use this for any PDF that is not a slide deck: a contract, a statement of work,
a proposal, a report. Write plain Markdown and let `prose.css` give it
structure; the visual rules list what each Markdown shape becomes.

## Render

Open the Markdown with front matter naming the document and its ID:

```yaml
---
pagetitle: NoTambourine · Client (SOW 2)
ref: NTB-CLI-SOW2
---
```

Wrap the Markdown with the pandoc template and the self-contained sheet, then
print it with Chrome:

```bash
KIT=node_modules/@notambourine/brand-kit
pandoc doc.md -f gfm+yaml_metadata_block -s --embed-resources \
  --template $KIT/doc-template.html --css $KIT/doc-standalone.css -o doc.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
  --no-pdf-header-footer --print-to-pdf=doc.pdf doc.html
```

- `ref` prints in every page's footer beside the page number. Build it as
  `NTB-<client code>-<document><number>` and use the same string for the
  filename and the DocuSign envelope, so a citation finds all three.
- `-f gfm` keeps a lone image a paragraph rather than a `<figure>` and turns a
  trailing `\` into the break a stat card needs.
- `doc-standalone.css` carries the faces, tokens, and lockup as data URIs, so
  `doc.html` is also a single file to attach. It is built from `prose.css` and
  `print.css`; correct the sources, never the build.
- The page box, margins, page numbers, light theme, and lockup come from the
  sheet. Never add a document-local `<style>` or print flags for them.
- Chrome may refuse to launch in a sandboxed agent shell; rerun the print
  unsandboxed.

## Content

- Title the H1 with both parties, so the client can place it among their
  vendors, and the document's short name in pink:
  `NoTambourine · Client (*SOW 2*)`. That is the H1's only pink; section heads
  and bullets print pink on their own, so never emphasize inside an H2. Leave
  the parties out of the body once the title names them.
- Make the paragraph under the H1 the purpose; it prints as the lede. Put
  references in a plain paragraph after it.
- Use H2 for each section a reader will look for and H3 for the clauses under
  it. A wall of bold paragraphs prints flat.
- Put fees and dates in a table and right-align money columns with `---:`. Put
  figures worth seeing first in stat cards.
- Sign in a table: a header row of the parties, a `Name` row, then `Signature`
  and `Date` rows with every cell after the label left empty. Empty rows print
  as signing lines; never type underscores.
- Follow the voice rules for anything a client signs or reads.
