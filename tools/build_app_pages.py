#!/usr/bin/env python3
"""Builds one landing page per app (apps/<slug>.html) and the apps index (apps/index.html).
These pages give every app its own search-friendly URL. Data comes from tools/apps.json."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *  # noqa: E402,F401

PLAY_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M4.2 2.3c-.3.3-.4.7-.4 1.2v17c0 .5.1.9.4 1.2l9.6-9.7-9.6-9.7Zm10.9 8.4 2.9-2.9L6.5 1.3c-.4-.2-.8-.3-1.1-.2l9.7 9.6Zm0 2.6-9.7 9.6c.3.1.7 0 1.1-.2L18 16.2l-2.9-2.9Zm4.3-4.7-3 3 3 3 3.3-1.9c.9-.5.9-1.8 0-2.3l-3.3-1.8Z"/></svg>'


def app_card(a):
    return f'''<a class="app-card" href="{app_page(a)}">
            <img src="{icon(a)}" width="56" height="56" alt="" loading="lazy">
            <span><strong>{esc(a['name'])}</strong><small>{esc(a['desc'])}</small></span>
          </a>'''


def build(a, posts):
    c = CAT[a['cat']]
    path = app_page(a)
    trail = [('Home', SITE + '/'), ('Apps', SITE + '/apps/'), (a['name'], SITE + path)]
    sc = screens(a)
    hero_visual = (f'<div class="phone"><img src="{sc[0]}" width="{size(sc[0])[0]}" height="{size(sc[0])[1]}" alt="Screenshot of {esc(a["name"])}"></div>'
                   if sc else f'<div class="app-hero-icon"><img src="{icon(a)}" width="160" height="160" alt=""></div>')
    points = a.get('points', [])
    features = ''
    if points:
        features = f'''
    <section class="section-sm" aria-labelledby="feat-h">
      <div class="wrap">
        <h2 id="feat-h" class="h-sm">Features</h2>
        <ul class="feature-list">{''.join(f'<li>{esc(p)}</li>' for p in points)}</ul>
      </div>
    </section>'''
    gallery = ''
    if len(sc) > 1:
        imgs = ''.join(f'<li><img src="{s}" width="{size(s)[0]}" height="{size(s)[1]}" alt="{esc(a["name"])} screenshot {i + 1}" loading="lazy"></li>' for i, s in enumerate(sc))
        gallery = f'''
    <section class="section-sm" aria-labelledby="shots-h">
      <div class="wrap">
        <h2 id="shots-h" class="h-sm">Screenshots</h2>
        <ul class="gallery" tabindex="0" aria-label="Screenshots, scroll sideways to see more">{imgs}</ul>
      </div>
    </section>'''
    rel_posts = [p for p in posts if a in p['apps']]
    reading = ''
    if rel_posts:
        reading = f'''
    <section class="section-sm" aria-labelledby="read-h">
      <div class="wrap">
        <h2 id="read-h" class="h-sm">Related reading</h2>
        <ul class="link-list">{''.join(f'<li><a href="{p["url"]}">{esc(p["title"])}</a><span>{p["minutes"]} min read</span></li>' for p in rel_posts)}</ul>
      </div>
    </section>'''
    more = [x for x in APPS if x['cat'] == a['cat'] and x is not a][:6]
    info = [('Category', esc(c['title'])), ('Age', age_label(a)), ('Platform', 'Android (Google Play)'), ('Developer', 'Enhancerworx')]
    if a.get('pkg'):
        info.append(('Package', f'<code>{esc(a["pkg"])}</code>'))
    info.append(('Terms', f'<a href="{terms_page(a)}">Terms of Service</a>'))
    info.append(('Privacy', f'<a href="{privacy_page(a)}">Privacy Policy</a>'))
    body = f'''
  <main id="main">
    <div class="page-hero app-hero">
      <div class="wrap app-hero-grid">
        <div>
          {crumbs_html(trail)}
          <div class="terms-id">
            <img src="{icon(a)}" width="76" height="76" alt="">
            <div>
              <p class="eyebrow">{esc(c['title'])}</p>
              <h1>{esc(a['name'])}</h1>
            </div>
          </div>
          <p class="page-lead">{esc(a['desc'])}</p>
          <div class="tags"><span class="tag">Age {age_label(a)}</span><span class="tag">Android</span>{'<span class="tag">Works offline</span>' if 'offline' in a['desc'].lower() or 'offline' in a['name'].lower() else ''}</div>
          <div class="hero-cta">
            <a class="btn btn-solid btn-play" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">{PLAY_SVG}<span>Get it on Google Play<span class="sr"> (opens in a new tab)</span></span></a>
            <a class="btn btn-line" href="/#cat-{c['id']}">More {esc(c['title'].split(' and ')[0].lower())} apps</a>
          </div>
        </div>
        {hero_visual}
      </div>
    </div>{features}{gallery}
    <section class="section-sm" aria-labelledby="info-h">
      <div class="wrap">
        <h2 id="info-h" class="h-sm">App information</h2>
        <dl class="info-grid">{''.join(f'<div><dt>{k}</dt><dd>{v}</dd></div>' for k, v in info)}</dl>
      </div>
    </section>{reading}
    <section class="section tint" aria-labelledby="more-h">
      <div class="wrap">
        <div class="section-head row-head"><div><p class="eyebrow">{esc(c['title'])}</p><h2 id="more-h">More apps like this</h2></div><a class="btn btn-line" href="/apps/">All apps</a></div>
        <div class="app-card-grid">{''.join(app_card(x) for x in more)}</div>
      </div>
    </section>
  </main>'''
    app_ld = {"@context": "https://schema.org", "@type": "MobileApplication", "name": a['name'], "description": a['desc'],
              "operatingSystem": "ANDROID", "applicationCategory": "GameApplication" if is_game(a) else "EducationalApplication",
              "url": SITE + path, "installUrl": play_url(a), "image": SITE + icon(a),
              "audience": {"@type": "PeopleAudience", "suggestedMinAge": 0 if all_ages(a) else TERMS.get('min_age', 13)},
              "author": {"@id": f"{SITE}/#org"}, "publisher": {"@type": "Organization", "name": "Enhancerworx", "url": SITE + '/'}}
    if sc:
        app_ld["screenshot"] = [SITE + s for s in sc]
    write(path.lstrip('/'), page(f'{a["name"]} – Android app | Enhancerworx', a['desc'] + ' Get it on Google Play.',
                                 path, body, ld=[app_ld, breadcrumbs(trail)], card='summary', image=SITE + icon(a)))


def build_index():
    trail = [('Home', SITE + '/'), ('Apps', SITE + '/apps/')]
    blocks = ''.join(f'''
        <section class="cat" id="cat-{c['id']}"><div class="cat-head"><h2 class="h-sm">{esc(c['title'])} <span class="count">{sum(1 for a in APPS if a['cat'] == c['id'])}</span></h2><p>{esc(c['blurb'])}</p></div>
          <div class="app-card-grid">{''.join(app_card(a) for a in APPS if a['cat'] == c['id'])}</div></section>''' for c in CATS if any(a['cat'] == c['id'] for a in APPS))
    body = f'''
  <main id="main">
    <div class="page-hero">
      <div class="wrap">
        {crumbs_html(trail)}
        <p class="eyebrow">Our apps</p>
        <h1>Learning apps and games for Android</h1>
        <p class="page-lead">Geography, history, science, maths, programming and puzzle games, all available on Google Play.</p>
      </div>
    </div>
    <div class="wrap section-sm">{blocks}
    </div>
  </main>'''
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Enhancerworx apps",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + app_page(a), "name": a['name']} for i, a in enumerate(APPS)]}
    write('apps/index.html', page('All Enhancerworx apps: learning apps and games for Android', 'Browse every Enhancerworx app: India and world maps, history, science, maths, programming courses and puzzle games on Google Play.',
                                  '/apps/', body, ld=[ld, breadcrumbs(trail)]))


def main(posts):
    for a in APPS:
        build(a, posts)
    build_index()
    print(f'Built {len(APPS)} app pages and apps/index.html')


if __name__ == '__main__':
    import build_blog
    main(build_blog.load_posts())
