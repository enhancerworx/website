#!/usr/bin/env python3
"""Builds the blog from tools/posts/*.html.

Each post file starts with a JSON header inside an HTML comment:
  <!--
  {"title": "...", "description": "...", "date": "YYYY-MM-DD", "order": 1, "category": "...",
   "cover": "geo|sci|tech|biz", "apps": ["slug", ...]}
  -->
followed by the article body in plain HTML (<p>, <h2>, <ul>, <pre><code>, <aside class="callout">).

Output: blog/index.html, blog/<file-name>.html, blog/feed.xml
"""
import glob, json, os, re, sys, datetime
from email.utils import format_datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *  # noqa: E402,F401

SHARE_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M8.6 13.5l6.8 4M15.4 6.5l-6.8 4M21 5a3 3 0 1 1-6 0 3 3 0 0 1 6 0ZM9 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Zm12 7a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>'


def load_posts():
    posts = []
    for f in glob.glob('tools/posts/*.html'):
        raw = open(f, encoding='utf-8').read()
        m = re.match(r'\s*<!--(.*?)-->\s*(.*)', raw, re.S)
        meta = json.loads(m.group(1))
        meta['body'] = m.group(2).strip()
        meta['slug'] = os.path.splitext(os.path.basename(f))[0]
        meta['url'] = f'/blog/{meta["slug"]}.html'
        text = re.sub(r'<[^>]+>', ' ', meta['body'])
        meta['words'] = len(text.split())
        meta['minutes'] = max(1, round(meta['words'] / 200))
        meta['apps'] = [APP[s] for s in meta.get('apps', []) if s in APP]
        posts.append(meta)
    posts.sort(key=lambda p: (p['date'], p.get('order', 0)), reverse=True)
    return posts


def nice_date(d):
    x = datetime.date.fromisoformat(d)
    return f'{x.day} {x:%B %Y}'


def cover(p, big=False):
    icons = ''.join(f'<img src="{icon(a)}" width="64" height="64" alt="" loading="lazy">' for a in p['apps'][:2]) \
        or '<img src="/img/mark.webp" width="64" height="64" alt="" loading="lazy">'
    return f'<div class="cover cover-{p.get("cover", "biz")}{" cover-lg" if big else ""}" aria-hidden="true"><span class="cover-cat">{esc(p["category"])}</span><span class="cover-icons">{icons}</span></div>'


def card(p, featured=False):
    return f'''<article class="post-card{' post-card-featured' if featured else ''}" data-cat="{esc(p['category'])}">
          <a class="post-card-link" href="{p['url']}">
            {cover(p, featured)}
            <div class="post-card-body">
              <p class="post-meta"><span>{esc(p['category'])}</span><span>{p['minutes']} min read</span></p>
              <h3>{esc(p['title'])}</h3>
              <p>{esc(p['description'])}</p>
              <span class="read-more">Read article <span aria-hidden="true">&rarr;</span></span>
            </div>
          </a>
        </article>'''


def app_mini(a):
    return f'''<li class="app-mini">
              <a href="{app_page(a)}"><img src="{icon(a)}" width="48" height="48" alt="" loading="lazy"><span><strong>{esc(a['name'])}</strong><small>{esc(CAT[a['cat']]['title'])} · {age_label(a)}</small></span></a>
              <a class="app-go" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">Install on Google Play<span class="sr"> {esc(a['name'])} on Google Play (opens in a new tab)</span></a>
            </li>'''


