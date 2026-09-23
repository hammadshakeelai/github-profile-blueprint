# What renders, tested in three engines

Generated from real captures, not documentation. Each cell was checked by
loading a gallery of examples **inside GitHub's own rendered page** in Chromium
153, Firefox 155 and WebKit 26.6 (Safari's engine), at 1280px and 390px, in dark
and light, and scoring it by frame-differencing eight frames 0.73s apart. Source:
[`docs/CAPABILITY-MATRIX.md`](../../../docs/CAPABILITY-MATRIX.md).

Anything not measured is tagged **UNVERIFIED** and should be stated that way.

## Animation

**All fifteen techniques animate in all three engines, with one exception.**
SMIL, CSS `@keyframes`, stroke-dash drawing, masks, `animateMotion`, typing,
`textPath`, gauges, bar charts, glow, grain, particles, terminal simulation —
each confirmed moving, not assumed.

> **WebKit never animates `gradientTransform`.** The only engine difference
> found. Animate the gradient's `x1`/`x2` or its stop offsets instead; both were
> verified animating everywhere.

## Theme switching — all three mechanisms work

| Mechanism | Result |
|---|---|
| `<picture>` + `prefers-color-scheme` | works in all three |
| `#gh-dark-mode-only` / `#gh-light-mode-only` fragments | works in all three |
| `@media (prefers-color-scheme)` **inside** the SVG | works in all three |

In-SVG media queries are *not* blocked — an earlier version of this skill said
they were, and the capture disproves it. The real caveat is different: all three
mechanisms key off `prefers-color-scheme`, which follows the viewer's operating
system, not their GitHub theme setting. Someone running a light OS with GitHub
set to dark sees the light asset on a dark page. Nothing can read GitHub's own
theme from inside an image.

Prefer `<picture>` anyway: it is what the survey's profiles use (80 to 7), and
one theme per file is easier to verify than one file with two states.

## Media-gated `<picture>` sources

GitHub's sanitizer keeps the `media` attribute, and the host page evaluates it,
so a `<source>` can select a file by **viewport width** as well as by theme —
verified serving a phone-specific SVG at 390px and a desktop one at 1280px in
all three engines (`docs/research/WIDTH-GATED.md`). Combined with theme and
reduced motion, the first matching source wins, so order most-specific first.

## Reduced motion

`@media (prefers-reduced-motion: reduce)` **never applies inside an SVG
referenced as an image** — Chromium, Firefox and WebKit alike. It is dead code,
and 369 files across 26 surveyed profiles contain it. `prefers-color-scheme`
applies in exactly the same position, which is what makes the mistake so easy.

What works is gating a `<picture>` source, which the host page evaluates and
GitHub's sanitizer preserves:

```html
<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset=".../banner-still.svg">
  <img src=".../banner.svg" alt="…" width="600">
</picture>
```

Verified serving the still file in all three engines. Full method:
[`docs/research/REDUCED-MOTION.md`](../../../docs/research/REDUCED-MOTION.md).

## Blocked, and how the failure looks

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| `<script>` inside the SVG | blocked | blocked | blocked |
| `@import`ed web font | blocked | blocked | blocked |
| External `<image>` href | blocked — **draws a broken-image icon** | blocked — draws nothing | inconsistent |
| HTML in `<foreignObject>` | renders | renders | inconsistent |

A blocked external image does not fail quietly in Chrome; it paints a
broken-image icon into your design. This also caught out the survey tooling
once, which read the icon as a successful load.

Referencing an SVG through `<img>` puts the browser in the SVG spec's **secure
animated mode**: declarative animation runs, scripts and interaction do not.
That is browser behaviour, not a GitHub policy, which is why it is identical in
all three engines.

## Widths, measured from the live DOM

| Viewport | README column |
|---|---|
| 1920px desktop | **846px** |
| 1280px laptop | **831px** |
| 390px phone | **309px** |

Images are hard-capped to the column: an 854px-natural image renders at 846px.
309px is the number that kills banners.

## How long an update takes to appear

Push a committed SVG, then poll until the new bytes are served:

| | Branch URL (what a README uses) | Commit-pinned URL |
|---|---|---|
| Round 1 | 302.2s | 5.9s |
| Round 2 | 303.2s | 4.8s |

`Cache-Control: max-age=300`. **Wait five minutes before judging a change**, or
you will debug a design problem that is really a cache. A commit-pinned URL is
fresh in seconds but has to be rewritten into the README on every update.

## Asset routing

- **Repo-relative** (`./assets/banner.svg`) → rewritten to
  `github.com/{owner}/{repo}/raw/{branch}/{path}`, **not** Camo-proxied,
  `max-age=300`.
- **Third-party** → proxied through `camo.githubusercontent.com` under an
  HMAC-SHA1 digest, cached hard. You cannot hand-construct or warm a Camo URL.

- **Relative paths inside `<picture><source srcset>` resolve correctly on
  profile pages.** Earlier research claimed they fail; 33 live profiles that use
  them were loaded and 33 served the declared file
  (`docs/research/RELATIVE-SRCSET.md`). Absolute `raw.githubusercontent.com`
  URLs are still the better default — identical in every context, and portable
  if the markdown is viewed elsewhere — but a relative path is not a bug.
- Set the `<img>` fallback to the variant you would rather have seen, and make
  sure that file exists: it is what any client ignoring `<source>` will fetch. A
  surveyed profile pointed its fallback at a light file and served it, broken,
  on a dark page.

## Not testable from a desktop — check by hand

iOS Safari and the GitHub mobile apps cannot be driven headlessly. The gallery
is built so each answer is readable by eye; the checklist is at the end of
`docs/CAPABILITY-MATRIX.md`. Until someone runs it, those cells stay
**unverified** — say so rather than extrapolating from WebKit.
