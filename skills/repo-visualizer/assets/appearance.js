/* Appearance and language are user preferences, independent of the agent. */
(() => {
  "use strict";
  const config = JSON.parse(document.getElementById("appearance-config").textContent);
  const catalogs = JSON.parse(document.getElementById("interface-locales").textContent);
  const root = document.documentElement;
  const storage = {
    get(key) { try { return localStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { localStorage.setItem(key, value); } catch {} },
  };
  const query = new URLSearchParams(location.search);
  const graphLanguage = config.language.split("-")[0].toLowerCase();
  const supports = (lang) => Boolean(catalogs[lang] || (lang === graphLanguage && Object.keys(config.ui_strings || {}).length));
  let language = [query.get("lang"), storage.get("rv-language"), config.preference?.language, config.landing ? navigator.language.split("-")[0] : graphLanguage, "en"].find(supports);
  let theme = [query.get("theme"), storage.get("rv-theme"), config.preference?.theme, "system"].find(value => ["light", "dark", "system"].includes(value));
  const media = matchMedia("(prefers-color-scheme: dark)");
  function t(key, values = {}) {
    const custom = language === graphLanguage ? config.ui_strings?.[key] : undefined;
    return String(custom ?? catalogs[language]?.[key] ?? catalogs.en[key] ?? key).replace(/\{(\w+)\}/g, (_, name) => String(values[name] ?? "{" + name + "}"));
  }
  const flagShapes = {
    en: '<rect width="28" height="20" fill="#21468b"/><path d="m0 0 28 20m0-20L0 20" stroke="#fff" stroke-width="4"/><path d="m0 0 28 20m0-20L0 20" stroke="#c8102e" stroke-width="1.5"/><path d="M14 0v20M0 10h28" stroke="#fff" stroke-width="7"/><path d="M14 0v20M0 10h28" stroke="#c8102e" stroke-width="4"/>',
    cs: '<path fill="#fff" d="M0 0h28v10H0z"/><path fill="#d7141a" d="M0 10h28v10H0z"/><path fill="#11457e" d="m0 0 14 10L0 20z"/>',
    de: '<path fill="#151515" d="M0 0h28v7H0z"/><path fill="#d00" d="M0 7h28v6H0z"/><path fill="#ffce00" d="M0 13h28v7H0z"/>',
    fr: '<path fill="#002395" d="M0 0h9v20H0z"/><path fill="#fff" d="M9 0h10v20H9z"/><path fill="#ed2939" d="M19 0h9v20h-9z"/>',
    es: '<path fill="#aa151b" d="M0 0h28v20H0z"/><path fill="#f1bf00" d="M0 5h28v10H0z"/>',
  };
  function flag(lang) {
    if (flagShapes[lang]) return '<svg viewBox="0 0 28 20" aria-hidden="true">' + flagShapes[lang] + '</svg>';
    return '<svg viewBox="0 0 28 20" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="14" cy="10" r="8"/><ellipse cx="14" cy="10" rx="4" ry="8"/><path d="M6 10h16"/></svg>';
  }
  function languageName(lang) {
    return (lang === graphLanguage ? config.ui_strings?.languageName : undefined) || catalogs[lang]?.languageName || lang.toUpperCase();
  }
  function applyTheme() {
    root.dataset.theme = theme === "system" ? (media.matches ? "dark" : "light") : theme;
    root.style.colorScheme = root.dataset.theme;
    document.querySelectorAll("[data-theme-choice]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.themeChoice === theme)));
    document.dispatchEvent(new CustomEvent("repo-theme-change"));
  }
  function translate() {
    root.lang = language;
    for (const element of document.querySelectorAll("[data-i18n]")) element.textContent = t(element.dataset.i18n);
    for (const element of document.querySelectorAll("[data-i18n-aria]")) element.setAttribute("aria-label", t(element.dataset.i18nAria));
    for (const element of document.querySelectorAll("[data-i18n-title]")) element.title = t(element.dataset.i18nTitle);
    for (const element of document.querySelectorAll("[data-i18n-placeholder]")) element.placeholder = t(element.dataset.i18nPlaceholder);
    const toggle = document.getElementById("language-toggle");
    if (toggle) {
      document.getElementById("current-flag").innerHTML = flag(language);
      document.getElementById("current-language").textContent = languageName(language);
      document.getElementById("current-language-code").textContent = language.toUpperCase();
      toggle.title = t("languageLabel") + ": " + languageName(language);
      document.querySelectorAll("[data-language-choice]").forEach(button => button.setAttribute("aria-selected", String(button.dataset.languageChoice === language)));
    }
    const note = document.getElementById("graph-language-note");
    if (note) {
      const content = config.content_languages || [config.language];
      note.hidden = language === graphLanguage || content.includes(language);
      note.textContent = t("graphLanguageNote", {language: languageName(graphLanguage)});
    }
  }
  function setLanguage(value) {
    if (!supports(value)) return;
    language = value;
    storage.set("rv-language", language);
    translate();
    if (config.landing && location.protocol !== "file:") {
      const url = new URL(location.href); url.searchParams.set("lang", value); history.replaceState(null, "", url);
    }
    document.dispatchEvent(new CustomEvent("repo-language-change"));
  }
  function setTheme(value) {
    if (!["light", "dark", "system"].includes(value)) return;
    theme = value;
    storage.set("rv-theme", theme);
    applyTheme();
    if (config.landing && location.protocol !== "file:") {
      const url = new URL(location.href); url.searchParams.set("theme", value); history.replaceState(null, "", url);
    }
  }
  window.repoAppearance = {t, setLanguage, setTheme, translate, get language() {return language;}, get theme() {return theme;}, get resolvedTheme() {return root.dataset.theme;}};
  storage.set("rv-language", language); storage.set("rv-theme", theme); applyTheme();
  media.addEventListener("change", () => { if (theme === "system") applyTheme(); });
  document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("language-toggle");
    const menu = document.getElementById("language-menu");
    if (toggle && menu) {
      // Downloaded HTML can already contain options cloned from a live page.
      menu.replaceChildren();
      const options = [];
      function close(restoreFocus = false) {
        menu.hidden = true; toggle.setAttribute("aria-expanded", "false");
        if (restoreFocus) toggle.focus();
      }
      function open() {
        menu.hidden = false; toggle.setAttribute("aria-expanded", "true");
        (options.find(option => option.dataset.languageChoice === language) || options[0])?.focus();
      }
      const languages = [...Object.keys(catalogs)];
      if (!languages.includes(graphLanguage) && supports(graphLanguage)) languages.push(graphLanguage);
      for (const lang of languages) {
        const option = document.createElement("button");
        option.type = "button"; option.className = "language-option"; option.role = "option";
        option.dataset.languageChoice = lang;
        const symbol = document.createElement("span"); symbol.className = "locale-flag"; symbol.setAttribute("aria-hidden", "true"); symbol.innerHTML = flag(lang);
        const label = document.createElement("span"); label.textContent = languageName(lang);
        option.append(symbol, label);
        const check = document.createElementNS("http://www.w3.org/2000/svg", "svg"); check.setAttribute("viewBox", "0 0 20 20"); check.setAttribute("aria-hidden", "true"); check.classList.add("locale-check");
        const path = document.createElementNS("http://www.w3.org/2000/svg", "path"); path.setAttribute("d", "m4 10 4 4 8-8"); check.append(path); option.append(check);
        option.addEventListener("click", () => { setLanguage(lang); close(true); });
        options.push(option); menu.append(option);
      }
      toggle.addEventListener("click", () => menu.hidden ? open() : close(true));
      toggle.addEventListener("keydown", event => { if (["ArrowDown", "ArrowUp"].includes(event.key)) {event.preventDefault(); open();} });
      menu.addEventListener("keydown", event => {
        const index = options.indexOf(document.activeElement);
        if (event.key === "Escape") {event.preventDefault(); close(true);}
        else if (event.key === "Tab") close(true);
        else if (["ArrowDown", "ArrowUp", "Home", "End"].includes(event.key)) {
          event.preventDefault();
          const next = event.key === "Home" ? 0 : event.key === "End" ? options.length - 1 : (index + (event.key === "ArrowDown" ? 1 : -1) + options.length) % options.length;
          options[next].focus();
        }
      });
      document.addEventListener("click", event => { if (!event.target.closest(".language-control")) close(); });
    }
    document.querySelectorAll("[data-theme-choice]").forEach(button => button.addEventListener("click", () => setTheme(button.dataset.themeChoice)));
    translate(); applyTheme();
  });
})();
