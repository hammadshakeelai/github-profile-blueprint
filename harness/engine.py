#!/usr/bin/env python3
"""
ProfileHarness Engine: The Autonomous GitHub Profile Compiler & Architecture System
Compiles declarative profile.config.json into a production-grade README.md with
Git-native SVGs, Bento Grid layouts, interactive issue RPCs, and GitHub-sanitizer linting.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape as xml_escape, quoteattr as xml_quoteattr
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output even on Windows terminals with legacy code pages
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = Path(__file__).resolve().parent / "profile.config.json"
ASSETS_DIR = ROOT_DIR / "assets"
README_PATH = ROOT_DIR / "README.md"

STATE_SHA_REGEX = re.compile(r"<!--\s*HARNESS:STATE_SHA\s+([a-f0-9]{64})\s*-->")
EXPECTED_ASSETS = [
    "banner-dark.svg",
    "banner-light.svg",
    "dashboard.svg",
    "terminal-typing.svg",
    "pet.svg",
    "quantum-coherence.svg",
    "synaptic-network.svg",
]

def load_config():
    if not CONFIG_PATH.exists():
        print(f"Error: Config file not found at {CONFIG_PATH}", file=sys.stderr)
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

def compute_state_hash(config: dict, metrics: dict) -> str:
    """Computes a deterministic SHA-256 hash over compiler code, config, and raw telemetry."""
    hasher = hashlib.sha256()
    # 1. Compiler code identity (invalidates cache on code edits)
    hasher.update(Path(__file__).read_bytes())
    # 2. Canonicalized configuration
    config_bytes = json.dumps(config, sort_keys=True, separators=(",", ":")).encode("utf-8")
    hasher.update(config_bytes)
    # 3. Canonicalized dynamic telemetry inputs (strictly excluding updated_at)
    telemetry_input = {
        "recent_commits": metrics.get("recent_commits"),
        "ci_reliability": metrics.get("ci_reliability"),
    }
    telemetry_bytes = json.dumps(telemetry_input, sort_keys=True, separators=(",", ":")).encode("utf-8")
    hasher.update(telemetry_bytes)
    return hasher.hexdigest()

def extract_state_hash_from_readme() -> str | None:
    """Extracts the recorded state hash from line 1 of README.md without reading the full file."""
    if not README_PATH.exists():
        return None
    try:
        with open(README_PATH, "r", encoding="utf-8") as f:
            header = f.read(1024)
        match = STATE_SHA_REGEX.search(header)
        return match.group(1) if match else None
    except Exception:
        return None

def verify_asset_integrity() -> bool:
    """Fast pre-flight check verifying all required assets exist and have non-zero size."""
    for asset in EXPECTED_ASSETS:
        p = ASSETS_DIR / asset
        if not p.exists() or p.stat().st_size == 0:
            return False
    return True

def extract_dynamic_section(tag: str) -> str | None:
    """Extracts content within <!-- TAG:START --> and <!-- TAG:END --> from existing README.md."""
    if not README_PATH.exists():
        return None
    try:
        content = README_PATH.read_text(encoding="utf-8")
        pattern = re.compile(rf"(<!--\s*{tag}:START\s*-->.*?<!--\s*{tag}:END\s*-->)", re.DOTALL)
        match = pattern.search(content)
        return match.group(1) if match else None
    except Exception:
        return None

def fetch_workflow_reliability(
    owner: str,
    repo: str,
    token: str | None = None,
    workflow_file: str | None = None,
    window_size: int = 30,
) -> dict:
    """
    Fetches real-time GitHub Actions workflow run telemetry and computes
    the rolling empirical pass rate percentage over the last N decisive runs.
    """
    default_telemetry = {
        "ci_reliability": 99.8,
        "ci_status_text": "OPTIMAL (Zero failures)",
        "evaluated_runs": 0,
        "success_count": 0,
        "failure_count": 0,
        "cancelled_count": 0,
    }

    if workflow_file:
        url = (
            f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_file}/runs"
            f"?branch=main&per_page={window_size}"
        )
    else:
        url = (
            f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
            f"?branch=main&exclude_pull_requests=true&per_page={window_size}"
        )

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "ProfileHarness-Engine",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            runs = data.get("workflow_runs", [])
    except Exception:
        return default_telemetry

    current_run_id = int(os.environ.get("GITHUB_RUN_ID", 0))
    success_count = 0
    failure_count = 0
    cancelled_count = 0

    for run in runs:
        run_id = run.get("id")
        status = run.get("status")
        conclusion = run.get("conclusion")

        # Exclude active/current executing workflow instance
        if run_id == current_run_id or status != "completed":
            continue

        if conclusion == "success":
            success_count += 1
        elif conclusion in ("failure", "timed_out"):
            failure_count += 1
        elif conclusion == "cancelled":
            cancelled_count += 1

    total_decisive = success_count + failure_count

    if total_decisive == 0:
        reliability = 100.0
        status_text = "OPTIMAL (Zero failures)"
    else:
        reliability = round((success_count / total_decisive) * 100.0, 1)
        if failure_count == 0:
            status_text = "OPTIMAL (Zero failures)"
        elif reliability >= 98.0:
            status_text = "OPTIMAL (High availability)"
        elif reliability >= 95.0:
            status_text = "STABLE (Minor flakes)"
        else:
            status_text = f"DEGRADED ({failure_count} failures)"

    return {
        "ci_reliability": reliability,
        "ci_status_text": status_text,
        "evaluated_runs": total_decisive,
        "success_count": success_count,
        "failure_count": failure_count,
        "cancelled_count": cancelled_count,
    }

def get_previous_sync_state():
    """Extracts previous telemetry metrics from README.md to preserve determinism."""
    if not README_PATH.exists():
        return None, None, None
    try:
        txt = README_PATH.read_text(encoding="utf-8")
        commits_match = re.search(r"\|\s*Recent Git Commits\s*\|\s*(\d+)\s*\|", txt)
        rel_match = re.search(r"\|\s*Pipeline Reliability\s*\|\s*([\d.]+)%\s*\|", txt)
        sync_match = re.search(r"\|\s*Last Engine Sync\s*\|\s*([^|]+?)\s*\|", txt)
        prev_commits = int(commits_match.group(1)) if commits_match else None
        prev_rel = float(rel_match.group(1)) if rel_match else None
        prev_sync = sync_match.group(1).strip() if sync_match else None
        return prev_commits, prev_rel, prev_sync
    except Exception:
        return None, None, None

def fetch_github_metrics(username: str, token: str | None = None) -> dict:
    """Fetches real-time commit and CI telemetry from GitHub APIs."""
    metrics = {
        "recent_commits": 128,
        "ci_reliability": 99.8,
        "ci_status_text": "OPTIMAL (Zero failures)",
    }

    try:
        headers = {"User-Agent": "ProfileHarness-Engine"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
            
        url = f"https://api.github.com/users/{username}/events/public"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            events = json.loads(resp.read().decode())
            push_events = [e for e in events if e.get("type") == "PushEvent"]
            total_commits = sum(len(e.get("payload", {}).get("commits", [])) for e in push_events)
            if total_commits > 0:
                metrics["recent_commits"] = total_commits
    except Exception as e:
        print(f"Notice: Telemetry fallback engaged ({e})")

    # Fetch live CI workflow reliability
    repo_slug = os.environ.get("GITHUB_REPOSITORY", f"{username}/{username}")
    owner, repo = repo_slug.split("/", 1) if "/" in repo_slug else (username, username)
    ci_data = fetch_workflow_reliability(owner, repo, token, window_size=30)
    metrics["ci_reliability"] = ci_data["ci_reliability"]
    metrics["ci_status_text"] = ci_data["ci_status_text"]

    # Determine updated_at with strict idempotency guarantees:
    if "SOURCE_DATE_EPOCH" in os.environ:
        epoch = int(os.environ["SOURCE_DATE_EPOCH"])
        metrics["updated_at"] = datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
    else:
        prev_commits, prev_rel, prev_sync = get_previous_sync_state()
        if (
            prev_commits is not None
            and prev_rel is not None
            and prev_sync is not None
            and metrics["recent_commits"] == prev_commits
            and metrics["ci_reliability"] == prev_rel
        ):
            metrics["updated_at"] = prev_sync
        else:
            metrics["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    return metrics

def render_svg_dashboard(config: dict, metrics: dict):
    """Renders a zero-dependency Git-native telemetry SVG card."""
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    svg_path = ASSETS_DIR / "dashboard.svg"
    
    commits = metrics["recent_commits"]
    sync_time = metrics["updated_at"]
    ci_rel = float(metrics.get("ci_reliability", 99.8))
    ci_bar_width = max(0, min(180, int(round(180 * (ci_rel / 100.0)))))
    ci_status = xml_escape(metrics.get("ci_status_text", "OPTIMAL").split()[0])
    labels = config["modules"]["git_native_dashboard"]["metric_labels"]
    metric_1_label = xml_escape(str(labels.get("metric_1", "Recent Git Commits")))
    metric_2_label = xml_escape(str(labels.get("metric_2", "CI Pipeline Reliability")))
    metric_3_label = xml_escape(str(labels.get("metric_3", "Telemetry Status")))

    status_color = "#22c55e" if ci_rel >= 95.0 else "#ef4444"

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 140" width="650" height="140">
  <defs>
    <style>
      .card {{ fill: #0b0f19; stroke: #1e293b; stroke-width: 1.5; rx: 10px; }}
      .header {{ font-family: 'JetBrains Mono', -apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', monospace; font-size: 13px; fill: #38bdf8; font-weight: bold; }}
      .label {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif; font-size: 11px; fill: #94a3b8; }}
      .value {{ font-family: 'JetBrains Mono', -apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', monospace; font-size: 18px; font-weight: bold; fill: #f8fafc; }}
      .bar-bg {{ fill: #1e293b; rx: 3px; }}
      .bar-fill {{ fill: #38bdf8; rx: 3px; }}
      .status-dot {{ fill: {status_color}; }}
    </style>
  </defs>
  <rect class="card" x="2" y="2" width="646" height="136"/>
  <circle class="status-dot" cx="24" cy="24" r="4"/>
  <text class="header" x="38" y="28">SYSTEM TELEMETRY // PRODUCTION METRICS</text>
  
  <g transform="translate(24, 52)">
    <text class="label" x="0" y="0">{metric_1_label}</text>
    <text class="value" x="0" y="22">{commits}</text>
    <rect class="bar-bg" x="0" y="32" width="180" height="5"/>
    <rect class="bar-fill" x="0" y="32" width="{min(180, commits * 2)}" height="5"/>
  </g>
  
  <g transform="translate(234, 52)">
    <text class="label" x="0" y="0">{metric_2_label}</text>
    <text class="value" x="0" y="22">{ci_rel}%</text>
    <rect class="bar-bg" x="0" y="32" width="180" height="5"/>
    <rect class="bar-fill" x="0" y="32" width="{ci_bar_width}" height="5"/>
  </g>

  <g transform="translate(444, 52)">
    <text class="label" x="0" y="0">{metric_3_label}</text>
    <text class="value" x="0" y="22">{ci_status}</text>
    <rect class="bar-bg" x="0" y="32" width="180" height="5"/>
    <rect class="bar-fill" x="0" y="32" width="180" height="5"/>
  </g>
  
  <text x="24" y="120" font-family="-apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', monospace" font-size="10" fill="#64748b">SYNCHRONIZED: {sync_time} UTC // GIT-NATIVE ZERO CAMO LATENCY</text>
</svg>"""
    svg_path.write_text(svg, encoding="utf-8")
    print(f"Generated: {svg_path}")

