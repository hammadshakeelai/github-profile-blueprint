// Render every design in docs/book/designs/ onto one contact sheet, per theme.
//
//   PLAYWRIGHT_CORE=/path/to/playwright-core node tools/book/render.mjs [dark|light] [engine]
//
// A quick local look before publishing; GitHub's own render is checked separately.
import { createRequire } from 'module';
import { pathToFileURL } from 'url';
import fs from 'fs';
import path from 'path';

const require = createRequire(import.meta.url);
const pw = require(process.env.PLAYWRIGHT_CORE || 'playwright-core');
const theme = process.argv[2] || 'dark';
const engine = process.argv[3] || 'chromium';
const dir = path.resolve('docs/book/designs');
const files = fs.readdirSync(dir).filter(f => f.endsWith(`-${theme}.svg`)).sort();
const bg = theme === 'dark' ? '#0d1117' : '#ffffff';
const html = `<body style="margin:0;background:${bg};display:grid;grid-template-columns:repeat(3,600px);gap:14px;padding:14px">`
  + files.map(f => `<img src="${pathToFileURL(path.join(dir, f)).href}" width="600">`).join('') + '</body>';
const page = path.resolve('.cache/book/designs.html');
fs.mkdirSync(path.dirname(page), { recursive: true });
fs.writeFileSync(page, html);
const browser = await pw[engine].launch({ headless: true });
const tab = await (await browser.newContext({ viewport: { width: 1860, height: 1200 } })).newPage();
await tab.goto(pathToFileURL(page).href);
await tab.waitForTimeout(2000);
const out = `.cache/book/designs-${theme}-${engine}.png`;
await tab.screenshot({ path: out, fullPage: true });
console.log(out, files.length);
await browser.close();
