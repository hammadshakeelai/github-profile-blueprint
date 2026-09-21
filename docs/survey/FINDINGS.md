# Findings

What the survey data says, each claim tied to a number and the method that
produced it. Figures come from `data/summary.json` unless noted; the tables
behind them are `PROFILES.md`, `GENERATORS.md` and `TOOLS.md`.

## The sample

**446 personal profile READMEs**, in two populations that are reported
separately because they differ:

| Cohort | Profiles | How found | Represents |
|---|--:|---|---|
| **curated** | 187 | `abhisheknaiidu/awesome-github-profile-readme` (31k★) | Popular, widely copied — skews to the 2020–22 profile boom |
| **search** | 259 | GitHub code search for animation and filter primitives in committed `.svg` files, kept only in `username/username` repos | Ambitious — people hand-making SVGs |

487 candidates were collected; 38 turned out to be organisations (WebKit/WebKit,
Mailu/Mailu — an org page never shows a repo README as a profile), 2 were gone
and 1 had no README.

They reference **10,782 images (8,589 distinct URLs)**, every one of which was
fetched. The profiles were also loaded in headless Chrome to measure real
layout — **442 at phone width, 441 at desktop** — and 98% of rendered images
matched their fetched source.

The search cohort was chosen *for* hand-made SVGs, so its custom-SVG rates are
high by construction. Every other comparison between the cohorts — breakage,
theming, badge use, phone legibility — is independent of that selection.

---

## 1. Most-copied generators are dead, and free hosting killed them

**41% of profiles show at least one broken image** (39% curated, 44% search).

The single biggest cause is free-tier Vercel deployments being switched off:
**309 of the broken image URLs** return Vercel's `DEPLOYMENT_PAUSED` (215) or
`DEPLOYMENT_DISABLED` (94), confirmed from response headers (`Server: Vercel`,
`X-Vercel-Error`).

| Generator | Profiles using it | Images that load |
|---|--:|--:|
| github-readme-stats — public instance | 107 | **0%** |
| github-readme-activity-graph | 57 | **2%** |
| github-profile-trophy | 36 | **11%** |
| visitor badges (assorted) | 42 | 59% |
| spotify now-playing | 9 | 44% |
| github-readme-streak-stats | 95 | 97% |
| readme-typing-svg | 87 | 100% |
| profile views counter (komarev) | 103 | 100% |
| shields.io | 239 | 100% |

**24% of profiles still embed the dead github-readme-stats public instance** —
25% of the curated cohort and, notably, 24% of the ambitious one. The paused
instance returns the same 503 to a browser, to GitHub's own Camo proxy, and to
the survey client, so this is not the survey being blocked.

Repository metadata doesn't warn you. GitHub reports
`anuraghazra/github-readme-stats` as active (pushed 2026-08-31, not archived),
while its own README says it is no longer maintained and its public instance is
paused. Metadata said *active*, the README said *unmaintained*, the service said
*paused*. Only fetching the image told the truth.

