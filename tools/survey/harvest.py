#!/usr/bin/env python3
"""Harvest GitHub profile READMEs and every image they reference.

    python tools/survey/harvest.py              # full run
    python tools/survey/harvest.py --limit 5    # smoke test
    python tools/survey/harvest.py --refresh    # ignore the HTTP cache

Writes docs/survey/data/profiles.json and docs/survey/data/images.json.

Only links and derived measurements are stored. README text and image bodies
stay in the local cache (.cache/survey/, gitignored) and are never committed.
The GitHub token is sent to api.github.com only — never to image hosts.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CACHE = ROOT / ".cache" / "survey"
OUT = ROOT / "docs" / "survey" / "data"

UA = ("Mozilla/5.0 (compatible; profile-readme-survey/1.0; "
      "+https://github.com/hammadshakeelai/github-profile-blueprint)")
API = "https://api.github.com"

# Measured README container widths — see
# skills/github-profile-readme/references/measured-constraints.md
MOBILE_R = 309
DESKTOP_R = 846
SVG_DEFAULT_FONT_PX = 16.0   # CSS "medium", the SVG default when unset

RESERVED = {"topics", "sponsors", "features", "marketplace", "orgs", "about",
            "collections", "settings", "apps", "search", "trending", "login"}

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


# --------------------------------------------------------------------------- #
# HTTP with an on-disk cache
# --------------------------------------------------------------------------- #

def gh_token() -> str | None:
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        return tok
    try:
        out = subprocess.run(["gh", "auth", "token"], capture_output=True,
                             text=True, timeout=20)
        return out.stdout.strip() or None
    except Exception:
        return None


TOKEN: str | None = None
REFRESH = False


def _cache_key(url: str, accept: str) -> str:
    return hashlib.sha256(f"{url}|{accept}".encode()).hexdigest()[:40]


def to_uri(url: str) -> str:
    """Percent-encode what a browser would: non-ASCII, spaces, stray characters.

    READMEs are full of badge labels with accents and emoji, and filenames with
    spaces. Browsers encode these transparently; urllib raises instead, which
    would otherwise be misreported as the image host being down. Existing
    %-escapes are preserved.
    """
    p = urllib.parse.urlsplit(url)
    host = p.hostname or ""
    if any(ord(ch) > 127 for ch in host):
        idna = host.encode("idna").decode("ascii")
        netloc = p.netloc.replace(host, idna)
    else:
        netloc = p.netloc
    path = urllib.parse.quote(p.path, safe="/%:@!$&'()*+,;=~-._")
    query = urllib.parse.quote(p.query, safe="=&%:@!$'()*+,;/?~-._")
    return urllib.parse.urlunsplit((p.scheme, netloc, path, query, ""))


def http_get(url: str, accept: str = "*/*", timeout: float = 15.0,
             max_bytes: int = 4_000_000) -> dict:
    """GET with caching. Returns status, ctype, body, ms, final_url, error."""
    key = _cache_key(url, accept)
    meta_p, body_p = CACHE / f"{key}.json", CACHE / f"{key}.bin"
    if not REFRESH and meta_p.exists() and body_p.exists():
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
        meta["body"] = body_p.read_bytes()
        return meta

    headers = {"User-Agent": UA, "Accept": accept}
    if url.startswith(API):
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"

    t0 = time.perf_counter()
    meta = {"url": url, "status": 0, "ctype": "", "ms": 0,
            "final_url": url, "error": None}
    body = b""
    try:
        req = urllib.request.Request(to_uri(url), headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read(max_bytes + 1)[:max_bytes]
            meta.update(status=r.status, ctype=r.headers.get("Content-Type", ""),
                        final_url=r.geturl())
    except urllib.error.HTTPError as e:
        meta.update(status=e.code, ctype=e.headers.get("Content-Type", "") if e.headers else "")
        try:
            body = e.read(200_000)
        except Exception:
            pass
    except Exception as e:                       # timeouts, DNS, TLS, resets
        meta["error"] = f"{type(e).__name__}: {e}"[:200]
    meta["ms"] = round((time.perf_counter() - t0) * 1000)

    CACHE.mkdir(parents=True, exist_ok=True)
    meta_p.write_text(json.dumps(meta), encoding="utf-8")
    body_p.write_bytes(body)
    meta["body"] = body
    return meta


# --------------------------------------------------------------------------- #
# Candidates
# --------------------------------------------------------------------------- #

def parse_awesome_list(md: str, source: str) -> dict[str, dict]:
    """Profiles under '## Categories' in abhisheknaiidu/awesome-github-profile-readme."""
    out: dict[str, dict] = {}
    in_categories, category = False, None
    for line in md.splitlines():
        if line.startswith("## "):
            in_categories = line.strip().lower().startswith("## categories")
            continue
        if not in_categories:
            continue
        m = re.match(r"#{3,4}\s+(.*)", line)
        if m:
            category = re.sub(r"[^\w\s.&'-]", "", m.group(1)).strip()
            continue
        for user in re.findall(r"https?://github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)", line):
            if user.lower() in RESERVED:
                continue
            rec = out.setdefault(user.lower(), {"user": user, "sources": [], "categories": []})
            if source not in rec["sources"]:
                rec["sources"].append(source)
            if category and category not in rec["categories"]:
                rec["categories"].append(category)
    return out


def collect_candidates() -> dict[str, dict]:
    cands: dict[str, dict] = {}
    r = http_get(f"{API}/repos/abhisheknaiidu/awesome-github-profile-readme/readme",
                 accept="application/vnd.github.raw")
    if r["status"] != 200:
        sys.exit(f"could not fetch the awesome list: {r['status']} {r['error']}")
    batches = [parse_awesome_list(r["body"].decode("utf-8", "replace"),
                                  "awesome-github-profile-readme").values()]
    # Pluggable extra sources: each tools/survey/sources/*.json is a list of
    # {user, sources, categories, ...} records written by a source_*.py script.
    for f in sorted((Path(__file__).resolve().parent / "sources").glob("*.json")):
        batches.append(json.loads(f.read_text(encoding="utf-8")))
    for batch in batches:
        for v in batch:
            cur = cands.setdefault(v["user"].lower(),
                                   {"user": v["user"], "sources": [], "categories": []})
            cur["sources"] += [s for s in v.get("sources", []) if s not in cur["sources"]]
            cur["categories"] += [c for c in v.get("categories", []) if c not in cur["categories"]]
            if v.get("svg_paths"):
                cur.setdefault("svg_paths", [])
                cur["svg_paths"] += [s for s in v["svg_paths"] if s not in cur["svg_paths"]]
    return cands


# --------------------------------------------------------------------------- #
# README parsing
# --------------------------------------------------------------------------- #

COMMENT = re.compile(r"<!--.*?-->", re.S)
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
IMG_MD = re.compile(r"!\[[^\]]*\]\(\s*<?([^)\s>]+)")
IMG_TAG = re.compile(r"<img\b[^>]*>", re.I | re.S)
SOURCE_TAG = re.compile(r"<source\b[^>]*>", re.I | re.S)
PICTURE = re.compile(r"<picture\b.*?</picture>", re.I | re.S)
class _Attr:
    """Attribute value, quoted (may contain spaces) or bare. `.search()` mimics re."""

    def __init__(self, name: str):
        self.rx = re.compile(rf"\b{name}\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s>]+))", re.I)

    def search(self, s: str):
        m = self.rx.search(s)
        if not m:
            return None
        val = next(g for g in m.groups() if g is not None).strip()
        return type("M", (), {"group": lambda self, i=1: val})()


SRC, SRCSET, WIDTH, HEIGHT, MEDIA = (_Attr("src"), _Attr("srcset"), _Attr("width"),
                                     _Attr("height"), _Attr("media"))


def _dim(tag: str, rx: re.Pattern) -> tuple[float | None, bool]:
    m = rx.search(tag)
    if not m:
        return None, False
    raw = m.group(1).strip()
    num = re.match(r"([0-9.]+)", raw)
    if not num:
        return None, False
    try:
        return float(num.group(1)), raw.endswith("%")
    except ValueError:
        return None, False


def resolve(url: str, owner: str, repo: str, branch: str,
            aliases: frozenset = frozenset()) -> tuple[str | None, str]:
    """Absolute URL and host kind: committed | gh-upload | third-party | data-uri.

    `aliases` holds former usernames: renamed accounts often still hardcode the
    old name in raw URLs, which GitHub redirects, so those are still self-hosted.
    """
    selves = {owner.lower(), *aliases}
    u = url.strip().replace("&amp;", "&")
    if u.startswith("data:"):
        return None, "data-uri"
    if u.startswith("//"):
        u = "https:" + u
    if not re.match(r"https?://", u, re.I):
        path = re.sub(r"^\./", "", u).lstrip("/")
        return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}", "committed"

    p = urllib.parse.urlsplit(u)
    host = p.netloc.lower()
    m = re.match(r"/([^/]+)/([^/]+)/(?:blob|raw)/(.+)", p.path)
    if host == "github.com" and m:
        kind = "committed" if m.group(1).lower() in selves else "third-party"
        return f"https://raw.githubusercontent.com/{m.group(1)}/{m.group(2)}/{m.group(3)}", kind
    if host == "raw.githubusercontent.com":
        seg = p.path.strip("/").split("/")
        kind = "committed" if seg and seg[0].lower() in selves else "third-party"
        return u, kind
    if host in ("user-images.githubusercontent.com", "private-user-images.githubusercontent.com") \
            or (host == "github.com" and p.path.startswith("/user-attachments/")):
        return u, "gh-upload"
    return u, "third-party"


def extract_images(md: str, owner: str, repo: str, branch: str,
                   aliases: frozenset = frozenset()) -> tuple[list[dict], dict]:
    """Rendered image occurrences, plus README-level theme-switching signals."""
    body = FENCE.sub("", COMMENT.sub("", md))
    signals = {
        "picture_theme": bool(re.search(r"<source\b[^>]*prefers-color-scheme", body, re.I)),
        "fragment_theme": bool(re.search(r"#gh-(dark|light)-mode-only", body, re.I)),
    }
    occ: list[dict] = []

    def add(raw_url: str, width: tuple, height: tuple, via: str, media: str | None = None):
        frag = None
        if "#" in raw_url:
            raw_url, frag = raw_url.split("#", 1)
        absu, kind = resolve(raw_url, owner, repo, branch, aliases)
        occ.append({"url": absu, "raw": raw_url[:300], "kind": kind, "via": via,
                    "width": width[0], "width_pct": width[1],
                    "height": height[0], "fragment": frag, "media": media})

    # <picture> sources are theme or size variants of one displayed image
    for pic in PICTURE.findall(body):
        for tag in SOURCE_TAG.findall(pic):
            ms = SRCSET.search(tag)
            if ms:
                mm = MEDIA.search(tag)
                add(ms.group(1).split(",")[0].split()[0], (None, False), (None, False),
                    "source", mm.group(1) if mm else None)
    for tag in IMG_TAG.findall(body):
        ms = SRC.search(tag)
        if ms:
            add(ms.group(1), _dim(tag, WIDTH), _dim(tag, HEIGHT), "img")
    for m in IMG_MD.finditer(body):
        add(m.group(1), (None, False), (None, False), "markdown")
    return occ, signals


# --------------------------------------------------------------------------- #
# Image analysis
# --------------------------------------------------------------------------- #

ERROR_PHRASES = ("something went wrong", "rate limit", "api rate", "could not resolve",
                 "not found", "failed to", "please try again", "maximum retries",
                 "exceeded", "deployment_paused", "deployment has been disabled",
                 "user not found", "internal server error", "bad credentials")

# Signatures that GitHub Actions leave in the SVGs they commit. A committed file
# is not necessarily hand-made: these mark the ones a tool generated.
FINGERPRINTS = [
    ("snk contribution snake", re.compile(r"Platane/snk", re.I)),
    ("pacman-contribution-graph", re.compile(r"pacman-contribution-graph", re.I)),
    ("github-profile-3d-contrib", re.compile(r"rb-l0-left|class=\"radar\"")),
    ("lowlighter/metrics", re.compile(r"id=\"metrics-end\"")),
    ("github-readme-stats", re.compile(r"data-testid=\"(card-title|main-card-body|lang-items)\"")),
]
# Many generators announce themselves in the file; catch the ones not listed.
GENERATED_DESC = re.compile(r"<desc>\s*Generated (?:with|by)\s+([^<\n]{2,80})", re.I)

FONT_RX = [
    re.compile(r"font-size\s*[:=]\s*[\"']?\s*([0-9.]+)\s*(px|pt|em|rem|%)?", re.I),
    re.compile(r"\bfont\s*:\s*[^;\"'}]*?\b([0-9.]+)\s*(px|pt)\b", re.I),
]


import math
import xml.etree.ElementTree as ET

_LEN = re.compile(r"^\s*([0-9.]+)\s*(px|pt|em|rem|%)?\s*$", re.I)
_CSS_RULE = re.compile(r"([^{}]+)\{([^}]*)\}")
_CSS_SIZE = [re.compile(r"font-size\s*:\s*([0-9.]+\s*(?:px|pt|em|rem|%)?)", re.I),
             re.compile(r"\bfont\s*:\s*[^;]*?\b([0-9.]+\s*(?:px|pt))\b", re.I)]


def _length(val: str | None, parent: float) -> float | None:
    """A CSS font-size in px, resolving relative units against the parent size."""
    if not val:
        return None
    m = _LEN.match(val)
    if not m:
        return None
    v, unit = float(m.group(1)), (m.group(2) or "px").lower()
    return {"px": v, "pt": v * 4 / 3, "em": v * parent, "rem": v * 16.0,
            "%": parent * v / 100}[unit]


def _scale(transform: str | None) -> float:
    """Uniform scale factor of an SVG transform list (scale() and matrix())."""
    if not transform:
        return 1.0
    s = 1.0
    for fn, args in re.findall(r"(scale|matrix)\s*\(([^)]*)\)", transform, re.I):
        nums = [float(x) for x in re.findall(r"-?[0-9.]+(?:e-?\d+)?", args)]
        if fn.lower() == "scale" and nums:
            s *= math.sqrt(abs(nums[0] * (nums[1] if len(nums) > 1 else nums[0])))
        elif fn.lower() == "matrix" and len(nums) >= 4:
            s *= math.sqrt(abs(nums[0] * nums[3] - nums[1] * nums[2]))
    return s


def text_sizes(text: str) -> list[float] | None:
    """Effective size of every visible text run, in viewBox units.

    Walks the element tree carrying inherited font-size and the product of all
    enclosing transforms. A flat scan of font-size values gets badges wrong —
    shields.io sets font-size="110" and then applies transform="scale(.1)" —
    and misses em units and class-based CSS. Returns None if the SVG won't parse.

    These SVGs come from arbitrary third-party hosts, so they're untrusted. Any
    document declaring a DTD or entities is refused before parsing — the vector
    for both XXE and entity-expansion ("billion laughs") attacks, and the core
    of what defusedxml forbids — and falls back to the flat scan instead.
    """
    if re.search(r"<!DOCTYPE|<!ENTITY", text, re.I):
        return None
    try:
        root = ET.fromstring(text.encode("utf-8"))
    except ET.ParseError:
        return None
    by_class: dict[str, str] = {}
    by_tag: dict[str, str] = {}
    for style in root.iter():
        if style.tag.split("}")[-1] != "style" or not style.text:
            continue
        for selectors, body in _CSS_RULE.findall(style.text):
            size = next((m.group(1) for rx in _CSS_SIZE if (m := rx.search(body))), None)
            if not size:
                continue
            for sel in selectors.split(","):
                last = sel.strip().split()[-1] if sel.strip() else ""
                if last.startswith("."):
                    by_class[last[1:].split(":")[0]] = size
                elif last in ("text", "tspan", "textPath", "*", "svg", "g"):
                    by_tag[last] = size
    sizes: list[float] = []

    def walk(el, fs: float, scale: float) -> None:
        tag = el.tag.split("}")[-1]
        for key in ("*", tag):
            if key in by_tag:
                fs = _length(by_tag[key], fs) or fs
        for c in (el.get("class") or "").split():
            if c in by_class:
                fs = _length(by_class[c], fs) or fs
        fs = _length(el.get("font-size"), fs) or fs
        st = el.get("style") or ""
        m = re.search(r"font-size\s*:\s*([^;]+)", st, re.I)
        if m:
            fs = _length(m.group(1), fs) or fs
        scale *= _scale(el.get("transform"))
        if tag in ("text", "tspan", "textPath") and (el.text or "").strip():
            sizes.append(fs * scale)
        for child in el:
            walk(child, fs, scale)

    walk(root, SVG_DEFAULT_FONT_PX, 1.0)
    return [s for s in sizes if s > 0.5]


def svg_metrics(text: str) -> dict:
    root = re.search(r"<svg\b[^>]*>", text, re.S | re.I)
    root_tag = root.group(0) if root else ""
    vb = re.search(r"viewBox\s*=\s*[\"']\s*[-0-9.eE]+[\s,]+[-0-9.eE]+[\s,]+([0-9.eE]+)[\s,]+([0-9.eE]+)",
                   root_tag, re.I)
    w, w_pct = _dim(root_tag, WIDTH)
    h, _ = _dim(root_tag, HEIGHT)
    vbw = float(vb.group(1)) if vb else (w if w and not w_pct else None)
    vbh = float(vb.group(2)) if vb else h
    intrinsic = w if (w and not w_pct) else vbw

    has_text = bool(re.search(r"<(text|tspan|textPath)\b", text, re.I)) or "<foreignObject" in text
    sizes: list[float] = []
    for rx in FONT_RX:
        for num, unit in rx.findall(text):
            try:
                v = float(num)
            except ValueError:
                continue
            unit = (unit or "px").lower()
            if unit == "pt":
                v *= 4 / 3
            elif unit != "px":
                continue
            if v >= 4:            # ignore nonsense / hairline values
                sizes.append(v)
    # Prefer the tree walk (transforms, inheritance, CSS classes); fall back to
    # the flat scan only when the SVG doesn't parse as XML.
    walked = text_sizes(text) if has_text else None
    method = "tree" if walked else "scan"
    if walked:
        sizes = walked
    # Smallest text alone can't tell decorative micro-labels from an unreadable
    # card, so keep the largest too: if even that is illegible, the card is.
    min_font = (min(sizes) if sizes else SVG_DEFAULT_FONT_PX) if has_text else None
    max_font = (max(sizes) if sizes else SVG_DEFAULT_FONT_PX) if has_text else None

    low = text.lower()
    anim_smil = bool(re.search(r"<(animate|animatetransform|animatemotion|set)\b", low))
    anim_css = "@keyframes" in low
    techniques = sorted(t for t, hit in {
        "smil": anim_smil,
        "css-keyframes": anim_css,
        "filter": "<filter" in low,
        "blur-glow": "fegaussianblur" in low,
        "mask": "<mask" in low,
        "clip-path": "<clippath" in low,
        "gradient": "lineargradient" in low or "radialgradient" in low,
        "stroke-draw": "stroke-dash" in low and (anim_smil or anim_css),
        "foreign-object": "<foreignobject" in low,
        "embedded-font": "@font-face" in low and "data:" in low,
        # A base64 logo inside a badge is data:image/svg+xml — vector, not raster.
        "embedded-raster": bool(re.search(r"<image\b[^>]*href\s*=\s*[\"']data:image/(png|jpe?g|gif|webp)", low)),
        "embedded-svg": bool(re.search(r"<image\b[^>]*href\s*=\s*[\"']data:image/svg", low)),
        "theme-aware-svg": "prefers-color-scheme" in low,
        "script": "<script" in low,
        "text-path": "<textpath" in low,
    }.items() if hit)

    fingerprint = next((name for name, rx in FINGERPRINTS if rx.search(text)), None)
    if fingerprint is None and (m := GENERATED_DESC.search(text)):
        # "Generated with some-tool on Mon Sep 21 2026 …" -> "some-tool"
        fingerprint = re.split(r"\s+on\s+|\s+at\s+|\s*\(|,", m.group(1).strip())[0].strip()[:60] or None

    return {"fingerprint": fingerprint,
            "vb_w": vbw, "vb_h": vbh, "intrinsic_w": intrinsic, "has_text": has_text,
            "min_font": min_font, "max_font": max_font, "font_sizes_found": len(sizes),
            "size_method": method if has_text else None,
            "animated": anim_smil or anim_css, "techniques": techniques}


IMG_ACCEPT = "image/avif,image/webp,image/svg+xml,image/*,*/*;q=0.8"
TRANSIENT = {"timeout", "network"}
RECHECK_DELAY = 0.6        # seconds before each recheck request
RECHECK_WORKERS = 2


def recheck(url: str) -> dict:
    """Second attempt for timeouts and resets: drop the cached miss, allow 30s.

    A single slow response is not evidence a generator is dead, so only failures
    that repeat are reported as broken. The recheck runs slowly on purpose: the
    first pass sends hundreds of requests to hosts like img.shields.io, which then
    throttles the client — retrying at the same rate would measure our own
    flooding, not the service.
    """
    time.sleep(RECHECK_DELAY)
    key = _cache_key(url, IMG_ACCEPT)
    for suffix in (".json", ".bin"):
        (CACHE / f"{key}{suffix}").unlink(missing_ok=True)
    res = analyze_image(url, timeout=30.0)
    res["rechecked"] = True
    return res


def analyze_image(url: str, timeout: float = 15.0) -> dict:
    r = http_get(url, accept=IMG_ACCEPT, timeout=timeout)
    body, ctype = r["body"], (r["ctype"] or "").lower()
    head = body[:2048].lstrip().lower()
    is_svg = "svg" in ctype or head.startswith(b"<svg") or (head.startswith(b"<?xml") and b"<svg" in head)
    is_gif = "gif" in ctype or body[:6] in (b"GIF87a", b"GIF89a")
    is_image = is_svg or ctype.startswith("image/") or is_gif
    res = {"url": url, "status": r["status"], "ctype": ctype.split(";")[0], "bytes": len(body),
           "ms": r["ms"], "error": r["error"], "final_host": urllib.parse.urlsplit(r["final_url"]).netloc,
           "is_svg": is_svg, "is_gif": is_gif,
           "animated_gif": is_gif and body.count(b"\x21\xf9\x04") > 1}
    error_card = False
    if is_svg:
        text = body.decode("utf-8", "replace")
        res["svg"] = svg_metrics(text)
        # Identical bytes in different people's repos means a copied asset.
        res["sha1"] = hashlib.sha1(body).hexdigest()[:16]
        visible = re.sub(r"<[^>]+>", " ", text).lower()
        error_card = any(p in visible for p in ERROR_PHRASES)
    res["error_card"] = error_card
    res["ok"] = bool(200 <= r["status"] < 300 and is_image and not error_card and len(body) > 0)

    reason = None
    if r["error"]:
        e = r["error"].lower()
        reason = "dns" if "getaddrinfo" in e or "name or service" in e else \
                 "timeout" if "timed out" in e else "network"
    elif not 200 <= r["status"] < 300:
        # Vercel answers a shut-off free-tier deployment with 402/503 and one of
        # these markers; naming them separates "the service was switched off"
        # from an ordinary HTTP error.
        reason = ("vercel-paused" if b"DEPLOYMENT_PAUSED" in body else
                  "vercel-disabled" if b"DEPLOYMENT_DISABLED" in body else
                  f"http-{r['status']}")
    elif not body:
        reason = "empty"
    elif not is_image:
        reason = "not-image"
    elif error_card:
        reason = "error-card"
    res["fail_reason"] = reason
    return res


def rendered_width(o: dict, img: dict, container: float) -> float | None:
    s = img.get("svg") or {}
    vbw, vbh, intrinsic = s.get("vb_w"), s.get("vb_h"), s.get("intrinsic_w")
    if o.get("width") and o.get("width_pct"):
        return container * o["width"] / 100
    if o.get("width"):
        return min(o["width"], container)
    if o.get("height") and vbw and vbh:
        return min(o["height"] * vbw / vbh, container)
    return min(intrinsic, container) if intrinsic else None


def legibility(o: dict, img: dict, container: float, which: str = "min_font") -> float | None:
    """Effective on-screen px of the smallest (or largest) SVG text in this slot."""
    s = img.get("svg")
    if not s or not s.get("has_text") or not s.get("vb_w") or s.get(which) is None:
        return None
    rw = rendered_width(o, img, container)
    if not rw:
        return None
    return round(s[which] * rw / s["vb_w"], 2)


# --------------------------------------------------------------------------- #
# Driver
# --------------------------------------------------------------------------- #

def fetch_profile(c: dict) -> dict:
    user = c["user"]
    rec = {**c, "status": "missing"}
    meta = http_get(f"{API}/repos/{user}/{user}", accept="application/vnd.github+json")
    if meta["status"] != 200:
        rec["http"] = meta["status"]
        return rec
    info = json.loads(meta["body"] or b"{}")
    # Organisations like WebKit/WebKit match the owner==repo pattern, but an org
    # page never renders a repo README as a profile — they aren't profiles.
    if info.get("owner", {}).get("type") != "User":
        rec.update(status="org", owner=info.get("owner", {}).get("login", user))
        return rec
    owner, repo = info.get("owner", {}).get("login", user), info.get("name", user)
    branch = info.get("default_branch", "main")
    rec.update(owner=owner, repo=repo, branch=branch, pushed_at=info.get("pushed_at"),
               stars=info.get("stargazers_count"), archived=info.get("archived"),
               url=f"https://github.com/{owner}")

    rd = http_get(f"{API}/repos/{owner}/{repo}/readme", accept="application/vnd.github.raw")
    if rd["status"] != 200:
        rec["status"] = "no-readme"
        return rec
    md = rd["body"].decode("utf-8", "replace")
    rec["status"] = "live"
    rec["readme_kb"] = round(len(rd["body"]) / 1024, 1)

    wf = http_get(f"{API}/repos/{owner}/{repo}/contents/.github/workflows",
                  accept="application/vnd.github+json")
    try:
        rec["workflows"] = len(json.loads(wf["body"])) if wf["status"] == 200 else 0
    except Exception:
        rec["workflows"] = 0

    rec["images"], rec["signals"] = extract_images(md, owner, repo, branch,
                                                   frozenset({user.lower()}))
    return rec


def main() -> None:
    global TOKEN, REFRESH
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--workers", type=int, default=10)
    a = ap.parse_args()
    REFRESH = a.refresh
    TOKEN = gh_token()
    print(f"token: {'yes' if TOKEN else 'NO (60 req/h anonymous limit)'}", flush=True)

    cands = sorted(collect_candidates().values(), key=lambda c: c["user"].lower())
    if a.limit:
        cands = cands[: a.limit]
    print(f"candidates: {len(cands)}", flush=True)

    profiles: list[dict] = []
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, p in enumerate(ex.map(fetch_profile, cands), 1):
            profiles.append(p)
            if i % 20 == 0 or i == len(cands):
                print(f"  profiles {i}/{len(cands)}", flush=True)

    urls = sorted({o["url"] for p in profiles for o in p.get("images", []) if o["url"]})
    print(f"unique images: {len(urls)}", flush=True)
    images: dict[str, dict] = {}
    with cf.ThreadPoolExecutor(a.workers) as ex:
        for i, res in enumerate(ex.map(analyze_image, urls), 1):
            images[res["url"]] = res
            if i % 100 == 0 or i == len(urls):
                print(f"  images {i}/{len(urls)}", flush=True)

    flaky = [u for u, r in images.items()
             if r.get("fail_reason") in TRANSIENT and not r.get("rechecked")]
    if flaky:
        print(f"rechecking {len(flaky)} timeouts/resets slowly, 30s budget each", flush=True)
        with cf.ThreadPoolExecutor(RECHECK_WORKERS) as ex:
            for res in ex.map(recheck, flaky):
                images[res["url"]] = res
        still = sum(images[u].get("fail_reason") is not None for u in flaky)
        print(f"  {len(flaky) - still} recovered, {still} still failing", flush=True)

    for p in profiles:
        for o in p.get("images", []):
            img = images.get(o["url"])
            if img:
                o["mobile_px"] = legibility(o, img, MOBILE_R)
                o["mobile_best_px"] = legibility(o, img, MOBILE_R, "max_font")
                o["desktop_px"] = legibility(o, img, DESKTOP_R)

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "profiles.json").write_text(json.dumps(profiles, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    (OUT / "images.json").write_text(json.dumps(images, separators=(",", ":"), sort_keys=True), encoding="utf-8")
    live = sum(p["status"] == "live" for p in profiles)
    print(f"done: {live}/{len(profiles)} live profiles, {len(images)} images -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
