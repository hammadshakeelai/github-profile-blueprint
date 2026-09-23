#!/usr/bin/env python3
"""profile-lint — every rule this research measured, run against a real profile.

    python tools/lint/profile_lint.py hammadshakeelai
    python tools/lint/profile_lint.py --file profile/README.md --owner me --repo me
    python tools/lint/profile_lint.py --json torvalds sindresorhus

Fetches the README, resolves and fetches every image, and reports what the six
phases of this repository found worth checking. Each rule names the measurement
behind it, because a linter that can't say why is just an opinion with exit
codes.

Rules, and where they come from:

  broken-image      41% of surveyed profiles have one          docs/survey/FINDINGS.md
  dead-service      the most-copied stat card loads 0%         docs/survey/FINDINGS.md
  phone-illegible   55% of cards are unreadable at 309px       docs/survey/FINDINGS.md
  image-table       21% use tables; cards crush to 76px        docs/survey/FINDINGS.md
  no-theme          80% ship one theme                         docs/survey/FINDINGS.md
  badge-wall        42% are more than half badges              docs/survey/FINDINGS.md
  missing-alt       37.8% of text cards can't be reached       docs/research/ALT-TEXT.md
  dead-motion-guard in-SVG reduced-motion never applies        docs/research/REDUCED-MOTION.md
  unguarded-motion  animation with no still variant            docs/research/REDUCED-MOTION.md
  hidden-first-frame  opacity:0 start renders blank            docs/DIRECTION.md
  stripped-script   <script> in an SVG never runs              docs/CAPABILITY-MATRIX.md
  external-ref      external images are blocked; Chrome draws a broken icon
  webkit-gradient   WebKit never animates gradientTransform    docs/CAPABILITY-MATRIX.md

Exit status is 1 if any error-level rule fired, so it can gate a workflow.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "survey"))
from harvest import (  # noqa: E402
    analyze_image, extract_images, http_get, resolve, svg_metrics,
)

PHONE = 309          # measured README column on a 390px phone
FLOOR = 11.0         # px; below this, supporting text is unreadable
DESKTOP = 846

# Services the survey measured as dead or dying, with their load rates.
DEAD = {
    "github-readme-stats.vercel.app": "0% of its images load (public instance, paused)",
    "activity-graph.herokuapp.com": "2% load",
    "github-readme-activity-graph.vercel.app": "2% load",
    "github-profile-trophy.vercel.app": "11% load",
}
# The survey counts "badges and icons" as one class (analyze.py BADGE_ICON);
# matching that list keeps the badge-wall rule comparable to its 42% figure.
BADGE = re.compile(
    r"shields\.io|badgen\.net|forthebadge|badge\.fury|custom-icon-badges|skillicons\.dev"
    r"|simpleicons\.org|devicon|icons8|iconify|holopin|komarev\.com|visitor-badge"
    r"|moe-counter|count\.getloli|buymeacoff|ko-fi\.com|paypal|githubusercontent\.com/u/"
    r"|cdn\.jsdelivr\.net/(?:gh/)?devicons|go-skill-icons|techstack-generator", re.I)
GENERIC_ALT = {"banner", "image", "img", "picture", "gif", "logo", "icon", "badge", "header",
               "profile", "stats", "card", "svg", "animation", "graph", "photo", "avatar", "typing"}
SEV_ORDER = {"error": 0, "warn": 1, "note": 2}


@dataclass
class Finding:
    rule: str
    severity: str
    subject: str
    detail: str
    why: str


@dataclass
class Report:
    target: str
    findings: list[Finding] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def add(self, *a) -> None:
        self.findings.append(Finding(*a))

    @property
    def errors(self) -> int:
        return sum(1 for f in self.findings if f.severity == "error")


def short(url: str, n: int = 58) -> str:
    u = re.sub(r"^https?://", "", url)
    return u if len(u) <= n else u[: n - 1] + "…"


def alt_class(alt: str | None, src: str) -> str:
    if alt is None:
        return "absent"
    a = alt.strip()
    if not a:
        return "empty"
    stem = re.sub(r"[?#].*$", "", src).rsplit("/", 1)[-1]
    if a.lower() in (stem.lower(), stem.rsplit(".", 1)[0].lower()):
        return "filename"
    words = [w for w in re.split(r"[\s_-]+", a.lower()) if w.isalpha()]
    if len(words) <= 2 and words and all(w in GENERIC_ALT for w in words):
        return "generic"
    return "ok"


MD_IMG = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
HTML_IMG = re.compile(r"<img\b([^>]*)>", re.I)
ATTR = re.compile(r"""(\w[\w-]*)\s*=\s*["']([^"']*)["']""")


def alt_map(md: str) -> dict[str, str]:
    """src (as written) -> alt. extract_images() doesn't keep alt text."""
    out = {m.group(2).split("#")[0]: m.group(1) for m in MD_IMG.finditer(md)}
    for m in HTML_IMG.finditer(md):
        a = {k.lower(): v for k, v in ATTR.findall(m.group(1))}
        if a.get("src"):
            out[a["src"].split("#")[0]] = a.get("alt")
    return out


