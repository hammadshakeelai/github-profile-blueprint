// Do feTurbulence and feDisplacementMap actually do anything inside an SVG
// referenced as an image, in each engine?
//
//   PLAYWRIGHT_CORE=/path/to/playwright-core node tools/book/filters.mjs
//
// For each filter, render the same small SVG as an <img> twice — once with the
// filter applied, once without — and compare screenshots. Identical pixels mean
// the engine ignored the filter. The same method answered the reduced-motion
// question (docs/research/REDUCED-MOTION.md); a canvas read-back was rejected
// there because Firefox blocks it and reports false negatives.
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');

const scene = (filter, apply) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 120" width="200" height="120">
<defs>${filter}</defs>
<rect width="200" height="120" fill="#101018"/>
<g ${apply ? 'filter="url(#f)"' : ''}>
  <circle cx="60" cy="60" r="40" fill="#f97316"/><circle cx="140" cy="60" r="40" fill="#06b6d4"/>
  <rect x="20" y="95" width="160" height="10" fill="#fff"/>
</g></svg>`;

const FILTERS = {
  feTurbulence: '<filter id="f"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2"/>'
              + '<feComposite in2="SourceGraphic" operator="in"/></filter>',
  feDisplacementMap: '<filter id="f"><feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="3" result="n"/>'
                   + '<feDisplacementMap in="SourceGraphic" in2="n" scale="30" xChannelSelector="R" yChannelSelector="G"/></filter>',
  feGaussianBlur: '<filter id="f"><feGaussianBlur stdDeviation="6"/></filter>',   // control: known to work
};

const uri = s => 'data:image/svg+xml;utf8,' + encodeURIComponent(s);
for (const engine of ['chromium', 'firefox', 'webkit']) {
  const b = await pw[engine].launch({ headless: true });
  const p = await (await b.newContext({ viewport: { width: 300, height: 200 } })).newPage();
  const row = [];
  for (const [name, f] of Object.entries(FILTERS)) {
    const shots = [];
    for (const apply of [true, false]) {
      await p.setContent(`<body style="margin:0"><img id="i" src="${uri(scene(f, apply))}"></body>`);
      await p.waitForTimeout(400);
      shots.push(await p.locator('#i').screenshot());
    }
    row.push(`${name}: ${Buffer.compare(shots[0], shots[1]) !== 0 ? 'APPLIED' : 'ignored'}`);
  }
  console.log(engine.padEnd(9), row.join('   '));
  await b.close();
}
