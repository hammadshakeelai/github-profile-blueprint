# Part 05 — All AI Work Across Every Branch (archive/v1, research/claude, antigravity, v2/research, probe/cache)

This part documents **every line of AI-assisted work that lives outside `main`'s
final shape** — the five development branches of
`github-profile-blueprint` (https://github.com/hammadshakeelai/github-profile-blueprint),
plus the brief side-branch note. Everything below was read directly from git
objects (`git show origin/<branch>:<path>`, `git log`, `git diff`, `git merge-base`)
without checking out or modifying anything. Dates are commit dates (all 2026-09-20
through 2026-09-25). All commits are authored by `hammadai` /
`hammadshakeelAl` — i.e. **the AI committed under the human's identity**; the
branch names and commit messages are the only machine fingerprints.

---

## 1. Branch topology — one lineage, two eras, one orphan

Six branches exist. Their ancestry was verified with `git merge-base --is-ancestor`
(exit codes) and `git log A..B`:

| Branch | Tip | Commits | Relationship (verified) |
|---|---|--:|---|
| `main` | `b7ce609` | 67 | Root of era 2 (survey → book → showcase → v2 wipe) |
| `archive/v1` | `d5a44a3` | 19 | `archive/v1` ⊂ `main` (archived state of era 1) |
| `research/claude` | `c4f1919` | 18 | `research/claude` ⊂ `archive/v1` |
| `research/antigravity` | `f5666b9` | 14 | `research/antigravity` ⊂ `research/claude` |
| `v2/research` | `3aa476f` | 70 | `main` ⊂ `v2/research` (main + 3 frontier commits) |
| `probe/cache` | `1ca9afc` | 3 | **Orphan** — no merge-base with `main` at all |
| `helper/side-person_opencode` | `b7ce609` | 67 | Same tip as `main`; mentioned only in passing |

So the whole repo is a **single chain** for era 1:

```text
research/antigravity (14) ⊂ research/claude (18) ⊂ archive/v1 (19) ⊂ main (67) ⊂ v2/research (70)
                                                              probe/cache (3)  ← separate root, disconnected
```

Consequences proven by `git log origin/main..origin/<branch>`:

- `archive/v1`, `research/claude`, `research/antigravity` and the helper branch
  are **fully merged** — their `main..branch` logs are empty. Nothing on them is
  unique; it all reached `main` and was later **deleted by the v2 wipe** (main's
  tree no longer contains `harness/`, `skills/`, `docs/RESEARCH-*.md`,
  `edge-telemetry-worker/`, `templates/`).
- Only `v2/research` has live frontier commits (`562090a`, `5d877a4`, `3aa476f`)
  and only `probe/cache` has its own three.
- Exclusive commit sets: `research/claude` vs `research/antigravity` =
  `{c4f1919, fbc7d9f, d7feecf, a3b4b74}`; `archive/v1` vs `research/claude` =
  `{d5a44a3}`; `research/antigravity` contributes **nothing** that
  `research/claude` doesn't have.
- The repository contains exactly **two merge commits**, both reconciling the
  Antigravity work into the Claude line:
  - `c4f1919` — *"merge: Antigravity tracks 17-23, reconciling the font work"*
    (parents `fbc7d9f` + `f5666b9`)
  - `d7feecf` — *"merge: bring in Antigravity's C0/C1 fixes and tracks 7-19"*
    (parents `a3b4b74` + `a47ca5d`)

Reading order for this part: the harness (`archive/v1`), the research engine
(`research/antigravity`), the measurement ledger and skill (`research/claude`),
the visual frontier (`v2/research`), the cache probe (`probe/cache`).

---

## 2. `archive/v1` — the ProfileHarness era (the machine that wrote itself)

**19 commits, 2026-09-20 → 2026-09-21.** This is era 1's complete state: a
declarative "compiler" that generates the profile README, renders its SVGs,
lints the output, and commits the result back to GitHub from CI — plus an
8-chapter documentation set, three templates, a Cloudflare telemetry worker, and
two interactive state stores.

### 2.1 What it built — file inventory

| File (on `archive/v1`) | Bytes | Role |
|---|--:|---|
| `README.md` | 8,980 | The compiled autonomous profile README (banner `<picture>`, typing-svg tagline, `TELEMETRY` block, `STATE_SHA` comment) |
| `INDEX.md` | 6,865 | Master manual: repository blueprint, comparative matrix, roadmap |
| `AGENTS.md` | 461 | Agent instruction stub |
| `harness/engine.py` | 46,793 | Compiler / validator / SVG synthesis engine (Python) |
| `harness/hybrid_dispatcher.py` | 11,659 | Two-tier commit dispatcher (GraphQL → git CLI) |
| `harness/profile.config.json` | 3,674 | Declarative profile configuration |
| `.github/workflows/profile-harness.yml` | 1,831 | The engine's workflow |
| `.agents/hook.py` | 3,427 | **Continuous-research continuation hook** |
| `.agents/hooks.json` | 729 | Hook wiring (PreInvocation + Stop) |
| `docs/RESEARCH-LOG.md` | 126,620 | 24-track standing research log (see §3) |
| `docs/RESEARCH-CLAUDE.md` | 8,382 | Claude-side rendering ledger C0–C6 (see §4) |
| `docs/PLAN-V2.md` | 6,694 | v1 post-mortem → v2 rules (unique commit `d5a44a3`) |
| `docs/07-profile-harness-system.md` | 3,085 | Harness architecture doc |
| `docs/01…08` | — | Eight-chapter encyclopedia (design/CI/telemetry/gamification/frontier/… ) |
| `skills/github-profile-readme/SKILL.md` | 8,211 | Packaged agent skill (see §4.3) |
| `references/measured-constraints.md` | 4,594 | Measured widths, asset routing, cache behaviour |
| `references/banner-craft.md` | 5,501 | Banner craft rules |
| `references/svg-recipes.md` | 5,552 | SVG recipes |
| `edge-telemetry-worker/src/index.ts` | 5,566 | Cloudflare Worker → live Spotify SVG |
| `templates/` | 3 files | minimal-systems-engineer / interactive-full-stack / experimental-frontier |
| `assets/banner-{dark,light}.svg`, `dashboard.svg`, `pet.svg`, `quantum-coherence.svg`, `synaptic-network.svg`, `spotify-mock.svg`, `terminal-typing.*` | — | Generated art |
| `data/mud-state.json`, `ttt-state.json`, `tictactoe.py`, `game.yml` | — | Interactive state stores |
| `.github/scripts/cyber_mud.py`, `workflows/example-readme-updater.yml` | — | Scripts and example workflow |

### 2.2 The engine (`harness/engine.py`)

Public surface, extracted from the file itself:

```text
def fit_font_size(text, desired, advance, max_width, floor)   # shrink-to-fit with a legibility floor
def load_config()
def compute_state_hash(config, metrics) -> str                # short-circuit rebuilds
def extract_state_hash_from_readme() -> str | None
def verify_asset_integrity() -> bool
def extract_dynamic_section(tag) -> str | None                # preserve CI-owned sections across rebuilds
def fetch_workflow_reliability(...)
def fetch_github_metrics(username, token=None) -> dict
def render_svg_dashboard(config, metrics)
def render_svg_banners(config, metrics)                       # ← origin of bug C0
def render_virtual_pet_svg(...)
def render_quantum_coherence_svg(...)
def render_synaptic_network_svg(...)
def compile_readme(config, metrics, state_sha="") -> str
def lint_readme(content)                                      # ← fixed by C1
def check_commit_age_exceeds_threshold(threshold_days=45) -> bool
def main()                                                    # CLI: build / etc.
```

CLI documented in `docs/07-profile-harness-system.md`:

```bash
python harness/engine.py build   # compile README.md, render SVGs, run sanitizer linter
```

Its stated philosophy (doc §1): *narrative-driven bento grids, git-native asset
storage (0 ms, 100 % uptime, immune to Camo lag), and automated sanitizer
verification against `github/markup` rules before committing.*

### 2.3 The two-tier commit dispatcher (`harness/hybrid_dispatcher.py`)

Introduced by commit `a47ca5d` *"feat(harness): implement hybrid commit
dispatcher and record Track 18"*. Verbatim architecture from the module
docstring:

```python
"""
ProfileHarness Hybrid Commit Dispatcher
Implements a 2-tiered commit architecture:
  Tier 1: Verified GraphQL createCommitOnBranch (green verified badge, zero secret management)
  Tier 2: Resilient Git CLI fallback (git pull --rebase + git push, payload/rate-limit immune)
"""
```

Key mechanics, as written:

```python
GRAPHQL_ENDPOINT = "https://api.github.com/graphql"
MAX_PAYLOAD_BYTES = 7_500_000   # 7.5 MB raw ceiling (≈10 MB when base64 + JSON wrapped)
MAX_STALE_RETRIES = 3
```

- **Tier 1** queries the remote head OID (`query_remote_head_oid`) then posts a
  `createCommitOnBranch` mutation with base64 `fileChanges` and
  `expectedHeadOid`. On `STALE_DATA` it retries with jittered exponential backoff
  (`random.uniform(0.5, 1.5) * 2 ** (attempt-1)`), re-fetching between attempts;
  classifies `HTTP_413_PAYLOAD_TOO_LARGE`, `PRIMARY_RATE_LIMIT_EXHAUSTED`,
  `SECONDARY_RATE_LIMIT` (honours `Retry-After`), `SERVER_ERROR_5xx`.
  On success it `fetch` + `reset --hard origin/<branch>` to re-sync the workspace.
- **Tier 2** `git add` → `git commit` → `git pull --rebase origin <branch>` →
  `git push`, aborting the rebase and rolling back (`rebase --abort`,
  `checkout -- .`, `clean -fd`) on conflict.
- **Idempotency guard**: `"⚡ Idempotency Guard: Zero modified files detected.
  Commit graph preserved."` — exit 0 without committing.
- Default dispatch: targets `["README.md", "assets/"]`, message
  `chore(profile): synchronize telemetry and autonomous SVGs [skip ci]`.

### 2.4 The self-perpetuating agent hook (`.agents/`)

`hook.py` + `hooks.json` wire a **PreInvocation** and **Stop** hook so the agent
never ends a turn without advancing research. The payload it injects, verbatim:

```text
Read `docs/RESEARCH-LOG.md`. Find the first track not marked `done`. Continue
it, or start it. When it is finished, mark it `done`, record its open
questions, and immediately begin the next `todo` track. If every track is
`done`, mint new tracks from the accumulated open questions and append them as
`todo`. Never stop to ask permission. Never end a turn without either
advancing a track or appending a new one.
```

`Stop` mode returns `{"decision": "continue", "reason": "Active unfinished
research: <track>. …"}` whenever unfinished tracks exist — i.e. the agent is
**programmatically prevented from stopping** while the ledger has work. This is
the mechanism that produced 24 research tracks in one day.

### 2.5 The workflow (`.github/workflows/profile-harness.yml`)

Cron-driven `profile-harness.yml` runs the engine and commits via the dispatcher
— the loop the whole system exists to feed. It, plus `updater.yml` redundancy,
is what Track 0 diagnosed (see §3.2).

### 2.6 The post-mortem (`docs/PLAN-V2.md`, unique commit `d5a44a3`)

*"docs: plan v2 — return to the original profile README research goal"* — v1's
own verdict on itself:

- **Failure**: infrastructure outran research; the encyclopedia carries the line
  *"2 external references"* — documentation volume ≠ evidence.
- **Keep-list** for v2: the three measured widths (846 / 831 / 309 px), the
  legibility formula `F_min = target × W / R`, Camo-vs-raw routing knowledge,
  secure animated mode, the font/CSP findings, and the packaged `skills/`.

### 2.7 Value: **4/5 — and archived by its own author.**
Why: it is the most complete autonomous agent system in the repo (compiler +
validator + two-tier verified commits + anti-stop hook), and its measurement
findings survived into v2. It loses a point because it solved *maintenance*
rather than the stated *research* question, and `main`'s v2 wipe deleted most of
it — kept alive only as `archive/v1`.

### 2.8 Fate
Merged into `main`, then **deleted by the v2 wipe**; preserved on `archive/v1`
and referenced by `PLAN-V2.md` as the keep-list source.

---

## 3. `research/antigravity` — the 24-track CI/infra research engine

**14 commits (all also on `research/claude`), 2026-09-20 → 2026-09-21.** This
branch's entire identity is `docs/RESEARCH-LOG.md` (126,620 bytes) — a standing
ledger titled *"ProfileHarness Standing Research Log (branch:
research/antigravity)"* — plus the hook that feeds it. Versus `research/claude`
its tree is **missing** `docs/RESEARCH-CLAUDE.md` and `skills/`, and its
`harness/engine.py` is the pre-font-reconciliation copy (42,815 bytes vs 46,793).

