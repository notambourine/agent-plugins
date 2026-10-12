---
name: crawl
description: Crawl a site with Screaming Frog and turn the output into findings a repo can act on. Sizes each crawl to its task, keeps PageSpeed off, audits crawl scope before quoting numbers, and separates the repo's own defects from a third party's. Trigger on "run an SEO crawl", "audit the site", "what's Screaming Frog saying", "check redirects", "check our structured data", "why isn't this page eligible for rich results", or any request that starts from crawl output.
---

# SEO crawls with Screaming Frog

A finding counts when it names coverage, an owner, and a source file. Everything below serves that.

## Read the site supplement

Read `.claude/refs/nt-seo-spider.md` first when the repo has one. It holds the domain, sitemap URLs,
the paths this repo serves, where SEO source lives, and site rules. It wins over this skill.

Without it, a report fails silently twice: the crawl may have reached a third of the site, and many
failures may come from a platform this repo doesn't ship. Settle scope and ownership before any
finding.

## Pick the lightest tool

- Under about 50 URLs, skip Screaming Frog. A curl loop answers status, redirect targets, headers,
  and canonicals before the app starts.
- A revisit ("what did the last crawl say") loads a saved crawl with `sf_list_crawls` and
  `sf_load_crawl`. Say so and do it unless the user wants fresh data.

## Keep PageSpeed off

Local PageSpeed runs Lighthouse in a headless Chrome per URL, about 3s each, and holds every export
until the queue drains. One redirect crawl queued 1,046 URLs and ran hot for most of an hour on a
one-minute question. Never pass `--use-pagespeed`. Send performance questions to the
chrome-devtools MCP on specific pages.

Before launch, grep `~/.ScreamingFrogSEOSpider/spider.config` for `PSI.auto_connect`. When it is
`true`, every run queues Lighthouse whatever the flags, and no `.seospiderconfig` overrides it. Stop.
Ask the user to disconnect PageSpeed under Configuration -> API Access and untick connect-on-start.

## Size the crawl to the task

Rendering mode is the remaining cost switch. Text Only is the default (`mCrawlerMode=STANDARD` in
the log). `RENDER` drives headless Chromium per page. `mCrawlJavaScript=true` only fetches JS files
and costs nothing.

| Task | Seed | Mode | Cost |
| --- | --- | --- | --- |
| Redirects, 404s, status codes, canonicals, titles, meta, robots, sitemap hygiene | `--crawl-sitemap` or a `--crawl` spider | `links.seospiderconfig` | ~1 min |
| Structured data, rich-result eligibility | `--crawl-sitemap` of the section | `schema.seospiderconfig` | ~1 min |
| Scope audit, client-rendered listings, "is it in the hydrated DOM" | `--crawl` | `render.seospiderconfig` | ~5-10 min |

A render run over 200 URLs needs a go-ahead. State the URL count and the estimated time first.

About ten seconds in, grep `run.log` for `mCrawlerMode=` and `Connected to PageSpeed`. Kill the run
if the mode is heavier than the task or PageSpeed connected.

The run is done when the CSVs exist in the output folder. Exports land at the very end; a killed run
leaves none.

### Run headless

The CLI runs beside an open GUI, and only the CLI seeds from a sitemap. The launcher is
`/Applications/Screaming Frog SEO Spider.app/Contents/MacOS/ScreamingFrogSEOSpiderLauncher` on macOS
and `ScreamingFrogSEOSpiderCli` in the install directory on Windows and Linux.

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

### Pass a mode config

`sf_crawl` takes only url, name, project, and config_path. With no config, a run uses the user's
saved default, which can hold anything. Never edit that default. Always pass a mode config, via
`--config` or `config_path`, from `${CLAUDE_PLUGIN_ROOT}/skills/crawl/configs/` or the directory the
site supplement names.

A `.seospiderconfig` is Java-serialized binary. Never write or patch one by hand. To read one, run it
headless against `$SITE/robots.txt` and grep the config dump in the log.

Each config starts from factory defaults (Configuration -> Profiles -> Clear Default Config), takes
one change, and saves with Configuration -> Profiles -> Save As. When one is missing, ask the user to
build it:

- `schema`: Configuration -> Spider -> Extraction -> JSON-LD + Schema.org + Google rich results.
  Without it, `structured_data_all.csv` shows zero types on every row.
- `render`: Configuration -> Spider -> Rendering -> JavaScript.
- `links`: Configuration -> Spider -> Crawl -> untick Images, CSS, JavaScript, SWF, and External
  Links. Status questions need only internal HTML.

All three also tick Configuration -> Spider -> Crawl -> Crawl Linked XML Sitemaps, so a spidered
run's coverage can be audited. Factory defaults don't read sitemaps.

Runs on different configs measure different things. Never compare their numbers.

## Audit scope before quoting a number

