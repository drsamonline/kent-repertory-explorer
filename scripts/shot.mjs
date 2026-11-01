// Screenshots for this repo's docs — a DEVELOPMENT tool, not a runtime dependency.
// The app itself loads nothing: this file is only run by a maintainer, and needs
// puppeteer-core + a local Chromium.
//
//   node scripts/shot.mjs --url docs/play/index.html#demo=analysis --out docs/assets/app-desktop.png --w 1280 --h 820
//
import puppeteer from 'puppeteer-core';
import path from 'node:path';
import fs from 'node:fs';

const args = {};
for (let i = 2; i < process.argv.length; i += 2) args[process.argv[i].replace(/^--/, '')] = process.argv[i + 1];

const url = args.url || 'docs/index.html';
const out = args.out || 'docs/assets/shot.png';
const w = +(args.w || 1280);
const h = +(args.h || 820);
const waitFor = args.wait || null;         // JS expression that must be true before the shot
const full = args.full === '1';

const abs = path.resolve(url.startsWith('file:') ? url.replace('file://', '') : url);
const fileUrl = 'file://' + abs.split('#')[0] + (abs.includes('#') ? '#' + abs.split('#')[1] : '');

const browser = await puppeteer.launch({
  executablePath: '/usr/local/bin/chromium',
  args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
         '--force-color-profile=srgb', '--font-render-hinting=none'],
  defaultViewport: { width: w, height: h, deviceScaleFactor: 1 },
});
const page = await browser.newPage();
if (args.dark === '1') await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'dark' }]);
await page.goto(fileUrl, { waitUntil: 'load', timeout: 60000 });
if (waitFor) await page.waitForFunction(waitFor, { timeout: 45000, polling: 100 });
if (args.y) await page.evaluate(y => window.scrollTo(0, +y), args.y);
await new Promise(r => setTimeout(r, +(args.settle || 900)));   // let transitions settle
fs.mkdirSync(path.dirname(out), { recursive: true });
await page.screenshot({ path: out, fullPage: full });
await browser.close();
console.log('wrote', out, fs.statSync(out).size, 'bytes');
