#!/usr/bin/env python3
"""Tile profile screenshots into contact sheets for side-by-side review.

    python tools/survey/contact_sheet.py --width 390 --per-sheet 6 user1 user2 ...

Reads docs/survey/shots/<user>-<width>.jpg, crops away GitHub's own page chrome
where it can, labels each tile with the username, and writes
docs/survey/shots/sheets/sheet-<width>-<n>.jpg.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SHOTS = Path(__file__).resolve().parents[2] / "docs" / "survey" / "shots"

# Crop boxes (fraction of width, absolute px of height) that keep the README.
# Desktop shots are saved at 960px; the README column starts after the sidebar.
# Tuned to screenshot.py's emulated captures: on a phone the avatar, bio and
# achievements push the README down to roughly y=560.
CROP = {390: (0.0, 1.0, 560, 3400), 1280: (0.255, 0.985, 60, 2100)}
TILE_W = {390: 240, 1280: 420}


def tile(user: str, width: int) -> Image.Image | None:
    p = SHOTS / f"{user}-{width}.jpg"
    if not p.exists():
        return None
    img = Image.open(p).convert("RGB")
    x0, x1, y0, y1 = CROP[width]
    img = img.crop((int(img.width * x0), min(y0, img.height - 1),
                    int(img.width * x1), min(y1, img.height)))
    tw = TILE_W[width]
    img = img.resize((tw, round(img.height * tw / img.width)), Image.LANCZOS)
    canvas = Image.new("RGB", (tw, img.height + 22), (13, 17, 23))
    canvas.paste(img, (0, 22))
    d = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    d.text((4, 3), user, fill=(240, 246, 252), font=font)
    return canvas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("users", nargs="+")
    ap.add_argument("--width", type=int, default=390)
    ap.add_argument("--per-sheet", type=int, default=6)
    a = ap.parse_args()
    out = SHOTS / "sheets"
    out.mkdir(parents=True, exist_ok=True)
    tiles = [t for t in (tile(u, a.width) for u in a.users) if t]
    for n in range(0, len(tiles), a.per_sheet):
        group = tiles[n:n + a.per_sheet]
        h = max(t.height for t in group)
        sheet = Image.new("RGB", (sum(t.width for t in group) + 6 * (len(group) - 1), h), (48, 54, 61))
        x = 0
        for t in group:
            sheet.paste(t, (x, 0))
            x += t.width + 6
        path = out / f"sheet-{a.width}-{n // a.per_sheet + 1}.jpg"
        sheet.save(path, "JPEG", quality=80)
        print(path.name, sheet.size)


if __name__ == "__main__":
    main()