def check_markdown(md: str, rep: Report, signals: dict | None = None) -> None:
    """Rules that read the README itself."""
    if re.search(r"<table|^\s*\|.*\|.*\|", md, re.M) and len(re.findall(r"!\[|<img", md)) > 1:
        tables = re.findall(r"<table[\s\S]{0,4000}?</table>", md, re.I)
        with_imgs = [t for t in tables if len(re.findall(r"<img", t, re.I)) > 1]
        if with_imgs:
            rep.add("image-table", "error", f"{len(with_imgs)} table(s)",
                    "two or more images inside one table",
                    "on a phone GitHub either crushes the cards — 640px measured at 76px — "
                    "or scrolls the table sideways; 21% of surveyed profiles do this")

    themed = (signals or {}).get("picture_theme") or (signals or {}).get("fragment_theme")
    if not themed:
        rep.add("no-theme", "warn", "whole page", "no dark/light switching found",
                "only 20% of surveyed profiles switch; two files behind <picture> is verified "
                "working in Chromium, Firefox and WebKit")


def check_svg(url: str, body: str, alt: str | None, rep: Report) -> dict:
    """Rules that read a committed SVG's source. Returns its metrics."""
    m = svg_metrics(body) or {}
    name = short(url)

    if re.search(r"<script\b", body, re.I):
        rep.add("stripped-script", "error", name, "<script> inside the SVG",
                "blocked in all three engines — secure animated mode; the effort is wasted")

    if re.search(r'<(?:image|use)\b[^>]*href\s*=\s*["\']https?://', body, re.I):
        rep.add("external-ref", "error", name, "references an external image",
                "blocked everywhere; Chromium paints a broken-image icon into the design")

    if re.search(r"@import\b", body, re.I):
        rep.add("external-ref", "warn", name, "@import in the SVG's CSS",
                "external stylesheets and fonts never load inside an image")

    if re.search(r"prefers-reduced-motion", body, re.I):
        rep.add("dead-motion-guard", "warn", name,
                "guards animation with prefers-reduced-motion inside the SVG",
                "that query never applies inside an image — verified in all three engines. "
                "Gate a <picture> source on it instead (docs/research/REDUCED-MOTION.md)")

    if re.search(r'attributeName\s*=\s*["\']gradientTransform', body, re.I):
        rep.add("webkit-gradient", "warn", name, "animates gradientTransform",
                "WebKit never animates it; animate x1/x2 or the stop offsets instead")

    # Something that starts invisible and fades in shows nothing to a static
    # renderer — and was caught doing exactly that at phone width in this repo.
    if re.search(r'opacity\s*=\s*["\']0["\']', body) and re.search(r"<animate|@keyframes", body, re.I):
        rep.add("hidden-first-frame", "warn", name, "elements start at opacity 0 and animate in",
                "the first frame is what a screenshot, a cached thumbnail or a paused tab shows")

    if m.get("has_text") and alt_class(alt, url) != "ok":
        rep.add("missing-alt", "error", name,
                f"carries text but its alt is {alt_class(alt, url)}",
                "nothing inside an SVG reaches the accessibility tree — title, desc, aria-label "
                "and role are all invisible to the host page. 37.8% of surveyed text cards "
                "fail this (docs/research/ALT-TEXT.md)")
    return m


