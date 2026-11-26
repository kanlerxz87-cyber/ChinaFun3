// ChinaFun3 — minimal accessible interactivity: nav toggle, search filter, chip filters, column sort
document.addEventListener('DOMContentLoaded', () => {
  const btn = document.querySelector('[data-nav-toggle]');
  const nav = document.querySelector('[data-nav]');
  if (btn && nav) {
    btn.addEventListener('click', () => {
      nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
  }

  // Combined text search + optional chip category filter per table
  const tableStates = new Map();
  function applyTableFilter(tableId) {
    const table = document.getElementById(tableId);
    if (!table) return;
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    const state = tableStates.get(tableId) || { query: '', chip: 'all' };
    const rows = Array.from(tbody.querySelectorAll('tr'));
    let visible = 0;
    rows.forEach(tr => {
      const text = tr.textContent.toLowerCase();
      const cats = (tr.getAttribute('data-cats') || '').toLowerCase().split(/\s+/).filter(Boolean);
      const matchQ = !state.query || text.includes(state.query);
      const matchC = state.chip === 'all' || cats.includes(state.chip);
      const show = matchQ && matchC;
      tr.style.display = show ? '' : 'none';
      if (show) visible += 1;
    });
    const counter = document.querySelector(`[data-count-for="${tableId}"]`);
    if (counter) counter.textContent = `${visible} of ${rows.length} shown`;
  }

  document.querySelectorAll('[data-filter-target]').forEach(input => {
    const targetId = input.getAttribute('data-filter-target');
    if (!tableStates.has(targetId)) tableStates.set(targetId, { query: '', chip: 'all' });
    input.addEventListener('input', () => {
      const state = tableStates.get(targetId);
      state.query = input.value.trim().toLowerCase();
      applyTableFilter(targetId);
    });
  });

  document.querySelectorAll('[data-chip-target]').forEach(group => {
    const targetId = group.getAttribute('data-chip-target');
    if (!tableStates.has(targetId)) tableStates.set(targetId, { query: '', chip: 'all' });
    const buttons = Array.from(group.querySelectorAll('.chip-btn'));
    buttons.forEach(b => {
      b.addEventListener('click', () => {
        buttons.forEach(x => x.classList.remove('active'));
        b.classList.add('active');
        const state = tableStates.get(targetId);
        state.chip = (b.getAttribute('data-chip') || 'all').toLowerCase();
        applyTableFilter(targetId);
      });
    });
  });

  // Sortable columns
  document.querySelectorAll('th[data-sort]').forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
      const table = th.closest('table');
      const tbody = table.querySelector('tbody');
      const idx = Array.from(th.parentNode.children).indexOf(th);
      const type = th.getAttribute('data-sort');
      const dir = th.getAttribute('data-dir') === 'asc' ? 'desc' : 'asc';
      th.parentNode.querySelectorAll('th[data-dir]').forEach(s => { if (s !== th) s.removeAttribute('data-dir'); });
      th.setAttribute('data-dir', dir);
      const rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort((a, b) => {
        const av = a.children[idx]?.textContent.trim() ?? '';
        const bv = b.children[idx]?.textContent.trim() ?? '';
        if (type === 'numeric') {
          const an = parseFloat(av.replace(/[^0-9.\-]/g, ''));
          const bn = parseFloat(bv.replace(/[^0-9.\-]/g, ''));
          const ax = Number.isNaN(an) ? Number.POSITIVE_INFINITY : an;
          const bx = Number.isNaN(bn) ? Number.POSITIVE_INFINITY : bn;
          return dir === 'asc' ? ax - bx : bx - ax;
        }
        return dir === 'asc' ? av.localeCompare(bv) : bv.localeCompare(av);
      });
      rows.forEach(r => tbody.appendChild(r));
    });
  });
});
