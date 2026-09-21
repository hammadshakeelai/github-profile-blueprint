#!/usr/bin/env python3
"""Measure how long a pushed SVG change takes to reach viewers.

    python tools/matrix/cache_probe.py [--rounds 2]

A profile README embeds a committed SVG by branch path, which GitHub serves from
raw.githubusercontent.com behind a CDN. This measures the real delay between
`git push` and the new bytes being served:

  1. warm the CDN by fetching the current version of a probe file,
  2. commit and push a new token on a throwaway branch (probe/cache),
  3. poll the branch URL until the new token is served, and compare with the
     commit-pinned URL (…/<sha>/…), which is immutable and never stale.

Writes docs/matrix/cache.json. Uses a separate branch so probe commits never
touch the research branch's history.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPO = "hammadshakeelai/github-profile-blueprint"
REMOTE = "mirror"
BRANCH = "probe/cache"
PATH = "cache-probe.svg"
POLL_EVERY, GIVE_UP = 10, 900


def git(*args, cwd) -> str:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()


def fetch(url: str) -> tuple[str, dict]:
    req = urllib.request.Request(url, headers={"User-Agent": "profile-readme-survey/1.0"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace"), {k.lower(): v for k, v in r.headers.items()}


def svg(token: str) -> str:
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 60" width="400" height="60">'
            f'<rect width="400" height="60" fill="#0d1117"/>'
            f'<text x="16" y="38" font-family="ui-monospace, monospace" font-size="22" fill="#3fb950">{token}</text></svg>\n')


def push_token(work: Path, token: str) -> str:
    (work / PATH).write_text(svg(token), encoding="utf-8")
    git("add", PATH, cwd=work)
    git("commit", "-q", "-m", f"probe: {token}", cwd=work)
    git("push", "-q", REMOTE, f"HEAD:{BRANCH}", cwd=work)
    return git("rev-parse", "HEAD", cwd=work)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=2)
    a = ap.parse_args()
    branch_url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{PATH}"
    remote_url = git("remote", "get-url", REMOTE, cwd=ROOT)

    with tempfile.TemporaryDirectory(prefix="probe-") as tmp:
        work = Path(tmp)
        git("init", "-q", cwd=work)
        git("remote", "add", REMOTE, remote_url, cwd=work)
        # an orphan history that holds nothing but the probe file
        git("checkout", "-q", "--orphan", "probe", cwd=work)
        push_token(work, f"seed-{uuid.uuid4().hex[:8]}")
        time.sleep(5)

        rounds = []
        for n in range(a.rounds):
            # warm: make sure the CDN edge is holding the *current* version
            old, hdr = fetch(branch_url)
            token = f"t{n}-{uuid.uuid4().hex[:8]}"
            t0 = time.monotonic()
            sha = push_token(work, token)
            pinned_url = f"https://raw.githubusercontent.com/{REPO}/{sha}/{PATH}"
            pinned_at = branch_at = None
            polls = 0
            while time.monotonic() - t0 < GIVE_UP and (pinned_at is None or branch_at is None):
                polls += 1
                if pinned_at is None:
                    try:
                        if token in fetch(pinned_url)[0]:
                            pinned_at = round(time.monotonic() - t0, 1)
                    except Exception:
                        pass
                if branch_at is None and token in fetch(branch_url)[0]:
                    branch_at = round(time.monotonic() - t0, 1)
                if pinned_at is None or branch_at is None:
                    time.sleep(POLL_EVERY)
            rounds.append({"token": token, "sha": sha, "warm_cache_control": hdr.get("cache-control"),
                           "warm_x_cache": hdr.get("x-cache"), "branch_url_seconds": branch_at,
                           "pinned_url_seconds": pinned_at, "polls": polls})
            print(f"round {n + 1}: branch URL updated after {branch_at}s, "
                  f"commit-pinned URL after {pinned_at}s ({hdr.get('cache-control')})", flush=True)

    out = ROOT / "docs" / "matrix" / "cache.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"measured_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                               "branch_url": branch_url, "poll_every_seconds": POLL_EVERY,
                               "rounds": rounds}, indent=1), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