def check_size(url: str, m: dict, declared_w: float | None, rep: Report) -> None:
    """The legibility formula, applied at the measured phone column."""
    vb, small = m.get("vb_w"), m.get("min_font")
    if not (vb and small):
        return
    natural = declared_w or m.get("intrinsic_w") or vb
    rendered = min(natural, PHONE)
    eff = small * (rendered / vb)
    if eff < FLOOR:
        biggest = (m.get("max_font") or small) * (rendered / vb)
        sev = "error" if biggest < FLOOR else "warn"
        what = "its largest text" if biggest < FLOOR else "its smallest text"
        rep.add("phone-illegible", sev, short(url),
                f"{what} renders at {(biggest if biggest < FLOOR else eff):.1f}px on a phone "
                f"(viewBox {vb:.0f}, font {small:.0f})",
                f"the README column is {PHONE}px on a 390px phone; 55% of surveyed cards fail "
                f"this and 90% of those are legible at full size")


def lint(target: str, md: str, owner: str, repo: str, branch: str,
         workers: int = 8) -> Report:
    rep = Report(target)

    occurrences, signals = extract_images(md, owner, repo, branch)
    alts = alt_map(md)

    # One <picture> yields several occurrences of the same card — its <source>
    # variants plus the <img>. Fetch and report each file once, and take alt
    # text from the <img>, which is the only element that carries it.
    imgs: list[dict] = []
    seen: dict[str, dict] = {}
    for o in occurrences:
        o["alt"] = alts.get(o.get("raw") or "", alts.get(o.get("url") or ""))
        prev = seen.get(o["url"])
        if prev is None:
            seen[o["url"]] = o
            imgs.append(o)
        elif o.get("via") in ("img", "markdown") and prev.get("via") == "source":
            prev.update(o)
    # A themed pair (foo-dark.svg / foo-light.svg) shares one <img alt>; carry it
    # to the variants so they aren't reported as undescribed.
    for o in imgs:
        if o.get("via") == "source" and o.get("alt") is None:
            stem = re.sub(r"[-_](dark|light|still)", "", Path(o["url"]).stem, flags=re.I)
            for c in imgs:
                if c.get("via") in ("img", "markdown") and c.get("alt") and                    re.sub(r"[-_](dark|light|still)", "", Path(c["url"]).stem, flags=re.I) == stem:
                    o["alt"] = c["alt"]
                    break
    check_markdown(md, rep, signals)

    if not imgs:
        rep.stats = {"images": 0}
        return rep

    badges = sum(1 for i in imgs if BADGE.search(i.get("url") or ""))
    if badges > len(imgs) / 2 and badges >= 5:
        rep.add("badge-wall", "warn", f"{badges} of {len(imgs)} images",
                "more than half the images are badges",
                "42% of surveyed profiles are badge walls; none is more legible for it")

    for i in imgs:
        for host, rate in DEAD.items():
            if host in (i.get("url") or ""):
                rep.add("dead-service", "error", short(i["url"]),
                        f"hosted by a service the survey measured as dead — {rate}",
                        "free-tier deployments being switched off is the single biggest cause "
                        "of broken profile images; generate and commit instead")

    def one(i: dict) -> tuple[dict, dict]:
        return i, analyze_image(i["url"])

    with cf.ThreadPoolExecutor(workers) as ex:
        results = list(ex.map(one, imgs))

    svg_bodies: list[tuple[dict, str]] = []
    for i, res in results:
        if not res.get("ok"):
            rep.add("broken-image", "error", short(i["url"]),
                    f"does not load ({res.get('status') or res.get('fail_reason') or 'no response'})",
                    "41% of surveyed profiles show at least one broken image")
            continue
        if not res.get("is_svg"):
            continue
        m = res.get("svg") or {}
        # Badges and icons are excluded, as the survey excludes them: shields'
        # for-the-badge style sets 10px text on every device, so measuring them
        # would flag every profile that uses one and say nothing about design.
        if m and not BADGE.search(i.get("url") or ""):
            check_size(i["url"], m, i.get("width"), rep)
        # Only fetch the body for the profile's own committed SVGs: a service's
        # output isn't the author's to fix, and there can be hundreds of badges.
        if i.get("kind") == "committed":
            body = get_text(i["url"], accept="image/svg+xml")
            if body:
                svg_bodies.append((i, body))

    animated_unguarded = []
    for i, body in svg_bodies:
        m = check_svg(i["url"], body, i.get("alt"), rep)
        if (m or {}).get("animated") and "prefers-reduced-motion" not in md:
            animated_unguarded.append(i["url"])
    if animated_unguarded:
        rep.add("unguarded-motion", "note", f"{len(animated_unguarded)} animated file(s)",
                "nothing offers a still alternative",
                "a viewer who asked their OS for less motion has no way to get it; gate a "
                "<picture> source on prefers-reduced-motion, or design so the still frame is "
                "the whole composition")

    alts = Counter(alt_class(i.get("alt"), i.get("url") or "") for i, _ in results
                   if not BADGE.search(i.get("url") or ""))
    del occurrences
    rep.stats = {"images": len(imgs), "badges": badges,
                 "broken": sum(1 for _, r in results if not r.get("ok")),
                 "alt": dict(alts)}
    return rep


