'use strict';
// Progressive enhancement only: tables and sources remain readable without JS.
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const menu = $('.menu-toggle');
const sidebar = $('.sidebar');
function closeMenu(){ sidebar.classList.remove('open'); menu.setAttribute('aria-expanded','false'); }
menu?.addEventListener('click', () => {
  const open = sidebar.classList.toggle('open'); menu.setAttribute('aria-expanded',String(open));
});
document.addEventListener('keydown', event => { if(event.key==='Escape') closeMenu(); });
document.addEventListener('click', event => { if(!sidebar.contains(event.target) && !menu.contains(event.target)) closeMenu(); });
$('.print-button')?.addEventListener('click', () => window.print());
const filters = {};
function updateTable(id){
  const table = document.getElementById(id); if(!table) return;
  const term = ($(`[data-search="${id}"]`)?.value || '').trim().toLocaleLowerCase();
  const category = filters[id] || 'all';
  const rows = $$('tbody tr',table);
  let visible = 0;
  rows.forEach(row=>{
    const match = (row.dataset.searchable || row.textContent).toLocaleLowerCase().includes(term);
    const categoryMatch = category==='all' || row.dataset.category===category;
    row.hidden = !(match && categoryMatch); if(!row.hidden) visible++;
  });
  const count = document.getElementById(`${id}-count`);
  if(count) count.textContent = `${visible} of ${rows.length}`;
  let empty = document.getElementById(`${id}-empty`);
  if(!empty){empty = document.createElement('p');empty.id=`${id}-empty`;empty.className='empty-results';empty.setAttribute('role','status');table.parentElement.after(empty);}
  empty.hidden = visible>0;
  empty.textContent = 'No matching entries. Clear your search or choose All to see the full list.';
}
$$('[data-search]').forEach(input=>{
  const id=input.dataset.search;
  if(id==='dining-table') input.value=new URLSearchParams(location.search).get('cluster') || '';
  input.addEventListener('input',()=>updateTable(id));updateTable(id);
});
$$('[data-filter]').forEach(button=>button.addEventListener('click',()=>{
  const id=button.dataset.target;filters[id]=button.dataset.filter;
  $$(`[data-target="${id}"][data-filter]`).forEach(b=>{const on=b===button;b.classList.toggle('active',on);b.setAttribute('aria-pressed',String(on));});
  updateTable(id);
}));
let storageAvailable=true;
function read(key,fallback){try{const val=JSON.parse(localStorage.getItem(key));return val===null?fallback:val;}catch{storageAvailable=false;return fallback;}}
function persist(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true;}catch{storageAvailable=false;return false;}}
let toastTimer;
function toast(message){let box=$('.toast');if(!box){box=document.createElement('div');box.className='toast';box.setAttribute('role','status');document.body.append(box);}box.textContent=message;box.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>box.hidden=true,3800);}
const savedData=read('china-for-two:saved:v1',[]);
const saved=new Set(Array.isArray(savedData)?savedData.filter(x=>typeof x==='string'):[]);
$$('[data-save]').forEach(button=>{
  const id=button.dataset.save;
  const draw=()=>{button.textContent=saved.has(id)?'♥ Saved locally':'♡ Save candidate';button.setAttribute('aria-pressed',String(saved.has(id)));};draw();
  button.addEventListener('click',()=>{saved.has(id)?saved.delete(id):saved.add(id);const ok=persist('china-for-two:saved:v1',[...saved]);draw();toast(ok?'Shortlist updated in this browser only. No reservation made.':'Browser storage unavailable. This choice lasts only while the page is open.');});
});
const choicesData=read('china-for-two:suggestions:v1',{});
const choices=choicesData && !Array.isArray(choicesData) && typeof choicesData==='object' ? choicesData : {};
$$('[data-suggestion]').forEach(group=>{
  const id=group.dataset.suggestion;
  function draw(){
    $$('button',group).forEach(b=>b.setAttribute('aria-pressed',String(choices[id]===b.dataset.choice)));
    $('span',group).textContent=choices[id]==='consider'?'Consider for later':choices[id]==='defer'?'Deferred':'Not reviewed';
  }
  draw();
  $$('button',group).forEach(button=>button.addEventListener('click',()=>{
    if(choices[id]===button.dataset.choice) delete choices[id];else choices[id]=button.dataset.choice;
    const ok=persist('china-for-two:suggestions:v1',choices);draw();
    const note=$('#storage-note');if(note)note.textContent=ok?'Choices saved only in this browser. No enhancement has been authorized or implemented.':'Browser storage unavailable; export your choices to keep them. No change has been authorized.';
  }));
});
$('#export-decisions')?.addEventListener('click',()=>{
  const exportData={researchSnapshot:'2026-11-25',exportedAt:new Date().toISOString(),note:'Local review preferences only. Not implementation approval or booking authorization.',suggestions:choices,savedHotelIds:[...saved]};
  const url=URL.createObjectURL(new Blob([JSON.stringify(exportData,null,2)+'\n'],{type:'application/json'}));
  const a=document.createElement('a');a.href=url;a.download='china-for-two-review.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('Review choices exported. No changes have been implemented.');
});
if(!storageAvailable && $('#storage-note')) $('#storage-note').textContent='Browser storage is unavailable. You can still read everything and export optional review choices.';
