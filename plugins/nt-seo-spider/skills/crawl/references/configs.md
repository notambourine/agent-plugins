# Write a mode config

A config is a JSON file of top-level categories. `--config` and `config_path` apply it over factory
defaults, never over the user's saved default, so a file lists only what it changes:

```json
{ "crawlConfig": { "crawlerMode": "RENDER", "crawlSitemaps": true } }
```

The shipped modes:

- `links`: skips images, CSS, JavaScript, SWF, and external links. Status questions need only
  internal HTML.
- `schema`: `links` plus JSON-LD extraction with Schema.org and Google rich-result validation.
  Without it, `structured_data_all.csv` shows zero types on every row.
- `render`: JavaScript rendering, with the Chrome console log stored.

All three set `crawlSitemaps`, so a spidered run's coverage can be audited, and
`searchAllSubdomains`. Factory defaults don't read sitemaps.

## Find a setting

`sf_list_config_categories` names the categories and `sf_get_config_sub_schema <category>` returns
the fields and allowed values for one. Without the MCP, every run log prints the full effective
config as base64 JSON:

```sh
grep -o 'configfile=\[[^]]*' run.log | sed 's/configfile=\[//' | base64 -d
```

## Check the config loaded

The loader fails quietly, and the launcher exits 0 either way. After the first run on a new or
edited config, grep `run.log`:

- `Ignoring unknown config field` means a misspelt key was dropped and the default applied.
- `SeoSpider failed to start` means a value was invalid and nothing was crawled.

## Keep secrets out

A config stores custom JavaScript snippets, custom HTTP headers, and AI prompts verbatim. Read a
config for API keys and client facts before committing it. Site-specific configs belong in the
site's repo, in the directory its supplement names.

## Convert a legacy config

A binary `.seospiderconfig` still loads. To replace one, run it headless once, decode the
`configfile` dump, and keep only the settings the mode needs. Drop `configVersion` and the
`lastModCustomDate` fields, which record when the file was saved.
