#!/usr/bin/env python3
"""Pin the survey's parsing behaviour so a refactor can't change it silently.

    python tools/tests/golden.py --record     # write the expected fingerprint
    python tools/tests/golden.py              # check against it

The survey's numbers come from three functions — `extract_images`, `resolve`
and `svg_metrics`. Track 7 moves them out of `harvest.py` into a shared module
so `profile-lint` can run without the survey tooling, and every published figure
depends on them behaving identically afterwards.

So: run them over fixed inputs (the technique examples, the profile's own SVGs,
and a synthetic README exercising every image syntax), hash the results, and
compare. No network.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "survey"))
GOLDEN = ROOT / "tools" / "tests" / "golden.json"

README = """
# Fixture

![markdown image](assets/a.svg)
![](./b.png)
<img src="https://example.com/c.svg" width="400" alt="absolute">
<img src="assets/d.svg" width="100%">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/e-dark.svg">
  <source media="(max-width: 600px)" srcset="assets/e-phone.svg">
  <img src="assets/e.svg" alt="themed" width="600">
</picture>
<a href="x"><img src="https://img.shields.io/badge/a-b-blue" alt=""></a>
![fragment](assets/f.svg#gh-dark-mode-only)
<!-- ![commented out](assets/never.svg) -->
```
![in a fence](assets/never2.svg)
```
"""


def fingerprint() -> dict:
    from harvest import extract_images, resolve, svg_metrics  # noqa: E402

    occ, signals = extract_images(README, "owner", "owner", "main")
    out: dict = {
        "signals": signals,
        "images": [{k: o.get(k) for k in ("url", "kind", "via", "width", "width_pct",
                                          "media", "fragment")} for o in occ],
        "resolve": {u: list(resolve(u, "owner", "owner", "main", frozenset()))
                    for u in ("assets/a.svg", "./b.png", "/absolute/c.svg",
                              "https://example.com/d.svg",
                              "https://raw.githubusercontent.com/owner/owner/main/e.svg")},
        "svg": {},
    }
    for d in ("docs/techniques/examples", "profile/assets", "docs/research/examples"):
        for f in sorted((ROOT / d).glob("*.svg")):
            m = svg_metrics(f.read_text(encoding="utf-8")) or {}
            out["svg"][f"{d}/{f.name}"] = {k: m.get(k) for k in
                                           ("vb_w", "vb_h", "intrinsic_w", "min_font", "max_font",
                                            "has_text", "animated", "techniques", "size_method")}
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", action="store_true")
    a = ap.parse_args()

    got = fingerprint()
    digest = hashlib.sha256(json.dumps(got, sort_keys=True).encode()).hexdigest()[:16]

    if a.record:
        GOLDEN.write_text(json.dumps({"sha": digest, "data": got}, indent=1, sort_keys=True),
                          encoding="utf-8")
        print(f"recorded {len(got['svg'])} SVGs, {len(got['images'])} image occurrences — {digest}")
        return

    if not GOLDEN.exists():
        sys.exit("no golden.json — run with --record first")
    want = json.loads(GOLDEN.read_text(encoding="utf-8"))
    if want["sha"] == digest:
        print(f"ok — {len(got['svg'])} SVGs, {len(got['images'])} image occurrences, "
              f"fingerprint {digest}")
        return

    print(f"CHANGED: expected {want['sha']}, got {digest}\n")
    for section in ("signals", "resolve", "images", "svg"):
        a_, b_ = want["data"][section], got[section]
        if a_ == b_:
            continue
        print(f"  {section}:")
        if isinstance(a_, dict):
            for k in sorted(set(a_) | set(b_)):
                if a_.get(k) != b_.get(k):
                    print(f"    {k}\n      was {a_.get(k)}\n      now {b_.get(k)}")
        else:
            for i, (x, y) in enumerate(zip(a_, b_)):
                if x != y:
                    print(f"    [{i}]\n      was {x}\n      now {y}")
            if len(a_) != len(b_):
                print(f"    length {len(a_)} -> {len(b_)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
