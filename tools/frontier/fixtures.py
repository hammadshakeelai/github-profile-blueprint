#!/usr/bin/env python3
"""Fixtures for the visual-frontier experiments.

    python tools/frontier/fixtures.py

Writes docs/frontier/fixtures/. Two families:

  lighting-*.svg   SVG lighting filters — feSpecularLighting / feDiffuseLighting
                   with distant, point and spot lights, plus one whose light
                   *moves* (an animated fePointLight). None has been tested in
                   this repository; together they are what "lit" pseudo-3D needs.

  anim.{gif,png,webp,avif}
                   One 24-frame animation encoded four ways (APNG is the .png).
                   Real 3D can't run inside a README, but pre-rendered frames can
                   ship as an animated image — if GitHub and the browsers animate
                   the format.

  embed-*.svg      Each animated image embedded *inside* an SVG as a data URI.
                   If the frames still play there, crisp vector text can sit on
                   top of a rendered 3D scene in a single file.

Every fixture draws a visible label saying what it is, so a screenshot is
self-describing.
"""
from __future__ import annotations

import base64
import io
import math
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "frontier" / "fixtures"
MONO = "ui-monospace, Menlo, Consolas, monospace"


def label(text: str, y: int = 26) -> str:
    return (f'<text x="16" y="{y}" font-family="{MONO}" font-size="16" fill="#e6edf3">{text}</text>')


# --------------------------------------------------------------------------- #
# Lighting
# --------------------------------------------------------------------------- #
# A bump source: a blurred shape whose alpha becomes a height map.
BUMP = ('<feGaussianBlur in="SourceAlpha" stdDeviation="6" result="h"/>')
LIGHTS = {
    "specular-distant": ('feSpecularLighting', 'surfaceScale="6" specularConstant="1.1" specularExponent="22" lighting-color="#ffffff"',
                         '<feDistantLight azimuth="235" elevation="40"/>'),
    "specular-point": ('feSpecularLighting', 'surfaceScale="6" specularConstant="1.2" specularExponent="26" lighting-color="#ffffff"',
                       '<fePointLight x="90" y="40" z="120"/>'),
    "specular-spot": ('feSpecularLighting', 'surfaceScale="6" specularConstant="1.3" specularExponent="20" lighting-color="#fff4d6"',
                      '<feSpotLight x="60" y="20" z="160" pointsAtX="160" pointsAtY="90" pointsAtZ="0" specularExponent="8" limitingConeAngle="40"/>'),
    "diffuse-distant": ('feDiffuseLighting', 'surfaceScale="5" diffuseConstant="1.0" lighting-color="#ffffff"',
                        '<feDistantLight azimuth="235" elevation="45"/>'),
    # The one that matters for "alive": a highlight that sweeps across the surface.
    "specular-moving": ('feSpecularLighting', 'surfaceScale="6" specularConstant="1.3" specularExponent="24" lighting-color="#ffffff"',
                        '<fePointLight x="20" y="40" z="110"><animate attributeName="x" values="20;300;20" '
                        'dur="3s" repeatCount="indefinite"/></fePointLight>'),
}


def lighting(name: str, prim: str, attrs: str, light: str, apply: bool = True) -> str:
    filt = (f'<filter id="lit" x="-10%" y="-10%" width="120%" height="120%">{BUMP}'
            f'<{prim} in="h" {attrs} result="l">{light}</{prim}>'
            f'<feComposite in="l" in2="SourceAlpha" operator="in" result="lc"/>'
            f'<feComposite in="SourceGraphic" in2="lc" operator="arithmetic" k1="0" k2="1" k3="1" k4="0"/>'
            f'</filter>')
    shape = ('<g {f}><rect x="40" y="46" width="240" height="96" rx="26" fill="#3b4cca"/>'
             '<circle cx="250" cy="94" r="30" fill="#c2419b"/></g>').format(f='filter="url(#lit)"' if apply else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 170" width="320" height="170">'
            f'<defs>{filt}</defs><rect width="320" height="170" fill="#0d1117"/>{shape}'
            f'{label(name if apply else name + " (control, no filter)", 162)}</svg>\n')


# --------------------------------------------------------------------------- #
# Animated raster
# --------------------------------------------------------------------------- #
def frames(n: int = 24, w: int = 240, h: int = 120) -> list[Image.Image]:
    """A lit sphere orbiting a centre, so any single frame differs from the next."""
    out = []
    for i in range(n):
        im = Image.new("RGB", (w, h), (13, 17, 23))
        d = ImageDraw.Draw(im)
        a = 2 * math.pi * i / n
        cx, cy = w / 2 + 80 * math.cos(a), h / 2 + 30 * math.sin(a)
        for r in range(26, 0, -2):                      # cheap shading: stacked discs
            t = r / 26
            col = (int(88 + 150 * (1 - t)), int(166 + 80 * (1 - t)), 255)
            d.ellipse((cx - r - (1 - t) * 6, cy - r - (1 - t) * 6, cx + r - (1 - t) * 6, cy + r - (1 - t) * 6), fill=col)
        d.text((8, 6), f"frame {i:02d}", fill=(230, 237, 243))
        out.append(im)
    return out


def encode(fr: list[Image.Image]) -> dict[str, bytes]:
    enc = {}
    for fmt, ext, kw in [("GIF", "gif", {"optimize": True}),
                         ("PNG", "png", {}),                      # APNG
                         ("WEBP", "webp", {"quality": 80, "method": 6}),
                         ("AVIF", "avif", {"quality": 70})]:
        buf = io.BytesIO()
        try:
            fr[0].save(buf, format=fmt, save_all=True, append_images=fr[1:], duration=60, loop=0, **kw)
            enc[ext] = buf.getvalue()
        except Exception as e:                                    # a missing encoder is itself a finding
            print(f"  could not encode {ext}: {type(e).__name__}: {e}")
    return enc


def embed(ext: str, data: bytes) -> str:
    mime = {"gif": "image/gif", "png": "image/png", "webp": "image/webp", "avif": "image/avif"}[ext]
    uri = f"data:{mime};base64,{base64.b64encode(data).decode()}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'viewBox="0 0 240 150" width="240" height="150"><rect width="240" height="150" fill="#0d1117"/>'
            f'<image href="{uri}" xlink:href="{uri}" x="0" y="0" width="240" height="120"/>'
            f'{label(f"animated {ext} inside SVG", 142)}</svg>\n')


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (prim, attrs, light) in LIGHTS.items():
        (OUT / f"lighting-{name}.svg").write_text(lighting(name, prim, attrs, light), encoding="utf-8")
        (OUT / f"lighting-{name}-control.svg").write_text(lighting(name, prim, attrs, light, apply=False),
                                                           encoding="utf-8")
    enc = encode(frames())
    for ext, data in enc.items():
        (OUT / f"anim.{ext}").write_bytes(data)
        (OUT / f"embed-{ext}.svg").write_text(embed(ext, data), encoding="utf-8")
    # Verify each encoding really is multi-frame, rather than trusting the encoder.
    for ext in enc:
        with Image.open(OUT / f"anim.{ext}") as im:
            n = getattr(im, "n_frames", 1)
        print(f"  anim.{ext:5} {len(enc[ext]) / 1024:6.1f} KB  frames={n}")
    print(f"fixtures in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
