# Google Search Console

## 1. Verify the domain

Use a **Domain property**, not a URL prefix — it covers http, https, www and
every subdomain in one go, and the DNS record is already yours to edit.

1. https://search.google.com/search-console → Add property → **Domain**
2. Enter `thehelpingsun.com` (no https://, no www)
3. Google gives a TXT record. In Cloudflare → DNS → Records → Add record:
   - Type `TXT`, Name `@`, Content: the `google-site-verification=...` string
   - Proxy status is not applicable to TXT; leave TTL auto
4. Back in Search Console, press Verify. Usually works within a minute.

## 2. Submit the sitemap

Search Console → Sitemaps → enter `sitemap.xml` → Submit.

Full URL: `https://thehelpingsun.com/sitemap.xml`

## 3. The URLs

These are the canonical, extensionless forms. Cloudflare 307-redirects
`/prints.html` to `/prints`, so always submit the short form — submitting the
`.html` version asks Google to index a redirect.

```
https://thehelpingsun.com/
https://thehelpingsun.com/prints
https://thehelpingsun.com/privacy
https://thehelpingsun.com/terms
```

Paste each into the search bar at the top of Search Console, then
**Request indexing**. There is a daily quota of around 10, so four is fine.
Only the first two matter for traffic; the legal pages are submitted so the
site looks complete, not because anyone searches for them.

## 4. Also worth doing

- **Bing**: https://www.bing.com/webmasters — it can import directly from
  Search Console once that is verified, so it costs about one minute. Bing
  also feeds DuckDuckGo.
- Resubmit the sitemap after a batch of new photographs changes `/prints`.

## What is on the pages now

Each page carries a canonical link, a description and Open Graph tags, so a
link shared to Facebook or Instagram shows a title and summary rather than a
bare URL. `robots.txt` allows everything and points at the sitemap.

Nothing here blocks crawlers. There is no `noindex` anywhere on the site.

## A note on what Search Console will and will not do

It reports how the site appears in Google. It does not drive sales on its
own, and the shop at ian-sun.pixels.com is a separate domain that Google
indexes separately — you cannot submit it here, and Pixels handles its own
SEO. The traffic this site earns is for the story and the gallery; the shop
converts it.
