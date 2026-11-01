// The optional browser suite. Unlike tests/retrofit-web-kit.test.js this one is
// NOT dependency-free: it drives a real Chromium through puppeteer-core to prove
// the enhancement layer does what the changelog says.
//
//   npm i puppeteer-core                      # dev only, not a runtime dependency
//   CHROME=/usr/bin/chromium node tests/enhancements.test.mjs
//
import puppeteer from 'puppeteer-core';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const URL = pathToFileURL(path.join(ROOT, 'docs/play/index.html')).href;
const ok = [], bad = [];
const t = (name, cond, extra = '') => (cond ? ok : bad).push(name + (extra ? ' [' + extra + ']' : ''));

const browser = await puppeteer.launch({
  executablePath: process.env.CHROME || '/usr/local/bin/chromium',
  args: ['--no-sandbox', '--disable-gpu', '--allow-file-access-from-files', '--hide-scrollbars'],
  defaultViewport: { width: 1280, height: 860 },
});
const page = await browser.newPage();
const errors = [];
page.on('pageerror', e => errors.push(String(e).slice(0, 200)));

await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
await page.waitForFunction("document.getElementById('load').classList.contains('done')", { timeout: 45000, polling: 100 });
await new Promise(r => setTimeout(r, 800));

// 1 build stamp
t('build stamp in footer', await page.evaluate(() => !!document.getElementById('buildstamp')?.textContent));

// 16 light on first paint
t('theme follows the system (light)', await page.evaluate(() => document.body.classList.contains('light')));

// search + windowing + a11y
await page.click('#q');
await page.type('#q', 'weeping consolation');
await new Promise(r => setTimeout(r, 400));
const s1 = await page.evaluate(() => ({
  n: results.length, total: document.querySelector('#statline').textContent.trim(),
  more: !!document.getElementById('morebtn'),
  role: document.getElementById('listwrap').getAttribute('role'),
  opt: document.querySelector('#listwrap .rub')?.getAttribute('role'),
  act: document.getElementById('q').getAttribute('aria-activedescendant'),
  chipLabel: document.querySelector('#listwrap .rx')?.getAttribute('aria-label'),
}));
t('search returns rubrics', s1.n > 0, String(s1.n));
t('listbox role', s1.role === 'listbox');
t('options have role', s1.opt === 'option');
t('aria-activedescendant set', !!s1.act, s1.act || '');
t('remedy chip has an accessible label', !!s1.chipLabel, s1.chipLabel || '');

// 3 incremental narrowing gives the same answer as a cold search
const inc = await page.evaluate(() => {
  const q = document.getElementById('q');
  const stat = () => document.getElementById('statline').textContent.trim();
  q.value = ''; q.dispatchEvent(new Event('input', { bubbles: true }));
  ['w', 'we', 'wee', 'weep', 'weeping consolation'].forEach(v => {
    q.value = v; q.dispatchEvent(new Event('input', { bubbles: true }));
  });
  const warm = stat();
  q.value = ''; q.dispatchEvent(new Event('input', { bubbles: true }));
  q.value = 'weeping consolation'; q.dispatchEvent(new Event('input', { bubbles: true }));
  const cold = stat();
  return { warm, cold };
});
t('incremental narrowing == cold search', inc.warm === inc.cold && !!inc.cold, JSON.stringify(inc));

// 10 show more
const sm = await page.evaluate(() => {
  const q = document.getElementById('q');
  q.value = 'pain'; q.dispatchEvent(new Event('input', { bubbles: true }));
  const before = results.length, has = !!document.getElementById('morebtn');
  if (has) document.getElementById('morebtn').click();
  return { before, after: results.length, has };
});
t('progressive results (show more)', sm.has && sm.after > sm.before, JSON.stringify(sm));

// 4 typo suggestion
const fz = await page.evaluate(async () => {
  const q = document.getElementById('q');
  q.value = 'consolaton'; q.dispatchEvent(new Event('input', { bubbles: true }));
  return { total: results.length, sugg: [...document.querySelectorAll('[data-sugg]')].map(b => b.dataset.sugg) };
});
t('did-you-mean on a typo', fz.total === 0 && fz.sugg.includes('consolation'), JSON.stringify(fz));

// 5/7 remedy modals
const rx = await page.evaluate(() => {
  const q = document.getElementById('q');
  q.value = 'weeping consolation'; q.dispatchEvent(new Event('input', { bubbles: true }));
  const chip = document.querySelector('#listwrap .rx[data-rx]');
  chip.click();
  const title = document.getElementById('mtitle').textContent;
  const body = document.getElementById('mbody').textContent;
  closeModal();
  return { title, hasCount: /appears in \d+ rubrics/.test(body) };
});
t('remedy -> rubrics modal', rx.hasCount, rx.title);

