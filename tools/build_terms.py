#!/usr/bin/env python3
"""Builds one Terms of Service page per app (terms/<slug>.html) and the index (terms/index.html).

Data: tools/apps.json (apps) and tools/terms.json (developer details, dates, ages, app-specific clauses).
Usually run through tools/build.py.
"""
import csv, os, sys
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *  # noqa: E402,F401  (tools/layout.py)

T = TERMS
DATE = T['effective_date']
LAW = T['governing_law']
MIN_AGE = T.get('min_age', 13)


def ul(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def eligibility(a):
    if all_ages(a):
        return f'''
      <p>The App is a casual game suitable for players of all ages, including children.</p>
      <p>If you are under {MIN_AGE}, please use the App with the involvement of a parent or legal guardian. If you are under the age of majority where you live (18 in India), a parent or legal guardian must agree to these Terms on your behalf. They are responsible for your use of the App, including any purchases.</p>
      <p>Parents can manage purchases, ads preferences and screen time using Google Play&rsquo;s parental controls and Google Family Link.</p>'''
    return f'''
      <p><strong>The App is intended for users aged {MIN_AGE} and over.</strong> It is not directed at children under {MIN_AGE}, and children under {MIN_AGE} must not use it. We do not knowingly collect personal information from children under {MIN_AGE}. If you believe a child under {MIN_AGE} is using the App, please contact us.</p>
      <p>If you are {MIN_AGE} or older but under the age of majority where you live (18 in India), you may use the App only with the consent of a parent or legal guardian, who accepts these Terms on your behalf and is responsible for your use of the App, including any purchases.</p>'''


def sections_for(a):
    name = esc(a['name'])
    A = f'<strong>{name}</strong>'
    skip_cat = a['slug'] in T.get('skip_category_clauses', [])
    cat_clauses = [] if skip_cat else T['categories'].get(a['cat'], {}).get('content', [])
    app_clauses = T['apps'].get(a['slug'], [])
    pkg = a.get('pkg')
    pp_line = f'The <a href="{privacy_page(a)}">Privacy Policy for the App</a> is also linked on its Google Play listing, under App support.'
    game = is_game(a)
    tech = a['cat'] == 'tech'

    S = []
    S.append(('about', 'About these terms', f'''
      <p>These Terms of Service (the &ldquo;Terms&rdquo;) are an agreement between you and {esc(DEV['name'])} (&ldquo;Enhancerworx&rdquo;, &ldquo;we&rdquo;, &ldquo;us&rdquo; or &ldquo;our&rdquo;), the developer and publisher of the mobile application {A}{f' (package name <code>{esc(pkg)}</code>)' if pkg else ''} (the &ldquo;App&rdquo;).</p>
      <p>These Terms apply only to the App. By downloading, installing or using the App, you agree to them. If you do not agree, do not use the App and uninstall it.</p>
      <p>Your use of Google Play is also governed by Google&rsquo;s own terms. If these Terms conflict with the Google Play Terms of Service on a matter that Google Play governs, such as payments and refunds through Google Play, Google&rsquo;s terms apply to that matter.</p>'''))
    S.append(('eligibility', f'Age requirements ({age_label(a)})', eligibility(a)))
    S.append(('licence', 'Your licence to use the App', f'''
      <p>We give you a personal, limited, non-exclusive, non-transferable and revocable licence to install and use the App on Android devices that you own or control, for your own non-commercial {'enjoyment' if game else 'learning'}.</p>
      <p>You must not:</p>
      {ul(['copy, sell, rent, sublicense or redistribute the App or its content;',
           'reverse engineer, decompile or modify the App, except where the law expressly allows it;',
           'extract, scrape or republish questions, notes, maps, diagrams, videos, levels or other content from the App;',
           'remove copyright or other notices, or use the App to build a competing product;',
           'use the App in any unlawful way or in a way that harms the App, other users or us.'])}'''))
    intro = ('<p>The App is provided for entertainment and light learning.</p>' if game else
             '<p>We work hard to keep the App accurate and up to date, but we cannot promise that every lesson, answer, map or explanation is complete, current or free of errors. Use the App as one source among others, and check important facts against official or authoritative material.</p>')
    S.append(('content', 'Game content and fair play' if game else 'Learning content', intro + ''.join(f'<p>{c}</p>' for c in cat_clauses + app_clauses)))
    S.append(('your-data', 'Your data, notes and progress', f'''
      <p>Progress, scores, favourites, notes and settings are generally saved on your device. If you uninstall the App, clear its data or change devices, this information may be lost unless the App offers a backup option and you have used it.</p>
      <p>Any notes or other content you create in the App remain yours. You are responsible for what you create and must not use the App to store or share unlawful content.</p>
      <p>{pp_line} It explains what data the App and its service providers collect and how it is used. Our website privacy policy is at <a href="/privacyPolicy.html">{SITE.replace("https://", "")}/privacyPolicy.html</a>.</p>'''))
    ads_kids = (' Where the App may be used by children, ads are intended to be suitable for a general audience, in line with Google Play&rsquo;s policies.' if all_ages(a) else '')
    S.append(('ads-purchases', 'Ads, purchases and subscriptions', f'''
      <p>The App may be free to download and may show advertising, including ads served by Google AdMob. Ads are provided by third parties, and we are not responsible for the products or services they advertise.{ads_kids} Some apps let you watch an optional ad in exchange for a reward; rewards have no monetary value.</p>
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
      <p>Other names, logos and trademarks that appear in the App belong to their respective owners{', and are used only to identify the subjects taught' if tech else ''}.</p>'''))
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
      <p>These Terms are governed by {esc(LAW)}. Before starting any formal claim, please contact us so we can try to resolve the issue informally. Subject to the next paragraph, the courts of India have jurisdiction over any dispute relating to the App.</p>
      <p>If you are a consumer living in another country, you also keep the protection of the mandatory laws of that country and may bring a claim in its courts.</p>'''))
    addr = f'<p><strong>Address:</strong> {esc(DEV["address"])}</p>' if DEV.get('address') else f'<p><strong>Country:</strong> {esc(DEV["country"])}</p>'
    S.append(('contact', 'Contact us', f'''
      <p>For questions about these Terms or the App, or to report a problem, contact the developer:</p>
      <div class="contact-card">
        <p><strong>{esc(DEV['name'])}</strong>, developer of {name}</p>
        <p><strong>Email:</strong> <a href="mailto:{DEV['email']}?subject={esc(quote(a['name'] + ' - Terms of Service'))}">{DEV['email']}</a></p>
        <p><strong>Website:</strong> <a href="/">{SITE.replace("https://", "")}</a></p>
        {addr}
      </div>'''))
    return S


def build_app(a):
    secs = sections_for(a)
    name = esc(a['name'])
    toc = ''.join(f'<li><a href="#{sid}">{esc(t)}</a></li>' for sid, t, _ in secs)
    body_secs = ''.join(f'\n        <section id="{sid}"><h2><span class="n">{i}.</span>{esc(t)}</h2>{b}\n        </section>'
                        for i, (sid, t, b) in enumerate(secs, 1))
    pkg = a.get('pkg')
    meta = [f'<span><strong>Effective:</strong> {DATE}</span>', f'<span><strong>Age:</strong> {age_label(a)}</span>',
            f'<span><strong>Developer:</strong> {esc(DEV["name"])}</span>']
    if pkg:
        meta.append(f'<span><strong>Package:</strong> {esc(pkg)}</span>')
    game = is_game(a)
    summary = ul([
        f'These terms apply to the {name} app published on Google Play by {esc(DEV["name"])}.',
        ('Suitable for all ages. Children under 13 should play with a parent or guardian involved.' if all_ages(a)
         else f'The App is for users aged {MIN_AGE} and over. Users under 18 need a parent or guardian&rsquo;s consent.'),
        'You may use the App for your own personal, non-commercial ' + ('enjoyment.' if game else 'learning.'),
        'In-game items have no monetary value.' if game else 'Content is for learning and may contain errors; check important facts against official sources.',
        'Payments, subscriptions and refunds go through Google Play.',
        f'Questions? Email <a href="mailto:{DEV["email"]}">{DEV["email"]}</a>.'])
    path = terms_page(a)
    trail = [('Home', SITE + '/'), ('App terms', SITE + '/terms/'), (a['name'], SITE + path)]
    body = f'''
  <main id="main">
    <div class="page-hero">
      <div class="wrap">
        {crumbs_html(trail)}
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
        <div class="summary"><h2>In short</h2>{summary}<p class="summary-note">This summary is for convenience. The full terms below are what apply.</p></div>{body_secs}
        <div class="terms-foot-nav">
          <a class="btn btn-solid btn-sm" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">View on Google Play<span class="sr"> (opens in a new tab)</span></a>
          <a class="btn btn-line btn-sm" href="{privacy_page(a)}">Privacy Policy</a>
          <a class="btn btn-line btn-sm" href="{app_page(a)}">About this app</a>
          <a class="btn btn-line btn-sm" href="/terms/">Terms for our other apps</a>
        </div>
      </article>
    </div>
  </main>'''
    write(path.lstrip('/'), page(f'Terms of Service – {a["name"]} | Enhancerworx',
                                 f'Terms of Service for the {a["name"]} Android app by Enhancerworx. Age requirement: {age_label(a)}.',
                                 path, body, ld=[breadcrumbs(trail)], card='summary', image=SITE + icon(a)))
    return SITE + path


def build_index():
    blocks = []
    for c in CATS:
        items = [a for a in APPS if a['cat'] == c['id']]
        if not items:
            continue
        links = ''.join(f'<a href="{terms_page(a)}"><img src="{icon(a)}" width="44" height="44" alt="" loading="lazy">'
                        f'<span>{esc(a["name"])}<small>{esc(a["pkg"]) if a.get("pkg") else "Terms of Service"} · {age_label(a)}</small></span></a>' for a in items)
        blocks.append(f'<h2 class="terms-index-cat">{esc(c["title"])}</h2><div class="terms-index">{links}</div>')
    trail = [('Home', SITE + '/'), ('App terms', SITE + '/terms/')]
    body = f'''
  <main id="main">
    <div class="page-hero">
      <div class="wrap">
        {crumbs_html(trail)}
        <p class="eyebrow">Legal</p>
        <h1>App Terms of Service</h1>
        <p class="page-lead">Each Enhancerworx app has its own terms. Choose an app to read them. Effective {DATE}.</p>
      </div>
    </div>
    <div class="wrap section-sm">
      {''.join(blocks)}
      <p class="muted terms-index-foot">For this website, see the <a href="/termsOfService.html">website terms</a> and <a href="/privacyPolicy.html">privacy policy</a>.</p>
    </div>
  </main>'''
    write('terms/index.html', page('App Terms of Service | Enhancerworx', 'Terms of Service for each Enhancerworx app on Google Play.',
                                   '/terms/', body, ld=[breadcrumbs(trail)]))


def main():
    urls = [build_app(a) for a in APPS]
    build_index()
    print(f'Built {len(urls)} app terms pages and terms/index.html')
    return urls


if __name__ == '__main__':
    main()
