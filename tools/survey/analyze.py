#!/usr/bin/env python3
"""Turn harvested survey data into tables and summary statistics.

    python tools/survey/analyze.py            # write PROFILES.md, GENERATORS.md, data/summary.json
    python tools/survey/analyze.py --hosts    # list the most-used hosts not yet classified

Reads docs/survey/data/{profiles,images}.json produced by harvest.py.
"""
from __future__ import annotations

import argparse
import collections
import json
import statistics
import sys
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "survey" / "data"
SURVEY = ROOT / "docs" / "survey"
LEGIBLE_PX = 11.0

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# --------------------------------------------------------------------------- #
# Generator classification — built from the observed host list (--hosts)
# --------------------------------------------------------------------------- #

def _q(query: str) -> dict:
    return {k.lower(): v for k, v in urllib.parse.parse_qsl(query)}


# (name, source repository, predicate on (host, path, query, kind))
GENERATORS: list[tuple[str, str, callable]] = [
    ("github-readme-stats — public instance", "anuraghazra/github-readme-stats",
     lambda h, p, q, k: h == "github-readme-stats.vercel.app"),
    ("github-readme-stats — self-hosted", "anuraghazra/github-readme-stats",
     lambda h, p, q, k: h.endswith(".vercel.app") and h != "github-readme-stats.vercel.app"
     and (p.startswith(("/api/top-langs", "/api/pin", "/api/wakatime", "/api/gist"))
          or (p.rstrip("/") == "/api" and "username" in _q(q)))),
    ("github-readme-streak-stats", "DenverCoder1/github-readme-streak-stats",
     lambda h, p, q, k: "streak-stats" in h or "streak" in h and "github" in h),
    ("readme-typing-svg", "DenverCoder1/readme-typing-svg",
     lambda h, p, q, k: "readme-typing-svg" in h),
    ("github-profile-trophy", "ryo-ma/github-profile-trophy",
     lambda h, p, q, k: "github-profile-trophy" in h or "trophy" in h),
    ("github-readme-activity-graph", "Ashutosh00710/github-readme-activity-graph",
     lambda h, p, q, k: "activity-graph" in h),
    ("github-profile-summary-cards", "vn7n24fzkq/github-profile-summary-cards",
     lambda h, p, q, k: "profile-summary-cards" in h or "github-profile-summary-cards" in p),
    ("profile views counter (komarev)", "antonkomarev/github-profile-views-counter",
     lambda h, p, q, k: h in ("komarev.com", "www.komarev.com")),
    ("visitor badge", "various",
     lambda h, p, q, k: "visitor-badge" in h or h in ("api.visitorbadge.io", "visitor-badge.laobi.icu",
                                                      "hits.seeyoufarm.com", "hits.sh", "profile-counter.glitch.me",
                                                      "badges.pufler.dev", "hit.yhype.me", "views.whatilearened.today",
                                                      "gpvc.arturio.dev")),
    ("moe-counter", "journey-ad/Moe-Counter",
     lambda h, p, q, k: "getloli" in h or "moe-counter" in h),
    ("shields.io badges", "badges/shields",
     lambda h, p, q, k: h in ("img.shields.io", "shields.io", "badgen.net", "flat.badgen.net")),
    ("skill-icons", "tandpfun/skill-icons",
     lambda h, p, q, k: h == "skillicons.dev"),
    ("devicon", "devicons/devicon",
     lambda h, p, q, k: "devicon" in p.lower()),
    ("simple-icons", "simple-icons/simple-icons",
     lambda h, p, q, k: "simpleicons" in h or "simple-icons" in p.lower()),
    ("capsule-render", "kyechan99/capsule-render",
     lambda h, p, q, k: "capsule-render" in h),
    ("snk contribution snake", "Platane/snk",
     lambda h, p, q, k: "snake" in p.lower()),
    ("lowlighter/metrics", "lowlighter/metrics",
     lambda h, p, q, k: "metrics" in p.lower() and p.lower().endswith(".svg")),
    ("wakatime", "wakatime / athul/waka-readme",
     lambda h, p, q, k: "wakatime" in h),
    ("spotify now-playing", "novatorem/novatorem & kittinan/spotify-github-profile",
     lambda h, p, q, k: "spotify" in h or "novatorem" in h),
    ("readme-jokes / quotes", "various",
     lambda h, p, q, k: any(s in h for s in ("readme-jokes", "quotes", "jokes"))),
    ("contribution chart (ghchart)", "2016rshah/githubchart-api",
     lambda h, p, q, k: h == "ghchart.rshah.org"),
    ("lowlighter/metrics — hosted", "lowlighter/metrics",
     lambda h, p, q, k: h == "metrics.lecoq.io"),
    ("github-profile-trophy — forks", "ryo-ma/github-profile-trophy",
     lambda h, p, q, k: "trophies" in h),
    ("stackoverflow cards", "various",
     lambda h, p, q, k: "stackoverflow" in h),
    ("demolab badges & cards", "DenverCoder1 (demolab.com)",
     lambda h, p, q, k: h.endswith("demolab.com")),
    ("holopin badges", "holopin.io", lambda h, p, q, k: "holopin" in h),
    ("icon CDNs", "icons8 / vectorlogo.zone / iconify / wikimedia / flaticon",
     lambda h, p, q, k: h in ("img.icons8.com", "www.vectorlogo.zone", "cdn.worldvectorlogo.com",
                              "api.iconify.design", "upload.wikimedia.org", "image.flaticon.com")),
    ("GitHub avatars", "—", lambda h, p, q, k: h.startswith("avatars") and h.endswith("githubusercontent.com")),
    ("donation buttons", "buymeacoffee / ko-fi",
     lambda h, p, q, k: "buymeacoffee" in h or "ko-fi" in h),
    ("emoji GIFs", "slackmojis / partyparrot",
     lambda h, p, q, k: h in ("emojis.slackmojis.com", "cultofthepartyparrot.com")),
    ("other users' repos (raw assets)", "—",
     lambda h, p, q, k: k == "third-party" and h in ("raw.githubusercontent.com", "github.com")),
    ("giphy", "—", lambda h, p, q, k: "giphy.com" in h),
    ("imgur", "—", lambda h, p, q, k: "imgur.com" in h),
    ("tenor", "—", lambda h, p, q, k: "tenor.com" in h),
    ("GitHub upload (user-attachments)", "—", lambda h, p, q, k: k == "gh-upload"),
]


