# Enhancerworx website

Static site for https://www.enhancerworx.in, hosted on GitHub Pages. No build step, no dependencies.

## Edit the app list
1. Open `tools/apps.json` and add, change or remove an app.
2. Square icon at `img/app-<slug>.webp`. Optional screenshots at `img/screens/<slug>-1.webp`, `-2.webp`, ...
3. Run `python3 tools/build_apps.py` (needs Python 3 and `pip install pillow`). It rewrites the app lists in `index.html`.
4. Commit and push.

## App Terms of Service (for Google Play Console)
Every app has its own page at `https://www.enhancerworx.in/terms/<slug>.html`, with a list of all of them at `/terms/`.
- Paste each app's URL into Play Console > App content (or Store settings) > Terms of Service. All URLs are listed in `tools/terms-urls.csv`.
- Shared wording lives in `tools/build_terms.py`; developer details, dates and app-specific clauses live in `tools/terms.json`.
- `python3 tools/build_apps.py` rebuilds the app list and all terms pages and the sitemap. Run `python3 tools/build_terms.py` to rebuild only the terms.
- New app? Add it to `tools/apps.json` (and optionally to `tools/terms.json`), run the build, and its terms page is created automatically.

## Contact form
Sends through Formspree. Create a form at formspree.io, then replace `YOUR_FORM_ID` in `index.html` (search for it) with your form ID.

## WhatsApp
Number is +91 89207 95732 (wa.me/918920795732). To change it, search `918920795732` in `index.html` and `js/main.js`.

## Do not delete
`CNAME`, `app-ads.txt` and `google7f809a8f1b46f7d8.html` (Search Console ownership).
