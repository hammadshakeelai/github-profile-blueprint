#!/usr/bin/env python3
"""Build the profile README chosen in docs/DIRECTION.md.

    python tools/profile/build.py

Writes profile/ — README.md plus assets/ — ready to copy into the profile
repository (hammadshakeelAl/hammadshakeelAl). Also writes
profile/README.staging.md, identical except that its image URLs point at this
repository, so the result can be rendered and checked on GitHub before it ever
reaches the profile.

The design is comp C with comp A's discipline: a window header, six project
windows each linking to the running thing, then grouped markdown lists. Rules
and reasoning: docs/DIRECTION.md.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "direction"))
from build import MONO, SANS, THEMES, W, check, svg, wrap  # noqa: E402

OUT = ROOT / "profile"
ASSETS = OUT / "assets"
# Where the images live once this is in the profile repository. Absolute URLs:
# a profile page resolves relative srcset paths inconsistently, and an absolute
# raw URL works in both contexts.
LIVE_BASE = "https://raw.githubusercontent.com/hammadshakeelAl/hammadshakeelAl/main/assets"
STAGING_BASE = ("https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/"
                "v2/research/profile/assets")
FEATURED = ["LinuxWeb", "RetroMuseum", "Tidebreaker", "Doomsday in 8086", "paklegalbench", "PersonalRag"]


def window(p: dict, url: str, inner: str, h: int) -> str:
    """A browser window: chrome bar, three dots, an address field, then content."""
    return (f'<rect width="{W}" height="{h}" rx="14" fill="{p["panel"]}" stroke="{p["line"]}"/>'
            f'<path d="M0 14 a14 14 0 0 1 14 -14 h{W - 28} a14 14 0 0 1 14 14 v36 h-{W} z" fill="{p["chrome"]}"/>'
            f'<circle cx="24" cy="25" r="6" fill="#ff5f57"/><circle cx="44" cy="25" r="6" fill="#febc2e"/>'
            f'<circle cx="64" cy="25" r="6" fill="#28c840"/>'
            f'<rect x="88" y="11" width="{W - 108}" height="28" rx="14" fill="{p["panel"]}"/>'
            f'<text x="104" y="32" font-family="{MONO}" font-size="22" fill="{p["muted"]}">{escape(url)}</text>'
            + inner)


def host_of(project: dict) -> str:
    target = project["demo"] or project["repo"]
    host = target.split("//", 1)[1].rstrip("/")
    return host if len(host) <= 30 else host[:29] + "…"


def write_pair(stem: str, make) -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    for theme, pal in THEMES.items():
        text = make(pal)
        check(f"profile/{stem}-{theme}.svg", text)
        (ASSETS / f"{stem}-{theme}.svg").write_text(text, encoding="utf-8")


def picture(base: str, stem: str, alt: str) -> str:
    return (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{base}/{stem}-dark.svg">\n'
            f'  <source media="(prefers-color-scheme: light)" srcset="{base}/{stem}-light.svg">\n'
            f'  <img src="{base}/{stem}-dark.svg" alt="{escape(alt)}" width="600">\n</picture>')


def build(content: dict) -> None:
    projects = {p["name"]: p for g in content["groups"] for p in g["projects"]}

    def header(p):
        thesis = wrap(content["thesis"], 26, W - 64, 0.52)
        lines = "".join(f'<text x="32" y="{168 + i * 36}" font-family="{SANS}" font-size="26" '
                        f'fill="{p["muted"]}">{escape(t)}</text>' for i, t in enumerate(thesis))
        h = 196 + 36 * len(thesis)
        cursor_y = 168 + 36 * (len(thesis) - 1)
        inner = (f'<text x="32" y="124" font-family="{SANS}" font-size="52" font-weight="800" '
                 f'fill="{p["text"]}">{escape(content["name"])}</text>{lines}'
                 # the only motion on the page: a caret at the end of the last line
                 f'<rect x="{32 + len(thesis[-1]) * 26 * 0.52 + 8:.0f}" y="{cursor_y - 20}" width="11" height="26" '
                 f'fill="{p["accent"]}"><animate attributeName="opacity" values="1;0" dur="1.1s" '
                 f'repeatCount="indefinite" calcMode="discrete"/></rect>')
        return svg(h, window(p, f'{content["handle"]}.github.io', inner, h),
                   f'{content["name"]} — {content["thesis"]}')

    write_pair("header", header)

    stems = {}
    for name in FEATURED:
        proj = projects[name]
        stem = "tab-" + "".join(ch for ch in name.lower() if ch.isalnum())
        stems[name] = stem
        desc = wrap(proj["line"], 24, W - 64, 0.54)[:3]

        def card(p, proj=proj, desc=desc):
            h = 150 + 32 * len(desc)
            lines = "".join(f'<text x="32" y="{138 + i * 32}" font-family="{SANS}" font-size="24" '
                            f'fill="{p["muted"]}">{escape(t)}</text>' for i, t in enumerate(desc))
            action = "▶ open in a tab" if proj["demo"] else "view source"
            inner = (f'<text x="32" y="102" font-family="{SANS}" font-size="36" font-weight="800" '
                     f'fill="{p["text"]}">{escape(proj["name"])}</text>{lines}'
                     f'<text x="{W - 32}" y="102" text-anchor="end" font-family="{SANS}" font-size="22" '
                     f'font-weight="700" fill="{p["link"]}">{action}</text>')
            return svg(h, window(p, host_of(proj), inner, h), f'{proj["name"]}: {proj["line"]}')

        write_pair(stem, card)

    def readme(base: str) -> str:
        md = [picture(base, "header", f'{content["name"]} — {content["thesis"]}'), "",
              "Everything here runs in a browser tab. Tap a window to open the real thing.", ""]
        for name in FEATURED:
            proj = projects[name]
            md += [f'<a href="{proj["demo"] or proj["repo"]}">',
                   picture(base, stems[name], f'{proj["name"]}: {proj["line"]}'), "</a>", ""]
        md += ["---", "", "### Everything else", ""]
        for g in content["groups"]:
            rest = [p for p in g["projects"] if p["name"] not in FEATURED]
            if not rest:
                continue
            md += [f"**{g['title']}**", ""]
            for p in rest:
                link = f"[{p['name']}]({p['demo']})" if p["demo"] else f"**{p['name']}**"
                md.append(f"- {link} — {p['line']} · [source]({p['repo']})")
            md.append("")
        md += [f"Main profile: [@{content['handle']}](https://github.com/{content['handle']})", ""]
        return "\n".join(md)

    (OUT / "README.md").write_text(readme(LIVE_BASE), encoding="utf-8")
    (OUT / "README.staging.md").write_text(readme(STAGING_BASE), encoding="utf-8")
    print(f"built profile/: README.md (+ staging copy) and {len(list(ASSETS.glob('*.svg')))} SVGs")


if __name__ == "__main__":
    build(json.loads((ROOT / "docs" / "direction" / "content.json").read_text(encoding="utf-8")))
