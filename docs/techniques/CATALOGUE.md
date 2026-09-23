# Technique catalogue

Every technique found in hand-made profile SVGs, each with who actually uses
it, a minimal pattern, and what was verified on GitHub's real renderer.

- **Usage** counts come from the survey: profiles using the technique in at
  least one bespoke SVG (`docs/survey/data/summary.json`). Cited files are from
  `docs/survey/data/technique_exemplars.json`.
- **Examples** are original, in [`examples/`](examples/), and rendered together
  in [GALLERY.md](GALLERY.md).
- **Verified** means loaded — and, where it applies, seen animating — inside
  GitHub's rendered page at 1280px and 390px, dark and light, by
  `tools/techniques/verify.py`. Full grid: [VERIFIED.md](VERIFIED.md).
  Chromium, Firefox and WebKit side by side:
  [CAPABILITY-MATRIX.md](../CAPABILITY-MATRIX.md).

The ground rule behind all of it: an SVG in a README is displayed as an image,
which browsers run in *secure animated mode* — declarative animation runs;
scripts, interaction and external resources don't. Every entry below lives
inside that box.

---

## Motion

### SMIL animation — 129 profiles

`<animate>`, `<animateMotion>`, `<animateTransform>` and `<set>`, declared in
the SVG itself. The most-used animation method in hand-made profile SVGs.

