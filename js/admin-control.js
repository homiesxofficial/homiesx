document.addEventListener('DOMContentLoaded', () => {
  const search = document.querySelector('.command-search input');
  const rows = [...document.querySelectorAll('.activity-row, .content-row')];
  const selectAll = document.querySelector('[data-select-all]');
  const rowChecks = [...document.querySelectorAll('.row-check')];
  if (selectAll) selectAll.addEventListener('change', () => rowChecks.forEach((check) => { check.checked = selectAll.checked; }));
  if (!search || !rows.length) return;
  search.addEventListener('input', () => {
    const query = search.value.trim().toLowerCase();
    rows.forEach((row) => { row.hidden = query && !row.textContent.toLowerCase().includes(query); });
  });
  document.addEventListener('keydown', (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); search.focus(); }
  });
});
