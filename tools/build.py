#!/usr/bin/env python3
"""Builds the whole site. Run from anywhere:   python3 tools/build.py   (Windows: py tools\\build.py)

  1. Homepage (index.html): app directory, subject chips, gallery, latest blog posts, structured data,
     shared header and footer. Only the parts between <!--NAME:START--> and <!--NAME:END--> markers change.
  2. Static pages (privacyPolicy.html, termsOfService.html, 404.html): shared header and footer.
  3. Blog (blog/), app pages (apps/), app terms of service (terms/), sitemap.xml.

Requires Python 3.8+. Pillow (pip install pillow) is optional and only used to read screenshot sizes.
"""
import json, os, re, sys, html as _html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *  # noqa: E402,F401
import csv
import build_blog, build_app_pages, build_terms, build_privacy  # noqa: E402


def directory_html():
    blocks, n = [], 0
    for c in CATS:
        items = [a for a in APPS if a['cat'] == c['id']]
        if not items:
            continue
        blocks.append(f'<section class="cat" id="cat-{c["id"]}" aria-labelledby="h-{c["id"]}">')
        blocks.append(f'  <div class="cat-head"><h3 id="h-{c["id"]}">{esc(c["title"])} <span class="count">{len(items)}</span></h3><p>{esc(c["blurb"])}</p></div>')
        blocks.append('  <ul class="apps">')
        for a in items:
            attrs = (f'data-slug="{a["slug"]}" data-name="{esc(a["name"])}" data-desc="{esc(a["desc"])}" '
                     f'data-cat="{esc(c["title"])} · Age {age_label(a)}" data-url="{esc(play_url(a))}" data-icon="{icon(a)}" '
                     f'data-page="{app_page(a)}" data-terms="{terms_page(a)}" data-privacy="{privacy_page(a)}" '
                     f'data-points="{esc("|".join(a.get("points", [])))}" data-screens="{esc(",".join(screens(a)))}" '
                     f'data-search="{esc((a["name"] + " " + a["desc"] + " " + c["title"]).lower())}"')
            blocks.append(
                f'    <li {attrs}><div class="app-row">'
                f'<a class="app-open" href="{app_page(a)}" aria-haspopup="dialog"><img src="{icon(a)}" width="64" height="64" alt="" loading="lazy">'
                f'<span class="app-text"><strong>{esc(a["name"])}</strong><span>{esc(a["desc"])}</span></span></a>'
                f'<a class="app-go" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">Install<span class="sr"> {esc(a["name"])} on Google Play (opens in a new tab)</span></a>'
                f'</div></li>')
            n += 1
        blocks.append('  </ul>')
        blocks.append('</section>')
    return '\n' + '\n'.join(blocks) + '\n', n


def gallery_html():
    out = []
    for a in APPS:
        for p in screens(a)[:1]:
            w, h = size(p)
            out.append(f'<li><button type="button" class="shot" data-open="{a["slug"]}" aria-label="Open details for {esc(a["name"])}">'
                       f'<img src="{p}" width="{w}" height="{h}" alt="Screenshot of {esc(a["name"])}" loading="lazy"><span>{esc(a["name"])}</span></button></li>')
    return '\n'.join(out)


def faq_ld(text):
    qa = re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', text, re.S)
    clean = lambda s: _html.unescape(re.sub(r'<[^>]+>', '', s)).strip()
    return jsonld({"@context": "https://schema.org", "@type": "FAQPage",
                   "mainEntity": [{"@type": "Question", "name": clean(q), "acceptedAnswer": {"@type": "Answer", "text": clean(a)}} for q, a in qa]})


def versions(text):
    return re.sub(r'(/(?:css/style\.css|js/main\.js|js/theme\.js))\?v=\w+', lambda m: f'{m.group(1)}?v={ASSET_V}', text)


def build_index(posts):
    t = open('index.html', encoding='utf-8').read()
    apps_html, n = directory_html()
    t = replace_marker(t, 'HEADER', header())
    t = replace_marker(t, 'FOOTER', footer())
    t = replace_marker(t, 'APPS', apps_html)
    t = replace_marker(t, 'NAV', ''.join(f'<a class="chip" href="#cat-{c["id"]}">{esc(c["title"])}</a>' for c in CATS if any(a['cat'] == c['id'] for a in APPS)))
    t = replace_marker(t, 'GALLERY', gallery_html())
    t = replace_marker(t, 'BLOG', '\n' + build_blog.latest_cards(posts) + '\n')
    t = replace_marker(t, 'LDAPPS', jsonld({"@context": "https://schema.org", "@type": "ItemList", "name": "Enhancerworx apps on Google Play",
                                             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a['name'], "url": SITE + app_page(a)} for i, a in enumerate(APPS)]}))
    t = replace_marker(t, 'LDFAQ', faq_ld(t))
    t = re.sub(r'(<span class="js-total">)\d+(</span>)', lambda m: f'{m.group(1)}{n}{m.group(2)}', t)
    t = versions(t)
    open('index.html', 'w', encoding='utf-8').write(t)
    print(f'Built homepage: {n} apps')


def build_static():
    for f in ('privacyPolicy.html', 'termsOfService.html', '404.html'):
        t = open(f, encoding='utf-8').read()
        t = replace_marker(t, 'HEADER', header())
        t = replace_marker(t, 'FOOTER', footer())
        open(f, 'w', encoding='utf-8').write(versions(t))
    print('Built static pages')


def build_sitemap(posts):
    urls = [('/', '1.0'), ('/apps/', '0.9'), ('/blog/', '0.8'), ('/terms/', '0.5'), ('/privacy/', '0.5'),
            ('/privacyPolicy.html', '0.3'), ('/termsOfService.html', '0.3')]
    urls += [(app_page(a), '0.8') for a in APPS]
    urls += [(p['url'], '0.7') for p in posts]
    urls += [(terms_page(a), '0.4') for a in APPS]
    urls += [(privacy_page(a), '0.4') for a in APPS]
    rows = ''.join(f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for u, pr in urls)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n')
    print(f'Built sitemap.xml: {len(urls)} URLs')


def main():
    posts = build_blog.main()
    build_app_pages.main(posts)
    build_terms.main()
    build_privacy.main()
    build_index(posts)
    build_static()
    build_sitemap(posts)
    build_links_csv()


def build_links_csv():
    with open('tools/app-links.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['App name', 'Package name', 'Age', 'Privacy Policy URL', 'Terms of Service URL', 'App page'])
        for a in APPS:
            w.writerow([a['name'], a.get('pkg', ''), age_label(a), SITE + privacy_page(a), SITE + terms_page(a), SITE + app_page(a)])
    print('Wrote tools/app-links.csv')


if __name__ == '__main__':
    main()
