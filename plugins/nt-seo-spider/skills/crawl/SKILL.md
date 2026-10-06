---
name: crawl
description: Crawl a site with Screaming Frog, using the MCP for reports and the headless CLI for PageSpeed, then turn the output into findings a repo can act on. Sizes each crawl to its task, audits crawl scope before quoting numbers, measures Core Web Vitals across a URL set, and separates the repo's own defects from a third party's. Trigger on "run an SEO crawl", "audit the site", "what's Screaming Frog saying", "check redirects", "run pagespeed on <section>", "check our structured data", "why isn't this page eligible for rich results", or any request that starts from crawl output.
---

# SEO crawls with Screaming Frog

## Read the site supplement first

If the repo has `.claude/refs/nt-seo-spider.md`, read it before anything else. It holds the
site-specific facts this skill leaves out: the domain, sitemap URLs, which paths this repo serves,
where the SEO source lives, and site rules. Where it conflicts with this skill, it wins.

Without the supplement, a crawl report fails silently in two ways. The crawl may have seen a third
of the site without saying so, and many of the failures may come from a platform this repo doesn't
ship. Settle scope and ownership before writing any finding.

## Match the crawl's weight to the task

Two switches set a run's cost, and neither shows in the command line:

- **PageSpeed auto-connect** is an app setting, `PSI.auto_connect` in
  `~/.ScreamingFrogSEOSpider/spider.config`. When it is `true`, every run, headless or MCP, queues
  every HTML URL for local Lighthouse at about 3s each, `--use-pagespeed` or not. No
  `.seospiderconfig` overrides it.
- **Rendering mode** is spider config. The default is Text Only (`mCrawlerMode=STANDARD` in the
  log). `JAVASCRIPT` drives headless Chromium per page. `mCrawlJavaScript=true` only fetches JS files
  and costs nothing extra.

Pick the lightest mode that answers the question:

| Task | Seed | Mode | Cost |
| --- | --- | --- | --- |
| Redirects, 404s, status codes, canonicals, titles, meta, robots, sitemap hygiene | `--crawl-sitemap` or a `--crawl` spider | defaults, PageSpeed off | ~1 min |
| Structured data, rich-result eligibility | `--crawl-sitemap` of the section | `schema.seospiderconfig`, PageSpeed off | ~1 min |
| Scope audit, client-rendered listings, "is it in the hydrated DOM" | `--crawl` | `render.seospiderconfig`, PageSpeed off | ~5-10 min |
| Core Web Vitals | `--crawl-sitemap` of **one** section, never the site | defaults + `--use-pagespeed` | ~3s per URL |

**Before launching**, grep `spider.config` for `PSI.auto_connect`. If it's `true` and the task isn't
Core Web Vitals, stop and ask the user to disconnect PageSpeed under Configuration -> API Access and
untick its connect-on-start option. `--use-pagespeed` connects it for the runs that need it.

Before a render or PageSpeed run over 200 URLs, state the URL count and estimated time and get a go-ahead.

**About ten seconds in**, grep `run.log` for `mCrawlerMode=` and `Connected to PageSpeed`. If either
is heavier than the mode needs, kill the run. Don't wait it out: exports are written only after the
PageSpeed queue drains, so a killed or abandoned run leaves no CSVs.

**Done means the CSVs exist in the output folder.** It doesn't mean the spider hit 100%. A PSI run
then spends most of its time in `SpiderActiveAwaitingApiState`.

### Saved configs

`sf_crawl` takes only url, name, project, and config_path. Without a config, a run uses the user's
saved default, or factory defaults if there is none (`No user default config` in the log). Never
change the default to suit one task, because the next task inherits it. Pass a mode config with
`--config` or `config_path` from `${CLAUDE_PLUGIN_ROOT}/skills/crawl/configs/`, or from the directory
the site supplement names.

A `.seospiderconfig` is a Java-serialized binary, so never write or patch one by hand. Each one is
made in the GUI from factory defaults (File -> Config -> Clear Default Config), with one change, then
File -> Config -> Save As. If the one you need is missing, ask the user to make it:

- `schema`: Configuration -> Spider -> Extraction -> JSON-LD + Schema.org + Google rich results.
  Without it, `structured_data_all.csv` has zero types on every row.
- `render`: Configuration -> Spider -> Rendering -> JavaScript.

Both also check Configuration -> Spider -> Crawl -> **Crawl Linked XML Sitemaps**, so a spidered
run's coverage can be audited. A run on factory defaults doesn't read sitemaps.

Crawls run with different configs measure different things. Don't compare their numbers.

## Audit the scope before you trust a single number

A crawl reports confidently on whatever it reached. Nothing in the output says what it missed, so
every issue count is really a count among the pages this config could see. Run these four checks
before quoting any figure. A sitemap-seeded run skips them: its coverage is complete by construction.