def build_post(p, posts):
    trail = [('Home', SITE + '/'), ('Blog', SITE + '/blog/'), (p['title'], SITE + p['url'])]
    related = [q for q in posts if q is not p][:3]
    aside_apps = ''.join(app_mini(a) for a in p['apps'])
    aside = f'''<aside class="post-aside" aria-label="Related apps">
          {f'<div class="aside-box"><h2>Apps in this article</h2><ul class="app-minis">{aside_apps}</ul></div>' if aside_apps else ''}
          <div class="aside-box aside-cta">
            <h2>Building a learning app?</h2>
            <p>We design and build educational apps for schools, institutes and publishers.</p>
            <a class="btn btn-solid btn-sm" href="/#contact">Start a project</a>
          </div>
          <button class="btn btn-line btn-sm share-btn" type="button" data-share="{SITE + p['url']}" data-title="{esc(p['title'])}">{SHARE_SVG}<span>Share article</span></button>
          <p class="share-note" role="status" aria-live="polite"></p>
        </aside>'''
    body = f'''
  <main id="main">
    <article class="post">
      <header class="post-hero">
        <div class="wrap post-hero-grid">
          <div>
            {crumbs_html(trail)}
            <p class="eyebrow">{esc(p['category'])}</p>
            <h1>{esc(p['title'])}</h1>
            <p class="page-lead">{esc(p['description'])}</p>
            <p class="post-byline"><img src="/img/mark.webp" width="32" height="32" alt=""><span>By <strong>Enhancerworx team</strong><br><time datetime="{p['date']}">{nice_date(p['date'])}</time> · {p['minutes']} min read</span></p>
          </div>
          {cover(p, True)}
        </div>
      </header>
      <div class="wrap post-layout">
        <div class="prose">
{p['body']}
        </div>
        {aside}
      </div>
    </article>
    <section class="section tint" aria-labelledby="more-h">
      <div class="wrap">
        <div class="section-head row-head"><div><p class="eyebrow">Keep reading</p><h2 id="more-h">More from the blog</h2></div><a class="btn btn-line" href="/blog/">All articles</a></div>
        <div class="post-grid">{''.join(card(q) for q in related)}</div>
      </div>
    </section>
  </main>'''
    ld = [{"@context": "https://schema.org", "@type": "BlogPosting", "headline": p['title'], "description": p['description'],
           "datePublished": p['date'], "dateModified": p.get('updated', p['date']), "articleSection": p['category'],
           "wordCount": p['words'], "image": OG_DEFAULT, "mainEntityOfPage": SITE + p['url'], "inLanguage": "en-IN",
           "author": {"@type": "Organization", "name": "Enhancerworx", "url": SITE + '/'},
           "publisher": {"@type": "Organization", "name": "Enhancerworx", "logo": {"@type": "ImageObject", "url": SITE + '/icon-512.png'}}},
          breadcrumbs(trail)]
    extra = f'\n  <meta property="article:published_time" content="{p["date"]}">\n  <meta property="article:section" content="{esc(p["category"])}">'
    write(p['url'].lstrip('/'), page(p['title'] if len(p['title']) > 55 else f'{p["title"]} | Enhancerworx', p['description'], p['url'], body,
                                      active='Blog', og_type='article', ld=ld, extra=extra))


def build_index(posts):
    cats = []
    for p in posts:
        if p['category'] not in cats:
            cats.append(p['category'])
    chips = '<button type="button" class="chip is-active" data-filter="">All</button>' + ''.join(
        f'<button type="button" class="chip" data-filter="{esc(c)}">{esc(c)}</button>' for c in cats)
    trail = [('Home', SITE + '/'), ('Blog', SITE + '/blog/')]
    body = f'''
  <main id="main">
    <div class="page-hero">
      <div class="wrap">
        {crumbs_html(trail)}
        <p class="eyebrow">Blog</p>
        <h1>Study guides and ideas for better learning</h1>
        <p class="page-lead">Practical guides for students preparing for exams, developers learning new skills, and institutions planning learning apps.</p>
      </div>
    </div>
    <div class="wrap section-sm">
      <div class="filters blog-filters" role="group" aria-label="Filter articles by topic">{chips}</div>
      <div class="post-grid post-grid-index" id="postGrid">
        {card(posts[0], True)}
        {''.join(card(p) for p in posts[1:])}
      </div>
    </div>
  </main>'''
    ld = [{"@context": "https://schema.org", "@type": "Blog", "name": "Enhancerworx Blog", "url": SITE + '/blog/',
           "publisher": {"@type": "Organization", "name": "Enhancerworx"},
           "blogPost": [{"@type": "BlogPosting", "headline": p['title'], "url": SITE + p['url'], "datePublished": p['date']} for p in posts]},
          breadcrumbs(trail)]
    write('blog/index.html', page('Blog: study guides, exam tips and app development | Enhancerworx',
                                  'Study guides for UPSC, SSC and board exams, programming tutorials for beginners, and advice for schools planning a learning app.',
                                  '/blog/', body, active='Blog', ld=ld))


def build_feed(posts):
    items = ''.join(f'''
    <item>
      <title>{esc(p['title'])}</title>
      <link>{SITE + p['url']}</link>
      <guid isPermaLink="true">{SITE + p['url']}</guid>
      <pubDate>{format_datetime(datetime.datetime.fromisoformat(p['date'] + 'T09:00:00+05:30'))}</pubDate>
      <category>{esc(p['category'])}</category>
      <description>{esc(p['description'])}</description>
    </item>''' for p in posts)
    write('blog/feed.xml', f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>Enhancerworx Blog</title>
    <link>{SITE}/blog/</link>
    <atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>
    <description>Study guides, programming tutorials and learning-app advice from Enhancerworx.</description>
    <language>en-in</language>{items}
  </channel>
</rss>
''')


def latest_cards(posts, n=3):
    return '\n'.join(card(p) for p in posts[:n])


def main():
    posts = load_posts()
    for p in posts:
        build_post(p, posts)
    build_index(posts)
    build_feed(posts)
    print(f'Built {len(posts)} blog posts, blog/index.html and blog/feed.xml')
    return posts


if __name__ == '__main__':
    main()
