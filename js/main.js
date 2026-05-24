/* ═══════════════════════════════════════════════════
   ENHANCERWORX  ·  main.js
   ═══════════════════════════════════════════════════ */
'use strict';

/* 1. PAGE LOADER */
(function () {
  var loader = document.getElementById('loader');
  if (!loader) return;
  window.addEventListener('load', function () {
    setTimeout(function () {
      loader.classList.add('done');
      setTimeout(function () { loader.style.display = 'none'; }, 550);
    }, 900);
  });
})();

/* 2. THEME TOGGLE */
(function () {
  var KEY    = 'ew-theme';
  var root   = document.documentElement;
  var btn    = document.getElementById('themeBtn');
  var btnM   = document.getElementById('themeBtnMob');
  var mobLbl = document.querySelector('.tmob-label');
  var mobIco = document.querySelector('.tmob-icon');
  var saved   = localStorage.getItem(KEY);
  var sysDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  apply(saved || (sysDark ? 'dark' : 'light'));
  function apply(theme) {
    root.setAttribute('data-theme', theme);
    localStorage.setItem(KEY, theme);
    if (mobIco) mobIco.textContent = theme === 'dark' ? '🌙' : '☀️';
    if (mobLbl) mobLbl.textContent = theme === 'dark' ? 'Dark Mode' : 'Light Mode';
  }
  function toggle() { apply(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'); }
  if (btn)  btn.addEventListener('click', toggle);
  if (btnM) btnM.addEventListener('click', toggle);
})();

/* 3. CUSTOM CURSOR */
(function () {
  var dot  = document.getElementById('cDot');
  var ring = document.getElementById('cRing');
  if (!dot || !ring) return;
  if (!window.matchMedia('(pointer: fine)').matches) return;
  var mx = -100, my = -100, rx = -100, ry = -100;
  document.addEventListener('mousemove', function (e) { mx = e.clientX; my = e.clientY; });
  (function loop() {
    dot.style.transform  = 'translate(' + mx + 'px,' + my + 'px)';
    rx += (mx - rx) * 0.14; ry += (my - ry) * 0.14;
    ring.style.transform = 'translate(' + rx + 'px,' + ry + 'px)';
    requestAnimationFrame(loop);
  })();
  document.addEventListener('mouseleave', function () { dot.style.opacity = ring.style.opacity = '0'; });
  document.addEventListener('mouseenter', function () { dot.style.opacity = ring.style.opacity = '1'; });
})();

/* 4. NAV */
(function () {
  var nav     = document.getElementById('nav');
  var burger  = document.getElementById('burger');
  var drawer  = document.getElementById('navDrawer');
  var links   = document.querySelectorAll('.nm-link');
  var dmLinks = document.querySelectorAll('.dm-link');
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  function onScroll() {
    if (!nav) return;
    nav.classList.toggle('scrolled', window.scrollY > 40);
    setActiveLink();
  }
  if (burger && drawer) {
    burger.addEventListener('click', function () {
      var open = drawer.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      var spans = burger.querySelectorAll('span');
      if (open) {
        spans[0].style.transform = 'translateY(7px) rotate(45deg)';
        spans[1].style.opacity   = '0';
        spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
      } else {
        spans.forEach(function (s) { s.style.transform = ''; s.style.opacity = ''; });
      }
    });
  }
  dmLinks.forEach(function (a) {
    a.addEventListener('click', function () {
      drawer && drawer.classList.remove('open');
      if (burger) {
        var spans = burger.querySelectorAll('span');
        spans.forEach(function (s) { s.style.transform = ''; s.style.opacity = ''; });
      }
    });
  });
  function setActiveLink() {
    var sections = document.querySelectorAll('section[id]');
    var scrollY  = window.scrollY + 110;
    sections.forEach(function (sec) {
      if (scrollY >= sec.offsetTop && scrollY < sec.offsetTop + sec.offsetHeight) {
        var id = sec.getAttribute('id');
        links.forEach(function (l) {
          l.classList.toggle('active', l.getAttribute('href') === '#' + id);
        });
      }
    });
  }
})();

/* 5. SMOOTH SCROLL */
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var href = this.getAttribute('href');
      if (!href || href === '#') return;
      var target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      var navH = (document.getElementById('nav') || {}).offsetHeight || 70;
      var top  = target.getBoundingClientRect().top + window.scrollY - navH - 10;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });
})();

/* 6. BACK TO TOP */
(function () {
  var btn = document.getElementById('btt');
  if (!btn) return;
  window.addEventListener('scroll', function () {
    btn.classList.toggle('show', window.scrollY > 420);
  }, { passive: true });
})();

