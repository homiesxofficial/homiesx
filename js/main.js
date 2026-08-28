(() => {
  const root = document.documentElement;
  const pageName = window.location.pathname.split('/').pop() || 'index.html';
  const pageLinks = [
    ['Home', pageName === 'index.html' ? 'index.html' : '../index.html', pageName === 'index.html'],
    ['Dashboard', pageName === 'dashboard.html' ? 'dashboard.html' : '../dashboard/dashboard.html', pageName === 'dashboard.html'],
    ['Resources', pageName === 'resources.html' ? 'resources.html' : '../pages/resources.html', pageName === 'resources.html'],
    ['Events', pageName === 'events.html' ? 'events.html' : '../pages/events.html', pageName === 'events.html'],
    ['Opportunities', pageName === 'opportunities.html' ? 'opportunities.html' : '../pages/opportunities.html', pageName === 'opportunities.html'],
    ['Projects', pageName === 'projects.html' ? 'projects.html' : '../pages/projects.html', pageName === 'projects.html'],
  ];
  const addPublicNavigation = () => {
    if (document.querySelector('[data-header]')) return;
    const stylesheet = document.createElement('link');
    stylesheet.rel = 'stylesheet';
    stylesheet.href = pageName === 'index.html' ? 'css/public-nav.css' : '../css/public-nav.css';
    document.head.append(stylesheet);
    const interactionStylesheet = document.createElement('link');
    interactionStylesheet.rel = 'stylesheet';
    interactionStylesheet.href = pageName === 'index.html' ? 'css/public-interactions.css' : '../css/public-interactions.css';
    document.head.append(interactionStylesheet);
    const themeStylesheet = document.createElement('link');
    themeStylesheet.rel = 'stylesheet';
    themeStylesheet.href = pageName === 'index.html' ? 'css/site-wide-polish.css' : '../css/site-wide-polish.css';
    document.head.append(themeStylesheet);
    const existingHeader = document.querySelector('body > header');
    const header = existingHeader || document.createElement('header');
    header.className = `${header.className} public-header${document.body.classList.contains('auth-page') ? ' auth-nav' : ''}`.trim();
    header.innerHTML = `<a class="brand" href="${pageName === 'index.html' ? 'index.html' : '../index.html'}" aria-label="HOMIESX home"><span class="brand-mark">H</span>HOMIES<span>X</span></a><nav aria-label="Primary navigation">${pageLinks.map(([label, href, active]) => `<a class="${active ? 'active' : ''}" href="${href}">${label}</a>`).join('')}</nav><div class="public-header-actions"><a class="public-login" href="${pageName === 'index.html' ? 'pages/login.html' : 'login.html'}">Log in</a><a class="button button-primary public-join" href="${pageName === 'index.html' ? 'pages/signup.html' : 'signup.html'}">Join <span>↗</span></a>${!document.body.classList.contains('auth-page') ? '<button class="icon-button" data-theme-toggle aria-label="Switch theme">◐</button>' : ''}</div>`;
    if (existingHeader) existingHeader.replaceWith(header);
    else document.body.prepend(header);
  };
  addPublicNavigation();
  const showToast = (message) => {
    let toast = document.querySelector('[data-site-toast]');
    if (!toast) { toast = document.createElement('div'); toast.dataset.siteToast = ''; document.body.append(toast); }
    toast.textContent = message;
    toast.classList.add('is-visible');
    clearTimeout(window.homiesxToastTimer);
    window.homiesxToastTimer = setTimeout(() => toast.classList.remove('is-visible'), 2800);
  };
  const savedKey = (button) => `homiesx-saved-${button.getAttribute('aria-label')?.replace(/^(Save|Unsave) /, '')}`;
  const syncSavedButtons = () => document.querySelectorAll('button[aria-label^="Save "], button[aria-label^="Unsave "]').forEach((button) => {
    const saved = localStorage.getItem(savedKey(button)) === 'true';
    const title = button.getAttribute('aria-label').replace(/^(Save|Unsave) /, '');
    button.setAttribute('aria-label', `${saved ? 'Unsave' : 'Save'} ${title}`);
    if (button.textContent.trim() === '♡' || button.textContent.trim() === '♥') button.textContent = saved ? '♥' : '♡';
  });
  document.addEventListener('click', (event) => {
    const saveButton = event.target.closest('button[aria-label^="Save "], button[aria-label^="Unsave "]');
    if (saveButton) {
      const title = saveButton.getAttribute('aria-label').replace(/^(Save|Unsave) /, '');
      const saved = localStorage.getItem(savedKey(saveButton)) === 'true';
      localStorage.setItem(savedKey(saveButton), String(!saved));
      syncSavedButtons();
      showToast(`${title} ${saved ? 'removed from' : 'saved to'} your list.`);
      return;
    }
    const placeholder = event.target.closest('a[href="#"]');
    if (placeholder) {
      event.preventDefault();
      const label = placeholder.textContent.trim().toLowerCase();
      const destination = label.includes('opportunit') ? 'opportunities.html' : label.includes('resource') ? 'resources.html' : label.includes('event') ? 'events.html' : null;
      if (destination) window.location.href = destination;
      else showToast('This student action will open from your connected workspace.');
      return;
    }
    const viewButton = event.target.closest('button[aria-label^="View "]');
    if (viewButton) showToast(`${viewButton.getAttribute('aria-label').replace('View ', '')} details are ready for registration.`);
    if (event.target.closest('[data-upload-message]')) { event.stopImmediatePropagation(); showToast('Sign in to share a resource with your campus.'); setTimeout(() => { window.location.href = 'login.html?next=share'; }, 700); }
    if (event.target.closest('[data-create-project]')) { event.stopImmediatePropagation(); showToast('Create a profile first, then start your project.'); setTimeout(() => { window.location.href = 'signup.html?next=projects'; }, 700); }
    if (event.target.closest('.input-link')) { event.preventDefault(); showToast('Password recovery will be sent to your verified student email.'); }
  });
  syncSavedButtons();
  const savedButtonObserver = new MutationObserver(() => {
    savedButtonObserver.disconnect();
    syncSavedButtons();
    savedButtonObserver.observe(document.body, { childList: true, subtree: true });
  });
  savedButtonObserver.observe(document.body, { childList: true, subtree: true });
  const toggle = document.querySelector('[data-theme-toggle]');
  const savedTheme = localStorage.getItem('homiesx-theme');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const setTheme = (theme) => {
    root.dataset.theme = theme;
    if (toggle) toggle.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`);
  };
  setTheme(savedTheme || (prefersDark ? 'dark' : 'light'));
  toggle?.addEventListener('click', () => { const next = root.dataset.theme === 'dark' ? 'light' : 'dark'; setTheme(next); localStorage.setItem('homiesx-theme', next); });
  const menuButton = document.querySelector('[data-menu-toggle]');
  const menu = document.querySelector('[data-mobile-menu]');
  menuButton?.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') === 'true'; menuButton.setAttribute('aria-expanded', String(!open)); menu.hidden = open; });
  document.querySelector('[data-header]')?.classList.toggle('is-scrolled', window.scrollY > 4);
  window.addEventListener('scroll', () => document.querySelector('[data-header]')?.classList.toggle('is-scrolled', window.scrollY > 4), { passive: true });
  if (document.body.matches('.auth-page, .dashboard-page, .resources-page, .events-page, .opportunities-page, .projects-page')) {
    const pageStyles = document.createElement('link');
    pageStyles.rel = 'stylesheet';
    pageStyles.href = document.body.classList.contains('resources-page') ? '../css/resources.css' : document.body.classList.contains('events-page') ? '../css/events.css' : document.body.classList.contains('opportunities-page') ? '../css/opportunities.css' : document.body.classList.contains('projects-page') ? '../css/projects.css' : '../css/app-pages.css';
    document.head.append(pageStyles);
  }
  document.querySelectorAll('[data-auth-form]').forEach((form) => form.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = form.querySelector('[data-form-message]');
    message.textContent = form.checkValidity() ? 'This is a prototype—verification will be enabled with the Django backend.' : 'Please complete the required fields with a valid email address.';
    message.classList.add('show');
  }));
  if (document.body.classList.contains('dashboard-page')) {
    document.querySelectorAll('.dashboard-sidebar nav a').forEach((link) => {
      if (link.textContent.includes('Resources')) link.href = '../pages/resources.html';
      if (link.textContent.includes('Events')) link.href = '../pages/events.html';
      if (link.textContent.includes('Opportunities')) link.href = '../pages/opportunities.html';
      if (link.textContent.includes('Projects')) link.href = '../pages/projects.html';
    });
  }
})();
