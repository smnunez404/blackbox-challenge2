(() => {
  const player = document.getElementById('diapositivas');
  const slides = Array.from(document.querySelectorAll('.deck-slide'));
  if (!player || slides.length === 0) return;

  const previous = document.getElementById('previous-slide');
  const next = document.getElementById('next-slide');
  const counter = document.getElementById('slide-counter');
  const indexLabel = document.getElementById('deck-index');
  const titleLabel = document.getElementById('deck-title-status');
  const progress = document.querySelector('.deck-progress');
  const progressFill = document.getElementById('deck-progress-fill');
  const speakerNotesButton = document.getElementById('toggle-speaker-notes');
  const fullscreenButton = document.getElementById('fullscreen-deck');
  const startButton = document.getElementById('start-presentation');
  let current = 0;

  function showSlide(index) {
    current = Math.max(0, Math.min(index, slides.length - 1));
    slides.forEach((slide, i) => {
      const active = i === current;
      slide.classList.toggle('active', active);
      slide.setAttribute('aria-hidden', String(!active));
    });
    const humanIndex = current + 1;
    const padded = String(humanIndex).padStart(2, '0');
    if (counter) counter.textContent = `${humanIndex} / ${slides.length}`;
    if (indexLabel) indexLabel.textContent = `${padded} / ${String(slides.length).padStart(2, '0')}`;
    if (titleLabel) titleLabel.textContent = slides[current].dataset.title || `Diapositiva ${humanIndex}`;
    if (progressFill) progressFill.style.width = `${(humanIndex / slides.length) * 100}%`;
    if (progress) progress.setAttribute('aria-valuenow', String(humanIndex));
    if (previous) previous.disabled = current === 0;
    if (next) next.disabled = current === slides.length - 1;
  }

  async function enterFullscreen() {
    try {
      if (!document.fullscreenElement && player.requestFullscreen) {
        await player.requestFullscreen({ navigationUI: 'hide' });
      }
    } catch {
      player.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  previous?.addEventListener('click', () => showSlide(current - 1));
  next?.addEventListener('click', () => showSlide(current + 1));
  fullscreenButton?.addEventListener('click', enterFullscreen);
  startButton?.addEventListener('click', enterFullscreen);
  speakerNotesButton?.addEventListener('click', () => {
    const visible = player.classList.toggle('speaker-notes-visible');
    speakerNotesButton.setAttribute('aria-pressed', String(visible));
    speakerNotesButton.textContent = visible ? 'Ocultar guion del expositor' : 'Mostrar guion del expositor';
  });
  document.getElementById('print-deck')?.addEventListener('click', () => {
    document.body.classList.add('printing');
    window.print();
  });
  window.addEventListener('afterprint', () => document.body.classList.remove('printing'));
  document.addEventListener('fullscreenchange', () => {
    const label = document.fullscreenElement ? 'Salir de pantalla completa' : 'Pantalla completa';
    if (fullscreenButton) fullscreenButton.textContent = label;
  });
  document.addEventListener('keydown', (event) => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === 'ArrowRight' || event.key === 'PageDown') {
      event.preventDefault();
      showSlide(current + 1);
    } else if (event.key === 'ArrowLeft' || event.key === 'PageUp') {
      event.preventDefault();
      showSlide(current - 1);
    } else if (event.key === 'Home') {
      showSlide(0);
    } else if (event.key === 'End') {
      showSlide(slides.length - 1);
    } else if (event.key.toLowerCase() === 'f') {
      event.preventDefault();
      if (document.fullscreenElement) document.exitFullscreen?.();
      else enterFullscreen();
    }
  });

  showSlide(0);
})();