### 3.1 The ledger structure

Tracks 0–23, each with `#### Findings:` / `#### Evidence:` / `UNVERIFIED`
labels / `#### Recommendation` / `#### Open questions`, and a status table
(`done` / `todo` / `in-progress`). Tracks 0–23 are **all marked done**.

### 3.2 Tracks 0–11 — platform mechanics

| Track | Subject | Load-bearing finding |
|---|---|---|
| 0 | Push collisions / `updater.yml` | Two workflows pushing the same ref collide; `updater.yml` was redundant with the engine — removed; `git pull --rebase` hardening |
| 1 | Cron drift | GitHub cron is best-effort (delayed/missed at high load); never assume schedule fidelity |
| 2 | Camo proxy | Third-party images proxied through `camo.githubusercontent.com` with HMAC + cache lag; repo-relative assets bypass Camo entirely |
| 3 | API budget | `GITHUB_TOKEN` ≈ 1,000 points/hr GraphQL — engine must short-circuit (→ state hashing, Track 13) |
| 4 | Commit graph | Push topology, who may write which ref |
| 5 | Rollback | Recovering a bad autonomous commit |
| 6 | Security | Workflow/`GITHUB_TOKEN` hardening (`permissions:` scoping) |
| 7 | Abuse limits | Keepalive/spam patterns risk ToS enforcement |
| 8 | Runner economics | Free minutes, job duration, caching |
| 9 | Sanitizer | GitHub's HTML sanitizer strips tags/attributes; markdown must be linted pre-commit |
| 10 | Idempotency | Identical inputs must produce byte-identical outputs or the commit graph grows forever |
| 11 | Rebase conflicts | Autonomous push conflicts and the rollback recipe |

