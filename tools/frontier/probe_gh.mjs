// Probe the fixture gallery as github.com renders it, in three engines.
//
//   PLAYWRIGHT_CORE=... node tools/frontier/probe_gh.mjs
//
// Loads docs/frontier/GALLERY.md on github.com, finds each fixture's <img>, and
// for each one records: decoded (natural size), animates (two captures 900 ms
// apart differ), and — for lighting fixtures — lit (differs from its control).
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const URL = 'https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/frontier/GALLERY.md';
const out = {};
for (const engine of ['chromium', 'firefox', 'webkit']) {
  const b = await pw[engine].launch({ headless: true });
  const p = await (await b.newContext({ viewport: { width: 1280, height: 9000 },
                                        reducedMotion: process.env.REDUCED || 'no-preference' })).newPage();
  await p.goto(URL, { waitUntil: 'load', timeout: 90000 });
  await p.waitForTimeout(6000);                      // GitHub re-renders markdown client-side
  // GitHub wraps some animated images in an <animated-image> player that adds a
  // hidden duplicate <img> with the same alt; keep only the visible copy, and
  // record which fixtures got wrapped.
  const imgs = await p.$$eval('article.markdown-body img', els => els.map((e, i) => {
    const r = e.getBoundingClientRect();
    return { i, alt: e.alt, ok: e.naturalWidth > 0, x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height,
             wrapped: !!e.closest('animated-image') };
  }).filter(e => e.w > 0));
  const shoot = im => p.screenshot({ clip: { x: im.x, y: im.y, width: Math.max(1, im.w), height: Math.max(1, im.h) } });
  const first = {};
  for (const im of imgs) if (im.ok && im.w > 0) first[im.alt] = await shoot(im);
  await p.waitForTimeout(900);
  out[engine] = {};
  for (const im of imgs) {
    const r = { decodes: im.ok && im.w > 0, wrapped: im.wrapped };
    if (r.decodes) r.animates = Buffer.compare(first[im.alt], await shoot(im)) !== 0;
    out[engine][im.alt] = r;
  }
  for (const [alt, r] of Object.entries(out[engine])) {
    if (alt.startsWith('lighting-') && !alt.includes('-control') && r.decodes) {
      const ctl = alt.replace('.svg', '-control.svg');
      r.lit = first[ctl] ? Buffer.compare(first[alt], first[ctl]) !== 0 : null;
    }
  }
  await b.close();
  console.log(`${engine}: ${imgs.length} images`);
}
const fmt = r => !r ? '—' : !r.decodes ? 'NO DECODE' : [r.lit === undefined ? '' : (r.lit ? 'lit' : 'NOT LIT'), r.animates ? 'moves' : 'still', r.wrapped ? 'PLAYER' : ''].filter(Boolean).join(' · ');
const names = Object.keys(out.chromium).filter(n => !n.includes('-control'));
console.log(`\n${'fixture (on github.com)'.padEnd(34)} ${'chromium'.padEnd(16)} ${'firefox'.padEnd(16)} webkit`);
for (const n of names) console.log(`${n.padEnd(34)} ${fmt(out.chromium[n]).padEnd(16)} ${fmt(out.firefox[n]).padEnd(16)} ${fmt(out.webkit[n])}`);
fs.writeFileSync(`docs/frontier/data/probe-github-${process.env.REDUCED || 'motion'}.json`, JSON.stringify(out, null, 1));
