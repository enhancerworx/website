#!/usr/bin/env python3
"""Builds one privacy policy page per app (privacy/<slug>.html) and the index (privacy/index.html).

Data: tools/apps.json (apps), tools/terms.json (developer details, ages) and tools/privacy.json
(third-party services, permissions and on-device data per app). Usually run through tools/build.py.
"""
import json, os, sys
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from layout import *  # noqa: E402,F401

P = json.load(open('tools/privacy.json', encoding='utf-8'))
DATE = P['effective_date']
MIN_AGE = TERMS.get('min_age', 13)


def privacy_page(a):
    return f'/privacy/{a["slug"]}.html'


def ul(items):
    return '<ul>' + ''.join(f'<li>{x}</li>' for x in items) + '</ul>'


def cfg(a):
    return P['apps'].get(a['slug'], {})


def services(a):
    return [P['services'][k] for k in cfg(a).get('services', P['default_services'])]


def sections_for(a):
    name = esc(a['name'])
    c = cfg(a)
    svc = services(a)
    names = [s['name'] for s in svc]
    has = lambda n: n in names
    perms = c.get('permissions', [])
    on_device = ['learning progress, scores and quiz results', 'settings and preferences'] + c.get('on_device', [])
    kids = all_ages(a)
    pkg = a.get('pkg')
    S = []

    S.append(('intro', 'Introduction', f'''
      <p>This Privacy Policy explains how {esc(DEV['name'])} (&ldquo;Enhancerworx&rdquo;, &ldquo;we&rdquo;, &ldquo;us&rdquo; or &ldquo;our&rdquo;) handles information when you use the mobile application <strong>{name}</strong>{f' (package name <code>{esc(pkg)}</code>)' if pkg else ''} (the &ldquo;App&rdquo;), available on Google Play.</p>
      <p>We built the App to help people learn, not to collect data. The App does not require you to create an account or sign in. Most of what you do in the App stays on your device. Some information is collected by trusted third-party services that help us show ads, understand how the App is used, fix problems and send notifications. This policy explains what that information is, why it is collected and the choices you have.</p>
      <p>By using the App, you agree to this policy. If you do not agree, please do not use the App. This policy should be read together with the App&rsquo;s <a href="{terms_page(a)}">Terms of Service</a>.</p>'''))

    rows = [('Account or sign-in', 'Not required'),
            ('Information you type in the App', 'Stays on your device'),
            ('Advertising', 'Google AdMob' if has('Google AdMob') else 'None'),
            ('Analytics and crash reporting', 'Google Analytics for Firebase' if has('Google Analytics for Firebase') else 'None'),
            ('Push notifications', 'OneSignal (you can turn these off)' if has('OneSignal') else 'None'),
            ('We sell your personal data', 'Never'),
            ('Age', 'All ages' if kids else f'{MIN_AGE} and over')]
    S.append(('summary', 'Summary', '<div class="table-wrap"><table class="kv"><tbody>' + ''.join(f'<tr><th scope="row">{k}</th><td>{v}</td></tr>' for k, v in rows) + '</tbody></table></div>'))

    S.append(('collect', 'Information we collect', f'''
      <h3>Information stored only on your device</h3>
      <p>The App saves the following on your device so it can work and remember your progress. We do not upload it to our servers:</p>
      {ul([esc(x[0].upper() + x[1:]) for x in on_device])}
      <p>This information is deleted when you clear the App&rsquo;s data or uninstall the App. If your device&rsquo;s own Android backup is turned on, Android may back up App data to your Google account under Google&rsquo;s terms.</p>
      <h3>Information collected automatically by third-party services</h3>
      <p>When you use the App, the services described in the next section may automatically collect:</p>
      {ul(['<strong>Device identifiers</strong>, such as the Android advertising ID, an app-instance ID and a push-notification token;',
           '<strong>Device and network information</strong>, such as device model, operating system version, language, screen size, mobile carrier and IP address;',
           '<strong>Approximate location</strong>, worked out from your IP address (the App does not access your precise GPS location);',
           '<strong>Usage information</strong>, such as screens viewed, features used, session length, and when you install, open or update the App;',
           '<strong>Ad information</strong>, such as which ads were shown or tapped;',
           '<strong>Diagnostics and log data</strong>, such as crash reports, error logs, the App&rsquo;s configuration at the time of an error, and the date and time of use.'])}
      <h3>Information you choose to send us</h3>
      <p>If you email us for support or feedback, we receive your email address and whatever you include in your message. We use it only to reply to you and to improve the App.</p>
      <p>We do not ask for, and the App does not collect, your name, phone number, contacts, precise location, or payment card details. Any purchases are handled entirely by Google Play.</p>'''))

    svc_rows = ''.join(f'<tr><th scope="row">{esc(s["name"])}</th><td>{esc(s["purpose"])}</td><td><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">Privacy policy<span class="sr"> of {esc(s["name"])} (opens in a new tab)</span></a></td></tr>' for s in svc)
    video = ('<p>Some lessons may play videos hosted by a third-party video service. When you play such a video, that service may collect information under its own privacy policy.</p>'
             if c.get('videos') else '')
    S.append(('third-parties', 'Third-party services we use', f'''
      <p>The App uses the following third-party services. Each one collects and processes information under its own privacy policy, which we encourage you to read.</p>
      <div class="table-wrap"><table class="svc"><thead><tr><th scope="col">Service</th><th scope="col">What it does</th><th scope="col">Policy</th></tr></thead><tbody>{svc_rows}</tbody></table></div>
      {video}'''))

    S.append(('use', 'How we use information', f'''
      <p>We use the information described above to:</p>
      {ul(['provide the App&rsquo;s features and remember your progress on your device;',
           'show ads, which keep the App free to download, and measure how they perform;',
           'understand which lessons and features are useful, so we can improve them;',
           'find and fix crashes and other technical problems;',
           'send push notifications you have allowed, such as study reminders or news about new content;',
           'reply to your messages and support requests;',
           'detect and prevent fraud, abuse and security problems, including invalid ad activity;',
           'comply with the law and enforce our <a href="' + terms_page(a) + '">Terms of Service</a>.'])}
      <p>We process this information on the basis of your consent (for example, when you allow notifications or agree to personalised ads), to provide the App you asked for, and for our legitimate interest in keeping the App working, secure and free.</p>'''))

    perm_items = [('Internet and network access', 'To load ads, send analytics and crash reports, and download content where needed.'),
                  ('Notifications', 'To show push notifications. On Android 13 and later the App asks your permission first.'),
                  ('Advertising ID', 'Used by Google AdMob and Google Analytics for Firebase as described above.')] + [tuple(p) for p in perms]
    S.append(('permissions', 'Device permissions', '<p>The App asks only for the permissions it needs:</p><div class="table-wrap"><table class="kv"><tbody>' + ''.join(
        f'<tr><th scope="row">{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in perm_items) + '</tbody></table></div><p>You can review or withdraw permissions at any time in your phone&rsquo;s Settings &gt; Apps &gt; ' + name + ' &gt; Permissions.</p>'))

    ads_kids = (f'<p>Because the App is suitable for all ages, it may be used by children. Where the App knows or is told that a user is a child, ads are limited to non-personalised ads suitable for children, in line with Google Play&rsquo;s Families policy.</p>' if kids else '')
    S.append(('ads', 'Advertising and your ad choices', f'''
      <p>The App shows ads served by Google AdMob. Ads may be personalised based on your activity in this and other apps, or non-personalised, depending on your choices and the law where you live.</p>
      <p>If you are in the European Economic Area, the United Kingdom or Switzerland, the App asks for your consent before personalised ads are shown, and you can change your choice from the App&rsquo;s settings or privacy options where available.</p>
      <p>You can also control ads on your device:</p>
      {ul(['to delete or reset your advertising ID, open <strong>Settings &gt; Privacy &gt; Ads</strong> on your Android device (the wording may differ slightly on some phones);',
           'to manage ad personalisation across Google services, visit <a href="https://myadcenter.google.com/" target="_blank" rel="noopener noreferrer">My Ad Center</a>.'])}
      {ads_kids}'''))

    S.append(('notifications', 'Push notifications', '''
      <p>If you allow notifications, the App may send you reminders and news about new content through OneSignal. You can turn notifications off at any time in your phone&rsquo;s Settings &gt; Notifications, or in the App&rsquo;s settings where available.</p>''' if has('OneSignal') else '<p>The App does not send push notifications.</p>'))

    S.append(('cookies', 'Cookies and similar technologies', '''
      <p>The App does not use cookies itself. However, the third-party services listed above may use cookies, software development kits (SDKs) and similar technologies, such as device identifiers, to collect information and improve their services. You can limit this using the ad and notification choices described in this policy. If you refuse some of these technologies, parts of the App may not work as intended.</p>'''))

    S.append(('sharing', 'How information is shared', '''
      <p><strong>We do not sell your personal information.</strong> We share information only:</p>
      <ul>
        <li>with the service providers listed above, who process it to provide their services to us and are not allowed to use it for other purposes except as described in their own policies;</li>
        <li>when required by law, a court order or a lawful request from a public authority;</li>
        <li>when needed to protect the rights, property or safety of Enhancerworx, our users or others, including to prevent fraud;</li>
        <li>if Enhancerworx is involved in a merger, acquisition or sale of assets, in which case the information would remain protected by this policy or an equivalent one.</li>
      </ul>'''))

    S.append(('transfers', 'Where information is processed', '''
      <p>Enhancerworx is based in India. Our service providers may store and process information in other countries, including the United States, where data-protection laws may differ from those in your country. Where required, these providers use appropriate safeguards, such as standard contractual clauses, to protect your information.</p>'''))

    S.append(('retention', 'How long information is kept', '''
      <p>Information stored on your device stays there until you clear the App&rsquo;s data or uninstall the App. Information collected by third-party services is kept for the period set by each provider and by our settings with them, after which it is deleted or anonymised. Support emails are kept only as long as needed to help you and keep a record of our conversation.</p>'''))

    S.append(('security', 'Security', '''
      <p>We value your trust and use commercially reasonable measures to protect information, and we choose service providers that protect data with industry-standard security. However, no method of transmission over the internet or electronic storage is completely secure, so we cannot guarantee absolute security.</p>'''))

    S.append(('rights', 'Your rights and choices', f'''
      <p>Depending on where you live, including under India&rsquo;s Digital Personal Data Protection Act, 2023 and the EU and UK General Data Protection Regulation, you may have the right to:</p>
      {ul(['ask what personal information we hold about you and get a copy;',
           'ask us to correct or update it;',
           'ask us to delete it;',
           'withdraw consent you have given, such as for personalised ads or notifications;',
           'object to or restrict certain processing;',
           'complain to a data-protection authority.'])}
      <p>Because the App has no accounts, we usually cannot link information held by third-party services to you by name. To make a request, email us at <a href="mailto:{DEV['email']}?subject={esc(quote(a['name'] + ' - privacy request'))}">{DEV['email']}</a> with the App&rsquo;s name and details of your request. We will respond within the time required by law. You can also stop all collection by the App at any time by uninstalling it.</p>'''))

    if kids:
        child = f'''
      <p>The App is a casual game suitable for all ages, so children may use it. We do not knowingly collect personal information from children under {MIN_AGE} beyond what is permitted by law and by Google Play&rsquo;s Families policy, and we do not ask children to provide personal information. Where a user is a child, ads are limited to non-personalised ads suitable for children.</p>
      <p>Parents and guardians can manage their child&rsquo;s use of the App with Google Play parental controls and Google Family Link. If you believe your child has provided us with personal information, please contact us and we will delete it promptly.</p>'''
    else:
        child = f'''
      <p>The App is intended for users aged {MIN_AGE} and over and is not directed at children under {MIN_AGE}. We do not knowingly collect personal information from children under {MIN_AGE}. If we learn that a child under {MIN_AGE} has provided us with personal information, we will delete it promptly. If you are a parent or guardian and believe your child has provided us with personal information, please contact us so that we can take the necessary action.</p>
      <p>Users who are {MIN_AGE} or older but under 18 should use the App with the consent of a parent or guardian.</p>'''
    S.append(('children', 'Children&rsquo;s privacy', child))

    S.append(('links', 'Links to other sites', '''
      <p>The App may contain links to websites, videos or other apps that we do not operate. If you follow such a link, the other party&rsquo;s privacy policy applies. We have no control over, and are not responsible for, their content or practices.</p>'''))

    S.append(('changes', 'Changes to this policy', '''
      <p>We may update this Privacy Policy from time to time, for example when we add features or change service providers. We will post the updated policy on this page with a new effective date. If a change is significant, we will take reasonable steps to tell you, for example through the App. Please review this page periodically.</p>'''))

    addr = f'<p><strong>Address:</strong> {esc(DEV["address"])}</p>' if DEV.get('address') else f'<p><strong>Country:</strong> {esc(DEV["country"])}</p>'
    S.append(('contact', 'Contact us', f'''
      <p>If you have any questions, requests or complaints about this Privacy Policy or how the App handles information, please contact us. We aim to reply within a few working days.</p>
      <div class="contact-card">
        <p><strong>{esc(DEV['name'])}</strong>, developer of {name}</p>
        <p><strong>Email (including grievances):</strong> <a href="mailto:{DEV['email']}?subject={esc(quote(a['name'] + ' - Privacy'))}">{DEV['email']}</a></p>
        <p><strong>Website:</strong> <a href="/">{SITE.replace("https://", "")}</a></p>
        {addr}
      </div>'''))
    return S


def build_app(a):
    secs = sections_for(a)
    name = esc(a['name'])
    toc = ''.join(f'<li><a href="#{sid}">{t}</a></li>' for sid, t, _ in secs)
    body_secs = ''.join(f'\n        <section id="{sid}"><h2><span class="n">{i}.</span>{t}</h2>{b}\n        </section>' for i, (sid, t, b) in enumerate(secs, 1))
    pkg = a.get('pkg')
    meta = [f'<span><strong>Effective:</strong> {DATE}</span>', f'<span><strong>Age:</strong> {age_label(a)}</span>', f'<span><strong>Developer:</strong> {esc(DEV["name"])}</span>']
    if pkg:
        meta.append(f'<span><strong>Package:</strong> {esc(pkg)}</span>')
    path = privacy_page(a)
    trail = [('Home', SITE + '/'), ('App privacy', SITE + '/privacy/'), (a['name'], SITE + path)]
    body = f'''
  <main id="main">
    <div class="page-hero">
      <div class="wrap">
        {crumbs_html(trail)}
        <div class="terms-id">
          <img src="{icon(a)}" width="76" height="76" alt="">
          <div>
            <p class="eyebrow">Privacy Policy</p>
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
      <article class="terms-body">{body_secs}
        <div class="terms-foot-nav">
          <a class="btn btn-solid btn-sm" href="{esc(play_url(a))}" target="_blank" rel="noopener noreferrer">View on Google Play<span class="sr"> (opens in a new tab)</span></a>
          <a class="btn btn-line btn-sm" href="{terms_page(a)}">Terms of Service</a>
          <a class="btn btn-line btn-sm" href="/privacy/">Privacy policies for our other apps</a>
        </div>
      </article>
    </div>
  </main>'''
    write(path.lstrip('/'), page(f'Privacy Policy – {a["name"]} | Enhancerworx',
                                 f'Privacy Policy for the {a["name"]} Android app by Enhancerworx: what data is collected, how it is used and your choices.',
                                 path, body, ld=[breadcrumbs(trail)], card='summary', image=SITE + icon(a)))
    return SITE + path


def build_index():
    blocks = []
    for c in CATS:
        items = [a for a in APPS if a['cat'] == c['id']]
        if not items:
            continue
        links = ''.join(f'<a href="{privacy_page(a)}"><img src="{icon(a)}" width="44" height="44" alt="" loading="lazy">'
                        f'<span>{esc(a["name"])}<small>{esc(a["pkg"]) if a.get("pkg") else "Privacy Policy"}</small></span></a>' for a in items)
        blocks.append(f'<h2 class="terms-index-cat">{esc(c["title"])}</h2><div class="terms-index">{links}</div>')
    trail = [('Home', SITE + '/'), ('App privacy', SITE + '/privacy/')]
    body = f'''
  <main id="main">
    <div class="page-hero">
      <div class="wrap">
        {crumbs_html(trail)}
        <p class="eyebrow">Legal</p>
        <h1>App Privacy Policies</h1>
        <p class="page-lead">Each Enhancerworx app has its own privacy policy. Choose an app to read it. Effective {DATE}.</p>
      </div>
    </div>
    <div class="wrap section-sm">
      {''.join(blocks)}
      <p class="muted terms-index-foot">For this website, see the <a href="/privacyPolicy.html">website privacy policy</a>. Terms of service for each app are <a href="/terms/">here</a>.</p>
    </div>
  </main>'''
    write('privacy/index.html', page('App Privacy Policies | Enhancerworx', 'Privacy policies for each Enhancerworx app on Google Play.', '/privacy/', body, ld=[breadcrumbs(trail)]))


def main():
    urls = [build_app(a) for a in APPS]
    build_index()
    print(f'Built {len(urls)} app privacy pages and privacy/index.html')
    return urls


if __name__ == '__main__':
    main()