### 3.3 Tracks 12–18 — signing, state, telemetry

- **Track 12 — web-flow GPG signing.** Server-side `createCommitOnBranch`
  commits are signed by GitHub's internal web-flow key
  `9684 79A1 AFF9 27E3 7D1A 566B B569 0EEE BB95 2194` → green *Verified* badge
  with zero runner keys. (Extended in Track 21.)
- **Track 13 — state hashing.** `compute_state_hash(config, metrics)` +
  `STATE_SHA` comment in README → rebuilds short-circuit when nothing changed.
- **Track 14 — keepalive.** 60-day workflow keepalive (commit `0d2f485`);
  interacts with Track 7's abuse finding.
- **Track 15 — GraphQL retry engine.** `STALE_DATA` retry classification →
  implemented as `MAX_STALE_RETRIES` backoff in the dispatcher.
- **Track 16 — Fastly CDN.** Edge eviction / asset freshness windows for
  GitHub-served assets.
- **Track 17 — workflow telemetry.** Reliability data surfaced into the README
  (later "live workflow reliability" in `f5666b9`).
- **Track 18 — hybrid dispatcher.** The two-tier commit design of §2.3.

### 3.4 Tracks 19–23 — the final five (verbatim-grade detail)

**Track 19 — GitHub Mobile asset caching & SVG engine profiling.**
- GitHub Mobile renders Markdown/SVG in embedded web containers: `WKWebView`
  (iOS, Swift) and Chromium `WebView` (Android, Kotlin/Compose). SVGs are **not**
  rasterised server-side; they are fetched raw and rasterised locally
  (CoreSVG/Skia).
