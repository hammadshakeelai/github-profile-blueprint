# Track 2 · Does `prefers-reduced-motion` reach an SVG?

**No — and 369 files in the survey are written as though it does.** But there is
a mechanism that works, and it isn't the one people are using.

## Three findings

1. **The media query never applies inside an SVG referenced as an image.** Not
   in Chromium, not in Firefox, not in WebKit. A `@media (prefers-reduced-motion:
   reduce)` block in an SVG is dead code.
2. **`prefers-color-scheme` *does* apply in the same place, in all three.** So
   this isn't "image documents ignore media queries" — it is specific to the
   reduced-motion feature, which is what makes the mistake so easy to make.
3. **A `<picture>` source gated on reduced motion works**, because the host page
   evaluates it. GitHub's sanitizer keeps the attribute. This is the only way
   found to honour the preference in a README.

## What people are shipping

Re-fetching every SVG the survey recorded as animated
(`tools/research/reduced_motion_survey.py`, 1,863 of 1,871 still reachable):

| | |
|---|--:|
| Animated SVGs carrying a `prefers-reduced-motion` guard | **369** (19.8%) |
| Distinct profiles behind them | **26** |
| Profiles with any animated SVG | 273 |
| So: profiles that tried to respect the preference | **9.5%** |

The file count is skewed by a few prolific authors — Xalzeroph alone accounts
for 72 files, sepahead 36, harkirat-data and umang-eng 32 each. These are the
most conscientious profiles in the corpus, and the guard does nothing.

## How it was tested

**Isolated** (`/tmp` throwaway, method reproduced below): a 60×60 SVG whose only
behaviour is `fill: green`, turning red if the query applies, referenced from a
`data:` URL in a blank page. Two contexts per engine, identical except for the
emulated preference, compared by screenshot.

| Engine | `prefers-reduced-motion` | `prefers-color-scheme` (control) |
|---|---|---|
| Chromium 153 | no effect | **applied** |
| Firefox 155 | no effect | **applied** |
| WebKit 26.6 | no effect | **applied** |

The control is the point: the same mechanism, in the same file, through the same
harness, changes the image when the feature is `prefers-color-scheme`. So a null
result on reduced motion is the browser's behaviour, not the test failing.

**On GitHub** (`tools/matrix/capture.mjs`, now taking a `REDUCED` environment
variable and any `PAGE`): three fixtures in
[reduced-motion-gallery.md](reduced-motion-gallery.md) — a CSS keyframe
animation with the guard, a SMIL animation with the same guard, and a version
that tries to hide the animated layer and show a still one. Captured in all
three engines with and without the preference. **All three kept moving in every
engine, in both states.** The layer-swap trick fails for the same reason as the
rest: the query it depends on never matches.

Then the `<picture>` test, same page, reading which file each engine actually
loaded:

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| no preference | `rm-motion.svg` | `rm-motion.svg` | `rm-motion.svg` |
| `reduce` | **`rm-still.svg`** | **`rm-still.svg`** | **`rm-still.svg`** |

## The recipe that works

```html
<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-still.svg">
  <img alt="…" src="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner.svg" width="600">
</picture>
```

Combining it with dark/light means four files and ordered sources — the first
matching `<source>` wins, so the reduced-motion ones go first:

```html
<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)"  srcset=".../banner-still-dark.svg">
  <source media="(prefers-reduced-motion: reduce)"                                   srcset=".../banner-still-light.svg">
  <source media="(prefers-color-scheme: dark)"                                       srcset=".../banner-dark.svg">
  <img src=".../banner-light.svg" alt="…" width="600">
</picture>
```

Cheaper alternative, and often the better one: **don't animate the thing that
would need a still variant.** A design whose first frame is already the finished
composition — the rule the profile build follows — degrades to a still image for
free.

## Method note

The first version of the isolated test read the pixel back through a canvas and
reported "ignored" for Firefox on *both* features. That was a false negative:
Firefox blocks reading an SVG-backed canvas, so the probe could not distinguish
"query didn't apply" from "couldn't look". Caught by the control disagreeing
with the Phase 3 matrix, and replaced with screenshot comparison, which has no
such blind spot. Any tool that reports a negative it cannot distinguish from a
failure to measure is not a measurement.
