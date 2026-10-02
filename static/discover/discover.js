(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.isoulDiscover = api;
  if (root && root.document) {
    if (root.document.readyState === "loading") root.document.addEventListener("DOMContentLoaded", api.init);
    else api.init();
  }
})(typeof window !== "undefined" ? window : null, function () {
  "use strict";

  const STORAGE_KEY = "isoul.discover.preferences.v1";

  function filterItems(items, criteria) {
    const selected = criteria || {};
    return items.filter((item) => {
      if (selected.type && selected.type !== "all" && item.type !== selected.type) return false;
      if (selected.country && !(item.country || []).includes(selected.country)) return false;
      if (selected.genre && !(item.genres || []).includes(selected.genre)) return false;
      if (selected.underTwoHours && !(item.type === "film" && item.runtime_minutes <= 120)) return false;
      return true;
    });
  }

  function pickRandom(items, randomFn) {
    if (!items.length) return null;
    const random = randomFn || Math.random;
    return items[Math.min(items.length - 1, Math.floor(random() * items.length))];
  }

  function regionIsSelected(regionCode, selectedCode) {
    return regionCode === selectedCode;
  }

  function loadPreferences(storage) {
    try {
      const saved = JSON.parse(storage.getItem(STORAGE_KEY) || "{}");
      return { region: typeof saved.region === "string" ? saved.region : "GB" };
    } catch (_) {
      return { region: "GB" };
    }
  }

  function savePreferences(storage, preferences) {
    storage.setItem(STORAGE_KEY, JSON.stringify(preferences));
  }

  function init() {
    const app = document.querySelector("[data-discover-app]");
    if (!app) return;

    const cards = Array.from(app.querySelectorAll("[data-discover-card]"));
    const catalog = cards.map((card) => ({
      id: card.dataset.id,
      type: card.dataset.mediaType,
      country: (card.dataset.country || "").split("|").filter(Boolean),
      genres: (card.dataset.genres || "").split("|").filter(Boolean),
      runtime_minutes: Number(card.dataset.runtime || 0),
    }));
    const filterButtons = Array.from(app.querySelectorAll("[data-filter-type]"));
    const status = app.querySelector("[data-filter-status]");
    const randomButton = app.querySelector("[data-random]");
    const regionSelect = app.querySelector("[data-region]");
    const regionPanels = Array.from(app.querySelectorAll("[data-region-code]"));
    const storage = window.localStorage;
    const preferences = loadPreferences(storage);
    const criteria = { type: "all" };

    function applyFilter() {
      const visible = filterItems(catalog, criteria);
      const ids = new Set(visible.map((item) => item.id));
      cards.forEach((card) => { card.hidden = !ids.has(card.dataset.id); });
      if (status) status.textContent = `${visible.length} hand-picked ${visible.length === 1 ? "item" : "items"}`;
      return visible;
    }

    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        criteria.type = button.dataset.filterType;
        filterButtons.forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button)));
        applyFilter();
      });
    });

    if (randomButton) {
      randomButton.addEventListener("click", () => {
        const chosen = pickRandom(applyFilter());
        if (!chosen) return;
        const card = app.querySelector(`[data-id="${CSS.escape(chosen.id)}"]`);
        cards.forEach((item) => item.classList.remove("discover-card--chosen"));
        card.classList.add("discover-card--chosen");
        card.scrollIntoView({ behavior: "smooth", block: "center" });
      });
    }

    function applyRegion() {
      if (!regionPanels.some((panel) => panel.dataset.regionCode === preferences.region) && regionPanels.length) {
        preferences.region = regionPanels[0].dataset.regionCode;
      }
      regionPanels.forEach((panel) => { panel.hidden = !regionIsSelected(panel.dataset.regionCode, preferences.region); });
      if (regionSelect) regionSelect.value = preferences.region;
    }

    if (regionSelect) {
      applyRegion();
      regionSelect.addEventListener("change", () => {
        preferences.region = regionSelect.value;
        savePreferences(storage, preferences);
        applyRegion();
      });
    }

    applyFilter();
  }

  return { filterItems, pickRandom, regionIsSelected, loadPreferences, savePreferences, init };
});
