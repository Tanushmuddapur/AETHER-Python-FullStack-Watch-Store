/* AETHER HOROLOGY — Built by Tanush Muddapur | Light/Dark Theme, Scroll Animations & Live Color Switcher */
(function() {
  const savedTheme = localStorage.getItem('aether_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
})();

document.addEventListener('DOMContentLoaded', () => {
  // 1. Theme Toggle Button
  const themeBtn = document.getElementById('theme-toggle-btn');
  const updateThemeBtnLabel = () => {
    if (!themeBtn) return;
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    themeBtn.innerHTML = isDark ? '☀ Light' : '☾ Dark';
  };
  updateThemeBtnLabel();

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const curr = document.documentElement.getAttribute('data-theme');
      const next = curr === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('aether_theme', next);
      updateThemeBtnLabel();
    });
  }

  // 2. Scroll Slide-Up & Slide-Down Animations
  const obs = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) e.target.classList.add('in-view'); });
  }, { threshold: 0.08 });
  document.querySelectorAll('.slide-up, .slide-down, .fade-scale').forEach((el) => obs.observe(el));

  // 3. Liquid Glass Nav Specular Cursor & Auto-Hide
  const nav = document.querySelector('.liquid-glass-nav');
  if (nav) {
    nav.addEventListener('mousemove', (e) => {
      const r = nav.getBoundingClientRect();
      nav.style.setProperty('--mouse-x', `${((e.clientX - r.left) / r.width) * 100}%`);
      nav.style.setProperty('--mouse-y', `${((e.clientY - r.top) / r.height) * 100}%`);
    });
  }
  const navWrap = document.getElementById('liquid-nav-wrapper');
  let lastY = window.scrollY;
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (navWrap) {
      if (y > lastY && y > 380) navWrap.classList.add('nav-hidden');
      else navWrap.classList.remove('nav-hidden');
    }
    lastY = y;
  }, { passive: true });

  // 4. Mobile Hamburger
  const burger = document.getElementById('mobile-hamburger');
  const menu = document.getElementById('primary-nav-menu');
  if (burger && menu) burger.addEventListener('click', () => menu.classList.toggle('mobile-open'));

  // 5. Auto-dismiss toasts
  setTimeout(() => {
    document.querySelectorAll('.aether-toast').forEach((t) => { t.style.opacity = '0'; setTimeout(() => t.remove(), 400); });
  }, 4000);
});

// Switch Watch Card Image & Dial Color Label on Swatch Click
function switchCardWatchColor(swatchBtn, imgSrc, colorName) {
  const card = swatchBtn.closest('.watch-card, .premium-liquid-card');
  if (!card) return;
  const img = card.querySelector('.primary-watch-img');
  if (img && imgSrc) {
    img.style.opacity = '0.35';
    setTimeout(() => { img.src = imgSrc; img.style.opacity = '1'; }, 140);
  }
  const label = card.querySelector('.active-color-label');
  if (label) label.textContent = colorName;
  card.querySelectorAll('.swatch-circle').forEach(s => s.classList.remove('active'));
  swatchBtn.classList.add('active');
}

function swapFkImage(thumbEl, src, caption) {
  const mainImg = document.getElementById('fk-main-image');
  if (mainImg) {
    mainImg.style.opacity = '0.35';
    setTimeout(() => { mainImg.src = src; mainImg.style.opacity = '1'; }, 140);
  }
  const capEl = document.getElementById('fk-image-caption');
  if (capEl && caption) capEl.textContent = caption;
  document.querySelectorAll('.fk-thumb').forEach(t => t.classList.remove('active'));
  thumbEl.classList.add('active');
}

function togglePwd(id, btn) {
  const inp = document.getElementById(id);
  if (!inp) return;
  inp.type = inp.type === 'password' ? 'text' : 'password';
  btn.textContent = inp.type === 'password' ? 'Show' : 'Hide';
}


function toggleMoreMenu(e) {
  e.stopPropagation();
  const dd = document.getElementById('nav-more-dropdown');
  if (dd) dd.classList.toggle('open');
}

document.addEventListener('click', (e) => {
  const dd = document.getElementById('nav-more-dropdown');
  if (dd && !dd.contains(e.target)) {
    dd.classList.remove('open');
  }
});
