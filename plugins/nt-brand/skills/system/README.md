# brand-kit

NoTambourine brand assets and guidance for design, decks, and copy. Use the
stylesheets, fonts, and logo together. Read `SKILL.md` for the relevant
guidance.

| Link this        | To get                                                                     |
| ---------------- | -------------------------------------------------------------------------- |
| `tokens.css`     | The whole system: the faces, every value, and styled bare HTML.            |
| `vars.css`       | The values alone, for a surface with its own faces and base layer.         |
| `components.css` | `.nt-btn`, `.nt-card`, `.nt-nav`, and the rest, all `var()`-based.         |
| `deck.css`       | The Marpit slide theme, 1280x720. Load `tokens.css` on the page too.       |
| `prose.css`      | `.nt-prose` for rendered markdown, on screen and on paper.                 |
| `logo/`          | The mark, the lockup, the icons, and the rasters cut from them.            |
| `doctrine/`      | What the firm believes and how the team works, as the site publishes them. |

## Logo

`scripts/build-logo.py` holds the mark's path data and the wordmark's type
parameters, and writes every file under `logo/`. It traces the wordmark out of
`fonts/nunito-latin-var.woff2`, so the outlines cannot drift from the face the
stylesheets load. Change the logo by editing that script and re-running it:

```bash
./scripts/build-logo.py    # needs rsvg-convert on PATH
```

The raster half shells out to `rsvg-convert`, which ships in librsvg:
`brew install librsvg` on macOS or Linux, the GTK runtime on Windows. The vector
half runs without it.

### Pick a file

- `lockup.svg` is the default: mark plus outlined wordmark, no font needed.
  `-white` goes on dark, pink, or a photo; `-ink` on one-color print or light
  backgrounds where pink lacks contrast.
- `monogram*` is the short form (avatar, app icon, stamp). `mark*` drops the
  letters for watermarks or anywhere `no` would read as a word.
- `favicon.svg` and `icon*.svg` cover browser tabs and app tiles, including iOS
  square and Android maskable. Use `favicon.svg` at 16px; the monogram's letters
  lose detail there.
- `lockup-text.svg` is for editing the type only. librsvg and resvg overrun its
  viewBox, so ship and rasterize `lockup.svg`.
- `logo/export/` is generated output: regenerate it, never retouch it.

### Wire it up

`logo/site.webmanifest` names its icons relative to itself, so it works wherever
`logo/` is served as a unit.

```html
<link rel="icon" href="/logo/favicon.svg" type="image/svg+xml" />
<link rel="icon" href="/logo/export/favicon.ico" sizes="32x32" />
<link rel="apple-touch-icon" href="/logo/export/apple-touch-icon.png" />
<link rel="manifest" href="/logo/site.webmanifest" />
```

## Consume it

Install the package and import its stylesheets from `node_modules`. Keep copied
assets tied to the installed version.

```bash
npm install @notambourine/brand-kit
```

There is no `exports` map, so import or copy any shipped path directly:

```js
import "@notambourine/brand-kit/tokens.css";
```

```bash
cp -R node_modules/@notambourine/brand-kit/{fonts,logo} public/
```

`tokens.css` declares the `@font-face` rules and every `var()` the other two
read, so load it first and serve `fonts/` beside it. The paths inside it are
relative to the CSS file, so inlining it into a `<style>` block breaks the
faces.

### With Tailwind or StyleX

A surface with its own faces and base layer imports `vars.css` alone and writes
`var()` against the semantic aliases. Neither system needs anything from this
kit beyond the custom properties.

```js
import "@notambourine/brand-kit/vars.css";

const styles = stylex.create({
  card: { backgroundColor: "var(--bg-card)", padding: "var(--sp-6)" },
});
```

Tailwind claims the `--font-*` and `--ease-*` namespaces for its own utilities,
which is why those two groups ship a `--nt-*` primitive under the alias: a
Tailwind surface reads the primitive. StyleX hashes the names it generates and
collides with neither.

Two StyleX-specific traps. Bridging through `stylex.defineVars` breaks
`.theme-light`, because StyleX declares those properties on `:root` and a custom
property resolves where it is declared, so a `.theme-light` subtree still
inherits the dark value; a raw `var()` string resolves at the element and themes
correctly. And StyleX outranks the element styles in `elements.css` only while
`useCSSLayers` is off - turn layers on and an unlayered `h1` wins, so import
into a layer StyleX orders itself against:

```css
@import "@notambourine/brand-kit/tokens.css" layer(base);
```

Pin an exact version and bump it on purpose; a caret range moves the brand under
a consumer with no diff to review.

## Gate a consumer

A `var(--x)` that reads a token this repo stopped declaring falls through to its
fallback and the page still renders, so a bump can go wrong quietly. Check three
things in the consumer's CI: the font bytes hash against `fonts/`, every color
is one this kit defines, and every `var()` reads a property it still declares.
`notambourine/share`'s `npm run brand` is the reference implementation.

## Release

Update `version` in `package.json` and the lockfile, then merge to main. The
publish workflow releases versions that are not already on npm and tags the
published commit. Formatting must pass before the package is packed or
published.

Publishing uses npm trusted publishing with provenance.

## License

MIT for the stylesheets and `SKILL.md`. The faces in `fonts/` are SIL Open Font
License; see `fonts/OFL.txt`.
