---
name: crawl
description: Crawl a site with Screaming Frog and turn the output into findings a repo can act on. Sizes each crawl to its task, keeps PageSpeed off, audits crawl scope before quoting numbers, and separates the repo's own defects from a third party's. Trigger on "run an SEO crawl", "audit the site", "what's Screaming Frog saying", "check redirects", "check our structured data", "why isn't this page eligible for rich results", or any request that starts from crawl output.
---

# SEO crawls with Screaming Frog

## Read the site supplement first

If the repo has `.claude/refs/nt-seo-spider.md`, read it before anything else. It holds the
site-specific facts this skill leaves out: the domain, sitemap URLs, which paths this repo serves,
where the SEO source lives, and site rules. Where it conflicts with this skill, it wins.

Without the supplement, a crawl report fails silently in two ways. The crawl may have seen a third
of the site without saying so, and many of the failures may come from a platform this repo doesn't
ship. Settle scope and ownership before writing any finding.

## Pick the lightest tool

- **Under about 50 URLs**, skip Screaming Frog. A curl loop over the URLs answers status codes,
  redirect targets, headers, and canonicals faster than the app starts.
- **If the question sounds like a revisit** ("what did the last crawl say", a follow-up on earlier
  findings), ask whether to load a saved crawl (`sf_list_crawls`, `sf_load_crawl`) before recrawling.

## Never run PageSpeed

Local PageSpeed opens a headless Chrome per URL to run Lighthouse, about 3s each, and holds every
export until the queue drains. One redirect crawl queued 1,046 URLs and ran hot for most of an hour
answering a one-minute question. Never pass `--use-pagespeed`. Performance questions go to the
chrome-devtools MCP on the specific pages, not to a crawl.

**Before launching**, grep `~/.ScreamingFrogSEOSpider/spider.config` for `PSI.auto_connect`. If it's
`true`, every run queues Lighthouse regardless of flags, and no `.seospiderconfig` overrides it.
Stop and ask the user to disconnect PageSpeed under Configuration -> API Access and untick its
connect-on-start option.

## Match the crawl's weight to the task

Rendering mode is the remaining cost switch. The default is Text Only (`mCrawlerMode=STANDARD` in
the log). `RENDER` drives headless Chromium per page. `mCrawlJavaScript=true` only fetches JS files
and costs nothing extra.

| Task | Seed | Mode | Cost |
| --- | --- | --- | --- |
| Redirects, 404s, status codes, canonicals, titles, meta, robots, sitemap hygiene | `--crawl-sitemap` or a `--crawl` spider | `links.seospiderconfig` | ~1 min |
| Structured data, rich-result eligibility | `--crawl-sitemap` of the section | `schema.seospiderconfig` | ~1 min |
| Scope audit, client-rendered listings, "is it in the hydrated DOM" | `--crawl` | `render.seospiderconfig` | ~5-10 min |

Before a render run over 200 URLs, state the URL count and estimated time and get a go-ahead.

**About ten seconds in**, grep `run.log` for `mCrawlerMode=` and `Connected to PageSpeed`. If the
mode is heavier than the task needs, or PageSpeed connected at all, kill the run.

**Done means the CSVs exist in the output folder.** Exports are written at the very end, so a
killed run leaves none.

### Running headless

The CLI runs alongside an open GUI, and only the CLI can seed from a sitemap. On macOS the launcher
is `/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher`. On
Windows and Linux it is `ScreamingFrogSEOSpiderCli` in the install directory.

```sh
OUT=~/screaming-frog/<task>-<yyyymmdd>
mkdir -p "$OUT"
"$SF_LAUNCHER" --headless [--config <mode>.seospiderconfig] \
  --crawl-sitemap $SITE/<section-sitemap>.xml \
  --project-name <site> --task-name <task>-<yyyymmdd> --save-crawl \
  --output-folder "$OUT" --overwrite --export-format csv \
  --export-tabs "Internal:All,Response Codes:All" --save-report "Crawl Overview" \
  > "$OUT/run.log" 2>&1
```

Saved crawls land in DB storage. Open them from File -> Crawls..., not "Open Recent".

### Saved configs

`sf_crawl` takes only url, name, project, and config_path. Without a config, a run uses the user's
saved default, or factory defaults if there is none (`No user default config` in the log). Never
change the default to suit one task, because the next task inherits it. Pass a mode config with
`--config` or `config_path` from `${CLAUDE_PLUGIN_ROOT}/skills/crawl/configs/`, or from the directory
the site supplement names.

A `.seospiderconfig` is a Java-serialized binary, so never write or patch one by hand. To read one, run it headless against `$SITE/robots.txt` and grep the config dump in the log. Each one is
made in the GUI from factory defaults (Configuration -> Profiles -> Clear Default Config), with one change, then
Configuration -> Profiles -> Save As. If the one you need is missing, ask the user to make it:

- `schema`: Configuration -> Spider -> Extraction -> JSON-LD + Schema.org + Google rich results.
  Without it, `structured_data_all.csv` has zero types on every row.
- `render`: Configuration -> Spider -> Rendering -> JavaScript.
- `links`: Configuration -> Spider -> Crawl -> untick Images, CSS, JavaScript, SWF, and External Links.
  Status-code questions need only internal HTML.

All three also check Configuration -> Spider -> Crawl -> **Crawl Linked XML Sitemaps**, so a spidered
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
counts lower bounds. A sitemap-seeded run says "117 of 117" and moves on.
