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

Treat as **unsourced until re-verified**: `docs/01`–`docs/08`. Not deleted —
mined for hypotheses, then each claim either gets a citation or gets cut.

## The plan

### Phase 1 — Survey (the part never done)

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

### Phase 2 — Technique catalogue

Derive from Phase 1 only. For each technique: what it is, who uses it (link),
how it's built, whether it survives GitHub's sanitizer, how it behaves at 309px,
and whether it needs CI.

Covers: CSS keyframes vs SMIL, path/stroke-dash animation, gradients, masks,
clipping, filters and glow, typing effects, particles, charts and gauges,
animated text, contribution-graph art, terminal simulation, pseudo-interactive
components.

**Deliverable:** `docs/techniques/` — one file per family, each with a working
minimal example verified to render.

### Phase 3 — Platform capability matrix

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

Recommendation: **this repo, new branch `v2/research`.** The salvage list above
is most of its value and it's already public with history worth keeping.

Drop the two-agent path-ownership split — it existed to stop two agents
colliding and is now overhead. `docs/RESEARCH-LOG.md` and `docs/RESEARCH-CLAUDE.md`
merge into one ledger.

Keep `hammadshakeelai/github-profile-blueprint` as the research repo. The actual
profile ships separately to `hammadshakeelAl/hammadshakeelAl`, which still needs
auth for that account.

## Definition of done

- [ ] 60+ profiles catalogued with links and technique tags
- [ ] 25+ generators catalogued with liveness risk noted
- [ ] Every one screenshotted at 846px and 309px
- [ ] Technique catalogue where each entry cites a real user and has a verified
      minimal example
- [ ] Capability matrix with every cell tested
- [ ] Three rendered comps, one chosen with stated reasons
- [ ] Profile rebuilt against it
- [ ] Skill rewritten on the evidence
- [ ] No claim anywhere without a citation or an `UNVERIFIED` tag
