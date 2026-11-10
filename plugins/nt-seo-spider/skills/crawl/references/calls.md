# Question to call

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
