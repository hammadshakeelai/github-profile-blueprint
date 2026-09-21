#!/usr/bin/env python3
"""
ProfileHarness Hybrid Commit Dispatcher
Implements a 2-tiered commit architecture:
  Tier 1: Verified GraphQL createCommitOnBranch (green verified badge, zero secret management)
  Tier 2: Resilient Git CLI fallback (git pull --rebase + git push, payload/rate-limit immune)
"""

import os
import sys
import json
import base64
import time
import random
import subprocess
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Optional, Tuple

# Ensure UTF-8 output even on Windows terminals with legacy code pages
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
MAX_PAYLOAD_BYTES = 7_500_000  # 7.5 MB raw ceiling (approx 10 MB when base64 + JSON wrapped)
MAX_STALE_RETRIES = 3


def run_cmd(cmd: List[str], check: bool = True) -> subprocess.CompletedProcess:
    """Execute a shell command via subprocess."""
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=check)


def get_modified_files(target_paths: List[str]) -> List[Path]:
    """Return list of modified or untracked file paths matching target prefixes."""
    res = run_cmd(["git", "status", "--porcelain"])
    modified = []
    for line in res.stdout.splitlines():
        if not line.strip():
            continue
        rel_path = line[3:].strip()
        path = Path(rel_path)
        for target in target_paths:
            if rel_path == target or rel_path.startswith(target.rstrip("/") + "/"):
                if path.is_file():
                    modified.append(path)
                break
    return sorted(list(set(modified)))