def render_svg_banners(config: dict):
    """Renders responsive Dark and Light mode hero banner SVGs."""
    profile = config["profile"]
    name = xml_escape(profile["name"])
    headline_upper = xml_escape(profile["headline"].upper())
    
    # Dark Banner
    dark_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240" width="1200" height="240">
  <defs>
    <linearGradient id="dark-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#090d16" />
      <stop offset="50%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38bdf8" />
      <stop offset="100%" stop-color="#818cf8" />
    </linearGradient>
    <pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#1e293b" stroke-width="0.8" opacity="0.4"/>
    </pattern>
  </defs>
  <rect width="1200" height="240" fill="url(#dark-grad)" rx="12"/>
  <rect width="1200" height="240" fill="url(#grid)" rx="12"/>
  <rect x="0" y="236" width="1200" height="4" fill="url(#accent)"/>
  <circle cx="40" cy="35" r="6" fill="#ef4444" opacity="0.8"/>
  <circle cx="60" cy="35" r="6" fill="#eab308" opacity="0.8"/>
  <circle cx="80" cy="35" r="6" fill="#22c55e" opacity="0.8"/>
  <text x="40" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="38" font-weight="800" fill="#f8fafc">{name}</text>
  <text x="40" y="150" font-family="'JetBrains Mono', monospace" font-size="16" font-weight="600" fill="url(#accent)">{headline_upper}</text>
  <text x="40" y="185" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="14" fill="#94a3b8">Rust • Go • Linux Kernel &amp; eBPF Telemetry • High-Throughput Distributed State Machines</text>
