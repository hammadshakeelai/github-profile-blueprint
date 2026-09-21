import sys
import json
import re
from pathlib import Path

def find_workspace_root(payload: dict) -> Path:
    if payload.get("workspacePaths"):
        for p in payload["workspacePaths"]:
            path = Path(p)
            if (path / "docs" / "RESEARCH-LOG.md").exists():
                return path
    
    # Fallback to searching up from script or current working directory
    for start in [Path.cwd(), Path(__file__).resolve().parent]:
        cur = start
        for _ in range(5):
            if (cur / "docs" / "RESEARCH-LOG.md").exists():
                return cur
            cur = cur.parent
    return Path.cwd()

def get_unfinished_tracks(log_path: Path):
    if not log_path.exists():
        return None
    content = log_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    unfinished = []
    in_ledger = False
    for line in lines:
        if "## Ledger" in line:
            in_ledger = True
            continue
        if in_ledger:
            if line.strip().startswith("|") and "Track" in line:
                cols = [c.strip() for c in line.strip().split("|")[1:-1]]
                if len(cols) >= 2:
                    track_name = cols[0]
                    status = cols[1].lower()
                    if status in ["todo", "in-progress", "blocked"]:
                        unfinished.append((track_name, status))
            elif line.strip().startswith("---") or line.strip().startswith("###"):
                in_ledger = False
    return unfinished

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "stop"
    
    raw_input = "{}"
    try:
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read()
    except Exception:
        pass
        
    try:
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}
        
    root = find_workspace_root(payload)
    log_path = root / "docs" / "RESEARCH-LOG.md"
    unfinished = get_unfinished_tracks(log_path)
    
    hook_payload_text = (
        "Read `docs/RESEARCH-LOG.md`. Find the first track not marked `done`. Continue "
        "it, or start it. When it is finished, mark it `done`, record its open "
        "questions, and immediately begin the next `todo` track. If every track is "
        "`done`, mint new tracks from the accumulated open questions and append them as "
        "`todo`. Never stop to ask permission. Never end a turn without either "
        "advancing a track or appending a new one."
    )
    
    if mode == "pre_invocation":
        if unfinished:
            current_track = unfinished[0][0]
            msg = f"Continuation Hook active [{current_track}]: {hook_payload_text}"
            res = {
                "injectSteps": [
                    {
                        "ephemeralMessage": msg
                    }
                ]
            }
        else:
            res = {"injectSteps": []}
        print(json.dumps(res))
        
    elif mode == "stop":
        if unfinished:
            current_track = unfinished[0][0]
            res = {
                "decision": "continue",
                "reason": f"Active unfinished research: {current_track}. {hook_payload_text}"
            }
        else:
            res = {
                "decision": "allow"
            }
        print(json.dumps(res))
    else:
        print("{}")

if __name__ == "__main__":
    main()
