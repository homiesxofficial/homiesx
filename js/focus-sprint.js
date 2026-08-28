(() => {
  const form = document.querySelector('[data-focus-form]');
  const card = document.querySelector('[data-focus-card]');
  if (!form || !card) return;
  const clock = card.querySelector('[data-focus-clock]');
  const label = card.querySelector('[data-focus-label]');
  const yearLabel = card.querySelector('[data-focus-year]');
  const progress = card.querySelector('[data-focus-progress]');
  const toggle = card.querySelector('[data-focus-toggle]');
  const presets = [...form.querySelectorAll('[data-minutes]')];
  let totalSeconds = 50 * 60;
  let remainingSeconds = totalSeconds;
  let timer = null;
  const render = () => {
    const minutes = Math.floor(remainingSeconds / 60).toString().padStart(2, '0');
    const seconds = (remainingSeconds % 60).toString().padStart(2, '0');
    clock.textContent = `${minutes}:${seconds}`;
    progress.style.width = `${((totalSeconds - remainingSeconds) / totalSeconds) * 100}%`;
  };
  const stop = (completed = false) => {
    clearInterval(timer);
    timer = null;
    toggle.textContent = completed ? 'Start another sprint' : 'Start timer';
    label.textContent = completed ? 'SPRINT COMPLETE' : 'READY WHEN YOU ARE';
  };
  const tick = () => {
    remainingSeconds -= 1;
    render();
    if (remainingSeconds <= 0) stop(true);
  };
  presets.forEach((preset) => preset.addEventListener('click', () => {
    presets.forEach((item) => item.classList.remove('is-selected'));
    preset.classList.add('is-selected');
    totalSeconds = Number(preset.dataset.minutes) * 60;
    remainingSeconds = totalSeconds;
    stop();
    render();
  }));
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const subject = form.elements.subject.value.trim();
    if (!subject) return;
    card.dataset.subject = subject;
    yearLabel.textContent = form.elements.year.value;
    label.textContent = `FOCUSING ON ${subject.toUpperCase()}`;
    remainingSeconds = totalSeconds;
    render();
    toggle.focus();
  });
  toggle.addEventListener('click', () => {
    if (timer) {
      clearInterval(timer);
      timer = null;
      toggle.textContent = 'Resume timer';
      label.textContent = 'SPRINT PAUSED';
    } else {
      timer = setInterval(tick, 1000);
      toggle.textContent = 'Pause timer';
      label.textContent = `FOCUSING ON ${(card.dataset.subject || 'YOUR TASK').toUpperCase()}`;
    }
  });
  render();
})();