- CSS `@keyframes` inside SVGs execute at 60/120 Hz. Failure modes found:
  WebKit evaluates `transform-origin` against the whole SVG canvas unless
  `transform-box: fill-box` is declared (elements orbit off-screen); `<text>`
  has no CSS box model (needs `<foreignObject>`, which GitHub strips); iOS Low
  Power Mode halts animation timers.
- The "stuck asset" illusion: pull-to-refresh re-fetches markdown but never
  evicts the webview's decoded-image cache, and suspended apps keep stale SVG
  DOMs for days — even though WebKit/Chromium honour the 300 s freshness window.
- Defensive font stack prescribed:
  `font-family: -apple-system-ui-monospace, 'SF Mono', 'Roboto Mono', 'Cascadia Code', 'Fira Code', 'JetBrains Mono', Menlo, Consolas, monospace;`
  plus `@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }`.

**Track 20 — SLA alerting & visual degradation signals.**
- Computed WCAG contrast ratios: `#22c55e` on dark card `#0b0f19` = **8.37:1**
  (AAA) but on light `#ffffff` = **2.29:1** (FAILS AA); amber `#fbbf24` 11.59:1
  dark → 1.65:1 light; crimson `#ef4444` 5.09:1 dark → 3.77:1 light. Hence a
  theme-aware SLA palette (`#15803d` / `#b45309` / `#b91c1c` for light mode).
- **Tri-layer redundant signalling** for colour-blindness (~8 % of males):
  colour + uppercase token (`[OPTIMAL]` / `[DEGRADED]` / `[CRITICAL]`) + glyph
  (● / ▲ / ⯃).
- **Schmitt-trigger hysteresis**: degrade if `R < 93 %` **or** `k_fail ≥ 2`;
  recover only if `R ≥ 96 %` **and** `k_fail = 0` **and** `m_success ≥ 3`;
  deadband 93–96 % holds prior state (anti-flap). Single 1-off flakes set a mild
  `WARNING` but suppress webhooks. Rationale: a 30-run window on a 6-hour cron
  spans ~7.5 days, so one failure lingers ~7 days.
- Zero-dependency notifications: `gh issue list … --label sla-incident` for
  dedup, auto-close on recovery, Discord/Slack via Python `urllib` / `curl`,
  `$GITHUB_OUTPUT` (`sla_state=DEGRADED`, `sla_transition=ALERT`) gating
  downstream steps.
- State persisted **git-natively in README**: `<!-- HARNESS:SLA
  {"state":"OPTIMAL","streak":0,…} -->`, parsed on pre-flight; alerts fire only
  on edge transitions.

**Track 21 — Ephemeral SSH signing under branch protection.**
- Ed25519 keygen on the runner: **< 15 ms**, no network; Git ≥ 2.34 signs with
  `gpg.format ssh` + `ssh-keygen -Y sign`.
- `POST /user/keys` ≠ `POST /user/ssh_signing_keys` — auth keys cannot sign;
  signing keys need scope `write:ssh_signing_key`.
- **`GITHUB_TOKEN` can never register signing keys** (installation token,
  `401/403 "Resource not accessible by integration"`; `github-actions[bot]` is
  not a user). The **secret-escalation paradox**: avoiding stored keys requires
  storing a PAT that can inject signing keys account-wide.
