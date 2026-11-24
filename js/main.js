'use strict';

/* Theme toggle */
(function () {
  var btn = document.getElementById('themeBtn');
  if (!btn) return;
  function label() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    btn.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
  }
  label();
  btn.addEventListener('click', function () {
    var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('ew-theme', next); } catch (e) {}
    label();
  });
})();

/* Mobile menu: slide-down panel, locks page scroll, closes on outside tap */
(function () {
  var btn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  if (!btn || !nav) return;
  function setOpen(open) {
    nav.classList.toggle('open', open);
    document.body.classList.toggle('menu-open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function (e) { e.stopPropagation(); setOpen(!nav.classList.contains('open')); });
  nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
  document.addEventListener('click', function (e) {
    if (nav.classList.contains('open') && !nav.contains(e.target)) setOpen(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); btn.focus(); }
  });
  window.addEventListener('resize', function () { if (window.innerWidth > 820 && nav.classList.contains('open')) setOpen(false); });
})();

/* Highlight the subject chip for the category on screen */
(function () {
  var chips = document.querySelectorAll('.filters .chip');
  if (!chips.length || !('IntersectionObserver' in window)) return;
  var byId = {};
  chips.forEach(function (c) { byId[c.getAttribute('href').slice(1)] = c; });
  var current = null;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var chip = byId[en.target.id];
      if (!chip || chip === current) return;
      if (current) current.classList.remove('is-active');
      chip.classList.add('is-active');
      current = chip;
      var bar = chip.parentNode;
      if (bar.scrollWidth > bar.clientWidth) {
        bar.scrollTo({ left: chip.offsetLeft - bar.offsetLeft - 16, behavior: 'smooth' });
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  document.querySelectorAll('.cat').forEach(function (s) { io.observe(s); });
})();

/* App search */
(function () {
  var input = document.getElementById('appSearch');
  var note = document.getElementById('filterNote');
  var groups = document.querySelectorAll('.cat');
  var items = document.querySelectorAll('#appGroups li');
  if (!input) return;
  var total = items.length;
  input.addEventListener('input', function () {
    var q = input.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (li) {
      var hit = !q || li.getAttribute('data-search').indexOf(q) !== -1;
      li.hidden = !hit;
      if (hit) shown++;
    });
    groups.forEach(function (g) {
      g.hidden = !g.querySelector('li:not([hidden])');
    });
    if (!q) note.textContent = 'Showing all ' + total + ' apps.';
    else if (shown === 0) note.textContent = 'No apps match "' + input.value.trim() + '". Clear the search to see all ' + total + ' apps.';
    else note.textContent = 'Showing ' + shown + ' of ' + total + ' apps.';
  });
})();

/* Footer year */
(function () {
  var y = document.getElementById('year');
  if (y) y.textContent = new Date().getFullYear();
})();

/* App detail dialog (also opens from #app-<slug> links) */
(function () {
  var dlg = document.getElementById('appDialog');
  if (!dlg || typeof dlg.showModal !== 'function') return;
  var el = function (id) { return document.getElementById(id); };
  var items = document.querySelectorAll('#appGroups li[data-slug]');
  var bySlug = {};
  items.forEach(function (li) { bySlug[li.getAttribute('data-slug')] = li; });
  var lastFocus = null;

  function fill(li) {
    var slug = li.getAttribute('data-slug');
    el('dlgName').textContent = li.getAttribute('data-name');
    el('dlgCat').textContent = li.getAttribute('data-cat');
    el('dlgDesc').textContent = li.getAttribute('data-desc');
    var icon = li.getAttribute('data-icon');
    var img = el('dlgIcon');
    if (icon) { img.src = icon; img.hidden = false; } else { img.hidden = true; }
    var pts = el('dlgPoints'); pts.textContent = '';
    (li.getAttribute('data-points') || '').split('|').filter(Boolean).forEach(function (s) {
      var x = document.createElement('li'); x.textContent = s; pts.appendChild(x);
    });
    var shots = el('dlgShots'); shots.textContent = '';
    (li.getAttribute('data-screens') || '').split(',').filter(Boolean).forEach(function (src, n) {
      var im = document.createElement('img');
      im.src = src; im.alt = li.getAttribute('data-name') + ' screenshot ' + (n + 1); im.loading = 'lazy';
      shots.appendChild(im);
    });
    el('dlgPlay').href = li.getAttribute('data-url');
    var terms = el('dlgTerms');
    if (terms) terms.href = li.getAttribute('data-terms') || 'terms/';
    el('dlgNote').textContent = '';
    dlg.setAttribute('data-slug', slug);
  }
  function open(slug, fromHash) {
    var li = bySlug[slug];
    if (!li) return;
    fill(li);
    lastFocus = document.activeElement;
    if (!dlg.open) dlg.showModal();
    document.body.classList.add('dlg-open');
    if (!fromHash) { try { history.replaceState(null, '', '#app-' + slug); } catch (e) {} }
  }
  function closeIt() { if (dlg.open) dlg.close(); }

  dlg.addEventListener('close', function () {
    document.body.classList.remove('dlg-open');
    if (location.hash.indexOf('#app-') === 0) { try { history.replaceState(null, '', location.pathname + location.search + '#apps'); } catch (e) {} }
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  });
  dlg.addEventListener('click', function (e) { if (e.target === dlg) closeIt(); }); /* click on backdrop */
  el('dlgClose').addEventListener('click', closeIt);

  document.addEventListener('click', function (e) {
    var b = e.target.closest('.app-open');
    if (b) { open(b.closest('li').getAttribute('data-slug')); return; }
    var s = e.target.closest('[data-open]');
    if (s) open(s.getAttribute('data-open'));
  });

  el('dlgShare').addEventListener('click', function () {
    var slug = dlg.getAttribute('data-slug');
    var url = location.origin + location.pathname + '#app-' + slug;
    var title = el('dlgName').textContent;
    var note = el('dlgNote');
    if (navigator.share) {
      navigator.share({ title: title, text: title + ' by Enhancerworx', url: url }).catch(function () {});
    } else if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(url).then(function () { note.textContent = 'Link copied.'; }, function () { note.textContent = url; });
    } else { note.textContent = url; }
  });

  function fromHash() {
    var m = /^#app-([a-z0-9-]+)$/.exec(location.hash);
    if (m) open(m[1], true);
  }
  window.addEventListener('hashchange', fromHash);
  fromHash();
})();

