/* ==========================================================================
   MOBILE NAV (hamburger menu)
   ==========================================================================
   - Toggle button in .mobile-bar opens/closes the off-canvas sidebar.
   - Backdrop closes the drawer on click.
   - Sidebar links close the drawer on click (so navigating feels right).
   - ESC key closes the drawer.
   ========================================================================== */

(function () {
  'use strict';

  function init() {
    const toggle = document.querySelector('.mobile-bar-toggle');
    const backdrop = document.querySelector('.nav-backdrop');
    const sidebar = document.querySelector('.sidebar');
    if (!toggle || !sidebar) return;

    function open() {
      document.body.classList.add('is-nav-open');
      toggle.setAttribute('aria-expanded', 'true');
    }

    function close() {
      document.body.classList.remove('is-nav-open');
      toggle.setAttribute('aria-expanded', 'false');
    }

    function toggleDrawer() {
      if (document.body.classList.contains('is-nav-open')) {
        close();
      } else {
        open();
      }
    }

    toggle.addEventListener('click', toggleDrawer);

    if (backdrop) {
      backdrop.addEventListener('click', close);
    }

    // Close on link click inside the sidebar (so the drawer doesn't stay open after navigating)
    sidebar.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        close();
      }
    });

    // ESC key closes
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && document.body.classList.contains('is-nav-open')) {
        close();
      }
    });

    // If viewport grows past mobile breakpoint, force close
    window.addEventListener('resize', function () {
      if (window.innerWidth > 900) {
        close();
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