- Alternatives assessed: GraphQL `createCommitOnBranch` server-side web-flow
  signing (zero keys — the recommended path); **Sigstore/Gitsign is fatally
  rejected** by GitHub branch protection (`GH007 … doesn't have a valid
  signature`); artifact attestations can't sign commit objects.
- **The SaaS unverification trap**: deleting the ephemeral key retroactively
  flips every commit it signed to *Unverified*; not deleting it accumulates
  **1,460 orphaned keys/year** on a 6-hour cron; runner preemption leaks keys
  when cleanup never runs.

**Track 22 — Trigger suppression: PAT vs `GITHUB_TOKEN` vs App token.**
- Suppression binds to **token identity, not API**: `GITHUB_TOKEN` pushes
  suppress all `on: push` workflows (loop prevention); fine-grained/classic PATs
  and GitHub App tokens **trigger** them; `workflow_dispatch` /
  `repository_dispatch` always trigger.
- Fine-grained PAT needs `Contents: read+write`, plus `Workflows: read+write`
  if `.github/workflows/` files change (else 403), plus branch-protection
  bypass or it fails `BRANCH_PROTECTION_RULE_VIOLATION`.
- `[skip ci]` = global blunt instrument (all workflows, pre-scheduling);
  `paths` / `paths-ignore` = surgical routing (upstream ignores `README.md` +
  `assets/**`, downstream validator watches them).
- Verdict: intra-repo chaining should use native `on: workflow_run` with
  `if: github.event.workflow_run.conclusion == 'success'` — zero credentials,
  zero loops, verified badge retained.

**Track 23 — Dark-mode parity: `<picture>` vs in-SVG media queries.**
- **WebKit Bug 199134**: `WKWebView` does **not** evaluate
  `@media (prefers-color-scheme: dark)` inside SVGs loaded via `<img>` — iOS
  dark mode breaks completely, while Android Chromium honours it (asymmetric).
- HTML5 `<picture>` + `<source media="(prefers-color-scheme: dark)" srcset>`
  is evaluated at the host DOM level in both engines → seamless theme swap, and
  the client downloads **only one variant** (50 % bandwidth saved). Camo/Fastly
  cache the two files as distinct objects with independent ETags.
- GitHub has **deprecated** `#gh-dark-mode-only` / `#gh-light-mode-only` URL
  fragments — `<picture>` is the standard. (This branch's README already uses
  `<picture>`.)

### 3.5 Value: **5/5.**
Why: the densest evidence artifact in the repository — 24 tracks of
platform-mechanics research with quantified numbers (contrast ratios, key
accumulation rates, window arithmetic), every finding tied to an implementation
commit, and it drove the anti-stop hook.

### 3.6 Fate
Merged into `research/claude` (twice), then `main`; `docs/RESEARCH-LOG.md`
deleted by the v2 wipe; survives on `research/antigravity` and `archive/v1`.

---

## 4. `research/claude` — the measurement ledger, the bug ledger, the skill

**18 commits = antigravity's 14 + four exclusive ones** (`a3b4b74`, `d7feecf`,
`fbc7d9f`, `c4f1919`). This branch is where Claude's *own* work sits:
rendering measurements, two production bugs, and a packaged agent skill.

### 4.1 `docs/RESEARCH-CLAUDE.md` — ledger C0–C6 (8,382 bytes)

| ID | Severity | Finding |
|---|---|---|
| **C0** | P0 | `render_svg_banners()` interpolates config strings into SVG via a raw f-string — a bare `&` in a status/headline string produces **malformed XML** that GitHub renders as broken image. Fix: XML-escape config strings (commit `964dad3`) |
| **C1** | — | The sanitizer linter **false-succeeded** — it reported green while the SVG was unparseable. Fix: `ET.parse` XML well-formedness check in `lint_readme` (same commit `964dad3`) |
| **C2** | — | README content widths measured: **846 px** @1920, **831 px** @1280, **309 px** @390 (iPhone-class = binding constraint) |
| **C3** | — | Legibility: banner geometry 1200×240 (5:1) left only 62 px on mobile → 9.8/4.1/3.6 px type. Rebuilt at 900×300 (3:1) → 103 px, 22.0/11.7/11.3 px, all ≥ 11 px floor |
| **C4** | — | Fonts: GitHub CSP blocks external `@font-face` for image-referenced SVGs — `'JetBrains Mono'` was silently rendering as generic monospace; replace with system stacks |
| **C5** | — | Asset routing: repo-relative `./assets/*.svg` → `github.com/…/raw/…` (**not** Camo); third-party → `camo.githubusercontent.com/<hmac>/<hex-url>`; images clamp to container, never overflow |
| **C6** | — | Skill packaged: `skills/github-profile-readme/` (SKILL.md + 3 references + 5 examples) |

