#!/usr/bin/env python3
"""Track 3: what does the survey's corpus do about alt text?

    python tools/research/alt_text.py

The harvest recorded every image's URL, size and techniques but never its alt
text, so this re-fetches the READMEs of the surveyed profiles and parses the
images out again — markdown `![alt](src)` and HTML `<img alt="…">` alike.

Writes docs/research/data/alt-text.json.

Judging alt text mechanically is a blunt instrument, so the classes are
deliberately coarse and each is defined by what it can be checked for:

  absent      no alt attribute at all — a screen reader falls back to the URL
  empty       alt="" — correct for decoration, wrong for a card that says things
  filename    the alt is the file or a URL fragment ("banner.svg", "header")
  generic     one or two words from a fixed list ("banner", "image", "gif")
  descriptive anything else — not necessarily good, but at least written

An image is only as accessible as the weakest of these, and a profile is judged
by its non-badge images: a wall of shields with empty alt is correct.
"""
from __future__ import annotations

import concurrent.futures as cf
import json
import re
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "research" / "data" / "alt-text.json"
UA = {"User-Agent": "profile-readme-research (+https://github.com/hammadshakeelai/github-profile-blueprint)"}

MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
HTML_IMG = re.compile(r"<img\b([^>]*)>", re.I)
ATTR = re.compile(r"""(\w[\w-]*)\s*=\s*["']([^"']*)["']""")
GENERIC = {"banner", "image", "img", "picture", "gif", "logo", "icon", "badge", "header",
           "profile", "stats", "card", "svg", "animation", "graph", "photo", "avatar", "typing"}
BADGE_HOST = re.compile(r"shields\.io|badgen|forthebadge|badge\.fury|img\.badgesize", re.I)


def classify(alt: str | None, src: str) -> str:
    if alt is None:
        return "absent"
    a = alt.strip()
    if not a:
        return "empty"
    stem = re.sub(r"[?#].*$", "", src).rsplit("/", 1)[-1]
    if a.lower() in (stem.lower(), stem.rsplit(".", 1)[0].lower()) or re.fullmatch(r"\S+\.(svg|png|gif|jpe?g)", a, re.I):
        return "filename"
    words = [w for w in re.split(r"[\s_-]+", a.lower()) if w.isalpha()]
    if len(words) <= 2 and words and all(w in GENERIC for w in words):
        return "generic"
    return "descriptive"


def images(md: str) -> list[tuple[str | None, str]]:
    """(alt, src) for every image, markdown and HTML."""
    out: list[tuple[str | None, str]] = [(m.group(1), m.group(2)) for m in MD_IMG.finditer(md)]
    for m in HTML_IMG.finditer(md):
        attrs = {k.lower(): v for k, v in ATTR.findall(m.group(1))}
        out.append((attrs.get("alt"), attrs.get("src", "")))
    return out


def readme(user: str) -> str | None:
    for branch in ("main", "master"):
        try:
            req = urllib.request.Request(
                f"https://raw.githubusercontent.com/{user}/{user}/{branch}/README.md", headers=UA)
            return urllib.request.urlopen(req, timeout=20).read(900_000).decode("utf-8", "replace")
        except Exception:
            continue
    return None


def stem_of(url: str) -> str:
    return re.sub(r"[?#].*$", "", url).rsplit("/", 1)[-1].lower()


def text_cards() -> set[str]:
    """URLs the survey measured as SVGs that carry text — the images whose
    content is unreachable if nothing describes them."""
    images = json.loads((ROOT / "docs" / "survey" / "data" / "images.json").read_text(encoding="utf-8"))
    return {stem_of(u) for u, v in images.items()
            if (v.get("svg") or {}).get("has_text") and not BADGE_HOST.search(u)
            and ((v.get("svg") or {}).get("intrinsic_w") or 0) >= 200}


def main() -> None:
    # The same 446 the survey reports on: organisations and dead repos excluded.
    profiles = [p for p in json.loads((ROOT / "docs" / "survey" / "data" / "profiles.json")
                                      .read_text(encoding="utf-8"))
                if p.get("user") and p.get("status") == "live"]
    cohort = {p["user"]: ("curated" if "awesome-github-profile-readme" in (p.get("sources") or [])
                          else "search") for p in profiles}
    users = [p["user"] for p in profiles]
    print(f"re-fetching {len(users)} READMEs")

    per_class: Counter[str] = Counter()
    per_class_badge: Counter[str] = Counter()
    by_cohort: dict[str, Counter[str]] = {"curated": Counter(), "search": Counter()}
    profile_ok: dict[str, Counter[str]] = {"curated": Counter(), "search": Counter()}
    gone = 0
    examples: dict[str, list[str]] = {}
    cards = text_cards()
    card_class: Counter[str] = Counter()

    with cf.ThreadPoolExecutor(8) as ex:
        for user, md in zip(users, ex.map(readme, users)):
            if md is None:
                gone += 1
                continue
            c = cohort[user]
            described = content = 0
            for alt, src in images(md):
                kind = classify(alt, src)
                if BADGE_HOST.search(src):
                    per_class_badge[kind] += 1
                    continue
                per_class[kind] += 1
                # A relative path in the markdown is an absolute raw URL in the
                # survey's image table, so compare by filename.
                if stem_of(src) in cards:
                    card_class[kind] += 1
                by_cohort[c][kind] += 1
                content += 1
                if kind == "descriptive":
                    described += 1
                    if len(examples.setdefault("descriptive", [])) < 8 and len(alt) > 40:
                        examples["descriptive"].append(f"{user}: {alt[:110]}")
            if content:
                profile_ok[c]["all described" if described == content else
                              "none described" if described == 0 else "some described"] += 1

    total = sum(per_class.values())
    data = {"text_cards_by_class": dict(card_class), "profiles": len(users) - gone, "unreachable": gone,
            "content_images": total, "by_class": dict(per_class),
            "badge_images": dict(per_class_badge),
            "by_cohort": {k: dict(v) for k, v in by_cohort.items()},
            "profiles_by_coverage": {k: dict(v) for k, v in profile_ok.items()},
            "examples": examples}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")

    print(f"\n{total} non-badge images across {len(users) - gone} READMEs "
          f"({gone} unreachable)")
    for k in ("absent", "empty", "filename", "generic", "descriptive"):
        print(f"  {k:12} {per_class[k]:6}  {per_class[k] / max(total,1):6.1%}")
    ct = sum(card_class.values())
    print(f"\nof those, {ct} are SVG cards at least 200px wide that carry text —"
          f" the ones whose content is only inside the image:")
    for k in ("absent", "empty", "filename", "generic", "descriptive"):
        print(f"  {k:12} {card_class[k]:6}  {card_class[k] / max(ct,1):6.1%}")

    print(f"\nbadge images (judged separately): {sum(per_class_badge.values())}, "
          f"{per_class_badge['empty'] + per_class_badge['absent']} with no alt text")
    for c in ("curated", "search"):
        t = sum(by_cohort[c].values())
        print(f"  {c:8} {by_cohort[c]['descriptive'] / max(t,1):5.1%} descriptive of {t}")
    print("\nprofiles by coverage:", {c: dict(v) for c, v in profile_ok.items()})


if __name__ == "__main__":
    main()
