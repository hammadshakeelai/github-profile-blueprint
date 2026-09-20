# Dynamic GitHub Actions & CI/CD Automation Engine

This document details the architecture, script logic, and workflow patterns for mutating GitHub profile READMEs dynamically using scheduled cron jobs, event-driven triggers, and GitHub's GraphQL API v4.

---

## 1. Automation Architecture & Security Model

A profile README repository (`username/username`) acts as a persistent state store. When an Action mutates the markdown file and commits the changes back to `main`, GitHub's web interface instantly reflects the new state.

```text
[ Trigger: cron / event ]
         │
         ▼
[ GitHub Runner: ubuntu-latest ]
         │
         ├──► Fetch external data (GraphQL v4 / REST / RSS)
         │
         ├──► Load README.md and parse AST or regex markers
         │
         ├──► Inject fresh rendered markdown / SVG
         │
         ├──► Idempotency check: git diff --quiet?
         │         ├── YES ──► Exit (0 new commits, clean graph)
         │         └── NO  ──► Commit with GITHUB_TOKEN
         ▼
[ Git Push to origin/main ]
```

### Least Privilege Permissions
Always configure explicit job-level permissions rather than relying on default repository settings:

```yaml
permissions:
  contents: write    # Required to push commits to main
  issues: write      # Required if handling issue-driven interactions
```

> **Security Note**: When GitHub Actions commits using the built-in `${{ secrets.GITHUB_TOKEN }}`, GitHub intentionally prevents that commit from triggering subsequent workflow runs. This prevents recursive, runaway infinite CI loops.

---

## 2. Marker-Based Mutation Pattern

To update specific sections of a README without overwriting manual edits or surrounding static content, use atomic HTML marker pairs:

```markdown
# Hi, I'm Alex 👋

I build high-throughput distributed systems.

<!-- METRICS:START -->
<!-- Do not edit between these markers; dynamically populated by CI -->
<!-- METRICS:END -->

### Engineering Principles
- Correctness over cleverness.
- Measure twice, benchmark continuously.
```

### Python Marker Replacement Script
This script safely replaces whatever is between the markers:

```python
#!/usr/bin/env python3
import re
import sys
from pathlib import Path

def update_section(file_path: Path, marker_name: str, new_content: str) -> bool:
    pattern = re.compile(
        rf"(<!--\s*{marker_name}:START\s*-->)(.*?)(<!--\s*{marker_name}:END\s*-->)",
        re.DOTALL
    )
    
    file_text = file_path.read_text(encoding="utf-8")
    
    if not pattern.search(file_text):
        print(f"Error: Marker <!-- {marker_name}:START --> not found in {file_path}", file=sys.stderr)
        return False
        
    replacement = rf"\g<1>\n{new_content.strip()}\n\g<3>"
    updated_text = pattern.sub(replacement, file_text)
    
    if updated_text == file_text:
        print("No content changes detected.")
        return False
        
    file_path.write_text(updated_text, encoding="utf-8")
    print(f"Successfully updated section: {marker_name}")
    return True

if __name__ == "__main__":
    readme = Path("README.md")
    sample_content = """
| Metric | Value | 7-Day Trend |
| :--- | :--- | :--- |
| **Pull Requests Reviewed** | 42 | ↗ +12% |
| **Merged Commits** | 188 | ↗ +8% |
| **Primary Focus** | Distributed Consensus | Rust / Go |
"""
    update_section(readme, "METRICS", sample_content)
```

---

## 3. Querying GitHub GraphQL API v4

The GraphQL API is vastly superior to REST for profile metrics: it fetches deep, cross-relational data (contributions, reviews, pinned repositories, sponsor tiers) in a single HTTP request, eliminating rate-limiting issues.

### GraphQL Query Payload
Save as `.github/queries/profile-stats.graphql`:

```graphql
query($login: String!) {
  user(login: $login) {
    name
    createdAt
    followers {
      totalCount
    }
    starredRepositories {
      totalCount
    }
    pullRequests(states: MERGED) {
      totalCount
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestReviewContributions
      totalIssueContributions
      totalRepositoryContributions
      restrictedContributionsCount
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            color
          }
        }
      }
    }
  }
}
```

### Execution via Node.js
```javascript
// .github/scripts/fetch-stats.mjs
import { writeFileSync, readFileSync } from 'node:fs';

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const USERNAME = process.env.GITHUB_REPOSITORY_OWNER;

const query = `
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      totalCommitContributions
      totalPullRequestReviewContributions
    }
    pullRequests(states: MERGED) {
      totalCount
    }
  }
}
`;

async function fetchStats() {
  const response = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GITHUB_TOKEN}`,
      'Content-Type': 'application/json',
      'User-Agent': 'Profile-Readme-Updater'
    },
    body: JSON.stringify({ query, variables: { login: USERNAME } })
  });

  if (!response.ok) {
    throw new Error(`GraphQL failed: ${response.status} ${response.statusText}`);
  }

  const { data } = await response.json();
  const coll = data.user.contributionsCollection;
  const mergedPRs = data.user.pullRequests.totalCount;

  const markdown = `
| Total Commits (Year) | PR Reviews Completed | Total Merged PRs |
| :---: | :---: | :---: |
| **${coll.totalCommitContributions.toLocaleString()}** | **${coll.totalPullRequestReviewContributions.toLocaleString()}** | **${mergedPRs.toLocaleString()}** |
`;

  return markdown;
}

const statsMarkdown = await fetchStats();
console.log("Fetched statistics successfully:\n", statsMarkdown);
```

---

## 4. Safe Auto-Commit Engine (Preventing Graph Pollution)

A common mistake in profile automation is committing on every hourly cron run, resulting in hundreds of meaningless "update stats" commits that pollute your GitHub contribution graph.

### The Idempotency Check Pattern
Only stage, commit, and push if `git diff` detects genuine changes:

```bash
# Check if README or assets changed
git add README.md assets/

if git diff --staged --quiet; then
  echo "No changes detected. Skipping commit to preserve graph hygiene."
  exit 0
fi

# Configure official GitHub Actions bot metadata
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"

git commit -m "chore(telemetry): update profile metrics [skip ci]"
git push origin main
```

> **Tip**: Using the verified bot email `41898282+github-actions[bot]@users.noreply.github.com` attaches the official GitHub Actions badge to the commit in the Git history.

---

## 5. Cron Scheduling Realities & Jitter

GitHub Actions uses POSIX cron syntax:
```yaml
on:
  schedule:
    - cron: '0 */6 * * *' # Every 6 hours
  workflow_dispatch:      # Always include for manual runs & debugging
```

### Critical Quirks of GitHub Actions Cron:
1. **Queue Jitter**: High system load across GitHub's infrastructure means scheduled workflows rarely run at exact second zero. Expect a delay between 3 to 25 minutes during peak hours.
2. **Repository Inactivity Drop**: If a public repository has had zero commits or interactions for **60 consecutive days**, GitHub automatically disables all scheduled workflows. Adding `workflow_dispatch` allows one-click reactivations.
3. **High-Frequency Restrictions**: GitHub advises against running cron jobs every 5 minutes. Every 4 to 12 hours is optimal for profile READMEs.