`964dad3` message: *"fix(harness): implement C1 (ET.parse XML well-formedness
linter) and C0 (XML-escape config strings in SVGs)"* — a genuine P0 found and
fixed by the agent against its own generator.

### 4.2 The banner rebuild (unique commit `fbc7d9f`)

*"feat(banner): apply measured rendering research to the hero banner"* — the
textbook measurement→artifact commit. From its message, every change traceable
to a ledger entry:

```text
- Geometry 1200x240 -> 900x300 (C3). At mobile the old 5:1 ratio left 62px of
  height and every line below the legibility floor: 9.8px / 4.1px / 3.6px.
  3:1 gives 103px and needs 32-unit type instead of 43…
- Type now 64 / 34 / 33 units -> 22.0px / 11.7px / 11.3px on a 309px phone.
  All three clear the 11px floor; previously none did.
- Fonts moved to system stacks (C4)… Eight occurrences replaced…
- Added fit_font_size(): SVG cannot wrap or measure text… shrinks to fit,
  refuses to go below the floor, and warns instead of silently clipping.
  It caught both lines overflowing by 25% and 49%.
- Acted on that warning by shortening the content rather than the type:
  headline 58 -> 27 chars…
- Headline fill changed from a gradient to a solid colour; gradients cost
  contrast at 11px. Banners carry role="img" and an aria-label.
```

### 4.3 `skills/github-profile-readme/` (unique commit `a3b4b74`)

`a3b4b74` — *"research(claude): profile-README skill, measured constraints, and
two P0/P1 bugs"* — adds **1,026 insertions** across 11 files: `SKILL.md` (180
lines), `references/{measured-constraints,banner-craft,svg-recipes}.md`, and
`examples/` (`before-banner.svg`, `after-banner.svg`,
`after-banner-light.svg`, `reference-banner-dark.svg`, `legibility-check.html`),
plus +214 lines in `RESEARCH-CLAUDE.md` and +151/−31 in `engine.py`.

SKILL.md section spine:

```text
# GitHub Profile README Engineering
## The three numbers that decide everything
## The legibility formula — apply before drawing anything
## Fonts: your font is not loading
## What survives when an SVG is referenced as an image
## Asset routing: repo-relative vs external
## Dark and light
## Process
## Anti-patterns
## References
```

Its core doctrine — *"Everything here was measured, not quoted. Method included
so it can be re-measured when GitHub changes its layout — treat the numbers as
perishable and the method as durable"* — with the actual measurement snippet
(`.js-profile-readme article.markdown-body` → `getBoundingClientRect().width`)
and the results table (1920→846, 1280→831, 390→309). It also explains why
published figures disagree (830 = this measurement at ~1280; 894 = repo README
or older layout) and records the routing experiment's output:

```json
{ "github.com": 6, "camo.githubusercontent.com": 3 }
```

### 4.4 The reconciling merges

- `d7feecf` *"merge: bring in Antigravity's C0/C1 fixes and tracks 7-19"* — parents
  `a3b4b74` + `a47ca5d`.
- `c4f1919` *"merge: Antigravity tracks 17-23, reconciling the font work"* — parents
  `fbc7d9f` + `f5666b9`. The commit message itself records a **content conflict
  between the two agents** (Claude's font stacks vs Antigravity's Track 19/23
  styling) that had to be reconciled by hand.

### 4.5 Value: **5/5.**
Why: the only branch that pairs *measured numbers* with *production bugs it
found in its own code* (C0/C1) and packages the result as a reusable skill —
the repo's best "knowledge survives the agent" artifact.

### 4.6 Fate
Fully merged to `archive/v1` → `main`; `docs/RESEARCH-CLAUDE.md` and `skills/`
deleted by the v2 wipe; survive on `research/claude` and `archive/v1`.

---

## 5. `v2/research` — the visual frontier (only live non-main work)

**70 commits = `main` (67) + 3 unique, dated 2026-09-25** — four days after the
archive. Era 2's continuation: *"how far can a profile README be pushed toward a
next-generation, game-quality, 3D-looking visual — while still loading
everywhere, reading on a phone, respecting reduced motion?"*

### 5.1 The three commits

| Commit | Message | Adds |
|---|---|---|
| `562090a` | *frontier: fixtures and probe for SVG lighting and animated raster formats* | `docs/frontier/fixtures/*.svg` (lighting specular/diffuse/spot + unfiltered controls), `anim.{avif,gif,png,webp}`, `embed-*.svg`, `tools/frontier/fixtures.py`, `tools/frontier/probe.mjs` |
| `5d877a4` | *frontier: fixture gallery and a probe that reads it back from github.com* | `docs/frontier/GALLERY.md`, `tools/frontier/probe_gh.mjs` |
| `3aa476f` | *frontier: A and B — SVG lighting works everywhere; GitHub pauses only GIFs for reduced motion* | `docs/frontier/README.md`, `docs/frontier/data/probe{,-github,-github-motion,-github-reduce}.json` |

