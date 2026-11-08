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
    document.title = "Repo Visualizer — " + t("heroHeadline");
    document.querySelector("meta[name=description]").content =
      window.repoAppearance.t("subtitle");
    for (const e of document.querySelectorAll("[data-site]"))
      e.textContent = t(e.dataset.site);
    for (const e of document.querySelectorAll("[data-site-aria]"))
      e.setAttribute("aria-label", t(e.dataset.siteAria));
  }
  function updateMedia() {
    const suffix =
      (["cs", "de", "fr", "es"].includes(window.repoAppearance.language) ? "-" + window.repoAppearance.language : "") +
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
  window.repoReady.then(() => window.repoPlayer.selectNode("model"));
  const heroCommand = document.getElementById("hero-command");
  document.getElementById("copy-hero").addEventListener("click", async () => {
    const message = document.getElementById("hero-feedback");
    try {
      await navigator.clipboard.writeText(heroCommand.textContent);
      message.textContent = t("copied");
      const label = document.querySelector("#copy-hero span");
      label.textContent = t("heroCopied");
      setTimeout(() => { label.textContent = t("heroCopy"); }, 2400);
    } catch {
      const range = document.createRange();
      range.selectNodeContents(heroCommand);
      const selection = getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      message.textContent = t("selected");
    }
  });
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
  // Content is visible without scripts; motion follows the reader's position.
  const reduced = matchMedia("(prefers-reduced-motion: reduce)");
  const landscape = document.querySelector(".landscape img");
  const pending = new Set(document.querySelectorAll(
    ".landing-section .section-heading, .example-row, .install-section, .guide-steps article, .export-showcase, .privacy-note"
  ));
  const shifts = new WeakMap();
  let scheduled = false;
  function complete(element) {
    pending.delete(element);
    element.classList.remove("scroll-reveal");
    element.style.removeProperty("--reveal-opacity");
    element.style.removeProperty("--reveal-shift");
    element.style.removeProperty("will-change");
    shifts.delete(element);
  }
  function finishWithin(anchor) {
    if (!anchor) return;
    for (const element of [...pending]) {
      if (element === anchor || anchor.contains(element) || element.contains(anchor)) complete(element);
    }
  }
  function updateScroll() {
    scheduled = false;
    if (reduced.matches) {
      landscape.style.transform = "none";
      for (const element of [...pending]) complete(element);
      return;
    }
    landscape.style.transform = `translateY(${Math.min(scrollY, 700) * 0.075}px)`;
    // Batch geometry reads before style writes, including the previous translation.
    const readings = [...pending].map(element => ({
      element,
      top: element.getBoundingClientRect().top - (shifts.get(element) || 0),
    }));
    for (const { element, top } of readings) {
      const progress = Math.max(0, Math.min(1, (innerHeight * 0.94 - top) / (innerHeight * 0.26)));
      if (progress === 1) { complete(element); continue; }
      const shift = (1 - progress) * 20;
      shifts.set(element, shift);
      element.classList.add("scroll-reveal");
      element.style.setProperty("--reveal-opacity", String(0.22 + progress * 0.78));
      element.style.setProperty("--reveal-shift", shift + "px");
      element.style.willChange = progress > 0 ? "transform, opacity" : "auto";
    }
  }
  function scheduleScroll() {
    if (scheduled || document.hidden) return;
    scheduled = true;
    requestAnimationFrame(updateScroll);
  }
  function revealHash() {
    try { finishWithin(document.getElementById(decodeURIComponent(location.hash.slice(1)))); } catch {}
    scheduleScroll();
  }
  addEventListener("scroll", scheduleScroll, { passive: true });
  addEventListener("resize", scheduleScroll, { passive: true });
  addEventListener("hashchange", revealHash);
  document.addEventListener("focusin", event => finishWithin(event.target.closest?.(".scroll-reveal")));
  document.addEventListener("click", event => {
    const link = event.target.closest?.('a[href^="#"]');
    if (link) finishWithin(document.getElementById(link.getAttribute("href").slice(1)));
  });
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) scheduleScroll();
    else scheduled = false;
  });
  document.addEventListener("repo-language-change", scheduleScroll);
  reduced.addEventListener("change", scheduleScroll);
  if ("ResizeObserver" in window) new ResizeObserver(scheduleScroll).observe(document.body);
  revealHash();
  scheduleScroll();
})();