/* 7. HERO IMAGE SLIDER */
(function () {
  var track      = document.getElementById('slideTrack');
  var prevBtn    = document.getElementById('scPrev');
  var nextBtn    = document.getElementById('scNext');
  var dotsWrap   = document.getElementById('scDots');
  var labelText  = document.getElementById('slideLabelText');
  var counterEl  = document.getElementById('slideCurrentNum');
  if (!track) return;

  var slides  = track.querySelectorAll('.slide');
  var total   = slides.length;
  var current = 0;
  var timer;

  function goTo(idx) {
    current = (idx + total) % total;
    track.style.transform = 'translateX(-' + (current * 100) + '%)';

    if (dotsWrap) {
      dotsWrap.querySelectorAll('.sc-dot').forEach(function (d, i) {
        d.classList.toggle('active', i === current);
      });
    }

    var slide = slides[current];
    if (labelText)  labelText.textContent  = slide.getAttribute('data-label') || '';
    if (counterEl)  counterEl.textContent  = current + 1;
  }

  function next() { goTo(current + 1); }
  function prev() { goTo(current - 1); }

  function startAuto() {
    clearInterval(timer);
    timer = setInterval(next, 4500);
  }

  if (dotsWrap) {
    dotsWrap.querySelectorAll('.sc-dot').forEach(function (d) {
      d.addEventListener('click', function () {
        goTo(parseInt(this.getAttribute('data-idx'), 10));
        startAuto();
      });
    });
  }

  if (prevBtn) prevBtn.addEventListener('click', function () { prev(); startAuto(); });
  if (nextBtn) nextBtn.addEventListener('click', function () { next(); startAuto(); });

  var tx = 0;
  track.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend',   function (e) {
    var diff = tx - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) { diff > 0 ? next() : prev(); startAuto(); }
  });

  goTo(0);
  startAuto();
})();

/* 8. COUNTER ANIMATION */
(function () {
  var counters = document.querySelectorAll('.hc-num');
  if (!counters.length) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (!entry.isIntersecting) return;
      var el     = entry.target;
      var target = parseFloat(el.getAttribute('data-target')) || 0;
      var dur    = 1600;
      var start  = performance.now();
      (function tick(now) {
        var p    = Math.min((now - start) / dur, 1);
        var ease = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.round(target * ease);
        if (p < 1) requestAnimationFrame(tick);
      })(start);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });
  counters.forEach(function (el) { io.observe(el); });
})();

/* 9. PORTFOLIO FILTER */
(function () {
  var filtersWrap = document.getElementById('pfFilters');
  var grid        = document.getElementById('pfGrid');
  if (!filtersWrap || !grid) return;
  var btns  = filtersWrap.querySelectorAll('.pf-btn');
  var cards = grid.querySelectorAll('.pf-card');
  btns.forEach(function (btn) {
    btn.addEventListener('click', function () {
      btns.forEach(function (b) { b.classList.remove('active'); });
      this.classList.add('active');
      var filter = this.getAttribute('data-filter');
      cards.forEach(function (card) {
        var show = filter === 'all' || card.classList.contains(filter);
        card.style.transition = 'opacity .3s, transform .3s';
        if (show) {
          card.style.display = '';
          requestAnimationFrame(function () {
            card.style.opacity   = '1';
            card.style.transform = '';
          });
        } else {
          card.style.opacity   = '0';
          card.style.transform = 'scale(0.94)';
          setTimeout(function () {
            if (!card.classList.contains(filter) && filter !== 'all') {
              card.style.display = 'none';
            }
          }, 300);
        }
      });
    });
  });
})();