// 6 case, undo, redo
await page.evaluate(() => { document.getElementById('q').value = 'weeping consolation'; runSearch(); });
await page.click('#listwrap .addbtn');
await new Promise(r => setTimeout(r, 150));
const afterAdd = await page.evaluate(() => caseList.length);
await page.evaluate(() => document.body.focus());
await page.keyboard.down('Control'); await page.keyboard.press('z'); await page.keyboard.up('Control');
await new Promise(r => setTimeout(r, 200));
const afterUndo = await page.evaluate(() => caseList.length);
await page.keyboard.down('Control'); await page.keyboard.down('Shift'); await page.keyboard.press('z');
await page.keyboard.up('Shift'); await page.keyboard.up('Control');
await new Promise(r => setTimeout(r, 200));
const afterRedo = await page.evaluate(() => caseList.length);
t('undo removes the rubric', afterAdd === 1 && afterUndo === 0, `${afterAdd}->${afterUndo}`);
t('redo puts it back', afterRedo === 1, String(afterRedo));

// 6 multiple cases
const mc = await page.evaluate(async () => {
  document.getElementById('btnnewcase').click();
  const opts = [...document.querySelectorAll('#casesel option')].map(o => o.textContent);
  const emptyNow = caseList.length;
  const first = [...document.querySelectorAll('#casesel option')][0].value;
  document.getElementById('casesel').value = first;
  document.getElementById('casesel').dispatchEvent(new Event('change'));
  const back = caseList.length;
  return { opts, emptyNow, back, stored: (LS.get('cases', null) || { list: [] }).list.length };
});
t('second case is empty and separate', mc.opts.length === 2 && mc.emptyNow === 0 && mc.back === 1, JSON.stringify(mc));
t('cases persist under their own key', mc.stored === 2, String(mc.stored));

// 8 explain the ranking
const cov = await page.evaluate(() => {
  setRTab('an');
  const cell = document.querySelector('#rbody [data-rem]');
  if (!cell) return { none: true };
  cell.click();
  const body = document.getElementById('mbody').textContent;
  const title = document.getElementById('mtitle').textContent;
  closeModal();
  return { title, why: /why it ranks here/.test(title), covers: /covers \d+ of \d+/.test(body) };
});
t('ranking explanation modal', cov.why && cov.covers, cov.title || 'none');

// 9 chapter drill-down
const ch = await page.evaluate(() => {
  setTab('browse');
  const card = document.querySelector('#chapters [data-chb]');
  const name = card.dataset.chb;
  card.click();
  const subs = [...document.querySelectorAll('#chapters [data-chsub]')].length;
  const back = !!document.querySelector('#chapters [data-chback]');
  document.querySelector('#chapters [data-chback]').click();
  const chaptersBack = [...document.querySelectorAll('#chapters [data-chb]')].length;
  setTab('search');
  return { name, subs, back, chaptersBack };
});
t('chapter drill-down shows branches', ch.subs > 1 && ch.back, JSON.stringify(ch));
t('back returns to all chapters', ch.chaptersBack === 41, String(ch.chaptersBack));

// 12 print sheet
const pr = await page.evaluate(() => {
  dispatchEvent(new Event('beforeprint'));
  const el = document.getElementById('printhead');
  return { exists: !!el, text: el ? el.textContent.slice(0, 60) : '' };
});
t('print sheet header', pr.exists && pr.text.length > 10, pr.text);

// 14 deep links
const dl = await page.evaluate(async () => {
  location.hash = '#remedy=Ars';
  await new Promise(r => setTimeout(r, 400));
  const t1 = document.getElementById('mtitle').textContent;
  closeModal();
  const target = RUBRICS[100];
  location.hash = '#rubric=' + target.id;
  await new Promise(r => setTimeout(r, 600));
  const body = document.getElementById('mbody').textContent;
  const shown = body.includes(target.path.join(' \u203a ')) && /grade/.test(body);
  const listed = !!document.querySelector('#listwrap .rub.open');
  location.hash = '';
  return { t1, shown, listed, path: target.path.join(' > ') };
});
t('#remedy= deep link', /Ars\./.test(dl.t1), dl.t1);
t('#rubric= deep link opens that rubric', dl.shown, dl.path);
t('#rubric= also highlights it in the list', dl.listed);

// 13 chip bar exists
t('header chip bar', await page.evaluate(() => !!document.getElementById('chipbar')));

t('no page errors', errors.length === 0, errors.slice(0, 2).join(' | '));

console.log('PASS ' + ok.length + '  FAIL ' + bad.length);
ok.forEach(x => console.log('  ok   ' + x));
bad.forEach(x => console.log('  FAIL ' + x));
await browser.close();
process.exit(bad.length ? 1 : 0);
