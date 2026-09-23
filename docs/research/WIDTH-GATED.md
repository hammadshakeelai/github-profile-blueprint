# Track 6 · Width-gated `<picture>` sources

**They work — in Chromium, Firefox and WebKit, on GitHub's rendered page.** A
README can serve a different SVG to a phone than to a desktop, which means the
survey's largest finding stops being a trade-off and becomes a choice.

## Why this matters

The survey's headline: **55% of 1,730 SVG cards have their largest text under
11px on a phone, and 90% of those are perfectly legible at full size.** They
fail only because a 900- or 1200-unit canvas is squeezed into a 309px column.

Until now the advice was to pick a side: design small enough for the phone and
accept a modest desktop canvas, or accept illegibility on mobile. That is what
`docs/DIRECTION.md` decided by capping the profile's viewBox at 600 units.

With a width-gated source there is no compromise to make:

```html
<picture>
  <source media="(max-width: 600px)" srcset=".../card-phone.svg">
  <img src=".../card.svg" alt="…" width="900">
</picture>
```

The same card, drawn twice: 900 units for the desktop column, 309 units for the
phone, where a 13-unit label renders at exactly 13px.

| | 900-unit canvas | 309-unit canvas |
|---|---|---|
| 26-unit body text at 309px | **8.9px** — illegible | — |
| 13-unit body text at 309px | — | **13px** — comfortable |

## The measurement

Fixture: [width-gallery.md](width-gallery.md), one `<picture>` with a
`(max-width: 600px)` source. Loaded on github.com in each engine at both widths,
reading which file was actually served:

| | 1280px | 390px |
|---|---|---|
| Chromium 153 | `w-desktop.svg` | **`w-phone.svg`** |
| Firefox 155 | `w-desktop.svg` | **`w-phone.svg`** |
| WebKit 26.6 | `w-desktop.svg` | **`w-phone.svg`** |

Measured container: 861px at 1280, 324px at 390 (a repo blob page; a profile
page's column is 309px). The query is on the **viewport**, not the container, so
a 600px breakpoint sits comfortably between the two.

The survey had already seen this mechanism in the wild — Xalzeroph and SirAllap
ship `-mobile-` and `-m-` variants behind `max-width` sources — and Track 1 saw
those sources correctly *not* apply at desktop width. This closes the other half:
they do apply on a phone.

## What it costs

- **File count multiplies.** Width × theme is four files per card; adding the
  reduced-motion variant from Track 2 makes eight. Generate them, never hand-
  maintain them — one content source, one script.
- **Source order is significant.** The first matching `<source>` wins, so the
  most specific combinations go first:

```html
<source media="(max-width: 600px) and (prefers-color-scheme: dark)"  srcset=".../card-phone-dark.svg">
<source media="(max-width: 600px)"                                   srcset=".../card-phone-light.svg">
<source media="(prefers-color-scheme: dark)"                         srcset=".../card-dark.svg">
<img src=".../card-light.svg" alt="…" width="900">
```

- **The `<img>` fallback is what a non-`<picture>` renderer gets** — the GitHub
  mobile apps' native views among them (still unverified, Track 5). If the
  fallback is the wide desktop file, those readers get the illegible one. Two
  defensible choices: make the fallback the phone variant and let desktop
  readers see a small card, or keep the desktop file and accept the risk. There
  is no option that is right everywhere.
- **It is still two drawings.** Not a scale factor — a phone canvas wants fewer
  words, not the same words smaller. Treating it as "export at another size"
  reproduces the original problem.

## What this does not change

The legibility floor still governs each variant: a 309-unit canvas with 8-unit
text fails exactly as before. And markdown still beats both — real text reflows,
is searchable, and reaches a screen reader. This widens what an SVG can do
safely; it doesn't make SVG the right place for prose.

## The profile built in Phase 5

It doesn't need this: a 600-unit canvas clears the floor at 309px with 11.9px to
spare, and one file per theme is easier to verify. The option is now documented
for a design that wants a larger desktop canvas than 600 units — which the
`DIRECTION.md` trade-off previously ruled out on evidence that has now moved.
