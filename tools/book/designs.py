#!/usr/bin/env python3
"""Chapter 5: current design trends, built as README-safe SVGs.

    python tools/book/designs.py

Writes docs/book/designs/<name>-{dark,light}.svg. Every piece obeys the rules
this repository measured:

  * 600-unit canvas, so text >= 21.4 units clears 11px in a 309px phone column
    (enforced by `t()` below, which refuses to draw smaller);
  * the first frame is the finished composition — motion only adds;
  * no gradientTransform animation (WebKit never animates it);
  * no scripts, external images or web fonts; dark and light files.

Names and numbers come from the book's own data: docs/showcase/data/summary.json.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "book" / "designs"
W = 600
FLOOR = 11 * W / 309                     # 21.36 units
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
CONDENSED = "'Arial Narrow', 'Roboto Condensed', 'Helvetica Neue', Arial, sans-serif"

NAME = "Hammad Shakeel"
SUMMARY = json.loads((ROOT / "docs" / "showcase" / "data" / "summary.json").read_text(encoding="utf-8"))


# Average advance per character, as a fraction of font size. Deliberately
# generous: the real face varies per viewer, so a line must fit the widest
# plausible fallback, not the one on this machine.
ADVANCE = {MONO: 0.62, CONDENSED: 0.50, SANS: 0.56, SERIF: 0.55}


def t(x, y, s, size, fill, weight=400, family=SANS, anchor="start", extra="") -> str:
    if size < FLOOR:
        raise SystemExit(f"{s!r} at {size} units is below the {FLOOR:.1f}-unit phone floor")
    width = len(s) * size * ADVANCE.get(family, 0.56) * (1.06 if weight >= 700 else 1)
    left = x - (width / 2 if anchor == "middle" else width if anchor == "end" else 0)
    if left < 0 or left + width > W:
        raise SystemExit(f"{s!r} would run off the canvas: spans {left:.0f}..{left + width:.0f} of {W}")
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight != 400 else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}"{w} fill="{fill}"'
            f'{a}{extra}>{escape(s)}</text>')


def svg(h: int, body: str, label: str, defs: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'role="img" aria-label="{escape(label, {chr(34): "&quot;"})}"><title>{escape(label)}</title>'
            f'<defs>{defs}</defs>{body}</svg>\n')


def pair(name: str, make) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for theme in ("dark", "light"):
        (OUT / f"{name}-{theme}.svg").write_text(make(theme == "dark"), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1 · Aurora — drifting blurred light, with film grain over the top
# --------------------------------------------------------------------------- #
def aurora(dark: bool) -> str:
    h = 240
    bg = "#07080f" if dark else "#f7f5ff"
    ink = "#f4f2ff" if dark else "#141026"
    sub = "#b9b3d9" if dark else "#4b4570"
    blobs = [("#7c3aed", 140, 80, 150, 22), ("#06b6d4", 420, 120, 170, 27),
             ("#f43f5e", 300, 30, 120, 19), ("#22c55e", 520, 210, 110, 31)]
    # Each blob drifts on its own period; the blur turns circles into light.
    body = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{0.55 if dark else 0.35}">'
        f'<animate attributeName="cx" values="{x};{x + 60};{x - 40};{x}" dur="{d}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{y};{y + 30};{y - 20};{y}" dur="{d * 1.3:.0f}s" repeatCount="indefinite"/>'
        f'</circle>' for c, x, y, r, d in blobs)
    defs = ('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="46"/></filter>'
            '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/>'
            '<feColorMatrix values="0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0 0.5  0 0 0 0.09 0"/></filter>'
            f'<clipPath id="card"><rect width="{W}" height="{h}" rx="22"/></clipPath>')
    return svg(h, f'<g clip-path="url(#card)"><rect width="{W}" height="{h}" fill="{bg}"/>'
               f'<g filter="url(#soft)">{body}</g>'
               f'<rect width="{W}" height="{h}" filter="url(#grain)"/></g>'
               + t(40, 120, NAME, 58, ink, 800)
               + t(42, 168, "things that run in a browser tab", 24, sub)
               + t(42, 206, f"{SUMMARY['repos']} repositories · {SUMMARY['pages_sites']} live", 22, sub, family=MONO),
               f"{NAME}: aurora light drifting behind the name, with film grain", defs)


# --------------------------------------------------------------------------- #
# 2 · Liquid glass — a refracting pane over colour
# --------------------------------------------------------------------------- #
def liquid_glass(dark: bool) -> str:
    h = 260
    bg = "#0b0d14" if dark else "#eef1f8"
    ink = "#ffffff" if dark else "#0e1220"
    sub = "rgba(255,255,255,.78)" if dark else "rgba(14,18,32,.72)"
    backdrop = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"><animate attributeName="cx" '
        f'values="{x};{x + dx};{x}" dur="{d}s" repeatCount="indefinite"/></circle>'
        for x, y, r, c, dx, d in [(110, 70, 90, "#f97316", 80, 13), (300, 210, 110, "#8b5cf6", -70, 17),
                                  (500, 80, 95, "#06b6d4", -90, 15), (560, 230, 70, "#ec4899", -50, 11)])
    # feTurbulence noise drives feDisplacementMap: the pane bends what's behind it.
    defs = ('<filter id="refract" x="-10%" y="-10%" width="120%" height="120%">'
            '<feTurbulence type="fractalNoise" baseFrequency="0.012 0.02" numOctaves="2" seed="7" result="n"/>'
            '<feDisplacementMap in="SourceGraphic" in2="n" scale="38" xChannelSelector="R" yChannelSelector="G" result="d"/>'
            '<feGaussianBlur in="d" stdDeviation="7"/></filter>'
            '<clipPath id="pane"><rect x="44" y="40" width="512" height="180" rx="36"/></clipPath>'
            f'<clipPath id="cardclip"><rect width="{W}" height="{h}" rx="22"/></clipPath>'
            '<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#fff" stop-opacity=".9"/><stop offset=".35" stop-color="#fff" stop-opacity=".12"/>'
            '<stop offset=".7" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity=".55"/></linearGradient>')
    return svg(h,
               f'<g clip-path="url(#cardclip)"><rect width="{W}" height="{h}" fill="{bg}"/>'
               f'<g opacity="{0.9 if dark else 0.75}">{backdrop}</g></g>'
               f'<g clip-path="url(#pane)"><g filter="url(#refract)">{backdrop}</g>'
               f'<rect x="44" y="40" width="512" height="180" fill="{"#ffffff" if not dark else "#ffffff"}" opacity="{0.10 if dark else 0.45}"/></g>'
               f'<rect x="44.5" y="40.5" width="511" height="179" rx="35.5" fill="none" stroke="url(#rim)" stroke-width="1.6"/>'
               + t(84, 118, NAME, 46, ink, 700)
               + t(86, 162, "software · research · things in a tab", 23, sub)
               + t(86, 196, "refraction: feDisplacementMap", 22, sub, family=MONO),
               f"{NAME} on a pane of liquid glass that refracts moving colour behind it", defs)


# --------------------------------------------------------------------------- #
# 3 · Bento — modular tiles in one image, so a phone can't break the grid
# --------------------------------------------------------------------------- #
def bento(dark: bool) -> str:
    h = 420
    bg = "#0d1117" if dark else "#ffffff"
    tile = "#161b22" if dark else "#f4f6f8"
    line = "#30363d" if dark else "#d8dee4"
    ink = "#e6edf3" if dark else "#1f2328"
    mut = "#8b949e" if dark else "#59636e"
    acc = ["#58a6ff", "#f778ba", "#3fb950", "#d29922"] if dark else ["#0969da", "#bf3989", "#1a7f37", "#9a6700"]
    langs = SUMMARY["languages"][:4]
    total = sum(n for _, n in langs)
    bars = ""
    x = 330
    for i, (lang, n) in enumerate(langs):
        w = 238 * n / total
        bars += f'<rect x="{x:.1f}" y="92" width="{w:.1f}" height="14" fill="{acc[i]}"/>'
        x += w
    tiles = [
        (12, 12, 300, 200, t(36, 76, NAME.split()[0], 44, ink, 800) + t(36, 120, NAME.split()[1], 44, ink, 800)
         + t(36, 176, "builds things", 22, mut) + t(36, 202, "that run in a tab", 22, mut)),
        (324, 12, 264, 110, t(344, 52, "Top languages", 22, mut) + bars
         + t(344, 84, f"{langs[0][0]}", 22, ink, 700)),
        (324, 134, 128, 78, t(344, 176, str(SUMMARY["repos"]), 32, acc[0], 800) + t(344, 202, "repos", 22, mut)),
        (460, 134, 128, 78, t(480, 176, str(SUMMARY["pages_sites"]), 32, acc[2], 800) + t(480, 202, "live", 22, mut)),
        (12, 224, 188, 184, t(32, 268, "Now", 22, mut) + t(32, 304, "building a", 24, ink)
         + t(32, 334, "profile", 24, ink) + t(32, 364, "research", 24, ink) + t(32, 394, "book", 24, ink)),
        (212, 224, 376, 184, t(234, 268, "Latest", 22, mut)
         + "".join(t(234, 304 + i * 32, r["name"] if len(r["name"]) <= 24 else r["name"][:23] + "…", 23, ink)
                   for i, r in enumerate(SUMMARY["newest"][:3]))),
    ]
    body = f'<rect width="{W}" height="{h}" rx="22" fill="{bg}"/>' + "".join(
        f'<rect x="{x}" y="{y}" width="{w}" height="{hh}" rx="18" fill="{tile}" stroke="{line}"/>{inner}'
        for x, y, w, hh, inner in tiles)
    # One pulse: the "Now" tile's dot. Everything else is still.
    body += (f'<circle cx="{180}" cy="{262}" r="6" fill="{acc[2]}"><animate attributeName="opacity" '
             f'values="1;.25;1" dur="2.4s" repeatCount="indefinite"/></circle>')
    return svg(h, body, f"A bento grid: {NAME}, top languages, {SUMMARY['repos']} repositories, "
                        f"{SUMMARY['pages_sites']} live sites, what's being built now, latest repositories")


# --------------------------------------------------------------------------- #
# 4 · Neo-brutalism — hard shadows, thick outlines, flat loud colour
# --------------------------------------------------------------------------- #
def brutal(dark: bool) -> str:
    h = 250
    bg = "#1a1a1a" if dark else "#fff7e8"
    ink = "#111111"
    edge = "#f5f5f5" if dark else "#111111"
    card = "#ffde59"
    body = (f'<rect width="{W}" height="{h}" fill="{bg}"/>'
            f'<rect x="42" y="42" width="510" height="150" fill="{edge}"/>'           # hard shadow
            f'<rect x="30" y="30" width="510" height="150" fill="{card}" stroke="{ink}" stroke-width="5">'
            f'<animate attributeName="x" values="30;36;30" dur="2.2s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="30;36;30" dur="2.2s" repeatCount="indefinite"/></rect>'
            + t(58, 96, NAME.upper(), 44, ink, 900, CONDENSED)
            + t(60, 140, "SHIPS THINGS THAT RUN IN A TAB", 24, ink, 700, CONDENSED)
            + f'<rect x="30" y="200" width="150" height="38" fill="#ff5c8a" stroke="{edge}" stroke-width="4"/>'
            + t(48, 227, "LINUX", 23, ink, 800, CONDENSED)
            + f'<rect x="192" y="200" width="150" height="38" fill="#7dd3fc" stroke="{edge}" stroke-width="4"/>'
            + t(210, 227, "GAMES", 23, ink, 800, CONDENSED)
            + f'<rect x="354" y="200" width="186" height="38" fill="#86efac" stroke="{edge}" stroke-width="4"/>'
            + t(372, 227, "RETRIEVAL", 23, ink, 800, CONDENSED))
    return svg(h, body, f"{NAME.upper()} in neo-brutalist style: a yellow card with a hard black shadow "
                        "and three flat tags — Linux, games, retrieval")


# --------------------------------------------------------------------------- #
# 5 · Kinetic type — letters breathe in weight, one after another
# --------------------------------------------------------------------------- #
def kinetic(dark: bool) -> str:
    h = 200
    bg = "#0b0b0f" if dark else "#fafafa"
    ink = "#f5f5f5" if dark else "#101014"
    acc = "#a78bfa" if dark else "#6d28d9"
    word = "SHAKEEL"
    # One <text> with a <tspan> per letter keeps the font's own spacing; each
    # tspan animates its stroke, which reads as a weight axis swelling in turn.
    spans = "".join(
        f'<tspan stroke="{ink}" stroke-width="0" stroke-linejoin="round">{ch}'
        f'<animate attributeName="stroke-width" values="0;7;0" dur="2.8s" begin="{i * 0.18:.2f}s" '
        f'repeatCount="indefinite"/></tspan>' for i, ch in enumerate(word))
    letters = (f'<text x="{W / 2}" y="130" text-anchor="middle" font-family="{SANS}" font-size="96" '
               f'font-weight="800" fill="{ink}" letter-spacing="2">{spans}</text>')
    body = (f'<rect width="{W}" height="{h}" rx="22" fill="{bg}"/>' + letters
            + f'<rect x="46" y="150" width="508" height="5" fill="{acc}"><animate attributeName="width" '
              f'values="508;120;508" dur="5.6s" repeatCount="indefinite"/></rect>'
            + t(46, 184, "kinetic type · weight wave", 22, acc, family=MONO))
    return svg(h, body, "The name SHAKEEL in heavy capitals, each letter swelling in weight in turn")


# --------------------------------------------------------------------------- #
# 6 · Holographic chrome — a metallic wordmark with a sweeping highlight
# --------------------------------------------------------------------------- #
def chrome(dark: bool) -> str:
    h = 200
    bg = "#07070a" if dark else "#e9e9ef"
    stops = ["#ffffff", "#b8c6ff", "#ff9ee8", "#9ef6ff", "#fff3b0", "#ffffff"] if dark else \
            ["#3a3a55", "#5b6bd6", "#c2419b", "#1ea5b8", "#b7862a", "#3a3a55"]
    grad = "".join(f'<stop offset="{i / (len(stops) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(stops))
    defs = (f'<linearGradient id="holo" x1="0" y1="0" x2="1" y2="0">'
            # Animating x1/x2, never gradientTransform — WebKit ignores the latter.
            f'<animate attributeName="x1" values="-0.4;0.4;-0.4" dur="7s" repeatCount="indefinite"/>'
            f'<animate attributeName="x2" values="0.6;1.4;0.6" dur="7s" repeatCount="indefinite"/>{grad}</linearGradient>'
            '<linearGradient id="spec" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".7"/>'
            '<stop offset=".5" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    body = (f'<rect width="{W}" height="{h}" rx="22" fill="{bg}"/>'
            + t(W / 2, 118, "SHAKEEL", 104, "url(#holo)", 900, SANS, "middle",
                ' stroke="#ffffff" stroke-opacity=".25" stroke-width="1"')
            + t(W / 2, 118, "SHAKEEL", 104, "url(#spec)", 900, SANS, "middle", ' opacity=".35"')
            + t(W / 2, 168, "holographic chrome", 24, "#9aa0c8" if dark else "#555a78", family=MONO, anchor="middle"))
    return svg(h, body, "SHAKEEL as an iridescent chrome wordmark with a slowly sweeping highlight", defs)


# --------------------------------------------------------------------------- #
# 7 · Isometric city — the same real 24 months, drawn in isometric
# --------------------------------------------------------------------------- #
def isometric(dark: bool) -> str:
    h = 330
    bg = "#0d1117" if dark else "#ffffff"
    ink = "#e6edf3" if dark else "#1f2328"
    mut = "#8b949e" if dark else "#59636e"
    top, left, right = (("#56d364", "#2ea043", "#196c2e") if dark else ("#40c463", "#30a14e", "#216e39"))
    counts = dict(SUMMARY["months"])
    last = max(counts)
    y, m = int(last[:4]), int(last[5:7])
    keys = []
    for _ in range(24):
        keys.append(f"{y:04d}-{m:02d}")
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    keys.reverse()
    peak = max(counts.get(k, 0) for k in keys) or 1
    s, ox, oy = 17, 330, 118          # centred: the 12x2 block spans ~13 cube-widths
    cubes = []
    for i, k in enumerate(keys):
        col, row = i % 12, i // 12
        hgt = 6 + 150 * counts.get(k, 0) / peak
        cx = ox + (col - row) * s
        cy = oy + (col + row) * s * 0.5
        cubes.append((col + row, cx, cy, hgt))
    body = f'<rect width="{W}" height="{h}" rx="22" fill="{bg}"/>'
    for _, cx, cy, hgt in sorted(cubes):
        body += (f'<polygon points="{cx},{cy - hgt} {cx + s},{cy - hgt + s / 2} {cx},{cy - hgt + s} {cx - s},{cy - hgt + s / 2}" fill="{top}"/>'
                 f'<polygon points="{cx - s},{cy - hgt + s / 2} {cx},{cy - hgt + s} {cx},{cy + s} {cx - s},{cy + s / 2}" fill="{left}"/>'
                 f'<polygon points="{cx},{cy - hgt + s} {cx + s},{cy - hgt + s / 2} {cx + s},{cy + s / 2} {cx},{cy + s}" fill="{right}"/>')
    body += (t(28, 52, "24 months, isometric", 26, ink, 700)
             + t(28, 84, f"{keys[0]} → {keys[-1]}", 22, mut, family=MONO)
             + t(28, 306, "one tower per month · older year behind", 22, mut))
    return svg(h, body, f"An isometric city of 24 towers, one per month from {keys[0]} to {keys[-1]}, "
                        "height proportional to repository activity")


# --------------------------------------------------------------------------- #
# 8 · Blueprint — technical drawing, dimension lines and a title block
# --------------------------------------------------------------------------- #
def blueprint(dark: bool) -> str:
    h = 300
    bg = "#0b2a4a" if dark else "#eaf2fb"
    ln = "#9ec9ff" if dark else "#1d4f91"
    ink = "#e8f3ff" if dark else "#0b2a4a"
    grid = (f'<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse">'
            f'<path d="M20 0H0V20" fill="none" stroke="{ln}" stroke-opacity=".18"/></pattern>')
    draw = (f'<rect x="60" y="60" width="300" height="150" fill="none" stroke="{ln}" stroke-width="2" '
            f'pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="1;0" dur="2.4s" fill="freeze"/></rect>'
            f'<circle cx="210" cy="135" r="46" fill="none" stroke="{ln}" stroke-width="1.5" stroke-dasharray="6 5"/>'
            f'<path d="M60 238 H360 M60 230 V246 M360 230 V246" stroke="{ln}" stroke-width="1.5"/>'
            + t(210, 270, "600 units = 309 px", 22, ink, family=MONO, anchor="middle")
            + f'<path d="M388 60 V210 M380 60 H396 M380 210 H396" stroke="{ln}" stroke-width="1.5"/>')
    block = (f'<rect x="410" y="60" width="160" height="150" fill="none" stroke="{ln}" stroke-width="2"/>'
             f'<path d="M410 110 H570 M410 160 H570" stroke="{ln}"/>'
             + t(422, 94, "DWG 001", 22, ink, 700, MONO)
             + t(422, 144, "HAMMAD", 22, ink, family=MONO)
             + t(422, 194, "REV A", 22, ink, family=MONO))
    return svg(h, f'<rect width="{W}" height="{h}" rx="16" fill="{bg}"/><rect width="{W}" height="{h}" fill="url(#g)"/>'
                  + draw + block,
               "A blueprint drawing with dimension lines stating 600 units equals 309 pixels, "
               "and a title block reading DWG 001, HAMMAD, REV A", grid)


# --------------------------------------------------------------------------- #
# 9 · Halftone — a dot screen whose dots grow with a gradient
# --------------------------------------------------------------------------- #
def halftone(dark: bool) -> str:
    h = 240
    bg = "#101010" if dark else "#fff8f0"
    ink = "#ff4d2e" if dark else "#d9381e"
    txt = "#fafafa" if dark else "#141414"
    dots = []
    for row in range(12):
        for col in range(30):
            x, y = 12 + col * 20, 12 + row * 20
            r = 1 + 8.5 * (1 - math.hypot(x - 470, y - 120) / 480) ** 1.6
            if r > 1.2:
                dots.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{ink}"/>')
    body = (f'<rect width="{W}" height="{h}" rx="16" fill="{bg}"/>' + "".join(dots)
            + f'<rect x="24" y="70" width="352" height="110" rx="6" fill="{bg}"/>'
            + t(44, 124, "HALFTONE", 50, txt, 900, CONDENSED)
            + t(46, 160, "a print screen, in vector", 22, txt, family=MONO))
    return svg(h, body, "A red halftone dot screen that swells toward the right, with the word HALFTONE")


DESIGNS = {"aurora": aurora, "liquid-glass": liquid_glass, "bento": bento, "brutal": brutal,
           "kinetic": kinetic, "chrome": chrome, "isometric": isometric, "blueprint": blueprint,
           "halftone": halftone}


def main() -> None:
    for name, fn in DESIGNS.items():
        pair(name, fn)
    import xml.etree.ElementTree as ET   # parses only the files written above, never untrusted input
    files = sorted(OUT.glob("*.svg"))
    for f in files:
        ET.parse(f)
    print(f"{len(files)} SVGs written and parsed; every label >= {FLOOR:.1f} units "
          f"(11px in a phone column)")


if __name__ == "__main__":
    main()
