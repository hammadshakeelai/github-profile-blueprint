#!/usr/bin/env python3
"""Capture GitHub profile pages at phone and desktop width with headless Chrome.

    python tools/survey/screenshot.py user1 user2 ...
    python tools/survey/screenshot.py --scheme light user1

Writes docs/survey/shots/<user>-<width>[-light].jpg. 390px wide renders GitHub's
mobile layout (309px README container); 1280px renders the desktop layout.

Each capture uses its own throwaway browser profile, so captures can run in
parallel without fighting over a profile lock.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
SHOTS = ROOT / "docs" / "survey" / "shots"
CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]
VIEWPORTS = {390: 3600, 1280: 2800}      # width -> captured height
DESKTOP_SAVE_W = 960                      # downscale desktop shots to keep the repo light


def chrome() -> str:
    for c in CHROME_CANDIDATES:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome not found; set CHROME=/path/to/chrome")


def capture(user: str, width: int, scheme: str) -> str:
    height = VIEWPORTS[width]
    suffix = "" if scheme == "dark" else f"-{scheme}"
    out = SHOTS / f"{user}-{width}{suffix}.jpg"
    tmp = Path(tempfile.mkdtemp(prefix="shot-"))
    png = tmp / "shot.png"
    # Blink's PreferredColorScheme: 0 = dark, 1 = light.
    pref = 0 if scheme == "dark" else 1
    cmd = [chrome(), "--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu",
           "--hide-scrollbars", "--no-first-run", "--mute-audio",
           f"--user-data-dir={tmp / 'profile'}", f"--window-size={width},{height}",
           f"--blink-settings=preferredColorScheme={pref}",
           f"--screenshot={png}", f"https://github.com/{user}"]
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
        if not png.exists() or png.stat().st_size == 0:
            return f"FAIL  {user} @{width}"
        img = Image.open(png).convert("RGB")
        if width > 1000:
            img = img.resize((DESKTOP_SAVE_W, round(img.height * DESKTOP_SAVE_W / img.width)),
                             Image.LANCZOS)
        SHOTS.mkdir(parents=True, exist_ok=True)
        img.save(out, "JPEG", quality=72, optimize=True, progressive=True)
        return f"ok    {out.name}  {out.stat().st_size // 1024} KB"
    except subprocess.TimeoutExpired:
        return f"FAIL  {user} @{width} (timeout)"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("users", nargs="+")
    ap.add_argument("--scheme", choices=["dark", "light"], default="dark")
    ap.add_argument("--widths", default="390,1280")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    widths = [int(w) for w in a.widths.split(",")]
    jobs = [(u, w) for u in a.users for w in widths]
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for line in ex.map(lambda j: capture(j[0], j[1], a.scheme), jobs):
            print(line, flush=True)


if __name__ == "__main__":
    main()