/* Scroll progress bar and back-to-top button */
(function () {
  var bar = document.getElementById('progress');
  var top = document.getElementById('toTop');
  var ticking = false;
  function update() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    var y = window.pageYOffset || h.scrollTop;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(y / max, 1) : 0) + ')';
    if (top) top.hidden = y < 800;
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  update();
  if (top) top.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
})();

/* Contact form: sends through Formspree (https://formspree.io) */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  var status = document.getElementById('formStatus');
  var btn = document.getElementById('sendBtn');
  var MAIL = 'enhancerworx@gmail.com';
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function setStatus(html, kind) {
    status.textContent = '';
    status.className = 'form-status' + (kind ? ' ' + kind : '');
    if (typeof html === 'string') status.textContent = html;
    else if (html) status.appendChild(html);
    if (kind) status.focus();
  }
  function clearError(input) {
    var field = input.closest('.field');
    var old = field.querySelector('.field-error');
    if (old) old.remove();
    field.classList.remove('has-error');
    input.removeAttribute('aria-invalid');
  }
  function fieldError(input, msg) {
    clearError(input);
    var field = input.closest('.field');
    field.classList.add('has-error');
    input.setAttribute('aria-invalid', 'true');
    var p = document.createElement('p');
    p.className = 'field-error';
    p.textContent = msg;
    field.appendChild(p);
  }
  function validate() {
    var f = form.elements, ok = true, first = null;
    ['name', 'email', 'message', 'consent'].forEach(function (n) { clearError(f[n]); });
    if (!f.name.value.trim()) { fieldError(f.name, 'Enter your name so we know who to reply to.'); ok = false; first = first || f.name; }
    if (!EMAIL_RE.test(f.email.value.trim())) { fieldError(f.email, 'Enter an email address like name@example.com.'); ok = false; first = first || f.email; }
    if (!f.message.value.trim()) { fieldError(f.message, 'Write a few lines about what you need.'); ok = false; first = first || f.message; }
    if (!f.consent.checked) { fieldError(f.consent, 'Please tick this box so we can use your details to reply.'); ok = false; first = first || f.consent; }
    if (first) first.focus();
    return ok;
  }
  function collect() {
    var f = form.elements, d = {};
    ['name', 'email', 'phone', 'organisation', 'project_type', 'budget', 'timeline', 'message'].forEach(function (n) {
      d[n] = (f[n].value || '').trim();
    });
    d.platforms = Array.prototype.slice.call(form.querySelectorAll('input[name="platform"]:checked')).map(function (c) { return c.value; }).join(', ');
    d._subject = 'New enquiry from enhancerworx.in';
    d._gotcha = f._gotcha.value;
    return d;
  }
  function mailtoLink(d) {
    var body = 'Name: ' + d.name + '\nEmail: ' + d.email + '\nPhone: ' + (d.phone || '-') + '\nOrganisation: ' + (d.organisation || '-') +
      '\nNeed: ' + (d.project_type || '-') + '\nPlatforms: ' + (d.platforms || '-') + '\nBudget: ' + (d.budget || '-') +
      '\nTimeline: ' + (d.timeline || '-') + '\n\n' + d.message;
    return 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Project enquiry from ' + d.name) + '&body=' + encodeURIComponent(body);
  }
  function failMessage(d) {
    var wrap = document.createElement('span');
    wrap.appendChild(document.createTextNode('Your message could not be sent from here. '));
    var a = document.createElement('a');
    a.href = mailtoLink(d);
    a.textContent = 'Click here to send it by email instead';
    wrap.appendChild(a);
    wrap.appendChild(document.createTextNode('.'));
    return wrap;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    setStatus('', '');
    if (!validate()) return;
    var d = collect();
    if (d._gotcha) return; /* a bot filled the hidden field */

    var endpoint = form.getAttribute('action');
    if (endpoint.indexOf('YOUR_FORM_ID') !== -1) { setStatus(failMessage(d), 'err'); return; } /* Formspree ID not set yet */

    btn.disabled = true;
    btn.textContent = 'Sending…';
    fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(d)
    })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { return { ok: r.ok, body: j }; }); })
      .then(function (res) {
        if (!res.ok) throw new Error('send failed');
        form.reset();
        setStatus('Thank you. Your message has been sent and we will reply within one business day.', 'ok');
      })
      .catch(function () { setStatus(failMessage(d), 'err'); })
      .then(function () { btn.disabled = false; btn.textContent = 'Send message'; });
  });
})();

/* Terms pages: collapse the contents list on small screens, highlight the current section */
(function () {
  var toc = document.querySelector('.toc');
  if (!toc) return;
  if (window.matchMedia && window.matchMedia('(max-width: 900px)').matches) toc.removeAttribute('open');
  toc.addEventListener('click', function (e) {
    if (e.target.closest('a') && window.innerWidth <= 900) toc.removeAttribute('open');
  });
  if (!('IntersectionObserver' in window)) return;
  var links = {};
  toc.querySelectorAll('a').forEach(function (a) { links[a.getAttribute('href').slice(1)] = a; });
  var cur = null;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (!en.isIntersecting) return;
      var a = links[en.target.id];
      if (!a || a === cur) return;
      if (cur) cur.classList.remove('is-active');
      a.classList.add('is-active'); cur = a;
    });
  }, { rootMargin: '-20% 0px -70% 0px' });
  document.querySelectorAll('.terms-body section[id]').forEach(function (s) { io.observe(s); });
})();
