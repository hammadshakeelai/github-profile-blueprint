#!/usr/bin/env python3
"""Track 2, corpus half: how many animated SVGs in the survey guard their
animation behind `prefers-reduced-motion`?

    python tools/research/reduced_motion_survey.py

Re-fetches only the SVGs the survey already recorded as animated (the harvest
stored metrics, not bodies) and looks for a reduced-motion media query. Writes
docs/research/data/reduced-motion.json.
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "research" / "data" / "reduced-motion.json"
UA = {"User-Agent": "profile-readme-research (+https://github.com/hammadshakeelai/github-profile-blueprint)"}
GUARD = re.compile(r"prefers-reduced-motion", re.I)


def fetch(url: str) -> tuple[str, bool | None]:
    try:
        req = urllib.request.Request(url, headers=UA)
        body = urllib.request.urlopen(req, timeout=20).read(400_000).decode("utf-8", "replace")
        return url, bool(GUARD.search(body))
    except Exception:
        return url, None


def main() -> None:
    images = json.loads((ROOT / "docs" / "survey" / "data" / "images.json").read_text(encoding="utf-8"))
    animated = [u for u, v in images.items() if (v.get("svg") or {}).get("animated")]
    print(f"{len(animated)} animated SVGs to re-check")

    guarded, plain, gone = [], 0, 0
    with cf.ThreadPoolExecutor(8) as ex:
        for i, (url, hit) in enumerate(ex.map(fetch, animated), 1):
            if hit is None:
                gone += 1
            elif hit:
                guarded.append(url)
            else:
                plain += 1
            if i % 400 == 0:
                print(f"  {i}/{len(animated)}", flush=True)

    live = len(guarded) + plain
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"animated": len(animated), "refetched": live,
                               "guarded": len(guarded), "unguarded": plain,
                               "unreachable": gone, "guarded_urls": guarded}, indent=1),
                   encoding="utf-8")
    print(f"\nre-fetched {live} (of {len(animated)}; {gone} no longer reachable)")
    print(f"guard their animation with prefers-reduced-motion: {len(guarded)}"
          f"  ({len(guarded) / max(live, 1):.1%})")
    for u in guarded[:10]:
        print("   ", u)


if __name__ == "__main__":
    main()
