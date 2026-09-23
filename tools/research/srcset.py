#!/usr/bin/env python3
"""Track 1: did relative <picture><source srcset> paths resolve on profile pages?

    python tools/research/srcset.py

Read-only. Cross-references what each profile's markdown declared
(docs/survey/data/profiles.json) against what the browser actually loaded on the
live profile page (docs/survey/data/layout.json, captured in the dark scheme).

A <picture> whose dark <source> resolves serves that source's file. If a
relative srcset failed to resolve, the browser would fall back to the <img> src
instead — a different URL, which the layout capture would show.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "survey" / "data"


def resolve(user: str, branch: str, raw: str) -> str:
    """The URL GitHub rewrites a repo-relative markdown path to."""
    base = f"https://raw.githubusercontent.com/{user}/{user}/{branch or 'main'}/"
    return urljoin(base, raw.lstrip("./"))


def key(url: str) -> str:
    """Compare by filename: GitHub serves the same file from several hostnames."""
    return re.sub(r"[?#].*$", "", url).rsplit("/", 1)[-1].lower()


def main() -> None:
    profiles = {p["user"]: p for p in json.loads((DATA / "profiles.json").read_text(encoding="utf-8"))
                if p.get("user")}
    layout = json.loads((DATA / "layout.json").read_text(encoding="utf-8"))

    tested = resolved = fellback = 0
    unclear = 0
    examples: list[str] = []
    for user, pages in layout.items():
        prof = profiles.get(user)
        page = (pages or {}).get("1280") or {}
        if not prof or not page.get("images"):
            continue
        # The dark <source> of each <picture> written with a relative srcset.
        # Only sources gated purely on the colour scheme: a source that also
        # carries a width condition legitimately doesn't load at 1280px, and
        # counting it as a failure was a bug in the first run of this script.
        dark = [im for im in prof.get("images") or []
                if im.get("via") == "source"
                and "dark" in (im.get("media") or "")
                and "width" not in (im.get("media") or "")
                and not (im.get("raw") or "").startswith(("http", "data:"))]
        if not dark:
            continue
        loaded = {key(i["canonical"]) for i in page["images"] if i.get("canonical")}
        for im in dark:
            want = key(resolve(user, prof.get("branch"), im["raw"]))
            tested += 1
            if want in loaded:
                resolved += 1
            elif any(want.replace("-dark", "").replace("_dark", "") == l.replace("-light", "").replace("_light", "")
                     for l in loaded):
                fellback += 1
                if len(examples) < 6:
                    examples.append(f"{user}: declared {im['raw']} — page loaded a different variant")
            else:
                unclear += 1

    def has_rel(u: str) -> bool:
        pr = profiles.get(u)
        return bool(pr) and any(
            i.get("via") == "source" and "dark" in (i.get("media") or "")
            and "width" not in (i.get("media") or "")
            and not (i.get("raw") or "").startswith(("http", "data:"))
            for i in pr.get("images") or [])

    print(f"profiles with a relative dark <source>: {sum(1 for u in layout if has_rel(u))}")
    print(f"relative dark <source> entries tested : {tested}")
    print(f"  the declared file was what loaded   : {resolved}  ({resolved / max(tested,1):.0%})")
    print(f"  fell back to the other variant      : {fellback}")
    print(f"  neither (image broken or renamed)   : {unclear}")
    for e in examples:
        print("   ", e)


if __name__ == "__main__":
    main()
