// Rasterise docs/assets/icon.svg into the PNG sizes the manifest and the
// release builds need. Development tool only — the app loads nothing.
//
//   node scripts/icons.mjs
//
import puppeteer from 'puppeteer-core';
import fs from 'node:fs';
import path from 'node:path';

const dir = 'docs/assets';
const svg = fs.readFileSync(path.join(dir, 'icon.svg'), 'utf8');
const sizes = [192, 512, 256, 64, 48, 32, 16];

const browser = await puppeteer.launch({
  executablePath: '/usr/local/bin/chromium',
  args: ['--no-sandbox', '--disable-gpu', '--force-color-profile=srgb'],
});

for (const s of sizes) {
  const page = await browser.newPage();
  await page.setViewport({ width: s, height: s, deviceScaleFactor: 1 });
  await page.setContent(
    `<body style="margin:0;background:transparent">${svg.replace('<svg', `<svg width="${s}" height="${s}"`)}</body>`,
    { waitUntil: 'load' }
  );
  const out = path.join(dir, `icon-${s}.png`);
  await page.screenshot({ path: out, omitBackground: true });
  console.log('wrote', out);
  await page.close();
}

/* A social card, generated from the same icon and wordmark — so a shared link
   shows the app instead of a grey rectangle, with no image service involved. */
{
  const page = await browser.newPage();
  await page.setViewport({ width: 1200, height: 630, deviceScaleFactor: 1 });
  const card = `<!doctype html><meta charset="utf-8">
  <body style="margin:0;width:1200px;height:630px;background:#f4ecdd;color:#1a1510;
    font-family:ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
    display:flex;flex-direction:column;justify-content:center;padding:0 84px;
    background-image:repeating-linear-gradient(to bottom,transparent 0 47px,rgba(194,177,149,.5) 47px 48px)">
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:34px">
      <div style="width:76px;height:76px;border:2px solid #1a1510;border-radius:4px;display:grid;place-items:center;
        font:700 40px/1 Georgia,serif;background:#faf5ea">R</div>
      <div style="font:600 15px/1.5 ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;letter-spacing:.18em;text-transform:uppercase;color:#7d6f5c">
        Repertorium Publicum · 2008</div>
    </div>
    <div style="font:800 62px/1.02 ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;letter-spacing:-.03em;max-width:15ch">
      The repertory is a ledger.<br><span style="color:#b5432c">Search it like one.</span></div>
    <div style="margin-top:30px;font:500 23px/1.5 Georgia,serif;color:#4a4034;max-width:34ch">
      74,480 rubrics · 735,460 graded links · one file, offline</div>
    <div style="position:absolute;right:84px;bottom:64px;font:600 17px/1 ui-sans-serif,system-ui,-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;letter-spacing:.16em;
      text-transform:uppercase;color:#b5432c;border:2px solid #b5432c;padding:12px 16px;border-radius:3px;
      transform:rotate(-4deg)">On this device</div>
  </body>`;
  await page.setContent(card, { waitUntil: 'load' });
  await page.screenshot({ path: path.join(dir, 'og.png') });
  console.log('wrote', path.join(dir, 'og.png'));
  await page.close();
}

await browser.close();
