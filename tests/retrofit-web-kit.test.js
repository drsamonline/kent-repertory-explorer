'use strict';
/**
 * kent-repertory-explorer — the web-kit storage retrofit, proved.
 *
 * The app used to keep its state in a hand-rolled `LS` object over raw
 * localStorage under the `rp_` prefix. It now delegates to web-kit's
 * Loom.storage, namespaced to `rp_`. This suite asserts the three things that
 * retrofit could have got wrong, and one that a retrofit has got wrong before:
 *
 *   1. the kit is actually IN the page and actually does the writing;
 *   2. a value written through LS comes back through LS (a round trip);
 *   3. a key saved BEFORE the retrofit under `rp_<k>` is still read - no user
 *      loses a saved case because the store moved;
 *   4. the embedded repertory data still decompresses to the same counts.
 *
 * No dependencies: node's own vm + zlib.  node tests/retrofit-web-kit.test.js
 */
const fs = require('fs');
const path = require('path');
const vm = require('vm');
const zlib = require('zlib');

const root = path.join(__dirname, '..');
const file = process.argv[2] || path.join(root, 'docs/play/index.html');
const html = fs.readFileSync(file, 'utf8');

const results = [];
const ok = (n, c, e = '') => results.push({ n, p: !!c, e });

/* --- 1. the kit travels with the page -------------------------------------- */
const wkBlock = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).find(s => s.indexOf('web-kit — the shared offline-first runtime') !== -1);
ok('web-kit is inlined in the page', !!wkBlock);

const appBlock = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)]
  .map(m => m[1]).find(s => s.indexOf('async function loadData()') !== -1);
ok('the app script is still present', !!appBlock);

/* --- 2/3. run the real storage layer against a real-ish localStorage ------- */
function makeEnv(seed) {
  const store = Object.assign({}, seed || {});
  const localStorage = {
    getItem: k => (Object.prototype.hasOwnProperty.call(store, k) ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: k => { delete store[k]; },
    key: i => Object.keys(store)[i],
    get length() { return Object.keys(store).length; },
  };
  const ctx = { localStorage, console, JSON, Promise, Object, String, Date, Math, isNaN };
  ctx.window = ctx;
  ctx.document = { documentElement: { style: { setProperty() {} }, setAttribute() {} }, createElement() { return {}; } };
  vm.createContext(ctx);
  return { ctx, store };
}

function bootApp(seed) {
  const { ctx, store } = makeEnv(seed);
  if (wkBlock) vm.runInContext(wkBlock, ctx);
  const start = appBlock.indexOf("if(window.Loom&&Loom.storage) Loom.storage.namespace(");
  const end = appBlock.indexOf('async function loadData()');
  if (start === -1 || end === -1) throw new Error('storage preamble not found in the app script');
  vm.runInContext(appBlock.slice(start, end) + '\n;this.__LS=LS;', ctx);
  return { ctx, store, LS: ctx.__LS };
}

let app;
try { app = bootApp(); } catch (e) { ok('the storage preamble runs', false, String(e)); }
if (app) {
  ok('the storage preamble runs', true);
  ok('the kit is what provides storage', !!(app.ctx.Loom && app.ctx.Loom.storage));
  ok('the namespace is pinned to rp_', app.ctx.Loom.storage.prefix() === 'rp_:',
    String(app.ctx.Loom.storage.prefix()));

  // round trip: written through LS, read back through LS
  app.LS.set('caseList', [{ id: 'c1', note: 'sulpha' }]);
  const got = app.LS.get('caseList', null);
  ok('LS round-trips a value', Array.isArray(got) && got[0] && got[0].note === 'sulpha', JSON.stringify(got));
  ok('the value landed in the kit\'s namespaced key',
    app.store['rp_:caseList'] !== undefined, Object.keys(app.store).join(','));

  // a missing key still falls back to the default
  ok('a missing key returns the default', app.LS.get('never-written', 'D') === 'D');

  // a key saved BEFORE the retrofit is still read - the whole point of the guard
  const legacy = bootApp({ 'rp_caseList': JSON.stringify([{ id: 'old', note: 'belladonna' }]) });
  const oldVal = legacy.LS.get('caseList', null);
  ok('a pre-retrofit rp_ key is still read',
    Array.isArray(oldVal) && oldVal[0] && oldVal[0].id === 'old', JSON.stringify(oldVal));
  ok('the pre-retrofit key was not overwritten by a read', legacy.store['rp_:caseList'] === undefined);
}

/* --- 4. the embedded repertory data is untouched --------------------------- */
try {
  const m = html.match(/<script id="kentdata"[^>]*>([\s\S]*?)<\/script>/);
  const data = JSON.parse(zlib.gunzipSync(Buffer.from(m[1].replace(/\s+/g, ''), 'base64')).toString('utf8'));
  const counts = data.counts || {};
  const remedies = data.remedies || [];
  ok('the embedded data still decompresses', true);
  ok('the repertory still declares 74,480 rubrics', counts.rubrics === 74480, String(counts.rubrics));
  ok('the repertory still declares 735,460 graded links', counts.remedy_links === 735460, String(counts.remedy_links));
  ok('remedy count is 669', remedies.length === 669, String(remedies.length));
} catch (e) {
  ok('the embedded data still decompresses', false, String(e));
}

const failed = results.filter(r => !r.p);
console.log('\n==== RESULTS ====');
results.forEach(r => console.log(`${r.p ? 'PASS' : 'FAIL'}  ${r.n}${r.e ? '  [' + r.e + ']' : ''}`));
console.log(`\n${results.length - failed.length}/${results.length} passed`);
process.exit(failed.length ? 1 : 0);
