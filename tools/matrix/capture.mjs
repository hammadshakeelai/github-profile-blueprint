// Capture the technique gallery in Chromium, Firefox and WebKit.
//
//   PLAYWRIGHT_CORE=/path/to/node_modules/playwright-core node tools/matrix/capture.mjs
//
// Needs playwright-core and its browser builds (npm i playwright-core@1.63 &&
// npx playwright install chromium firefox webkit). WebKit is Safari's engine,
// so it stands in for Safari; it is not iOS Safari or the GitHub mobile app.
//
// For every engine x width x colour scheme it loads GALLERY.md as rendered on
// github.com, lists the gallery images, and saves FRAMES crops of each shown
// image, FRAME_GAP ms apart. tools/matrix/analyze.py scores them with the same
// frame-diff and pixel checks used by tools/techniques/verify.py.

import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const OUT = process.env.OUT || path.join(ROOT, '.cache', 'matrix');
const REF = process.env.REF || 'v2/research';
const PAGE = process.env.PAGE || 'docs/techniques/GALLERY.md';
const URL = `https://github.com/hammadshakeelai/github-profile-blueprint/blob/${REF}/${PAGE}`;
// 'reduce' emulates a viewer who has asked their OS for less animation.
const REDUCED = process.env.REDUCED || 'no-preference';
// 730ms rather than a round number: a gap that divides a loop's length evenly
// revisits the same few moments every cycle and can miss brief motion entirely.
const FRAMES = +(process.env.FRAMES || 8), FRAME_GAP = +(process.env.FRAME_GAP || 730);
const ONLY = process.env.ONLY ? new Set(process.env.ONLY.split(',')) : null;

const ENGINES = ['chromium', 'firefox', 'webkit'];
const WIDTHS = process.env.WIDTHS ? process.env.WIDTHS.split(',').map(Number) : [1280, 390];
const SCHEMES = process.env.SCHEMES ? process.env.SCHEMES.split(',') : ['dark', 'light'];

const LIST = `(async () => {
  const art = document.querySelector('article.markdown-body');
  if (!art) return {error: 'no-article'};
  const imgs = [...art.querySelectorAll('img')];
  await Promise.race([
    Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => {
      i.addEventListener('load', r, {once: true}); i.addEventListener('error', r, {once: true}); }))),
    new Promise(r => setTimeout(r, 15000))]);
  await new Promise(r => setTimeout(r, 1500));
  // GitHub's desktop file view re-renders markdown client-side after load, replacing the <img> elements; measuring the first set would read detached nodes as zero-sized. So wait, then query afresh.
  const live = document.querySelector('article.markdown-body');
  const fresh = [...live.querySelectorAll('img')];
  return {
    container: Math.round(live.getBoundingClientRect().width),
    images: fresh.map(i => { const b = i.getBoundingClientRect(); const src = i.currentSrc || i.src;
      return { src, file: (src.match(/examples\\/([\\w-]+\\.svg)/) || [])[1] || null,
        loaded: i.complete && i.naturalWidth > 0,
        x: b.left + scrollX, y: b.top + scrollY, w: b.width, h: b.height,
        shown: b.width > 0 && b.height > 0 && getComputedStyle(i).display !== 'none' }; }) };
})()`;

async function pass(browser, engine, width, scheme) {
  const opts = { viewport: { width, height: 9000 }, colorScheme: scheme, deviceScaleFactor: 1,
                 reducedMotion: REDUCED };
  // Firefox has no mobile emulation mode; it gets the narrow viewport only.
  if (width < 700 && engine !== 'firefox') Object.assign(opts, { isMobile: true, hasTouch: true });
  const ctx = await browser.newContext(opts);
  const page = await ctx.newPage();
  const dir = path.join(OUT, `${engine}-${width}-${scheme}`);
  fs.mkdirSync(dir, { recursive: true });
  try {
    let listing;
    for (let attempt = 0; attempt < 3; attempt++) {
      await page.goto(URL, { waitUntil: 'load', timeout: 60000 });
      listing = await page.evaluate(LIST);
      if (!listing.error && listing.images.some(i => i.shown)) break;
      await page.waitForTimeout(8000);
    }
    const shown = (listing.images || []).filter(i => i.file && i.shown && (!ONLY || ONLY.has(i.file)));
    for (let step = 0; step < FRAMES; step++) {
      if (step) await page.waitForTimeout(FRAME_GAP);
      for (const im of shown) {
        await page.screenshot({ path: path.join(dir, `${im.file}.${step}.png`),
          clip: { x: im.x, y: im.y, width: im.w, height: im.h } });
      }
    }
    fs.writeFileSync(path.join(dir, 'listing.json'), JSON.stringify({ engine, width, scheme, url: URL, ...listing }, null, 1));
    console.log(`  ${engine} ${width}px ${scheme}: ${shown.length} shown of ${(listing.images || []).length}`);
  } catch (e) {
    fs.writeFileSync(path.join(dir, 'listing.json'), JSON.stringify({ engine, width, scheme, error: String(e) }));
    console.log(`  ${engine} ${width}px ${scheme}: FAILED ${e.message.split('\n')[0]}`);
  } finally {
    await ctx.close();
  }
}

for (const engine of (process.env.ENGINES ? process.env.ENGINES.split(',') : ENGINES)) {
  const browser = await pw[engine].launch({ headless: true });
  console.log(`${engine} ${browser.version()}`);
  try {
    for (const width of WIDTHS) for (const scheme of SCHEMES) await pass(browser, engine, width, scheme);
  } finally {
    await browser.close();
  }
}
