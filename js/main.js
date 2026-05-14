/* =========================================================
   ENHANCERWORX — Main JS
   ========================================================= */

/* ---- Custom Cursor ---- */
(function () {
  const dot  = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');
  if (!dot || !ring) return;
  let mx = 0, my = 0, rx = 0, ry = 0;
  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
  function loop() {
    rx += (mx - rx) * 0.18;
    ry += (my - ry) * 0.18;
    dot.style.transform  = `translate(${mx}px,${my}px)`;
    ring.style.transform = `translate(${rx}px,${ry}px)`;
    requestAnimationFrame(loop);
  }
  loop();
})();

/* ---- Nav scroll behaviour ---- */
(function () {
  const nav     = document.getElementById('nav');
  const backTop = document.getElementById('backTop');
  function onScroll() {
    const y = window.scrollY;
    nav.classList.toggle('scrolled', y > 60);
    if (backTop) backTop.classList.toggle('visible', y > 400);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();

/* ---- Mobile nav burger ---- */
(function () {
  const burger = document.getElementById('navBurger');
  const mobile = document.getElementById('navMobile');
  if (!burger || !mobile) return;
  burger.addEventListener('click', () => {
    mobile.classList.toggle('open');
    burger.classList.toggle('open');
  });
  document.querySelectorAll('.mob-link').forEach(a => {
    a.addEventListener('click', () => {
      mobile.classList.remove('open');
      burger.classList.remove('open');
    });
  });
})();

/* ---- Active nav link on scroll ---- */
(function () {
  const sections = document.querySelectorAll('section[id]');
  const links    = document.querySelectorAll('.nav-link');
  function update() {
    const scrollY = window.scrollY + 120;
    let current = '';
    sections.forEach(s => {
      if (s.offsetTop <= scrollY) current = s.id;
    });
    links.forEach(l => {
      l.classList.toggle('active', l.getAttribute('href') === '#' + current);
    });
  }
  window.addEventListener('scroll', update, { passive: true });
  update();
})();

/* ---- Reveal on scroll ---- */
(function () {
  const els = document.querySelectorAll('.reveal');
  if (!els.length) return;
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  els.forEach(el => io.observe(el));
})();

/* ---- Portfolio filter ---- */
(function () {
  const btns  = document.querySelectorAll('.pf-btn');
  const items = document.querySelectorAll('.port-item');
  if (!btns.length) return;
  btns.forEach(btn => {
    btn.addEventListener('click', () => {
      btns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const filter = btn.dataset.filter;
      items.forEach(item => {
        const show = filter === 'all' || item.classList.contains(filter);
        item.style.display = show ? '' : 'none';
        if (show) {
          item.style.animation = 'none';
          item.offsetHeight; // reflow
          item.style.animation = 'fadeUp 0.4s ease both';
        }
      });
    });
  });
})();

/* ---- Reviews slider ---- */
(function () {
  const track  = document.getElementById('reviewsTrack');
  const prev   = document.getElementById('rvPrev');
  const next   = document.getElementById('rvNext');
  const dotsEl = document.getElementById('rvDots');
  if (!track) return;

  const cards = track.querySelectorAll('.review-card');
  let current = 0;
  let perView = getPerView();

  function getPerView() {
    return window.innerWidth < 600 ? 1 : window.innerWidth < 900 ? 2 : 3;
  }

  const total = Math.ceil(cards.length / perView);

  // Build dots
  function buildDots() {
    dotsEl.innerHTML = '';
    for (let i = 0; i < Math.ceil(cards.length / perView); i++) {
      const d = document.createElement('div');
      d.className = 'rv-dot' + (i === current ? ' active' : '');
      d.addEventListener('click', () => goTo(i));
      dotsEl.appendChild(d);
    }
  }

  function goTo(idx) {
    const maxIdx = Math.ceil(cards.length / perView) - 1;
    current = Math.max(0, Math.min(idx, maxIdx));
    const cardW = cards[0].offsetWidth + 24;
    track.style.transform = `translateX(-${current * perView * cardW}px)`;
    dotsEl.querySelectorAll('.rv-dot').forEach((d, i) => d.classList.toggle('active', i === current));
  }

  prev && prev.addEventListener('click', () => goTo(current - 1));
  next && next.addEventListener('click', () => goTo(current + 1));

  // Auto-play
  let timer = setInterval(() => goTo(current + 1 > Math.ceil(cards.length / perView) - 1 ? 0 : current + 1), 5000);
  track.addEventListener('mouseenter', () => clearInterval(timer));
  track.addEventListener('mouseleave', () => {
    timer = setInterval(() => goTo(current + 1 > Math.ceil(cards.length / perView) - 1 ? 0 : current + 1), 5000);
  });

  window.addEventListener('resize', () => {
    perView = getPerView();
    current = 0;
    buildDots();
    goTo(0);
  });

  buildDots();
})();

/* ---- Contact form ---- */
(function () {
  const form = document.getElementById('contactForm');
  if (!form) return;
  form.addEventListener('submit', e => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const orig = btn.innerHTML;
    btn.innerHTML = 'Sending… <span>⏳</span>';
    btn.disabled = true;
    setTimeout(() => {
      btn.innerHTML = 'Message Sent! <span>✓</span>';
      btn.style.background = 'var(--green)';
      setTimeout(() => {
        btn.innerHTML = orig;
        btn.style.background = '';
        btn.disabled = false;
        form.reset();
      }, 3000);
    }, 1200);
  });
})();

/* ---- Smooth scroll for anchor links ---- */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
});

/* ---- Add reveal class to sections ---- */
(function () {
  const targets = document.querySelectorAll(
    '.about-grid, .service-card, .port-item, .review-card, .contact-grid, .section-header'
  );
  targets.forEach(el => el.classList.add('reveal'));
  // Trigger immediately for elements already in view
  setTimeout(() => {
    document.querySelectorAll('.reveal').forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.9) el.classList.add('visible');
    });
  }, 100);
})();
