/* =========================================================
   ENHANCERWORX — main.js
   EdTech Studio · All interactive features
   ========================================================= */

'use strict';

/* =========================================================
   1. THEME TOGGLE (Dark / Light)
   ========================================================= */
(function initTheme() {
  const root       = document.documentElement;
  const btn        = document.getElementById('themeToggle');
  const btnMob     = document.getElementById('themeToggleMob');
  const mobIcon    = document.querySelector('.theme-icon-mob');
  const STORAGE_KEY = 'ew-theme';

  // Determine initial theme: saved → system preference → dark
  const saved      = localStorage.getItem(STORAGE_KEY);
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initial    = saved || (prefersDark ? 'dark' : 'light');

  applyTheme(initial);

  function applyTheme(theme) {
    root.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    if (mobIcon) mobIcon.textContent = theme === 'dark' ? '🌙' : '☀️';
  }

  function toggle() {
    const current = root.getAttribute('data-theme');
    applyTheme(current === 'dark' ? 'light' : 'dark');
  }

  if (btn)    btn.addEventListener('click', toggle);
  if (btnMob) btnMob.addEventListener('click', toggle);
})();


/* =========================================================
   2. CUSTOM CURSOR
   ========================================================= */
(function initCursor() {
  const dot  = document.querySelector('.cursor-dot');
  const ring = document.querySelector('.cursor-ring');
  if (!dot || !ring) return;

  let mx = -100, my = -100;
  let rx = -100, ry = -100;
  let rafId;

  document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });

  function animate() {
    // Dot follows exactly
    dot.style.transform  = `translate(${mx}px, ${my}px)`;
    // Ring lags
    rx += (mx - rx) * 0.15;
    ry += (my - ry) * 0.15;
    ring.style.transform = `translate(${rx}px, ${ry}px)`;
    rafId = requestAnimationFrame(animate);
  }
  animate();

  document.addEventListener('mouseleave', () => {
    dot.style.opacity  = '0';
    ring.style.opacity = '0';
  });
  document.addEventListener('mouseenter', () => {
    dot.style.opacity  = '1';
    ring.style.opacity = '1';
  });
})();


/* =========================================================
   3. NAV — scroll style + active link + burger
   ========================================================= */
(function initNav() {
  const nav        = document.getElementById('nav');
  const burger     = document.getElementById('navBurger');
  const mobileMenu = document.getElementById('navMobile');
  const navLinks   = document.querySelectorAll('.nav-link');
  const mobLinks   = document.querySelectorAll('.mob-link');

  // Scroll → add .scrolled
  window.addEventListener('scroll', () => {
    nav.classList.toggle('scrolled', window.scrollY > 40);
    updateActiveLink();
  }, { passive: true });

  // Burger toggle
  if (burger && mobileMenu) {
    burger.addEventListener('click', () => {
      const open = mobileMenu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open);
      // Animate burger bars
      const spans = burger.querySelectorAll('span');
      if (open) {
        spans[0].style.transform = 'translateY(7px) rotate(45deg)';
        spans[1].style.opacity   = '0';
        spans[2].style.transform = 'translateY(-7px) rotate(-45deg)';
      } else {
        spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
      }
    });
  }

  // Close mobile menu on link click
  mobLinks.forEach(link => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      const spans = burger.querySelectorAll('span');
      spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    });
  });

  // Active link on scroll
  const sections = document.querySelectorAll('section[id]');
  function updateActiveLink() {
    const scrollY = window.scrollY + 120;
    sections.forEach(sec => {
      if (scrollY >= sec.offsetTop && scrollY < sec.offsetTop + sec.offsetHeight) {
        const id = sec.getAttribute('id');
        navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + id));
      }
    });
  }
  updateActiveLink();
})();


/* =========================================================
   4. BACK TO TOP
   ========================================================= */
(function initBackTop() {
  const btn = document.getElementById('backTop');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 400);
  }, { passive: true });
})();


/* =========================================================
   5. SCROLL REVEAL
   ========================================================= */
(function initReveal() {
  // Add .reveal to key elements
  const targets = [
    '.service-card', '.it-card', '.port-item',
    '.review-card', '.pillar', '.about-content',
    '.about-img-wrap', '.contact-left', '.contact-right',
    '.section-header', '.it-cta-bar', '.hero-badge',
    '.hero-stats', '.contact-info-item'
  ];

  targets.forEach(sel => {
    document.querySelectorAll(sel).forEach((el, i) => {
      el.classList.add('reveal');
      el.style.transitionDelay = `${i * 60}ms`;
    });
  });

  const io = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  document.querySelectorAll('.reveal').forEach(el => io.observe(el));
})();


