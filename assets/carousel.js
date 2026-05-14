/* ==========================================================================
   IG CAROUSEL RUNTIME
   ==========================================================================
   - Finds all .carousel elements on the page
   - Wires prev/next arrows and dot clicks
   - Updates active slide, dot, and counter
   - Supports keyboard left/right when carousel is focused
   - Swipe gestures on touch devices
   ========================================================================== */

(function () {
  'use strict';

  function initCarousel(root) {
    const slides = Array.from(root.querySelectorAll('.carousel-slide'));
    const dots = Array.from(root.querySelectorAll('.carousel-dot'));
    const prev = root.querySelector('.carousel-prev');
    const next = root.querySelector('.carousel-next');
    const counter = root.querySelector('.carousel-counter');
    const total = slides.length;
    if (total <= 1) return;

    let current = 0;

    function update() {
      slides.forEach((s, i) => s.classList.toggle('is-active', i === current));
      dots.forEach((d, i) => d.classList.toggle('is-active', i === current));
      if (counter) counter.textContent = `${current + 1} / ${total}`;
      if (prev) prev.disabled = (current === 0);
      if (next) next.disabled = (current === total - 1);
    }

    function go(idx) {
      current = Math.max(0, Math.min(total - 1, idx));
      update();
    }

    if (prev) prev.addEventListener('click', () => go(current - 1));
    if (next) next.addEventListener('click', () => go(current + 1));
    dots.forEach((d, i) => d.addEventListener('click', () => go(i)));

    // Keyboard
    root.setAttribute('tabindex', '0');
    root.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(current - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); go(current + 1); }
    });

    // Touch swipe
    let touchStartX = null;
    root.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });
    root.addEventListener('touchend', (e) => {
      if (touchStartX === null) return;
      const dx = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(dx) > 40) {
        if (dx > 0) go(current - 1);
        else go(current + 1);
      }
      touchStartX = null;
    });

    update();
  }

  function init() {
    document.querySelectorAll('.carousel').forEach(initCarousel);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
