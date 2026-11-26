"""Shared layout, data and SEO helpers for every generated page.

Edit the header, footer or <head> here, then run:  python3 tools/build.py
"""
import json, html, os, glob, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

APPS_DATA = json.load(open('tools/apps.json', encoding='utf-8'))
TERMS = json.load(open('tools/terms.json', encoding='utf-8'))
DEV = TERMS['developer']
SITE = DEV['website'].rstrip('/')
DEV_URL = APPS_DATA['developer_url']
CATS = APPS_DATA['categories']
CAT = {c['id']: c for c in CATS}
APPS = APPS_DATA['apps']
APP = {a['slug']: a for a in APPS}
ASSET_V = '20261126a'          # bump when css/js change so browsers fetch fresh copies
TODAY = '2026-11-26'
OG_DEFAULT = f'{SITE}/img/og-image.jpg'

esc = lambda s: html.escape(str(s), quote=True)


# ---------- app helpers ----------
def play_url(a):
    return f'https://play.google.com/store/apps/details?id={a["pkg"]}' if a.get('pkg') else DEV_URL


def icon(a):
    for ext in ('webp', 'png', 'jpg'):
        if os.path.exists(f"img/app-{a['slug']}.{ext}"):
            return f"/img/app-{a['slug']}.{ext}"
    return '/img/mark.webp'


def screens(a):
    return ['/' + p.replace(os.sep, '/') for p in sorted(glob.glob(f"img/screens/{a['slug']}-*.*"))]


def all_ages(a):
    return a['slug'] in TERMS.get('all_ages', [])


def age_label(a):
    return 'All ages' if all_ages(a) else '13+'


def is_game(a):
    return a['cat'] == 'games' and a['slug'] not in TERMS.get('skip_category_clauses', [])


def app_page(a):
    return f'/apps/{a["slug"]}.html'


def terms_page(a):
    return f'/terms/{a["slug"]}.html'


def privacy_page(a):
    return f'/privacy/{a["slug"]}.html'


def size(p):
    try:
        from PIL import Image
        return Image.open(p.lstrip('/')).size
    except Exception:
        return 166, 296


# ---------- layout ----------
THEME_BTN = ('<button class="icon-btn" id="themeBtn" type="button" aria-label="Switch to dark theme">'
             '<svg class="i-moon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
             '<svg class="i-sun" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
             '</button>')

NAV = [('Apps', '/#apps'), ('Services', '/#services'), ('Process', '/#process'), ('About', '/#about'),
       ('Blog', '/blog/'), ('FAQ', '/#faq'), ('Contact', '/#contact')]


def header(active=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur if t == active else ""}>{t}</a>' for t, h in NAV)
    return f'''<header class="site-header" id="top">
    <div class="wrap bar">
      <a class="brand" href="/" aria-label="Enhancerworx home">
        <img src="/img/mark.webp" width="40" height="40" alt="">
        <span class="brand-name">Enhancer<span>worx</span></span>
      </a>
      <nav class="nav" id="nav" aria-label="Main">
        {links}
        <a class="nav-cta" href="/#contact">Start a project</a>
      </nav>
      <div class="bar-actions">
        {THEME_BTN}
        <a class="btn btn-sm btn-solid hide-sm" href="/#contact">Start a project</a>
        <button class="icon-btn menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">
          <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path class="m1" d="M4 7h16"/><path class="m2" d="M4 12h16"/><path class="m3" d="M4 17h16"/></svg>
        </button>
      </div>
    </div>
  </header>'''


