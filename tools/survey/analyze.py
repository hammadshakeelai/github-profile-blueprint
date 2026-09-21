#!/usr/bin/env python3
"""Turn harvested survey data into tables and summary statistics.

    python tools/survey/analyze.py            # write PROFILES.md, GENERATORS.md, data/summary.json
    python tools/survey/analyze.py --hosts    # list the most-used hosts not yet classified

Reads docs/survey/data/{profiles,images}.json produced by harvest.py.
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import re
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
     lambda h, p, q, k: h.endswith("demolab.com") or "custom-icon-badges" in h),
    ("leetcode cards", "JacobLinCool/LeetCode-Stats-Card",
     lambda h, p, q, k: "leetcard" in h or "leetcode-stats" in h),
    ("techstack-generator", "various", lambda h, p, q, k: "techstack-generator" in h),
    ("committers.top badge", "gayanvoice/top-github-users", lambda h, p, q, k: "committers.top" in h),
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


SHA_OWNERS: dict[str, set] = {}      # svg content hash -> profiles displaying it (set in main)


def svg_origin(url: str, kind: str, img: dict | None = None, owner: str | None = None) -> str:
    """Where an SVG's design came from.

    'bespoke'    committed or personally hosted, not a known tool's output, and
                 not byte-identical to an SVG in anyone else's profile
    'copied'     byte-identical to an SVG shown in another profile — a template
    'generated'  committed output of a known Action (snk, metrics, 3d-contrib…)
    'service'    a live third-party generator
    'badge-icon' tiny templated badges and icons
    """
    svg = (img or {}).get("svg") or {}
    g = classify(url, kind)
    if svg.get("fingerprint"):
        return "generated" if kind == "committed" else "service"
    host = urllib.parse.urlsplit(url or "").netloc.lower()
    # Self-made means committed to the user's own repos, or served from a domain
    # carrying their name (adamalston.com). An unrecognised third-party host is
    # still a service someone else runs — unknown is not the same as bespoke.
    personal = bool(owner and owner != "any" and len(owner) > 3 and owner.lower() in host)
    if kind == "committed" or personal:
        sha = (img or {}).get("sha1")
        if sha and owner and len(SHA_OWNERS.get(sha, ())) > 1:
            return "copied"
        return "bespoke"
    return "badge-icon" if g in BADGE_ICON else "service"


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def load() -> tuple[list[dict], dict, dict]:
    profiles = json.loads((DATA / "profiles.json").read_text(encoding="utf-8"))
    images = json.loads((DATA / "images.json").read_text(encoding="utf-8"))
    lp = DATA / "layout.json"
    layout = json.loads(lp.read_text(encoding="utf-8")) if lp.exists() else {}
    return profiles, images, layout


def norm_url(u: str) -> str:
    """Comparable form of an image URL as written in a README or as rendered.

    GitHub renders repo-relative images as github.com/<o>/<r>/raw/<b>/<path> and
    keeps a third-party image's original URL in data-canonical-src; the harvest
    stores raw.githubusercontent.com URLs. Normalise both sides to one shape.
    """
    u = html.unescape(u or "").split("#")[0].strip()
    m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/(?:raw|blob)/(.+)", u, re.I)
    if m:
        u = f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{m.group(3)}"
    u = re.sub(r"[?&]raw=true$", "", u)
    return urllib.parse.unquote(u).lower()


def cohort(p: dict) -> str:
    return "curated" if "awesome-github-profile-readme" in p.get("sources", []) else "search"


def measured_slots(lay: dict | None, idx: dict, kinds: dict | None = None,
                   owner: str | None = None) -> tuple[list[dict], int, int]:
    """Legibility from real rendered widths. Returns (slots, shown, matched).

    Each slot records its SVG origin and two sizes for its largest text: at the
    image's native width and as actually rendered. That separates cards the
    phone *shrinks* into illegibility from ones too small on any device.
    Badges and icons are tagged so callers can leave them out of "cards".
    """
    if not lay or "error" in lay:
        return [], 0, 0
    slots, shown, matched = [], 0, 0
    for im in lay.get("images", []):
        if im["w"] <= 0:
            continue                      # hidden theme variant or failed image
        shown += 1
        key = norm_url(im["canonical"])
        met = idx.get(key)
        if met is None:
            continue
        matched += 1
        s = met.get("svg")
        if not s or not s.get("has_text") or not s.get("vb_w") or s.get("min_font") is None:
            continue
        k = im["w"] / s["vb_w"]
        native_w = s.get("intrinsic_w") or s["vb_w"]
        kind = (kinds or {}).get(key, "third-party")
        slots.append({"worst": s["min_font"] * k, "best": s["max_font"] * k,
                      "native_best": s["max_font"] * native_w / s["vb_w"],
                      "origin": svg_origin(met.get("url", ""), kind, met, owner),
                      "in_table": im["in_table"], "w": im["w"], "nat": im["nat"]})
    return slots, shown, matched


def card_slots(slots: list[dict]) -> list[dict]:
    """Slots that are cards: everything except templated badges and icons."""
    return [s for s in slots if s["origin"] != "badge-icon"]


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

def profile_row(p: dict, images: dict, layout: dict | None = None, idx: dict | None = None) -> dict:
    lay = (layout or {}).get(p.get("owner", p["user"]), {})
    own = p.get("owner", p["user"])
    kinds = {norm_url(o["url"]): o["kind"] for o in p.get("images", []) if o.get("url")}
    m_all, m_shown, m_matched = measured_slots(lay.get("390"), idx or {}, kinds, own)
    d_all, _, _ = measured_slots(lay.get("1280"), idx or {}, kinds, own)
    m_slots, d_slots = card_slots(m_all), card_slots(d_all)
    phone = lay.get("390") or {}
    tables = phone.get("tables", []) if "error" not in phone else []
    crushed = sum(1 for im in phone.get("images", []) if "error" not in phone
                  and im["in_table"] and 0 < im["w"] < 120 and im["nat"] >= 300)
    desk = lay.get("1280") or {}
    measured = {
        "layout_measured": bool(phone) and "error" not in phone,
        "layout_measured_desktop": bool(desk) and "error" not in desk,
        "m_images_shown": m_shown, "m_images_matched": m_matched,
        "m_text_cards": len(m_slots),
        "m_illegible_cards": sum(s["best"] < LEGIBLE_PX for s in m_slots),
        # legible at native size, illegible only because the phone shrank it
        "m_illegible_phone_caused": sum(s["best"] < LEGIBLE_PX <= s["native_best"] for s in m_slots),
        # too small even at full size — a design problem on any device
        "m_illegible_everywhere": sum(s["native_best"] < LEGIBLE_PX for s in m_slots),
        "m_card_origins": dict(collections.Counter(s["origin"] for s in m_slots
                                                   if s["best"] < LEGIBLE_PX)),
        "m_card_origin_totals": dict(collections.Counter(s["origin"] for s in m_slots)),
        "m_some_illegible": sum(s["worst"] < LEGIBLE_PX for s in m_slots),
        "m_worst_px": round(min(s["worst"] for s in m_slots), 1) if m_slots else None,
        "d_illegible_cards": sum(s["best"] < LEGIBLE_PX for s in d_slots),
        "tables_scrolling_with_images": sum(1 for t in tables if t["imgs"] and t["scroll"] > t["client"] + 1),
        "crushed_in_table": crushed,
        "page_overflow_phone": bool(phone.get("page_overflow")),
    }
    occ = displayed(p)
    imgs = [images.get(o["url"], {}) for o in occ]
    gens = collections.Counter(filter(None, (classify(o["url"], o["kind"]) for o in occ)))
    svg_occ = [(o, i) for o, i in zip(occ, imgs) if i.get("is_svg")]
    owner = p.get("owner", p["user"])
    origins = [svg_origin(o["url"], o["kind"], i, owner) for o, i in svg_occ]
    custom = [(o, i) for (o, i), g in zip(svg_occ, origins) if g == "bespoke"]
    copied = sum(g == "copied" for g in origins)
    generated = sum(g == "generated" for g in origins)
    # Techniques from custom SVGs only — badge templates would otherwise tag
    # nearly every profile with filter/clip-path/blur.
    techniques = sorted({t for _, i in custom for t in i.get("svg", {}).get("techniques", [])})
    badge_share = (sum(classify(o["url"], o["kind"]) in BADGE_ICON for o in occ) / len(occ)) if occ else 0.0
    mob = [o.get("mobile_px") for o in occ if o.get("mobile_px") is not None]
    mob_best = [o.get("mobile_best_px") for o in occ if o.get("mobile_best_px") is not None]
    sig = p.get("signals", {})
    theme = "picture" if sig.get("picture_theme") else "fragment" if sig.get("fragment_theme") else "none"
    return {
        **measured,
        "cohort": cohort(p),
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
        "custom_svgs": len(custom),              # bespoke only
        "custom_animated": sum(bool(i.get("svg", {}).get("animated")) for _, i in custom),
        "copied_svgs": copied,
        "generated_svgs": generated,
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
        "**min px** smallest text on a phone · **sideways** the page or a table of images "
        "scrolls horizontally on a phone.",
        "",
        "Phone figures come from real layout measured in headless Chrome at 390px "
        "(`tools/survey/layout.py`). A `~` marks a profile that couldn't be measured, where "
        "the value is the column-fit estimate instead.",
        "",
        "| Profile | Category | Pushed | img | own/up/3rd | Generators | svg (anim) | theme | brk | wf | illeg | min px | sideways |",
        "|---|---|---|--:|---|---|---|---|--:|--:|--:|--:|---|",
    ]
    for r in sorted(rows, key=lambda r: (r["status"] != "live", r["user"].lower())):
        if r["status"] != "live":
            lines.append(f"| [{r['user']}]({r['url']}) | {', '.join(r['categories'][:1])} | "
                         f"— | | | *{r['status']}* | | | | | | | |")
            continue
        gens = ", ".join(g.split(" — ")[0].split(" (")[0] for g in list(r["generators"])[:3]) or "—"
        pushed = (r["pushed_at"] or "")[:7]
        if r["layout_measured"]:
            ill = r["m_illegible_cards"] or ""
            mp = f"{r['m_worst_px']:.1f}" if r["m_worst_px"] is not None else "—"
            side = ", ".join(x for x, hit in (("page", r["page_overflow_phone"]),
                                              ("table", r["tables_scrolling_with_images"])) if hit)
        else:
            ill = f"~{r['illegible_cards']}" if r["illegible_cards"] else ""
            mp = f"~{r['mobile_worst_px']:.1f}" if r["mobile_worst_px"] is not None else "—"
            side = "?"
        cat = r["categories"][0].replace("code-search: ", "search: ") if r["categories"] else ""
        lines.append(
            f"| [{r['user']}]({r['url']}) | {cat} | {pushed} | {r['images']} | "
            f"{r['committed']}/{r['gh_upload']}/{r['third_party']} | {gens} | "
            f"{r['svgs']} ({r['animated_svgs']}) | {r['theme_switch']} | {r['broken'] or ''} | "
            f"{r['workflows'] or ''} | {ill} | {mp} | {side} |")
    (SURVEY / "PROFILES.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def measured_best_px(p: dict, o: dict, images: dict, layout: dict) -> float | None:
    """Largest text of this image as actually rendered on the phone, in px."""
    lay = (layout.get(p.get("owner", p["user"])) or {}).get("390") or {}
    svg = (images.get(o["url"]) or {}).get("svg") or {}
    if "error" in lay or not svg.get("has_text") or not svg.get("vb_w") or svg.get("max_font") is None:
        return None
    key = norm_url(o["url"])
    widths = [im["w"] for im in lay.get("images", []) if im["w"] > 0 and norm_url(im["canonical"]) == key]
    return svg["max_font"] * widths[0] / svg["vb_w"] if widths else None


def generator_stats(profiles: list[dict], images: dict, layout: dict | None = None) -> list[dict]:
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
            px = measured_best_px(p, o, images, layout or {})
            if px is not None:
                s["best_px"].append(px)
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
            "cards_measured": len(bp),
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
        "**illegible on phone** is the share of its rendered images whose *largest* text is under "
        "11px, measured from real layout at 390px; the number in brackets is how many it rests on, "
        "so read small ones with care. A dash means no measurable text (icons, animations, or a "
        "service that returned nothing).",
        "",
        "| Generator | Source | Profiles | URLs | Live | Main failure | Median ms | Illegible on phone |",
        "|---|---|--:|--:|--:|---|--:|--:|",
    ]
    for g in gens:
        fail = ", ".join(f"{k} ×{v}" for k, v in list(g["fail_reasons"].items())[:2]) or "—"
        ill = (f"{100 * g['illegible_share']:.0f}% ({g['cards_measured']})"
               if g["illegible_share"] is not None else "—")
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
    origin = {u: svg_origin(u, kind_of[u], svgs[u], "any") for u in svgs}

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
        "svg_techniques_bespoke": techs("bespoke"),
        "svg_techniques_copied": techs("copied"),
        "svg_techniques_services": techs("service"),
        "bespoke_svgs_animated": sum(bool(svgs[u].get("svg", {}).get("animated"))
                                     for u in svgs if origin[u] == "bespoke"),
        "profiles_using_technique_bespoke": _profiles_per_technique(live, res),
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


def _profiles_per_technique(live: list[dict], res: dict) -> dict:
    """How many profiles use each technique in at least one bespoke SVG.

    Counting SVGs would let one profile with forty animated files outvote forty
    profiles with one each; profiles are the honest unit.
    """
    c = collections.Counter()
    for p in live:
        owner = p.get("owner", p["user"])
        seen = set()
        for o in displayed(p):
            img = res.get(o["url"], {})
            if img.get("is_svg") and svg_origin(o["url"], o["kind"], img, owner) == "bespoke":
                seen.update(img.get("svg", {}).get("techniques", []))
        c.update(seen)
    return dict(c.most_common())


def blob_url(raw: str) -> str:
    """raw.githubusercontent.com/<o>/<r>/<b>/<p> -> github.com/<o>/<r>/blob/<b>/<p> for humans."""
    m = re.match(r"https://raw\.githubusercontent\.com/([^/]+)/([^/]+)/([^/]+)/(.+)", raw)
    return f"https://github.com/{m.group(1)}/{m.group(2)}/blob/{m.group(3)}/{m.group(4)}" if m else raw


def technique_exemplars(live: list[dict], res: dict, per: int = 8) -> dict:
    """Real bespoke SVGs using each technique — the evidence Phase 2 cites.

    One file per profile per technique, preferring profiles whose images all
    load, so every cited example can actually be opened.
    """
    out: dict[str, list] = collections.defaultdict(list)

    def rank(p):
        own = p.get("owner", p["user"])
        broken = sum(not res.get(o["url"], {}).get("ok", False) for o in displayed(p))
        bespoke = sum(1 for o in displayed(p) if res.get(o["url"], {}).get("is_svg")
                      and svg_origin(o["url"], o["kind"], res.get(o["url"]), own) == "bespoke")
        return (broken > 0, -bespoke, own.lower())

    appearances: collections.Counter = collections.Counter()
    for p in sorted(live, key=rank):
        owner = p.get("owner", p["user"])
        taken = set()
        for o in displayed(p):
            if appearances[owner] >= 3:          # spread examples across profiles
                break
            img = res.get(o["url"], {})
            if not (img.get("ok") and img.get("is_svg")):
                continue
            if svg_origin(o["url"], o["kind"], img, owner) != "bespoke":
                continue
            for t in img.get("svg", {}).get("techniques", []):
                if t in taken or len(out[t]) >= per or appearances[owner] >= 3:
                    continue
                taken.add(t)
                appearances[owner] += 1
                out[t].append({"user": owner, "profile": f"https://github.com/{owner}",
                               "svg": blob_url(o["url"]), "bytes": img.get("bytes"),
                               "animated": img.get("svg", {}).get("animated", False)})
    return dict(out)


def cohort_summary(rows: list[dict]) -> dict:
    """Headline rates per population. Curated = popular; search = ambitious SVG users."""
    out = {}
    for name in ("curated", "search", "all"):
        rs = [r for r in rows if r["status"] == "live" and (name == "all" or r["cohort"] == name)]
        meas = [r for r in rs if r["layout_measured"]]
        n, m = len(rs), len(meas)

        def share(pred, pool):
            return f"{100 * sum(1 for r in pool if pred(r)) / len(pool):.0f}%" if pool else "—"

        out[name] = {
            "profiles": n, "layout_measured": m,
            "median_images": statistics.median(r["images"] for r in rs) if rs else None,
            "with_broken_image": share(lambda r: r["broken"] > 0, rs),
            "using_dead_stats_instance": share(lambda r: "github-readme-stats — public instance" in r["generators"], rs),
            "dark_light_switching": share(lambda r: r["theme_switch"] != "none", rs),
            "with_custom_svg": share(lambda r: r["custom_svgs"] > 0, rs),
            "with_animated_custom_svg": share(lambda r: r["custom_animated"] > 0, rs),
            "with_workflows": share(lambda r: r["workflows"] > 0, rs),
            "badge_wall_over_half": share(lambda r: r["badge_share"] > 0.5, rs),
            "phone_illegible_card_measured": share(lambda r: r["m_illegible_cards"] > 0, meas),
            "phone_some_tiny_text_measured": share(lambda r: r["m_some_illegible"] > 0, meas),
            "desktop_illegible_card_measured": share(lambda r: r["d_illegible_cards"] > 0,
                                                     [r for r in rs if r["layout_measured_desktop"]]),
            "table_scrolls_sideways_on_phone": share(lambda r: r["tables_scrolling_with_images"] > 0, meas),
            "cards_crushed_in_table": share(lambda r: r["crushed_in_table"] > 0, meas),
            "page_scrolls_sideways_on_phone": share(lambda r: r["page_overflow_phone"], meas),
        }
        cards = sum(r["m_text_cards"] for r in meas)
        ill = sum(r["m_illegible_cards"] for r in meas)
        out[name].update({
            "cards_measured": cards,
            "cards_illegible_on_phone": f"{100 * ill / cards:.0f}%" if cards else "—",
            "of_those_phone_caused": f"{100 * sum(r['m_illegible_phone_caused'] for r in meas) / ill:.0f}%" if ill else "—",
            "of_those_tiny_everywhere": f"{100 * sum(r['m_illegible_everywhere'] for r in meas) / ill:.0f}%" if ill else "—",
        })
        by_origin = {}
        for o in ("bespoke", "service", "generated", "copied"):
            tot = sum(r["m_card_origin_totals"].get(o, 0) for r in meas)
            bad = sum(r["m_card_origins"].get(o, 0) for r in meas)
            if tot:
                by_origin[o] = f"{bad}/{tot} ({100 * bad / tot:.0f}%)"
        out[name]["illegible_cards_by_origin"] = by_origin
    return out


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
    profiles, images, layout = load()
    if a.hosts:
        unclassified_hosts(profiles)
        return
    idx = {norm_url(u): r for u, r in images.items()}
    for p in profiles:
        if p["status"] != "live":
            continue
        for o in displayed(p):
            sha = images.get(o["url"], {}).get("sha1")
            if sha:
                SHA_OWNERS.setdefault(sha, set()).add(p.get("owner", p["user"]))
    rows = [profile_row(p, images, layout, idx) for p in profiles]
    gens = generator_stats([p for p in profiles if p["status"] == "live"], images, layout)
    write_profiles_md(rows)
    write_generators_md(gens)
    s = summary(profiles, images, rows, gens)
    s["by_cohort"] = cohort_summary(rows)
    shown = sum(r["m_images_shown"] for r in rows)
    s["layout_match_rate"] = f"{100 * sum(r['m_images_matched'] for r in rows) / shown:.0f}%" if shown else None
    (DATA / "summary.json").write_text(json.dumps(s, indent=1), encoding="utf-8")
    (DATA / "rows.json").write_text(json.dumps(rows, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    ex = technique_exemplars([p for p in profiles if p["status"] == "live"], images)
    (DATA / "technique_exemplars.json").write_text(json.dumps(ex, indent=1), encoding="utf-8")
    print(json.dumps(s, indent=1))


if __name__ == "__main__":
    main()
