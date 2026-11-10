---
name: crawl
description: Crawl a site with Screaming Frog and turn the output into findings a repo can act on. Use for SEO crawls and site audits, redirect or structured-data checks, rich-result eligibility questions, or any request that starts from crawl output.
---

# SEO crawls with Screaming Frog

The output is a list of findings a developer in this repo can fix. Each finding states how much of
the site the crawl covered, who owns the defect, and the source file that emits it.

## Read the site supplement

Read `.claude/refs/nt-seo-spider.md` first when the repo has one. It holds the domain, sitemap URLs,
the paths this repo serves, where SEO source lives, and site rules. It wins over this skill.

Without it, settle two things before any finding: how much of the site the crawl reached, and which
failures come from a platform this repo doesn't ship.

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

When a mode config is missing, ask the user to build it per
[references/configs.md](references/configs.md).

Runs on different configs measure different things. Never compare their numbers.

## Audit scope before quoting a number

A crawl reports confidently on what it reached and says nothing about what it missed. Every count is
a count among pages this config could see. Before quoting a figure from a spidered crawl, run the
checks in [references/scope-audit.md](references/scope-audit.md). A sitemap-seeded run skips them;
its coverage is complete by construction.

## Three data shapes

| Tool | What it is | Use it when |
| --- | --- | --- |
| `sf_generate_report` | 61 pre-baked cross-cutting analyses | The question spans URLs: chains, reciprocity, rich-result eligibility, totals |
| `sf_export_seo_element_urls` | The UI's tab and filter grid | "Give me the URLs where X", where X is a filter in a tab |
| `sf_generate_bulk_export` | Edges and raw content | "What links to the broken thing", or "dump the rendered HTML" |

## Work in this order

0. Scope audit. A count from an unaudited crawl is a lower bound.
1. `Crawl Overview`: inventory, content types, indexable vs not.
2. `Issues Overview`: the triage table, with priority, URL count, and How-To-Fix per row. It names
   the next report worth running.
3. Drill into whatever Issues Overview ranks High.
4. Trace each candidate to a source file before it becomes a finding.

For the report or export that answers a specific question, read
[references/calls.md](references/calls.md).

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