A crawl reports confidently on what it reached and says nothing about what it missed. Every count is
a count among pages this config could see. Run four checks before quoting a figure. A sitemap-seeded
run skips them; its coverage is complete by construction.

1. Elapsed time, from the `Crawl Overview` header, divided by URL count. Under roughly 50ms per URL
   means JavaScript rendering was off; a headless render can't run that fast.
2. The `Sitemaps` block of `Crawl Overview`. `URLs in Sitemap: 0` means the crawl never read a
   sitemap, not that the site lacks one. Every sitemap figure below it is 0 and meaningless. Fix the
   config; don't interpret the zero.
3. Crawled pages against the sitemap. This is the real coverage number.

   ```sh
   curl -s $SITE/robots.txt | grep -i sitemap          # find the index; often not sitemap.xml
   curl -s $SITE/<sitemap-index> | grep -o '<loc>[^<]*' | sed 's/<loc>//'   # then each child
   ```

   Export `Internal` / `HTML` with `Address`, normalise trailing slashes on both sides, and `comm`
   them. Group misses by first path segment. A whole missing segment usually has one cause.
4. The crawl-depth histogram. Export `Internal` / `HTML` with `Crawl Depth` and count by depth. A
   real crawl tapers. A cliff, many pages at the deepest level and none beyond, means
   `Limit Search Depth` cut it off. Confirm the queue drained (`waiting: 0` in `sf_crawl_progress`)
   and no URL cap stopped it.

| Signature | Cause | Effect |
| --- | --- | --- |
| Depth histogram cliffs with a large deepest bucket | `Limit Search Depth` is set | Everything past that hop is invisible |
| `URLs in Sitemap: 0` | Crawl Linked XML Sitemaps is off | Only link-reachable pages are seen |
| Elapsed time implausibly low; a segment missing wholesale | JS rendering off | Any client-rendered listing is a dead end |

JS rendering off compounds the others. An index page that ships an app shell has no links in raw
HTML, so nothing behind it is reachable at any depth. Check with
`curl -sL $URL | grep -c 'href="/<segment>/'` before blaming depth.

## Three data shapes

| Tool | What it is | Use it when |
| --- | --- | --- |
| `sf_generate_report` | 61 pre-baked cross-cutting analyses | The question spans URLs: chains, reciprocity, rich-result eligibility, totals |
| `sf_export_seo_element_urls` | The UI's tab and filter grid | "Give me the URLs where X", where X is a filter in a tab |
| `sf_generate_bulk_export` | Edges and raw content | "What links to the broken thing", or "dump the rendered HTML" |

Report is the analysis, element export is the tab, bulk export is the edges.

## Work in this order

0. Scope audit. A count from an unaudited crawl is a lower bound.
1. `Crawl Overview`: inventory, content types, indexable vs not.
2. `Issues Overview`: the triage table, with priority, URL count, and How-To-Fix per row. It names
   the next report worth running.
3. Drill into whatever Issues Overview ranks High.
4. Trace each candidate to a source file before it becomes a finding.

## Question to call

### Structured data

| Question | Call |
| --- | --- |
| Which rich-result types do we qualify for? | report `Structured Data:Google Rich Results Features Summary` |
| Which property fails, on how many URLs? | report `Structured Data:Validation Errors & Warnings Summary` |
| The failing URLs themselves | report `Structured Data:Validation Errors & Warnings` |
| Malformed JSON-LD, not merely invalid | report `Structured Data:Parse Errors` |
| Pages with no structured data | element `Structured Data`, filter `Missing` |

Summary first, per-URL second. Google's rich-result rules are stricter than schema.org validity:
`Course.description` must be 60 characters or fewer, so a Course graph needs its own short field, not
reused page prose.

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

## Traps

- The MCP needs the desktop app open and idle. Otherwise every tool throws
  `IllegalStateException: Tool cannot be called currently`: app state, not bad arguments. The
  headless CLI runs beside the GUI.
- Load a crawl before any report: `sf_list_crawls`, then `sf_load_crawl <id>`.
- Output dirs aren't created for you. `file_path` is relative to `sf_list_allowed_base_directory`.
  Run `sf_create_directory` first or get `NoSuchFileException`.
- During a crawl only `sf_crawl_progress` responds. Crawl, poll, then export.
- Pass `export_type: "CSV"`. The default NDJSON arrives as one giant line.
- `sf_list_available_bulk_exports` overflows the token limit. Call it once and keep the list.
- Always write to `file_path`. Inline content burns context; slice the file with shell.

## Report

Lead every set of counts with coverage ("238 of 727 sitemap URLs, 33%") and call the counts lower
bounds. A sitemap-seeded run says "117 of 117" and moves on.

Sort findings into three buckets, in order:

1. Confirmed ours. This repo serves the URL, and you name the file and line that emits the defect.
   Only these go in a PR.
2. Real, untraced. Name the system not yet ruled out and the check that settles it.
3. Untriaged rows, straight from `Issues Overview`, labelled uninvestigated.