def classify(url: str, kind: str) -> str | None:
    if not url:
        return None
    sp = urllib.parse.urlsplit(url)
    h, p, q = sp.netloc.lower(), sp.path, sp.query
    for name, _, pred in GENERATORS:
        try:
            if pred(h, p, q, kind):
                return name
        except Exception:
            continue
    return None


REPO_OF = {name: repo for name, repo, _ in GENERATORS}

# Tiny, templated images. Their SVG markup (shields.io alone is ~70% of every SVG
# fetched) carries filters, clip-paths and embedded logos from one template, so
# counting techniques across them measures the template, not anyone's design.
BADGE_ICON = {"shields.io badges", "devicon", "simple-icons", "icon CDNs", "skill-icons",
              "demolab badges & cards", "visitor badge", "profile views counter (komarev)",
              "moe-counter", "holopin badges", "GitHub avatars", "donation buttons"}


def svg_origin(url: str, kind: str) -> str:
    """'custom' (committed, or a personal host), 'badge-icon', or 'service'."""
    g = classify(url, kind)
    if kind == "committed" or g is None:
        return "custom"
    return "badge-icon" if g in BADGE_ICON else "service"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def load() -> tuple[list[dict], dict]:
    profiles = json.loads((DATA / "profiles.json").read_text(encoding="utf-8"))
    images = json.loads((DATA / "images.json").read_text(encoding="utf-8"))
    return profiles, images


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.0f}%" if d else "—"


def displayed(p: dict) -> list[dict]:
    """Occurrences that are actually displayed (<source> variants excluded)."""
    return [o for o in p.get("images", []) if o["via"] != "source" and o.get("url")]


def months_since(iso: str | None) -> float | None:
    if not iso:
        return None
    t = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - t).days / 30.44