**1. Elapsed time, from the `Crawl Overview` header.** Divide by URL count. Under roughly 50ms per
URL means JavaScript rendering was off, because a headless render cannot run that fast.

**2. The `Sitemaps` block of `Crawl Overview`.** `URLs in Sitemap: 0` doesn't mean the site has no
sitemap. It means the crawl never read one, so every sitemap-derived figure below it is also 0 and
meaningless. Fix the config instead of interpreting the zero.

**3. Crawled pages against the sitemap.** This is the real coverage number:

```sh
curl -s $SITE/robots.txt | grep -i sitemap          # find the index; often not sitemap.xml
curl -s $SITE/<sitemap-index> | grep -o '<loc>[^<]*' | sed 's/<loc>//'   # then each child
```

Export `Internal` / `HTML` with `Address`, normalise trailing slashes on both sides, and `comm`
them. Group the misses by first path segment. If a whole segment is missing, look for one cause.

**4. The crawl-depth histogram.** Export `Internal` / `HTML` with `Crawl Depth` and count by depth.
A real crawl tapers. A **cliff**, many pages at the deepest level and none beyond, means
`Limit Search Depth` truncated it. Confirm the queue drained (`waiting: 0` in `sf_crawl_progress`)
and the crawl didn't stop at a URL cap.

| Signature | Cause | Effect |
| --- | --- | --- |
| Depth histogram cliffs with a large deepest bucket | `Limit Search Depth` is set | Everything past that hop is invisible |
| `URLs in Sitemap: 0` | Crawl Linked XML Sitemaps is off | Only link-reachable pages are seen |
| Elapsed time implausibly low; a segment missing wholesale | JS rendering off | Any client-rendered listing is a dead end |

The last one compounds the others. If an index page ships an app shell, its links don't exist in
raw HTML, and the crawler can't reach anything behind it at any depth. Check with
`curl -sL $URL | grep -c 'href="/<segment>/'` before blaming depth.

## Core Web Vitals: the headless CLI, not the MCP

`sf_crawl` can't request PageSpeed. Only the CLI's `--use-pagespeed` can, so a performance question
needs a second, headless process. It runs alongside an open GUI. On macOS the launcher is
`/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher`. On
Windows and Linux it is `ScreamingFrogSEOSpiderCli` in the install directory.

```sh
OUT=~/screaming-frog/<section>-psi-<yyyymmdd>
mkdir -p "$OUT"
"$SF_LAUNCHER" --headless \
  --crawl-sitemap $SITE/<section-sitemap>.xml --use-pagespeed \
  --project-name <site> --task-name <section>-psi-<yyyymmdd> --save-crawl \
  --output-folder "$OUT" --overwrite --export-format csv \
  --export-tabs "Internal:All,PageSpeed:All,Response Codes:All,Structured Data:All" \
  --save-report "Crawl Overview,PageSpeed:PageSpeed Opportunities Summary" \
  > "$OUT/run.log" 2>&1
```

- **`PSI.datasource=LOCAL`** in the log means the bundled Lighthouse ran locally, with no API key or
  quota. Confirm the line. The keyless PSI API quota is routinely exhausted.
- **Mobile emulation, Slow-4G, 4x CPU throttle.** Every millisecond is that lab profile. A 9s lab
  LCP can be a 0.5s real one. Say which you are quoting.
- **`Core Web Vitals Assessment` is blank on every row.** That column is CrUX field data, which
  LOCAL can't fetch. A blank there means nothing.
- **Progress.** The `mUrlsResponded=` counter stops updating once the spider completes. Poll for
  the CSVs.
- **Saved crawls land in DB storage.** Open them from File -> Crawls..., not "Open Recent".

Start with `pagespeed_opportunities_summary.csv`. In `pagespeed_all.csv` the columns that carry the
story are `Performance Score`, `Largest Contentful Paint Time (ms)`,
`First Contentful Paint Time (ms)`, `LCP Request Discovery`, `JavaScript Size (Bytes)`,
`Third Party Size (Bytes)`, `Reduce Unused JavaScript Savings (Bytes)`, and
`Improve Image Delivery Savings (Bytes)`.

### Reading an LCP result

Subtract FCP from LCP. A small gap means the whole page is slow and the fix is payload. A large gap
means the LCP element arrives late and the fix is discovery. Group by page type before quoting a
median; a site-wide p50 hides each template's behaviour.

`LCP Request Discovery` counts failed checks without naming them. It runs three: the element is in
the initial HTML, it isn't lazy-loaded, and it has `fetchpriority="high"`. Rule out the first two
against the served HTML; whichever check is left is the failure.

On Next.js sites, `priority` doesn't set `fetchpriority`. It only preloads and disables lazy
loading, so pass `fetchPriority="high"` explicitly on any LCP candidate. Two `priority` images for
one photo, hidden from each other by CSS, cost two downloads: CSS doesn't suppress a preload.

## The three data shapes