</svg>"""
    (ASSETS_DIR / "banner-dark.svg").write_text(dark_svg, encoding="utf-8")

    # Light Banner
    light_svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 240" width="1200" height="240">
  <defs>
    <linearGradient id="light-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#f8fafc" />
      <stop offset="50%" stop-color="#f1f5f9" />
      <stop offset="100%" stop-color="#e2e8f0" />
    </linearGradient>
    <linearGradient id="light-accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0284c7" />
      <stop offset="100%" stop-color="#4f46e5" />
    </linearGradient>
    <pattern id="light-grid" width="30" height="30" patternUnits="userSpaceOnUse">
      <path d="M 30 0 L 0 0 0 30" fill="none" stroke="#cbd5e1" stroke-width="0.8" opacity="0.6"/>
    </pattern>
  </defs>
  <rect width="1200" height="240" fill="url(#light-grad)" rx="12"/>
  <rect width="1200" height="240" fill="url(#light-grid)" rx="12"/>
  <rect x="0" y="236" width="1200" height="4" fill="url(#light-accent)"/>
  <circle cx="40" cy="35" r="6" fill="#ef4444" opacity="0.8"/>
  <circle cx="60" cy="35" r="6" fill="#eab308" opacity="0.8"/>
  <circle cx="80" cy="35" r="6" fill="#22c55e" opacity="0.8"/>
  <text x="40" y="110" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="38" font-weight="800" fill="#0f172a">{name}</text>
  <text x="40" y="150" font-family="'JetBrains Mono', monospace" font-size="16" font-weight="600" fill="url(#light-accent)">{headline_upper}</text>
  <text x="40" y="185" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="14" fill="#475569">Rust • Go • Linux Kernel &amp; eBPF Telemetry • High-Throughput Distributed State Machines</text>
</svg>"""
    (ASSETS_DIR / "banner-light.svg").write_text(light_svg, encoding="utf-8")
    print("Generated: assets/banner-dark.svg and assets/banner-light.svg")

