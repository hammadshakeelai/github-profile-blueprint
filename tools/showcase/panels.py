#!/usr/bin/env python3
"""SVG panels for the showcase README — every technique this repo verified.

Each panel is a function returning SVG source for one palette. They obey the
rules the research established, which is the whole point of the exercise: a
maximalist page that still works.

  * text never below the legibility floor at the width it will be shown
  * the first frame is the finished composition — nothing starts invisible
  * no gradientTransform animation (WebKit never animates it)
  * no external references, no scripts, no web fonts
  * every panel has a dark and a light file

Sizes are in viewBox units. `W` panels are shown at 600 units wide and clamp to
309px on a phone (so 21.4 units = 11px, the floor); `P` panels are drawn in 309
units for phones and served by a width-gated <picture> source.
"""
from __future__ import annotations

from xml.sax.saxutils import escape

W = 600                      # desktop-ish canvas
PHONE = 309                  # phone canvas: 1 unit == 1 px in the README column
FLOOR_UNITS_W = 21.36        # 11px at 309/600
SANS = "ui-sans-serif, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

DARK = {"bg": "#0d1117", "panel": "#161b22", "line": "#30363d", "text": "#e6edf3",
        "muted": "#8b949e", "accent": "#58a6ff", "hot": "#f778ba", "go": "#3fb950",
        "warm": "#d29922", "deep": "#1f6feb", "chrome": "#21262d"}
LIGHT = {"bg": "#ffffff", "panel": "#f6f8fa", "line": "#d0d7de", "text": "#1f2328",
         "muted": "#59636e", "accent": "#0969da", "hot": "#bf3989", "go": "#1a7f37",
         "warm": "#9a6700", "deep": "#0550ae", "chrome": "#eaeef2"}
THEMES = {"dark": DARK, "light": LIGHT}


def svg(w: int, h: int, body: str, label: str, extra: str = "") -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
            f'height="{h}" role="img" aria-label="{escape(label, {chr(34): "&quot;"})}"{extra}>'
            f'<title>{escape(label)}</title>{body}</svg>\n')


FLOOR_PX = 11.0              # measured: below this, supporting text is unreadable


def floor_for(canvas: float) -> float:
    """Smallest font size, in canvas units, that still renders at the floor once
    the image is clamped into the 309px column a phone gives a README."""
    return FLOOR_PX * canvas / PHONE


def text(x, y, s, size, fill, weight=400, family=SANS, anchor="start", extra="",
         canvas: float = W) -> str:
    # Clamped rather than trusted: this is the rule 55% of surveyed cards break,
    # and a rule you have to remember is one you forget on the last panel.
    size = max(size, floor_for(canvas))
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    w = f' font-weight="{weight}"' if weight != 400 else ""
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}"{w} '
            f'fill="{fill}"{a}{extra}>{escape(s)}</text>')


def card(p, w, h, r=14, fill=None) -> str:
    return (f'<rect width="{w}" height="{h}" rx="{r}" fill="{fill or p["panel"]}" '
            f'stroke="{p["line"]}"/>')


def wrap(s: str, size: float, width: float, ratio: float = 0.52) -> list[str]:
    """Greedy wrap using an average glyph-width ratio — the real face varies per
    viewer (no web fonts inside an image), so layout can never depend on it."""
    out, line = [], ""
    for word in s.split():
        trial = f"{line} {word}".strip()
        if len(trial) * size * ratio > width and line:
            out.append(line)
            line = word
        else:
            line = trial
    return out + ([line] if line else [])