| Tool | What it is | Reach for it when |
| --- | --- | --- |
| `sf_generate_report` | 61 pre-baked cross-cutting analyses | The question spans URLs: chains, reciprocity, rich-result eligibility, totals |
| `sf_export_seo_element_urls` | The UI's tab and filter grid | "Give me the URLs where X", where X is a filter in a tab |
| `sf_generate_bulk_export` | Edges and raw content | "What links to the broken thing", or "dump the rendered HTML" |

Mnemonic: **report = the analysis, element export = the tab, bulk export = the edges.**

## Entry points, in order

0. **Scope audit, above.** A count from an unaudited crawl is a lower bound.
1. **`Crawl Overview`**: inventory, content types, indexable vs not.
2. **`Issues Overview`**: the triage table, with priority, URL count, and a How-To-Fix per row. Start
   here; it names which other report is worth running.
3. Drill into whatever Issues Overview ranked High.
4. **Trace each candidate to a source file** before it becomes a finding.

## Question to call

### Structured data
| Question | Call |
| --- | --- |
| Which rich-result types do we qualify for? | report `Structured Data:Google Rich Results Features Summary` |
| Which property fails, on how many URLs? | report `Structured Data:Validation Errors & Warnings Summary` |
| The failing URLs themselves | report `Structured Data:Validation Errors & Warnings` |
| Malformed JSON-LD, not merely invalid | report `Structured Data:Parse Errors` |
| Pages with no structured data | element `Structured Data`, filter `Missing` |

Summary first, per-URL second. Google's rich-result rules are stricter than schema.org validity.
`Course.description`, for example, must be 60 characters or fewer, so a Course graph needs its own
short field rather than reused page prose.

### Crawlability and delivery
| Question | Call |
| --- | --- |
| What's 404ing, and what links to it? | bulk `Response Codes:Internal:Internal Client Error (4xx) Inlinks` |
| Where are the redirect hops? | report `Redirects:Redirect Chains` |
| What links to each redirect? | bulk `Response Codes:Internal:Internal Redirection (3xx) Inlinks` |
| What is robots.txt blocking? | element `Response Codes`, filter `Blocked by Robots.txt` |
| What did we noindex? | element `Directives`, filter `Noindex` |
| Non-indexable pages in the sitemap | bulk `Sitemaps:Non-Indexable URLs in Sitemap Inlinks` |
| Pages nothing links to | report `Orphan Pages` |

### Performance
| Question | Call |
| --- | --- |
| How fast is a section, and what's the biggest lever? | headless `--use-pagespeed` run, then `pagespeed_opportunities_summary.csv` |
| Why is LCP slow? | `pagespeed_all.csv`, LCP minus FCP, then `LCP Request Discovery` |
| Which page carries an outsized asset? | `pagespeed_all.csv` sorted by `Improve Image Delivery Savings (Bytes)` |
| What is the LCP element? | chrome-devtools MCP: a `largest-contentful-paint` PerformanceObserver with `buffered: true` |

Only the last one names the LCP element. It measures unthrottled desktop, so use it to identify the
element, not to time it.

### Content and answerability
| Question | Call |
| --- | --- |
| Is the answer text in the served HTML? | bulk `Web:All Page Text`, then grep |
| What did the renderer produce? | bulk `Web:All Page Source` |
| Thin pages | element `Content`, filter `Low Content Pages` |
| Near-duplicate bodies | bulk `Content:Near Duplicates` |

## Mechanics that will bite you

- **The desktop app must be open and idle** for the MCP. Otherwise every tool throws
  `IllegalStateException: Tool cannot be called currently`, which means app state, not bad
  arguments. The headless CLI runs alongside the GUI.
- **Load a crawl before any report.** `sf_list_crawls`, then `sf_load_crawl <id>`.
- **Output dirs aren't created for you.** `file_path` is relative to `sf_list_allowed_base_directory`;
  run `sf_create_directory` first or get `NoSuchFileException`.
- **During a crawl only `sf_crawl_progress` responds.** Crawl, poll, then export.
- **Pass `export_type: "CSV"`.** The default NDJSON arrives as one giant line.
- **`sf_list_available_bulk_exports` overflows the token limit.** Call it once and keep the list.
- **Always write to `file_path`.** Inline content burns context; slice the file with shell.

## Reporting the result

Write findings in three buckets, in order:

1. **Confirmed ours, traced to a file.** The URL is served by this repo, and you can name the file
   and line that emits the defect. Only these are actionable in a PR.
2. **Real, but untraced.** Say which system you haven't ruled out and the check that would settle it.
3. **Untriaged report rows.** Straight from `Issues Overview`, labelled as uninvestigated.

Lead every set of counts with the coverage figure ("238 of 727 sitemap URLs, 33%") and call the
counts lower bounds. A sitemap-seeded run says "117 of 117" and moves on. Label every timing as lab
or field.
