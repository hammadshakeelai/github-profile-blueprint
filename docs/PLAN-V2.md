# Plan v2 — back to the original goal

## What went wrong

The original goal was a **research and design** task: survey the best GitHub
profile READMEs in the wild, build a library of SVG techniques, generators and
references, and use that to design something premium.

What got built was **infrastructure**: a compiler, a commit dispatcher, state
hashing, keepalives, rate-limit accounting, WebKit workarounds. Twenty-four
research tracks, almost all of them about making a pipeline reliable.

That work isn't wasted — but it answered "how do we ship an asset dependably"
before anyone answered "what asset is worth shipping". The design brief was
skipped and the plumbing was built around a placeholder.

The tell, measurable: `docs/06-the-encyclopedia-of-creativity.md` contains
**2 external references**. A survey doc with no survey in it. Every design doc
in `docs/` was written from general knowledge rather than from looking at real
profiles. That is the hole this plan fills.

## Standing rule for v2

**No design doc may be written before the examples that justify it are
collected.** Every technique claim cites a real profile or repository that uses
it, with a link. If it can't be pointed at, it doesn't go in.

The failure mode last time was fluent writing that sounded researched. Citations
are the cure, not longer prose.

## What the repo keeps (the "friend")

Genuinely load-bearing, carry forward unchanged:

| Keep | Why |
|---|---|
| Measured container widths — 846 / 831 / 309 | Measured from live DOM. Foundational to every layout decision. |
| Legibility formula `F_min = target × W / R` | Turns "looks small" into arithmetic. |
| Camo vs raw routing, verified two ways | Decides generated-and-committed vs third-party hosted. |
| Secure animated mode facts | Defines the ceiling: animation yes, interaction no. |
| Font/CSP behaviour + the stack | Explains why most banners don't look as designed. |
| `skills/github-profile-readme/` | Correct shape. Needs the survey poured into it. |
| XML escaping + `ET.parse` linting | Real bugs, real fixes. Keep. |
| Idempotency machinery (state hash, `SOURCE_DATE_EPOCH`) | Needed the moment anything is generated. |

Keep but **park** — correct work, premature, revisit only if a design needs it:
hybrid commit dispatcher, verified-commit GraphQL path, 60-day keepalive, live
CI telemetry gauge, SLA hysteresis. None of these should drive design decisions.

**Left behind** on `archive/v1`: `docs/01`–`docs/08`. They were written from
general knowledge and read as authoritative; mining them would smuggle
unsourced claims into v2 wearing Phase 1 citations. The technique catalogue
starts empty and is built only from survey evidence.

## The plan

### Phase 1 — Survey (the part never done) — **done**

> **Outcome:** 446 personal profiles (187 curated, 259 found by technique-first
> code search), 10,782 images fetched, phone layout measured for 442 in headless
> Chrome, 65 tool repositories health-checked, 15 shortlisted after visual
> review. Exceeds every target below. See `docs/survey/FINDINGS.md` and
> `docs/survey/SHORTLIST.md`.
>
> Two changes from the original plan, both forced by evidence: screenshots were
> taken for the shortlist rather than all 60+ (real layout measurement replaced
> eyeballing for the rest, and proved more accurate), and a second, technique-
> first source was added because the curated list only shows what's popular.

Build the library. Breadth first, judgement later.

- **1.1** Collect **60+ real profile READMEs** worth studying. Sources: awesome-
  github-profile-readme lists, GitHub search on profile repos, trending, and
  the generators' own showcase galleries. Record: URL, what's notable, which
  techniques, whether assets are generated or static, whether it still renders.
- **1.2** Collect **25+ SVG/generator repositories** — stats cards, activity
  graphs, typing SVGs, snake/contribution art, terminal simulators, chart and
  gauge generators. Record what each produces, hosted vs self-hosted, liveness
  risk.
- **1.3** Screenshot every one at **846px and 309px**. This is where most of
  them will fail, and that failure is the finding.
- **1.4** Rank into a shortlist of ~15 that are genuinely exceptional rather
  than merely busy.

**Deliverable:** `docs/survey/PROFILES.md`, `docs/survey/GENERATORS.md`, plus a
screenshot set. Data, not opinion.

### Phase 2 — Technique catalogue — **done**