# --------------------------------------------------------------------------- #
# Per-profile row
# --------------------------------------------------------------------------- #

def profile_row(p: dict, images: dict) -> dict:
    occ = displayed(p)
    imgs = [images.get(o["url"], {}) for o in occ]
    gens = collections.Counter(filter(None, (classify(o["url"], o["kind"]) for o in occ)))
    svg_occ = [(o, i) for o, i in zip(occ, imgs) if i.get("is_svg")]
    custom = [(o, i) for o, i in svg_occ if svg_origin(o["url"], o["kind"]) == "custom"]
    # Techniques from custom SVGs only — badge templates would otherwise tag
    # nearly every profile with filter/clip-path/blur.
    techniques = sorted({t for _, i in custom for t in i.get("svg", {}).get("techniques", [])})
    badge_share = (sum(classify(o["url"], o["kind"]) in BADGE_ICON for o in occ) / len(occ)) if occ else 0.0
    mob = [o.get("mobile_px") for o in occ if o.get("mobile_px") is not None]
    mob_best = [o.get("mobile_best_px") for o in occ if o.get("mobile_best_px") is not None]
    sig = p.get("signals", {})
    theme = "picture" if sig.get("picture_theme") else "fragment" if sig.get("fragment_theme") else "none"
    return {
        "user": p.get("owner", p["user"]), "url": p.get("url", f"https://github.com/{p['user']}"),
        "categories": p.get("categories", []), "status": p["status"],
        "pushed_at": p.get("pushed_at"), "workflows": p.get("workflows", 0),
        "images": len(occ),
        "committed": sum(o["kind"] == "committed" for o in occ),
        "gh_upload": sum(o["kind"] == "gh-upload" for o in occ),
        "third_party": sum(o["kind"] == "third-party" for o in occ),
        "generators": dict(gens.most_common()),
        "svgs": len(svg_occ),
        "animated_svgs": sum(bool(i.get("svg", {}).get("animated")) for _, i in svg_occ),
        "custom_svgs": len(custom),
        "custom_animated": sum(bool(i.get("svg", {}).get("animated")) for _, i in custom),
        "badge_share": round(badge_share, 2),
        "techniques": techniques,
        "theme_switch": theme,
        "gifs": sum(bool(i.get("is_gif")) for i in imgs),
        "broken": sum(not i.get("ok", False) for i in imgs),
        "illegible_cards": sum(1 for o in occ
                               if o.get("mobile_best_px") is not None and o["mobile_best_px"] < LEGIBLE_PX),
        "mobile_worst_px": min(mob) if mob else None,
        "mobile_best_px_min": min(mob_best) if mob_best else None,
    }


# --------------------------------------------------------------------------- #
# Outputs
# --------------------------------------------------------------------------- #

