#!/usr/bin/env python3
"""Measure real rendered image widths on live profile pages with headless Chrome.

    python tools/survey/layout.py                 # every live profile, phone + desktop
    python tools/survey/layout.py --width 390     # phone only
    python tools/survey/layout.py --limit 5

The legibility formula assumes an image shrinks to fit the README column. That
holds outside tables, but inside an HTML table GitHub either squeezes cards to
share the row (640px cards measured at 76px) or keeps them full width and makes
the table scroll sideways. Only real layout answers which, so this loads each
page and reads every image's rendered box.

Writes docs/survey/data/layout.json.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cdp import browser  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "survey" / "data"

MEASURE_JS = r"""
(async () => {
  const art = document.querySelector('.js-profile-readme article.markdown-body')
           || document.querySelector('article.markdown-body');
  if (!art) return {error: document.title.includes('Too many') ? 'rate-limited' : 'no-readme'};
  const imgs = [...art.querySelectorAll('img')];
  await Promise.race([
    Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => {
      i.addEventListener('load', r, {once: true}); i.addEventListener('error', r, {once: true}); }))),
    new Promise(r => setTimeout(r, 12000))]);
  await new Promise(r => setTimeout(r, 300));
  return {
    container: Math.round(art.getBoundingClientRect().width),
    page_overflow: document.documentElement.scrollWidth > innerWidth + 1,
    images: imgs.map(i => { const b = i.getBoundingClientRect(); return {
      canonical: i.getAttribute('data-canonical-src') || i.currentSrc || i.src,
      w: Math.round(b.width * 10) / 10, nat: i.naturalWidth,
      in_table: !!i.closest('table'), loaded: i.complete && i.naturalWidth > 0}; }),
    tables: [...art.querySelectorAll('table')].map(t => ({
      client: t.clientWidth, scroll: t.scrollWidth, imgs: t.querySelectorAll('img').length})),
  };
})()
"""


async def measure(tab, user: str) -> dict:
    tab.drain()
    await tab.send("Page.navigate", {"url": f"https://github.com/{user}"})
    await tab.wait_event("Page.loadEventFired", 30)
    r = await tab.send("Runtime.evaluate", {"expression": MEASURE_JS, "awaitPromise": True,
                                            "returnByValue": True}, timeout=45)
    return r.get("result", {}).get("result", {}).get("value") or {"error": "no-result"}


async def run_width(users: list[str], width: int, workers: int) -> dict:
    queue: asyncio.Queue = asyncio.Queue()
    for u in users:
        queue.put_nowait(u)
    out: dict = {}

    async with browser() as new_tab:
        async def worker():
            tab = await new_tab()
            await tab.emulate(width, 9000)
            while True:
                try:
                    user = queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
                for attempt in range(3):
                    try:
                        res = await measure(tab, user)
                    except Exception as e:                # navigation/evaluate timeouts
                        res = {"error": type(e).__name__}
                    if res.get("error") != "rate-limited":
                        break
                    await asyncio.sleep(30 * (attempt + 1))   # back off politely
                out[user] = res
                if len(out) % 25 == 0 or len(out) == len(users):
                    print(f"  @{width}: {len(out)}/{len(users)}", flush=True)
                await asyncio.sleep(0.8)                  # ~1 page/s across workers
            tab.reader.cancel()

        await asyncio.gather(*(worker() for _ in range(workers)))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--width", type=int, action="append")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    widths = a.width or [390, 1280]
    profiles = json.loads((DATA / "profiles.json").read_text(encoding="utf-8"))
    users = [p["owner"] for p in profiles if p["status"] == "live"]
    if a.limit:
        users = users[: a.limit]
    path = DATA / "layout.json"
    for w in widths:
        print(f"measuring {len(users)} profiles at {w}px", flush=True)
        res = asyncio.run(run_width(users, w, a.workers))
        layout = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        for u, v in res.items():
            layout.setdefault(u, {})[str(w)] = v
        path.write_text(json.dumps(layout, separators=(",", ":"), sort_keys=True), encoding="utf-8")
        errs = sum("error" in v for v in res.values())
        print(f"  done @{w}: {len(res) - errs} measured, {errs} errors", flush=True)


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
