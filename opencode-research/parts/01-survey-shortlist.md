# Part 01 — The Survey: 446 Profiles Measured (repo's own research)

Everything in this part comes from Phase 1 of the github-profile-blueprint repo: the survey in `docs/survey/`. No outside sources. The survey measured **446 real GitHub profile READMEs**, fetched **10,782 images**, rendered **442 profiles at phone width and 441 at desktop width** in headless Chrome, health-checked **65 tool repositories**, and screenshotted **20 shortlisted profiles**. Files: [FINDINGS.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/survey/FINDINGS.md) (statistics + method), [SHORTLIST.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/survey/SHORTLIST.md) (the profiles), [GENERATORS.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/survey/GENERATORS.md), [TOOLS.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/survey/TOOLS.md), [PROFILES.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/survey/PROFILES.md) (all 446 rows), and `data/*.json`.

---

## What the survey is

From `docs/survey/README.md`: a library of real GitHub profile READMEs and the generators they depend on, "built from evidence rather than general knowledge. Every row is filled by fetching the actual README and every image it references, and phone behaviour is measured from real rendered layout."

**446 personal profiles · 10,782 images fetched · layout measured for 442 at phone and 441 at desktop width · 65 tool repositories health-checked · 20 shortlisted and screenshotted.**

### The sample, exactly as reported

| Cohort | Profiles | How found | Represents |
|---|--:|---|---|
| **curated** | 187 | `abhisheknaiidu/awesome-github-profile-readme` (31k★) | Popular, widely copied — skews to the 2020–22 profile boom |
| **search** | 259 | GitHub code search for animation and filter primitives in committed `.svg` files, kept only in `username/username` repos | Ambitious — people hand-making SVGs |

487 candidates were collected; 38 turned out to be organisations (WebKit/WebKit, Mailu/Mailu — an org page never shows a repo README as a profile), 2 were gone and 1 had no README.

They reference **10,782 images (8,589 distinct URLs)**, every one of which was fetched. The profiles were also loaded in headless Chrome to measure real layout — **442 at phone width, 441 at desktop** — and 98% of rendered images matched their fetched source.

Image origins across the corpus: **2,689 committed**, **7,934 third-party**, **159 GitHub uploads** (from `data/summary.json`). 344 profiles were pushed within 12 months, 41 more than 36 months ago, median time since push **1.1 months**.

The search cohort was chosen *for* hand-made SVGs, so its custom-SVG rates are high by construction. Every other comparison between the cohorts — breakage, theming, badge use, phone legibility — is independent of that selection. Both cohorts are reported separately throughout.

### How it was measured

Everything re-runs from `tools/survey/`:

| Step | Script | Does |
|---|---|---|
| 1 | `source_codesearch.py` | Technique-first candidate discovery via code search |
| 2 | `harvest.py` | Fetches each profile's README via the API, resolves and fetches every image, derives SVG metrics |
| 3 | `layout.py` | Loads each live profile in headless Chrome at 390px and 1280px and records every image's rendered box |
| 4 | `analyze.py` | Builds `PROFILES.md`, `GENERATORS.md`, `summary.json` |
| 5 | `tools_health.py` | Maintenance status of the tool repositories → `TOOLS.md` |
| 6 | `shortlist.py` | Ranks candidates worth looking at (a pre-filter, not the judgement) |
| 7 | `screenshot.py`, `contact_sheet.py` | Captures and tiles pages for visual review |

The search query for the ambitious cohort was GitHub code search for these primitives in committed `.svg` files, kept only to `username/username` repos owned by a person:

```
animateMotion, animateTransform, stroke-dashoffset, keyframes,
feGaussianBlur, feTurbulence, feDisplacementMap, textPath,
prefers-color-scheme
```

Privacy and safety: nothing copied from the READMEs themselves is stored — the repo keeps links and derived measurements; README text and image bodies live in a gitignored cache (`.cache/survey/`). The GitHub token is sent to `api.github.com` only; SVGs from third-party hosts are treated as untrusted and refused if they declare a DTD or entities.

**How the shortlist was chosen:** `tools/survey/shortlist.py` ranked every profile by how much of its own visual work actually renders — bespoke SVGs, animation, dark/light support — and penalised breakage, badge walls and phone-illegible cards. The top 30 from that ranking, plus the ten strongest from the curated list, were screenshotted at 390px and 1280px and **looked at**. "Ranking is not judgement: several high scorers turned out competent but conventional, and the scorer can't see an idea."

---

## Survey-wide findings

Eight numbered findings from FINDINGS.md, each tied to its numbers.

### 1. Most-copied generators are dead, and free hosting killed them

**41% of profiles show at least one broken image** (39% curated, 44% search).

The single biggest cause is free-tier Vercel deployments being switched off: **309 of the broken image URLs** return Vercel's `DEPLOYMENT_PAUSED` (215) or `DEPLOYMENT_DISABLED` (94), confirmed from response headers (`Server: Vercel`, `X-Vercel-Error`).

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

**24% of profiles still embed the dead github-readme-stats public instance** — 25% of the curated cohort and, notably, 24% of the ambitious one. The paused instance returns the same 503 to a browser, to GitHub's own Camo proxy, and to the survey client, so this is not the survey being blocked.

Repository metadata doesn't warn you: GitHub reports `anuraghazra/github-readme-stats` as active (pushed 2026-08-31, not archived), while its own README says it is no longer maintained and its public instance is paused. Metadata said *active*, the README said *unmaintained*, the service said *paused*. Only fetching the image told the truth.

