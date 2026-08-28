(() => {
  const resources = [
    { title: 'Data Structures: practice set', type: 'PDF', subject: 'Data Structures', semester: 'Semester 3', author: 'Aarav Mehta', saves: 96, accent: 'violet', date: 4 },
    { title: 'Complete DSA notes', type: 'Notes', subject: 'Data Structures', semester: 'Semester 3', author: 'Priya Shah', saves: 72, accent: 'mint', date: 3 },
    { title: 'Web development roadmap', type: 'Link', subject: 'Web Development', semester: 'Semester 3', author: 'Community pick', saves: 188, accent: 'peach', date: 2 },
    { title: 'Discrete mathematics revision', type: 'PDF', subject: 'Mathematics', semester: 'Semester 4', author: 'Nisha Kulkarni', saves: 41, accent: 'yellow', date: 1 },
    { title: 'Responsive CSS reference', type: 'Link', subject: 'Web Development', semester: 'Semester 4', author: 'HOMIESX collection', saves: 56, accent: 'violet', date: 5 },
    { title: 'Stack and queue visual notes', type: 'Notes', subject: 'Data Structures', semester: 'Semester 3', author: 'Rohan Patil', saves: 35, accent: 'mint', date: 6 }
  ];
  const grid = document.querySelector('[data-resource-grid]');
  const empty = document.querySelector('[data-resource-empty]');
  const count = document.querySelector('[data-result-count]');
  const query = document.querySelector('#resource-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  const sort = document.querySelector('[data-sort]');
  const render = () => {
    const search = query.value.trim().toLowerCase();
    const chosen = Object.fromEntries(filters.map((item) => [item.dataset.filter, item.value]));
    const list = resources.filter((item) => (!search || Object.values(item).join(' ').toLowerCase().includes(search)) && Object.entries(chosen).every(([key, value]) => value === 'all' || item[key] === value)).sort((a, b) => sort.value === 'popular' ? b.saves - a.saves : a.date - b.date);
    count.textContent = list.length;
    grid.innerHTML = list.map((item) => `<article class="resource-card"><div class="resource-card-top"><span class="resource-kind ${item.accent}">${item.type}</span><button type="button" aria-label="Save ${item.title}">♡</button></div><div><h2>${item.title}</h2><p>${item.subject} · ${item.semester}</p></div><div class="resource-card-bottom"><span>by ${item.author}</span><span>♡ ${item.saves}</span></div></article>`).join('');
    empty.hidden = list.length !== 0;
    grid.hidden = list.length === 0;
  };
  [query, sort, ...filters].forEach((input) => input.addEventListener('input', render));
  document.querySelectorAll('[data-filter-reset]').forEach((button) => button.addEventListener('click', () => { query.value = ''; sort.value = 'newest'; filters.forEach((item) => item.value = 'all'); render(); }));
  render();
})();