### 5.2 Findings (from `docs/frontier/README.md`, measured — not argued)

**A · SVG lighting (`feSpecularLighting` / `feDiffuseLighting`).** Five fixtures
× three engines (Chromium 153, Firefox 155, WebKit 26.6), screenshot-compared
against unfiltered controls: **all five light in every engine**, and a *moving*
`fePointLight` animates everywhere — *"the single most 'real-looking' effect SVG
can produce — and it is safe."* Nothing in the 446-profile survey uses these
filters.

**B · Animated formats.** One 24-frame animation encoded four ways:

| Format | Size | Served as |
|---|--:|---|
| GIF | 33.9 KB | `image/gif` |
| APNG | 29.9 KB | `image/png` |
| animated WebP | 20.9 KB | `image/webp` |
| animated AVIF | **4.5 KB** | `image/avif` |

- GitHub wraps **GIF only** in an `<animated-image>` player and **pauses it for
  `prefers-reduced-motion`** → GIF is the one accessible-by-default animated
  format. APNG/WebP/AVIF ignore reduced motion (ship them via `<picture>`
  gated on the media query → still fallback).
- Animated **WebP** is the practical choice for rendered 3D (all three engines,
  ⅓ smaller than GIF, full colour).
- Frames **inside an SVG** animate in Chromium and WebKit but **freeze in
  Firefox** → single-file "rendered scene + SVG text" only works if the frozen
  frame is itself finished.
- AVIF is 7× smaller but did not decode in the tested Playwright WebKit build
  → flagged **UNVERIFIED**, not safe as the only file.

**Method honesty, self-caught:** the first pass reported GIF failing everywhere;
inspecting the DOM showed the `<animated-image>` player injects a hidden
zero-sized duplicate `<img>` and the probe let it overwrite the visible one.
The probe now keeps only visible images and records GitHub's wrapping — *"which
is how finding 1 surfaced at all."*

`GALLERY.md` renders every fixture inside github.com so the results are
re-checkable in the browser; `data/probe*.json` hold the raw three-engine
readings (local, github, github+motion, github+reduced-motion).

### 5.3 Value: **4/5.**
Why: it is the only branch with unmerged forward research, it converts the
book's "native/animated" prose into engine-by-engine evidence, and it
publishes its own methodological error. Loses a point because steps C–D–E
(real-3D CI render, pure-SVG lit flagship, side-by-side page) are still marked
`next` — the roadmap outgrew the results.

### 5.4 Fate
Live, unmerged — the current frontier of the whole repository.

---

## 6. `probe/cache` — the orphan cache probe

**3 commits, 2026-09-21, root commit `d7b3ca2`** — `git merge-base` with `main`
fails (exit ≠ 0): a deliberately disconnected single-file branch.

```text
d7b3ca2 probe: seed-b1455ee1
14e483b probe: t0-4aa9f9d1
1ca9afc probe: t1-f0aa81eb
```

Artifact: `cache-probe.svg` (400 × 60) whose visible text changes per commit
(`t1-f0aa81eb`, `t0-4aa9f9d1`, `seed-b1455ee1`). Purpose, reading the pattern
against Track 16 (Fastly edge eviction) and Track 19 (stuck-asset illusion):
**a canary for GitHub's asset cache** — push a new text payload, re-fetch, see
when the edge/webview actually stops serving the old bytes. Timestamps
(identical to the harness era) place it inside the same day's caching research.

### Value: **2/5.** Why: tiny and self-evident, but a real experiment design —
a content-identical-path mutation probe — and the only orphan branch in the repo.

### Fate
Unmerged, disconnected, unreferenced by any doc — a loose end.

---

## 7. `helper/side-person_opencode` — side branch, brief note

Tip `b7ce609`, 67 commits — **identical to `main`**, zero unique commits
(`main..helper` is empty). Nothing AI-specific lives there; recorded here only
so the branch census in this part is complete.

---

## 8. Cross-branch synthesis — what the branches prove

1. **The same research problem was attacked by two different agents and had to
   be merged twice** (`d7feecf`, `c4f1919`) — the second merge's subject
   (*"reconciling the font work"*) is direct evidence of a human-resolved
   content conflict between Claude's C4 font stacks and Antigravity's Tracks
   19/23 mobile styling.
2. **Findings were perishable and the repo knew it.** `measured-constraints.md`
   says *"treat the numbers as perishable and the method as durable"*; the
   widths (846/831/309), the `F_min` formula, and the Camo-vs-raw routing are
   the keep-list `PLAN-V2.md` refuses to lose.
3. **The agent found P0 bugs in its own generator** (C0 malformed SVG, C1
   false-success linter) and fixed them in `964dad3` — the strongest
   evidence-of-craft commit in the archive.
4. **The most valuable knowledge is negative**: `GITHUB_TOKEN` can never sign
   (Track 21), Sigstore will never satisfy branch protection (Track 21),
   in-SVG media queries are dead on iOS (Track 23), frames inside SVG freeze in
   Firefox (frontier B), `[skip ci]` silences everything (Track 22).
