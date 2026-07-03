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

  /* ------------------------------------------------------------------
     Save-to-camera-roll via the native share sheet (iOS / Android).
     Websites can't write to Photos directly, but sharing the video file
     opens the share sheet where "Save Video" puts it in the camera roll.
     Falls back to a normal download if anything fails.
     ------------------------------------------------------------------ */
  const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) ||
    (navigator.maxTouchPoints > 1 && /Mac/i.test(navigator.userAgent));

  function canShareVideoFiles() {
    if (!isMobile || !navigator.share || !navigator.canShare) return false;
    try {
      const probe = new File([''], 'probe.mov', { type: 'video/quicktime' });
      return navigator.canShare({ files: [probe] });
    } catch (e) {
      return false;
    }
  }

  function mimeFor(name) {
    const n = name.toLowerCase();
    if (n.endsWith('.mp4') || n.endsWith('.m4v')) return 'video/mp4';
    return 'video/quicktime';
  }

  function fallbackDownload(href) {
    const a = document.createElement('a');
    a.href = href;
    a.setAttribute('download', '');
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function wireVideoShare(btn, href) {
    if (!canShareVideoFiles()) return;

    btn.innerHTML = '<span class="ig-download-icon">⤓</span> Save to camera roll';

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      if (btn.dataset.busy) return;
      btn.dataset.busy = '1';
      const original = btn.innerHTML;
      btn.innerHTML = '<span class="ig-download-icon">…</span> Preparing video';

      fetch(href)
        .then(r => {
          if (!r.ok) throw new Error('fetch failed');
          return r.blob();
        })
        .then(blob => {
          const name = href.split('/').pop().split('?')[0];
          const file = new File([blob], name, { type: mimeFor(name) });
          if (!navigator.canShare({ files: [file] })) throw new Error('cannot share');
          return navigator.share({ files: [file] });
        })
        .catch(err => {
          if (!err || err.name !== 'AbortError') fallbackDownload(href);
        })
        .finally(() => {
          delete btn.dataset.busy;
          btn.innerHTML = original;
        });
    });
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
    document.querySelectorAll('.story-card, .stories-grid > *').forEach(card => {
      // Don't double-inject if already there
      if (card.querySelector('.ig-download-btn')) return;

      // Old markup | thumbnail anchor linking to the video file
      const link = card.querySelector('a.story-image, a.story-video-link');
      if (link) {
        const href = link.getAttribute('href');
        if (!href || href === '#') return;
        const btn = makeDownloadButton(href, 'Download video');
        if (btn) {
          link.after(btn);
          wireVideoShare(btn, href);
        }
        return;
      }

      // New markup | inline <video> player, no anchor
      const video = card.querySelector('video[src]');
      if (video) {
        const src = video.getAttribute('src');
        if (!src) return;
        const btn = makeDownloadButton(src, 'Download video');
        if (btn) {
          video.after(btn);
          wireVideoShare(btn, src);
        }
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