/* 10. REVIEWS SLIDER */
(function () {
  var track  = document.getElementById('rvTrack');
  var dotsEl = document.getElementById('rvDots');
  var prev   = document.getElementById('rvPrev');
  var next   = document.getElementById('rvNext');
  if (!track) return;
  var cards   = track.querySelectorAll('.rv-card');
  var total   = cards.length;
  var current = 0;
  var perView = getPerView();
  var maxIdx  = Math.max(0, total - perView);
  var timer;
  function buildDots() {
    if (!dotsEl) return;
    dotsEl.innerHTML = '';
    for (var i = 0; i <= maxIdx; i++) {
      var d = document.createElement('button');
      d.className = 'rv-dot' + (i === current ? ' active' : '');
      d.setAttribute('aria-label', 'Go to review ' + (i + 1));
      (function (idx) { d.addEventListener('click', function () { goTo(idx); startAuto(); }); })(i);
      dotsEl.appendChild(d);
    }
  }
  function updateDots() {
    if (!dotsEl) return;
    dotsEl.querySelectorAll('.rv-dot').forEach(function (d, i) { d.classList.toggle('active', i === current); });
  }
  function getPerView() {
    var w = window.innerWidth;
    if (w < 540) return 1;
    if (w < 860) return 2;
    return 3;
  }
  function cardWidth() {
    var c = cards[0];
    if (!c) return 0;
    var gap = parseFloat(getComputedStyle(track).gap) || 20;
    return c.offsetWidth + gap;
  }
  function goTo(idx) {
    current = Math.max(0, Math.min(idx, maxIdx));
    track.style.transform = 'translateX(-' + (current * cardWidth()) + 'px)';
    updateDots();
  }
  function goNext() { goTo(current >= maxIdx ? 0 : current + 1); }
  function goPrev() { goTo(current <= 0 ? maxIdx : current - 1); }
  function startAuto() { clearInterval(timer); timer = setInterval(goNext, 5000); }
  if (prev) prev.addEventListener('click', function () { goPrev(); startAuto(); });
  if (next) next.addEventListener('click', function () { goNext(); startAuto(); });
  var tx = 0;
  track.addEventListener('touchstart', function (e) { tx = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend',   function (e) {
    var diff = tx - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) { diff > 0 ? goNext() : goPrev(); startAuto(); }
  });
  window.addEventListener('resize', function () {
    perView = getPerView(); maxIdx = Math.max(0, total - perView);
    current = Math.min(current, maxIdx); buildDots(); goTo(current);
  }, { passive: true });
  buildDots(); goTo(0); startAuto();
})();

/* 11. CONTACT FORM */
(function () {
  var form = document.getElementById('contactForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var name  = (document.getElementById('fname')  || {}).value || '';
    var email = (document.getElementById('femail') || {}).value || '';
    var type  = (document.getElementById('ftype')  || {}).value || '';
    var msg   = (document.getElementById('fmsg')   || {}).value || '';
    name = name.trim(); email = email.trim();
    if (!name)  { showToast('Please enter your name.', 'error'); return; }
    if (!email || !isEmail(email)) { showToast('Please enter a valid email.', 'error'); return; }
    var subject = type ? '[Enhancerworx] ' + type + ' — ' + name : '[Enhancerworx Enquiry] ' + name;
    var body = 'Hi Enhancerworx,\n\nName: ' + name + '\nEmail: ' + email + '\n' +
      (type ? 'Project Type: ' + type + '\n' : '') + (msg ? '\nMessage:\n' + msg + '\n' : '') +
      '\nLooking forward to hearing from you!';
    window.location.href = 'mailto:enhancerworx@gmail.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
    showToast('Opening your mail client… 📧', 'success');
  });
  function isEmail(v) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); }
})();

/* 12. TOAST */
function showToast(msg, type) {
  document.querySelectorAll('.ew-toast').forEach(function (t) { t.remove(); });
  var t = document.createElement('div');
  t.className = 'ew-toast';
  t.textContent = msg;
  t.style.background = (type === 'error') ? '#ef4444' : '#5b5ef4';
  document.body.appendChild(t);
  requestAnimationFrame(function () { requestAnimationFrame(function () { t.classList.add('show'); }); });
  setTimeout(function () { t.classList.remove('show'); setTimeout(function () { t.remove(); }, 350); }, 3500);
}

/* 13. SCROLL REVEAL */
(function () {
  var selectors = ['.svc-card','.pf-card','.rv-card','.pillar','.pillar-icon',
    '.av-pill','.ct-info-row','.pf-cta-strip','.sec-header','.about-visual',
    '.about-content','.ct-left','.ct-right'];
  var els = [];
  selectors.forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (el, i) {
      if (!el.classList.contains('reveal')) {
        el.classList.add('reveal');
        el.style.transitionDelay = (i * 55) + 'ms';
        els.push(el);
      }
    });
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { entry.target.classList.add('visible'); io.unobserve(entry.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  els.forEach(function (el) { io.observe(el); });
})();

/* 14. CARD TILT */
(function () {
  if (window.matchMedia('(pointer: coarse)').matches) return;
  document.querySelectorAll('.svc-card').forEach(function (card) {
    card.addEventListener('mousemove', function (e) {
      var r = card.getBoundingClientRect();
      var rx = ((e.clientY - r.top - r.height / 2) / r.height) * -6;
      var ry = ((e.clientX - r.left - r.width  / 2) / r.width)  *  6;
      card.style.transform = 'translateY(-5px) perspective(700px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
    });
    card.addEventListener('mouseleave', function () { card.style.transform = ''; });
  });
})();

/* 15. PORTFOLIO IMAGE FALLBACK */
(function () {
  document.querySelectorAll('.pfc-img img').forEach(function (img) {
    img.addEventListener('error', function () { this.style.display = 'none'; });
  });
})();
