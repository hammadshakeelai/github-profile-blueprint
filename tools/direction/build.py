#!/usr/bin/env python3
"""Build the three Phase 4 design comps from docs/direction/content.json.

    python tools/direction/build.py

Writes docs/direction/comp-{a,b,c}/ — a README.md plus dark and light SVGs —
and refuses to write any SVG whose smallest text would render under 11px in
GitHub's 309px phone column (the legibility floor from the survey).

  A · Index  — restrained and typographic; markdown does the reading
  B · Boot   — dense instrument panel; a boot log of the systems
  C · Tabs   — the unexpected one: each project is a browser window you can
               tap into, because everything here runs in a browser tab

Output is deterministic: same content, same bytes.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "direction"
sys.path.insert(0, str(ROOT / "tools" / "survey"))
from harvest import svg_metrics  # noqa: E402  (the survey's own legibility measure)

W = 600                    # viewBox width for every card
PHONE = 309                # measured profile README column on a 390px phone
FLOOR = 11                 # px
MIN_UNITS = FLOOR * W / PHONE          # 21.36 -> text runs are set at 22+ units

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
SERIF = "'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

THEMES = {
    "dark":  {"page": "#0d1117", "panel": "#161b22", "line": "#30363d", "text": "#e6edf3",
              "muted": "#8b949e", "accent": "#ff7b54", "ok": "#3fb950", "link": "#58a6ff", "chrome": "#21262d"},
    "light": {"page": "#ffffff", "panel": "#f6f8fa", "line": "#d0d7de", "text": "#1f2328",
              "muted": "#59636e", "accent": "#c4401b", "ok": "#1a7f37", "link": "#0969da", "chrome": "#eaeef2"},
}


def wrap(text: str, size: float, width: float, advance: float = 0.54) -> list[str]:
    """Greedy word wrap using a conservative mean glyph advance."""
    per_line = max(1, int(width / (size * advance)))
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if len(trial) <= per_line:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur] if cur else lines


def svg(height: int, body: str, label: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" '
            f'height="{height}" role="img" aria-label="{escape(label, {chr(34): "&quot;"})}">\n{body}\n</svg>\n')


def check(name: str, text: str) -> None:
    m = svg_metrics(text)
    if m["has_text"]:
        px = m["min_font"] * PHONE / m["vb_w"]
        if px < FLOOR - 0.01:
            sys.exit(f"{name}: smallest text {m['min_font']} units renders {px:.1f}px at {PHONE}px — below {FLOOR}px")


def write(folder: Path, stem: str, make) -> str:
    for theme, pal in THEMES.items():
        text = make(pal)
        check(f"{folder.name}/{stem}-{theme}.svg", text)
        (folder / f"{stem}-{theme}.svg").write_text(text, encoding="utf-8")
    return stem


def picture(stem: str, alt: str, width: int | None = None) -> str:
    w = f' width="{width}"' if width else ""
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{stem}-dark.svg">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="{stem}-light.svg">\n'
            f'  <img src="{stem}-dark.svg" alt="{escape(alt)}"{w}>\n</picture>')


# --------------------------------------------------------------------------- #
# A · Index
# --------------------------------------------------------------------------- #

def comp_a(c: dict) -> None:
    d = OUT / "comp-a"
    d.mkdir(parents=True, exist_ok=True)

    def header(p):
        thesis = wrap(c["thesis"], 26, W - 64, 0.52)
        lines = "".join(f'<text x="32" y="{176 + i * 36}" font-family="{SANS}" font-size="26" fill="{p["muted"]}">'
                        f'{escape(t)}</text>' for i, t in enumerate(thesis))
        h = 196 + 36 * len(thesis)
        return svg(h, f'<rect width="{W}" height="{h}" fill="{p["page"]}"/>'
                      f'<text x="32" y="96" font-family="{SERIF}" font-size="62" font-weight="700" '
                      f'fill="{p["text"]}">{escape(c["name"])}</text>'
                      f'<rect x="32" y="120" width="56" height="5" fill="{p["accent"]}"/>{lines}',
                   f'{c["name"]} — {c["thesis"]}')

    write(d, "header", header)
    md = [picture("header", f'{c["name"]} — {c["thesis"]}'), "",
          "**Everything below runs in a browser tab.** Open a name to use it; source sits beside it.", ""]
    for g in c["groups"]:
        md += [f"### {g['title']}", ""]
        for p in g["projects"]:
            name = f"**[{p['name']}]({p['demo']})**" if p["demo"] else f"**{p['name']}**"
            md.append(f"- {name} — {p['line']} · [source]({p['repo']})")
        md.append("")
    md += ["---", "", f"More on the main profile: [@{c['handle']}](https://github.com/{c['handle']})", ""]
    (d / "README.md").write_text("\n".join(md), encoding="utf-8")


# --------------------------------------------------------------------------- #
# B · Boot
# --------------------------------------------------------------------------- #

def comp_b(c: dict) -> None:
    d = OUT / "comp-b"
    d.mkdir(parents=True, exist_ok=True)
    systems = [p for g in c["groups"] for p in g["projects"]][:6]
    tags = {"LinuxWeb": "alpine · v86", "archbtw": "arch · v86", "RetroMuseum": "retro · v86",
            "OpenVScode": "android ide", "Tidebreaker": "three.js", "Boat-Chase": "three.js"}

    def boot(p):
        # SVG collapses runs of spaces, so columns get explicit x positions.
        rows = ["$ boot --all"] + [
            f'[ ok ]<tspan x="122">{escape(s["name"])}</tspan>'
            f'<tspan x="296" fill="{p["muted"]}">{escape(tags.get(s["name"], ""))}</tspan>' for s in systems]
        body = [f'<rect width="{W}" height="{H}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>',
                f'<circle cx="28" cy="26" r="7" fill="#ff5f57"/><circle cx="50" cy="26" r="7" fill="#febc2e"/>'
                f'<circle cx="72" cy="26" r="7" fill="#28c840"/>',
                f'<text x="100" y="33" font-family="{MONO}" font-size="22" fill="{p["muted"]}">hammad@web</text>']
        for i, r in enumerate(rows):
            y = 84 + i * 36
            colour = p["text"] if i else p["ok"]
            # settle once: each line appears in turn, then everything stays
            body.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="22" fill="{colour}" opacity="0">'
                        f'{r if i else escape(r)}<set attributeName="opacity" to="1" begin="{0.25 + i * 0.28:.2f}s" fill="freeze"/></text>')
        ready_y = 84 + len(rows) * 36 + 8
        body.append(f'<text x="28" y="{ready_y}" font-family="{MONO}" font-size="22" font-weight="700" '
                    f'fill="{p["ok"]}" opacity="0">ready — every system runs in a browser tab'
                    f'<set attributeName="opacity" to="1" begin="{0.25 + len(rows) * 0.28:.2f}s" fill="freeze"/></text>')
        return svg(H, "".join(body), "Boot log listing the systems, each marked ok")

    H = 84 + 7 * 36 + 8 + 40
    write(d, "boot", boot)

    def monitor(p):
        y, parts = 40, []
        for g in c["groups"]:
            parts.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="22" font-weight="700" '
                         f'fill="{p["accent"]}">{escape(g["title"].upper())}</text>')
            y += 38
            for proj in g["projects"]:
                live = bool(proj["demo"])
                parts.append(f'<circle cx="36" cy="{y - 7}" r="6" fill="{p["ok"] if live else p["muted"]}"/>'
                             f'<text x="54" y="{y}" font-family="{MONO}" font-size="22" fill="{p["text"]}">'
                             f'{escape(proj["name"])}</text>'
                             f'<text x="{W - 28}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="22" '
                             f'fill="{p["muted"]}">{"live" if live else "source"}</text>')
                y += 34
            y += 20
        return svg(y, f'<rect width="{W}" height="{y}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>'
                      + "".join(parts), "Process monitor listing every project, live demos marked green")

    write(d, "monitor", monitor)
    md = [picture("boot", "Boot log listing the systems, each marked ok"), "",
          picture("monitor", "Every project, grouped; green means a live demo you can open"), ""]
    for g in c["groups"]:
        md += [f"<details>\n<summary><b>{g['title']}</b></summary>", ""]
        for p in g["projects"]:
            demo = f" · [open]({p['demo']})" if p["demo"] else ""
            md.append(f"- **{p['name']}** — {p['line']}{demo} · [source]({p['repo']})")
        md += ["", "</details>", ""]
    md += [f"More on the main profile: [@{c['handle']}](https://github.com/{c['handle']})", ""]
    (d / "README.md").write_text("\n".join(md), encoding="utf-8")


# --------------------------------------------------------------------------- #
# C · Tabs
# --------------------------------------------------------------------------- #

def comp_c(c: dict) -> None:
    d = OUT / "comp-c"
    d.mkdir(parents=True, exist_ok=True)

    def window(p, url: str, inner: str, h: int) -> str:
        return (f'<rect width="{W}" height="{h}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>'
                f'<path d="M0 14 a14 14 0 0 1 14 -14 h{W - 28} a14 14 0 0 1 14 14 v36 h-{W} z" fill="{p["chrome"]}"/>'
                f'<circle cx="24" cy="25" r="6" fill="#ff5f57"/><circle cx="44" cy="25" r="6" fill="#febc2e"/>'
                f'<circle cx="64" cy="25" r="6" fill="#28c840"/>'
                f'<rect x="88" y="11" width="{W - 108}" height="28" rx="14" fill="{p["panel"]}"/>'
                f'<text x="104" y="32" font-family="{MONO}" font-size="22" fill="{p["muted"]}">{escape(url)}</text>'
                + inner)

    def header(p):
        thesis = wrap(c["thesis"], 26, W - 64, 0.52)
        lines = "".join(f'<text x="32" y="{168 + i * 36}" font-family="{SANS}" font-size="26" fill="{p["muted"]}">'
                        f'{escape(t)}</text>' for i, t in enumerate(thesis))
        h = 190 + 36 * len(thesis)
        inner = (f'<text x="32" y="124" font-family="{SANS}" font-size="52" font-weight="800" fill="{p["text"]}">'
                 f'{escape(c["name"])}</text>{lines}')
        return svg(h, window(p, f"{c['handle']}.github.io", inner, h), f'{c["name"]} — {c["thesis"]}')

    write(d, "header", header)
    featured = ["LinuxWeb", "archbtw", "RetroMuseum", "Tidebreaker", "Boat-Chase",
                "Doomsday in 8086", "paklegalbench", "PersonalRag"]
    projects = {p["name"]: p for g in c["groups"] for p in g["projects"]}
    md = [picture("header", f'{c["name"]} — {c["thesis"]}'), "",
          "Each window below is a real project. Tap one to open it — they all run in a browser tab.", ""]
    for name in featured:
        proj = projects[name]
        stem = "tab-" + "".join(ch for ch in name.lower() if ch.isalnum())
        host = proj["demo"].split("//", 1)[1].rstrip("/") if proj["demo"] else proj["repo"].split("//", 1)[1]
        host = host if len(host) <= 30 else host[:29] + "…"
        # never drop words: a card grows to three lines rather than truncate
        desc = wrap(proj["line"], 24, W - 64, 0.54)[:3]

        def card(p, proj=proj, host=host, desc=desc):
            h = 150 + 32 * len(desc)
            lines = "".join(f'<text x="32" y="{138 + i * 32}" font-family="{SANS}" font-size="24" '
                            f'fill="{p["muted"]}">{escape(t)}</text>' for i, t in enumerate(desc))
            action = "▶ open in a tab" if proj["demo"] else "view source"
            inner = (f'<text x="32" y="102" font-family="{SANS}" font-size="36" font-weight="800" '
                     f'fill="{p["text"]}">{escape(proj["name"])}</text>{lines}'
                     f'<text x="{W - 32}" y="102" text-anchor="end" font-family="{SANS}" font-size="22" '
                     f'font-weight="700" fill="{p["link"]}">{action}</text>')
            return svg(h, window(p, host, inner, h), f'{proj["name"]}: {proj["line"]}')

        write(d, stem, card)
        target = proj["demo"] or proj["repo"]
        md += [f'<a href="{target}">', picture(stem, f'{proj["name"]}: {proj["line"]}'), "</a>", ""]
    rest = [p for g in c["groups"] for p in g["projects"] if p["name"] not in featured]
    md += ["**Also:** " + " · ".join(f"[{p['name']}]({p['demo'] or p['repo']})" for p in rest), "",
           f"More on the main profile: [@{c['handle']}](https://github.com/{c['handle']})", ""]
    (d / "README.md").write_text("\n".join(md), encoding="utf-8")


def main() -> None:
    content = json.loads((OUT / "content.json").read_text(encoding="utf-8"))
    comp_a(content)
    comp_b(content)
    comp_c(content)
    n = sum(1 for _ in OUT.glob("comp-*/*.svg"))
    print(f"built 3 comps, {n} SVGs, every text run >= {MIN_UNITS:.1f} units (>= {FLOOR}px at {PHONE}px)")


if __name__ == "__main__":
    main()