/* =========================================================
   6. PORTFOLIO FILTER
   ========================================================= */
(function initPortfolioFilter() {
  const filterBtns = document.querySelectorAll('.pf-btn');
  const items      = document.querySelectorAll('.port-item');
  if (!filterBtns.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Update active button
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      items.forEach(item => {
        const show = filter === 'all' || item.classList.contains(filter);
        item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        if (show) {
          item.style.display   = 'block';
          requestAnimationFrame(() => {
            item.style.opacity   = '1';
            item.style.transform = 'scale(1)';
          });
        } else {
          item.style.opacity   = '0';
          item.style.transform = 'scale(0.95)';
          setTimeout(() => { item.style.display = 'none'; }, 300);
        }
      });
    });
  });

  // Wire IT Training placeholder cards to mailto
  document.querySelectorAll('.port-it-placeholder').forEach(card => {
    card.addEventListener('click', () => {
      const appName = card.querySelector('h4')?.textContent || 'IT Training App';
      window.location.href = `mailto:enhancerworx@gmail.com?subject=App Enquiry - ${encodeURIComponent(appName)}&body=Hi, I'm interested in the ${encodeURIComponent(appName)} app. Please share details.`;
    });
  });
})();


/* =========================================================
   7. REVIEWS SLIDER
   ========================================================= */
(function initReviews() {
  const track  = document.getElementById('reviewsTrack');
  const dotsWrap = document.getElementById('rvDots');
  const prevBtn  = document.getElementById('rvPrev');
  const nextBtn  = document.getElementById('rvNext');
  if (!track) return;

  const cards      = track.querySelectorAll('.review-card');
  const total      = cards.length;
  let current      = 0;
  let perView      = getPerView();
  let maxIndex     = Math.max(0, total - perView);
  let autoTimer;

  // Build dots
  function buildDots() {
    if (!dotsWrap) return;
    dotsWrap.innerHTML = '';
    const count = maxIndex + 1;
    for (let i = 0; i < count; i++) {
      const d = document.createElement('div');
      d.className = 'rv-dot' + (i === current ? ' active' : '');
      d.addEventListener('click', () => goTo(i));
      dotsWrap.appendChild(d);
    }
  }

  function updateDots() {
    if (!dotsWrap) return;
    dotsWrap.querySelectorAll('.rv-dot').forEach((d, i) =>
      d.classList.toggle('active', i === current)
    );
  }

  function getPerView() {
    if (window.innerWidth < 600)  return 1;
    if (window.innerWidth < 900)  return 2;
    return 3;
  }

  function getCardWidth() {
    const card = cards[0];
    if (!card) return 0;
    const style = getComputedStyle(card);
    const gap = parseFloat(getComputedStyle(track).gap) || 24;
    return card.offsetWidth + gap;
  }

  function goTo(index) {
    current = Math.max(0, Math.min(index, maxIndex));
    track.style.transform = `translateX(-${current * getCardWidth()}px)`;
    updateDots();
  }

  function next() { goTo(current >= maxIndex ? 0 : current + 1); }
  function prev() { goTo(current <= 0 ? maxIndex : current - 1); }

  function startAuto() {
    clearInterval(autoTimer);
    autoTimer = setInterval(next, 5000);
  }
  function stopAuto() { clearInterval(autoTimer); }

  if (prevBtn) prevBtn.addEventListener('click', () => { prev(); stopAuto(); startAuto(); });
  if (nextBtn) nextBtn.addEventListener('click', () => { next(); stopAuto(); startAuto(); });

  // Touch/swipe
  let touchStartX = 0;
  track.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; }, { passive: true });
  track.addEventListener('touchend', e => {
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (Math.abs(diff) > 40) { diff > 0 ? next() : prev(); stopAuto(); startAuto(); }
  });

  // Recalculate on resize
  window.addEventListener('resize', () => {
    perView  = getPerView();
    maxIndex = Math.max(0, total - perView);
    current  = Math.min(current, maxIndex);
    buildDots();
    goTo(current);
  }, { passive: true });

  buildDots();
  goTo(0);
  startAuto();
})();


/* =========================================================
   8. CONTACT FORM — mailto handler
   ========================================================= */
