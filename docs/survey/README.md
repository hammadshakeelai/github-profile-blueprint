# Survey — Phase 1

A library of real GitHub profile READMEs and the generators they depend on,
built from evidence rather than general knowledge. Every row is filled by
fetching the actual README and the actual images it references.

## Method

`tools/survey/harvest.py` collects; `tools/survey/analyze.py` turns the raw data
into the tables here. Both are re-runnable, so the survey can be refreshed as
profiles change or die.

1. **Candidates** come from curated sources (see *Sources*), each tagged with
   where it was found and the curator's category.
2. For each candidate, the GitHub API supplies the profile repo's metadata, its
   README source, and whether it has workflows.
3. Every image the README references — markdown `![]()`, `<img src>`, and
   `<picture><source srcset>` — is resolved to an absolute URL and fetched.
4. SVG responses are parsed for technique markers and for the legibility maths
   in `skills/github-profile-readme/references/measured-constraints.md`.

Nothing here is copied from the READMEs themselves: the repo stores links and
derived measurements, not other people's content.

## Row schema — profiles

| Field | Meaning |
|---|---|
| `user` | GitHub username; the profile lives at `github.com/<user>` |
| `source`, `category` | Where it was found, and the curator's tag |
| `status` | `live`, `missing` (repo gone or renamed), or `no-readme` |
| `pushed_at` | Last push to the profile repo — staleness signal |
| `images` | Total images referenced |
| `repo_assets` | Images committed to the profile repo itself |
| `third_party` | Images served by an external host |
| `generators` | Named generators identified from image URLs |
| `svgs`, `animated_svgs` | SVG images, and how many contain SMIL or CSS animation |
| `techniques` | SVG features found: filter, mask, clipPath, gradient, stroke-dash draw, embedded font, embedded raster, theme-aware SVG |
| `theme_switch` | `picture` (`<picture>` + `prefers-color-scheme`), `fragment` (`#gh-dark-mode-only`), or `none` |
| `gifs` | Animated GIF count |
| `broken` | Images that did not return a usable image — the *still live* test |
| `workflows` | Number of Actions workflows; non-zero suggests generated content |
| `mobile_worst_px` | Smallest text in any SVG, in px, once scaled into a 309px phone container |

A row is complete when every field is filled from fetched data. `notes` —
the qualitative "what's notable" — is written only for the shortlist, after
the profile has actually been looked at.

## Row schema — generators

| Field | Meaning |
|---|---|
| `generator` | Name, and the repository that builds it |
| `profiles` | How many surveyed profiles use it |
| `requests`, `ok` | Image requests made, and how many returned a usable image |
| `error_cards` | 200 responses whose body is an error message ("rate limit", "something went wrong") |
| `median_ms` | Median response time |
| `mobile_worst_px` | Median smallest-text size at 309px across its cards |

## Sources

| Source | Why |
|---|---|
| `abhisheknaiidu/awesome-github-profile-readme` | Canonical curated list, 31k stars, ~190 profiles across 16 categories |
| Its `## Tools` section | Seed list of generators |

Further sources are added here as they are harvested, each with the same
treatment.

## Outputs

- `PROFILES.md` — every surveyed profile, one row each
- `GENERATORS.md` — every generator seen, ranked by use, with liveness
- `FINDINGS.md` — what the data says, each claim tied to the numbers
- `data/` — the raw derived JSON the tables are built from