def render_virtual_pet_svg(config: dict, metrics: dict):
    """Renders the commit-fed Tamagotchi virtual pet SVG badge."""
    commits = metrics["recent_commits"]
    pet = config["modules"].get("virtual_pet", {})
    name = pet.get("pet_name", "Byte")

    if commits >= 50:
        mood = "Euphoric & Thriving!"
        face = "(づ｡◕‿‿◕｡)づ"
        level = "Lvl 3 (Cyber Evolution)"
        color = "#22c55e"
    elif commits >= 15:
        mood = "Healthy & Content"
        face = "(•‿•)"
        level = "Lvl 2 (Active Stage)"
        color = "#38bdf8"
    else:
        mood = "Hungry for Commits!"
        face = "(╯°□°)╯"
        level = "Lvl 1 (Starving)"
        color = "#f59e0b"

    face_escaped = xml_escape(face)
    name_upper = xml_escape(name.upper())
    level_escaped = xml_escape(level)
    mood_upper = xml_escape(mood.upper())

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 80" width="320" height="80">
  <defs>
    <style>
      .pet-card {{ fill: #0d1117; stroke: #30363d; stroke-width: 1.5; rx: 8px; }}
      .pet-face {{ font-family: monospace; font-size: 20px; fill: {color}; font-weight: bold; }}
      .pet-name {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; font-size: 13px; font-weight: bold; fill: #f0f6fc; }}
      .pet-status {{ font-family: monospace; font-size: 10px; fill: #8b949e; }}
      .pet-pulse {{ fill: {color}; animation: pulse 1.5s infinite; }}
      @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
    </style>
  </defs>
  <rect class="pet-card" x="1" y="1" width="318" height="78"/>
  <text class="pet-face" x="20" y="48">{face_escaped}</text>
  <g transform="translate(140, 24)">
    <text class="pet-name" x="0" y="0">PET: {name_upper}</text>
    <circle class="pet-pulse" cx="95" cy="-4" r="3"/>
    <text class="pet-status" x="0" y="20">{level_escaped}</text>
    <text class="pet-status" x="0" y="38">STATUS: {mood_upper}</text>
  </g>
</svg>"""
    (ASSETS_DIR / "pet.svg").write_text(svg, encoding="utf-8")
    print("Generated: assets/pet.svg")

def render_quantum_coherence_svg(config: dict, metrics: dict):
    """Renders an abstract Quantum Coherence & Entropic Field Hologram SVG."""
    commits = metrics["recent_commits"]
    entropy = round(0.124 + (commits % 17) * 0.005, 3)
    phase = round(98.2 + (commits % 7) * 0.25, 1)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 200" width="650" height="200">
  <defs>
    <style>
      .holo-card {{ fill: #07090e; stroke: #1e293b; stroke-width: 1.5; rx: 12px; }}
      .hud-title {{ font-family: 'JetBrains Mono', -apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', monospace; font-size: 12px; fill: #38bdf8; font-weight: bold; letter-spacing: 1px; }}
      .hud-val {{ font-family: 'JetBrains Mono', -apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', monospace; font-size: 15px; fill: #f8fafc; font-weight: bold; }}
      .hud-sub {{ font-family: 'JetBrains Mono', -apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', monospace; font-size: 10px; fill: #64748b; }}
      
      .orbit-ring-1 {{
        transform-box: fill-box;
        transform-origin: 530px 100px;
        animation: spin1 16s linear infinite;
      }}
      .orbit-ring-2 {{
        transform-box: fill-box;
        transform-origin: 530px 100px;
        animation: spin2 22s linear infinite reverse;
      }}
      .orbit-ring-3 {{
        transform-box: fill-box;
        transform-origin: 530px 100px;
        animation: spin3 12s linear infinite;
      }}
      @keyframes spin1 {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
      @keyframes spin2 {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
      @keyframes spin3 {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
      
      .quantum-pulse {{
        animation: qpulse 2.5s infinite ease-in-out;
      }}
      @keyframes qpulse {{ 0%, 100% {{ opacity: 0.8; r: 6px; }} 50% {{ opacity: 0.3; r: 10px; }} }}

      @media (prefers-reduced-motion: reduce) {{
        * {{ animation: none !important; }}
      }}
    </style>
    <linearGradient id="quantum-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="#818cf8" stop-opacity="0.3"/>
    </linearGradient>
  </defs>

  <rect class="holo-card" x="2" y="2" width="646" height="196"/>

  <!-- Left: Telemetry Data Matrix -->
  <g transform="translate(24, 30)">
    <circle cx="4" cy="4" r="4" fill="#38bdf8"/>
    <text class="hud-title" x="16" y="8">QUANTUM COHERENCE &amp; ENTROPIC FIELD</text>

    <text class="hud-sub" x="0" y="38">STATE VECTOR |ψ⟩</text>
    <text class="hud-val" x="0" y="58">0.866|0⟩ + 0.500e^(iπ/3)|1⟩</text>

    <text class="hud-sub" x="0" y="88">PHASE COHERENCE</text>
    <text class="hud-val" x="0" y="108">{phase}% // ZERO DRIFT</text>

    <text class="hud-sub" x="0" y="136">SYSTEM ENTROPY</text>
    <text class="hud-val" x="0" y="154">{entropy} nats // OPTIMAL EQUILIBRIUM</text>
  </g>

  <!-- Divider Line -->
  <line x1="380" y1="20" x2="380" y2="180" stroke="#1e293b" stroke-dasharray="3 3"/>

  <!-- Right: Holographic Orbital Bloch Spheres -->
  <g class="orbit-ring-1">
    <ellipse cx="530" cy="100" rx="75" ry="32" fill="none" stroke="url(#quantum-grad)" stroke-width="1.5"/>
    <circle cx="605" cy="100" r="3" fill="#38bdf8"/>
  </g>

  <g class="orbit-ring-2">
    <ellipse cx="530" cy="100" rx="75" ry="32" fill="none" stroke="#818cf8" stroke-width="1.2" stroke-dasharray="6 4"/>
    <circle cx="455" cy="100" r="3" fill="#818cf8"/>
  </g>

  <g class="orbit-ring-3">
    <circle cx="530" cy="100" r="45" fill="none" stroke="#0ea5e9" stroke-width="1" stroke-dasharray="2 4"/>
    <circle cx="530" cy="55" r="3" fill="#22c55e"/>
  </g>

  <!-- Quantum Nucleus -->
  <circle class="quantum-pulse" cx="530" cy="100" r="6" fill="#38bdf8"/>
  <circle cx="530" cy="100" r="3" fill="#ffffff"/>
</svg>"""
    (ASSETS_DIR / "quantum-coherence.svg").write_text(svg, encoding="utf-8")
    print("Generated: assets/quantum-coherence.svg")

def render_synaptic_network_svg(config: dict, metrics: dict):
    """Renders an abstract Synaptic Neural Architecture graph with animated pulse transmissions."""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 650 180" width="650" height="180">
  <defs>
    <style>
      .synapse-card {{ fill: #07090e; stroke: #1e293b; stroke-width: 1.5; rx: 12px; }}
      .node-text {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; fill: #94a3b8; font-weight: bold; }}
      .title-text {{ font-family: 'JetBrains Mono', monospace; font-size: 12px; fill: #818cf8; font-weight: bold; letter-spacing: 1px; }}
      
      .synapse-wire {{
        stroke: #1e293b;
        stroke-width: 1.5;
      }}
      .synapse-pulse {{
        stroke: #38bdf8;
        stroke-width: 2;
        stroke-dasharray: 6 30;
        animation: firePulse 2.8s linear infinite;
      }}
      .synapse-pulse-fast {{
        stroke: #a855f7;
        stroke-width: 2;
        stroke-dasharray: 6 30;
        animation: firePulse 1.9s linear infinite;
      }}
      @keyframes firePulse {{
        0% {{ stroke-dashoffset: 60; }}
        100% {{ stroke-dashoffset: 0; }}
      }}
      .core-node {{ fill: #0f172a; stroke: #38bdf8; stroke-width: 2; }}
      .input-node {{ fill: #0f172a; stroke: #64748b; stroke-width: 1.5; }}
      .output-node {{ fill: #0f172a; stroke: #22c55e; stroke-width: 2; }}
    </style>
  </defs>

  <rect class="synapse-card" x="2" y="2" width="646" height="176"/>

  <text class="title-text" x="24" y="26">SYNAPTIC COMPUTATION &amp; KERNEL NEURAL FLOW</text>

  <!-- Connecting Synapse Lines (Background) -->
  <!-- Layer 1 to Layer 2 -->
  <line class="synapse-wire" x1="100" y1="55" x2="310" y2="70"/>
  <line class="synapse-wire" x1="100" y1="55" x2="310" y2="120"/>
  <line class="synapse-wire" x1="100" y1="105" x2="310" y2="70"/>
  <line class="synapse-wire" x1="100" y1="105" x2="310" y2="120"/>
  <line class="synapse-wire" x1="100" y1="150" x2="310" y2="120"/>

  <!-- Layer 2 to Layer 3 -->
  <line class="synapse-wire" x1="310" y1="70" x2="520" y2="65"/>
  <line class="synapse-wire" x1="310" y1="70" x2="520" y2="135"/>
  <line class="synapse-wire" x1="310" y1="120" x2="520" y2="65"/>
  <line class="synapse-wire" x1="310" y1="120" x2="520" y2="135"/>

  <!-- Animated Pulse Overlays -->
  <line class="synapse-pulse" x1="100" y1="55" x2="310" y2="70"/>
  <line class="synapse-pulse-fast" x1="100" y1="105" x2="310" y2="120"/>
  <line class="synapse-pulse" x1="310" y1="70" x2="520" y2="65"/>
  <line class="synapse-pulse-fast" x1="310" y1="120" x2="520" y2="135"/>

  <!-- Layer 1: Ingress Nodes -->
  <circle class="input-node" cx="100" cy="55" r="8"/>
  <text class="node-text" x="25" y="58">eBPF Telemetry</text>

  <circle class="input-node" cx="100" cy="105" r="8"/>
  <text class="node-text" x="35" y="108">io_uring WAL</text>

  <circle class="input-node" cx="100" cy="150" r="8"/>
  <text class="node-text" x="42" y="153">Socket IPC</text>

  <!-- Layer 2: Core Processing Nodes -->
  <circle class="core-node" cx="310" cy="70" r="10"/>
  <text class="node-text" x="326" y="74">Raft Consensus</text>

  <circle class="core-node" cx="310" cy="120" r="10"/>
  <text class="node-text" x="326" y="124">Lock-Free Shm</text>

  <!-- Layer 3: Output Quorum Nodes -->
  <circle class="output-node" cx="520" cy="65" r="9"/>
  <text class="node-text" x="536" y="69">Cluster Quorum</text>

  <circle class="output-node" cx="520" cy="135" r="9"/>
  <text class="node-text" x="536" y="139">Zero-Copy Stream</text>
</svg>"""
    (ASSETS_DIR / "synaptic-network.svg").write_text(svg, encoding="utf-8")
    print("Generated: assets/synaptic-network.svg")

def compile_readme(config: dict, metrics: dict, state_sha: str = "") -> str:
    """Compiles the full Markdown README adhering to 2026 Bento Grid best practices."""
    profile = config["profile"]
    username = profile["username"]
    sync_time = metrics["updated_at"]
    commits = metrics["recent_commits"]

    # Optional cross-link to the author's primary account. Rendered only when set,
    # so the link survives every rebuild instead of being overwritten by it.
    main_profile = profile.get("socials", {}).get("main_profile")
    main_profile_md = ""
    if main_profile:
        main_handle = main_profile.rstrip("/").split("/")[-1]
        main_profile_md = f"""
---

<p align="center">
  <a href="{main_profile}">
    <img src="https://img.shields.io/badge/Main_Profile-{main_handle}-38BDF8?style=for-the-badge&logo=github&logoColor=white" alt="Main profile: {main_handle}"/>
  </a>
</p>
"""

    # 1. Hero Picture
    hero_md = f"""<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./assets/banner-light.svg">
    <img alt="{profile['name']} Banner" src="./assets/banner-dark.svg" width="100%">
  </picture>
</p>"""

    # 2. Typing tagline
    typing_query = "%3B".join(urllib.parse.quote(line) for line in config["modules"]["hero_banner"]["typing_lines"])
    typing_md = f"""<p align="center">
  <a href="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=18&duration=2800&pause=1000&color=38BDF8&center=true&vCenter=true&width=550&lines={typing_query}">
    <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=18&duration=2800&pause=1000&color=38BDF8&center=true&vCenter=true&width=550&lines={typing_query}" alt="Typing Tagline" />
  </a>
</p>"""

    # 3. Terminal simulation
    terminal_md = f"""<p align="center">
  <img src="./assets/terminal-typing.svg" width="650" alt="Terminal Simulation"/>
</p>"""

    ci_rel_str = f"{metrics.get('ci_reliability', 99.8)}%"
    ci_status_str = metrics.get("ci_status_text", "OPTIMAL (Zero failures)")
    telemetry_md = f"""<!-- TELEMETRY:START -->
```text
+-----------------------------------------------------------------------------------+
| METRIC                    | VALUE             | STATUS                            |
+---------------------------+-------------------+-----------------------------------+
| Recent Git Commits        | {commits:<17} | ACTIVE                            |
| Pipeline Reliability      | {ci_rel_str:<17} | {ci_status_str:<33} |
| Last Engine Sync          | {sync_time:<17} | UTC SYNCHRONIZED                  |
+-----------------------------------------------------------------------------------+
```
<!-- TELEMETRY:END -->

<p align="center">
  <img src="./assets/dashboard.svg" width="650" alt="Telemetry Dashboard"/>
</p>"""

    # 5. Bento Grid Layout
    blocks = config["modules"]["bento_blocks"]
    bento_rows = []
    for i in range(0, len(blocks), 2):
        b1 = blocks[i]
        b2 = blocks[i+1] if i+1 < len(blocks) else None
        
        row = f"""  <tr>
    <td width="50%" valign="top">
      <h4>{b1['title']}</h4>
      <ul>
        {"".join(f"<li>{item}</li>" for item in b1['items'])}
      </ul>
    </td>"""
        if b2:
            row += f"""
    <td width="50%" valign="top">
      <h4>{b2['title']}</h4>
      <ul>
        {"".join(f"<li>{item}</li>" for item in b2['items'])}
      </ul>
    </td>"""
        row += "\n  </tr>"
        bento_rows.append(row)

    bento_table = f"""<table width="100%" cellspacing="0" cellpadding="8" border="0">
{chr(10).join(bento_rows)}
</table>"""

    # 6. Virtual Pet
    pet_md = f"""<p align="center">
  <img src="./assets/pet.svg" width="320" alt="Virtual Pet"/>
</p>"""

    # 7. Native Mermaid Architecture
    mermaid_md = """```mermaid
flowchart LR
  subgraph Cluster ["Bare-Metal Edge Nodes"]
    direction TB
    K3s["K3s Cluster"] --> Ingress["Traefik Zero-Trust"]
    Ingress --> eBPF["eBPF Telemetry Daemon"]
  end

  subgraph Consensus ["Distributed Consensus"]
    direction TB
    Raft["Raft Replication"] --> WAL["NVMe io_uring WAL"]
    WAL --> Shm["Lock-Free IPC Ring Buffer"]
  end

  Cluster <--> Consensus

  classDef darkNode fill:#0d1117,stroke:#38bdf8,stroke-width:1.5px,color:#f0f6fc;
  class K3s,Ingress,eBPF,Raft,WAL,Shm darkNode;
```"""

    # 8. Interactive Game, MUD Dungeon & Guestbook (Section-Preserving Splicing)
    existing_game = extract_dynamic_section("GAME")
    if existing_game:
        game_md = f"### 🎮 Community State Machine (Tic-Tac-Toe)\n\n{existing_game}"
    else:
        game_md = f"""### 🎮 Community State Machine (Tic-Tac-Toe)

<!-- GAME:START -->
**Current State**: Your turn! (Playing as **X**) — *Click an open tile to make your move via GitHub Issues:*

| Column 0 | Column 1 | Column 2 |
| :---: | :---: | :---: |
| [⬜ Play (0,0)](https://github.com/{username}/{username}/issues/new?title=ttt%7Cmove%7C0&body=Click+Submit+to+confirm+move.) | ❌ | [⬜ Play (0,2)](https://github.com/{username}/{username}/issues/new?title=ttt%7Cmove%7C2&body=Click+Submit+to+confirm+move.) |
| ⭕ | ❌ | ⭕ |
| [⬜ Play (2,0)](https://github.com/{username}/{username}/issues/new?title=ttt%7Cmove%7C6&body=Click+Submit+to+confirm+move.) | [⬜ Play (2,1)](https://github.com/{username}/{username}/issues/new?title=ttt%7Cmove%7C7&body=Click+Submit+to+confirm+move.) | ❌ |

*(Powered by Minimax bot running inside GitHub Actions. State preserved in repository.)*
<!-- GAME:END -->"""

    existing_mud = extract_dynamic_section("MUD")
    if existing_mud:
        mud_md = existing_mud
    else:
        mud_md = f"""<!-- MUD:START -->
### 🕹️ Git-Native Cyberpunk Dungeon (Multi-User Adventure)

**Current Location**: `Mainframe Core // Sector 7G`  
**Last Adventurer**: [@octocat](https://github.com/octocat) • **System Ticks**: `42`

> *A subterranean chamber housing three crystalline Raft consensus nodes. The air smells of ozone and liquid helium. Optical telemetry cables pulse with blue coherent light.*

**Available Actions**:  
[⚡ Ping Quorum Node](https://github.com/{username}/{username}/issues/new?title=mud%7Caction%7Cping&body=Click+Submit+new+issue+to+advance+the+dungeon.) • [🔍 Inspect Memory Ring Buffer](https://github.com/{username}/{username}/issues/new?title=mud%7Caction%7Cinspect&body=Click+Submit+new+issue+to+advance+the+dungeon.) • [🚪 Enter Engine Bay](https://github.com/{username}/{username}/issues/new?title=mud%7Cmove%7Cengine_bay&body=Click+Submit+new+issue+to+advance+the+dungeon.)

**Recent World Log**:  
> [2026-09-20] @octocat initialized the mainframe core.
> [2026-09-20] Telemetry daemon loaded 14 eBPF probes successfully.
<!-- MUD:END -->"""

    existing_guestbook = extract_dynamic_section("GUESTBOOK")
    if existing_guestbook:
        guestbook_entries = existing_guestbook
    else:
        guestbook_entries = """<!-- GUESTBOOK:START -->
| Date | Signer | Message |
| :--- | :--- | :--- |
| 2026-09-20 | [@octocat](https://github.com/octocat) | Welcome to GitHub Profile Architecture 2026! 🚀 |
| 2026-09-18 | [@systems-dev](https://github.com/systems-dev) | Loving the zero-latency Git-native dashboard. |
<!-- GUESTBOOK:END -->"""

    guestbook_md = f"""### 📖 Community Guestbook

Click below to sign my profile README! An automated GitHub Action will append your handle and message:

<p align="center">
  <a href="https://github.com/{username}/{username}/issues/new?title=guestbook%7CSign%7CYour+Name&body=Leave+your+message+here!+(Max+100+characters)">
    <img src="https://img.shields.io/badge/Sign_The_Guestbook-238636?style=for-the-badge&logo=github&logoColor=white" alt="Sign Guestbook"/>
  </a>
</p>

{guestbook_entries}"""

    # 9. Abstract Frontier: Quantum Coherence & Synaptic Flow
    abstract_md = """---

### ⚛️ Abstract Frontier: Quantum Coherence & State Vector

<p align="center">
  <img src="./assets/quantum-coherence.svg" width="650" alt="Quantum Coherence Hologram"/>
</p>

---

### 🧠 Synaptic Kernel Neural Flow (Live Pulse Architecture)

<p align="center">
  <img src="./assets/synaptic-network.svg" width="650" alt="Synaptic Neural Architecture"/>
</p>"""

    # 10. Assembly
    sha_header = f"<!-- HARNESS:STATE_SHA {state_sha} -->\n" if state_sha else ""
    full_readme = f"""{sha_header}{hero_md}

{typing_md}

---

### 🖥️ Systems & Architecture HUD

{terminal_md}

{telemetry_md}

---

### 🍱 Architecture Bento Grid

{bento_table}

---

### 👾 Commit-Fed Virtual Pet

{pet_md}

---

### 📐 High-Throughput Node Topology (Native Mermaid)

{mermaid_md}

{abstract_md}

---

{game_md}

---

{mud_md}

---

{guestbook_md}

---

### 📂 Architecture & Blueprint Documentation

* 📑 [**Master Architecture & Comparative Matrix (`INDEX.md`)**](./INDEX.md)
* 🎨 [**Visual Design, SVG Animations & Camo Invalidation (`docs/01`)**](./docs/01-visual-design-and-svg.md)
* ⚙️ [**Dynamic GitHub Actions & CI/CD State Mutators (`docs/02`)**](./docs/02-dynamic-actions-and-ci.md)
* 📡 [**Real-Time Telemetry & Edge Endpoints (`docs/03`)**](./docs/03-telemetry-and-integrations.md)
* 🎮 [**Gamification, Tic-Tac-Toe & Issue RPCs (`docs/04`)**](./docs/04-gamification-and-interactivity.md)
* 🚀 [**Frontier Concepts & AI Daily Pulse (`docs/05`)**](./docs/05-frontier-concepts.md)
* 🌌 [**Encyclopedia of Creativity (`docs/06`)**](./docs/06-the-encyclopedia-of-creativity.md)
* 🎛️ [**ProfileHarness Engine Specification (`docs/07`)**](./docs/07-profile-harness-system.md)
* 🔮 [**Frontier Abstract Architectures (`docs/08`)**](./docs/08-frontier-abstract-architectures.md)
{main_profile_md}"""
    return full_readme.strip() + "\n"

def lint_readme(content: str):
    """Lints generated markdown against GitHub's HTML sanitizer and mobile constraints."""
    print("\n🔍 Running ProfileHarness Linter...")
    errors = []
    warnings = []

    # Check for stripped inline style attribute (must be an HTML attribute, not inside a URL)
    if re.search(r"<[a-zA-Z0-9]+(?:\s+[^>]*?)?\s+style\s*=", content):
        errors.append("Forbidden 'style=\"...\"' attribute detected on HTML element! GitHub will strip this.")

    # Check for forbidden tags
    forbidden_tags = ["script", "style", "iframe", "form", "button", "input"]
    for tag in forbidden_tags:
        if re.search(rf"</?{tag}[>\s]", content, re.IGNORECASE):
            errors.append(f"Forbidden tag '<{tag}>' detected! GitHub HTML sanitizer will scrub it.")

    # Check table column count (mobile responsiveness rule)
    for line in content.splitlines():
        if line.strip().startswith("|") and line.count("|") > 4:
            warnings.append(f"Table with > 3 columns detected: '{line[:40]}...' may wrap on mobile screens.")

    # Check for forbidden URI schemes
    if re.search(r"(?:href|src)\s*=\s*['\"]javascript:", content, re.IGNORECASE):
        errors.append("Forbidden 'javascript:' URI detected! GitHub strips all script URIs.")

    # Check that SVGs exist and validate SVG sanitizer hygiene
    expected_assets = [
        "banner-dark.svg",
        "banner-light.svg",
        "dashboard.svg",
        "terminal-typing.svg",
        "pet.svg",
        "quantum-coherence.svg",
        "synaptic-network.svg"
    ]
    for asset in expected_assets:
        svg_file = ASSETS_DIR / asset
        if not svg_file.exists():
            errors.append(f"Missing required asset: assets/{asset}")
        else:
            # C1: Validate XML well-formedness with stdlib ElementTree first
            try:
                tree = ET.parse(svg_file)
                root = tree.getroot()
                if not root.tag.endswith("svg"):
                    errors.append(f"Malformed SVG in assets/{asset}: root tag is <{root.tag}>, expected <svg>")
                if "viewBox" not in root.attrib:
                    warnings.append(f"Accessibility Warning: assets/{asset} is missing 'viewBox' attribute")
            except ET.ParseError as e:
                errors.append(f"Malformed XML in assets/{asset}: {e}")

            svg_text = svg_file.read_text(encoding="utf-8")
            if "<foreignObject" in svg_text:
                errors.append(f"Sanitizer Error: <foreignObject> found in assets/{asset} (blocked by GitHub Camo / renderers)")
            if "<script" in svg_text:
                errors.append(f"Sanitizer Error: <script> found in assets/{asset} (forbidden in SVG)")
            if svg_file.stat().st_size > 500 * 1024:
                errors.append(f"Size Warning: assets/{asset} exceeds 500KB ceiling ({svg_file.stat().st_size} bytes)")

    if errors:
        print("❌ LINT ERRORS FOUND:")
        for err in errors:
            print(f"  • {err}")
        return False
    else:
        print("✅ 0 Sanitizer Errors. Conforms to GitHub Flavored Markdown specification.")

    if warnings:
        print("⚠️ LINT WARNINGS:")
        for warn in warnings:
            print(f"  • {warn}")
    else:
        print("✅ 0 Mobile Responsiveness Warnings. Layout is fully mobile-safe.")

    return True

def check_commit_age_exceeds_threshold(threshold_days: int = 45) -> bool:
    """Returns True if the last repository commit is older than threshold_days (keepalive fallback)."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ct"],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=True,
            timeout=5,
        )
        commit_epoch = int(result.stdout.strip())
        current_epoch = int(datetime.now(timezone.utc).timestamp())
        return (current_epoch - commit_epoch) > (threshold_days * 86400)
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="ProfileHarness: Autonomous GitHub Profile Architecture Engine")
    parser.add_argument("command", choices=["build", "lint", "test"], default="build", nargs="?", help="Action to execute")
    parser.add_argument("--force", "-f", action="store_true", help="Force rebuild bypassing state hash match")
    args = parser.parse_args()

    config = load_config()
    username = config["profile"]["username"]
    token = os.environ.get("GITHUB_TOKEN")

    if args.command in ["build", "test"]:
        metrics = fetch_github_metrics(username, token)
        state_sha = compute_state_hash(config, metrics)
        existing_sha = extract_state_hash_from_readme()
        force_rebuild = args.force or os.environ.get("FORCE_REBUILD") == "1"

        if not force_rebuild and check_commit_age_exceeds_threshold(45):
            print("🕒 Inactivity threshold reached (>45 days). Bypassing cache for keepalive refresh.")
            force_rebuild = True

        if not force_rebuild and existing_sha == state_sha and verify_asset_integrity():
            print(f"⚡ Telemetry and configuration unchanged (SHA: {state_sha[:12]}). Build short-circuited.")
            sys.exit(0)

        print(f"🚀 Compiling ProfileHarness for @{username} (SHA: {state_sha[:12]})...")
        render_svg_banners(config)
        render_svg_dashboard(config, metrics)
        render_virtual_pet_svg(config, metrics)
        render_quantum_coherence_svg(config, metrics)
        render_synaptic_network_svg(config, metrics)
        
        readme_content = compile_readme(config, metrics, state_sha)
        
        # Fail-closed: validate sanitizer rules in memory BEFORE committing to disk
        if not lint_readme(readme_content):
            print("❌ FATAL: Sanitizer linter rejected generated markdown! Aborting build.", file=sys.stderr)
            sys.exit(1)

        # Atomic replacement: write to tempfile first, then atomic rename
        tmp_readme = README_PATH.with_suffix(".tmp")
        tmp_readme.write_text(readme_content, encoding="utf-8")
        os.replace(tmp_readme, README_PATH)
        print(f"✅ Successfully compiled {README_PATH}")

    elif args.command == "lint":
        if not README_PATH.exists():
            print("Error: README.md does not exist. Run 'build' first.", file=sys.stderr)
            sys.exit(1)
        if not lint_readme(README_PATH.read_text(encoding="utf-8")):
            sys.exit(1)

if __name__ == "__main__":
    main()
