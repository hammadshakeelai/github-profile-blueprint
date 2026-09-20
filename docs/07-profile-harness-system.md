# ProfileHarness: Autonomous GitHub Profile Architecture Engine

ProfileHarness is a declarative compiler and validation harness designed to eliminate the manual toil and brittleness of maintaining modern GitHub profile READMEs.

---

## 1. System Philosophy: The 2026 Shift

In 2026, developer profile design moved decisively away from uncurated "badge walls" and fragile third-party SVG endpoints toward:
1. **Narrative-Driven Bento Grids**: Clean, structured 2-column tabular blocks that never cause horizontal scrolling on mobile viewports.
2. **Git-Native Storage**: Generating pure SVG assets inside CI and saving them locally (`./assets/*.svg`), guaranteeing **0ms latency**, **100% uptime**, and **total immunity to GitHub Camo proxy caching lag**.
3. **Automated Sanitizer Verification**: Linting generated markdown against GitHub's HTML sanitizer rules (`github/markup`) before committing, preventing broken tags and stripped attributes.

---

## 2. Configuration Specification (`harness/profile.config.json`)

The harness is driven entirely by a declarative JSON file:

```json
{
  "profile": {
    "username": "hammadshakeelAl",
    "name": "Hammad Shakeel",
    "headline": "Principal Systems Architect & Distributed Systems Engineer",
    "theme": "tokyo_night",
    "status": {
      "text": "ONLINE // COMPILING DISTRIBUTED ENGINES",
      "dot_color": "#22c55e"
    }
  },
  "layout": {
    "style": "bento_grid",
    "mobile_optimized": true,
    "max_columns": 2
  },
  "modules": {
    "hero_banner": { "enabled": true },
    "terminal_hud": { "enabled": true },
    "bento_blocks": [ ... ],
    "git_native_dashboard": { "enabled": true },
    "virtual_pet": { "enabled": true },
    "quantum_coherence": { "enabled": true },
    "synaptic_network": { "enabled": true },
    "interactive_tictactoe": { "enabled": true },
    "community_guestbook": { "enabled": true },
    "mermaid_diagram": { "enabled": true }
  }
}
```

---

## 3. CLI Commands

The engine provides a built-in CLI:

```bash
# Compile README.md, render all SVG assets, and run the sanitizer linter
python harness/engine.py build

# Run the strict GitHub Flavored Markdown and sanitizer validator only
python harness/engine.py lint

# Dry-run test without writing to disk
python harness/engine.py test
```

---

## 4. GitHub Actions Automation

ProfileHarness runs automatically every 6 hours via `.github/workflows/profile-harness.yml`:

```text
[ Cron Trigger: 0 */6 * * * ]
             │
             ▼
[ Setup Python 3.12 ]
             │
             ▼
[ python harness/engine.py build ]
  ├── Fetches real-time Git commit velocity
  ├── Generates banner-dark.svg & banner-light.svg
  ├── Generates dashboard.svg & pet.svg
  ├── Generates quantum-coherence.svg & synaptic-network.svg
  └── Assembles README.md & executes linter
             │
             ▼
[ Idempotency Check: git diff --staged --quiet ]
  ├── 0 changes  ──► Exit 0 (zero commit graph noise)
  └── Changes    ──► Commit as verified github-actions[bot]
```
