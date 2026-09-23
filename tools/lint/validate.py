#!/usr/bin/env python3
"""Check profile-lint against the survey it was derived from.

    python tools/lint/validate.py --n 80

A linter whose rules came from a 446-profile survey should, run over profiles
from that survey, report roughly the rates the survey reported. Where it
doesn't, either the rule is wrong or the survey is — and both are worth knowing.

Samples profiles at random (fixed seed), lints each one live, and prints its
rates beside the survey's. Writes docs/research/data/lint-validation.json.

The two are not measuring identically and are not expected to match exactly:
the survey rendered each profile in a real browser, while the linter reads the
markdown and the files. Differences are reported, not smoothed.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "lint"))
from profile_lint import fetch_readme, lint  # noqa: E402

OUT = ROOT / "docs" / "research" / "data" / "lint-validation.json"

# What the survey reported, for comparison. docs/survey/FINDINGS.md.
SURVEY = {
    "broken-image": ("41% of profiles show at least one broken image", 0.41),
    "badge-wall": ("42% are more than half badges", 0.42),
    "no-theme": ("80% don't switch dark/light", 0.80),
    "image-table": ("21% put two or more images in a table", 0.21),
    # The survey's headline counts a card as illegible when its LARGEST text
    # falls below the floor, which is the linter's error level. The linter also
    # warns when only some text does, so the two are reported separately.
    "phone-illegible!error": ("15% curated / 70% search have a card whose largest text "
                              "is under 11px", None),
    "phone-illegible": ("any text below the floor — warn level, no survey equivalent", None),
}


def one(user: str) -> tuple[str, set[str], dict] | None:
    """Rules fired; an error-level firing is also recorded as "<rule>!error"."""
    got = fetch_readme(user)
    if not got:
        return None
    md, branch = got
    rep = lint(user, md, user, user, branch, workers=4)
    rules = {f.rule for f in rep.findings}
    rules |= {f"{f.rule}!error" for f in rep.findings if f.severity == "error"}
    return user, rules, rep.stats


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=80)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()

    profiles = [p for p in json.loads((ROOT / "docs" / "survey" / "data" / "profiles.json")
                                      .read_text(encoding="utf-8"))
                if p.get("status") == "live" and p.get("user")]
    rng = random.Random(20260923)
    sample = rng.sample(profiles, min(a.n, len(profiles)))
    users = [p["user"] for p in sample]
    cohort = {p["user"]: ("curated" if "awesome-github-profile-readme" in (p.get("sources") or [])
                          else "search") for p in sample}
    print(f"linting {len(users)} profiles from the survey sample")

    fired: Counter[str] = Counter()
    by_cohort: dict[str, Counter[str]] = {"curated": Counter(), "search": Counter()}
    seen = 0
    rows = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for res in ex.map(one, users):
            if not res:
                continue
            user, rules, stats = res
            seen += 1
            for r in rules:
                fired[r] += 1
                by_cohort[cohort[user]][r] += 1
            rows.append({"user": user, "cohort": cohort[user],
                         "rules": sorted(rules), "stats": stats})
            print(".", end="", flush=True)

    print(f"\n\n{seen} profiles linted\n")
    print(f"{'rule':20} {'lint':>8}   survey")
    for rule, (text, expect) in SURVEY.items():
        got = fired[rule] / max(seen, 1)
        note = f"{expect:.0%} — {text}" if expect is not None else text
        print(f"{rule:20} {got:7.0%}   {note}")
    print("\nother rules fired:")
    for rule, n in sorted(fired.items()):
        if rule not in SURVEY:
            print(f"  {rule:20} {n / max(seen,1):6.0%}  ({n} profiles)")
    print("\nby cohort (curated / search):")
    cn = {c: sum(1 for u in users if cohort[u] == c) for c in ("curated", "search")}
    for rule in sorted(fired):
        print(f"  {rule:20} {by_cohort['curated'][rule] / max(cn['curated'],1):5.0%} / "
              f"{by_cohort['search'][rule] / max(cn['search'],1):5.0%}")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"sampled": seen, "fired": dict(fired),
                               "by_cohort": {k: dict(v) for k, v in by_cohort.items()},
                               "cohort_sizes": cn, "rows": rows}, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
