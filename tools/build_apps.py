#!/usr/bin/env python3
"""Rebuilds the app lists in index.html from tools/apps.json.

Add an app:
  1. Add an entry to tools/apps.json ("pkg" is what follows id= in the Play Store URL; leave "" to link to your developer page).
  2. Put its icon at img/app-<slug>.webp (square). No icon? A coloured tile with initials is used.
  3. Optional screenshots: img/screens/<slug>-1.webp, <slug>-2.webp ... (they appear in the app's detail window and the gallery).
  4. Run:  python3 tools/build_apps.py
Requires Python 3 and, for screenshot sizes, Pillow (pip install pillow).
"""
import json, html, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
data = json.load(open('tools/apps.json', encoding='utf-8'))
dev, apps, cats = data['developer_url'], data['apps'], data['categories']
esc = lambda s: html.escape(s, quote=True)
cat_title = {c['id']: c['title'] for c in cats}

def play_url(a):
    return f'https://play.google.com/store/apps/details?id={a["pkg"]}' if a.get('pkg') else dev

def icon(a, i):
    for ext in ('webp', 'png', 'jpg'):
        p = f"img/app-{a['slug']}.{ext}"
        if os.path.exists(p):
            return p
    return None

def screens(a):
    return sorted(glob.glob(f"img/screens/{a['slug']}-*.*"))

def size(p):
    try:
        from PIL import Image
        w, h = Image.open(p).size
        return w, h
    except Exception:
        return 166, 296

used = [c for c in cats if any(a['cat'] == c['id'] for a in apps)]
blocks, n = [], 0
for c in used:
    items = [a for a in apps if a['cat'] == c['id']]
    blocks.append(f'<section class="cat" id="cat-{c["id"]}" aria-labelledby="h-{c["id"]}">')
    blocks.append(f'  <div class="cat-head"><h3 id="h-{c["id"]}">{esc(c["title"])} <span class="count">{len(items)}</span></h3><p>{esc(c["blurb"])}</p></div>')
    blocks.append('  <ul class="apps">')
    for a in items:
        ic = icon(a, n)
        sc = screens(a)
        if ic:
            img = f'<img src="{ic}" width="64" height="64" alt="" loading="lazy">'
        else:
            ini = a.get('initials') or ''.join(w[0] for w in re.findall(r'[A-Za-z]+', a['name'])[:2]).upper()
            img = f'<span class="tile t{n % 5 + 1}" aria-hidden="true">{esc(ini)}</span>'
        attrs = (f'data-slug="{a["slug"]}" data-name="{esc(a["name"])}" data-desc="{esc(a["desc"])}" '
                 f'data-cat="{esc(cat_title[a["cat"]])}" data-url="{esc(play_url(a))}" data-icon="{ic or ""}" '
                 f'data-points="{esc("|".join(a.get("points", [])))}" data-screens="{esc(",".join(sc))}" '
                 f'data-search="{esc((a["name"] + " " + a["desc"] + " " + cat_title[a["cat"]]).lower())}"')
        blocks.append(
            f'    <li {attrs}><div class="app-row">'
            f'<button type="button" class="app-open" aria-haspopup="dialog">{img}'
            f'<span class="app-text"><strong>{esc(a["name"])}</strong><span>{esc(a["desc"])}</span></span></button>'
            f'<a class="app-go" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">Install<span class="sr"> {esc(a["name"])} on Google Play (opens in a new tab)</span></a>'
            f'</div></li>')
        n += 1
    blocks.append('  </ul>')
    blocks.append('</section>')

nav = ''.join(f'<a class="chip" href="#cat-{c["id"]}">{esc(c["title"])}</a>' for c in used)

gal = []
for a in apps:
    for p in screens(a):
        w, h = size(p)
        gal.append(f'<li><button type="button" class="shot" data-open="{a["slug"]}" aria-label="Open details for {esc(a["name"])}">'
                   f'<img src="{p}" width="{w}" height="{h}" alt="Screenshot of {esc(a["name"])}" loading="lazy"><span>{esc(a["name"])}</span></button></li>')

foot = ''.join(f'<a href="#cat-{c["id"]}">{esc(c["title"])}</a>' for c in used)

ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Enhancerworx apps on Google Play",
      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a["name"], "url": play_url(a)}
                          for i, a in enumerate([a for a in apps if a.get('pkg')])]}

t = open('index.html', encoding='utf-8').read()
def sub(tag, body):
    global t
    t, k = re.subn(rf'<!--{tag}:START-->.*?<!--{tag}:END-->', lambda m: f'<!--{tag}:START-->{body}<!--{tag}:END-->', t, flags=re.S)
    if not k: sys.exit(f'Marker {tag} not found in index.html')
sub('APPS', '\n' + '\n'.join(blocks) + '\n')
sub('NAV', nav)
sub('GALLERY', '\n'.join(gal))
sub('FOOTCATS', foot)
sub('LDAPPS', '<script type="application/ld+json">\n' + json.dumps(ld, indent=2) + '\n</script>')
t = re.sub(r'(<span class="js-total">)\d+(</span>)', lambda m: f'{m.group(1)}{n}{m.group(2)}', t)
open('index.html', 'w', encoding='utf-8').write(t)
print(f'Built {n} apps, {len(used)} categories, {len(gal)} gallery screenshots.')