def get_text(url: str, accept: str = "*/*") -> str | None:
    r = http_get(url, accept=accept)
    if r and r.get("status") == 200 and r.get("body"):
        return r["body"].decode("utf-8", "replace")
    return None


def fetch_readme(user: str) -> tuple[str, str] | None:
    for branch in ("main", "master"):
        md = get_text(f"https://raw.githubusercontent.com/{user}/{user}/{branch}/README.md")
        if md:
            return md, branch
    return None


def render(rep: Report) -> str:
    out = [f"\n{rep.target}", "=" * len(rep.target)]
    if not rep.findings:
        out.append("  clean — every rule passed")
    for f in sorted(rep.findings, key=lambda f: (SEV_ORDER[f.severity], f.rule)):
        mark = {"error": "ERROR", "warn": "warn ", "note": "note "}[f.severity]
        out += [f"  {mark} [{f.rule}] {f.subject}", f"        {f.detail}", f"        why: {f.why}"]
    s = rep.stats
    if s.get("images"):
        out.append(f"\n  {s['images']} images, {s['badges']} badges, {s['broken']} broken; "
                   f"alt: {s.get('alt', {})}")
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser(description="Lint a GitHub profile README against measured rules.")
    ap.add_argument("users", nargs="*", help="GitHub usernames (their username/username repo)")
    ap.add_argument("--file", type=Path, help="lint a local README instead")
    ap.add_argument("--owner", default="OWNER"), ap.add_argument("--repo", default="REPO")
    ap.add_argument("--branch", default="main")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    reports = []
    if a.file:
        reports.append(lint(str(a.file), a.file.read_text(encoding="utf-8"),
                            a.owner, a.repo, a.branch))
    for user in a.users:
        got = fetch_readme(user)
        if not got:
            print(f"{user}: no README found at {user}/{user}", file=sys.stderr)
            continue
        md, branch = got
        reports.append(lint(user, md, user, user, branch))

    if a.json:
        print(json.dumps([{"target": r.target, "stats": r.stats,
                           "findings": [vars(f) for f in r.findings]} for r in reports], indent=1))
    else:
        for r in reports:
            print(render(r))
    sys.exit(1 if any(r.errors for r in reports) else 0)


if __name__ == "__main__":
    main()
