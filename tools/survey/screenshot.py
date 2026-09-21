#!/usr/bin/env python3
"""Capture GitHub profile pages at phone and desktop width with headless Chrome.

    python tools/survey/screenshot.py user1 user2 ...
    python tools/survey/screenshot.py --scheme light user1

Writes docs/survey/shots/<user>-<width>[-light].jpg.

The phone capture uses true mobile emulation over the DevTools protocol (mobile
viewport semantics at 390px, giving GitHub's 309px README column) rather than a
narrowed desktop window — a narrow window keeps desktop layout rules and can
clip content at the right edge. Desktop captures are downscaled to keep the
repository light.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cdp import browser, chrome  # noqa: E402,F401  (chrome re-exported for callers)

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "survey" / "shots"
VIEWPORTS = {390: 3600, 1280: 2800}      # width -> captured height
DESKTOP_SAVE_W = 960

SETTLE_JS = r"""
(async () => {
  const imgs = [...document.querySelectorAll('article.markdown-body img')];
  await Promise.race([
    Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => {
      i.addEventListener('load', r, {once: true}); i.addEventListener('error', r, {once: true}); }))),
    new Promise(r => setTimeout(r, 12000))]);
  await new Promise(r => setTimeout(r, 2500));  // let client-side re-render finish and animations settle
  return imgs.length;
})()
"""


async def capture(new_tab, user: str, width: int, scheme: str, out_dir: Path | None = None) -> str:
    """`user` is a GitHub username, or name=URL to capture any page (e.g. a comp)."""
    name, url = (user.split("=", 1) if "=" in user else (user, f"https://github.com/{user}"))
    suffix = "" if scheme == "dark" else f"-{scheme}"
    out = (out_dir or SHOTS) / f"{name}-{width}{suffix}.jpg"
    tab = await new_tab()
    try:
        await tab.emulate(width, VIEWPORTS[width], scheme)
        tab.drain()
        await tab.send("Page.navigate", {"url": url})
        await tab.wait_event("Page.loadEventFired", 30)
        await tab.send("Runtime.evaluate", {"expression": SETTLE_JS, "awaitPromise": True}, timeout=45)
        shot = await tab.send("Page.captureScreenshot", {"format": "png"}, timeout=60)
        img = Image.open(io.BytesIO(base64.b64decode(shot["result"]["data"]))).convert("RGB")
        if width > 1000:
            img = img.resize((DESKTOP_SAVE_W, round(img.height * DESKTOP_SAVE_W / img.width)),
                             Image.LANCZOS)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, "JPEG", quality=72, optimize=True, progressive=True)
        return f"ok    {out.name}  {out.stat().st_size // 1024} KB"
    except Exception as e:
        return f"FAIL  {name} @{width} ({type(e).__name__})"
    finally:
        tab.reader.cancel()
        await tab.ws.close()


async def run(users: list[str], widths: list[int], scheme: str, workers: int,
              out_dir: Path | None = None) -> None:
    jobs = [(u, w) for u in users for w in widths]
    sem = asyncio.Semaphore(workers)
    async with browser() as new_tab:
        async def one(job):
            async with sem:
                line = await capture(new_tab, job[0], job[1], scheme, out_dir)
                print(line, flush=True)
        await asyncio.gather(*(one(j) for j in jobs))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("users", nargs="+")
    ap.add_argument("--scheme", choices=["dark", "light"], default="dark")
    ap.add_argument("--widths", default="390,1280")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--out", type=Path, default=None, help="directory for the JPEGs (default: docs/survey/shots)")
    a = ap.parse_args()
    asyncio.run(run(a.users, [int(w) for w in a.widths.split(",")], a.scheme, a.workers, a.out))


if __name__ == "__main__":
    main()
