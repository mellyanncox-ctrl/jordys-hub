/* ==========================================================================
   IG DOWNLOAD BUTTONS
   ==========================================================================
   Finds every IG post + story on a week page, and injects a "Download"
   button below each one. Works for:
   - Single-image posts (.image-slot inside .card with .card-tag.is-social)
   - Carousels (each slide gets its own download)
   - Story videos (.story-image with href to .mov/.mp4)
   ========================================================================== */

(function () {
  'use strict';

  function makeDownloadButton(href, label) {
    if (!href) return null;
    const a = document.createElement('a');
    a.className = 'ig-download-btn';
    a.href = href;
    a.setAttribute('download', '');
    a.innerHTML = `<span class="ig-download-icon">⤓</span> ${label || 'Download'}`;
    return a;
  }

  function processPosts() {
    // Each post card with social tag gets a download under the image/carousel
    document.querySelectorAll('.section .card').forEach(card => {
      const isIg = card.querySelector('.card-tag.is-social');
      if (!isIg) return;

      // Single image post
      const imageSlot = card.querySelector('.image-slot');
      if (imageSlot) {
        const img = imageSlot.querySelector('img');
        if (img && img.getAttribute('src')) {
          const btn = makeDownloadButton(img.getAttribute('src'), 'Download photo');
          if (btn) imageSlot.after(btn);
        }
        return;
      }

      // Carousel post | one download per slide
      const carousel = card.querySelector('.carousel');
      if (carousel) {
        const slides = Array.from(carousel.querySelectorAll('.carousel-slide img'));
        if (slides.length === 0) return;

        const wrap = document.createElement('div');
        wrap.className = 'ig-download-row';

        slides.forEach((img, i) => {
          const btn = makeDownloadButton(img.getAttribute('src'), `Image ${i + 1}`);
          if (btn) wrap.appendChild(btn);
        });

        carousel.after(wrap);
      }
    });
  }

  function processStories() {
    // Story videos | each story-image anchor wraps a thumb; add download below
    document.querySelectorAll('.story-card, .stories-grid > *').forEach(card => {
      // Find the media link inside
      const link = card.querySelector('a.story-image, a.story-video-link');
      if (!link) return;
      const href = link.getAttribute('href');
      if (!href || href === '#') return;

      // Don't double-inject if already there
      if (card.querySelector('.ig-download-btn')) return;

      const btn = makeDownloadButton(href, 'Download video');
      if (btn) {
        // Put it right after the link (above the caption)
        link.after(btn);
      }
    });
  }

  function init() {
    processPosts();
    processStories();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
