(() => {
  const form = document.querySelector('[data-campus-guide]');
  const result = document.querySelector('[data-guide-result]');
  if (!form || !result) return;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const query = new FormData(form).get('q').trim();
    const year = new FormData(form).get('year');
    const track = year === 'all' ? 'all years' : year.toUpperCase();
    const terms = query.toLowerCase();
    const destination = terms.includes('event') ? 'pages/events.html' : terms.includes('intern') || terms.includes('scholar') ? 'pages/opportunities.html' : terms.includes('project') || terms.includes('team') ? 'pages/projects.html' : 'pages/resources.html';
    result.classList.add('is-found');
    result.innerHTML = `Showing ${track} matches for <strong>${query.replace(/[<>]/g, '')}</strong>. <a href="${destination}?year=${encodeURIComponent(year)}">Open recommendations →</a>`;
  });
})();
