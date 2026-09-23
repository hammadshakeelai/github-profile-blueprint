#!/usr/bin/env python3
"""Collect the raw material for the README book: every kind of thing people put
in a GitHub profile README, weighted toward the rare and exotic.

    python tools/book/collect.py tools      # the tool ecosystem, by topic and keyword
    python tools/book/collect.py lists      # tools named in curated awesome-lists
    python tools/book/collect.py exotic     # code search across real profile repos
    python tools/book/collect.py all

Writes docs/book/data/{tools,lists,exotic}.json. Uses `gh api`, so it runs as
whoever `gh auth status` says; search is rate-limited (30/min for repositories,
10/min for code) and this script paces itself to stay under both.

Only public metadata and links are stored — never README bodies.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "docs" / "book" / "data"


GH = shutil.which("gh") or "gh"


def gh(endpoint: str) -> dict | list | None:
    # Argument list, no shell: endpoints carry query strings, and some values
    # (download URLs) come from API responses rather than from this file.
    r = subprocess.run([GH, "api", "-H", "Accept: application/vnd.github+json", endpoint],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        if "rate limit" in (r.stderr + r.stdout).lower():
            print("  rate limited — waiting 60s", flush=True)
            time.sleep(60)
            return gh(endpoint)
        return None
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        return None


# --------------------------------------------------------------------------- #
# 1 · The tool ecosystem — repositories that make things for profile READMEs
# --------------------------------------------------------------------------- #
TOPICS = ["github-profile-readme", "profile-readme", "readme-profile", "github-readme",
          "readme-stats", "github-readme-stats", "readme-generator", "profile-readme-generator",
          "github-profile", "readme-template", "contribution-graph", "github-contributions",
          "readme-svg", "dynamic-readme", "readme-badges", "github-stats", "awesome-readme"]
KEYWORDS = ['"profile readme" in:description', '"github profile" svg in:description',
            '"for your github profile" in:description', '"your profile readme" in:description',
            '"README" "dynamically" in:description', '"contribution graph" in:description',
            '"readme" "github action" "profile" in:description']


def collect_tools() -> None:
    seen: dict[str, dict] = {}
    queries = [f"topic:{t}" for t in TOPICS] + KEYWORDS
    for q in queries:
        for page in (1, 2):
            res = gh(f"search/repositories?q={quote(q)}&sort=stars&order=desc&per_page=100&page={page}")
            items = (res or {}).get("items") or []
            for r in items:
                seen.setdefault(r["full_name"], {
                    "repo": r["full_name"], "url": r["html_url"],
                    "desc": (r.get("description") or "")[:240], "stars": r["stargazers_count"],
                    "topics": r.get("topics") or [], "pushed": r["pushed_at"][:10],
                    "archived": r.get("archived", False), "homepage": r.get("homepage") or "",
                    "found_by": [],
                })["found_by"].append(q)
            print(f"  {q[:48]:48} p{page}: {len(items):3}  (total {len(seen)})", flush=True)
            time.sleep(2.2)                           # 30/min search budget
            if len(items) < 100:
                break
    out = sorted(seen.values(), key=lambda r: -r["stars"])
    (DATA / "tools.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"tools: {len(out)} repositories")


# --------------------------------------------------------------------------- #
# 2 · Curated lists — the tools people bothered to recommend
# --------------------------------------------------------------------------- #
LISTS = ["rzashakeri/beautify-github-profile", "abhisheknaiidu/awesome-github-profile-readme",
         "EddieHubCommunity/awesome-github-profiles", "kautukkundan/Awesome-Profile-README-templates",
         "coderjojo/creative-profile-readme", "DenverCoder1/github-readme-tools",
         "matiassingers/awesome-readme", "anmol098/waka-readme-stats",
         "Kaan-Ozer/awesome-github-profile-tools", "arturssmirnovs/github-profile-readme-generator"]
LINK = re.compile(r"\[([^\]]{1,80})\]\((https://github\.com/[\w.-]+/[\w.-]+)[/)#]?")


def collect_lists() -> None:
    found: dict[str, dict] = {}
    for lst in LISTS:
        meta = gh(f"repos/{lst}/readme")
        if not meta or "download_url" not in meta:
            print(f"  {lst}: no readme")
            continue
        url = meta["download_url"]
        if not url.startswith("https://raw.githubusercontent.com/"):
            print(f"  {lst}: unexpected download host, skipped")
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "profile-readme-book"})
        body = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
        section = "?"
        n = 0
        for line in body.splitlines():
            h = re.match(r"^#{2,4}\s+(.*)", line)
            if h:
                section = re.sub(r"[^\w &/+-]", "", h.group(1)).strip()[:60]
                continue
            for label, url in LINK.findall(line):
                repo = "/".join(url.split("/")[3:5])
                if repo.lower() == lst.lower():
                    continue
                e = found.setdefault(repo.lower(), {"repo": repo, "label": label.strip(),
                                                    "lists": [], "sections": []})
                if lst not in e["lists"]:
                    e["lists"].append(lst)
                if section not in e["sections"]:
                    e["sections"].append(section)
                n += 1
        print(f"  {lst:48} {n:4} links", flush=True)
    out = sorted(found.values(), key=lambda e: -len(e["lists"]))
    (DATA / "lists.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"lists: {len(out)} distinct repositories named")


# --------------------------------------------------------------------------- #
# 3 · Exotic features — code search across real username/username READMEs
# --------------------------------------------------------------------------- #
# Each probe is something rare enough that its presence in a profile README is
# itself worth an entry. `filename:README.md` plus a check that the repository
# name equals its owner keeps only profile READMEs.
PROBES = {
    # GitHub-native renderers most people don't know work inside a README
    "geojson-map": '"```geojson"', "topojson-map": '"```topojson"', "stl-3d-model": '"```stl"',
    "mermaid-diagram": '"```mermaid"', "math-block": '"$$" "\\\\frac"',
    "alert-callouts": '"[!NOTE]"', "footnotes": '"[^1]:"', "details-collapse": '"<details>" "<summary>"',
    "kbd-keys": '"<kbd>"', "sub-sup": '"<sup>" "<sub>"',
    # Uploaded media
    "video-upload": '"user-attachments/assets"', "mp4-video": '".mp4"', "audio": '".mp3"',
    # Interactivity via issues and links
    "issue-driven-game": '"issues/new?title="', "chess-via-issues": '"chess" "issues/new"',
    "tic-tac-toe": '"tic-tac-toe" OR "tictactoe"', "connect-four": '"connect4" OR "connect-four"',
    "guestbook": '"guestbook"', "wordle-in-readme": '"wordle"', "minesweeper": '"minesweeper"',
    "reversi": '"reversi" OR "othello"', "sudoku": '"sudoku"', "rock-paper-scissors": '"rock paper scissors"',
    "pokemon-game": '"pokemon" "issues/new"', "voting-poll": '"vote" "issues/new"',
    # Contribution-graph art
    "snake": '"github-contribution-grid-snake"', "pacman": '"pacman-contribution-graph"',
    "3d-contrib": '"profile-3d-contrib"', "breakout": '"github-breakout" OR "breakout.svg"',
    "space-shooter": '"space-shooter"', "game-of-life": '"game-of-life" OR "gameoflife"',
    "tetris": '"tetris"', "skyline": '"skyline"', "isometric-contrib": '"isometric"',
    # Live data pipes
    "spotify-now-playing": '"spotify" "now-playing" OR "spotify-github-profile"',
    "lastfm": '"last.fm" OR "lastfm"', "wakatime": '"wakatime"', "blog-post-workflow": '"BLOG-POST-LIST"',
    "youtube-feed": '"YOUTUBE-VIDEO-LIST" OR "youtube-cards"', "leetcode": '"leetcode" "card"',
    "codeforces": '"codeforces"', "monkeytype": '"monkeytype"', "duolingo": '"duolingo"',
    "chesscom-lichess": '"lichess" OR "chess.com"', "steam": '"steam" "profile" "card"',
    "anilist-myanimelist": '"anilist" OR "myanimelist"', "goodreads": '"goodreads"',
    "strava": '"strava"', "discord-presence": '"lanyard"', "weather": '"weather" "svg"',
    "quote-of-the-day": '"quote" "readme" "svg"', "jokes": '"readme-jokes"',
    "hacker-news": '"hacker news"', "star-history": '"star-history.com"', "repobeats": '"repobeats"',
    "metrics-plugins": '"metrics.plugins"', "trophies": '"github-profile-trophy"',
    "profile-summary-cards": '"profile-summary-cards"', "activity-graph": '"activity-graph"',
    "visitor-map": '"visitor" "map"', "clustrmaps": '"clustrmaps"',
    # Art and oddities
    "ascii-art": '"```" "⠀" OR "█▀▀"', "rickroll": '"dQw4w9WgXcQ"', "konami": '"konami"',
    "qr-code": '"qr" "code" "svg"', "morse": '"morse"', "binary-bio": '"01001000"',
    "emoji-art": '"🟩🟩🟩"', "hidden-comment": '"<!-- hidden"', "marquee-tag": '"<marquee"',
    "readme-in-another-language": '"<div dir=\\"rtl\\">"', "pixel-art": '"pixel art"',
    "neofetch": '"neofetch"', "fastfetch": '"fastfetch"', "terminal-svg": '"terminal" "typing" "svg"',
    "resume-in-readme": '"resume" "json"', "json-bio": '"const me = {" OR "\\"name\\":"',
    "python-class-bio": '"class " "def __init__(self)"', "yaml-bio": '"```yaml" "name:"',
    "sql-bio": '"SELECT" "FROM developer"', "rust-bio": '"fn main()"',
    "timezone-clock": '"timezone" "clock"', "age-counter": '"years old" "svg"',
    "tip-jar": '"buymeacoffee" OR "ko-fi"', "sponsors-wall": '"sponsorkit"',
    "all-contributors": '"ALL-CONTRIBUTORS-LIST"', "gh-sponsors-button": '"github.com/sponsors"',
    "dependabot-badge": '"dependabot"', "rss": '"rss" "feed"',
    "random-image-per-load": '"random" "unsplash"', "cats-api": '"cataas" OR "thecatapi"',
    "dog-api": '"dog.ceo"', "gif-banner": '".gif" "banner"', "lottie": '"lottie"',
    "readme-changes-daily": '"updated daily" OR "last updated"',
}


def collect_exotic() -> None:
    out: dict[str, dict] = {}
    for key, probe in PROBES.items():
        q = f"{probe} filename:README.md"
        res = gh(f"search/code?q={quote(q)}&per_page=100")
        items = (res or {}).get("items") or []
        profiles = []
        for it in items:
            repo = it["repository"]
            owner = repo["owner"]["login"]
            if repo["name"].lower() == owner.lower() and it["path"].lower() == "readme.md":
                profiles.append(owner)
        uniq = sorted(set(profiles))
        out[key] = {"probe": probe, "total_hits": (res or {}).get("total_count", 0),
                    "profiles": uniq[:40], "profile_count_in_sample": len(uniq)}
        print(f"  {key:26} hits {out[key]['total_hits']:>7}  profiles-in-top-100 {len(uniq):3}",
              flush=True)
        time.sleep(6.5)                               # 10/min code-search budget
    (DATA / "exotic.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"exotic: {len(out)} probes")


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("tools", "all"):
        collect_tools()
    if what in ("lists", "all"):
        collect_lists()
    if what in ("exotic", "all"):
        collect_exotic()


if __name__ == "__main__":
    main()
