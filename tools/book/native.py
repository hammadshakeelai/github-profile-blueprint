#!/usr/bin/env python3
"""Generate the live exhibits for chapter 4: an ASCII-STL skyline of real
activity data, and a GeoJSON map of where the most-copied profiles are made.

    python tools/book/native.py

Writes docs/book/data/skyline.stl.txt and docs/book/data/famous.geojson, which
the chapter embeds inside ```stl and ```geojson fences — GitHub renders both as
interactive viewers directly inside markdown.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "book" / "data"


def box(x0, y0, z0, x1, y1, z1) -> list[tuple]:
    """Twelve triangles of an axis-aligned box, outward-facing."""
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    faces = [((0, 2, 1), (0, 3, 2), (0, 0, -1)), ((4, 5, 6), (4, 6, 7), (0, 0, 1)),
             ((0, 1, 5), (0, 5, 4), (0, -1, 0)), ((2, 3, 7), (2, 7, 6), (0, 1, 0)),
             ((1, 2, 6), (1, 6, 5), (1, 0, 0)), ((0, 4, 7), (0, 7, 3), (-1, 0, 0))]
    out = []
    for a, b, n in faces:
        out += [(n, [v[i] for i in a]), (n, [v[i] for i in b])]
    return out


def skyline() -> str:
    """24 months of the account's real repository activity as a 3D bar city on a plinth."""
    summary = json.loads((DATA.parent.parent / "showcase" / "data" / "summary.json").read_text(encoding="utf-8"))
    counts = dict(summary["months"])
    # A continuous run of calendar months, quiet ones included: the API lists only
    # months with a push, and taking the last 24 of *those* would silently drop the
    # gaps and compress the timeline.
    last = max(counts)
    y, m = int(last[:4]), int(last[5:7])
    keys = []
    for _ in range(24):
        keys.append(f"{y:04d}-{m:02d}")
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    keys.reverse()
    tris = box(-1, -1, 0, len(keys) * 3 + 1, 4, 0.6)                 # plinth
    peak = max(counts.get(k, 0) for k in keys) or 1
    for i, k in enumerate(keys):
        h = 0.6 + 14 * counts.get(k, 0) / peak
        tris += box(i * 3, 0.5, 0.6, i * 3 + 2, 2.5, h)
    lines = ["solid skyline"]
    for n, (a, b, c) in tris:
        lines += [f"  facet normal {n[0]} {n[1]} {n[2]}", "    outer loop",
                  *[f"      vertex {p[0]:.2f} {p[1]:.2f} {p[2]:.2f}" for p in (a, b, c)],
                  "    endloop", "  endfacet"]
    return "\n".join(lines + ["endsolid skyline"]) + "\n"


# Locations as stated on each profile (GitHub API `location`, September 2026);
# profiles that state none are left off rather than guessed.
FAMOUS = [("rafaballerini", 2696, "Santa Catarina, Brazil", -27.24, -50.22),
          ("midudev", 1465, "Barcelona", 41.39, 2.17),
          ("novatorem", 758, "Toronto", 43.65, -79.38),
          ("anmol098", 689, "Dubai", 25.20, 55.27),
          ("trinib", 508, "Trinidad & Tobago", 10.69, -61.22),
          ("simonw", 443, "Half Moon Bay, California", 37.46, -122.43),
          ("MartinHeinz", 440, "Bratislava", 48.15, 17.11),
          ("andyruwruw", 290, "Bay Area, California", 37.77, -122.42)]


def famous_map() -> dict:
    return {"type": "FeatureCollection", "features": [
        {"type": "Feature",
         "geometry": {"type": "Point", "coordinates": [lon, lat]},
         "properties": {"profile": f"github.com/{u}", "stars": s, "location": loc,
                        "marker-size": "large" if s > 1000 else "medium" if s > 500 else "small",
                        "marker-color": "#f778ba" if s > 1000 else "#58a6ff"}}
        for u, s, loc, lat, lon in FAMOUS]}


def main() -> None:
    (DATA / "skyline.stl.txt").write_text(skyline(), encoding="utf-8")
    (DATA / "famous.geojson").write_text(json.dumps(famous_map(), indent=1), encoding="utf-8")
    stl = (DATA / "skyline.stl.txt").read_text()
    print(f"skyline: {stl.count('facet normal')} triangles, {len(stl) / 1024:.0f} KB "
          f"(GitHub's markdown limit is 512 KB)")
    print(f"map: {len(FAMOUS)} profiles")


if __name__ == "__main__":
    main()
