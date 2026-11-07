(() => {
  const command = document.getElementById("install-command");
  if (!command) return;
  const catalogs = JSON.parse(
    document.getElementById("site-locales").textContent,
  );
  const t = (key) =>
    catalogs[window.repoAppearance.language]?.[key] ?? catalogs.en[key];
  const feedback = document.getElementById("install-feedback");
  function translate() {
    document.title = "Repo Visualizer — " + window.repoAppearance.t("headline");
    document.querySelector("meta[name=description]").content =
      window.repoAppearance.t("subtitle");
    for (const e of document.querySelectorAll("[data-site]"))
      e.textContent = t(e.dataset.site);
    for (const e of document.querySelectorAll("[data-site-aria]"))
      e.setAttribute("aria-label", t(e.dataset.siteAria));
  }
  function updateMedia() {
    const suffix =
      (window.repoAppearance.language === "cs" ? "-cs" : "") +
      (window.repoAppearance.resolvedTheme === "dark" ? "-dark" : "");
    const video = document.querySelector("video"),
      source = video.querySelector("source");
    const target = "media/walkthrough" + suffix + ".mp4";
    video.poster = "media/poster" + suffix + ".png";
    if (source.getAttribute("src") !== target) {
      video.pause();
      source.src = target;
      video.load();
    }
    document.querySelector('.download-list a[href$=".gif"]').href =
      "media/walkthrough" + suffix + ".gif";
    document.querySelector('.download-list a[href$=".mp4"]').href = target;
  }
  for (const [suffix, format] of [
    [".html", "html"],
    [".svg", "svg"],
  ]) {
    document
      .querySelector('.download-list a[href$="' + suffix + '"]')
      .addEventListener("click", (event) => {
        event.preventDefault();
        repoPlayer.export(format).catch(() => {});
      });
  }
  translate();
  updateMedia();
  document.addEventListener("repo-language-change", () => {
    translate();
    updateMedia();
  });
  document.addEventListener("repo-theme-change", updateMedia);
  const buttons = [...document.querySelectorAll("[data-install-agent]")];
  const base =
    "npx skills add HonzaCuhel/repo-visualizer --skill repo-visualizer";
  for (const button of buttons)
    button.addEventListener("click", () => {
      const value = button.dataset.installAgent;
      command.textContent =
        base + (value === "both" ? " -a codex -a claude-code" : " -a " + value);
      for (const item of buttons)
        item.setAttribute("aria-pressed", String(item === button));
      feedback.textContent = t("installHint");
    });
  document
    .getElementById("copy-install")
    .addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(command.textContent);
        feedback.textContent = t("copied");
      } catch {
        const range = document.createRange();
        range.selectNodeContents(command);
        const selection = getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        feedback.textContent = t("selected");
      }
    });
  // Content stays visible without JavaScript or when reduced motion is requested.
  // A section enters once; scrolling never starts the repository animation.
  if (
    !matchMedia("(prefers-reduced-motion: reduce)").matches &&
    "IntersectionObserver" in window
  ) {
    const observer = new IntersectionObserver(
      (entries) => {
        for (const { target, isIntersecting } of entries) {
          if (!isIntersecting) continue;
          observer.unobserve(target);
          target.animate(
            [
              {
                opacity: 0.45,
                transform: "translateY(12px)",
                filter: "blur(1px)",
              },
              { opacity: 1, transform: "translateY(0)", filter: "blur(0)" },
            ],
            { duration: 460, easing: "cubic-bezier(0.16,1,0.3,1)" },
          );
        }
      },
      { threshold: 0.12 },
    );
    document
      .querySelectorAll(".landing-section")
      .forEach((section) => observer.observe(section));
  }
})();