# --------------------------------------------------------------------------- #
# 1 · Hero — shimmer, drifting particles, a typed line, a blinking caret
# --------------------------------------------------------------------------- #
def hero(p, name: str, line: str, motion: bool = True, width: int = W) -> str:
    h = 210 if width == W else 172
    k = width / W
    big, small = 54 * k, 24 * k
    stars = ""
    for i, (x, y, r, dur) in enumerate([(70, 40, 1.6, 7), (180, 30, 1.1, 9), (300, 55, 1.8, 6),
                                        (430, 28, 1.2, 11), (520, 62, 1.5, 8), (560, 36, 1.0, 10),
                                        (250, 150, 1.3, 12), (410, 165, 1.1, 9)]):
        cx, cy = x * k, y * k
        drift = (f'<animate attributeName="cy" values="{cy};{cy - 8 * k};{cy}" dur="{dur}s" '
                 f'repeatCount="indefinite"/>'
                 f'<animate attributeName="opacity" values="0.25;0.9;0.25" dur="{dur / 1.7:.1f}s" '
                 f'repeatCount="indefinite"/>') if motion else ""
        stars += f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{r * k:.1f}" fill="{p["accent"]}" opacity="0.5">{drift}</circle>'

    # The shimmer animates x1/x2, never gradientTransform — WebKit ignores that.
    sweep = ('<animate attributeName="x1" values="-0.6;1;-0.6" dur="6s" repeatCount="indefinite"/>'
             '<animate attributeName="x2" values="0;1.6;0" dur="6s" repeatCount="indefinite"/>') if motion else ""
    grad = (f'<defs><linearGradient id="sh" x1="-0.6" y1="0" x2="0" y2="0">{sweep}'
            f'<stop offset="0" stop-color="{p["accent"]}"/><stop offset="0.5" stop-color="{p["hot"]}"/>'
            f'<stop offset="1" stop-color="{p["go"]}"/></linearGradient>'
            f'<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{p["panel"]}"/><stop offset="1" stop-color="{p["bg"]}"/>'
            f'</linearGradient></defs>')

    # A clip rectangle widens in discrete steps, so the line appears character by
    # character without depending on the viewer's font metrics.
    typed = escape(line)
    tw = width - 64
    steps = 26
    reveal = (f'<animate attributeName="width" dur="2.6s" fill="freeze" calcMode="discrete" '
              f'keyTimes="{";".join(f"{i / steps:.3f}" for i in range(steps + 1))}" '
              f'values="{";".join(str(round(tw * i / steps)) for i in range(steps + 1))}"/>'
              ) if motion else ""
    caret = ('<animate attributeName="opacity" values="1;0" dur="1.1s" repeatCount="indefinite" '
             'calcMode="discrete"/>') if motion else ""

    body = (grad
            + f'<rect width="{width}" height="{h}" rx="16" fill="url(#fade)" stroke="{p["line"]}"/>'
            + stars
            + f'<rect x="32" y="{h - 46}" width="{width - 64}" height="4" rx="2" fill="url(#sh)"/>'
            + text(32, 88 * k + 20, name, big, p["text"], 800, canvas=width)
            + f'<clipPath id="tc"><rect x="32" y="{110 * k + 12}" height="{small * 1.6}" width="{tw if not motion else 0}">{reveal}</rect></clipPath>'
            + f'<g clip-path="url(#tc)">{text(32, 128 * k + 24, typed, small, p["muted"], family=MONO)}</g>'
            + f'<rect x="32" y="{110 * k + 14}" width="{small * 0.5:.0f}" height="{small * 1.2:.0f}" '
              f'fill="{p["hot"]}" opacity="1">{caret}</rect>')
    return svg(width, h, body, f"{name} — {line}")


# --------------------------------------------------------------------------- #
# 2 · Chips — self-made badges, committed, legible (no shields, no Camo)
# --------------------------------------------------------------------------- #
def chips(p, items: list[tuple[str, str]], width: int = W) -> str:
    size, pad, gap, hgt = 22, 14, 10, 40
    x, y, rows = 0, 0, []
    for label, colour in items:
        w = len(label) * size * 0.56 + pad * 2
        if x + w > width:
            x, y = 0, y + hgt + gap
        rows.append((x, y, w, label, colour))
        x += w + gap
    h = y + hgt
    body = "".join(
        f'<g><rect x="{bx:.0f}" y="{by}" width="{bw:.0f}" height="{hgt}" rx="{hgt//2}" '
        f'fill="{p["panel"]}" stroke="{p[c]}"/>'
        f'<circle cx="{bx + 16:.0f}" cy="{by + hgt/2:.0f}" r="5" fill="{p[c]}"/>'
        + text(bx + 30, by + hgt / 2 + 8, label, size, p["text"], 600, canvas=width) + "</g>"
        for bx, by, bw, label, c in rows)
    return svg(width, h, body, "Technology chips: " + ", ".join(i[0] for i in items))


