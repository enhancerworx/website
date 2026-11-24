#!/usr/bin/env python3
"""Builds one Terms of Service page per app, plus an index, from tools/apps.json and tools/terms.json.

Output:
  terms/<slug>.html   -> https://www.enhancerworx.in/terms/<slug>.html  (paste this URL into Play Console)
  terms/index.html    -> https://www.enhancerworx.in/terms/
  sitemap.xml         -> rewritten to include every page
  tools/terms-urls.csv-> app name, package and terms URL, for easy copying

Run on its own (python3 tools/build_terms.py) or via tools/build_apps.py, which calls it.
"""
import json, html, os, csv
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
apps_data = json.load(open('tools/apps.json', encoding='utf-8'))
T = json.load(open('tools/terms.json', encoding='utf-8'))
DEV = T['developer']
SITE = DEV['website'].rstrip('/')
DATE = T['effective_date']
LAW = T['governing_law']
esc = lambda s: html.escape(s, quote=True)
cats = {c['id']: c for c in apps_data['categories']}
apps = apps_data['apps']
DEV_URL = apps_data['developer_url']

THEME_SVG = ('<svg class="i-moon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>'
             '<svg class="i-sun" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>')


def play_url(a):
    return f'https://play.google.com/store/apps/details?id={a["pkg"]}' if a.get('pkg') else DEV_URL


def icon(a):
    for ext in ('webp', 'png', 'jpg'):
        if os.path.exists(f"img/app-{a['slug']}.{ext}"):
            return f"/img/app-{a['slug']}.{ext}"
    return '/img/mark.webp'