def write_profiles_md(rows: list[dict]) -> None:
    live = [r for r in rows if r["status"] == "live"]
    lines = [
        "# Profiles",
        "",
        f"{len(rows)} candidates, {len(live)} live. Generated by `tools/survey/analyze.py` — "
        "do not edit by hand.",
        "",
        "Column key: **img** displayed images · **own/up/3rd** committed to the user's repos / "
        "uploaded to GitHub / third-party host · **svg (anim)** SVGs and how many animate · "
        "**theme** dark/light switching · **brk** images that failed to load · **wf** Actions "
        "workflows · **illeg** cards whose *largest* text is under 11px on a phone · "
        "**min px** smallest text on a phone.",
        "",
        "| Profile | Category | Pushed | img | own/up/3rd | Generators | svg (anim) | theme | brk | wf | illeg | min px |",
        "|---|---|---|--:|---|---|---|---|--:|--:|--:|--:|",
    ]
    for r in sorted(rows, key=lambda r: (r["status"] != "live", r["user"].lower())):
        if r["status"] != "live":
            lines.append(f"| [{r['user']}]({r['url']}) | {', '.join(r['categories'][:1])} | "
                         f"— | | | *{r['status']}* | | | | | | |")
            continue
        gens = ", ".join(g.split(" — ")[0].split(" (")[0] for g in list(r["generators"])[:3]) or "—"
        pushed = (r["pushed_at"] or "")[:7]
        mp = f"{r['mobile_worst_px']:.1f}" if r["mobile_worst_px"] is not None else "—"
        lines.append(
            f"| [{r['user']}]({r['url']}) | {', '.join(r['categories'][:1])} | {pushed} | {r['images']} | "
            f"{r['committed']}/{r['gh_upload']}/{r['third_party']} | {gens} | "
            f"{r['svgs']} ({r['animated_svgs']}) | {r['theme_switch']} | {r['broken'] or ''} | "
            f"{r['workflows'] or ''} | {r['illegible_cards'] or ''} | {mp} |")
    (SURVEY / "PROFILES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def generator_stats(profiles: list[dict], images: dict) -> list[dict]:
    by: dict[str, dict] = {}
    for p in profiles:
        for o in displayed(p):
            g = classify(o["url"], o["kind"])
            if not g:
                continue
            s = by.setdefault(g, {"generator": g, "repo": REPO_OF.get(g, "—"), "users": set(),
                                  "urls": set(), "best_px": []})
            s["users"].add(p.get("owner", p["user"]))
            s["urls"].add(o["url"])
            if o.get("mobile_best_px") is not None:
                s["best_px"].append(o["mobile_best_px"])
    out = []
    for g, s in by.items():
        res = [images[u] for u in s["urls"] if u in images]
        ok = sum(r.get("ok", False) for r in res)
        reasons = collections.Counter(r.get("fail_reason") for r in res if not r.get("ok"))
        ms = [r["ms"] for r in res if r.get("ms")]
        bp = s["best_px"]
        out.append({
            "generator": g, "repo": s["repo"], "profiles": len(s["users"]),
            "requests": len(res), "ok": ok,
            "fail_reasons": dict(reasons.most_common()),
            "median_ms": round(statistics.median(ms)) if ms else None,
            "illegible_share": (sum(x < LEGIBLE_PX for x in bp) / len(bp)) if bp else None,
            "median_best_px": round(statistics.median(bp), 1) if bp else None,
        })
    return sorted(out, key=lambda r: (-r["profiles"], r["generator"]))


def write_generators_md(gens: list[dict]) -> None:
    lines = [
        "# Generators",
        "",
        "Every image service seen in the surveyed profiles, ranked by how many profiles use it. "
        "Generated by `tools/survey/analyze.py` — do not edit by hand.",
        "",
        "**live** is the share of distinct image URLs that returned a usable image when fetched. "
        "**illegible on phone** is the share of its cards whose *largest* text renders under 11px "
        "in the 309px mobile container.",
        "",
        "| Generator | Source | Profiles | URLs | Live | Main failure | Median ms | Illegible on phone |",
        "|---|---|--:|--:|--:|---|--:|--:|",
    ]
    for g in gens:
        fail = ", ".join(f"{k} ×{v}" for k, v in list(g["fail_reasons"].items())[:2]) or "—"
        ill = f"{100 * g['illegible_share']:.0f}%" if g["illegible_share"] is not None else "—"
        repo = f"[{g['repo']}](https://github.com/{g['repo']})" if "/" in g["repo"] and " " not in g["repo"] else g["repo"]
        lines.append(f"| {g['generator']} | {repo} | {g['profiles']} | {g['requests']} | "
                     f"{pct(g['ok'], g['requests'])} | {fail} | {g['median_ms'] or '—'} | {ill} |")
    (SURVEY / "GENERATORS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def summary(profiles: list[dict], images: dict, rows: list[dict], gens: list[dict]) -> dict:
    live = [p for p in profiles if p["status"] == "live"]
    lrows = [r for r in rows if r["status"] == "live"]
    occ = [o for p in live for o in displayed(p)]
    res = {o["url"]: images.get(o["url"], {}) for o in occ}
    svgs = {u: r for u, r in res.items() if r.get("is_svg")}
    kind_of = {}
    for o in occ:
        kind_of.setdefault(o["url"], o["kind"])
    origin = {u: svg_origin(u, kind_of[u]) for u in svgs}

    def techs(which: str) -> dict:
        c = collections.Counter(t for u, r in svgs.items() if origin[u] == which
                                for t in r.get("svg", {}).get("techniques", []))
        return dict(c.most_common())

    tech = collections.Counter(t for r in svgs.values() for t in r.get("svg", {}).get("techniques", []))
    age = [months_since(p.get("pushed_at")) for p in live]
    age = [a for a in age if a is not None]
    kinds = collections.Counter(o["kind"] for o in occ)
    broken_by_kind = collections.Counter(o["kind"] for o in occ if not res[o["url"]].get("ok"))
    reasons = collections.Counter(r.get("fail_reason") for r in res.values() if not r.get("ok"))
    text_slots = [o for o in occ if o.get("mobile_best_px") is not None]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "candidates": len(profiles),
        "status": dict(collections.Counter(p["status"] for p in profiles)),
        "pushed_within_12mo": sum(a <= 12 for a in age), "pushed_over_36mo_ago": sum(a > 36 for a in age),
        "median_months_since_push": round(statistics.median(age), 1) if age else None,
        "displayed_images": len(occ), "distinct_image_urls": len(res),
        "image_kinds": dict(kinds), "broken_occurrences_by_kind": dict(broken_by_kind),
        "broken_occurrences": sum(broken_by_kind.values()),
        "profiles_with_broken": sum(r["broken"] > 0 for r in lrows),
        "fail_reasons_distinct_urls": dict(reasons.most_common()),
        "distinct_svgs": len(svgs),
        "animated_svgs": sum(bool(r.get("svg", {}).get("animated")) for r in svgs.values()),
        "svg_techniques_all": dict(tech.most_common()),
        "svg_origin_counts": dict(collections.Counter(origin.values())),
        "svg_techniques_custom": techs("custom"),
        "svg_techniques_services": techs("service"),
        "custom_svgs_animated": sum(bool(svgs[u].get("svg", {}).get("animated"))
                                    for u in svgs if origin[u] == "custom"),
        "theme_switch": dict(collections.Counter(r["theme_switch"] for r in lrows)),
        "profiles_with_workflows": sum(r["workflows"] > 0 for r in lrows),
        "profiles_with_gifs": sum(r["gifs"] > 0 for r in lrows),
        "text_card_slots": len(text_slots),
        "slots_fully_illegible_mobile": sum(o["mobile_best_px"] < LEGIBLE_PX for o in text_slots),
        "slots_some_illegible_mobile": sum(o["mobile_px"] < LEGIBLE_PX for o in text_slots
                                           if o.get("mobile_px") is not None),
        "slots_some_illegible_desktop": sum(o["desktop_px"] < LEGIBLE_PX for o in text_slots
                                            if o.get("desktop_px") is not None),
        "profiles_with_illegible_card": sum(r["illegible_cards"] > 0 for r in lrows),
        "top_generators": [(g["generator"], g["profiles"], pct(g["ok"], g["requests"])) for g in gens[:15]],
    }


def unclassified_hosts(profiles: list[dict]) -> None:
    c = collections.defaultdict(set)
    for p in profiles:
        for o in displayed(p):
            if classify(o["url"], o["kind"]) is None and o["kind"] == "third-party":
                c[urllib.parse.urlsplit(o["url"]).netloc.lower()].add(p.get("owner", p["user"]))
    for host, users in sorted(c.items(), key=lambda kv: -len(kv[1]))[:40]:
        print(f"{len(users):4d}  {host}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hosts", action="store_true")
    a = ap.parse_args()
    profiles, images = load()
    if a.hosts:
        unclassified_hosts(profiles)
        return
    rows = [profile_row(p, images) for p in profiles]
    gens = generator_stats([p for p in profiles if p["status"] == "live"], images)
    write_profiles_md(rows)
    write_generators_md(gens)
    s = summary(profiles, images, rows, gens)
    (DATA / "summary.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
    (DATA / "rows.json").write_text(json.dumps(rows, indent=1, sort_keys=True), encoding="utf-8")
    print(json.dumps(s, indent=1))


if __name__ == "__main__":
    main()
