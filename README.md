# Enhancerworx website

Static site for https://www.enhancerworx.in, hosted on GitHub Pages. No build step, no dependencies.

## Edit the app list
1. Open `tools/apps.json` and add, change or remove an app.
2. Square icon at `img/app-<slug>.webp`. Optional screenshots at `img/screens/<slug>-1.webp`, `-2.webp`, ...
3. Run `python3 tools/build_apps.py` (needs Python 3 and `pip install pillow`). It rewrites the app lists in `index.html`.
4. Commit and push.

## Contact form
Sends through FormSubmit to enhancerworx@gmail.com. The very first submission triggers an activation email: click the link in it once.

## Do not delete
`CNAME`, `app-ads.txt` and `google7f809a8f1b46f7d8.html` (Search Console ownership).