**What survives:** services run on dedicated infrastructure (shields.io, komarev, DenverCoder1's demolab.com services) and anything committed to the profile repo itself. Committed images loaded **99%** of the time (31 broken of 2,689 occurrences, mostly paths that no longer exist).

Full failure-reason counts over distinct URLs (`data/summary.json`): `vercel-paused` 215, `vercel-disabled` 94, `http-404` 68, `error-card` 25, `http-403` 17, `http-410` 15, `dns` 9, `http-500` 7, `http-400` 7, `network` 5, `not-image` 2, `http-429` 2, `timeout` 1, `http-504` 1 — 490 broken occurrences across 185 profiles.

### 2. Most SVG cards are unreadable on a phone — and it's the phone's doing

GitHub's README column is **309px wide on a 390px phone** (846px on desktop), and an SVG scales down as a single unit, text included.

Of **1,730 SVG cards** measured on the phone — badges and icons excluded — **55% have their *largest* text under 11px.**

- **90% of those are phone-caused**: legible at the image's native width, illegible only after shrinking into the 309px column. Just 10% are too small on any device.
- **Profiles with at least one such card: 15% curated, 70% search.**
- **Hand-made cards fail more than services: 63% vs 37%.** Generator authors design at moderate widths; people crafting their own panels design wide canvases with small text, which is exactly what a phone punishes.
- **Desktop is not immune, just far better:** measured the same way at 1280px (441 profiles), 15% of profiles have at least one illegible card (137 cards) — 3% curated, 23% search. Mostly panels drawn wider than the 846px column.

Measured per generator (images in brackets): readme-typing-svg **54%** (98), lowlighter/metrics **83%** (29), github-profile-summary-cards **60%** (52), github-readme-streak-stats **23%** (90), self-hosted github-readme-stats **20%** (82). shields.io's **53%** (4,502) is by design rather than by phone: its `for-the-badge` style sets text at 10px on every device.

Looking confirms the numbers. On a phone, JGit705's hero subtitle, chips, terminal panel and stat-card labels turn to specks — while the markdown paragraph right below them stays perfectly readable, because real text reflows and an SVG doesn't.

The exception worth copying: ayxn07's display type is so large it survives the shrink. Its headline system reads on a phone even where body copy doesn't.

Cohort detail (`data/summary.json`): 6,500 text-bearing card slots measured; 2,810 fully illegible on mobile, 3,332 with some illegible text on mobile, 2,682 with some illegible text on desktop; **252 profiles** have at least one illegible card. Illegible-card rates by origin, all profiles: **bespoke 672/1,065 (63%)**, **service 198/532 (37%)**, generated 71/131 (54%), copied 2/2 (100%).

### 3. Tables misbehave differently than you'd expect

21% of profiles put two or more images inside a table (HTML or markdown, counted from the rendered page). On a phone, GitHub does one of two things, neither of which is "shrink to fit":

- **Squeeze cards to share the row** — 640px cards measured at **76px** in a four-column table. 9% of profiles have cards crushed this way.
- **Keep cards full width and scroll the table sideways** — a 450px card stayed 450px and the table scrolled to 532px. 7% of profiles.

The page itself never scrolls sideways (0 of 442): GitHub contains the overflow inside the table.

### 4. Dark and light switching is rare

**20% of profiles switch images between dark and light themes** — 5% curated, 30% search. Of those that do, `<picture>` with `prefers-color-scheme` dominates (**80 profiles**) over the older fragment form (**7 profiles**).

```
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="…-dark.svg">
  <img src="…-light.svg" alt="…">
</picture>
```

(The legacy alternative seen in 7 profiles is the `#gh-dark-mode-only` fragment suffix on a single URL.)

Separately, **35 profiles** put `prefers-color-scheme` *inside* their SVGs (15 of them alongside `<picture>`). Inside an image, that media query follows the viewer's operating system, not their GitHub theme setting, so it can mismatch the page. Whether it behaves across GitHub's mobile clients is an open Phase 3 question.

Counts from `data/summary.json`'s `theme_switch`: none 359, picture 80, fragment 7.

### 5. Badge walls are common everywhere

**42% of profiles are more than half badges and icons** — 40% curated, 43% search. Even people hand-crafting animated SVGs fill the rest of the page with shields.

### 6. What hand-made SVGs actually use

Profiles using each technique in at least one bespoke SVG (counting profiles, so one profile with forty files can't outvote forty with one):

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

SMIL is used more than CSS keyframes in hand-made work. Both run in GitHub's secure-animated-mode rendering; interaction and external resources don't. Real example files for each are in `data/technique_exemplars.json` (781 lines of per-technique exemplar URLs — e.g. gradient exemplars from sepahead, Dhyanesh006 and ashfordeOU; clip-path from ayxn07; theme-aware SVG from umang-eng and YoraiLevi).

Corpus-wide technique counts over all 6,844 distinct SVGs (1,472 animated), from `data/summary.json`: gradient 2,429 · embedded-svg 2,301 · clip-path 1,775 · filter 1,632 · blur-glow 1,556 · css-keyframes 920 · smil 703 · stroke-draw 432 · mask 368 · theme-aware-svg 316 · foreign-object 156 · embedded-font 151 · text-path 118 · embedded-raster 104 · script 8. SVG origins: badge-icon 4,434 · bespoke 1,506 · service 683 · generated 192 · copied 29. Of the 1,506 bespoke SVGs, **842 animate**.

### 7. "Custom" isn't always original

Of **1,506 bespoke SVGs** (committed to the user's own repos and not a known tool's output), 842 animate.

- **192 committed SVGs are generated** by five Actions, identified by signatures they leave in the file. The signatures, verbatim from FINDINGS.md:

```
<desc>Generated with …</desc>          (snk, pacman-contribution-graph)
id="metrics-end"                       (lowlighter/metrics)
rb-l0-left classes                     (github-profile-3d-contrib)
data-testid="card-title"               (github-readme-stats cards)
```

Any other SVG announcing itself with a `Generated with/by` description is caught too.

- **Byte-identical copying is rare**: 29 files across 14 profiles.
- **Structural templates are not rare, and hashing can't see them.** Four profiles share one "Index Nº 001" layout with personalised text — found by looking, then confirmed by markers in their SVG source.
- A distinct recent style emerged: profiles built entirely from dozens of bespoke animated SVGs with separate `-dark` / `-light` files. The suspected clones among them turned out not to be — no pair shares more than 30% of its filenames.

### 8. Most profiles are automated, so "recently pushed" means little

**54% of profiles run GitHub Actions workflows** (41% curated, 63% search), many committing on a schedule. That's why the median profile was last pushed 1.1 months ago, including many whose human content hasn't changed in years. A push date is not evidence anyone is maintaining the page. (`data/summary.json`: 240 profiles with workflows.)

---

## The legibility arithmetic (the survey's central constraint)

- **390px phone → 309px README column.** Images are hard-capped to the column; 309px is the number that kills banners. Desktop column: 846px at 1280px viewport.
- **The floor is 11px**: a card counts as illegible on a phone when its *largest* `<text>` renders under 11px in that 309px column.
- **55% of 1,730 cards fail it; 90% of those failures are phone-caused.**
- Text sizes are computed by walking the SVG tree with inherited sizes, CSS classes and transforms (97% of text-bearing SVGs); the rest fall back to a flat scan.
- Badges are excluded from card statistics — they're small on every device by design.
- The limits, stated by the survey: legibility is measured from SVG `<text>` only (raster text and path-outlined lettering, like ayxn07's, can't be scored); the 11px floor is a design threshold, not a hard perceptual limit; layout was measured in dark mode at two widths only; breakage is a snapshot of September 2026 from one network location; code search returns at most 1,000 hits per query, so the search cohort is a large sample of ambitious profiles, not all of them.

**Design implications listed by the survey:**

1. **Design for 309px first.** Either keep text large relative to the viewBox, or keep reading text in markdown.
2. **Let markdown do the reading, SVG do the atmosphere.** The one layer that survives every screen is real text.
3. **Own your data panels.** Generate and commit them; the rented services are where the breakage is.
4. **Avoid image tables** for layout that must work on a phone.
5. **Ship dark and light as equals** through `<picture>`.
6. **The open space**: nobody surveyed is both visually ambitious *and* legible at 309px. That's the target.

### How the method was corrected along the way

Listed in FINDINGS.md because each would otherwise have been published as a false claim:

- **shields.io looked flaky** (92 persistent failures). It was the survey's own client failing on non-ASCII badge labels, which browsers percent-encode and Python didn't. After fixing: 99.7% loaded.
- **Single-pass timeouts overstated breakage.** A slow, spaced second attempt recovered 39 of 151 in the first run.
- **38 "profiles" were organisations** matched by the owner-equals-repo rule.
- **Badge text was read as 100px.** shields.io draws at `font-size="110"` and scales by 0.1. Text sizes are now computed by walking the SVG tree.
- **The column-fit model was wrong inside tables** (see finding 3), so phone figures come from measured layout, not the formula.
- **Badges counted as illegible cards.** They're small on every device by design, so they're excluded.
- **Unrecognised third-party hosts were counted as bespoke.** Only files in the user's own repos, or on a domain carrying their name, count now.
- **Committed Action output was counted as hand-made.** A pacman contribution graph in 10 profiles slipped past the fingerprint list; generators that describe themselves in a `<desc>` element are now detected generically.
- **A desktop figure briefly read 0%.** No desktop layout had been measured yet, so the pool was empty. It never reached the document; the measured figure is 15%.

---

## The generators, ranked by use

From GENERATORS.md (every image service seen, ranked by how many profiles use it). **Live** = share of distinct image URLs that returned a usable image; **illegible on phone** = share of its rendered images whose largest text is under 11px at 390px, with the count in brackets.

| Generator | Profiles | URLs | Live | Main failure | Median ms | Illegible on phone |
|---|--:|--:|--:|---|--:|--:|
| shields.io badges | 239 | 3690 | 100% | error-card ×10 | 690 | 53% (4502) |
| github-readme-stats — public instance | 107 | 215 | **0%** | vercel-paused ×215 | 370 | — |
| profile views counter (komarev) | 103 | 103 | 100% | — | 1701 | 45% (103) |
| github-readme-streak-stats | 95 | 97 | 97% | vercel-disabled ×3 | 2708 | 23% (90) |
| readme-typing-svg | 87 | 103 | 100% | — | 1112 | 54% (98) |
| snk contribution snake | 67 | 74 | 93% | http-404 ×5 | 952 | 100% (2) |
| other users' repos (raw assets) | 58 | 241 | 89% | http-404 ×27 | 1081 | 21% (14) |
| github-readme-activity-graph | 57 | 58 | **2%** | vercel-disabled ×55, http-404 ×2 | 536 | 100% (1) |
| skill-icons | 56 | 197 | 100% | — | 330 | — |
| visitor badge | 42 | 44 | 59% | http-410 ×14, dns ×3 | 1448 | 67% (24) |
| GitHub upload (user-attachments) | 41 | 89 | 99% | http-403 ×1 | 1923 | 100% (1) |
| capsule-render | 41 | 65 | 100% | — | 675 | 28% (29) |
| github-readme-stats — self-hosted | 39 | 86 | 94% | vercel-disabled ×3, http-410 ×1 | 1897 | 20% (82) |
| github-profile-trophy | 36 | 37 | **11%** | vercel-disabled ×31, http-404 ×1 | 939 | 100% (4) |
| giphy | 35 | 66 | 98% | http-404 ×1 | 2336 | — |
| icon CDNs (icons8 / vectorlogo.zone / iconify / wikimedia / flaticon) | 31 | 189 | 92% | http-400 ×7, http-403 ×4 | 617 | 100% (2) |
| devicon | 27 | 201 | 100% | http-403 ×1 | 755 | — |
| github-profile-summary-cards | 20 | 53 | 89% | error-card ×6 | 2616 | 60% (52) |
| readme-jokes / quotes | 19 | 15 | 93% | not-image ×1 | 1306 | 6% (17) |
| simple-icons | 17 | 72 | 100% | — | 506 | — |
| lowlighter/metrics | 15 | 30 | 97% | http-404 ×1 | 1196 | 83% (29) |
| GitHub avatars | 13 | 159 | 100% | — | 516 | — |
| donation buttons (buymeacoffee / ko-fi) | 10 | 6 | 83% | http-403 ×1 | 568 | — |
| holopin badges | 9 | 9 | 100% | — | 4952 | — |
| spotify now-playing | 9 | 9 | 44% | http-500 ×2, network ×1 | 2539 | 0% (4) |
| demolab badges & cards (DenverCoder1) | 8 | 67 | 97% | http-404 ×2 | 989 | 25% (68) |
| imgur | 8 | 23 | 96% | http-403 ×1 | 1508 | — |
| wakatime (wakatime / athul/waka-readme) | 8 | 9 | 100% | — | 2229 | 44% (9) |
| emoji GIFs (slackmojis / partyparrot) | 7 | 27 | 100% | — | 1069 | — |
| techstack-generator | 7 | 16 | 100% | — | 402 | 9% (11) |
| moe-counter | 6 | 7 | 100% | — | 1768 | 100% (1) |
| tenor | 6 | 17 | 100% | — | 3753 | — |
| github-profile-trophy — forks | 5 | 5 | 100% | — | 2562 | 100% (5) |
| leetcode cards | 5 | 6 | 100% | — | 1469 | 100% (5) |
| stackoverflow cards | 5 | 5 | 100% | — | 1314 | 20% (5) |
| committers.top badge | 4 | 4 | 100% | — | 1292 | 100% (4) |
| lowlighter/metrics — hosted | 3 | 3 | **0%** | http-500 ×2, timeout ×1 | 13428 | — |
| contribution chart (ghchart) | 2 | 2 | 100% | — | 2512 | 100% (2) |

## The 65 tool repositories

TOOLS.md: **65 repositories: 38 active, 11 slowing, 12 dormant, 4 archived.** Definitions: active = pushed within 6 months · slowing = within 2 years · dormant = older · archived = read-only · gone = missing or renamed. "Pushes include bot and dependency-update commits, so *active* means the repository is touched, not necessarily that a human is developing it."

The top of the table (stars, last push, status):

| Repository | Stars | Last push | Status |
|---|--:|---|---|
| anuraghazra/github-readme-stats | 79,816 | 2026-08-31 | active |
| abhisheknaiidu/awesome-github-profile-readme | 31,120 | 2026-09-11 | active |
| badges/shields | 27,202 | 2026-09-19 | active |
| simple-icons/simple-icons | 25,889 | 2026-09-20 | active |
| rahuldkjain/github-profile-readme-generator | 24,443 | 2025-10-28 | slowing |
| lowlighter/metrics | 17,213 | 2026-05-29 | active |
| Ileriayo/markdown-badges | 17,062 | 2026-08-11 | active |
| tandpfun/skill-icons | 13,145 | 2026-02-27 | slowing |
| devicons/devicon | 11,831 | 2026-09-19 | active |
| DenverCoder1/readme-typing-svg | 9,352 | 2026-09-17 | active |
| DenverCoder1/github-readme-streak-stats | 7,142 | 2026-09-17 | active |
| ryo-ma/github-profile-trophy | 6,655 | 2026-07-25 | active |
| Platane/snk | 6,094 | 2026-04-29 | active |
| antonkomarev/github-profile-views-counter | 5,025 | 2026-01-26 | slowing |
| anmol098/waka-readme-stats | 3,997 | 2026-08-24 | active |
| vn7n24fzkq/github-profile-summary-cards | 3,658 | 2026-09-10 | active |
| gautamkrishnar/blog-post-workflow | 3,445 | 2026-08-10 | active |
| journey-ad/Moe-Counter | 3,081 | 2026-04-16 | active |
| Ashutosh00710/github-readme-activity-graph | 2,339 | 2026-05-17 | active |
| kittinan/spotify-github-profile | 2,227 | 2026-07-21 | active |
| athul/waka-readme | 1,832 | 2026-02-18 | slowing |
| kyechan99/capsule-render | 1,826 | 2026-09-18 | active |
| yoshi389111/github-profile-3d-contrib | 1,750 | 2026-09-13 | active |
| stats-organization/github-stats-extended | 1,318 | 2026-09-21 | active |
| rishavanand/github-profilinator | 1,230 | 2025-04-08 | archived |

The tail includes dormant and archived casualties that profiles still embed: `arturssmirnovs/github-profile-readme-generator` (dormant since 2023-11), `khalby786/REHeader` (dormant, 2020-10), `ankurparihar/readme-pagespeed-insights` (dormant, 2022-04), `omidnikrah/github-readme-stackoverflow` (dormant, 2024-02), `soroushchehresa/github-readme-linkedin` (dormant, 2024-07), `gazf/github-readme-twitter` (archived, 2023-03), `DenverCoder1/github-readme-youtube-stats` (archived, 2021-06), `maddhruv/github-readme-npm-downloads` (archived, 2024-06). A long tail of tiny active tools is also there — `dahan8473/snake-and-commits`, `prsdx/YourTomo`, `egorthinks/git-bonsai`, `flycran/github-gravity`, `0xharkirat/dither-portrait`, `starlash7/github-candles`, `dvigo/github-stats`, `icortesb/vinilo` — the 2026 generation of one-off generators, most with under 30 stars.

---

## The pattern across all fifteen shortlisted profiles

From SHORTLIST.md, verbatim in substance: **the most visually ambitious profiles are the least readable on a phone.** Of the fifteen, **thirteen** have at least one card whose largest text renders under 11px in the 309px mobile column — most of them several. The other two can't be scored: ayxn07 outlines its text into paths, and marcizhu's board has no text. They are designed as desktop web pages and scaled down whole. The ones that hold up on a phone do so for one of two reasons: display type big enough to survive the shrink (**ayxn07**), or real markdown text doing the reading instead of SVG (**JGit705**'s About section, **codeSTACKr**, **10ishk**'s `<details>`).

That gap — ambitious *and* legible at 309px — is empty. Nobody in the survey occupies it convincingly.

### At a glance

| Profile | Archetype | Idea to take | Phone |
|---|---|---|---|
| [ayxn07](https://github.com/ayxn07) | Editorial brutalist | One visual system, top to bottom | Display type survives; body copy doesn't |
| [ashfordeOU](https://github.com/ashfordeOU) | Luxury brand | Serif type in a sea of monospace | 11 of 21 cards illegible |
| [JGit705](https://github.com/JGit705) | Domain storytelling | Visuals drawn from the actual work | 7 of 11 cards illegible; markdown reads fine |
| [JConfessor](https://github.com/JConfessor) | Domain storytelling | A chart from the job itself | 8 of 12 illegible |
| [SergiGTAr](https://github.com/SergiGTAr) | Sci-fi HUD | Discipline inside a loud aesthetic | 6 of 7 illegible |
| [brandon-fryslie](https://github.com/brandon-fryslie) | Format concept | The profile as a daily edition | 4 of 7 illegible |
| [marcizhu](https://github.com/marcizhu) | Interactive | A game played through Issues | Board table scrolls sideways |
| [10ishk](https://github.com/10ishk) | IDE concept | SVG for polish, `<details>` for depth | 3 of 3 illegible; details read fine |
| [SimarBhatiaSB7](https://github.com/SimarBhatiaSB7) | Restrained typographic | Scale contrast, one accent | 5 of 6 illegible |
| [adamalston](https://github.com/adamalston) | One object | The whole README is a single SVG | Graphic reads; labels are texture |
| [XxMasterepicxX](https://github.com/XxMasterepicxX) | Ornamental | Illustration instead of UI | 16 of 21 illegible |
| [Dhyanesh006](https://github.com/Dhyanesh006) | Terminal, total commitment | Self-generated stats, no services | 18 of 28 illegible |
| [getaudra](https://github.com/getaudra) | Command centre | Honest labels on the data | 7 of 8 illegible |
| [sepahead](https://github.com/sepahead) | Data narrative | A graph of how the projects relate | 28 of 33 illegible |
| [atikulmunna](https://github.com/atikulmunna) | Monochrome arcade | Game animation as the banner | 10 of 14 illegible |

Rating key used below: **How good** is scored out of 5 from measured evidence only — the shortlist ranker's score where the profile appears in `data/shortlist_candidates.json`, bespoke SVG/animation counts, zero-broken-image record, theme switching, and the measured phone-legibility counts from `PROFILES.md` (illegible cards / cards measured, smallest text in px). Ambition without legibility, and legibility without ambition, both cost points; that trade-off is the survey's headline.

---

## The fifteen, profile by profile

### Editorial and brand

#### [ayxn07](https://github.com/ayxn07) — Editorial brutalist — **4.5/5**

**What it is:** the most complete visual system in the survey. Teal and black, huge condensed display type, numbered sections (`01 WHOAMI`, `02 PROJECTS`, `03 STACK`) with a nav row, project cards carrying live-status tags. It reads as a designed editorial site rather than a GitHub profile.

**Measured:** 33 images, **31 bespoke SVGs, 23 animated**, all committed (33/0/0 own/upload/third-party), snk contribution snake, theme switching *none*, 0 broken, 1 workflow. Shortlist score **34** (tied highest in the candidate file); techniques: clip-path, css-keyframes, embedded-svg, stroke-draw. Phone: text outlined into paths, so illegibility **can't be read from source** (min px `—`); looking at it, the display type is big enough to survive 309px while small body copy turns to specks.

**How good:** the ceiling of the survey for visual systems, docked half a point only because its display-type solution doesn't extend to body copy and it ships no dark/light switching. Take: **make display type big enough to carry the message alone on a phone.**

#### [ashfordeOU](https://github.com/ashfordeOU) — Luxury brand — **4/5**

**What it is:** a serif wordmark with an orbital emblem, *"For the missions that cannot fail"* in italic serif, and a navy-and-gold palette carried all the way to a gold contribution heatmap. Serif type is almost absent from developer profiles, which is exactly why it reads as premium. Embeds its font in the SVG so it renders everywhere.

**Measured:** 21 images, **21 bespoke SVGs (12 animated)**, all committed, 0 broken, theme `picture`, 1 workflow. Shortlist score **33**. Phone: **11 of 21 cards illegible**, smallest text **3.1px**.

**How good:** a rare aesthetic carried with discipline and a 0-broken record; loses points for half the page dying at 309px. Take: **the rare choice is the memorable one; carry one palette into every panel, including the data.**

#### [XxMasterepicxX](https://github.com/XxMasterepicxX) — Ornamental — **3.5/5**

**What it is:** a serif name framed in illustrated gold and pink vines. Ornament and illustration instead of dashboard UI; "the only profile in the survey that looks drawn rather than engineered."

**Measured:** 23 images, **21 bespoke SVGs (19 animated)**, 21/0/2 own/third-party, generators: profile views counter + github-readme-streak-stats, theme `picture`, 0 broken. Shortlist score **33**; techniques incl. feDisplacementMap (it was found by that search). Phone: **16 of 21 cards illegible**, min text 3.2px, badge share 0.04.

**How good:** original lane, poor legibility, and it still leans on a streak service. Take: **illustration is an open lane.**

### Storytelling from the work itself

#### [JGit705](https://github.com/JGit705) — Domain storytelling — **4/5**

**What it is:** a mechanical engineer moving into data. The hero is a route map of London; project cards carry small bar charts and radar diagrams. The visuals are specific to what he does, which makes them far more memorable than generic neon. And his About section is plain markdown — on a phone it's the most readable thing on the page.

**Measured:** 16 images, **16 bespoke SVGs (12 animated)**, 12/0/4 own/upload/third-party, shields.io + skill-icons + snk, theme `picture`, 0 broken, 2 workflows. Shortlist score **33**, badge share 0.25. Phone: **7 of 11 cards illegible**, min 2.8px — while the markdown below stays readable.

**How good:** the clearest proof of the survey's prescription (SVG for atmosphere, markdown for reading); measured illegibility still bites the SVG layer. Take: **draw from the real work; let markdown carry the reading.**

#### [JConfessor](https://github.com/JConfessor) — Domain storytelling — **3.5/5**

**What it is:** a data analyst in wind energy. An animated turbine hero, a pipeline diagram ("from raw signal to something someone opens") and a section titled *"The chart I read for a living"* — a turbine power curve. One chart from the actual job says more than a skills grid.

**Measured:** 12 images, **12 bespoke SVGs (3 animated)**, all committed, no generators, theme `picture`, 0 broken. Shortlist score **29** (lowest of the fifteen in the candidate file). Phone: **8 of 12 illegible**, min 2.7px.

**How good:** the idea is exemplary, the execution is measured-illegible and only lightly animated. Take: **show the one artefact that defines the work.**

#### [sepahead](https://github.com/sepahead) — Data narrative — **3.5/5**

**What it is:** a contribution chart plotted as a trajectory, a weekday donut, a repository grid, and a node graph of how his projects connect to each other. A diagram of his own work rather than of his tools.

**Measured:** 66 images (the heaviest of the fifteen), **63 bespoke SVGs (17 animated)**, 44/0/22, devicon only, theme `picture`, 0 broken, **5 workflows**. Shortlist score **33**; badge share 0.33. Phone: **28 of 33 cards illegible** — "also the densest" — min 3.3px. Exemplifies gradient + clip-path technique in `technique_exemplars.json` (`assets/hero-light.svg`).

**How good:** the most information-rich page in the survey and the worst at 309px; that combination is exactly the pattern the survey flags. Take: **map relationships between projects, not proficiency in languages.**

### Systems and HUDs

#### [SergiGTAr](https://github.com/SergiGTAr) — Sci-fi HUD — **4/5**

**What it is:** `SERGIGTAR OS // PUBLIC NODE`. Neon green on black, huge condensed headline, status panels, a command line, bordered CTA buttons. A loud aesthetic held together by strict consistency — every panel uses the same border, type and spacing.

**Measured:** 7 images, **7 bespoke SVGs, all 7 animated**, all committed (7/0/0), no generators, theme `picture`, 0 broken. Shortlist score **33**. Phone: **6 of 7 illegible**, min 3.2px. Its `pipboy-terminal-dark.svg` (60 KB, animated) is an embedded-raster exemplar.

**How good:** small, self-contained, zero breakage, fully animated — loud by choice, systematic in execution; almost unreadable on a phone. Take: **a bold style works when it's systematic.**

#### [getaudra](https://github.com/getaudra) — Command centre — **3.5/5**

**What it is:** `SYSTEMS ONLINE` command centre with a mission pipeline (idea → research → prototype → test → falsify → iterate). Notable for honesty: it states that its language labels "describe observed repository activity groupings, not skill percentages or proficiency claims".

**Measured:** 8 images, **8 bespoke SVGs (5 animated)**, all committed, no generators, theme *none*, 0 broken. Shortlist score **28**. Phone: **7 of 8 illegible**, min 3.8px.

**How good:** the honesty of labelling is the survey's standout idea here, but no theme switching and near-total phone illegibility. Take: **label data for what it is.**

#### [Dhyanesh006](https://github.com/Dhyanesh006) — Terminal, total commitment — **4/5**

**What it is:** a Matrix terminal carried through every section: boot sequence, `cat tech-stack.dat`, stats, activity, trophies. Its README notes the stats are "auto-refreshed daily from the GitHub API… pure SVG + SMIL, no external card services" — deliberately avoiding the third-party generators the survey found dying.

**Measured:** 28 images, **28 bespoke SVGs, all 28 animated**, all committed (28/0/0), **no generators at all**, theme `picture`, 0 broken, 3 workflows. Shortlist score **33**. Phone: **18 of 28 illegible**, min 2.6px. `assets/matrix-banner.svg` (70 KB, animated) is a gradient exemplar.

**How good:** the only profile of the fifteen that fully practices finding 1 (own your data panels) *and* finding 6 (SMIL everywhere); the Matrix styling still shrinks to specks. Take: **generate your own data panels; don't rent them.**

### Concepts and formats

#### [brandon-fryslie](https://github.com/brandon-fryslie) — Format concept — **4/5**

**What it is:** the header is a newspaper masthead dated today, followed by an auto-generated changelog of the last 24 hours and the week, written as real text. The profile as a daily edition — and it openly says it was "hand-crafted by generative AI".

**Measured:** 8 images, **8 bespoke SVGs, all 8 animated**, all committed, no generators, theme *none*, 0 broken, **8 workflows** (the automation behind the daily edition). Shortlist score **32**. Phone: **4 of 7 illegible**, min 2.1px (the worst minimum text among the fifteen — but the changelog itself is markdown).

**How good:** the strongest *concept* in the survey and the content is real text; no theming and the smallest measured type. Take: **a format is a stronger idea than a style.**

#### [marcizhu](https://github.com/marcizhu) — Interactive — **4/5**

**What it is:** the whole README is a playable chess game. Moving means clicking a link that opens a GitHub Issue; an Action plays the move and updates the board. The canonical example of the one real input channel a README has.

**Measured:** **65 images** (second-heaviest of the fifteen), 64/0/1, visitor badge only, 16 SVGs (0 animated — the board is image tiles), theme *none*, 0 broken, 1 workflow. Phone: the board is a table of images, which **scrolls sideways** rather than shrinking (`sideways=table`); no text cards to score (min px `—`).

**How good:** unique interactivity, honest about its plainness; no theme, table layout breaks the phone. Take: **Issues are the interaction layer.**

#### [atikulmunna](https://github.com/atikulmunna) — Monochrome arcade — **3.5/5**

**What it is:** black and white throughout; the banner is an animated side-scrolling game, the contribution graph an invaders-style animation. Game motion used as identity, in a disciplined monochrome.

**Measured:** 15 images, **14 bespoke SVGs, all 14 animated**, all committed, no generators, theme *none*, 0 broken, 1 workflow. Shortlist score **28**. Phone: **10 of 14 illegible**, min **2.2px**.

**How good:** total commitment to one idea with zero breakage; monochrome discipline lets motion carry it, but no theme and severe phone shrink. Take: **restraint in colour lets motion carry personality.**

### Restraint

#### [SimarBhatiaSB7](https://github.com/SimarBhatiaSB7) — Restrained typographic — **3.5/5**

**What it is:** a huge bold name, one red accent, monospace metadata rows, numbered sections. The clearest example of Swiss-style typographic hierarchy — but also a member of the shared "Index Nº 001" template family (see below), which costs it originality.

**Measured:** 7 images, **6 bespoke SVGs (6 animated)**, all committed, snk contribution snake, theme `picture`, 0 broken. Shortlist score **33**. Phone: **5 of 6 illegible**, min 3.4px.

**How good:** the design lesson is clean and real; provenance as one of four near-identical layouts caps the score. Take: **scale contrast and one accent colour are enough.**

#### [adamalston](https://github.com/adamalston) — One object — **4/5**

**What it is:** the entire README is one orbital "observatory" SVG, with separate dark and light versions served through `<picture>`. Its HUD labels render at 3px on a phone — but they're texture; the orbit graphic is the message and reads fine.

**Measured:** **1 image** (the whole profile), 0/0/1 (served from a third-party-free single asset), no generators, theme **`picture`**, 0 broken, no workflows. Phone: **1 card, illegible (min 3.0px)** — yet the survey explicitly reads its tiny labels as texture rather than failure.

**How good:** the purest answer to "one strong object"; correct theming, one illegible card that doesn't matter. Take: **one strong object can be the whole profile.**

#### [10ishk](https://github.com/10ishk) — IDE concept — **4/5**

**What it is:** a code-editor hero, an orbital skill diagram and a terminal project list, then native markdown `<details>` for each project's specifics. SVG for polish, markdown for depth and real text.

**Measured:** 7 images, **6–7 bespoke SVGs (all animated)**, all committed, snk contribution snake, theme `picture`, 0 broken, 1 workflow. Shortlist score **33** (tied third). Techniques: blur-glow, filter, gradient, mask, smil, stroke-draw. Phone: **3 of 3 illegible**, min **2.6px** — but the `<details>` markdown reads fine.

**How good:** the split the survey recommends (SVG polish + markdown depth), executed deliberately; every SVG card still fails 309px. Take: **split the work between SVG and markdown on purpose.**

---

## A template family

**umang-eng**, **harkirat-data**, **SimarBhatiaSB7** and **aniketpitre** share one layout — a `PORTFOLIO — INDEX Nº 001` header, numbered sections, `FIG.` captions. umang-eng and harkirat-data carry all four markers checked in their SVG source (`INDEX Nº`, `~/01-whoami`, `FIG. 0`, `DATA IN MOTION`); the other two share the header. The text is personalised, so byte-hashing can't catch it — it took looking at them side by side, then confirming in source. Listed once, via SimarBhatiaSB7, rather than as four originals.

Measured (`PROFILES.md`):

| Profile | img | own/up/3rd | svg (anim) | theme | illeg | min px |
|---|--:|---|---|---|--:|--:|
| [umang-eng](https://github.com/umang-eng) | 21 | 16/0/5 | 21 (16) | picture | 8 | 2.6 |
| [harkirat-data](https://github.com/harkirat-data) | 17 | 16/0/1 | 16 (16) | picture | 8 | 2.6 |
| [aniketpitre](https://github.com/aniketpitre) | 11 | 7/1/3 | 10 (7) | picture | 6 | 3.1 |
| SimarBhatiaSB7 | 7 | 7/0/0 | 6 (6) | picture | 5 | 3.4 |

---

## Worth studying for one idea

Five more, each carried by a single idea (from SHORTLIST.md):

#### [erogluyusuf](https://github.com/erogluyusuf) — **3/5**

**What it is:** skill icons laid out as a keyboard, a committed PNG (`key.png`). A genuinely unexpected metaphor. The rest of the page is a pacman contribution graph (an Action's output) and repo cards from a card service he built himself on a free Vercel deployment.

**Measured:** 16 images, 4/0/12, github-readme-activity-graph (the 2%-live service), 12 bespoke SVGs (12 animated), theme `picture`, **1 broken image**, 6 workflows, phone **12 cards illegible**, min 2.6px. Shortlist score **33**.

**How good:** the keyboard idea alone earns the mention; the surrounding execution demonstrates findings 1 and 2 simultaneously (dead service + phone-illegible cards). Take: **the keyboard metaphor.**

#### [codeSTACKr](https://github.com/codeSTACKr) — **3.5/5**

**What it is:** auto-updated lists of latest videos and blog posts as plain text. Unglamorous, and legible on every screen. "It still embeds the dead github-readme-stats public instance."

**Measured:** 33 images, 13/2/18, devicon + shields.io + GitHub upload, 30 SVGs (**0 animated**), theme `fragment` (`#gh-dark-mode-only`), **1 broken**, 3 workflows, no scored illegible cards (min `—`). Category: GitHub Actions.

**How good:** legibility on every screen and working theme fragments — and a live demonstration of the dead-stats finding sitting inside a shortlisted profile. Take: **plain auto-updated text wins screens.**

#### [BrunnerLivio](https://github.com/BrunnerLivio) — **3/5**

**What it is:** ironic 90s GeoCities: WordArt title, spinning globe, and a guestbook that works through Issues.

**Measured:** 14 images, 9/0/5, GitHub avatars, 3 SVGs (3 animated), theme *none*, 0 broken, 1 workflow, phone **1 illegible card**, min 6.2px (the most legible minimum among all mentioned profiles), `sideways=table`. Category: Retro.

**How good:** the joke lands and the type is comparatively large; no theme and a sideways-scrolling table. Take: **a guestbook through Issues.**

#### [nihalsheikh](https://github.com/nihalsheikh) — **3.5/5**

**What it is:** a glassy dashboard card done with real polish; the conventional idea at its best.

**Measured:** 7 images, **7 bespoke SVGs (all animated)**, all committed, no generators, theme *none*, 0 broken, 1 workflow. Shortlist score **34** (tied highest in the candidate file) with techniques clip-path, css-keyframes, embedded-raster, embedded-svg, gradient, mask, smil. Phone: no measured illegible cards (min `—`).

**How good:** highest ranker score, small and flawless — but conventional and without theme switching, which is why it's "one idea" rather than one of the fifteen. Take: **glassy card polish done properly.**

#### [JackLuciano](https://github.com/JackLuciano) — **3.5/5**

**What it is:** one warm orange accent held across a pipeline diagram, telemetry grid, heatmap and 3D contribution graph.

**Measured:** 38 images, 27/0/11, shields.io + profile views counter + skill-icons, **38 bespoke SVGs (27 animated)**, theme `picture`, 0 broken, 2 workflows, phone **17 cards illegible**, min 2.7px, badge share 0.29. Shortlist score **33**.

**How good:** colour discipline plus massive custom-SVG volume; still a wall of tiny text on a phone and three third-party services. Take: **one accent across every panel.**

---

## What none of them do

- **Stay readable at 309px while being ambitious.** The gap noted at the top.
- **Treat dark and light as equal citizens.** Five of the fifteen have no theme switching at all. The rest were reviewed in dark mode only; whether their light versions hold up is a Phase 3 question, not yet answered.
- **Use motion sparingly.** Animation is everywhere; almost nothing settles.
- **Combine real interactivity with high design.** marcizhu is interactive but plain; the beautiful profiles are static.

---

## One-line statistics index (all verbatim from the survey)

- 446 profiles (187 curated / 259 search) · 487 candidates · 38 orgs · 2 gone · 1 no README
- 10,782 images · 8,589 distinct URLs · 2,689 committed / 7,934 third-party / 159 GitHub uploads
- 442 profiles measured at phone width · 441 at desktop · 98% render match
- 41% of profiles show a broken image (39% curated / 44% search) · 490 broken occurrences · 185 profiles affected
- 309 broken image URLs from Vercel `DEPLOYMENT_PAUSED` (215) + `DEPLOYMENT_DISABLED` (94)
- public github-readme-stats instance loads **0%** · still embedded by **24%** of profiles
- 309px phone column · 846px desktop column · 11px legibility floor
- **55% of 1,730 cards** phone-illegible · 90% phone-caused · 15% curated / 70% search profiles affected
- desktop: 15% of profiles have an illegible card (3% curated / 23% search)
- hand-made cards fail **63%** vs service cards **37%**
- 21% use image tables · 9% crushed in table · 7% table scrolls sideways · 0% page scrolls sideways
- 20% dark/light switching (5% curated / 30% search) · `<picture>` 80 vs fragment 7 · 35 profiles with in-SVG `prefers-color-scheme`
- 42% badge walls (40% curated / 43% search)
- 54% run Actions workflows (41% / 63%) · median push age 1.1 months
- 6,844 distinct SVGs, 1,472 animated · 1,506 bespoke (842 animated) · 192 generated · 29 copied
- 65 tool repositories: 38 active, 11 slowing, 12 dormant, 4 archived
- 20 shortlisted and screenshotted · 15 exceptional + 5 one-idea profiles
- 13 of the 15 have a card under 11px at 309px; 2 unscorable (ayxn07, marcizhu)