**What survives:** services run on dedicated infrastructure (shields.io,
komarev, DenverCoder1's demolab.com services) and anything committed to the
profile repo itself. Committed images loaded 99% of the time (31 broken of
2,689 occurrences, mostly paths that no longer exist).

## 2. Most SVG cards are unreadable on a phone — and it's the phone's doing

GitHub's README column is **309px wide on a 390px phone** (846px on desktop),
and an SVG scales down as a single unit, text included.

Of **1,730 SVG cards** measured on the phone — badges and icons excluded —
**55% have their *largest* text under 11px.**

- **90% of those are phone-caused**: legible at the image's native width,
  illegible only after shrinking into the 309px column. Just 10% are too small
  on any device.
- **Profiles with at least one such card: 15% curated, 70% search.**
- **Hand-made cards fail more than services: 63% vs 37%.** Generator authors
  design at moderate widths; people crafting their own panels design wide
  canvases with small text, which is exactly what a phone punishes.
- **Desktop is not immune, just far better:** measured the same way at 1280px
  (441 profiles), 15% of profiles have at least one illegible card (137 cards)
  — 3% curated, 23% search. Mostly panels drawn wider than the 846px column.

Measured per generator (images in brackets): readme-typing-svg **54%** (98),
lowlighter/metrics **83%** (29), github-profile-summary-cards **60%** (52),
github-readme-streak-stats **23%** (90), self-hosted github-readme-stats **20%**
(82). shields.io's 53% (4,502) is by design rather than by phone: its
`for-the-badge` style sets text at 10px on every device.

Looking confirms the numbers. On a phone, JGit705's hero subtitle, chips,
terminal panel and stat-card labels turn to specks — while the markdown
paragraph right below them stays perfectly readable, because real text reflows
and an SVG doesn't.

The exception worth copying: ayxn07's display type is so large it survives
the shrink. Its headline system reads on a phone even where body copy doesn't.

## 3. Tables misbehave differently than you'd expect

21% of profiles put two or more images inside a table (HTML or markdown,
counted from the rendered page). On a phone, GitHub does one of two things,
neither of which is "shrink to fit":

- **Squeeze cards to share the row** — 640px cards measured at **76px** in a
  four-column table. 9% of profiles have cards crushed this way.
- **Keep cards full width and scroll the table sideways** — a 450px card stayed
  450px and the table scrolled to 532px. 7% of profiles.

The page itself never scrolls sideways (0 of 442): GitHub contains the overflow
inside the table.

## 4. Dark and light switching is rare

**20% of profiles switch images between dark and light themes** — 5% curated,
30% search. Of those that do, `<picture>` with `prefers-color-scheme`
dominates (80 profiles) over the older `#gh-dark-mode-only` fragment (7).

Separately, 35 profiles put `prefers-color-scheme` *inside* their SVGs (15 of
them alongside `<picture>`).
Inside an image, that media query follows the viewer's operating system, not
their GitHub theme setting, so it can mismatch the page. Whether it behaves
across GitHub's mobile clients is an open Phase 3 question.

## 5. Badge walls are common everywhere

**42% of profiles are more than half badges and icons** — 40% curated, 43%
search. Even people hand-crafting animated SVGs fill the rest of the page with
shields.

## 6. What hand-made SVGs actually use

Profiles using each technique in at least one bespoke SVG (counting profiles,
so one profile with forty files can't outvote forty with one):

| Technique | Profiles |
|---|--:|
| Gradients | 130 |
| SMIL animation (`<animate>`, `animateMotion`) | 129 |
| Filters | 102 |
| CSS `@keyframes` | 101 |
| Stroke-dash line drawing | 93 |
| Blur / glow (`feGaussianBlur`) | 90 |
| Clip paths | 90 |
| `prefers-color-scheme` inside the SVG | 35 |
| `<foreignObject>` | 32 |
| Masks | 28 |
| Embedded base64 fonts | 13 |
| Text on a path | 12 |

SMIL is used more than CSS keyframes in hand-made work. Both run in GitHub's
secure-animated-mode rendering; interaction and external resources don't.
Real example files for each are in `data/technique_exemplars.json`.

## 7. "Custom" isn't always original

Of **1,506 bespoke SVGs** (committed to the user's own repos and not a known
tool's output), 842 animate.

- **192 committed SVGs are generated** by five Actions, identified by
  signatures they leave in the file: snk and pacman-contribution-graph write
  `<desc>Generated with …</desc>`, lowlighter/metrics ends with
  `id="metrics-end"`, github-profile-3d-contrib uses `rb-l0-left` classes, and
  github-readme-stats cards carry `data-testid="card-title"`. Any other SVG
  announcing itself with a `Generated with/by` description is caught too.
- **Byte-identical copying is rare**: 29 files across 14 profiles.
- **Structural templates are not rare, and hashing can't see them.** Four
  profiles share one "Index Nº 001" layout with personalised text — found by
  looking, then confirmed by markers in their SVG source.
- A distinct recent style emerged: profiles built entirely from dozens of
  bespoke animated SVGs with separate `-dark` / `-light` files. The suspected
  clones among them turned out not to be — no pair shares more than 30% of its
  filenames.

## 8. Most profiles are automated, so "recently pushed" means little

**54% of profiles run GitHub Actions workflows** (41% curated, 63% search),
many committing on a schedule. That's why the median profile was last pushed
1.1 months ago, including many whose human content hasn't changed in years. A
push date is not evidence anyone is maintaining the page.

---

## Implications for the design

1. **Design for 309px first.** The legibility formula
   (`skills/github-profile-readme/references/measured-constraints.md`) applies
   to every card, not just the banner. Either keep text large relative to the
   viewBox, or keep reading text in markdown.
2. **Let markdown do the reading, SVG do the atmosphere.** The one layer that
   survives every screen is real text.
3. **Own your data panels.** Generate and commit them; the rented services are
   where the breakage is.
4. **Avoid image tables** for layout that must work on a phone.
5. **Ship dark and light as equals** through `<picture>`.
6. **The open space**: nobody surveyed is both visually ambitious *and* legible
   at 309px. That's the target.

## How the method was corrected along the way

Several first readings were wrong, and fixing them changed the results. Listed
because each would otherwise have been published as a false claim:

- **shields.io looked flaky** (92 persistent failures). It was the survey's own
  client failing on non-ASCII badge labels, which browsers percent-encode and
  Python didn't. After fixing: 99.7% loaded.
- **Single-pass timeouts overstated breakage.** A slow, spaced second attempt
  recovered 39 of 151 in the first run.
- **38 "profiles" were organisations** matched by the owner-equals-repo rule.
- **Badge text was read as 100px.** shields.io draws at `font-size="110"` and
  scales by 0.1. Text sizes are now computed by walking the SVG tree with
  inherited sizes, CSS classes and transforms (97% of text-bearing SVGs); the
  rest fall back to a flat scan.
- **The column-fit model was wrong inside tables** (see §3), so phone figures
  come from measured layout, not the formula.
- **Badges counted as illegible cards.** They're small on every device by
  design, so they're excluded from card statistics.
- **Unrecognised third-party hosts were counted as bespoke.** Only files in the
  user's own repos, or on a domain carrying their name, count now.
- **Committed Action output was counted as hand-made.** A pacman contribution
  graph in 10 profiles slipped past the fingerprint list; generators that
  describe themselves in a `<desc>` element are now detected generically.
- **A desktop figure briefly read 0%.** No desktop layout had been measured yet,
  so the pool was empty. It never reached this document; the measured figure
  is 15%.

## Limits

- Legibility is measured from SVG `<text>` only. Raster images with text, and
  SVGs whose lettering is outlined into paths (ayxn07), can't be scored.
- The 11px floor is a design threshold, not a hard perceptual limit.
- Layout was measured in dark mode at two widths (390px phone, 1280px desktop).
  Light mode, other widths and GitHub's native mobile apps are Phase 3.
- Breakage is a snapshot of September 2026 from one network location.
- Code search returns at most 1,000 hits per query, so the search cohort is a
  large sample of ambitious profiles, not all of them.
