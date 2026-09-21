#!/usr/bin/env python3
"""Technique-first candidate discovery via GitHub code search.

Curated lists surface *popular* profiles. This finds *ambitious* ones: it
searches committed .svg files for animation and effect primitives, and keeps
only hits inside a profile repo (owner == repo name). A profile that commits its
own animated SVG is doing something a stat-card embed is not.

    python tools/survey/source_codesearch.py

Writes tools/survey/sources/codesearch.json, which harvest.py merges in.
Code search allows ~10 requests/minute; each term pages up to 1,000 results
(10 requests), so terms are spaced a minute apart.
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

OUT = Path(__file__).resolve().parent / "sources" / "codesearch.json"

TERMS = [
    "animateMotion",        # motion along a path
    "animateTransform",     # SMIL rotate/scale/translate
    "stroke-dashoffset",    # line-drawing animation
    "keyframes",            # CSS animation inside the SVG
    "feGaussianBlur",       # glow / blur
    "feTurbulence",         # noise, grain, organic texture
    "feDisplacementMap",    # distortion effects
    "textPath",             # text along a curve
    "prefers-color-scheme", # theme-aware SVG
]


def search(term: str) -> list[dict]:
    cmd = ["gh", "search", "code", term, "--extension", "svg",
           "--limit", "1000", "--json", "repository,path"]
    for attempt in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 0:
            return json.loads(r.stdout or "[]")
        print(f"  {term}: attempt {attempt + 1} failed: {r.stderr.strip()[:160]}", flush=True)
        time.sleep(70)
    return []


def main() -> None:
    found: dict[str, dict] = {}
    for i, term in enumerate(TERMS):
        if i:
            time.sleep(65)
        hits = search(term)
        prof = 0
        for h in hits:
            owner, name = h["repository"]["nameWithOwner"].split("/", 1)
            if owner.lower() != name.lower():
                continue
            prof += 1
            rec = found.setdefault(owner.lower(), {"user": owner, "sources": ["code-search"],
                                                   "categories": [], "svg_paths": []})
            cat = f"code-search: {term}"
            if cat not in rec["categories"]:
                rec["categories"].append(cat)
            if h["path"] not in rec["svg_paths"]:
                rec["svg_paths"].append(h["path"])
        print(f"{term:22s} hits={len(hits):4d}  in profile repos={prof:3d}  "
              f"unique profiles so far={len(found)}", flush=True)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(sorted(found.values(), key=lambda r: r["user"].lower()), indent=1),
                   encoding="utf-8")
    print(f"wrote {len(found)} profiles -> {OUT}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
