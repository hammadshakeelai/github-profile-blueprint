#!/usr/bin/env python3
"""Photograph profile READMEs so the best-looking ones can be chosen by eye.

    python tools/book/look.py user1 user2 ...        # or --file names.txt
    python tools/book/look.py --sheet                # tile the captures

Captures the README area of each profile at 1280px, dark scheme, and tiles the
results into contact sheets. Captures stay in .cache/book/ (gitignored): they
are for judging, not for publishing — the book links to people's work and
embeds their own asset URLs rather than redistributing screenshots of it.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import io
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "survey"))
from cdp import browser  # noqa: E402

CACHE = ROOT / ".cache" / "book" / "looks"
SHEETS = ROOT / ".cache" / "book" / "sheets"
THUMB_W, THUMB_H = 420, 700

SETTLE = r"""
(async () => {
  const art = document.querySelector('.js-profile-readme article, article.markdown-body');
  if (!art) return null;
  const imgs = [...art.querySelectorAll('img')];
  await Promise.race([Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => {
      i.onload = r; i.onerror = r; }))), new Promise(r => setTimeout(r, 12000))]);
  await new Promise(r => setTimeout(r, 2500));
  const b = (document.querySelector('.js-profile-readme article, article.markdown-body'))
              .getBoundingClientRect();
  return JSON.stringify({x: b.left + scrollX, y: b.top + scrollY, w: b.width, h: b.height});
})()
"""


async def shoot(new_tab, user: str, sem: asyncio.Semaphore) -> str:
    out = CACHE / f"{user}.jpg"
    if out.exists():
        return f"cached {user}"
    async with sem:
        t = await new_tab()
        try:
            await t.emulate(1280, 2600, "dark")
            t.drain()
            await t.send("Page.navigate", {"url": f"https://github.com/{user}"})
            await t.wait_event("Page.loadEventFired", 40)
            r = await t.send("Runtime.evaluate", {"expression": SETTLE, "awaitPromise": True},
                             timeout=45)
            val = r["result"]["result"].get("value")
            if not val:
                return f"no-readme {user}"
            import json
            box = json.loads(val)
            clip = {"x": box["x"], "y": box["y"], "width": box["w"],
                    "height": min(box["h"], 2400), "scale": 1}
            shot = await t.send("Page.captureScreenshot",
                                {"format": "png", "clip": clip, "captureBeyondViewport": True},
                                timeout=60)
            img = Image.open(io.BytesIO(base64.b64decode(shot["result"]["data"]))).convert("RGB")
            CACHE.mkdir(parents=True, exist_ok=True)
            img.save(out, "JPEG", quality=78)
            return f"ok {user} {img.size}"
        except Exception as e:
            return f"fail {user} {type(e).__name__}"
        finally:
            t.reader.cancel()
            await t.ws.close()


async def run(users: list[str]) -> None:
    sem = asyncio.Semaphore(3)
    async with browser() as new_tab:
        for line in await asyncio.gather(*(shoot(new_tab, u, sem) for u in users)):
            print(line, flush=True)


def sheet(per: int = 8) -> None:
    files = sorted(CACHE.glob("*.jpg"))
    SHEETS.mkdir(parents=True, exist_ok=True)
    for n in range(0, len(files), per):
        batch = files[n:n + per]
        cols = 4
        rows = (len(batch) + cols - 1) // cols
        canvas = Image.new("RGB", (cols * THUMB_W, rows * (THUMB_H + 28)), "#0d1117")
        d = ImageDraw.Draw(canvas)
        for i, f in enumerate(batch):
            im = Image.open(f)
            im = im.resize((THUMB_W, round(im.height * THUMB_W / im.width)))
            im = im.crop((0, 0, THUMB_W, min(im.height, THUMB_H)))
            x, y = (i % cols) * THUMB_W, (i // cols) * (THUMB_H + 28)
            canvas.paste(im, (x, y + 28))
            d.text((x + 8, y + 6), f.stem, fill="#e6edf3")
        path = SHEETS / f"sheet-{n // per + 1:02d}.jpg"
        canvas.save(path, "JPEG", quality=80)
        print(path.relative_to(ROOT), [f.stem for f in batch])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("users", nargs="*")
    ap.add_argument("--file", type=Path)
    ap.add_argument("--sheet", action="store_true")
    a = ap.parse_args()
    users = list(a.users)
    if a.file:
        users += [u.strip() for u in a.file.read_text(encoding="utf-8").split() if u.strip()]
    if users:
        asyncio.run(run(users))
    if a.sheet:
        sheet()


if __name__ == "__main__":
    main()
