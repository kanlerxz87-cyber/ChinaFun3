// ChinaFun3 — minimal interactivity: nav toggle + table filter + sort
document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav
  const btn = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (btn && nav) {
    btn.addEventListener('click', () => {
      nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
  }

  // Simple table filter (search input with data-filter="tableId")
  document.querySelectorAll('[data-filter-target]').forEach(input => {
    const targetId = input.getAttribute('data-filter-target');
    const table = document.getElementById(targetId);
    if (!table) return;
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    const rows = Array.from(tbody.querySelectorAll('tr'));
    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      rows.forEach(tr => {
        const text = tr.textContent.toLowerCase();
        tr.style.display = (!q || text.includes(q)) ? '' : 'none';
      });
    });
  });

  // Column sort (optional: th with data-sort="numeric|text")
  document.querySelectorAll('th[data-sort]').forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
      const table = th.closest('table');
      const tbody = table.querySelector('tbody');
      const idx = Array.from(th.parentNode.children).indexOf(th);
      const type = th.getAttribute('data-sort');
      const dir = th.getAttribute('data-dir') === 'asc' ? 'desc' : 'asc';
      // reset siblings
      th.parentNode.querySelectorAll('th[data-dir]').forEach(s => { if (s !== th) s.removeAttribute('data-dir'); });
      th.setAttribute('data-dir', dir);
      const rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort((a, b) => {
        const av = a.children[idx]?.textContent.trim() ?? '';
        const bv = b.children[idx]?.textContent.trim() ?? '';
        if (type === 'numeric') {
          const an = parseFloat(av.replace(/[$,¥\s]/g, '')) || 0;
          const bn = parseFloat(bv.replace(/[$,¥\s]/g, '')) || 0;
          return dir === 'asc' ? an - bn : bn - an;
        } else {
          return dir === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
        }
      });
      rows.forEach(r => tbody.appendChild(r));
    });
  });

  // Copy link helper
  document.querySelectorAll('[data-copy]').forEach(btn => {
    btn.addEventListener('click', async () => {
      const v = btn.getAttribute('data-copy');
      try {
        await navigator.clipboard.writeText(v);
        const old = btn.textContent;
        btn.textContent = 'Copied!';
        setTimeout(() => btn.textContent = old, 1200);
      } catch {}
    });
  });
});
