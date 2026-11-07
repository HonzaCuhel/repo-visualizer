/* Theme and interface language are user preferences, independent of the agent. */
(() => {
  "use strict";
  const config = JSON.parse(
    document.getElementById("appearance-config").textContent,
  );
  const catalogs = JSON.parse(
    document.getElementById("interface-locales").textContent,
  );
  const root = document.documentElement;
  const storage = {
    get(key) {
      try {
        return localStorage.getItem(key);
      } catch {
        return null;
      }
    },
    set(key, value) {
      try {
        localStorage.setItem(key, value);
      } catch {}
    },
  };
  const query = new URLSearchParams(location.search);
  const graphLanguage = config.language.split("-")[0].toLowerCase();
  const supports = (lang) =>
    Boolean(
      catalogs[lang] ||
        (lang === graphLanguage &&
          config.ui_strings &&
          Object.keys(config.ui_strings).length),
    );
  let language = [
    query.get("lang"),
    storage.get("rv-language"),
    config.preference?.language,
    config.landing ? navigator.language.split("-")[0] : graphLanguage,
    "en",
  ].find(supports);
  let theme = [
    query.get("theme"),
    storage.get("rv-theme"),
    config.preference?.theme,
    "system",
  ].find((value) => ["light", "dark", "system"].includes(value));
  const media = matchMedia("(prefers-color-scheme: dark)");
  function t(key, values = {}) {
    const custom =
      language === graphLanguage ? config.ui_strings?.[key] : undefined;
    return String(
      custom ?? catalogs[language]?.[key] ?? catalogs.en[key] ?? key,
    ).replace(/\{(\w+)\}/g, (_, name) =>
      String(values[name] ?? "{" + name + "}"),
    );
  }
  function applyTheme() {
    root.dataset.theme =
      theme === "system" ? (media.matches ? "dark" : "light") : theme;
    root.style.colorScheme = root.dataset.theme;
    document
      .querySelector(".theme-control svg path")
      ?.setAttribute(
        "d",
        root.dataset.theme === "dark"
          ? "M20.5 14.4A8.5 8.5 0 0 1 9.6 3.5 8.5 8.5 0 1 0 20.5 14.4Z"
          : "M12 8a4 4 0 1 0 0 8a4 4 0 0 0 0-8M12 2v2m0 16v2M2 12h2m16 0h2M5 5l1.5 1.5m11 11L19 19M5 19l1.5-1.5m11-11L19 5",
      );
    document
      .querySelectorAll("[data-theme-choice]")
      .forEach((b) =>
        b.setAttribute("aria-pressed", String(b.dataset.themeChoice === theme)),
      );
    const select = document.getElementById("theme-select");
    if (select) select.value = theme;
    document.dispatchEvent(new CustomEvent("repo-theme-change"));
  }
  function translate() {
    root.lang = language;
    for (const element of document.querySelectorAll("[data-i18n]"))
      element.textContent = t(element.dataset.i18n);
    for (const element of document.querySelectorAll("[data-i18n-aria]"))
      element.setAttribute("aria-label", t(element.dataset.i18nAria));
    for (const element of document.querySelectorAll("[data-i18n-title]"))
      element.title = t(element.dataset.i18nTitle);
    for (const element of document.querySelectorAll("[data-i18n-placeholder]"))
      element.placeholder = t(element.dataset.i18nPlaceholder);
    const select = document.getElementById("language-select");
    if (select) select.value = language;
  }
  function setLanguage(value) {
    if (!supports(value)) return;
    language = value;
    storage.set("rv-language", language);
    translate();
    if (config.landing && location.protocol !== "file:") {
      const url = new URL(location.href);
      url.searchParams.set("lang", value);
      history.replaceState(null, "", url);
    }
    document.dispatchEvent(new CustomEvent("repo-language-change"));
  }
  function setTheme(value) {
    if (!["light", "dark", "system"].includes(value)) return;
    theme = value;
    storage.set("rv-theme", theme);
    applyTheme();
    if (config.landing && location.protocol !== "file:") {
      const url = new URL(location.href);
      url.searchParams.set("theme", value);
      history.replaceState(null, "", url);
    }
  }
  window.repoAppearance = {
    t,
    setLanguage,
    setTheme,
    translate,
    get language() {
      return language;
    },
    get theme() {
      return theme;
    },
    get resolvedTheme() {
      return root.dataset.theme;
    },
  };
  storage.set("rv-language", language);
  storage.set("rv-theme", theme);
  applyTheme();
  media.addEventListener("change", () => {
    if (theme === "system") applyTheme();
  });
  document.addEventListener("DOMContentLoaded", () => {
    const languageSelect = document.getElementById("language-select");
    if (languageSelect) {
      if (!catalogs[graphLanguage] && supports(graphLanguage)) {
        const option = document.createElement("option");
        option.value = graphLanguage;
        option.textContent = config.ui_strings.languageName || graphLanguage;
        languageSelect.append(option);
      }
      languageSelect.addEventListener("change", (event) =>
        setLanguage(event.target.value),
      );
    }
    document
      .getElementById("theme-select")
      ?.addEventListener("change", (event) => setTheme(event.target.value));
    translate();
    applyTheme();
  });
})();
