#!/usr/bin/env python3
"""Full-page capture of any GitHub page, for checking how something renders.

    python tools/book/shot.py URL OUT.jpg [--width 1280] [--height 6000]
                              [--scheme dark|light] [--save-width 900]

Waits for images and GitHub's rendered viewers (Mermaid, STL, GeoJSON iframes)
to settle before capturing. Output is for inspection; it lives under .cache/.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "survey"))
from cdp import browser  # noqa: E402

SETTLE = r"""
(async () => {
  const imgs = [...document.querySelectorAll('article.markdown-body img')];
  await Promise.race([
    Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => { i.onload = r; i.onerror = r; }))),
    new Promise(r => setTimeout(r, 15000))]);
  await new Promise(r => setTimeout(r, 7000));   // viewers render inside iframes, later
  return imgs.length;
})()
"""


async def capture(url: str, out: Path, width: int, height: int, scheme: str, save_w: int) -> None:
    async with browser() as new_tab:
        t = await new_tab()
        await t.emulate(width, height, scheme)
        t.drain()
        await t.send("Page.navigate", {"url": url})
        await t.wait_event("Page.loadEventFired", 40)
        await t.send("Runtime.evaluate", {"expression": SETTLE, "awaitPromise": True}, timeout=60)
        shot = await t.send("Page.captureScreenshot", {"format": "png"}, timeout=90)
        img = Image.open(io.BytesIO(base64.b64decode(shot["result"]["data"]))).convert("RGB")
        if save_w and img.width > save_w:
            img = img.resize((save_w, round(img.height * save_w / img.width)), Image.LANCZOS)
        out.parent.mkdir(parents=True, exist_ok=True)
        img.save(out, "JPEG", quality=80)
        print(out, img.size)
        await t.ws.close()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("out", type=Path)
    ap.add_argument("--width", type=int, default=1280)
    ap.add_argument("--height", type=int, default=6000)
    ap.add_argument("--scheme", choices=["dark", "light"], default="dark")
    ap.add_argument("--save-width", type=int, default=900)
    a = ap.parse_args()
    asyncio.run(capture(a.url, a.out, a.width, a.height, a.scheme, a.save_width))


if __name__ == "__main__":
    main()
