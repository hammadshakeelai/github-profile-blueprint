# What 446 real profiles actually do

Every number here comes from the survey in
[`docs/survey/FINDINGS.md`](../../../docs/survey/FINDINGS.md): 446 personal
profile READMEs (187 from `awesome-github-profile-readme`, 259 found by code
search for SVG animation primitives in `username/username` repos), 10,782 images
fetched, 442 profiles loaded in headless Chrome to measure real layout. Tables:
`docs/survey/PROFILES.md`, `GENERATORS.md`, `TOOLS.md`.

Cite this file rather than intuition. If a claim isn't here or in
[platform-facts.md](platform-facts.md), it isn't established.

## The four failures that matter

| Failure | Rate |
|---|---|
| Profile shows at least one broken image | **41%** |
| SVG cards whose *largest* text is under 11px on a phone | **55%** of 1,730 |
| Profiles that are more than half badges and icons | **42%** |
| Profiles that switch between dark and light | only **20%** |

### 1 · Rented images die

309 broken URLs are free-tier Vercel deployments switched off
(`DEPLOYMENT_PAUSED` / `DEPLOYMENT_DISABLED` in the response headers).

| Service | Profiles | Images that load |
|---|--:|--:|
| github-readme-stats — public instance | 107 | **0%** |
| github-readme-activity-graph | 57 | **2%** |
| github-profile-trophy | 36 | **11%** |
| visitor badges | 42 | 59% |
| github-readme-streak-stats | 95 | 97% |
| readme-typing-svg | 87 | 100% |
| komarev profile views | 103 | 100% |
| shields.io | 239 | 100% |

24% of profiles still embed the dead github-readme-stats instance. Its
repository metadata says active; its README says unmaintained; the service
returns 503. **Only fetching the image tells the truth.**

Images committed to the profile repo loaded **99%** of the time. That is the
argument for generate-and-commit over embed-a-service, and it is the single
highest-value rule in this skill.

### 2 · The phone, not the design, is what makes text illegible

90% of illegible cards are legible at their native width and fail only after
shrinking into the 309px column. 10% are too small on any device.

- This is now avoidable without compromise: a `<source media="(max-width:
  600px)">` can serve a phone-scale drawing, verified in three engines
  (`docs/research/WIDTH-GATED.md`).
- Hand-made cards fail **more** than generator output: **63% vs 37%**. People
  drawing their own panels choose wide canvases with small type.
- By service: lowlighter/metrics 83%, github-profile-summary-cards 60%,
  readme-typing-svg 54%, self-hosted github-readme-stats 20%.
- shields.io's 53% is by design — `for-the-badge` sets 10px text on every
  device, phone or not.
- Desktop is better but not immune: 15% of profiles have an illegible card at
  1280px, mostly panels drawn wider than the 846px column.

### 3 · Tables do something worse than shrinking

21% of profiles put two or more images in a table. On a phone GitHub either
**squeezes the cards** — 640px cards measured at **76px** in a four-column table
(9% of profiles) — or **keeps them full width and scrolls the table sideways**
(7%). The page itself never scrolls sideways; GitHub contains the overflow. Both
outcomes are worse than one column, so don't lay out with tables.

### 4 · What hand-made SVGs are built from

Counted per profile, so one profile with forty files can't outvote forty with
one:

| Technique | Profiles |
|---|--:|
| Gradients | 130 |
| SMIL (`<animate>`, `animateMotion`) | 129 |
| Filters | 102 |
| CSS `@keyframes` | 101 |
| Stroke-dash line drawing | 93 |
| Blur / glow | 90 |
| Clip paths | 90 |
| `prefers-color-scheme` inside the SVG | 35 |
| `<foreignObject>` | 32 |
| Masks | 28 |
| Base64-embedded fonts | 13 |
| Text on a path | 12 |

SMIL beats CSS keyframes in hand-made work. Every one of these is rebuilt as a
minimal working example in
[`docs/techniques/CATALOGUE.md`](../../../docs/techniques/CATALOGUE.md).

### 5 · A third of content images can't be reached at all

Re-parsed from the live READMEs (`docs/research/ALT-TEXT.md`):

| Class | Non-badge images | Text-bearing cards |
|---|--:|--:|
| no `alt` attribute | 34.2% | 30.3% |
| `alt=""` | 9.9% | 7.5% |
| the filename, or a word like "banner" | 8.0% | 5.0% |
| anything actually written | 48.0% | 57.2% |

"Anything actually written" is a ceiling, not a score — the classifier only
rejects obvious junk. 61 profiles describe none of their images. The hand-made
cohort does better (57.5% vs 31.1%), the reverse of the legibility split.

### 6 · "Custom" is often generated or templated

Of 1,506 bespoke SVGs, 192 are Action output identifiable by signatures the
generators leave behind (`<desc>Generated with …`, `id="metrics-end"`,
`data-testid="card-title"`). Byte-identical copying is rare (29 files), but
**structural templates are not** — four profiles share one "Index Nº 001"
layout with personalised text. Hashing can't see that; looking can.

### 7 · A recent push means nothing

54% of profiles run Actions, many committing on a schedule. The median profile
was "last pushed" 1.1 months ago while its human content is years old.

## The gap worth aiming at

Nobody in the 446 is both visually ambitious **and** legible at 309px. The
ambitious ones fail the phone; the legible ones are plain markdown. That space
is empty, and it is where a profile should be designed.

The fifteen standouts and what to take from each:
[`docs/survey/SHORTLIST.md`](../../../docs/survey/SHORTLIST.md).