(function initContactForm() {
  const form = document.getElementById('contactForm');
  if (!form) return;

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const name    = (form.querySelector('#fname')?.value  || '').trim();
    const email   = (form.querySelector('#femail')?.value || '').trim();
    const type    = (form.querySelector('#ftype')?.value  || '').trim();
    const message = (form.querySelector('#fmsg')?.value   || '').trim();

    if (!name || !email) {
      showToast('Please fill in your name and email.', 'error');
      return;
    }
    if (!isValidEmail(email)) {
      showToast('Please enter a valid email address.', 'error');
      return;
    }

    const subject = type
      ? `[Enhancerworx Enquiry] ${type} — ${name}`
      : `[Enhancerworx Enquiry] ${name}`;

    const body =
      `Hi Enhancerworx,\n\n` +
      `My name is ${name}.\n` +
      `Email: ${email}\n` +
      (type    ? `Project Type: ${type}\n` : '') +
      (message ? `\nMessage:\n${message}\n` : '') +
      `\nLooking forward to hearing from you!`;

    const mailto = `mailto:enhancerworx@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailto;
    showToast('Opening your mail client… 📧', 'success');
  });

  function isValidEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
})();


/* =========================================================
   9. TOAST NOTIFICATION
   ========================================================= */
function showToast(message, type = 'success') {
  // Remove existing
  document.querySelectorAll('.ew-toast').forEach(t => t.remove());

  const toast = document.createElement('div');
  toast.className = 'ew-toast';
  toast.textContent = message;

  Object.assign(toast.style, {
    position:      'fixed',
    bottom:        '32px',
    left:          '50%',
    transform:     'translateX(-50%) translateY(20px)',
    background:    type === 'success' ? '#5b5ef4' : '#ef4444',
    color:         '#fff',
    padding:       '14px 28px',
    borderRadius:  '50px',
    fontSize:      '14px',
    fontWeight:    '500',
    fontFamily:    "'DM Sans', sans-serif",
    boxShadow:     '0 8px 30px rgba(0,0,0,0.25)',
    zIndex:        '99999',
    opacity:       '0',
    transition:    'opacity 0.3s ease, transform 0.3s ease',
    pointerEvents: 'none',
    whiteSpace:    'nowrap',
  });

  document.body.appendChild(toast);
  requestAnimationFrame(() => {
    toast.style.opacity   = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });
  setTimeout(() => {
    toast.style.opacity   = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
    setTimeout(() => toast.remove(), 350);
  }, 3500);
}


/* =========================================================
   10. SMOOTH ANCHOR SCROLL (offset for fixed nav)
   ========================================================= */
(function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const navH   = document.getElementById('nav')?.offsetHeight || 70;
      const top    = target.getBoundingClientRect().top + window.scrollY - navH - 12;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });
})();


/* =========================================================
   11. IT TRAINING CARD — Tilt effect on hover (desktop)
   ========================================================= */
(function initTilt() {
  if (window.matchMedia('(pointer: coarse)').matches) return; // skip touch

  document.querySelectorAll('.it-card, .service-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const cx = rect.width / 2;
      const cy = rect.height / 2;
      const rotX = ((y - cy) / cy) * -6;
      const rotY = ((x - cx) / cx) *  6;
      card.style.transform = `translateY(-5px) perspective(800px) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
})();


/* =========================================================
   12. HERO STATS — Animated number counter
   ========================================================= */
(function initCounters() {
  const stats = document.querySelectorAll('.stat-num');
  if (!stats.length) return;

  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el  = entry.target;
      const raw = el.textContent.trim();
      // Extract numeric part and suffix
      const match = raw.match(/^([\d.]+)(.*)$/);
      if (!match) return;
      const target = parseFloat(match[1]);
      const suffix = match[2];
      const isInt  = Number.isInteger(target);
      const duration = 1600;
      const start    = performance.now();

      function tick(now) {
        const elapsed  = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease     = 1 - Math.pow(1 - progress, 3);
        const val      = target * ease;
        el.textContent = (isInt ? Math.round(val) : val.toFixed(1)) + suffix;
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      io.unobserve(el);
    });
  }, { threshold: 0.5 });

  stats.forEach(el => io.observe(el));
})();


/* =========================================================
   13. PORTFOLIO ITEM — Image lazy load fallback
   ========================================================= */
(function initImageFallback() {
  document.querySelectorAll('.port-img-wrap img').forEach(img => {
    img.addEventListener('error', function () {
      this.style.display = 'none';
      const parent = this.closest('.port-img-wrap');
      if (parent && !parent.querySelector('.img-placeholder')) {
        const ph = document.createElement('div');
        ph.className = 'img-placeholder';
        Object.assign(ph.style, {
          width: '100%', height: '100%',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: '40px', color: 'var(--text-3)',
          position: 'absolute', inset: '0',
        });
        ph.textContent = '📱';
        parent.appendChild(ph);
      }
    });
  });
})();


/* =========================================================
   14. SECTION OBSERVER — add class for CSS transitions
   ========================================================= */
(function initSectionAnims() {
  const sections = document.querySelectorAll('section');
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => e.target.classList.toggle('in-view', e.isIntersecting));
  }, { threshold: 0.08 });
  sections.forEach(s => io.observe(s));
})();