def footer():
    cats = ''.join(f'<a href="/#cat-{c["id"]}">{esc(c["title"])}</a>' for c in CATS if any(a['cat'] == c['id'] for a in APPS))
    return f'''<footer class="site-footer">
    <div class="wrap">
      <div class="foot-grid">
        <div class="foot-brand">
          <a class="brand" href="/" aria-label="Enhancerworx home">
            <img src="/img/mark.webp" width="36" height="36" alt="">
            <span class="brand-name">Enhancer<span>worx</span></span>
          </a>
          <p>Educational apps for Android, iOS and the web. Learn. Build. Grow.</p>
          <a class="foot-mail" href="mailto:{DEV['email']}">{DEV['email']}</a>
        </div>
        <nav aria-label="Apps by subject">
          <h2>Apps</h2>
          {cats}
          <a href="{DEV_URL}" target="_blank" rel="noopener noreferrer">All apps on Google Play</a>
        </nav>
        <nav aria-label="Company">
          <h2>Company</h2>
          <a href="/#services">Services</a>
          <a href="/#process">How we work</a>
          <a href="/#about">About</a>
          <a href="/blog/">Blog</a>
          <a href="/#faq">FAQ</a>
          <a href="/#contact">Contact</a>
        </nav>
        <nav aria-label="Legal">
          <h2>Legal</h2>
          <a href="/terms/">App terms of service</a>
          <a href="/privacy/">App privacy policies</a>
          <a href="/privacyPolicy.html">Website privacy policy</a>
          <a href="/termsOfService.html">Website terms</a>
          <a href="/blog/feed.xml">RSS feed</a>
        </nav>
      </div>
      <div class="copy">
        <p>&copy; <span id="year">2026</span> Enhancerworx. All rights reserved.</p>
        <p>Google Play is a trademark of Google LLC.</p>
      </div>
    </div>
  </footer>
  <button class="to-top" id="toTop" type="button" aria-label="Back to top" hidden>
    <svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
  </button>'''


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'


def breadcrumbs(items):
    """items: list of (name, absolute_url)"""
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def crumbs_html(items):
    out = []
    for i, (n, u) in enumerate(items):
        if i == len(items) - 1:
            out.append(f'<span aria-current="page">{esc(n)}</span>')
        else:
            out.append(f'<a href="{u.replace(SITE, "") or "/"}">{esc(n)}</a><span aria-hidden="true">/</span>')
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ''.join(out) + '</nav>'


def head(title, desc, path, og_type='website', image=OG_DEFAULT, card='summary_large_image',
         ld=(), robots='index, follow, max-image-preview:large', extra='', csp_extra=''):
    url = SITE + path
    lds = '\n  '.join(jsonld(x) for x in ld)
    return f'''<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="{robots}">
  <meta name="author" content="Enhancerworx">
  <meta name="theme-color" content="#F7F9FD" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#0A1220" media="(prefers-color-scheme: dark)">
  <meta name="color-scheme" content="light dark">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'self'; manifest-src 'self'; form-action 'none'; upgrade-insecure-requests{csp_extra}">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <meta property="og:type" content="{og_type}">
  <meta property="og:site_name" content="Enhancerworx">
  <meta property="og:locale" content="en_IN">
  <meta property="og:title" content="{esc(title)}">
  <meta property="og:description" content="{esc(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{image}">
  <meta name="twitter:card" content="{card}">
  <meta name="twitter:title" content="{esc(title)}">
  <meta name="twitter:description" content="{esc(desc)}">
  <meta name="twitter:image" content="{image}">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="alternate" type="application/rss+xml" title="Enhancerworx blog" href="/blog/feed.xml">
  <link rel="preload" href="/fonts/sora-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/figtree-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <script src="/js/theme.js?v={ASSET_V}"></script>
  <link rel="stylesheet" href="/css/style.css?v={ASSET_V}">{extra}
  {lds}'''


def page(title, desc, path, body, active='', **kw):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  {head(title, desc, path, **kw)}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <div class="progress" id="progress" aria-hidden="true"></div>
  {header(active)}
{body}
  {footer()}
  <script src="/js/main.js?v={ASSET_V}" defer></script>
</body>
</html>
'''


def write(path, text):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    open(path, 'w', encoding='utf-8').write(text)


def replace_marker(text, tag, body):
    new, k = re.subn(rf'<!--{tag}:START-->.*?<!--{tag}:END-->', lambda m: f'<!--{tag}:START-->{body}<!--{tag}:END-->', text, flags=re.S)
    if not k:
        raise SystemExit(f'Marker {tag} not found')
    return new


ORG = {"@context": "https://schema.org", "@type": "Organization", "@id": f"{SITE}/#org", "name": "Enhancerworx",
       "url": f"{SITE}/", "logo": f"{SITE}/icon-512.png", "email": DEV['email'], "foundingDate": "2018",
       "description": "EdTech app studio building educational apps for Android, iOS and the web.",
       "sameAs": [DEV_URL]}
