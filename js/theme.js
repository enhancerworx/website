/* Runs before first paint so the page never flashes the wrong theme. */
(function () {
  var d = document.documentElement, t = null;
  d.classList.add('js');
  try { t = localStorage.getItem('ew-theme'); } catch (e) {}
  if (t !== 'light' && t !== 'dark') {
    t = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  d.setAttribute('data-theme', t);
})();
