# Survey — Phase 1

A library of real GitHub profile READMEs and the generators they depend on,
built from evidence rather than general knowledge. Every row is filled by
fetching the actual README and every image it references, and phone behaviour
is measured from real rendered layout.

**446 personal profiles · 10,782 images fetched · layout measured for 442 at
phone and 441 at desktop width · 65 tool repositories health-checked · 20
shortlisted and screenshotted.**

## Read these

| File | What it is |
|---|---|
| [FINDINGS.md](FINDINGS.md) | What the data says, each claim tied to its numbers — start here |
| [SHORTLIST.md](SHORTLIST.md) | The fifteen exceptional profiles, plus five for one idea each |
| [GENERATORS.md](GENERATORS.md) | Every image service seen, ranked by use, with liveness and phone legibility |
| [TOOLS.md](TOOLS.md) | The repositories behind them, and whether anyone maintains them |
| [PROFILES.md](PROFILES.md) | All 446 profiles, one row each |
| `shots/` | Shortlisted profiles at 390px (phone) and 1280px (desktop) |
| `data/` | The derived JSON every table is built from |

## Sources

| Source | Cohort | Why |
|---|---|---|
| `abhisheknaiidu/awesome-github-profile-readme` (31k★) | curated · 187 | The canonical curated list; shows what's popular and copied |
| GitHub code search for `animateMotion`, `animateTransform`, `stroke-dashoffset`, `keyframes`, `feGaussianBlur`, `feTurbulence`, `feDisplacementMap`, `textPath`, `prefers-color-scheme` in committed `.svg` files, kept only in `username/username` repos owned by a person | search · 259 | Finds the ambitious — people hand-making SVGs — rather than the popular |
| The awesome list's `## Tools` section, plus the major generators observed | — | Seed list for `TOOLS.md` |

The cohorts are reported separately throughout. The search cohort was selected
for hand-made SVGs, so its custom-SVG rates are high by construction; its other
rates are comparable.

## Method

All of it re-runs from `tools/survey/`:

| Step | Script | Does |
|---|---|---|
| 1 | `source_codesearch.py` | Technique-first candidate discovery via code search |
| 2 | `harvest.py` | Fetches each profile's README via the API, resolves and fetches every image, derives SVG metrics |
| 3 | `layout.py` | Loads each live profile in headless Chrome at 390px and 1280px and records every image's rendered box |
| 4 | `analyze.py` | Builds `PROFILES.md`, `GENERATORS.md`, `summary.json` |
| 5 | `tools_health.py` | Maintenance status of the tool repositories → `TOOLS.md` |
| 6 | `shortlist.py` | Ranks candidates worth looking at (a pre-filter, not the judgement) |
| 7 | `screenshot.py`, `contact_sheet.py` | Captures and tiles pages for visual review |

Nothing copied from the READMEs themselves is stored: the repo keeps links and
derived measurements. README text and image bodies live in a gitignored cache
(`.cache/survey/`). The GitHub token is sent to `api.github.com` only; SVGs from
third-party hosts are treated as untrusted and refused if they declare a DTD or
entities.

Several first-pass readings were wrong and were corrected before any finding was
written — the full list is at the end of [FINDINGS.md](FINDINGS.md).

## Row schema — profiles

| Field | Meaning |
|---|---|
| `user`, `cohort`, `category` | Profile, which population it's in, and where it was found |
| `status` | `live`, `org` (an organisation, excluded), `missing`, or `no-readme` |
| `images` | Images displayed (theme variants in `<picture>` not double-counted) |
| `committed` / `gh_upload` / `third_party` | Where each image is served from |
| `generators` | Named services and tools identified from image URLs |
| `custom_svgs`, `custom_animated` | Bespoke SVGs — in the user's own repos, not a known tool's output, not copied |
| `generated_svgs`, `copied_svgs` | Committed outputs of known Actions; byte-identical copies of someone else's SVG |
| `techniques` | Features found in the bespoke SVGs |
| `theme_switch` | `picture`, `fragment` (`#gh-dark-mode-only`), or `none` |
| `broken` | Images that did not return a usable image after two attempts |
| `workflows` | Actions workflows in the profile repo |
| `m_text_cards`, `m_illegible_cards` | SVG cards (badges excluded) measured on the phone, and how many have their largest text under 11px |
| `m_illegible_phone_caused` / `m_illegible_everywhere` | Of those: legible at native size but shrunk by the phone, vs too small on any device |
| `tables_scrolling_with_images`, `crushed_in_table` | Phone table behaviour, measured |
