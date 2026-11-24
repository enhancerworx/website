# Enhancerworx website

Static site for https://www.enhancerworx.in, hosted on GitHub Pages. No build step, no dependencies.

## Edit the app list
1. Open `tools/apps.json` and add, change or remove an app.
2. Put its icon at `img/app-<slug>.webp` (square, about 160x160). Without one, a coloured tile with initials is used.
3. Run `python3 tools/build_apps.py`. It rewrites the apps section of `index.html`.
4. Commit and push.

## Contact form
Set your Formspree form ID in `index.html` (search for `YOUR_FORM_ID`).

## Do not delete
`CNAME`, `app-ads.txt` and `google7f809a8f1b46f7d8.html` (Search Console ownership).
