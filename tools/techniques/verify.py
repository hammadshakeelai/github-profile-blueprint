#!/usr/bin/env python3
"""Verify the technique gallery on GitHub's real renderer.

    python tools/techniques/verify.py [--ref v2/research]

Loads docs/techniques/GALLERY.md as rendered on github.com, at desktop (1280px)
and phone (390px) width, in dark and light colour schemes, and for every image:

  * loaded      — did GitHub serve it and the browser decode it
  * animates    — two frames captured 1.2s apart differ, i.e. the animation runs
                  inside GitHub's page, not just when the file is opened alone
  * boundary    — for the test images, the answer read from the pixels (script
                  ran? external image loaded? web font loaded? foreignObject
                  rendered?)
  * theme       — which variant each switching mechanism showed

Writes docs/techniques/verified.json and rendered crops to
docs/techniques/rendered/. VERIFIED.md is written from the JSON.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import io
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "survey"))
from cdp import browser  # noqa: E402

OUT = ROOT / "docs" / "techniques"
REPO = "hammadshakeelai/github-profile-blueprint"

LIST_JS = r"""
(async () => {
  const art = document.querySelector('article.markdown-body');
  if (!art) return {error: 'no-article'};
  const imgs = [...art.querySelectorAll('img')];
  await Promise.race([
    Promise.all(imgs.map(i => i.complete ? 0 : new Promise(r => {
      i.addEventListener('load', r, {once: true}); i.addEventListener('error', r, {once: true}); }))),
    new Promise(r => setTimeout(r, 15000))]);
  await new Promise(r => setTimeout(r, 1500));
  const sx = window.scrollX, sy = window.scrollY;
  return {
    container: Math.round(art.getBoundingClientRect().width),
    images: imgs.map(i => { const b = i.getBoundingClientRect();
      const src = i.currentSrc || i.src;
      return { alt: i.alt, src,
        file: (src.match(/examples\/([\w-]+\.svg)/) || [])[1] || null,
        loaded: i.complete && i.naturalWidth > 0,
        x: b.left + sx, y: b.top + sy, w: b.width, h: b.height,
        shown: b.width > 0 && b.height > 0 && getComputedStyle(i).display !== 'none' }; }),
  };
})()
"""


async def clip(tab, im: dict) -> Image.Image:
    shot = await tab.send("Page.captureScreenshot", {
        "format": "png", "captureBeyondViewport": True,
        "clip": {"x": im["x"], "y": im["y"], "width": im["w"], "height": im["h"], "scale": 1}},
        timeout=60)
    return Image.open(io.BytesIO(base64.b64decode(shot["result"]["data"]))).convert("RGB")


def changed_fraction(a: Image.Image, b: Image.Image, level: int = 24) -> float:
    if a.size != b.size:
        return 1.0
    diff = ImageChops.difference(a, b).convert("L").point(lambda v: 255 if v > level else 0)
    return sum(diff.histogram()[255:]) / (a.width * a.height)


def px(img: Image.Image, fx: float, fy: float) -> tuple:
    """Pixel at a fractional position of the crop."""
    return img.getpixel((min(img.width - 1, int(img.width * fx)), min(img.height - 1, int(img.height * fy))))


def near(c: tuple, target: str, tol: int = 40) -> bool:
    t = tuple(int(target[i:i + 2], 16) for i in (1, 3, 5))
    return all(abs(a - b) <= tol for a, b in zip(c, t))


def bright_extent(img: Image.Image, y0: float, y1: float) -> float:
    """Horizontal span of bright pixels within a band, as a fraction of width."""
    g = img.convert("L")
    xs = [x for y in range(int(g.height * y0), int(g.height * y1))
          for x in range(g.width) if g.getpixel((x, y)) > 200]
    return (max(xs) - min(xs)) / g.width if xs else 0.0


def boundary(file: str, img: Image.Image) -> dict:
    if file == "test-script.svg":
        c = px(img, 0.03, 0.12)
        return {"script_ran": near(c, "#cf222e"), "panel_rgb": c}
    if file == "test-external-image.svg":
        # A blocked <image> is not invisible: Chrome paints its broken-image icon
        # (a page with a green hill and blue sky) over whatever is beneath. So
        # "not the placeholder colour" does not mean "loaded" — look for the icon.
        box = img.crop((int(img.width * 0.066), int(img.height * 0.19),
                        int(img.width * 0.233), int(img.height * 0.81)))
        pixels = list(box.getdata())
        green = sum(1 for r, g, b in pixels if g > 140 and r < 130 and b < 130) / len(pixels)
        placeholder = sum(1 for p in pixels if near(p, "#21262d", 16)) / len(pixels)
        if green > 0.03:
            verdict = "blocked — browser draws a broken-image icon"
        elif placeholder > 0.6:
            verdict = "blocked — nothing drawn"
        else:
            verdict = "loaded"
        return {"external_image": verdict, "green_share": round(green, 3),
                "placeholder_share": round(placeholder, 3)}
    if file == "test-external-font.svg":
        # "PIXEL FONT?" is ~11 wide blocky glyphs in Press Start 2P; far narrower in a fallback serif
        span = bright_extent(img, 0.36, 0.56)
        return {"web_font_loaded": span > 0.48, "title_span": round(span, 3)}
    if file == "test-foreign-object.svg":
        found = any(near(img.getpixel((x, y)), "#8957e5", 30)
                    for x in range(0, img.width, 3) for y in range(0, img.height, 3))
        return {"foreign_object_rendered": found}
    if file == "theme-aware.svg":
        c = px(img, 0.02, 0.5)
        return {"in_svg_scheme": "dark" if sum(c) < 150 else "light", "bg_rgb": c}
    return {}


FRAMES, FRAME_GAP = 8, 0.8     # ~6.4s of sampling covers every loop in the gallery


async def load(tab, url: str, width: int, scheme: str) -> dict:
    await tab.emulate(width, 9000, scheme)
    tab.drain()
    await tab.send("Page.navigate", {"url": url})
    await tab.wait_event("Page.loadEventFired", 40)
    r = await tab.send("Runtime.evaluate", {"expression": LIST_JS, "awaitPromise": True,
                                            "returnByValue": True}, timeout=60)
    return r["result"]["result"]["value"]


async def run_pass(new_tab, url: str, width: int, scheme: str, save: bool) -> list[dict]:
    tab = await new_tab()
    try:
        page = await load(tab, url, width, scheme)
        # A page that rendered nothing (interstitial, half-loaded) is a failed
        # load, not a result — retry rather than report every image as hidden.
        for _ in range(2):
            if "error" not in page and any(im["shown"] for im in page["images"]):
                break
            await asyncio.sleep(8)
            page = await load(tab, url, width, scheme)
        if "error" in page:
            return [{"error": page["error"]}]
        rows = []
        shown = [im for im in page["images"] if im["file"] and im["shown"]]
        # Animations with built-in holds (typing, gauges) can look static across
        # any single pair of frames, so sample a full cycle and take the maximum.
        frames: dict[str, list] = {im["file"]: [] for im in shown}
        for step in range(FRAMES):
            if step:
                await asyncio.sleep(FRAME_GAP)
            for im in shown:
                frames[im["file"]].append(await clip(tab, im))
        for im in page["images"]:
            if not im["file"]:
                continue
            row = {"file": im["file"], "width": width, "scheme": scheme, "loaded": im["loaded"],
                   "shown": im["shown"], "rendered_w": round(im["w"], 1), "container": page["container"]}
            if im["shown"]:
                fs = frames[im["file"]]
                a = fs[0]
                row["changed"] = round(max(changed_fraction(a, f) for f in fs[1:]), 4)
                row["animates"] = row["changed"] > 0.003
                row.update(boundary(im["file"], a))
                if save:
                    (OUT / "rendered").mkdir(parents=True, exist_ok=True)
                    a.save(OUT / "rendered" / f"{Path(im['file']).stem}-{width}-{scheme}.png", optimize=True)
            rows.append(row)
        return rows
    finally:
        tab.reader.cancel()
        await tab.ws.close()


PASSES = [(1280, "dark"), (1280, "light"), (390, "dark"), (390, "light")]
STATIC_BY_DESIGN = {"grain.svg", "theme-aware.svg", "theme-picture-dark.svg", "theme-picture-light.svg",
                    "theme-fragment-dark.svg", "theme-fragment-light.svg", "test-script.svg",
                    "test-external-image.svg", "test-external-font.svg", "test-foreign-object.svg"}


def write_report(data: dict) -> None:
    """VERIFIED.md, generated from verified.json so the page can't drift from the data."""
    by: dict[str, dict] = {}
    for r in data["results"]:
        if r.get("file"):
            by.setdefault(r["file"], {})[(r["width"], r["scheme"])] = r

    def cell(r):
        if r is None:
            return "—"
        if not r["shown"]:
            return "hidden"
        if not r["loaded"]:
            return "✗ failed"
        return "✓ moves" if r.get("animates") else "✓"

    lines = [
        "# Verified on GitHub",
        "",
        f"Generated by `tools/techniques/verify.py` from `verified.json` — do not edit by hand. "
        f"Source page: <{data['url']}>.",
        "",
        "Each example was loaded inside GitHub's rendered markdown in headless Chrome, at desktop "
        "(1280px) and phone (390px) width, in dark and light schemes. **✓** means GitHub served it "
        "and the browser drew it. **moves** means eight frames sampled 0.8s apart differed — the "
        "animation runs inside GitHub's page, not only when the file is opened alone. **hidden** is "
        "the correct outcome for a theme variant that shouldn't show in that scheme.",
        "",
        "## Techniques",
        "",
        "| Example | 1280 dark | 1280 light | 390 dark | 390 light | Verdict |",
        "|---|---|---|---|---|---|",
    ]
    for f in sorted(by):
        if f.startswith("test-") or f.startswith("theme-"):
            continue
        rs = [by[f].get(p) for p in PASSES]
        loads = all(r and r["loaded"] for r in rs)
        moves = any(r and r.get("animates") for r in rs)
        verdict = ("renders, static by design" if f in STATIC_BY_DESIGN else
                   "renders and animates" if loads and moves else
                   "renders, motion not caught" if loads else "does not render")
        lines.append(f"| [`{f}`](examples/{f}) | " + " | ".join(cell(r) for r in rs) + f" | {verdict} |")

    lines += ["", "## Theme switching", "",
              "| Mechanism | Dark scheme shows | Light scheme shows |", "|---|---|---|"]
    def shown_variant(prefix, scheme, width=1280):
        vis = [f for f in by if f.startswith(prefix) and (r := by[f].get((width, scheme))) and r["shown"]]
        return ", ".join(v.replace(prefix, "").replace(".svg", "") for v in vis) or "nothing"
    lines.append(f"| `<picture>` + `prefers-color-scheme` | {shown_variant('theme-picture-', 'dark')} | "
                 f"{shown_variant('theme-picture-', 'light')} |")
    lines.append(f"| `#gh-dark-mode-only` / `#gh-light-mode-only` | {shown_variant('theme-fragment-', 'dark')} | "
                 f"{shown_variant('theme-fragment-', 'light')} |")
    ta = {p: by.get("theme-aware.svg", {}).get(p, {}).get("in_svg_scheme") for p in PASSES}
    lines.append(f"| `@media (prefers-color-scheme)` inside the SVG | {ta[(1280, 'dark')]} | {ta[(1280, 'light')]} |")

    lines += ["", "## Boundary tests", "", "| Test | Result, every pass |", "|---|---|"]
    def uniform(file, key, fmt):
        vals = {by[file][p].get(key) for p in PASSES if by.get(file, {}).get(p, {}).get("shown")}
        return fmt(vals.pop()) if len(vals) == 1 else f"inconsistent: {sorted(map(str, vals))}"
    lines.append("| `<script>` inside the SVG | " +
                 uniform("test-script.svg", "script_ran", lambda v: "ran" if v else "**blocked** — never runs") + " |")
    lines.append("| External `<image href=\"https://…\">` | " +
                 uniform("test-external-image.svg", "external_image", lambda v: f"**{v}**") + " |")
    lines.append("| `@import` of a web font | " +
                 uniform("test-external-font.svg", "web_font_loaded",
                         lambda v: "loaded" if v else "**blocked** — falls back to the next font") + " |")
    lines.append("| HTML inside `<foreignObject>` | " +
                 uniform("test-foreign-object.svg", "foreign_object_rendered",
                         lambda v: "**renders** (in Chrome)" if v else "not rendered") + " |")
    (OUT / "VERIFIED.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


async def main_async(ref: str) -> None:
    url = f"https://github.com/{REPO}/blob/{ref}/docs/techniques/GALLERY.md"
    results = []
    async with browser() as new_tab:
        for width in (1280, 390):
            for scheme in ("dark", "light"):
                rows = await run_pass(new_tab, url, width, scheme, save=(scheme == "dark"))
                print(f"  {width}px {scheme}: {len(rows)} images", flush=True)
                results += rows
    data = {"url": url, "results": results}
    (OUT / "verified.json").write_text(json.dumps(data, indent=1), encoding="utf-8")
    write_report(data)
    print(f"wrote {OUT / 'verified.json'} and VERIFIED.md")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="v2/research")
    ap.add_argument("--report-only", action="store_true", help="rebuild VERIFIED.md from verified.json")
    a = ap.parse_args()
    if a.report_only:
        write_report(json.loads((OUT / "verified.json").read_text(encoding="utf-8")))
        print("wrote VERIFIED.md")
        return
    asyncio.run(main_async(a.ref))


if __name__ == "__main__":
    main()