> **Outcome:** `docs/techniques/` — a catalogue of every technique with survey
> usage counts and cited real files, 23 original examples, a gallery rendered by
> GitHub, and `tools/techniques/verify.py`, which checks each example inside
> GitHub's page at two widths and both schemes. All 14 animated examples were
> seen animating; three theme mechanisms verified; scripts, web-font imports
> and external images verified blocked; `<foreignObject>` verified rendering in
> Chrome. One surprise: a blocked external image shows a broken-image icon.
>
> Deviation: one catalogue file rather than one per family — the entries are
> short and cross-reference each other, so a single page reads better.

> **Already banked from Phase 1:** `docs/survey/data/technique_exemplars.json`
> holds up to eight real bespoke SVGs per technique, spread across profiles and
> preferring ones whose images all load, plus usage counts by profile. So
> Phase 2 is not discovery. For each technique: open the cited exemplars,
> extract the minimal pattern, verify it renders on GitHub (desktop and phone),
> and write it up. Techniques with almost no users (`<script>`: 1, embedded SVG
> images: 3) go in a short "seen but rare" note rather than getting entries —
> an entry implies the technique is viable, and one user isn't evidence.

Derive from Phase 1 only. For each technique: what it is, who uses it (link),
how it's built, whether it survives GitHub's sanitizer, how it behaves at 309px,
and whether it needs CI.

Covers: CSS keyframes vs SMIL, path/stroke-dash animation, gradients, masks,
clipping, filters and glow, typing effects, particles, charts and gauges,
animated text, contribution-graph art, terminal simulation, pseudo-interactive
components.

**Deliverable:** `docs/techniques/` — one file per family, each with a working
minimal example verified to render.

### Phase 3 — Platform capability matrix — **done**

> **Outcome:** `docs/CAPABILITY-MATRIX.md`, generated from captures in
> Chromium 153, Firefox 155 and WebKit 26.6 (Safari's engine), each at 1280px
> and 390px in both schemes, scored by the same code as the Chrome pass. Found
> one real engine difference — WebKit never animates `gradientTransform` — and
> measured update latency: ~302s on a branch URL, ~5s commit-pinned. iOS Safari
> and the GitHub mobile apps can't be driven from here, so the matrix ends with
> a by-hand checklist for them.

Extend the existing measurements into a single table: desktop web, mobile web,
GitHub mobile app, light, dark. Each cell tested, not assumed. Absorbs the
WebKit findings already made.

**Deliverable:** `docs/CAPABILITY-MATRIX.md`, with method so it can be re-run.

### Phase 4 — Design direction

Only now. Three distinct concepts, each a real comp rendered at both widths, not
a description:

- one restrained and typographic
- one dense and instrument-panel
- one unexpected — the concept that isn't a stat card

Pick one deliberately, with reasons. Include what it deliberately omits.

**Deliverable:** `docs/DIRECTION.md` + three comps.

### Phase 5 — Build

Rebuild the profile against the chosen direction, reusing the parked
infrastructure where it earns its place. Static unless a value genuinely
changes; generated where it does.

### Phase 6 — Fold back into the skill

Rewrite `skills/github-profile-readme/` on top of real evidence: the catalogue
becomes its references, the survey its examples, the matrix its constraints.

## Sequencing

Phases are ordered because each depends on the last. The one rule that matters:
**Phase 4 cannot start before Phases 1–3 are done.** Jumping to design with
infrastructure instinct is exactly what happened the first time.

Phase 1 is the long pole and the highest value. If only one phase ever gets
done, make it that one.

## Where the work lives

**Decided and done:** this repo, branch `v2/research`, started from a clean tree.
Everything from v1 is frozen unchanged on `archive/v1`; only the measured
material (the skill) was carried forward. `docs/01`–`08` stayed behind on the
archive rather than sitting next to new docs as peers.

The two-agent path-ownership split is dropped — it existed to stop two agents
colliding and is now overhead.

Keep `hammadshakeelai/github-profile-blueprint` as the research repo. The actual
profile ships separately to `hammadshakeelAl/hammadshakeelAl`, which still needs
auth for that account.

## Definition of done

- [x] 60+ profiles catalogued with links and technique tags — 446
- [x] 25+ generators catalogued with liveness risk noted — 40+ services, 65 repos
- [x] Every one checked at desktop and phone width — real layout measured for
      442 (phone) and 441 (desktop); the 20 shortlisted also screenshotted
- [x] Technique catalogue where each entry cites a real user and has a verified
      minimal example
- [x] Capability matrix with every cell tested (except the hand-check rows)
- [ ] Three rendered comps, one chosen with stated reasons
- [ ] Profile rebuilt against it
- [ ] Skill rewritten on the evidence
- [ ] No claim anywhere without a citation or an `UNVERIFIED` tag
