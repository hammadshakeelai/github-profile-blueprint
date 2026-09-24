// Probe the frontier fixtures in Chromium, Firefox and WebKit.
//
//   PLAYWRIGHT_CORE=... node tools/frontier/probe.mjs [local|github]
//
// local  — each fixture as an <img> from disk.
// github — the same fixtures as GitHub serves and renders them, via the
//          fixture gallery page (what a README visitor actually gets).
//
// Two questions per fixture, both answered by comparing screenshots (canvas
// read-back gives false negatives in Firefox — see docs/research/REDUCED-MOTION.md):
//   decodes?   the image has a natural size and isn't the broken-image box
//   animates?  two captures 900 ms apart differ
//   applied?   (lighting) the filtered file differs from its unfiltered control
import { createRequire } from 'module';
import { pathToFileURL } from 'url';
import fs from 'fs';
import path from 'path';

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const mode = process.argv[2] || 'local';
const dir = path.resolve('docs/frontier/fixtures');
const GH = 'https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/frontier/fixtures/';
const src = f => mode === 'github' ? GH + f : pathToFileURL(path.join(dir, f)).href;

const files = fs.readdirSync(dir).filter(f => !f.includes('-control')).sort();
const results = {};
for (const engine of ['chromium', 'firefox', 'webkit']) {
  const b = await pw[engine].launch({ headless: true });
  const p = await (await b.newContext({ viewport: { width: 420, height: 260 } })).newPage();
  // A page created with setContent is about:blank, which may not load file://
  // images at all — every fixture then "fails to decode" and the result is the
  // harness, not the format. So each probe navigates to a real page instead.
  const holder = path.resolve('.cache/frontier/holder.html');
  fs.mkdirSync(path.dirname(holder), { recursive: true });
  const shot = async f => {
    fs.writeFileSync(holder, `<body style="margin:0;background:#0d1117"><img id="i" src="${src(f)}"></body>`);
    await p.goto(pathToFileURL(holder).href + '?' + encodeURIComponent(f));
    await p.waitForFunction(() => document.getElementById('i').complete, null, { timeout: 20000 }).catch(() => {});
    await p.waitForTimeout(500);
    const ok = await p.evaluate(() => document.getElementById('i').naturalWidth > 0);
    const a = ok ? await p.locator('#i').screenshot() : null;
    await p.waitForTimeout(900);
    const c = ok ? await p.locator('#i').screenshot() : null;
    return { ok, a, c };
  };
  results[engine] = {};
  for (const f of files) {
    const r = await shot(f);
    const row = { decodes: r.ok, animates: r.ok ? Buffer.compare(r.a, r.c) !== 0 : null };
    if (f.startsWith('lighting-')) {
      const ctl = await shot(f.replace('.svg', '-control.svg'));
      row.applied = r.ok && ctl.ok ? Buffer.compare(r.a, ctl.a) !== 0 : null;
    }
    results[engine][f] = row;
  }
  await b.close();
  console.log(`${engine} done`);
}

// A compact table: one row per fixture, one column per engine.
const fmt = r => !r.decodes ? 'NO DECODE' :
  [r.applied === undefined ? '' : (r.applied ? 'lit' : 'NOT LIT'), r.animates ? 'moves' : 'still'].filter(Boolean).join(' · ');
console.log(`\n${'fixture'.padEnd(34)} ${'chromium'.padEnd(18)} ${'firefox'.padEnd(18)} webkit`);
for (const f of files) console.log(`${f.padEnd(34)} ${fmt(results.chromium[f]).padEnd(18)} ${fmt(results.firefox[f]).padEnd(18)} ${fmt(results.webkit[f])}`);
fs.mkdirSync('docs/frontier/data', { recursive: true });
fs.writeFileSync(`docs/frontier/data/probe-${mode}.json`, JSON.stringify(results, null, 1));
