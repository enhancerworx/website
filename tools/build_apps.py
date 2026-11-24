#!/usr/bin/env python3
"""Rebuilds the apps section of index.html from tools/apps.json.

Add an app:  add one entry to tools/apps.json, then run:  python3 tools/build_apps.py
Icon:        put a square image at img/app-<slug>.webp (or .png/.jpg). With no icon, a coloured tile with initials is used.
Link:        "pkg" is the part after id= in the Play Store URL. Leave it empty to link to your developer page instead.
"""
import json, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(os.path.join(ROOT, 'tools', 'apps.json'), encoding='utf-8'))
dev = data['developer_url']
apps = data['apps']
cats = data['categories']
TILES = 5

def icon_for(a, i):
    for ext in ('webp', 'png', 'jpg'):
        p = f"img/app-{a['slug']}.{ext}"
        if os.path.exists(os.path.join(ROOT, p)):
            return f'<img src="{p}" width="64" height="64" alt="" loading="lazy">'
    ini = a.get('initials') or ''.join(w[0] for w in re.findall(r'[A-Za-z]+', a['name'])[:2]).upper()
    return f'<span class="tile t{i % TILES + 1}" aria-hidden="true">{html.escape(ini)}</span>'

out = []
n = 0
for c in cats:
    items = [a for a in apps if a['cat'] == c['id']]
    if not items:
        continue
    out.append(f'<section class="cat" id="cat-{c["id"]}" aria-labelledby="h-{c["id"]}">')
    out.append(f'  <div class="cat-head"><h3 id="h-{c["id"]}">{html.escape(c["title"])} <span class="count">{len(items)}</span></h3><p>{html.escape(c["blurb"])}</p></div>')
    out.append('  <ul class="apps">')
    for a in items:
        url = f'https://play.google.com/store/apps/details?id={a["pkg"]}' if a.get('pkg') else dev
        name, desc = html.escape(a['name']), html.escape(a['desc'])
        search = html.escape((a['name'] + ' ' + a['desc']).lower(), quote=True)
        out.append(f'    <li data-search="{search}"><a href="{url}" target="_blank" rel="noopener noreferrer">{icon_for(a, n)}'
                   f'<span class="app-text"><strong>{name}</strong><span>{desc}</span></span>'
                   f'<span class="app-go">Google Play<span class="sr"> (opens in a new tab)</span></span></a></li>')
        n += 1
    out.append('  </ul>')
    out.append('</section>')

block = '\n'.join(out)
nav = ''.join(f'<a class="chip" href="#cat-{c["id"]}">{html.escape(c["title"])}</a>' for c in cats if any(a['cat'] == c['id'] for a in apps))

path = os.path.join(ROOT, 'index.html')
t = open(path, encoding='utf-8').read()
t, k1 = re.subn(r'<!--APPS:START-->.*?<!--APPS:END-->', lambda m: f'<!--APPS:START-->\n{block}\n<!--APPS:END-->', t, flags=re.S)
t, k2 = re.subn(r'<!--NAV:START-->.*?<!--NAV:END-->', lambda m: f'<!--NAV:START-->{nav}<!--NAV:END-->', t, flags=re.S)
t = re.sub(r'(<span id="appTotal">)\d+(</span>)', lambda m: f'{m.group(1)}{n}{m.group(2)}', t)
if not (k1 and k2):
    sys.exit('Markers not found in index.html')
open(path, 'w', encoding='utf-8').write(t)
print(f'Built {n} apps in {len([c for c in cats if any(a["cat"]==c["id"] for a in apps)])} categories.')
