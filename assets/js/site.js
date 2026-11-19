// Shared menu bar, footer and small helpers used by every page.
(function () {
  const PAGES = [
    { href: 'index.html', label: 'Home' },
    { href: 'MCcampaigns.html', label: 'Campaigns' },
    { href: 'MCgauntlet.html', label: 'Gauntlet' },
    { href: 'MCscenarios.html', label: 'Modular Sets' },
    { href: 'MC-solo-champions-league-archive.html', label: 'SCL Archive' },
    { href: 'MCscoring.html', label: 'Scoring' },
  ];

  const current = (location.pathname.split('/').pop() || 'index.html').toLowerCase();

  function renderNav() {
    const nav = document.getElementById('site-nav');
    if (!nav) return;
    const links = PAGES.map(p => {
      const active = p.href.toLowerCase() === current ? ' aria-current="page"' : '';
      return `<a class="nav-link" href="${p.href}"${active}>${p.label}</a>`;
    }).join('');
    nav.className = 'sticky top-0 z-20 bg-gray-900/95 backdrop-blur border-b border-gray-800';
    nav.innerHTML = `
      <div class="container mx-auto px-4 sm:px-6 flex items-center gap-4 h-14">
        <a href="index.html" class="flex items-center gap-2 shrink-0 font-bold tracking-wide text-red-500 hover:text-red-400">
          <img src="assets/img/favicon.png" alt="CEREBRO home" class="w-7 h-7 rounded-md">
          <span class="hidden lg:inline">CEREBRO</span>
        </a>
        <div class="flex gap-0.5 sm:gap-1 overflow-x-auto -mr-4 pr-4 sm:mr-0 sm:pr-0">${links}</div>
      </div>`;
    nav.setAttribute('aria-label', 'Main');
  }

  function renderFooter() {
    const footer = document.getElementById('site-footer');
    if (!footer) return;
    const credit = footer.dataset.credit ? `<p class="mb-1">${footer.dataset.credit}</p>` : '';
    footer.className = 'mt-12 border-t border-gray-800 py-6 text-center text-xs text-gray-500 px-4';
    footer.innerHTML = `${credit}
      <p>CEREBRO is an unofficial fan-made site. Marvel Champions is published by Fantasy Flight Games.
      This site is not affiliated with or endorsed by Fantasy Flight Games or Marvel.</p>`;
  }

  // localStorage can throw (private mode, blocked storage), so every call is guarded.
  const store = {
    get(key, fallback = null) {
      try {
        const v = localStorage.getItem(key);
        return v === null ? fallback : JSON.parse(v);
      } catch { return fallback; }
    },
    set(key, value) {
      try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch { return false; }
    },
    getRaw(key) { try { return localStorage.getItem(key); } catch { return null; } },
    setRaw(key, value) { try { localStorage.setItem(key, value); return true; } catch { return false; } },
    remove(key) { try { localStorage.removeItem(key); } catch { /* ignore */ } },
  };

  const escapeHtml = s => String(s ?? '').replace(/[&<>"']/g, c => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  // Makes every <button class="hint-btn" aria-controls="id"> toggle its hint panel.
  function wireHints(root = document) {
    root.querySelectorAll('.hint-btn[aria-controls]').forEach(btn => {
      btn.setAttribute('aria-expanded', 'false');
      btn.addEventListener('click', () => {
        const panel = document.getElementById(btn.getAttribute('aria-controls'));
        const open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', String(!open));
        panel.hidden = open;
      });
    });
  }

  window.MC = { store, escapeHtml, wireHints };

  renderNav();
  renderFooter();
})();
