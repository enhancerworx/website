# Enhancerworx website

Static site for https://www.enhancerworx.in, hosted on GitHub Pages. The pages in this folder are ready to publish as they are; the build script only regenerates them after you change the data.

## Rebuild after any change
```
python3 tools/build.py        (Windows: py tools\build.py)
```
This regenerates the homepage app list, the shared header and footer on every page, the blog, one page per app (`/apps/`), one Terms of Service page per app (`/terms/`), `sitemap.xml` and the RSS feed (`/blog/feed.xml`). Pillow (`pip install pillow`) is optional and only used to read screenshot sizes.

## Common edits
| What | Where |
|---|---|
| Add, change or remove an app | `tools/apps.json`, icon at `img/app-<slug>.webp`, screenshots at `img/screens/<slug>-1.webp` |
| Write a blog post | Add `tools/posts/<url-name>.html` (copy an existing post: JSON header, then the article HTML) |
| Terms of Service wording, ages, developer details | `tools/terms.json` (data) and `tools/build_terms.py` (wording) |
| Privacy policies: SDKs, permissions, on-device data | `tools/privacy.json` (data) and `tools/build_privacy.py` (wording) |
| Header, footer, menu, SEO tags | `tools/layout.py` |
| Homepage text | `index.html` (edit outside the `<!--NAME:START-->...<!--NAME:END-->` markers) |
| Styles / scripts | `css/style.css`, `js/main.js` |

## Ages
All apps are 13+ except the games listed under `"all_ages"` in `tools/terms.json` (Snake Word, Merge Balls 2048, Rock Balance Master).

## Play Console: Privacy Policy and Terms of Service URLs
- Privacy policy: `https://www.enhancerworx.in/privacy/<slug>.html`
- Terms of service: `https://www.enhancerworx.in/terms/<slug>.html`

The full list for every app is in `tools/app-links.csv`. Privacy wording lives in `tools/build_privacy.py`; third-party services, permissions and on-device data per app are in `tools/privacy.json`.

## After changing CSS or JS
Browsers cache `css/style.css` and `js/*.js`. Bump `ASSET_V` in `tools/layout.py` and run the build so visitors get the new files immediately.

## Contact form
Sends through Formspree (form ID in `index.html`, search for `formspree.io/f/`).

## SEO checklist after publishing
1. In Google Search Console, submit `https://www.enhancerworx.in/sitemap.xml`.
2. Use URL Inspection on the homepage and one blog post to request indexing.

## Do not delete
`CNAME`, `app-ads.txt`, `.nojekyll` and `google7f809a8f1b46f7d8.html` (Search Console ownership).
