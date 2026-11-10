# Build a missing mode config

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
