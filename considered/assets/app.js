'use strict';
// Progressive enhancement: all findings and links are usable without JavaScript.
document.querySelectorAll('.print').forEach(button => button.addEventListener('click', () => window.print()));
const search = document.querySelector('.table-search');
let distinction = 'all';
function applyFilters() {
  if (!search) return;
  const wrap = search.closest('.table-tools').nextElementSibling;
  const rows = [...wrap.querySelectorAll('tbody tr')];
  const query = search.value.trim().toLocaleLowerCase();
  let visible = 0;
  rows.forEach(row => {
    const text = row.textContent.toLocaleLowerCase();
    const selected = row.querySelector('.badge.green') !== null;
    const match = text.includes(query) && (distinction === 'all' || (distinction === 'selected' ? selected : !selected));
    row.hidden = !match;
    if (match) visible++;
  });
  document.querySelector('.result-count').textContent = `${visible} of ${rows.length} entries`;
  wrap.querySelector('.no-results').hidden = visible > 0;
}
if (search) {
  search.addEventListener('input', applyFilters);
  applyFilters();
}
document.querySelectorAll('[data-filter]').forEach(button => {
  button.addEventListener('click', () => {
    distinction = button.dataset.filter;
    document.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    applyFilters();
  });
});
const choiceButtons = [...document.querySelectorAll('[data-choice]')];
const allowed = new Set(choiceButtons.map(button => button.dataset.choice));
let choices = new Set();
try {
  const saved = JSON.parse(localStorage.getItem('china-review-paths-v1') || '[]');
  if (Array.isArray(saved)) choices = new Set(saved.filter(item => allowed.has(item)));
} catch (_) { /* Private browsers can deny local storage. Selection still works in memory. */ }
function renderChoices() {
  choiceButtons.forEach(button => {
    const selected = choices.has(button.dataset.choice);
    button.setAttribute('aria-pressed', String(selected));
    button.textContent = selected ? 'Shortlisted for review ✓' : 'Shortlist this path';
  });
  const status = document.getElementById('choice-status');
  if (status) status.textContent = choices.size ? `${choices.size} path(s) shortlisted in this browser only. Nothing has been implemented or booked.` : 'No review path selected.';
}
function saveChoices() {
  try { localStorage.setItem('china-review-paths-v1', JSON.stringify([...choices])); } catch (_) { /* In-memory fallback. */ }
  renderChoices();
}
choiceButtons.forEach(button => button.addEventListener('click', () => {
  const key = button.dataset.choice;
  choices.has(key) ? choices.delete(key) : choices.add(key);
  saveChoices();
}));
document.getElementById('clear-choices')?.addEventListener('click', () => { choices.clear(); saveChoices(); });
renderChoices();
