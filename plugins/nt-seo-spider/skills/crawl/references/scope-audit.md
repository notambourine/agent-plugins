# Scope audit

Run these four checks on a spidered crawl before quoting a figure from it.

1. Elapsed time, from the `Crawl Overview` header, divided by URL count. Under roughly 50ms per URL
   means JavaScript rendering was off, because a headless render cannot run that fast.
2. The `Sitemaps` block of `Crawl Overview`. `URLs in Sitemap: 0` means the crawl never read a
   sitemap. It does not mean the site lacks one, and every sitemap figure below it is also 0. Fix
   the config and rerun before reading those figures.
3. Crawled pages against the sitemap. This is the real coverage number.

   ```sh
   curl -s $SITE/robots.txt | grep -i sitemap          # find the index; often not sitemap.xml
   curl -s $SITE/<sitemap-index> | grep -o '<loc>[^<]*' | sed 's/<loc>//'   # then each child
   ```

   Export `Internal` / `HTML` with `Address`, normalise trailing slashes on both sides, and `comm`
   them. Group the misses by first path segment, since a segment that is missing entirely usually
   has one cause.
4. The crawl-depth histogram. Export `Internal` / `HTML` with `Crawl Depth` and count by depth. A
   complete crawl tapers off. Many pages at the deepest level and none beyond it means
   `Limit Search Depth` cut it off. Confirm the queue drained (`waiting: 0` in `sf_crawl_progress`)
   and no URL cap stopped it.

| Signature | Cause | Effect |
| --- | --- | --- |
| Depth histogram cliffs with a large deepest bucket | `Limit Search Depth` is set | Everything past that hop is invisible |
| `URLs in Sitemap: 0` | Crawl Linked XML Sitemaps is off | Only link-reachable pages are seen |
| Elapsed time implausibly low; a segment missing wholesale | JS rendering off | Any client-rendered listing is a dead end |

JS rendering being off makes the other two worse. An index page that ships an app shell has no
links in its raw HTML, so nothing behind it is reachable at any depth. Check with
`curl -sL $URL | grep -c 'href="/<segment>/'` before blaming depth.