Used by: [JGit705](https://github.com/JGit705),
[SergiGTAr](https://github.com/SergiGTAr),
[getaudra](https://github.com/getaudra) · file:
[AlexChek51/header-dark.svg](https://github.com/AlexChek51/AlexChek51/blob/main/assets/header-dark.svg)

```svg
<path id="track" d="M50 160 C 190 30, 410 30, 550 160" fill="none"/>
<circle r="11" fill="#58a6ff">
  <animateMotion dur="3s" repeatCount="indefinite"
                 calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.55 1">
    <mpath href="#track"/>
  </animateMotion>
</circle>
```

Examples: [`smil-motion.svg`](examples/smil-motion.svg),
[`smil-draw.svg`](examples/smil-draw.svg) · **Verified: renders and animates.**

- `calcMode="spline"` with `keySplines` gives eased motion; `discrete` gives
  hard steps (typing, blinking cursors).
- `fill="freeze"` holds the last frame of a one-shot animation instead of
  snapping back.
- SMIL can animate things CSS can't reach in an SVG image: `startOffset` on
  `textPath`, `gradientTransform`, path motion.

### CSS `@keyframes` inside the SVG — 101 profiles

A `<style>` block in the SVG with ordinary CSS animations.

Used by: [ayxn07](https://github.com/ayxn07),
[ashfordeOU](https://github.com/ashfordeOU),
[sepahead](https://github.com/sepahead) · file:
[sepahead/hero-light.svg](https://github.com/sepahead/sepahead/blob/main/assets/hero-light.svg)

```svg
<style>
  .ring { transform-box: fill-box; transform-origin: center;
          animation: spin 6s linear infinite; }
  @keyframes spin { to { transform: rotate(360deg); } }
  @media (prefers-reduced-motion: reduce) { .ring { animation: none; } }
</style>
```

Example: [`css-keyframes.svg`](examples/css-keyframes.svg) · **Verified:
renders and animates.**

- **`transform-box: fill-box` is not optional.** Without it, `transform-origin:
  center` means the centre of the whole SVG canvas, and a rotating element
  orbits instead of spinning.
- A `prefers-reduced-motion` query inside the image follows the viewer's
  operating-system setting. Include it; not verified here (Phase 3).

### Ambient particles — seen across starfield and "space" profiles

Many small elements with the same short loop, desynchronised.

```svg
<circle cx="120" cy="40" r="1.6" fill="#e6edf3">
  <animate attributeName="opacity" values="0.15;1;0.15"
           dur="2.7s" begin="-1.3s" repeatCount="indefinite"/>
</circle>
```

Example: [`particles.svg`](examples/particles.svg) · **Verified: renders and
animates.**

- **A negative `begin` starts the loop part-way through**, so dozens of
  identical animations twinkle at random phases without any timeline logic.

---

## Drawing

### Stroke-dash line drawing — 93 profiles

A path "draws itself" by animating `stroke-dashoffset`.

Used by: [ayxn07](https://github.com/ayxn07),
[SimarBhatiaSB7](https://github.com/SimarBhatiaSB7),
[JConfessor](https://github.com/JConfessor) · file:
[ayxn07/card-ayxn-studio.svg](https://github.com/ayxn07/Ayxn07/blob/main/assets/card-ayxn-studio.svg)

```svg
<path pathLength="1" d="M40 130 Q 110 40 180 120 T 320 110 …"
      stroke-dasharray="1" stroke-dashoffset="1" …/>
<!-- then animate stroke-dashoffset 1 → 0 with CSS or <animate> -->
```

Examples: [`stroke-draw.svg`](examples/stroke-draw.svg) (CSS),
[`smil-draw.svg`](examples/smil-draw.svg) (SMIL) · **Verified: both render and
animate.**

- **`pathLength="1"` normalises the path's length**, so `dasharray="1"` and an
  offset from 1 to 0 work for any path without measuring it. The same trick
  with `pathLength="100"` makes a dash length read as a percentage (see
  Gauges).

---

## Light and texture

### Glow — 90 profiles

`feGaussianBlur` merged back under the source graphic.

Used by: [Dhyanesh006](https://github.com/Dhyanesh006),
[SergiGTAr](https://github.com/SergiGTAr),
[JackLuciano](https://github.com/JackLuciano) · file:
[Dhyanesh006/matrix-banner.svg](https://github.com/Dhyanesh006/Dhyanesh006/blob/main/assets/matrix-banner.svg)

```svg
<filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/>
           <feMergeNode in="SourceGraphic"/></feMerge>
</filter>
```

Example: [`glow.svg`](examples/glow.svg) · **Verified: renders and animates**
(the flicker is a brief opacity dip, so not every sampling pass catches it).

- **Enlarge the filter region.** The default is 10% past the bounding box; a
  big blur is clipped to a hard rectangle without the `x/y/width/height` above.

### Film grain — part of the 102 profiles using filters

`feTurbulence` noise, desaturated and faded, composited over a surface.

```svg
<filter id="grain">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7"/>
  <feColorMatrix type="saturate" values="0"/>
  <feComponentTransfer><feFuncA type="linear" slope="0.22"/></feComponentTransfer>
  <feComposite in2="SourceGraphic" operator="in"/>
</filter>
```

Example: [`grain.svg`](examples/grain.svg) · **Verified: renders** (static by
design).

- Texture with no image file and a fixed `seed`, so output is deterministic —
  it won't create a new commit every time a generator runs.

### Gradients — 130 profiles

The most common technique of all. Static fills, and animated shimmer.

```svg
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0">
  <stop offset="0.45" stop-color="#8b949e"/><stop offset="0.5" stop-color="#fff"/>
  <stop offset="0.55" stop-color="#8b949e"/>
  <animate attributeName="x1" values="-300;300" dur="2.6s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="0;600"    dur="2.6s" repeatCount="indefinite"/>
</linearGradient>
```

Example: [`gradient-shimmer.svg`](examples/gradient-shimmer.svg) · **Verified:
renders and animates in Chromium, Firefox and WebKit.**

- **Don't animate `gradientTransform`.** It's the obvious approach and the one
  most tutorials show, but **WebKit — Safari's engine — never animates it** in
  an SVG image, on text or on shapes: in a 45-frame capture the highlight stayed
  frozen in every frame, while Chromium and Firefox moved. Animating the
  gradient's `x1`/`x2` (above) or its stop `offset`s works in all three.
  The frozen version is kept as
  [`gradient-transform.svg`](examples/gradient-transform.svg) so the capability
  matrix records the difference.

---

## Reveals and text

### Masks and clip paths — 28 and 90 profiles

Clip paths mostly round card corners; masks do soft reveals.

Used by: [JGit705](https://github.com/JGit705),
[atikulmunna](https://github.com/atikulmunna),
[nihalsheikh](https://github.com/nihalsheikh) · file:
[JGit705/hero.svg](https://github.com/JGit705/JGit705/blob/main/profile/assets/hero.svg)

```svg
<mask id="reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="600" height="220">
  <rect width="0" height="220" fill="url(#soft)">
    <animate attributeName="width" values="0;600;600;0" keyTimes="0;0.4;0.85;1"
             dur="4s" repeatCount="indefinite"/>
  </rect>
</mask>
```

Example: [`mask-reveal.svg`](examples/mask-reveal.svg) · **Verified: renders and
animates.**

- A gradient inside the mask gives the reveal a soft leading edge instead of a
  hard wipe.

### Typing — via readme-typing-svg (87 profiles) or hand-made

A clip rectangle widening one character at a time, plus a blinking cursor.

Used by: [readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg)
(the service; 54% of its instances are illegible on a phone — see
`docs/survey/GENERATORS.md`) · hand-made file:
[SuperZombi/typing.svg](https://github.com/SuperZombi/SuperZombi/blob/main/stats/typing.svg)

```svg
<text textLength="390" lengthAdjust="spacingAndGlyphs" font-family="ui-monospace, …">
  hello, profile</text>
<!-- clip width steps of 390 / 14 = 27.86 units, calcMode="discrete" -->
```

Example: [`typing.svg`](examples/typing.svg) · **Verified: renders and
animates.**

- **`textLength` makes it font-proof.** The viewer's fallback monospace varies
  by platform; forcing the string to an exact width means each clip step
  reveals exactly one character everywhere. Without it, the reveal drifts out of
  step with the letters.
- Keep the text large: typing banners are wide, and the service's defaults
  often end up under 11px on a phone.

### Text on a path — 12 profiles

```svg
<text><textPath href="#wave" startOffset="0">riding the curve …
  <animate attributeName="startOffset" values="0;-300" dur="6s" repeatCount="indefinite"/>
</textPath></text>
```

Used by: [SuperZombi](https://github.com/SuperZombi),
[rroy233](https://github.com/rroy233) · Example:
[`textpath.svg`](examples/textpath.svg) · **Verified: renders and animates.**

### Terminal simulation — a recurring shortlist motif

Lines appearing in sequence under a window chrome.

Used by: [10ishk](https://github.com/10ishk),
[Dhyanesh006](https://github.com/Dhyanesh006),
[JGit705](https://github.com/JGit705)

```svg
<text opacity="0">engineer · builder
  <animate attributeName="opacity" values="0;1" keyTimes="0;0.22"
           dur="5s" repeatCount="indefinite" calcMode="discrete"/></text>
```

Example: [`terminal.svg`](examples/terminal.svg) · **Verified: renders and
animates.**

- **One cycle, one timeline per line.** Chaining `begin="x.end"` timers across
  elements gets fragile fast; giving every line its own discrete keyTime on the
  same repeating duration resets cleanly each loop.

---

## Data

### Gauges and meters

```svg
<path d="M-80 0 A 80 80 0 0 1 80 0" pathLength="100"
      stroke-dasharray="72 100" …/>   <!-- 72% -->
```

Example: [`gauge.svg`](examples/gauge.svg) · **Verified: renders and animates.**

- `pathLength="100"` turns the dash length into the value itself.

### Charts

Bars rising with a staggered `begin`, animating `height` and `y` together (SVG
rects grow downward from `y`).

Used by: [sepahead](https://github.com/sepahead),
[JConfessor](https://github.com/JConfessor) · Example:
[`bars.svg`](examples/bars.svg) · **Verified: renders and animates.**

- Real data means a generator and a workflow to refresh it. Commit the output
  rather than rent a service: the survey found hosted chart services among the
  most broken (`docs/survey/FINDINGS.md` §1).

### Contribution art — generated by Actions

Not hand-made, but everywhere. Counted by the signature each tool leaves in the
files that loaded: the snk snake (65 profiles), lowlighter/metrics (17), 3D
contribution graphs (12), pacman (5). Each runs as a scheduled Action that
commits its SVG. They survive because they're committed; some are among the
least legible on a phone (metrics: 83% of its cards).

---

## Theme switching

Three mechanisms, all **verified working** — each showed the dark variant under
a dark scheme and the light one under a light scheme.

| Mechanism | Profiles | Follows |
|---|--:|---|
| `<picture>` + `prefers-color-scheme` | 80 | The page |
| `#gh-dark-mode-only` / `#gh-light-mode-only` on the image URL | 7 | The page — still works in 2026 |
| `@media (prefers-color-scheme)` inside the SVG | 35 | The viewer's operating system |

```html
<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="…/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="…/banner-light.svg">
  <img src="…/banner-dark.svg" alt="…">
</picture>
```

Examples: [`theme-picture-*.svg`](examples/),
[`theme-fragment-*.svg`](examples/), [`theme-aware.svg`](examples/theme-aware.svg).

- **`<picture>` is the one to use.** It evaluates against the host page, needs
  two files, and costs nothing at runtime.
- An in-SVG media query can disagree with the page when a signed-in viewer has
  set GitHub's theme differently from their OS. That case needs a signed-in
  test and is open for Phase 3 — the verification here was signed out, where
  GitHub follows the OS and the two agree.
- Relative `srcset` paths **do** resolve on the profile page — verified on 33
  live profiles, `docs/research/RELATIVE-SRCSET.md`. Absolute
  `raw.githubusercontent.com` URLs remain the safer default for portability, not
  for correctness.

---

## Fonts

- **System stacks work everywhere** — and so does a named font listed first,
  for viewers who have it installed.
- **`@import` of a web font is blocked.** Verified: the test falls back to the
  next font in the stack, in every pass.
- **Embedded base64 fonts work — 13 profiles** — at a cost. Surveyed SVGs
  that embed a font have a median size of **27.3 KB**, against **3.1 KB** for
  bespoke SVGs without. Subset to the glyphs you use. Used by
  [ashfordeOU](https://github.com/ashfordeOU) and
  [SimarBhatiaSB7](https://github.com/SimarBhatiaSB7) · file:
  [ashfordeOU/hero-light.svg](https://github.com/ashfordeOU/ashfordeOU/blob/main/assets/hero-light.svg).
  Not re-demonstrated here to avoid redistributing a font file; the cited
  exemplars render with their fonts on GitHub today.

## Embedded images

- **Embedded raster — 23 profiles** (base64 PNG/JPEG inside the SVG, e.g. an
  avatar in a card). Works; median file **69.9 KB**, 22× a plain bespoke SVG.
- **External `<image href="https://…">` is blocked in every engine** — but
  not uniformly. Chromium draws its broken-image icon in place of the image,
  covering whatever was beneath; Firefox and WebKit draw nothing. Never
  reference external images from inside an SVG; embed them or leave them out.

## `<foreignObject>` — 32 profiles

HTML and CSS inside an SVG. **Verified rendering in Chromium, Firefox and
WebKit** — flexbox, rounded backgrounds and system fonts all drew. Mostly reaches profiles through one
generator: [jstrieb/github-stats](https://github.com/jstrieb/github-stats)
builds its cards this way (committed by
[MacroPower](https://github.com/MacroPower) and others). Hand-made use:
[YoraiLevi/card-dark-0.svg](https://github.com/YoraiLevi/YoraiLevi/blob/master/assets/card-dark-0.svg).

- Safari has a long history of `foreignObject` bugs inside images. Desktop
  WebKit 26.6 renders this example correctly; iOS Safari and the GitHub mobile
  apps are untested.

## Interaction

Nothing inside an SVG image is interactive. What profiles use instead:

- **A link around an image** — the whole card becomes a button.
- **Issues as input** — a link opens a pre-filled Issue; an Action reads it and
  commits a new README. [marcizhu](https://github.com/marcizhu)'s chess game and
  [BrunnerLivio](https://github.com/BrunnerLivio)'s guestbook work this way.
- **`<details>`** — native markdown, collapsible, real text. Rendered in the
  gallery; reflows at any width.

## Verified to fail

| Attempt | Result on GitHub |
|---|---|
| `<script>` in the SVG | Never runs — the test panel stayed green in every pass |
| External `<image>` | Blocked; broken-image icon drawn |
| `@import` web font | Blocked; falls back |
| Inline `<svg>` pasted into markdown | Removed by GitHub's sanitizer (skill reference; not re-tested) |

## Seen but rare

Not given entries — one or two users isn't evidence a technique is viable:
`<script>` in a profile SVG (1 profile), SVG images embedded as base64 inside
another SVG (3).

## Limits

- Verified signed out, at two widths, in Chromium, Firefox and desktop WebKit.
  iOS Safari and the GitHub mobile apps can't be driven from here; the
  capability matrix ends with a checklist for checking them by hand.
- A committed copy of a service's output can pass as "bespoke" in the usage
  counts when the tool leaves no signature (one profile commits cached service
  cards under `assets/auto/`).
