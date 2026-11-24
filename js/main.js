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

/* Mobile menu */
(function () {
  var btn = document.getElementById('menuBtn');
  var nav = document.getElementById('nav');
  if (!btn || !nav) return;
  function setOpen(open) {
    nav.classList.toggle('open', open);
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  btn.addEventListener('click', function () { setOpen(!nav.classList.contains('open')); });
  nav.addEventListener('click', function (e) { if (e.target.tagName === 'A') setOpen(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('open')) { setOpen(false); btn.focus(); }
  });
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

/* Contact form */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  var status = document.getElementById('formStatus');
  var btn = document.getElementById('sendBtn');
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function setStatus(msg, kind) {
    status.textContent = msg;
    status.className = 'form-status' + (kind ? ' ' + kind : '');
  }
  function fieldError(input, msg) {
    var field = input.closest('.field');
    var old = field.querySelector('.field-error');
    if (old) old.remove();
    field.classList.toggle('has-error', !!msg);
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
    if (msg) {
      var p = document.createElement('p');
      p.className = 'field-error';
      p.textContent = msg;
      field.appendChild(p);
    }
  }
  function validate() {
    var name = form.elements.name, email = form.elements.email, ok = true;
    fieldError(name, ''); fieldError(email, '');
    if (!name.value.trim()) { fieldError(name, 'Enter your name so we know who to reply to.'); ok = false; }
    if (!EMAIL_RE.test(email.value.trim())) { fieldError(email, 'Enter an email address like name@example.com.'); ok = false; }
    if (!ok) (form.querySelector('[aria-invalid="true"]') || name).focus();
    return ok;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    setStatus('', '');
    if (!validate()) return;
    if (form.elements._gotcha.value) return; /* bot filled the hidden field */

    var action = form.getAttribute('action') || '';
    var data = new FormData(form);

    /* Formspree not set up yet: fall back to the visitor's email app. */
    if (action.indexOf('YOUR_FORM_ID') !== -1) {
      var body = 'Name: ' + data.get('name') + '\nEmail: ' + data.get('email') + '\nNeed: ' + (data.get('project_type') || '-') + '\n\n' + (data.get('message') || '');
      window.location.href = 'mailto:enhancerworx@gmail.com?subject=' + encodeURIComponent('Project enquiry from ' + data.get('name')) + '&body=' + encodeURIComponent(body);
      setStatus('Opening your email app. Press send there to finish.', 'ok');
      return;
    }

    btn.disabled = true;
    setStatus('Sending…', '');
    fetch(action, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
      .then(function (r) {
        if (!r.ok) throw new Error('bad status');
        form.reset();
        setStatus('Message sent. We will reply within one business day.', 'ok');
      })
      .catch(function () {
        setStatus('The message did not send. Check your connection and try again, or email enhancerworx@gmail.com.', 'err');
      })
      .then(function () { btn.disabled = false; });
  });
})();