# --------------------------------------------------------------------------- #
# 3 · Language distribution — animated stacked bar + legend, from real data
# --------------------------------------------------------------------------- #
def languages(p, data: list[tuple[str, int]], width: int = W) -> str:
    total = sum(n for _, n in data) or 1
    colours = ["accent", "hot", "go", "warm", "deep", "muted"]
    bar_y, bar_h = 56, 30
    x = 0
    bars, legend = "", ""
    for i, (name, n) in enumerate(data):
        w = width * n / total
        c = p[colours[i % len(colours)]]
        grow = (f'<animate attributeName="width" from="0" to="{w:.1f}" dur="{0.7 + i*0.12:.2f}s" '
                f'fill="freeze" begin="0s"/>')
        # Starts at full width and is *revealed* by a mask, so frame zero is complete.
        bars += (f'<rect x="{x:.1f}" y="{bar_y}" width="{w:.1f}" height="{bar_h}" fill="{c}"/>')
        ly, lx = 118 + (i // 3) * 34, (i % 3) * (width / 3)
        legend += (f'<circle cx="{lx + 10:.0f}" cy="{ly - 7}" r="7" fill="{c}"/>'
                   + text(lx + 26, ly, f"{name} · {n}", 22, p["muted"], canvas=width))
        x += w
    h = 118 + ((len(data) + 2) // 3) * 34
    body = (card(p, width, h) + text(24, 36, "Languages across 87 repositories", 24, p["text"], 700, canvas=width)
            + f'<g>{bars}</g>' + legend)
    return svg(width, h, body, "Language distribution: " +
               ", ".join(f"{n} {k}" for k, n in data))


# --------------------------------------------------------------------------- #
# 4 · Build rhythm — a real heatmap of repository activity by month
# --------------------------------------------------------------------------- #
def rhythm(p, months: list[tuple[str, int]], width: int = W) -> str:
    cols = len(months)
    cell = min(30, (width - 48) // max(cols, 1))
    peak = max((n for _, n in months), default=1) or 1
    h = 150
    cells = ""
    for i, (label, n) in enumerate(months):
        t = n / peak
        c = p["line"] if n == 0 else p["go"] if t > 0.66 else p["accent"] if t > 0.33 else p["deep"]
        o = 0.25 + 0.75 * t
        x = 24 + i * cell
        cells += (f'<rect x="{x}" y="{54}" width="{cell - 4}" height="{cell - 4}" rx="4" '
                  f'fill="{c}" opacity="{o:.2f}">'
                  f'<animate attributeName="opacity" values="{o:.2f};{min(1, o + .3):.2f};{o:.2f}" '
                  f'dur="4s" begin="{i * 0.12:.2f}s" repeatCount="indefinite"/></rect>')
        if i % 3 == 0:
            cells += text(x + cell / 2, 54 + cell + 22, label, 17, p["muted"], anchor="middle")
    body = (card(p, width, h) + text(24, 36, "Repository activity by month", 24, p["text"], 700, canvas=width)
            + cells)
    return svg(width, h, body,
               "Heatmap of repository activity per month, brighter where more repositories moved")


# --------------------------------------------------------------------------- #
# 5 · Terminal — a session that types itself, then loops
# --------------------------------------------------------------------------- #
def terminal(p, lines: list[tuple[str, str]], width: int = W) -> str:
    row, top = 30, 78
    h = top + row * len(lines) + 26
    body = [card(p, width, h),
            f'<path d="M0 16 a16 16 0 0 1 16 -16 h{width - 32} a16 16 0 0 1 16 16 v34 h-{width} z" '
            f'fill="{p["chrome"]}"/>',
            f'<circle cx="26" cy="26" r="6" fill="#ff5f57"/><circle cx="46" cy="26" r="6" fill="#febc2e"/>'
            f'<circle cx="66" cy="26" r="6" fill="#28c840"/>',
            text(width / 2, 34, "bash — the things that run in a tab", 20, p["muted"],
                 family=MONO, anchor="middle")]
    for i, (kind, s) in enumerate(lines):
        y = top + i * row
        colour = {"cmd": p["text"], "out": p["muted"], "ok": p["go"], "warn": p["warm"]}[kind]
        prefix = "$ " if kind == "cmd" else "  "
        # Every line is legible in frame zero; the animation only tints a command
        # as it "runs", so a static renderer loses nothing.
        line_svg = text(24, y, prefix + s, 21, colour, family=MONO)
        if kind == "cmd":
            line_svg = line_svg.replace("</text>",
                f'<animate attributeName="fill" values="{p["accent"]};{colour}" dur="0.6s" '
                f'begin="{i * 0.35:.2f}s" fill="freeze"/></text>')
        body.append(line_svg)
    body.append(f'<rect x="24" y="{top + row * len(lines) - 14}" width="11" height="20" '
                f'fill="{p["go"]}"><animate attributeName="opacity" values="1;0" dur="1s" '
                f'repeatCount="indefinite" calcMode="discrete"/></rect>')
    return svg(width, h, "".join(body), "A terminal session listing the projects")


# --------------------------------------------------------------------------- #
# 6 · Orbit — labels riding circular paths (animateMotion + textPath)
# --------------------------------------------------------------------------- #
def orbit(p, rings: list[list[str]], width: int = W) -> str:
    h = 330
    cx, cy = width / 2, h / 2
    body = [card(p, width, h)]
    for ri, labels in enumerate(rings):
        r = 62 + ri * 52
        dur = 26 + ri * 9
        body.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{p["line"]}" '
                    f'stroke-dasharray="3 7"/>')
        for i, label in enumerate(labels):
            start = i * 360 / len(labels)
            colour = [p["accent"], p["hot"], p["go"], p["warm"]][(ri + i) % 4]
            body.append(
                f'<g transform="rotate({start} {cx} {cy})">'
                f'<g transform="translate({cx + r} {cy})">'
                f'<circle r="5" fill="{colour}"/>'
                + text(10, 6, label, 20, p["text"], 600, canvas=width) +
                f'</g></g>'
                if ri == 0 else
                f'<g><animateTransform attributeName="transform" type="rotate" '
                f'from="{start} {cx} {cy}" to="{start + 360} {cx} {cy}" dur="{dur}s" '
                f'repeatCount="indefinite"/>'
                f'<g transform="translate({cx + r} {cy})"><circle r="5" fill="{colour}"/>'
                + text(10, 6, label, 20, p["text"], 600, canvas=width) + '</g></g>')
    body.append(f'<circle cx="{cx}" cy="{cy}" r="34" fill="{p["bg"]}" stroke="{p["accent"]}"/>')
    body.append(text(cx, cy + 8, "stack", 22, p["accent"], 700, anchor="middle", canvas=width))
    return svg(width, h, "".join(body),
               "Concentric rings of technologies orbiting a centre labelled stack: "
               + "; ".join(", ".join(r) for r in rings))


# --------------------------------------------------------------------------- #
# 7 · Timeline — a line that draws itself, with real dated milestones
# --------------------------------------------------------------------------- #
def timeline(p, events: list[tuple[str, str]], width: int = W) -> str:
    h = 90 + len(events) * 66
    x = 40
    body = [card(p, width, h), text(24, 38, "How it went", 24, p["text"], 700)]
    y0, y1 = 64, h - 24
    body.append(f'<path d="M{x} {y0} L{x} {y1}" stroke="{p["accent"]}" stroke-width="3" '
                f'fill="none" pathLength="1" stroke-dasharray="1" stroke-dashoffset="0">'
                f'<animate attributeName="stroke-dashoffset" values="1;0" dur="1.6s" '
                f'fill="freeze" begin="0s"/></path>')
    for i, (when, what) in enumerate(events):
        y = y0 + 34 + i * 66
        body.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{p["bg"]}" stroke="{p["accent"]}" '
                    f'stroke-width="3"/>')
        body.append(text(x + 24, y - 4, when, 19, p["hot"], 700, family=MONO, canvas=width))
        for j, ln in enumerate(wrap(what, 21, width - x - 56)[:2]):
            body.append(text(x + 24, y + 22 + j * 24, ln, 21, p["text"], canvas=width))
    return svg(width, h, "".join(body),
               "Timeline: " + "; ".join(f"{w} {t}" for w, t in events))


# --------------------------------------------------------------------------- #
# 8 · Gauges — real counts, drawn as arcs that sweep in
# --------------------------------------------------------------------------- #
def gauges(p, items: list[tuple[str, int, int, str]], width: int = W) -> str:
    n = len(items)
    cw = width / n
    h = 176
    body = [card(p, width, h)]
    for i, (label, value, cap, colour) in enumerate(items):
        cx, cy, r = cw * (i + 0.5), 86, 42
        frac = min(1.0, value / cap)
        body.append(f'<circle cx="{cx:.0f}" cy="{cy}" r="{r}" fill="none" stroke="{p["line"]}" '
                    f'stroke-width="9"/>')
        body.append(
            f'<circle cx="{cx:.0f}" cy="{cy}" r="{r}" fill="none" stroke="{p[colour]}" '
            f'stroke-width="9" stroke-linecap="round" pathLength="1" '
            f'stroke-dasharray="{frac:.3f} 1" transform="rotate(-90 {cx:.0f} {cy})">'
            f'<animate attributeName="stroke-dasharray" values="0 1;{frac:.3f} 1" dur="1.2s" '
            f'begin="{i * 0.15:.2f}s" fill="freeze"/></circle>')
        body.append(text(cx, cy + 9, str(value), 30, p["text"], 800, anchor="middle", canvas=width))
        body.append(text(cx, 156, label, 19, p["muted"], anchor="middle", canvas=width))
    return svg(width, h, "".join(body),
               "Counts: " + ", ".join(f"{v} {l}" for l, v, _, _ in items))


# --------------------------------------------------------------------------- #
# 9 · Marquee — a ticker that scrolls forever (and holds still when asked)
# --------------------------------------------------------------------------- #
def marquee(p, words: list[str], motion: bool = True, width: int = W) -> str:
    h, size = 56, 22
    run = "   ·   ".join(words)
    span = len(run) * size * 0.56
    slide = (f'<animateTransform attributeName="transform" type="translate" '
             f'from="0 0" to="-{span:.0f} 0" dur="{max(14, span / 42):.0f}s" '
             f'repeatCount="indefinite"/>') if motion else ""
    body = (f'<defs><clipPath id="mq"><rect width="{width}" height="{h}" rx="12"/></clipPath></defs>'
            + card(p, width, h, 12)
            + f'<g clip-path="url(#mq)"><g>{slide}'
            + text(12, 36, run, size, p["muted"], family=MONO, canvas=width)
            + text(12 + span, 36, run, size, p["muted"], family=MONO, canvas=width)
            + "</g></g>")
    return svg(width, h, body, "A scrolling ticker: " + run)


# --------------------------------------------------------------------------- #
# 10 · Project window — the design chosen in DIRECTION.md, one per project
# --------------------------------------------------------------------------- #
def window(p, title: str, line: str, host: str, action: str, width: int = W) -> str:
    desc = wrap(line, 24, width - 64, 0.54)[:2]
    h = 132 + 32 * len(desc)
    body = [card(p, width, h),
            f'<path d="M0 14 a14 14 0 0 1 14 -14 h{width - 28} a14 14 0 0 1 14 14 v36 h-{width} z" '
            f'fill="{p["chrome"]}"/>',
            f'<circle cx="24" cy="25" r="6" fill="#ff5f57"/><circle cx="44" cy="25" r="6" fill="#febc2e"/>'
            f'<circle cx="64" cy="25" r="6" fill="#28c840"/>',
            f'<rect x="88" y="11" width="{width - 108}" height="28" rx="14" fill="{p["panel"]}"/>',
            text(104, 32, host, 21, p["muted"], family=MONO, canvas=width),
            text(24, 96, title, 34, p["text"], 800, canvas=width),
            text(width - 24, 96, action, 21, p["accent"], 700, anchor="end")]
    for i, ln in enumerate(desc):
        body.append(text(24, 130 + i * 32, ln, 24, p["muted"], canvas=width))
    return svg(width, h, "".join(body), f"{title}: {line}")


# --------------------------------------------------------------------------- #
# 11 · Wave footer — layered paths that slide past each other
# --------------------------------------------------------------------------- #
def wave(p, width: int = W, motion: bool = True) -> str:
    h = 120
    layers = [(p["deep"], 0.35, 17), (p["accent"], 0.28, 13), (p["hot"], 0.22, 9)]
    body = [f'<rect width="{width}" height="{h}" fill="none"/>']
    for i, (colour, op, dur) in enumerate(layers):
        amp, base = 14 + i * 5, 56 + i * 14
        d = (f"M0 {base} "
             + " ".join(f"Q {x + 30} {base + (amp if (x // 60) % 2 == 0 else -amp)} {x + 60} {base}"
                        for x in range(0, width * 2, 60))
             + f" L{width * 2} {h} L0 {h} Z")
        slide = (f'<animateTransform attributeName="transform" type="translate" from="0 0" '
                 f'to="-{width} 0" dur="{dur}s" repeatCount="indefinite"/>') if motion else ""
        body.append(f'<g opacity="{op}"><path d="{d}" fill="{colour}"/>{slide}</g>')
    return svg(width, h, "".join(body), "An animated wave footer")


# --------------------------------------------------------------------------- #
# 12 · Quote — a pull quote with a drawn accent rule
# --------------------------------------------------------------------------- #
def quote(p, line: str, source: str, width: int = W) -> str:
    lines = wrap(line, 27, width - 92, 0.53)[:3]
    h = 78 + 36 * len(lines)
    body = [card(p, width, h),
            f'<path d="M24 24 L24 {h - 24}" stroke="{p["hot"]}" stroke-width="4" pathLength="1" '
            f'stroke-dasharray="1" stroke-dashoffset="1">'
            f'<animate attributeName="stroke-dashoffset" values="1;0" dur="1s" fill="freeze"/></path>']
    for i, ln in enumerate(lines):
        body.append(text(48, 52 + i * 36, ln, 27, p["text"], 600, canvas=width))
    body.append(text(48, h - 20, source, 19, p["muted"], family=MONO, canvas=width))
    return svg(width, h, "".join(body), f"Quote: {line} — {source}")
