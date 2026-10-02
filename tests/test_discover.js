const assert = require('node:assert/strict');
const path = require('node:path');

const discover = require(path.join(__dirname, '..', 'static', 'discover', 'discover.js'));

const catalog = [
  { id: 'film', type: 'film', country: ['United Kingdom'], genres: ['Drama'], runtime_minutes: 90 },
  { id: 'anime', type: 'anime', country: ['Japan'], genres: ['Fantasy'] },
  { id: 'long-film', type: 'film', country: ['France'], genres: ['Drama'], runtime_minutes: 140 },
];

assert.deepEqual(discover.filterItems(catalog, { type: 'film' }).map((item) => item.id), ['film', 'long-film']);
assert.deepEqual(discover.filterItems(catalog, { country: 'Japan' }).map((item) => item.id), ['anime']);
assert.deepEqual(discover.filterItems(catalog, { underTwoHours: true }).map((item) => item.id), ['film']);
assert.equal(discover.pickRandom(catalog, () => 0.6).id, 'anime');

assert.equal(discover.regionIsSelected('GB', 'GB'), true);
assert.equal(discover.regionIsSelected('JP', 'GB'), false);
assert.equal(discover.calendarPanelIsSelected(
  { region: 'GB', medium: 'tv', season: '2026-autumn' },
  { region: 'GB', calendarMedium: 'tv', calendarSeason: '2026-autumn' },
), true);
assert.equal(discover.calendarPanelIsSelected(
  { region: 'US', medium: 'tv', season: '2026-autumn' },
  { region: 'GB', calendarMedium: 'tv', calendarSeason: '2026-autumn' },
), false);
assert.equal(discover.calendarSeasonOptionIsSelected(
  { region: 'US', season: '2026-autumn' },
  { region: 'US', calendarSeason: '2026-autumn' },
), true);
assert.equal(discover.calendarSeasonOptionIsSelected(
  { region: 'GB', season: '2026-autumn' },
  { region: 'US', calendarSeason: '2026-autumn' },
), false);

const storage = new Map();
const localStorageStub = {
  getItem: (key) => storage.has(key) ? storage.get(key) : null,
  setItem: (key, value) => storage.set(key, value),
};

discover.savePreferences(localStorageStub, {
  region: 'GB',
  calendarMedium: 'movie',
  calendarSeason: '2026-autumn',
});
assert.deepEqual(discover.loadPreferences(localStorageStub), {
  region: 'GB',
  calendarMedium: 'movie',
  calendarSeason: '2026-autumn',
});

function fakeElement({ dataset = {}, value = '', options = [] } = {}) {
  const listeners = new Map();
  const attributes = new Map();
  return {
    dataset,
    value,
    options,
    hidden: false,
    disabled: false,
    selected: false,
    addEventListener(type, listener) { listeners.set(type, listener); },
    dispatch(type) { listeners.get(type)?.(); },
    setAttribute(name, valueToSet) { attributes.set(name, valueToSet); },
    getAttribute(name) { return attributes.get(name); },
  };
}

const globalRegion = fakeElement({ value: 'GB' });
const tonightGb = fakeElement({ dataset: { regionCode: 'GB' } });
const tonightUs = fakeElement({ dataset: { regionCode: 'US' } });
const seasonGb = fakeElement({ dataset: { calendarSeasonRegion: 'GB' }, value: '2026-autumn' });
const seasonUs = fakeElement({ dataset: { calendarSeasonRegion: 'US' }, value: '2026-autumn' });
const seasonSelect = fakeElement({ options: [seasonGb, seasonUs], value: '2026-autumn' });
const tvButton = fakeElement({ dataset: { calendarMedium: 'tv' } });
const movieButton = fakeElement({ dataset: { calendarMedium: 'movie' } });
const calendarGbTv = fakeElement({ dataset: { calendarRegion: 'GB', calendarType: 'tv', calendarSeason: '2026-autumn' } });
const calendarGbMovie = fakeElement({ dataset: { calendarRegion: 'GB', calendarType: 'movie', calendarSeason: '2026-autumn' } });
const calendarUsTv = fakeElement({ dataset: { calendarRegion: 'US', calendarType: 'tv', calendarSeason: '2026-autumn' } });
const calendarUsMovie = fakeElement({ dataset: { calendarRegion: 'US', calendarType: 'movie', calendarSeason: '2026-autumn' } });
const tonightPanels = [tonightGb, tonightUs];
const mediumButtons = [tvButton, movieButton];
const calendarPanels = [calendarGbTv, calendarGbMovie, calendarUsTv, calendarUsMovie];
const domStorage = new Map();
const domStorageStub = {
  getItem: (key) => domStorage.has(key) ? domStorage.get(key) : null,
  setItem: (key, value) => domStorage.set(key, value),
};
const app = {
  querySelector(selector) {
    return {
      '[data-global-region]': globalRegion,
      '[data-calendar-season]': seasonSelect,
    }[selector] || null;
  },
  querySelectorAll(selector) {
    return {
      '[data-discover-card]': [],
      '[data-filter-type]': [],
      '[data-region-code]': tonightPanels,
      '[data-calendar-medium]': mediumButtons,
      '[data-calendar-panel]': calendarPanels,
    }[selector] || [];
  },
};

global.window = { localStorage: domStorageStub };
global.document = { querySelector: (selector) => selector === '[data-discover-app]' ? app : null };
discover.init();

globalRegion.value = 'US';
globalRegion.dispatch('change');
assert.equal(tonightGb.hidden, true);
assert.equal(tonightUs.hidden, false);
assert.equal(calendarGbTv.hidden, true);
assert.equal(calendarUsTv.hidden, false);
assert.equal(calendarUsMovie.hidden, true);
assert.equal(seasonGb.hidden, true);
assert.equal(seasonGb.disabled, true);
assert.equal(seasonUs.hidden, false);
assert.equal(seasonUs.disabled, false);
assert.equal(seasonUs.selected, true);
assert.equal(globalRegion.value, 'US');
assert.deepEqual(JSON.parse(domStorage.get('isoul.discover.preferences.v1')), {
  region: 'US',
  calendarMedium: 'tv',
  calendarSeason: '2026-autumn',
});
delete global.window;
delete global.document;

console.log('discover.js behavior tests passed');