def page(title, desc, canonical, body, extra_head=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta name="robots" content="index, follow">
  <meta name="color-scheme" content="light dark">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; base-uri 'self'; form-action 'none'; upgrade-insecure-requests">
  <meta name="referrer" content="strict-origin-when-cross-origin">
  <link rel="icon" href="/favicon.ico" sizes="any">
  <link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="preload" href="/fonts/sora-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/fonts/figtree-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
  <script src="/js/theme.js"></script>
  <link rel="stylesheet" href="/css/style.css">{extra_head}
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap bar">
      <a class="brand" href="/" aria-label="Enhancerworx home">
        <img src="/img/mark.webp" width="40" height="40" alt="">
        <span class="brand-name">Enhancer<span>worx</span></span>
      </a>
      <div class="bar-actions">
        <button class="icon-btn" id="themeBtn" type="button" aria-label="Switch to dark theme">{THEME_SVG}</button>
        <a class="btn btn-sm btn-line" href="/">Home</a>
      </div>
    </div>
  </header>
{body}
  <footer class="site-footer">
    <div class="wrap">
      <div class="legal-foot">
        <a class="brand" href="/" aria-label="Enhancerworx home">
          <img src="/img/mark.webp" width="36" height="36" alt="">
          <span class="brand-name">Enhancer<span>worx</span></span>
        </a>
        <nav aria-label="Footer" class="legal-nav">
          <a href="/terms/">App terms of service</a>
          <a href="/privacyPolicy.html">Privacy policy</a>
          <a href="/termsOfService.html">Website terms</a>
          <a href="mailto:{DEV['email']}">{DEV['email']}</a>
        </nav>
      </div>
      <p class="copy">&copy; <span id="year">2026</span> {esc(DEV['name'])}. All rights reserved.</p>
    </div>
  </footer>
  <script src="/js/main.js" defer></script>
</body>
</html>
'''


def ul(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def sections_for(a):
    name = esc(a['name'])
    A = f'<strong>{name}</strong>'
    cat = a['cat']
    skip_cat = a['slug'] in T.get('skip_category_clauses', [])
    cat_clauses = [] if skip_cat else T['categories'].get(cat, {}).get('content', [])
    app_clauses = T['apps'].get(a['slug'], [])
    pkg = a.get('pkg')
    pp_line = (f'The privacy policy for the App is linked on its <a href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">Google Play listing</a>, under App support.'
               if pkg else 'The privacy policy for the App is linked on its Google Play listing, under App support.')
    is_tech = cat == 'tech'
    is_game = cat == 'games' and not skip_cat

    S = []
    S.append(('about', 'About these terms', f'''
      <p>These Terms of Service (the &ldquo;Terms&rdquo;) are an agreement between you and {esc(DEV['name'])} (&ldquo;Enhancerworx&rdquo;, &ldquo;we&rdquo;, &ldquo;us&rdquo; or &ldquo;our&rdquo;), the developer and publisher of the mobile application {A}{f' (package name <code>{esc(pkg)}</code>)' if pkg else ''} (the &ldquo;App&rdquo;).</p>
      <p>These Terms apply only to the App. By downloading, installing or using the App, you agree to them. If you do not agree, do not use the App and uninstall it.</p>
      <p>Your use of Google Play is also governed by Google&rsquo;s own terms. If these Terms conflict with the Google Play Terms of Service on a matter that Google Play governs, such as payments and refunds through Google Play, Google&rsquo;s terms apply to that matter.</p>'''))
    S.append(('eligibility', 'Who can use the App', '''
      <p>The App is designed for learners of all ages. If you are under the age of majority where you live (18 in India), you may use the App only with the involvement and consent of a parent or legal guardian, who accepts these Terms on your behalf and is responsible for your use of the App, including any purchases.</p>'''))
    S.append(('licence', 'Your licence to use the App', f'''
      <p>We give you a personal, limited, non-exclusive, non-transferable and revocable licence to install and use the App on Android devices that you own or control, for your own non-commercial learning and enjoyment.</p>
      <p>You must not:</p>
      {ul(['copy, sell, rent, sublicense or redistribute the App or its content;',
           'reverse engineer, decompile or modify the App, except where the law expressly allows it;',
           'extract, scrape or republish questions, notes, maps, diagrams, videos or other content from the App;',
           'remove copyright or other notices, or use the App to build a competing product;',
           'use the App in any unlawful way or in a way that harms the App, other users or us.'])}'''))

    content_intro = ('<p>We work hard to keep the App accurate and up to date, but we cannot promise that every lesson, answer, map or explanation is complete, current or free of errors. Use the App as one source among others, and check important facts against official or authoritative material.</p>'
                     if not is_game else '<p>The App is provided for entertainment and light learning.</p>')
    extra = cat_clauses + app_clauses
    S.append(('content', 'Learning content' if not is_game else 'Game content and fair play', content_intro + (''.join(f'<p>{c}</p>' for c in extra) if extra else '')))

    S.append(('your-data', 'Your data, notes and progress', f'''
      <p>Progress, scores, favourites, notes and settings are generally saved on your device. If you uninstall the App, clear its data or change devices, this information may be lost unless the App offers a backup option and you have used it.</p>
      <p>Any notes or other content you create in the App remain yours. You are responsible for what you create and must not use the App to store or share unlawful content.</p>
      <p>{pp_line} It explains what data the App and its service providers collect and how it is used. Our website privacy policy is at <a href="/privacyPolicy.html">{SITE.replace("https://", "")}/privacyPolicy.html</a>.</p>'''))
    S.append(('ads-purchases', 'Ads, purchases and subscriptions', f'''
      <p>The App may be free to download and may show advertising, including ads served by Google AdMob. Ads are provided by third parties, and we are not responsible for the products or services they advertise. Some apps let you watch an optional ad in exchange for a reward; rewards have no monetary value.</p>
      <p>The App may offer optional in-app purchases or subscriptions, for example to remove ads or unlock premium content. Where it does:</p>
      {ul(['prices are shown in the App and on Google Play before you pay, and all payments are processed by Google Play Billing; we never see your card or payment details;',
           'subscriptions renew automatically until you cancel them in the Google Play Store app (Profile &gt; Payments and subscriptions &gt; Subscriptions);',
           'refunds are handled under Google Play&rsquo;s refund policies; you can request one through Google Play, or contact us and we will help where we can;',
           'purchases are linked to the Google account used to buy them and can be restored on another device with the same account where the App supports it.'])}
      <p>Whether the App currently contains ads or in-app purchases is shown on its Google Play listing.</p>'''))
    S.append(('third-party', 'Third-party services and links', '''
      <p>The App relies on services provided by others, such as Google Play services and advertising networks, and may link to websites or videos that we do not control. Those services are governed by their own terms and privacy policies, and we are not responsible for their content or availability.</p>'''))
    S.append(('ip', 'Intellectual property', f'''
      <p>The App and its content, including text, questions, illustrations, maps, diagrams, audio, video, design, code and the Enhancerworx name and logo, are owned by or licensed to {esc(DEV['name'])} and are protected by copyright and other laws. Except for the licence above, these Terms do not give you any rights in them.</p>
      <p>Other names, logos and trademarks that appear in the App belong to their respective owners{', and are used only to identify the subjects taught' if is_tech else ''}.</p>'''))
    S.append(('feedback', 'Feedback and reviews', '''
      <p>We welcome suggestions and bug reports. If you send us feedback, you agree that we may use it to improve our apps without any obligation to you. Reviews you post on Google Play are governed by Google Play&rsquo;s policies.</p>'''))
    S.append(('changes-app', 'Updates and availability', '''
      <p>We may update the App from time to time to add features, fix problems or change content, and some updates may be required to keep using it. We may also change or stop offering the App or parts of it. Where you have paid for a feature that we withdraw, we will act fairly, which may include offering a refund or an equivalent alternative, as required by applicable law.</p>
      <p>The App is designed to run on supported Android versions. We cannot guarantee that it will work on every device. Some features may need an internet connection.</p>'''))
    S.append(('disclaimer', 'Disclaimer', '''
      <p>To the fullest extent permitted by law, the App is provided &ldquo;as is&rdquo; and &ldquo;as available&rdquo;, without warranties of any kind, whether express or implied, including warranties of accuracy, fitness for a particular purpose or uninterrupted, error-free operation.</p>'''))
    S.append(('liability', 'Limitation of liability', f'''
      <p>To the fullest extent permitted by law, {esc(DEV['name'])} is not liable for any indirect, incidental, special or consequential loss, or for loss of data, profits, opportunities or exam results, arising from your use of or inability to use the App. Our total liability to you for any claim relating to the App is limited to the amount you paid us for the App in the twelve months before the claim, or INR 1,000 if you paid nothing.</p>
      <p>Nothing in these Terms limits any liability that cannot be limited by law, or any rights you have as a consumer under the mandatory laws of the country where you live.</p>'''))
    S.append(('termination', 'Ending these terms', '''
      <p>You may stop using the App at any time by uninstalling it. We may suspend or end your licence if you seriously or repeatedly break these Terms. Sections that by their nature should continue, such as intellectual property, disclaimer and limitation of liability, survive after the Terms end.</p>'''))
    S.append(('changes-terms', 'Changes to these terms', '''
      <p>We may update these Terms to reflect changes to the App, the law or our business. The updated version will be posted on this page with a new effective date. If a change is significant, we will take reasonable steps to tell you, for example through the App. Continuing to use the App after a change means you accept the updated Terms.</p>'''))
    S.append(('law', 'Governing law and disputes', f'''
      <p>These Terms are governed by {esc(LAW)}. Before starting any formal claim, please contact us so we can try to resolve the issue informally. Subject to the next sentence, the courts of India have jurisdiction over any dispute relating to the App.</p>
      <p>If you are a consumer living in another country, you also keep the protection of the mandatory laws of that country and may bring a claim in its courts.</p>'''))
    addr = f'<p><strong>Address:</strong> {esc(DEV["address"])}</p>' if DEV.get('address') else f'<p><strong>Country:</strong> {esc(DEV["country"])}</p>'
    S.append(('contact', 'Contact us', f'''
      <p>For questions about these Terms or the App, or to report a problem, contact the developer:</p>
      <div class="contact-card">
        <p><strong>{esc(DEV['name'])}</strong>, developer of {name}</p>
        <p><strong>Email:</strong> <a href="mailto:{DEV['email']}?subject={esc(quote(a['name'] + ' - Terms of Service'))}">{DEV['email']}</a></p>
        <p><strong>Phone / WhatsApp:</strong> <a href="tel:{DEV['phone_link']}">{esc(DEV['phone'])}</a></p>
        <p><strong>Website:</strong> <a href="{SITE}/">{SITE.replace("https://", "")}</a></p>
        {addr}
      </div>'''))
    return S


def build_app(a):
    secs = sections_for(a)
    name = esc(a['name'])
    toc = ''.join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t, _ in secs)
    body_secs = ''.join(f'\n    <section id="{sid}"><h2><span class="n">{i}.</span>{esc(t)}</h2>{b}\n    </section>'
                        for i, (sid, t, b) in enumerate(secs, 1))
    pkg = a.get('pkg')
    meta = [f'<span><strong>Effective:</strong> {DATE}</span>', f'<span><strong>Developer:</strong> {esc(DEV["name"])}</span>']
    if pkg:
        meta.append(f'<span><strong>Package:</strong> {esc(pkg)}</span>')
    summary = ul([
        f'These terms apply to the {name} app published on Google Play by {esc(DEV["name"])}.',
        'You may use the App for your own personal, non-commercial learning.' if a['cat'] != 'games' else 'You may use the App for your own personal, non-commercial enjoyment.',
        'Content is for learning and may contain errors; always check important facts against official sources.' if a['cat'] != 'games' else 'In-game items have no monetary value.',
        'Payments, subscriptions and refunds go through Google Play.',
        f'Questions? Email <a href="mailto:{DEV["email"]}">{DEV["email"]}</a>.'])
    canonical = f'{SITE}/terms/{a["slug"]}.html'
    body = f'''
  <main id="main">
    <div class="terms-hero">
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/terms/">App terms</a><span aria-hidden="true">/</span><span>{name}</span></nav>
        <div class="terms-id">
          <img src="{icon(a)}" width="76" height="76" alt="">
          <div>
            <p class="eyebrow">Terms of Service</p>
            <h1>{name}</h1>
          </div>
        </div>
        <div class="terms-meta">{''.join(meta)}</div>
      </div>
    </div>
    <div class="wrap terms-layout">
      <details class="toc" open>
        <summary>On this page</summary>
        <ol>{toc}</ol>
      </details>
      <article class="terms-body">
        <div class="summary"><h2>In short</h2>{summary}<p style="margin-top:.6rem">This summary is for convenience. The full terms below are what apply.</p></div>{body_secs}
        <div class="terms-foot-nav">
          <a class="btn btn-solid btn-sm" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">View on Google Play<span class="sr"> (opens in a new tab)</span></a>
          <a class="btn btn-line btn-sm" href="/terms/">Terms for our other apps</a>
        </div>
      </article>
    </div>
  </main>
'''
    html_out = page(f'Terms of Service - {a["name"]} | Enhancerworx',
                    f'Terms of Service for the {a["name"]} app by Enhancerworx on Google Play.', canonical, body)
    # The inline style above would break the CSP (style-src 'self'); use a class instead.
    html_out = html_out.replace('<p style="margin-top:.6rem">', '<p class="summary-note">')
    os.makedirs('terms', exist_ok=True)
    open(f'terms/{a["slug"]}.html', 'w', encoding='utf-8').write(html_out)
    return canonical


def build_index():
    blocks = []
    for c in apps_data['categories']:
        items = [a for a in apps if a['cat'] == c['id']]
        if not items:
            continue
        links = ''.join(f'<a href="/terms/{a["slug"]}.html"><img src="{icon(a)}" width="44" height="44" alt="" loading="lazy">'
                        f'<span>{esc(a["name"])}<small>{esc(a["pkg"]) if a.get("pkg") else "Terms of Service"}</small></span></a>' for a in items)
        blocks.append(f'<h2 class="terms-index-cat">{esc(c["title"])}</h2><div class="terms-index">{links}</div>')
    body = f'''
  <main id="main" class="legal"><div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><span>App terms</span></nav>
    <h1>App Terms of Service</h1>
    <p class="updated">Each Enhancerworx app has its own terms. Choose an app to read them. Effective {DATE}.</p>
    {''.join(blocks)}
    <p class="updated" style="margin-top:2.5rem">For this website, see the <a href="/termsOfService.html">website terms</a> and <a href="/privacyPolicy.html">privacy policy</a>.</p>
  </div></main>
'''
    out = page('App Terms of Service | Enhancerworx', 'Terms of Service for each Enhancerworx app on Google Play.', f'{SITE}/terms/', body)
    out = out.replace('<p class="updated" style="margin-top:2.5rem">', '<p class="updated terms-index-foot">')
    open('terms/index.html', 'w', encoding='utf-8').write(out)


def build_sitemap(urls):
    core = [f'{SITE}/', f'{SITE}/privacyPolicy.html', f'{SITE}/termsOfService.html', f'{SITE}/terms/']
    lastmod = '2026-11-24'
    rows = ''.join(f'  <url><loc>{u}</loc><lastmod>{lastmod}</lastmod></url>\n' for u in core + urls)
    open('sitemap.xml', 'w', encoding='utf-8').write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + rows + '</urlset>\n')


def main():
    urls = [build_app(a) for a in apps]
    build_index()
    build_sitemap(urls)
    with open('tools/terms-urls.csv', 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['App name', 'Package name', 'Terms of Service URL'])
        for a, u in zip(apps, urls):
            w.writerow([a['name'], a.get('pkg', ''), u])
    print(f'Built {len(urls)} app terms pages, terms/index.html and sitemap.xml.')


if __name__ == '__main__':
    main()
