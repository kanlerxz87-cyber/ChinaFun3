// Simple client-side filter for tables (no backend). Filters rows by text + status.
function initFilter(tableId, searchId, statusId){
  const table=document.getElementById(tableId); if(!table) return;
  const search=document.getElementById(searchId);
  const status=document.getElementById(statusId);
  function apply(){
    const q=(search?search.value:'').toLowerCase();
    const s=status?status.value:'all';
    table.querySelectorAll('tbody tr').forEach(tr=>{
      const txt=tr.innerText.toLowerCase();
      const st=tr.getAttribute('data-status')||'';
      const okQ=!q||txt.includes(q);
      const okS=s==='all'||st===s;
      tr.style.display=(okQ&&okS)?'':'none';
    });
  }
  if(search) search.addEventListener('input',apply);
  if(status) status.addEventListener('change',apply);
}
document.addEventListener('DOMContentLoaded',()=>{
  initFilter('restaurants-table','r-search','r-status');
  initFilter('hotels-table','h-search','h-status');
  initFilter('activities-table','a-search','a-status');
});
