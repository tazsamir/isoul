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

const storage = new Map();
const localStorageStub = {
  getItem: (key) => storage.has(key) ? storage.get(key) : null,
  setItem: (key, value) => storage.set(key, value),
};

discover.savePreferences(localStorageStub, {
  region: 'GB',
});
assert.deepEqual(discover.loadPreferences(localStorageStub), {
  region: 'GB',
});

console.log('discover.js behavior tests passed');
