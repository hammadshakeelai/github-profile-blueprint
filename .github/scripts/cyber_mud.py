#!/usr/bin/env python3
"""
Git-Native Cyberpunk MUD (Multi-User Dungeon) Engine
Processes text RPG moves triggered by GitHub Issues and mutates world state in Git.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path("data/mud-state.json")
README_FILE = Path("README.md")
REPO = os.environ.get("GITHUB_REPOSITORY", "hammadshakeelAl/hammadshakeelAl")
ISSUE_TITLE = os.environ.get("ISSUE_TITLE", "")
ISSUE_USER = os.environ.get("ISSUE_USER", "AnonymousAdventurer")

ROOMS = {
    "mainframe": {
        "title": "Mainframe Core // Sector 7G",
        "desc": "A subterranean chamber housing three crystalline Raft consensus nodes. The air smells of ozone and liquid helium. Optical telemetry cables pulse with blue coherent light.",
        "actions": [
            ("⚡ Ping Quorum Node", "mud|action|ping"),
            ("🔍 Inspect Memory Ring Buffer", "mud|action|inspect"),
            ("🚪 Enter Engine Bay", "mud|move|engine_bay")
        ]
    },
    "engine_bay": {
        "title": "Sub-Kernel Engine Bay // Low-Level Core",
        "desc": "Heavy industrial server racks line the walls. eBPF socket filters hum at gigahertz frequencies. A heavy blast door leads back to the Mainframe.",
        "actions": [
            ("🔧 Overclock NVMe io_uring", "mud|action|overclock"),
            ("📊 Probe TCP Tracepoint", "mud|action|probe"),
            ("🚪 Return to Mainframe", "mud|move|mainframe")
        ]
    }
}

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "location_key": "mainframe",
        "last_explorer": ISSUE_USER,
        "system_ticks": 1,
        "log": []
    }

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")

def render_mud_markdown(state):
    loc_key = state.get("location_key", "mainframe")
    room = ROOMS.get(loc_key, ROOMS["mainframe"])

    actions_md = " • ".join(
        f"[{label}](https://github.com/{REPO}/issues/new?title={cmd}&body=Click+Submit+new+issue+to+advance+the+dungeon.)"
        for label, cmd in room["actions"]
    )

    recent_logs = "\n".join(f"> {item}" for item in state.get("log", [])[-3:])

    return f"""
<!-- MUD:START -->
### 🕹️ Git-Native Cyberpunk Dungeon (Multi-User Adventure)

**Current Location**: `{room['title']}`  
**Last Adventurer**: [@{state.get('last_explorer', 'octocat')}](https://github.com/{state.get('last_explorer', 'octocat')}) • **System Ticks**: `{state.get('system_ticks', 42)}`

> *{room['desc']}*

**Available Actions**:  
{actions_md}

**Recent World Log**:  
{recent_logs}
<!-- MUD:END -->
""".strip()

def main():
    state = load_state()
    loc = state.get("location_key", "mainframe")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")

    print(f"MUD Command Received: '{ISSUE_TITLE}' by @{ISSUE_USER}")

    if "mud|move|engine_bay" in ISSUE_TITLE:
        state["location_key"] = "engine_bay"
        state["log"].append(f"[{today}] @{ISSUE_USER} traversed the airlock into the Engine Bay.")
    elif "mud|move|mainframe" in ISSUE_TITLE:
        state["location_key"] = "mainframe"
        state["log"].append(f"[{today}] @{ISSUE_USER} returned to the Mainframe Core.")
    elif "mud|action|ping" in ISSUE_TITLE:
        state["system_ticks"] = state.get("system_ticks", 0) + 1
        state["log"].append(f"[{today}] @{ISSUE_USER} sent a consensus heartbeat. Quorum acknowledged in 0.4ms.")
    elif "mud|action|inspect" in ISSUE_TITLE:
        state["log"].append(f"[{today}] @{ISSUE_USER} inspected memory registers: 0 lock contention detected.")
    elif "mud|action|overclock" in ISSUE_TITLE:
        state["log"].append(f"[{today}] @{ISSUE_USER} overclocked the io_uring ring buffer. IOPS increased to 4.2M!")
    elif "mud|action|probe" in ISSUE_TITLE:
        state["log"].append(f"[{today}] @{ISSUE_USER} triggered an eBPF network probe. Zero packets dropped.")

    state["last_explorer"] = ISSUE_USER
    state["system_ticks"] = state.get("system_ticks", 0) + 1
    state["log"] = state["log"][-10:] # Keep last 10 entries

    save_state(state)

    # Update README
    if README_FILE.exists():
        text = README_FILE.read_text(encoding="utf-8")
        pattern = re.compile(r"<!--\s*MUD:START\s*-->.*?<!--\s*MUD:END\s*-->", re.DOTALL)
        mud_md = render_mud_markdown(state)
        if pattern.search(text):
            updated = pattern.sub(mud_md, text)
            README_FILE.write_text(updated, encoding="utf-8")
            print("README.md MUD section updated successfully.")

if __name__ == "__main__":
    main()
