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

  function calendarPanelIsSelected(panel, preferences) {
    return panel.region === preferences.region
      && panel.medium === preferences.calendarMedium
      && panel.season === preferences.calendarSeason;
  }

  function calendarSeasonOptionIsSelected(option, preferences) {
    return option.region === preferences.region
      && option.season === preferences.calendarSeason;
  }

  function loadPreferences(storage) {
    try {
      const saved = JSON.parse(storage.getItem(STORAGE_KEY) || "{}");
      return {
        region: typeof saved.region === "string" ? saved.region : "GB",
        calendarMedium: ["tv", "movie"].includes(saved.calendarMedium) ? saved.calendarMedium : "tv",
        calendarSeason: typeof saved.calendarSeason === "string" ? saved.calendarSeason : "",
      };
    } catch (_) {
      return { region: "GB", calendarMedium: "tv", calendarSeason: "" };
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
    const globalRegionSelect = app.querySelector("[data-global-region]");
    const regionPanels = Array.from(app.querySelectorAll("[data-region-code]"));
    const calendarSeasonSelect = app.querySelector("[data-calendar-season]");
    const calendarMediumButtons = Array.from(app.querySelectorAll("[data-calendar-medium]"));
    const calendarPanels = Array.from(app.querySelectorAll("[data-calendar-panel]"));
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
        savePreferences(storage, preferences);
      }
      regionPanels.forEach((panel) => { panel.hidden = !regionIsSelected(panel.dataset.regionCode, preferences.region); });
      if (globalRegionSelect) globalRegionSelect.value = preferences.region;
    }

    function applyCalendar() {
      if (!calendarPanels.length) return;
      const matchingRegionAndMedium = calendarPanels.filter((panel) => (
        panel.dataset.calendarRegion === preferences.region
        && panel.dataset.calendarType === preferences.calendarMedium
      ));
      if (!matchingRegionAndMedium.some((panel) => panel.dataset.calendarSeason === preferences.calendarSeason)) {
        preferences.calendarSeason = matchingRegionAndMedium.length
          ? matchingRegionAndMedium[0].dataset.calendarSeason
          : calendarPanels[0].dataset.calendarSeason;
        savePreferences(storage, preferences);
      }
      calendarPanels.forEach((panel) => {
        panel.hidden = !calendarPanelIsSelected({
          region: panel.dataset.calendarRegion,
          medium: panel.dataset.calendarType,
          season: panel.dataset.calendarSeason,
        }, preferences);
      });
      calendarMediumButtons.forEach((button) => {
        button.setAttribute("aria-pressed", String(button.dataset.calendarMedium === preferences.calendarMedium));
      });
      if (calendarSeasonSelect) {
        Array.from(calendarSeasonSelect.options).forEach((option) => {
          const available = option.dataset.calendarSeasonRegion === preferences.region
            && calendarPanels.some((panel) => (
              panel.dataset.calendarRegion === preferences.region
              && panel.dataset.calendarType === preferences.calendarMedium
              && panel.dataset.calendarSeason === option.value
            ));
          option.hidden = !available;
          option.disabled = !available;
          option.selected = available && calendarSeasonOptionIsSelected({
            region: option.dataset.calendarSeasonRegion,
            season: option.value,
          }, preferences);
        });
      }
    }

    if (globalRegionSelect) {
      applyRegion();
      globalRegionSelect.addEventListener("change", () => {
        preferences.region = globalRegionSelect.value;
        savePreferences(storage, preferences);
        applyRegion();
        applyCalendar();
      });
    }
    if (calendarSeasonSelect) {
      calendarSeasonSelect.addEventListener("change", () => {
        preferences.calendarSeason = calendarSeasonSelect.value;
        savePreferences(storage, preferences);
        applyCalendar();
      });
    }
    calendarMediumButtons.forEach((button) => {
      button.addEventListener("click", () => {
        preferences.calendarMedium = button.dataset.calendarMedium;
        preferences.calendarSeason = "";
        savePreferences(storage, preferences);
        applyCalendar();
      });
    });

    applyCalendar();
    applyFilter();
  }

  return {
    filterItems,
    pickRandom,
    regionIsSelected,
    calendarPanelIsSelected,
    calendarSeasonOptionIsSelected,
    loadPreferences,
    savePreferences,
    init,
  };
});
