(() => {
  const back = document.querySelector('.detail-back');
  if (!back) return;
  const home = document.querySelector('.wordmark');
  function update() {
    const url = new URL(location.protocol === 'file:'
      ? 'https://honzacuhel.github.io/repo-visualizer/' : './', location.href);
    url.searchParams.set('lang', repoAppearance.language);
    url.searchParams.set('theme', repoAppearance.theme);
    home.href = url.href;
    url.hash = 'examples';
    back.href = url.href;
  }
  update();
  document.addEventListener('repo-language-change', update);
  document.addEventListener('repo-theme-change', update);
})();