5. **Era 1 optimized for autonomy; era 2 for evidence.** The v2 wipe deleted the
   harness, hook, worker and skill but kept `PLAN-V2.md`'s measurements and
   `main`'s book/survey; the frontier branch continues the measurement discipline
   with probes instead of self-writing loops.

**Value ranking of the five branches:** `research/antigravity` 5,
`research/claude` 5, `archive/v1` 4, `v2/research` 4, `probe/cache` 2.

---

## Appendix A — full commit logs (dated)

### A.1 `archive/v1` (19) — superset of both research branches

```text
d5a44a3 2026-09-21 docs: plan v2 — return to the original profile README research goal
c4f1919 2026-09-21 merge: Antigravity tracks 17-23, reconciling the font work
fbc7d9f 2026-09-21 feat(banner): apply measured rendering research to the hero banner
f5666b9 2026-09-21 feat(research): complete tracks 17-23, integrate live workflow reliability, and mobile SVG styling
d7feecf 2026-09-21 merge: bring in Antigravity's C0/C1 fixes and tracks 7-19
a47ca5d 2026-09-21 feat(harness): implement hybrid commit dispatcher and record Track 18
0d2f485 2026-09-21 feat(keepalive): implement 60-day workflow keepalive, record Track 14, and mint Tracks 17-19
d821cd3 2026-09-21 docs(research): record Track 16 findings (Fastly CDN edge eviction and asset freshness)
99ba52f 2026-09-21 docs(research): record Track 15 findings (GraphQL createCommitOnBranch retry engine)
ff134fd 2026-09-21 feat(harness): implement state hashing short-circuit, dynamic section splicing, and complete research tracks 11-13
964dad3 2026-09-21 fix(harness): implement C1 (ET.parse XML well-formedness linter) and C0 (XML-escape config strings in SVGs)
a3b4b74 2026-09-21 research(claude): profile-README skill, measured constraints, and two P0/P1 bugs
0ed153c 2026-09-21 feat(research): complete tracks 6-10 (hardening, abuse limits, runner economics, sanitizer, byte idempotency) and configure continuation hook
aa67a97 2026-09-21 snapshot: working state of the profile blueprint
81e33cb 2026-09-20 fix(ci): eliminate redundant updater.yml and harden pushes with git pull --rebase
b88a793 2026-09-20 fix(harness): make the main-profile cross-link survive rebuilds
89a300e 2026-09-20 chore: initialize repository baseline
8afcffc 2026-09-20 Update README.md
389c6ef 2026-09-20 Initial commit
```

### A.2 `research/claude` (18)

A.1 minus `d5a44a3` (`docs: plan v2…` is unique to `archive/v1`). Verified via
`git log origin/research/claude` — identical order and hashes otherwise.

### A.3 `research/antigravity` (14)

A.1 minus `{d5a44a3, c4f1919, fbc7d9f, a3b4b74}` — i.e. the chain ends at
`f5666b9`. Exclusive set vs `research/claude` is **empty**:
`git log origin/research/claude..origin/research/antigravity` returns nothing.

### A.4 `v2/research` unique commits (3)

```text
3aa476f 2026-09-25 frontier: A and B — SVG lighting works everywhere; GitHub pauses only GIFs for reduced motion
5d877a4 2026-09-25 frontier: fixture gallery and a probe that reads it back from github.com
562090a 2026-09-25 frontier: fixtures and probe for SVG lighting and animated raster formats
```

### A.5 `probe/cache` (3, orphan root `d7b3ca2`)

```text
1ca9afc 2026-09-21 probe: t1-f0aa81eb
14e483b 2026-09-21 probe: t0-4aa9f9d1
d7b3ca2 2026-09-21 probe: seed-b1455ee1
```

---

## Appendix B — known gaps in this part

- **Track 0–11 finding bodies** were read in the earlier pass and are
  summarised in §3.2 rather than quoted at full length; Tracks 19–23 (§3.4) are
  quoted in near-verbatim detail.
- **`harness/engine.py` internals** (46,793 bytes) were inventoried by symbol
  and referenced through its bug ledger, but not read line-by-line; the
  `render_svg_banners` f-string (C0) is characterised from `RESEARCH-CLAUDE.md`
  and the fix commit, not quoted from source.
- **`docs/frontier/data/probe*.json`** raw readings were listed, not parsed;
  the frontier findings in §5.2 are taken from `docs/frontier/README.md`'s own
  tables.
- **`main`'s own 67 commits** (survey, book, showcase) belong to other parts of
  the compilation; only their role as `archive/v1`'s destination and
  `v2/research`'s base is described here.
- The **exact textual diff** of the two reconciling merges (what the font-work
  reconciliation changed line-by-line) was not extracted — the merge subjects
  and parents are documented, the hunks are not.
