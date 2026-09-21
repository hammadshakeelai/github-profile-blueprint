#!/usr/bin/env python3
"""Rank surveyed profiles into candidates worth looking at.

    python tools/survey/shortlist.py [--top 40]

This is a pre-filter, not the judgement. It surfaces profiles doing their own
visual work that actually renders; which of them are genuinely exceptional is
decided by looking at them (see screenshot.py), and recorded by hand in
docs/survey/SHORTLIST.md.

Rewards: custom SVGs, animation in them, dark/light switching.
Penalises: broken images, cards illegible on a phone, badge walls.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[2] / "docs" / "survey" / "data"


def score(r: dict) -> float:
    s = 3 * min(r["custom_svgs"], 6) + 4 * min(r["custom_animated"], 4)
    s += 5 if r["theme_switch"] != "none" else 0
    s -= 4 * min(r["broken"], 3)
    s -= 2 * min(r["illegible_cards"], 3)
    s -= 6 if r["badge_share"] > 0.5 else 0
    return s


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    rows = json.loads((DATA / "rows.json").read_text(encoding="utf-8"))
    live = [r for r in rows if r["status"] == "live" and r["images"] > 0]
    ranked = sorted(live, key=lambda r: (-score(r), r["user"].lower()))[: a.top]
    for r in ranked:
        r["score"] = score(r)
        src = "search" if any(c.startswith("code-search") for c in r["categories"]) else "curated"
        print(f"{r['score']:5.0f}  {r['user']:<24} {src:<8} custom={r['custom_svgs']:<3} "
              f"anim={r['custom_animated']:<3} theme={r['theme_switch']:<8} brk={r['broken']:<2} "
              f"illeg={r['illegible_cards']:<2} badges={r['badge_share']:.0%}")
    (DATA / "shortlist_candidates.json").write_text(
        json.dumps([{k: r[k] for k in ("user", "url", "score", "categories", "custom_svgs",
                                        "custom_animated", "theme_switch", "broken",
                                        "illegible_cards", "badge_share", "techniques")}
                    for r in ranked], indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
