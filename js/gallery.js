// Галерея с увеличением: клик по фото в .gallery открывает его на весь экран.
// Листать — стрелками на экране, клавишами ← → или свайпом; закрыть — ✕, Esc или клик по фону.
(function () {
  var imgs = Array.prototype.slice.call(document.querySelectorAll('.gallery img'));
  if (!imgs.length) return;

  var box = document.createElement('div');
  box.className = 'lightbox';
  box.setAttribute('role', 'dialog');
  box.setAttribute('aria-modal', 'true');
  box.setAttribute('aria-label', 'Просмотр фото');
  box.innerHTML =
    '<button type="button" class="lb-close" aria-label="Закрыть">✕</button>' +
    '<button type="button" class="lb-prev" aria-label="Предыдущее фото">‹</button>' +
    '<figure><img alt=""><figcaption></figcaption></figure>' +
    '<button type="button" class="lb-next" aria-label="Следующее фото">›</button>';
  document.body.appendChild(box);

  var big = box.querySelector('img'), cap = box.querySelector('figcaption'), cur = 0, lastFocus = null;

  function show(i) {
    cur = (i + imgs.length) % imgs.length;
    big.src = imgs[cur].currentSrc || imgs[cur].src;
    big.alt = imgs[cur].alt;
    var fc = imgs[cur].closest('figure') && imgs[cur].closest('figure').querySelector('figcaption');
    cap.textContent = fc ? fc.textContent : '';
  }
  function open(i) { lastFocus = document.activeElement; show(i); box.classList.add('open'); document.body.style.overflow = 'hidden'; box.querySelector('.lb-close').focus(); }
  function close() { box.classList.remove('open'); document.body.style.overflow = ''; if (lastFocus) lastFocus.focus(); }

  imgs.forEach(function (img, i) {
    img.tabIndex = 0;
    img.setAttribute('role', 'button');
    img.addEventListener('click', function () { open(i); });
    img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(i); } });
  });
  box.querySelector('.lb-close').addEventListener('click', close);
  box.querySelector('.lb-prev').addEventListener('click', function () { show(cur - 1); });
  box.querySelector('.lb-next').addEventListener('click', function () { show(cur + 1); });
  box.addEventListener('click', function (e) { if (e.target === box) close(); });
  document.addEventListener('keydown', function (e) {
    if (!box.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') show(cur - 1);
    if (e.key === 'ArrowRight') show(cur + 1);
  });
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
    x0 = null;
  });
})();