def query_remote_head_oid(repo_owner: str, repo_name: str, branch: str, token: str) -> str:
    """Fetch current remote branch tip OID using GraphQL."""
    query = """
    query($owner: String!, $repo: String!, $ref: String!) {
      repository(owner: $owner, name: $repo) {
        ref(qualifiedName: $ref) {
          target {
            oid
          }
        }
      }
    }
    """
    payload = {
        "query": query,
        "variables": {
            "owner": repo_owner,
            "repo": repo_name,
            "ref": f"refs/heads/{branch}"
        }
    }
    req = urllib.request.Request(
        GRAPHQL_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ProfileHarness-HybridDispatcher/1.0"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        ref_data = data.get("data", {}).get("repository", {}).get("ref")
        if not ref_data or not ref_data.get("target"):
            raise ValueError(f"Branch ref 'refs/heads/{branch}' not found on remote.")
        return ref_data["target"]["oid"]


def submit_graphql_commit(
    repo_owner: str,
    repo_name: str,
    branch: str,
    expected_oid: str,
    files: List[Path],
    message: str,
    token: str
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Submit createCommitOnBranch mutation.
    Returns: (success, commit_oid_or_error_type, error_message)
    """
    file_additions = []
    total_bytes = 0

    for f in files:
        raw_bytes = f.read_bytes()
        total_bytes += len(raw_bytes)
        b64_content = base64.b64encode(raw_bytes).decode("ascii")
        posix_path = f.as_posix().lstrip("./")
        file_additions.append({
            "path": posix_path,
            "contents": b64_content
        })

    if total_bytes > MAX_PAYLOAD_BYTES:
        return False, "PAYLOAD_TOO_LARGE", f"Total payload size ({total_bytes} bytes) exceeds 7.5 MB safe limit."

    mutation = """
    mutation($input: CreateCommitOnBranchInput!) {
      createCommitOnBranch(input: $input) {
        commit {
          oid
          url
        }
      }
    }
    """
    mutation_input = {
        "branch": {
            "repositoryNameWithOwner": f"{repo_owner}/{repo_name}",
            "branchName": branch
        },
        "message": {
            "headline": message.splitlines()[0],
            "body": "\n".join(message.splitlines()[1:]) if "\n" in message else None
        },
        "fileChanges": {
            "additions": file_additions
        },
        "expectedHeadOid": expected_oid
    }

    req_body = json.dumps({"query": mutation, "variables": {"input": mutation_input}}).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_ENDPOINT,
        data=req_body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "ProfileHarness-HybridDispatcher/1.0"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_body = resp.read().decode("utf-8")
            data = json.loads(resp_body)

            if "errors" in data and data["errors"]:
                err = data["errors"][0]
                err_type = err.get("type", "GRAPHQL_ERROR")
                err_msg = err.get("message", "Unknown GraphQL error")
                return False, err_type, err_msg

            commit_data = data.get("data", {}).get("createCommitOnBranch", {}).get("commit")
            if commit_data and "oid" in commit_data:
                return True, commit_data["oid"], None
            return False, "UNKNOWN_RESPONSE", "No commit OID returned in GraphQL response."

    except urllib.error.HTTPError as e:
        status = e.code
        headers = e.headers
        remaining = headers.get("x-ratelimit-remaining")
        retry_after = headers.get("retry-after")

        if status == 413:
            return False, "HTTP_413_PAYLOAD_TOO_LARGE", "HTTP 413: Mutation payload rejected by API gateway."
        if status == 403 and remaining == "0":
            return False, "PRIMARY_RATE_LIMIT_EXHAUSTED", "Primary GITHUB_TOKEN rate limit (1,000 pts/hr) exhausted."
        if status in (403, 429) and retry_after:
            return False, "SECONDARY_RATE_LIMIT", f"Secondary rate limit triggered (Retry-After: {retry_after}s)."
        if status in (500, 502, 503, 504):
            return False, f"SERVER_ERROR_{status}", f"GitHub GraphQL server error {status}."
        return False, f"HTTP_{status}", f"HTTP Error {status}: {e.read().decode('utf-8', errors='ignore')}"

    except Exception as ex:
        return False, "NETWORK_ERROR", str(ex)


def run_git_cli_fallback(files: List[Path], branch: str, message: str) -> bool:
    """
    Tier 2: Standard Git CLI fallback.
    Executes git add, git commit, git pull --rebase, git push.
    """
    print("🔄 Tier 2: Initiating resilient Git CLI fallback...")
    try:
        run_cmd(["git", "config", "user.name", "github-actions[bot]"])
        run_cmd(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"])

        for f in files:
            run_cmd(["git", "add", f.as_posix()])

        staged_check = run_cmd(["git", "diff", "--staged", "--quiet"], check=False)
        if staged_check.returncode == 0:
            print("⚡ Git CLI: No staged changes detected. Skipping commit.")
            return True

        run_cmd(["git", "commit", "-m", message])

        print(f"📥 Rebasing onto origin/{branch}...")
        rebase_res = run_cmd(["git", "pull", "--rebase", "origin", branch], check=False)
        if rebase_res.returncode != 0:
            print("⚠️ Rebase conflict encountered! Rolling back workspace...", file=sys.stderr)
            run_cmd(["git", "rebase", "--abort"], check=False)
            run_cmd(["git", "checkout", "--", "."], check=False)
            run_cmd(["git", "clean", "-fd"], check=False)
            raise RuntimeError(f"Git rebase failed: {rebase_res.stderr}")

        print(f"🚀 Pushing commit to origin/{branch}...")
        run_cmd(["git", "push", "origin", branch])
        print("✅ Git CLI fallback commit pushed successfully.")
        return True

    except Exception as e:
        print(f"❌ FATAL: Git CLI fallback failed: {e}", file=sys.stderr)
        return False


def dispatch_hybrid_commit(target_dirs: List[str], message: str) -> None:
    token = os.environ.get("GITHUB_TOKEN")
    repo_full = os.environ.get("GITHUB_REPOSITORY")
    branch = os.environ.get("GITHUB_REF_NAME", "main")

    if not token or not repo_full:
        print("⚠️ Missing GITHUB_TOKEN or GITHUB_REPOSITORY. Falling back directly to Git CLI.")
        files = get_modified_files(target_dirs)
        if not files:
            print("⚡ Zero changes detected. Exiting 0.")
            sys.exit(0)
        success = run_git_cli_fallback(files, branch, message)
        sys.exit(0 if success else 1)

    repo_owner, repo_name = repo_full.split("/", 1)
    modified_files = get_modified_files(target_dirs)

    if not modified_files:
        print("⚡ Idempotency Guard: Zero modified files detected. Commit graph preserved.")
        sys.exit(0)

    print(f"📋 Detected {len(modified_files)} modified file(s): {[f.as_posix() for f in modified_files]}")

    # ==========================================
    # TIER 1: Attempt Verified GraphQL Commit
    # ==========================================
    print("🔒 Tier 1: Attempting verified commit via GraphQL createCommitOnBranch...")
    for attempt in range(1, MAX_STALE_RETRIES + 1):
        try:
            head_oid = query_remote_head_oid(repo_owner, repo_name, branch, token)
        except Exception as e:
            print(f"⚠️ Failed to query remote head OID ({e}). Triggering Tier 2 fallback immediately.")
            break

        success, err_or_oid, msg = submit_graphql_commit(
            repo_owner, repo_name, branch, head_oid, modified_files, message, token
        )

        if success:
            print(f"✅ Tier 1 SUCCESS: Verified commit created on origin/{branch} (SHA: {err_or_oid[:8]})")
            print("🔄 Synchronizing local git index with remote...")
            run_cmd(["git", "fetch", "origin", branch])
            run_cmd(["git", "reset", "--hard", f"origin/{branch}"])
            print("✨ Local workspace cleanly synchronized with verified remote commit.")
            sys.exit(0)

        print(f"⚠️ GraphQL Attempt {attempt}/{MAX_STALE_RETRIES} failed: [{err_or_oid}] {msg}")

        if err_or_oid == "STALE_DATA" and attempt < MAX_STALE_RETRIES:
            jitter = random.uniform(0.5, 1.5) * (2 ** (attempt - 1))
            print(f"⏳ Concurrency race detected. Backing off for {jitter:.2f}s before retry...")
            time.sleep(jitter)
            run_cmd(["git", "fetch", "origin", branch], check=False)
            modified_files = get_modified_files(target_dirs)
            if not modified_files:
                print("⚡ Upstream sync eliminated diff. Clean no-op exit.")
                sys.exit(0)
            continue
        else:
            print(f"🛑 Permanent or non-retriable GraphQL error ({err_or_oid}). Triggering Tier 2 immediately.")
            break

    # ==========================================
    # TIER 2: Git CLI Fallback
    # ==========================================
    fallback_ok = run_git_cli_fallback(modified_files, branch, message)
    if not fallback_ok:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    targets = ["README.md", "assets/"]
    msg = "chore(profile): synchronize telemetry and autonomous SVGs [skip ci]"
    dispatch_hybrid_commit(targets, msg)
