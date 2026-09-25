# Part 02 — Techniques, Engine Capability Matrix & Open Research Tracks

This part is the engineering half of the compilation: what SVG techniques real profiles actually use, what GitHub's renderer allows in each of three browser engines, and the eight open research tracks that document the edges. Every claim here is sourced from the repository's own research: the [technique catalogue](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/CATALOGUE.md), its [gallery](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/GALLERY.md) and [verification log](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/VERIFIED.md), the [capability matrix](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/CAPABILITY-MATRIX.md), the eight [research tracks](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/TRACKS.md) with their reports under [`docs/research/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/docs/research), and the reusable skill at [`skills/github-profile-readme/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/skills/github-profile-readme). Usage rates come from a survey of 446 real profiles; engine verdicts come from captures run inside GitHub's own rendered page in Chromium, Firefox and WebKit. Nothing is asserted that was not measured, and anything unmeasured is tagged **UNVERIFIED**.

---

## Ground rules — what GitHub's renderer allows

The catalogue opens with the rule everything else depends on:

> SVG in a README is displayed as an image, and browsers run it in **secure animated mode**: declarative animation runs; scripts, interaction and external resources don't.

This is the SVG integration spec's behaviour, not a GitHub policy — which is why it is identical in Chromium, Firefox and WebKit. Referencing an SVG through `<img>` or `![]()` triggers it; opening the same file directly does not, which is why an animation that plays when you open the file also plays in the README while its hover states and web fonts silently don't.

### What runs, what doesn't

| Feature | Behaviour in a README (Chromium / Firefox / WebKit) |
|---|---|
| SMIL (`<animate>`, `<animateMotion>`, `<animateTransform>`, `<set>`) | **runs, all engines** |
| CSS `@keyframes` | **runs, all engines** |
| Masks, clip paths, stroke-dash, `textPath`, filters, gauges, particles | **run, all engines** |
| `gradientTransform` animation | Chromium ✓, Firefox ✓, **WebKit never animates it** — the one engine difference found; animate `x1`/`x2` or stop offsets instead (both verified everywhere) |
| `<script>`, `onclick` / `onmouseover`, `:hover`, tooltips | **blocked / stripped in all engines** |
| `@import`ed web fonts (Google Fonts etc.) | **blocked in all engines**, silent fallback |
| External `<image href="https://…">` | blocked — Chromium **paints a broken-image icon** into the design, Firefox draws nothing, WebKit inconsistent |
| HTML inside `<foreignObject>` | renders (Chromium), renders (Firefox), inconsistent (WebKit) |
| Inline `<svg>` pasted into markdown | **removed entirely by GitHub's sanitizer** — `svg` is not on the allowed-element list; the file must be referenced, never pasted |
| `@media (prefers-reduced-motion: reduce)` inside the SVG | **never applies, any engine** — dead code (369 files across 26 surveyed profiles contain it) |
| `@media (prefers-color-scheme)` inside the SVG | **applies, all engines** — which is what makes the reduced-motion mistake so easy to make |
| `<source media="…">` on `<picture>` | GitHub's sanitizer keeps the `media` attribute and the host page evaluates it — theme, viewport width and reduced motion all work as gates |

The failure modes are documented as boundary-test fixtures in [`docs/techniques/examples/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/docs/techniques/examples): `test-script.svg`, `test-external-image.svg`, `test-external-font.svg`, `test-foreign-object.svg`. A blocked external image does not fail quietly — it draws Chrome's broken-image glyph into the layout, which once fooled the survey tooling itself into recording a successful load.

### Things that look like they should work and do not

From the skill's recipe reference:

| Attempt | Result |
|---|---|
| `<script>` in SVG | stripped |
| `onclick`, `onmouseover` | stripped |
| `:hover` CSS in SVG | never fires — no interactivity |
| `<foreignObject>` with HTML | unreliable; avoid |
| `@import url(fonts.googleapis…)` | blocked by CSP, silent fallback |
| `<image href="https://…">` inside SVG | external ref, blocked |
| inline `<svg>` in markdown | removed by sanitizer |
| `prefers-color-scheme` inside the SVG | **works** — verified in three engines; follows the OS, not the GitHub theme setting, exactly as `<picture>` does |

Two practical consequences the research keeps returning to: **the only interaction available in a README is a link** (wrap a `<picture>` in an `<a>` and an entire panel becomes the largest tap target a README can have), and **an SVG cannot fetch anything**, so `font-family: 'JetBrains Mono', monospace` renders as JetBrains Mono only for viewers who already have it — everyone else silently gets the next entry. Design for the fallback stack, embed a subset as base64 if you must (13 surveyed profiles do), or convert the wordmark to paths.

---

## The technique catalogue

[`docs/techniques/CATALOGUE.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/CATALOGUE.md) is the survey's technique list turned into minimal working examples. Usage counts come from `docs/survey/data/summary.json` and exemplar references from `technique_exemplars.json`; each entry names profiles that actually ship the technique. Every example lives in [`docs/techniques/examples/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/docs/techniques/examples) and is embedded in the gallery below.

### How often each technique appears

Counted per profile, so one profile with forty files can't outvote forty with one (survey of 446 profiles):

| Technique | Profiles | Notes |
|---|--:|---|
| Gradients | 130 | |
| SMIL (`<animate>`, `animateMotion`) | 129 | beats CSS keyframes in hand-made work |
| Filters | 102 | |
| CSS `@keyframes` | 101 | |
| Stroke-dash line drawing | 93 | |
| Blur / glow | 90 | |
| Clip paths | 90 | |
| `prefers-color-scheme` inside the SVG | 35 | theme switching without `<picture>` |
| `<foreignObject>` | 32 | renders in Chromium/Firefox, inconsistent in WebKit |
| Masks | 28 | |
| Base64-embedded fonts | 13 | |
| Text on a path (`textPath`) | 12 | |
| Contribution art: snk | 65 | |
| Contribution art: lowlighter/metrics | 17 | |
| Contribution art: 3D graphs | 12 | |
| Contribution art: pacman | 5 | |
| Theme via `<picture>` | 80 | vs 7 using `#gh-dark-mode-only` fragments |

All catalogue entries were rebuilt as minimal examples; the gallery renders them all; "Verified" below means each was loaded and seen animating **inside GitHub's rendered page** at 1280px and 390px, dark and light, by `tools/techniques/verify.py`.

### SMIL animation — 129 profiles

`<animate>`, `<animateMotion>`, `<animateTransform>` and `<set>` — declarative, so they run in secure animated mode in every engine. Exemplar: `AlexChek51/header-dark.svg`; shipping profiles include **JGit705**, **SergiGTAr**, **getaudra**.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 220" width="600" height="220" role="img" aria-label="A dot travelling along a curved path">
  <rect width="600" height="220" rx="16" fill="#0d1117"/>
  <path id="track" d="M50 160 C 190 30, 410 30, 550 160" fill="none" stroke="#30363d" stroke-width="3" stroke-linecap="round"/>
  <circle r="11" fill="#58a6ff">
    <animateMotion dur="3s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.55 1">
      <mpath href="#track"/>
    </animateMotion>
  </circle>
  <text x="50" y="200" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace" font-size="24" fill="#8b949e">animateMotion + mpath</text>
</svg>
```

(`examples/smil-motion.svg` — `calcMode="spline"` with `keySplines="0.45 0 0.55 1"` gives an ease-in-out glide; `<mpath href="#track">` follows the drawn curve. Verified.)

### Particles

A field of stars, each `<circle>` twinkling on its own cycle. The trick is a **negative `begin`**, which starts every particle mid-phase so the field never blinks in unison:

```svg
<circle cx="128" cy="20" r="2.1" fill="#e6edf3"><animate attributeName="opacity" values="0.15;1;0.15" dur="2.24s" begin="-0.31s" repeatCount="indefinite"/></circle>
<circle cx="118" cy="187" r="1.2" fill="#e6edf3"><animate attributeName="opacity" values="0.15;1;0.15" dur="3.14s" begin="-0.1s" repeatCount="indefinite"/></circle>
<circle cx="20" cy="54" r="2.6" fill="#e6edf3"><animate attributeName="opacity" values="0.15;1;0.15" dur="2.48s" begin="-0.39s" repeatCount="indefinite"/></circle>
<!-- … 44 more <circle> elements, same pattern, dur 1.7–4.2s, begin -0.02s to -3.82s … -->
<text x="40" y="190" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace" font-size="24" fill="#8b949e">negative begin = random phase</text>
```

(`examples/particles.svg` — 47 circles on a `#010409` field, viewBox 0 0 600 220. Verified.)

### CSS `@keyframes` — 101 profiles

Shipping profiles include **ayxn07**, **ashfordeOU**, **sepahead**. One rule makes or breaks it: `transform-box: fill-box` — without it, `transform-origin: center` resolves against the wrong box and the ring orbits off-card.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 220" width="600" height="220" role="img" aria-label="A rotating ring around a pulsing core">
  <style>
    .ring { transform-box: fill-box; transform-origin: center; animation: spin 6s linear infinite; }
    .core { transform-box: fill-box; transform-origin: center; animation: pulse 2s ease-in-out infinite; }
    @keyframes spin  { to { transform: rotate(360deg); } }
    @keyframes pulse { 50% { transform: scale(0.72); opacity: 0.6; } }
    @media (prefers-reduced-motion: reduce) { .ring, .core { animation: none; } }
  </style>
  <rect width="600" height="220" rx="16" fill="#0d1117"/>
  <circle class="ring" cx="120" cy="105" r="62" fill="none" stroke="#a371f7" stroke-width="6" stroke-dasharray="60 30" stroke-linecap="round"/>
  <circle class="core" cx="120" cy="105" r="26" fill="#a371f7"/>
  <text x="230" y="98"  font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="30" font-weight="700" fill="#f0f6fc">CSS @keyframes</text>
  <text x="230" y="138" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace" font-size="24" fill="#8b949e">transform-box: fill-box</text>
</svg>
```

Note the last line of the `<style>` block: `@media (prefers-reduced-motion: reduce)`. It is **dead code inside an SVG** — Track 2 proved the query never applies in any engine — kept here deliberately because 369 files across 26 surveyed profiles contain exactly that guard, and because `prefers-color-scheme` applies in the same position, which is what makes the mistake so easy.

### Stroke-dash line drawing — 93 profiles

Shipping profiles include **ayxn07**, **SimarBhatiaSB7**, **JConfessor**. `pathLength="1"` normalises any path to one unit so the dash maths is trivial. Two flavours, both Verified:

```svg
<!-- CSS flavour: examples/stroke-draw.svg -->
<style>
  .draw { stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 3.5s ease-in-out infinite; }
  @keyframes draw { 0% { stroke-dashoffset: 1; } 55%, 80% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -1; } }
</style>
<path class="draw" pathLength="1" d="M40 130 Q 110 40 180 120 T 320 110 T 460 100 T 560 70"
      fill="none" stroke="#3fb950" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
```

```svg
<!-- SMIL flavour: examples/smil-draw.svg -->
<path d="M40 132 L 400 132" pathLength="1" stroke="#f78166" stroke-width="7" stroke-linecap="round" stroke-dasharray="1" stroke-dashoffset="1">
  <animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;0.4;0.85;1" dur="3s" repeatCount="indefinite"/>
</path>
```

### Masks and reveal

`examples/mask-reveal.svg` — a `<mask>` whose rect grows `0 → 600` and resets, with a soft-gradient edge so the headline wipes in rather than snapping:

```svg
<defs>
  <linearGradient id="soft" x1="0" x2="1"><stop offset="0.85" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <mask id="reveal" maskUnits="userSpaceOnUse" x="0" y="0" width="600" height="220">
    <rect x="0" y="0" width="0" height="220" fill="url(#soft)">
      <animate attributeName="width" values="0;600;600;0" keyTimes="0;0.4;0.85;1" dur="4s" repeatCount="indefinite"/>
    </rect>
  </mask>
</defs>
<g mask="url(#reveal)">
  <text x="40" y="112" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="52" font-weight="800" fill="#f0f6fc">Revealed by a mask</text>
</g>
```

### Film grain — no image file

`examples/grain.svg` — `feTurbulence` noise composited inside the card's own clip path. Static (the matrix records it as static-but-rendering), which is the point: texture without motion:

```svg
<filter id="grain">
  <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="7" result="noise"/>
  <feColorMatrix in="noise" type="saturate" values="0" result="mono"/>
  <feComponentTransfer in="mono" result="faint"><feFuncA type="linear" slope="0.22"/></feComponentTransfer>
  <feComposite in="faint" in2="SourceGraphic" operator="in"/>
</filter>
<clipPath id="card"><rect width="600" height="220" rx="16"/></clipPath>
<g clip-path="url(#card)">
  <rect width="600" height="220" fill="url(#g)"/>
  <rect width="600" height="220" fill="#fff" filter="url(#grain)"/>
</g>
```

### Glow — 90 profiles

Shipping profiles include **Dhyanesh006**, **SergiGTAr**, **JackLuciano**. `examples/glow.svg` — `feGaussianBlur` merged back over the source, plus a slow opacity pulse so the neon breathes:

```svg
<defs>
  <filter id="glow" x="-20%" y="-40%" width="140%" height="180%">
    <feGaussianBlur in="SourceGraphic" stdDeviation="6" result="blur"/>
    <feMerge><feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>
<text x="300" y="120" text-anchor="middle" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="56" font-weight="800" fill="#39d0d8" filter="url(#glow)">NEON
  <animate attributeName="opacity" values="1;0.55;1;1;0.8;1" keyTimes="0;0.04;0.08;0.6;0.63;1" dur="4s" repeatCount="indefinite"/>
</text>
```

### Shimmer — animate `x1`/`x2`, not `gradientTransform`

The one engine difference in the whole matrix: **WebKit never animates `gradientTransform`.** Two Verified workarounds:

```svg
<!-- examples/gradient-shimmer.svg — animates x1/x2 in user space. Works everywhere. -->
<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="-300" y1="0" x2="0" y2="0">
  <stop offset="0" stop-color="#8b949e"/><stop offset="0.45" stop-color="#8b949e"/>
  <stop offset="0.5" stop-color="#ffffff"/>
  <stop offset="0.55" stop-color="#8b949e"/><stop offset="1" stop-color="#8b949e"/>
  <animate attributeName="x1" values="-300;300" dur="2.6s" repeatCount="indefinite"/>
  <animate attributeName="x2" values="0;600" dur="2.6s" repeatCount="indefinite"/>
</linearGradient>
```

```svg
<!-- examples/gradient-transform.svg — Chromium ✓ Firefox ✓, WebKit NO MOTION (renders static) -->
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="2.6s" repeatCount="indefinite"/>
```

Animating the gradient's stop offsets instead is the third portability option, also verified everywhere.

### Typing effect

`examples/typing.svg` — a clip rect steps one character at a time; `textLength="390"` forces the string to exactly 390 units whatever font the viewer falls back to, so each step of 27.86 units reveals exactly one character:

```svg
<defs>
  <clipPath id="typed"><rect x="40" y="60" height="70" width="0">
    <animate attributeName="width" dur="5s" repeatCount="indefinite" calcMode="discrete"
      values="0.0;27.9;55.7;83.6;111.4;139.3;167.1;195.0;222.9;250.7;278.6;306.4;334.3;362.1;390.0;390;0"
      keyTimes="0.0;0.032;0.064;0.096;0.129;0.161;0.193;0.225;0.257;0.289;0.321;0.354;0.386;0.418;0.45;0.9;1"/>
  </rect></clipPath>
</defs>
<g clip-path="url(#typed)">
  <text x="40" y="112" textLength="390" lengthAdjust="spacingAndGlyphs"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace" font-size="44" fill="#3fb950">hello, profile</text>
</g>
```

The caret is a second rect animating `x` on the same `keyTimes` grid, with a `values="1;0"` opacity blink. The `readme-typing-svg` service renders the same idea as a rented image — it loaded 100% in the survey, but a committed file has no third party on the critical path at all.

### Text on a path — 12 profiles

Shipping profiles include **SuperZombi**, **rroy233**. `examples/textpath.svg` — animating `startOffset` slides the string along the wave:

```svg
<defs><path id="wave" d="M-40 120 Q 60 50 160 120 T 360 120 T 560 120 T 760 120"/></defs>
<text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="30" font-weight="700" fill="#d2a8ff">
  <textPath href="#wave" startOffset="0">riding the curve · riding the curve · riding the curve
    <animate attributeName="startOffset" values="0;-300" dur="6s" repeatCount="indefinite"/>
  </textPath>
</text>
```

### Terminal motif

Shipping profiles include **10ishk**, **Dhyanesh006**, **JGit705**. `examples/terminal.svg` — one repeating 5s cycle, each line revealed by `calcMode="discrete"` opacity steps, so no timers need chaining (an `begin="x.end"` chain desynchronises over time):

```svg
<g font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace" font-size="24">
  <text x="32" y="90" fill="#3fb950" opacity="0">$ whoami
    <animate attributeName="opacity" values="0;1" keyTimes="0;0.06" dur="5s" repeatCount="indefinite" calcMode="discrete"/></text>
  <text x="32" y="130" fill="#e6edf3" opacity="0">engineer · builder
    <animate attributeName="opacity" values="0;1" keyTimes="0;0.22" dur="5s" repeatCount="indefinite" calcMode="discrete"/></text>
  <text x="32" y="170" fill="#e6edf3" opacity="0">status: shipping
    <animate attributeName="opacity" values="0;1" keyTimes="0;0.38" dur="5s" repeatCount="indefinite" calcMode="discrete"/></text>
  <rect x="32" y="190" width="14" height="26" fill="#e6edf3">
    <animate attributeName="opacity" values="1;0" dur="0.9s" repeatCount="indefinite" calcMode="discrete"/>
  </rect>
</g>
```

Caution carried over from the survey: a terminal that starts everything at `opacity="0"` shows **nothing** to a static renderer — see the first-frame rule in the process section.

### Gauges

`examples/gauge.svg` — `pathLength="100"` turns the arc into a percentage track, so `stroke-dasharray="72 100"` *is* the value:

```svg
<path d="M-80 0 A 80 80 0 0 1 80 0" pathLength="100" fill="none" stroke="#e3b341" stroke-width="18" stroke-linecap="round"
      stroke-dasharray="72 100">
  <animate attributeName="stroke-dasharray" values="0 100;72 100;72 100;0 100" keyTimes="0;0.3;0.9;1"
           dur="4s" repeatCount="indefinite" calcMode="spline" keySplines="0.3 0 0.2 1;0 0 1 1;0.4 0 1 1"/>
</path>
```

### Bar charts

Shipping profiles include **sepahead**, **JConfessor**. `examples/bars.svg` — two rules: animate **`height` and `y` together** (grow from the baseline, not from the top edge), and stagger `begin` by 0.12s per bar:

```svg
<rect x="52" width="34" rx="4" fill="#58a6ff" y="170" height="0">
  <animate attributeName="height" values="0;48;48;0" keyTimes="0;0.25;0.9;1" dur="4s" begin="0.00s" repeatCount="indefinite" calcMode="spline" keySplines="0.2 0.8 0.2 1;0 0 1 1;0.6 0 1 1"/>
  <animate attributeName="y" values="170;122;122;170" keyTimes="0;0.25;0.9;1" dur="4s" begin="0.00s" repeatCount="indefinite" calcMode="spline" keySplines="0.2 0.8 0.2 1;0 0 1 1;0.6 0 1 1"/>
</rect>
<rect x="104" width="34" rx="4" fill="#58a6ff" y="170" height="0">
  <animate attributeName="height" values="0;82;82;0" keyTimes="0;0.25;0.9;1" dur="4s" begin="0.12s" repeatCount="indefinite" calcMode="spline" keySplines="0.2 0.8 0.2 1;0 0 1 1;0.6 0 1 1"/>
  <animate attributeName="y" values="170;88;88;170" keyTimes="0;0.25;0.9;1" dur="4s" begin="0.12s" repeatCount="indefinite" calcMode="spline" keySplines="0.2 0.8 0.2 1;0 0 1 1;0.6 0 1 1"/>
</rect>
<!-- … four more bars, begin 0.24s / 0.36s / 0.48s / 0.60s, values scaled to 64/110/95/130 … -->
```

Six bars, values 48–130 units off a `y=170` baseline, one 4s cycle. For live data the survey's standing advice applies throughout: **generate the SVG and commit it** — committed images loaded 99% of the time, rented chart services 0–11%.

### Contribution art

Whole-repo drawings counted in the wild: **snk** (the GitHub-contribution snake) 65 profiles, **lowlighter/metrics** 17, animated 3D contribution graphs 12, **pacman** 5. These are mostly CI-generated and committed — which is exactly why they survive.

### Theme switching — three mechanisms, all verified

```svg
<!-- examples/theme-aware.svg — mechanism 3: @media inside the SVG -->
<style>
  .bg { fill: #0d1117; } .fg { fill: #f0f6fc; } .muted { fill: #8b949e; }
  @media (prefers-color-scheme: light) { .bg { fill: #ffffff; } .fg { fill: #1f2328; } .muted { fill: #59636e; } }
</style>
```

| Mechanism | Profiles / usage | Verdict |
|---|---|---|
| `<picture>` + `prefers-color-scheme` | 80 profiles | works in all three engines — **prefer this**: one theme per file is easier to verify |
| `#gh-dark-mode-only` / `#gh-light-mode-only` fragments | 7 profiles | works in all three engines |
| `@media (prefers-color-scheme)` inside the SVG | 35 profiles | works in all three engines — *earlier skill docs said this was blocked; the capture disproved it* |

All three key off `prefers-color-scheme` — the viewer's **operating system**, never GitHub's theme setting. Someone with a light OS and GitHub set to dark sees the light asset on a dark page; nothing inside an image can read GitHub's theme.

---

## The gallery and its verification log

[`docs/techniques/GALLERY.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/GALLERY.md) embeds every catalogue example **the way a profile README embeds an image**, so GitHub's own markdown pipeline renders it — `tools/techniques/verify.py` then loads the page on github.com and records, per image, whether it loaded, whether it actually animates inside GitHub's page, and what the boundary tests reveal.

Design constraint stated up front: **all examples use a 600-unit viewBox with text at 24 units or more**, so text stays at or above ~12px in the 309px phone column.

The gallery's sections, each an `<img src="examples/…">` embed with descriptive `alt`:

- **Motion** — `smil-motion.svg`, `css-keyframes.svg`, `particles.svg`
- **Drawing** — `stroke-draw.svg`, `smil-draw.svg`
- **Light and texture** — `glow.svg`, `grain.svg`, `gradient-shimmer.svg`, `gradient-transform.svg`
- **Reveals and text** — `mask-reveal.svg`, `typing.svg`, `textpath.svg`, `terminal.svg`
- **Data** — `gauge.svg`, `bars.svg`
- **Theme switching** — all three mechanisms:

```html
<!-- inside the SVG (follows the viewer's OS scheme) -->
<img src="examples/theme-aware.svg" alt="A card that switches colours with the colour scheme">

<!-- <picture> with prefers-color-scheme -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="examples/theme-picture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="examples/theme-picture-light.svg">
  <img src="examples/theme-picture-dark.svg" alt="Theme variant served by picture">
</picture>

<!-- legacy URL fragments -->
![Dark variant served by fragment](examples/theme-fragment-dark.svg#gh-dark-mode-only)
![Light variant served by fragment](examples/theme-fragment-light.svg#gh-light-mode-only)
```

- **Boundary tests** — `test-script.svg`, `test-external-image.svg`, `test-external-font.svg`, `test-foreign-object.svg`, each built so the answer is visible in the render.
- **Native markdown** — a real `<details>` block: *"Markdown inside `<details>` reflows to any width, stays selectable and searchable, and is read by screen readers. It is the one layer of a profile that survives every screen."*

### What verify.py recorded

[`docs/techniques/VERIFIED.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/VERIFIED.md), generated from `verified.json` (do not edit by hand). Source page: `https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/techniques/GALLERY.md`. Each example was loaded inside GitHub's rendered markdown in headless Chrome at desktop (1280px) and phone (390px) width, dark and light. **✓** = GitHub served it and the browser drew it; **moves** = eight frames sampled 0.8s apart differed — the animation runs inside GitHub's page, not only when the file is opened alone; **hidden** = the correct outcome for a theme variant that shouldn't show in that scheme.

| Example | 1280 dark | 1280 light | 390 dark | 390 light | Verdict |
|---|---|---|---|---|---|
| `bars.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `css-keyframes.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `gauge.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `glow.svg` | ✓ moves | ✓ | ✓ moves | ✓ | renders and animates |
| `gradient-shimmer.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `gradient-transform.svg` | ✓ moves | ✓ moves | ✓ | ✓ moves | renders and animates |
| `grain.svg` | ✓ moves | ✓ | ✓ | ✓ | renders, static by design |
| `mask-reveal.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `particles.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `smil-draw.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `smil-motion.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `stroke-draw.svg` | ✓ moves | ✓ moves | ✓ | ✓ | renders and animates |
| `terminal.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `textpath.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |
| `typing.svg` | ✓ moves | ✓ moves | ✓ moves | ✓ moves | renders and animates |

Theme switching as recorded by the same pass:

| Mechanism | Dark scheme shows | Light scheme shows |
|---|---|---|
| `<picture>` + `prefers-color-scheme` | dark | light |
| `#gh-dark-mode-only` / `#gh-light-mode-only` | dark | light |
| `@media (prefers-color-scheme)` inside the SVG | dark | light |

Boundary tests, every pass:

| Test | Result |
|---|---|
| `<script>` inside the SVG | **blocked** — never runs |
| External `<image href="https://…">` | **blocked — browser draws a broken-image icon** |
| `@import` of a web font | **blocked** — falls back to the next font |
| HTML inside `<foreignObject>` | **renders** (in Chrome) |

---

## Capability matrix — what runs in each engine

[`docs/CAPABILITY-MATRIX.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/CAPABILITY-MATRIX.md) is generated by `tools/matrix/analyze.py` from captures made by `tools/matrix/capture.mjs` — do not edit by hand. Every cell was checked by loading `docs/techniques/GALLERY.md` **inside GitHub's rendered page** in each engine, at 1280px and 390px, in dark and light, scoring animation with eight frames 0.73s apart and boundary tests with pixel reads. Engines: **Chromium 153, Firefox 155, WebKit 26.6** (Safari's engine — not iOS Safari or the GitHub mobile app, which are covered by manual checks). Sample technology versions current as of the capture run; the method is designed to be re-run.

### Techniques

| | Chromium | Firefox | WebKit (Safari's engine) |
|---|---|---|---|
| `bars.svg` | ✓ animates | ✓ animates | ✓ animates |
| `css-keyframes.svg` | ✓ animates | ✓ animates | ✓ animates |
| `gauge.svg` | ✓ animates | ✓ animates | ✓ animates |
| `glow.svg` | ✓ animates | ✓ animates | ✓ animates |
| `gradient-shimmer.svg` | ✓ animates | ✓ animates | ✓ animates |
| `gradient-transform.svg` | ✓ animates | ✓ animates | ✓ **no motion** |
| `grain.svg` | ✓ | ✓ | ✓ |
| `mask-reveal.svg` | ✓ animates | ✓ animates | ✓ animates |
| `particles.svg` | ✓ animates | ✓ animates | ✓ animates |
| `smil-draw.svg` | ✓ animates | ✓ animates | ✓ animates |
| `smil-motion.svg` | ✓ animates | ✓ animates | ✓ animates |
| `stroke-draw.svg` | ✓ animates | ✓ animates | ✓ animates |
| `terminal.svg` | ✓ animates | ✓ animates | ✓ animates |
| `textpath.svg` | ✓ animates | ✓ animates | ✓ animates |
| `typing.svg` | ✓ animates | ✓ animates | ✓ animates |

**All fifteen techniques animate in all three engines, with one exception: WebKit never animates `gradientTransform`** — the only engine difference the whole research found. `grain.svg` is static by design in every column.

### Theme switching (dark scheme → light scheme)

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| `<picture>` + `prefers-color-scheme` | dark → light | dark → light | dark → light |
| `#gh-dark-mode-only` / `#gh-light-mode-only` | dark → light | dark → light | dark → light |
| `@media` inside the SVG | dark → light | dark → light | dark → light |

### Reduced motion

`@media (prefers-reduced-motion: reduce)` **never applies inside an SVG referenced as an image** — none of the three engines. A `<picture>` source gated on it does work, in all three, because the host page evaluates the query and GitHub's sanitizer keeps the attribute. Method and counts: [`docs/research/REDUCED-MOTION.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/REDUCED-MOTION.md).

### Boundary tests

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| `<script>` inside the SVG | blocked | blocked | blocked |
| External `<image>` | blocked — browser draws a broken-image icon | blocked — nothing drawn | inconsistent |
| `@import` web font | blocked | blocked | blocked |
| HTML in `<foreignObject>` | renders | renders | inconsistent |

### How long an update takes to show

Measured by `tools/matrix/cache_probe.py`: push a new version of a committed SVG, then poll until it's served. A profile README embeds images by branch path, so the branch URL is what visitors see.

| Round | Branch URL (what a README uses) | Commit-pinned URL | Cache header |
|---|---|---|---|
| 1 | 302.2s | 5.9s | `max-age=300` |
| 2 | 303.2s | 4.8s | `max-age=300` |

Polled every 10s from one location on 2026-09-21: a pushed change takes about five minutes to appear (the CDN's `max-age=300`), while a URL pinned to the commit is fresh within seconds but has to be rewritten into the README on every update. **Wait five minutes before judging a change** — half of "my SVG didn't update" is this.

### Phone layout

The phone column measured 309px on a real profile page (Chromium, true mobile emulation — see `docs/survey/FINDINGS.md`). Firefox has no mobile emulation mode, so its 390px pass is a narrow desktop viewport.

### Not testable here — check by hand

iOS Safari and the GitHub mobile apps can't be driven from a desktop machine. The gallery is built so each answer is visible by eye — open it on the device and read it off:

| Check | What you should see if it works |
|---|---|
| Animation | The dot moves along its curve; the ring spins; stars twinkle |
| `<picture>` theming | Switch the device between dark and light: the card label changes between "DARK variant" and "LIGHT variant" |
| In-SVG theming | "Theme-aware SVG" card background follows the device theme |
| Script test | Panel is **green** (red would mean scripts ran) |
| External image | A "?" or a broken-image icon, not a photo |
| `<foreignObject>` | A purple "HTML" pill next to "inside SVG"; a blank card means unsupported |
| `<details>` | The collapsed block at the bottom expands on tap |

Until someone runs it, these cells stay **unverified** — say so rather than extrapolating from WebKit.

---

## Open research tracks

[`docs/TRACKS.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/TRACKS.md): the six phases of PLAN-V2 are done; these are the questions that work left open, each minted from something the research could not answer at the time, plus the tools the findings imply. Standing rule: **no claim without a citation, a measurement, or an `UNVERIFIED` tag.**

| # | Track | Status |
|---|---|---|
| 1 | Does a relative `srcset` resolve on a profile page? | **done** |
| 2 | Does `prefers-reduced-motion` reach an SVG in secure animated mode? | **done** |
| 3 | Alt text and accessibility across 10,782 images | **done** |
| 4 | `profile-lint` — every measured rule as a checker | **done** |
| 5 | Narrow the iOS unknown with an iPhone-emulated WebKit pass | **done** |
| 6 | Can a `<picture>` source be gated on **width**? | **done** |
| 7 | Package profile-lint so other people can run it | todo |
| 8 | A five-minute real-device checklist | **built — needs a phone** |

### Track 1 · Does a relative `srcset` resolve on a profile page? — **Yes.** [`RELATIVE-SRCSET.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/RELATIVE-SRCSET.md)

Verified live on 33 real profiles. The claim that it fails — carried from the archived v1 research and repeated in the skill with an `UNVERIFIED` tag — is false.

**Why it stayed open.** Profile pages resolve relative markdown paths against a different base than repo pages, so the concern was plausible. Testing it the obvious way means editing a live profile README, which nobody was going to do to someone's account. That left it unverified through Phases 2–6, and made the built profile use absolute URLs.

**How it was answered without editing anything** — two read-only passes:

- **Corpus pass** (`tools/research/srcset.py`): the Phase 1 survey had recorded, for 442 profiles, both what the markdown declared and what the browser actually loaded on the live page. 34 profiles declared a `<picture>` dark source with a relative path — 197 such sources once width-gated mobile sources are excluded. **174 (88%) served exactly the declared file.**
- **Live pass** (`tools/research/srcset_live.py`): the 33 of those 34 still using a relative dark srcset today, loaded fresh at 1280px dark, reading each `<picture>`'s `currentSrc`:

| Result | Profiles |
|---|--:|
| Dark file served — relative path resolved | **32** |
| Reported mismatch | 1 |

The single mismatch is the tool's, not the platform's: SirAllap's first relative dark source is `header-m-dark.svg`, a `max-width` mobile variant that correctly does not apply at 1280px, and the page served `header-dark.svg` as it should. **33 of 33 behave correctly.**

**Corrections this forces:** the skill's `platform-facts.md` carried this as an UNVERIFIED failure — now a verified success; and `svg-recipes.md`, `banner-craft.md`, `SKILL.md` and `docs/PROFILE.md` all justified absolute URLs with "relative can fail on a profile page" — the justification was wrong. **The recommendation does not change, but its reason does:** use absolute `raw.githubusercontent.com` URLs because they are unambiguous, work identically in a repo README and a profile README, and survive the file being viewed anywhere else — not because relative paths break. A profile that uses relative paths is not carrying a bug.

**One real failure found along the way.** Not the one being looked for. Xalzeroph's `<picture>` blocks set the `<img>` fallback to the **light** file, and at survey time the dark-scheme capture showed four of them serving that light file *broken*. The lesson generalises: the `<img>` src is not a formality, it's what every client that ignores `<source>` will fetch, so it should point at the variant you'd rather have seen — and it must exist. (That profile has since switched to absolute URLs with cache-busting query strings, and now serves its dark files correctly.)

**Method note.** The corpus pass's first run reported 23 failures — all of them width-conditioned sources that correctly don't load at desktop width: a bug in the classifier, fixed before anything was written down. Recorded "for the same reason the survey records its corrections: the measurement was wrong first."

### Track 2 · Does `prefers-reduced-motion` reach an SVG? — **No.** [`REDUCED-MOTION.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/REDUCED-MOTION.md)

**Three findings:**

1. **The media query never applies inside an SVG referenced as an image.** Not in Chromium, not in Firefox, not in WebKit. A `@media (prefers-reduced-motion: reduce)` block in an SVG is dead code.
2. **`prefers-color-scheme` *does* apply in the same place, in all three.** So this isn't "image documents ignore media queries" — it's specific to the reduced-motion feature, which is what makes the mistake so easy.
3. **A `<picture>` source gated on reduced motion works**, because the host page evaluates it. GitHub's sanitizer keeps the attribute. This is the only way found to honour the preference in a README.

**What people are shipping** — re-fetching every SVG the survey recorded as animated (`tools/research/reduced_motion_survey.py`, 1,863 of 1,871 still reachable):

| | |
|---|--:|
| Animated SVGs carrying a `prefers-reduced-motion` guard | **369** (19.8%) |
| Distinct profiles behind them | **26** |
| Profiles with any animated SVG | 273 |
| So: profiles that tried to respect the preference | **9.5%** |

The file count is skewed by a few prolific authors — Xalzeroph alone accounts for 72 files, sepahead 36, harkirat-data and umang-eng 32 each. "These are the most conscientious profiles in the corpus, and the guard does nothing."

**How it was tested.** *Isolated* (a 60×60 SVG whose only behaviour is `fill: green`, turning red if the query applies, referenced from a `data:` URL; two contexts per engine, identical except for the emulated preference, compared by screenshot):

| Engine | `prefers-reduced-motion` | `prefers-color-scheme` (control) |
|---|---|---|
| Chromium 153 | no effect | **applied** |
| Firefox 155 | no effect | **applied** |
| WebKit 26.6 | no effect | **applied** |

The control is the point: the same mechanism, same file, same harness changes the image when the feature is `prefers-color-scheme`, so a null result on reduced motion is the browser's behaviour, not the test failing.

*On GitHub* (`tools/matrix/capture.mjs`, now taking a `REDUCED` environment variable and any `PAGE`): three fixtures in [reduced-motion-gallery.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/reduced-motion-gallery.md) — a CSS keyframe animation with the guard, a SMIL animation with the same guard, and a version that tries to hide the animated layer and show a still one. Captured in all three engines with and without the preference. **All three kept moving in every engine, in both states.** The layer-swap trick fails for the same reason: the query it depends on never matches. Then the `<picture>` test, reading which file each engine actually loaded:

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| no preference | `rm-motion.svg` | `rm-motion.svg` | `rm-motion.svg` |
| `reduce` | **`rm-still.svg`** | **`rm-still.svg`** | **`rm-still.svg`** |

**The recipe that works:**

```html
<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-still.svg">
  <img alt="…" src="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner.svg" width="600">
</picture>
```

Combining it with dark/light means four files and ordered sources — the first matching `<source>` wins, so the reduced-motion ones go first:

```html
<picture>
  <source media="(prefers-reduced-motion: reduce) and (prefers-color-scheme: dark)"  srcset=".../banner-still-dark.svg">
  <source media="(prefers-reduced-motion: reduce)"                                   srcset=".../banner-still-light.svg">
  <source media="(prefers-color-scheme: dark)"                                       srcset=".../banner-dark.svg">
  <img src=".../banner-light.svg" alt="…" width="600">
</picture>
```

Cheaper alternative, and often the better one: **don't animate the thing that would need a still variant.** A design whose first frame is already the finished composition — the rule the profile build follows — degrades to a still image for free.

**Method note.** The first version of the isolated test read the pixel back through a canvas and reported "ignored" for Firefox on *both* features — a false negative, because Firefox blocks reading an SVG-backed canvas, so the probe couldn't distinguish "query didn't apply" from "couldn't look". Caught by the control disagreeing with the Phase 3 matrix, replaced with screenshot comparison. *"Any tool that reports a negative it cannot distinguish from a failure to measure is not a measurement."*

### Track 3 · Alt text and accessibility across 10,782 images — [`ALT-TEXT.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/ALT-TEXT.md)

The survey measured whether a card can be *read*. This asks whether it can be reached at all by someone who can't see it — and finds the genre's second structural failure, after the phone.

**The shape of the problem.** An SVG card puts its words inside an image; markdown text reflows and is read aloud, a card's text is pixels. The only channel back out is `alt` — and that is measured, not assumed: an `<img>` pointing at an SVG declaring `role="img"`, an `aria-label`, `<title>` **and** `<desc>` exposes an accessible name of `""` in Chromium's accessibility tree. **Nothing inside the file crosses the boundary.**

| What the `<img>` had | Accessible name |
|---|---|
| SVG with `role`, `aria-label`, `<title>`, `<desc>`; no `alt` | `""` |
| The same SVG, `alt="ALT ON THE IMG TAG"` | `"ALT ON THE IMG TAG"` |
| The same SVG, `alt=""` | not in the tree at all (decorative, correct) |

**What the 446 profiles do** (re-parsed from live READMEs, `tools/research/alt_text.py`, 439 reachable; badges counted separately because a shield with `alt=""` is correct):

| Class | Non-badge images | Share |
|---|--:|--:|
| **absent** — no `alt` attribute | 2,258 | **34.2%** |
| **empty** — `alt=""` | 653 | 9.9% |
| **filename** — the alt is the file name | 389 | 5.9% |
| **generic** — one or two words like "banner", "gif" | 137 | 2.1% |
| descriptive — anything actually written | 3,173 | 48.0% |

Narrowed to where it matters most — SVG cards ≥200px wide the survey measured as carrying text, i.e. the ones whose content exists nowhere else:

| Class | Text-bearing cards | Share |
|---|--:|--:|
| absent | 765 | 30.3% |
| empty | 189 | 7.5% |
| filename | 43 | 1.7% |
| generic | 84 | 3.3% |
| descriptive | 1,446 | 57.2% |

**954 cards — 37.8% — put text on screen and offer no way to hear it.** The 127 filename and generic ones are arguably worse: they occupy the slot where a description should be, so nothing flags them as missing. By cohort, hand-made profiles do markedly better: **57.5% descriptive** in the code-search cohort vs **31.1%** in the curated one — "the same split as the phone-legibility finding, but inverted: people building their own SVGs write more alt text and smaller type." Per profile: **61 profiles describe nothing at all** (curated 32, search 29).

**Rules this justifies:**

1. **Every content image gets a real `alt`** — write what the card *says*, not what it is: `"LinuxWeb: real Alpine Linux in a browser tab"`, never `"banner"` or `"project card"`.
2. **`alt=""` is correct for decoration** (divider, wave, a badge whose text is also in the markdown beside it) and wrong for anything carrying information; the 189 text-bearing cards using it are not being deliberate.
3. **Don't bother labelling inside the SVG** — `<title>`, `<desc>`, `aria-label`, `role="img"` don't cross into the host page. Harmless, never a substitute.
4. **If the alt is hard to write, the card is carrying too much** — an alt you can't summarise in a sentence is a sign the information belongs in markdown, where it is readable, reflowable and searchable anyway.

**Method and its limits.** "Descriptive" means only *not obviously junk*, so 48% and 57.2% are **ceilings**, not achievements; the failure classes (absent, empty, filename, generic) are exact, which is why the findings lean on those. The accessibility-tree measurement is Chromium's; Firefox and WebKit expose trees through platform APIs that can't be read from this harness, so whether they agree is **UNVERIFIED** — though the alt-only channel is what the HTML spec requires of a replaced element, so disagreement would be surprising.

### Track 5 · Narrow the iOS unknown with an iPhone-emulated WebKit pass — [`IOS.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/IOS.md)

**What was run:** WebKit 26.6 with **actual iPhone device emulation** rather than a narrow window — an iOS 18 Safari user agent, `deviceScaleFactor: 3`, `isMobile`, touch (`DEVICE=iphone` in `tools/matrix/capture.mjs`); the full technique gallery, both schemes, on GitHub's own rendered page.

| | Emulated iPhone (WebKit) | Desktop WebKit |
|---|---|---|
| Techniques rendered | 22 of 23 | 22 of 23 |
| Animating | 13 | 13 |
| Not animating | `gradient-transform.svg` | `gradient-transform.svg` |
| Images failing to load | none | none |
| `<picture>` theming | dark → `theme-picture-dark.svg`, light → `theme-picture-light.svg` | same |
| `#gh-dark-mode-only` fragments | both files present, fragment-selected | same |
| In-SVG `@media` theming | card differs between schemes | same |
| README column | 324px (repo blob page; a profile page's is 309px) | 831px |

**Nothing changed under iPhone emulation.** Touch emulation doesn't alter any of it — none of these techniques depends on input.

**What is still unknown, precisely:** (1) **iOS Safari's own behaviour on top of WebKit**, notably **Low Power Mode**, which is documented to throttle animation — a profile that depends on motion to be legible could be still on a phone saving battery, one more argument for a first frame that is already the whole composition; (2) **the GitHub mobile apps**, which render READMEs in native views with their own markdown support — whether `<picture>` theming, SMIL or `<details>` behave there is genuinely untested; (3) **real device rasterisation** — subpixel text at 3× on a physical panel, which is what actually decides whether 11px is readable in the hand.

*"It would have been easy to run the emulated pass and write 'verified on iOS'. The emulator is Safari's engine on a desktop OS with an iPhone's metrics — close enough to rule out engine differences, not close enough to speak for the device. The distinction is the whole point of the matrix."*

### Track 6 · Can a `<picture>` source be gated on **width**? — **Yes.** [`WIDTH-GATED.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/WIDTH-GATED.md)

They work — in Chromium, Firefox and WebKit, on GitHub's rendered page. A README can serve a different SVG to a phone than to a desktop, which means the survey's largest finding stops being a trade-off and becomes a choice.

**Why this matters.** The survey's headline: **55% of 1,730 SVG cards have their largest text under 11px on a phone, and 90% of those are perfectly legible at full size** — they fail only because a 900- or 1200-unit canvas is squeezed into a 309px column. Until now the advice was to pick a side; `docs/DIRECTION.md` decided by capping the profile's viewBox at 600 units. With a width-gated source there is no compromise:

```html
<picture>
  <source media="(max-width: 600px)" srcset=".../card-phone.svg">
  <img src=".../card.svg" alt="…" width="900">
</picture>
```

The same card, drawn twice: 900 units for the desktop column, 309 units for the phone, where a 13-unit label renders at exactly 13px.

| | 900-unit canvas | 309-unit canvas |
|---|---|---|
| 26-unit body text at 309px | **8.9px** — illegible | — |
| 13-unit body text at 390px column | — | **13px** — comfortable |

**The measurement.** Fixture: [width-gallery.md](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/width-gallery.md), one `<picture>` with a `(max-width: 600px)` source, loaded on github.com in each engine at both widths, reading which file was actually served:

| | 1280px | 390px |
|---|---|---|
| Chromium 153 | `w-desktop.svg` | **`w-phone.svg`** |
| Firefox 155 | `w-desktop.svg` | **`w-phone.svg`** |
| WebKit 26.6 | `w-desktop.svg` | **`w-phone.svg`** |

Measured container: 861px at 1280, 324px at 390 (repo blob page; a profile page's column is 309px). The query is on the **viewport**, not the container, so a 600px breakpoint sits comfortably between the two. The survey had already seen the mechanism in the wild — Xalzeroph and SirAllap ship `-mobile-` and `-m-` variants behind `max-width` sources — and Track 1 saw those sources correctly *not* apply at desktop width; this closes the other half: they do apply on a phone.

**What it costs:**

- **File count multiplies.** Width × theme is four files per card; adding the reduced-motion variant makes eight. Generate them, never hand-maintain them — one content source, one script.
- **Source order is significant.** The first matching `<source>` wins, so the most specific combinations go first:

```html
<source media="(max-width: 600px) and (prefers-color-scheme: dark)"  srcset=".../card-phone-dark.svg">
<source media="(max-width: 600px)"                                   srcset=".../card-phone-light.svg">
<source media="(prefers-color-scheme: dark)"                         srcset=".../card-dark.svg">
<img src=".../card-light.svg" alt="…" width="900">
```

- **The `<img>` fallback is what a non-`<picture>` renderer gets** — the GitHub mobile apps' native views among them. If the fallback is the wide desktop file, those readers get the illegible one. Two defensible choices: make the fallback the phone variant and let desktop readers see a small card, or keep the desktop file and accept the risk. **There is no option that is right everywhere.**
- **It is still two drawings.** Not a scale factor — a phone canvas wants fewer words, not the same words smaller. Treating it as "export at another size" reproduces the original problem.

**What this does not change.** The legibility floor still governs each variant (a 309-unit canvas with 8-unit text fails exactly as before), and markdown still beats both — real text reflows, is searchable, reaches a screen reader. "This widens what an SVG can do safely; it doesn't make SVG the right place for prose."

**The profile built in Phase 5 doesn't need this:** a 600-unit canvas clears the floor at 309px with 11.9px to spare, and one file per theme is easier to verify. The option is documented for a design that wants a larger desktop canvas than 600 units — which the DIRECTION.md trade-off previously ruled out on evidence that has now moved.

### Track 7 · Package profile-lint — **todo**

It currently runs from a checkout of this repository. A composite GitHub Action, or a single file with no imports from `tools/survey/`, would let anyone point it at their profile. "Worth doing only once the rules have settled."

### Track 8 · A five-minute real-device checklist — **built, needs a phone** [`PHONE-CHECK.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/PHONE-CHECK.md)

Track 5 left three things emulation cannot answer — iOS Low Power Mode, the GitHub mobile apps' native renderers, real 3× rasterisation — "all three answerable by one person with a phone in a few minutes, if the gallery is laid out so each answer is a yes/no you can read off." Built: five cards, each drawn in a 309-unit canvas so it obeys the rule it tests, with a table to fill in. **It cannot be completed from a desktop machine**; it needs someone to open it on a phone, in the browser and in the GitHub app, with Low Power Mode and Reduce Motion toggled.

---

## Legibility math and banner craft

The survey's headline failure is mechanical, not aesthetic. From `references/measured-constraints.md` and `references/banner-craft.md` of the skill (measured 2026-09-21 against `github.com`; treat the numbers as perishable and the method as durable).

### The three numbers

| Viewport | README column |
|---|---|
| 1920px desktop | **846px** (caps here; wider viewports don't widen the column) |
| 1280px laptop | **831px** |
| 390px phone | **309px** — iPhone-class, **the binding constraint** |

Images are hard-capped to the container: an image with `naturalWidth: 854` rendered at `846` — clamped, never overflow. **309px is the number that kills banners.** Published figures disagree (830px, 894px in blog posts): 830 is this same measurement at a ~1280 viewport; 894 appears to be a repo README or an older layout — profile and repo README containers are not identical.

Measurement method (re-runnable):

```js
const art = document.querySelector('.js-profile-readme article.markdown-body')
         || document.querySelector('article.markdown-body');
JSON.stringify({
  viewport: window.innerWidth,
  contentWidth: Math.round(art.getBoundingClientRect().width)
});
```

### The legibility formula — apply before drawing anything

An SVG scales as a unit; text shrinks with the viewBox. For text at size `F` in a viewBox of width `W`, rendered into a column of width `R`:

```
effective_px = F × (R / W)          F_min = target_px × W / R
```

**11px is the floor for supporting text, 13px for anything that must be read.** For a 1200-wide viewBox that means **F ≥ 43 units** for phone legibility — far larger than it looks in a design tool, and why most banners fail. A 600-unit viewBox needs only F ≥ 21.4; the arithmetic stops fighting you.

Four ways out, in order:

1. **Shrink the viewBox, not the type.** Design at roughly the real display width — simplest, one file per theme, enough for most designs.
2. **Cut the text.** A name and one line beats four lines nobody can read. Put the detail in markdown, where it reflows.
3. **Draw it twice and gate on width** — verified in all three engines (Track 6): a 900-unit desktop canvas *and* a 309-unit phone canvas where 13 units is 13px. Multiplies files (width × theme × motion) — generate them, never hand-maintain them; the `<img>` fallback is what any renderer ignoring `<source>` gets.
4. **Accept desktop-only** for one decorative line, deliberately — never for the name.

**Enforce it in code:** a generator should refuse to emit an SVG whose smallest text would fall below the floor; a working example is `check()` in `tools/direction/build.py`. *"A rule you have to remember is a rule you will forget on the last card."*

**SVG does not need 2× dimensions for retina.** It is resolution independent — the viewBox is a coordinate system, not a resolution. That advice is for PNG/JPG, and following it is what produces 2400px viewBoxes with 20px type.

### The banner worksheet

The banner is the only element with no competition for attention, and the only one read at two wildly different sizes. Height on screen is `846 / ratio` desktop, `309 / ratio` mobile:

| Ratio | Desktop height | Mobile height | Verdict |
|---|---|---|---|
| 5.0 : 1 (1200×240) | 169px | **62px** | Too short on mobile to hold two lines |
| 4.0 : 1 (1200×300) | 212px | 77px | Workable, tight |
| 3.0 : 1 (900×300) | 282px | 103px | **Good default.** Two lines breathe |
| 2.5 : 1 (900×360) | 338px | 124px | Generous; risks pushing content below fold |
| 2.0 : 1 | 423px | 155px | Only for image-led, text-light designs |

**Default to 3:1 with a 900-unit viewBox** — ~103px of mobile height, enough for a name and one supporting line, without eating the desktop fold. A 900-unit viewBox also improves the legibility ratio: mobile needs F ≥ 32 rather than F ≥ 43, "roughly 25% more effective type size for free, purely by choosing a smaller coordinate system."

The worksheet, filled before drawing (`W` = viewBox width):

```
W = ______

Mobile floor   (11px @ R=309):  F_min = 11 × W / 309 = ______
Desktop floor  (11px @ R=846):  F_min = 11 × W / 846 = ______

Element          Size (units)   Mobile px    Desktop px   OK?
name             ______         ______       ______
role / headline  ______         ______       ______
supporting line  ______         ______       ______
```

- For `W = 900`: mobile floor **32**, desktop floor **12**.
- For `W = 1200`: mobile floor **43**, desktop floor **16**.

*"Any row below its mobile floor is a decision, not an accident. Either enlarge it, cut it, or consciously accept it is desktop-only decoration."*

### Type scale that survives the squeeze

At a 900-unit viewBox:

| Role | Units | Mobile px | Desktop px |
|---|---|---|---|
| Name | 64 | 22 | 60 |
| Role / headline | 34 | 12 | 32 |
| Supporting line | 32 | 11 | 30 |

The ratio between name and supporting text is **2:1, not the 4:1 you would use in print** — *"wide dynamic range in type does not survive downscaling; the small end falls off a cliff. Compress the scale and create hierarchy with weight, colour, and space instead of size."* Hierarchy without size: weight (800 against 400 reads at 11px), colour/value, space (generous leading), a 4-unit accent strip.

Composition rules: **left-align** (centred text collapses badly at mobile height); safe margin ~4% of viewBox width; **nothing critical in the right third** (first thing to feel crowded; decorative elements belong there); avoid fine detail — hairlines below ~1.5 units and grid patterns below ~20 units turn into mud or moiré at 309px. Colour: two files served with `<picture>`; an in-SVG `@media` works but buys nothing and is harder to check; check contrast at the *rendered* size — thin type at 11px needs more contrast than the same type at 60px, WCAG AA (4.5:1) a floor not a target; GitHub's dark canvas is near `#0d1117`, light is `#ffffff`.

Motion on a banner: *"The banner is read in about one second. Animation that takes longer than that to make its point is never seen."* Looping motion is visible the entire time someone reads the page below — prefer a single settle on load or a very slow ambient drift. *"Animation cannot respond to `prefers-reduced-motion` reliably here. Assume it always plays, for everyone, forever. If that would bother you, do not add it."*

Generated vs static: *"Generate only if a value genuinely changes."* If generating, the output must be byte-identical when inputs are unchanged — timestamps, unordered dict iteration, floating-point formatting and random gradient ids break this and produce a commit on every run forever. Pin them.

---

## The reusable skill — `github-profile-readme`

The whole research is packaged as an agent skill at [`skills/github-profile-readme/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/skills/github-profile-readme): `SKILL.md` plus five references (`evidence.md`, `platform-facts.md`, `measured-constraints.md`, `banner-craft.md`, `svg-recipes.md`), with `docs/PROFILE.md` as the worked end-to-end example (design rules, six generated cards, measurement confirming 11.9px smallest text on a phone, built by `tools/profile/build.py`).

Its frontmatter description defines the trigger: *"Use when designing, building, reviewing or debugging a GitHub profile README (the username/username repo) or any README banner, hero image, stats card, or generated SVG asset…"* — built on the 446-profile survey and the three-engine captures, covering what actually breaks, the measured container widths and legibility math, which SVG features survive GitHub's renderer, theme switching, cache timing, and how to verify a design instead of guessing.

Governing principle, stated in the skill itself:

> Most profile-README advice is aesthetic and unsourced. This skill is built from measurement… Two reference files carry the evidence. Read the relevant one before asserting anything. **If a claim appears in neither, say it is unverified. Fluent writing that sounds researched is the failure mode this skill exists to prevent.**

### Start here: the four failures

| Failure | Rate in the wild | The rule that avoids it |
|---|---|---|
| A broken image on the page | **41%** | Commit every image to the repo. Committed images load 99% of the time; the public github-readme-stats instance loads **0%** and is still embedded in 24% of profiles. |
| SVG text illegible on a phone | **55%** of 1,730 cards | Run the legibility formula on every card, not just the banner. 90% of failures are legible at full size and die only in the 309px column. |
| Badge wall | **42%** of profiles | Badges are not information. Fifteen shields read as noise and each is a Camo fetch. |
| No dark/light | 80% don't | Two files behind `<picture>`. |

*"Hand-made cards fail the phone **more** than generator output (63% vs 37%) — being the designer is not protection, it is the risk."*

### The dead-service evidence (`references/evidence.md`)

Every number from the survey: 446 personal profile READMEs (187 from `awesome-github-profile-readme`, 259 found by code search for SVG animation primitives in `username/username` repos), 10,782 images fetched, 442 profiles loaded in headless Chrome.

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

309 broken URLs are free-tier Vercel deployments switched off (`DEPLOYMENT_PAUSED` / `DEPLOYMENT_DISABLED` in the response headers). 24% of profiles still embed the dead github-readme-stats instance — *"its repository metadata says active; its README says unmaintained; the service returns 503. **Only fetching the image tells the truth.**"* Images committed to the profile repo loaded **99%** of the time: "the argument for generate-and-commit over embed-a-service, and the single highest-value rule in this skill."

Other survey facts carried in evidence.md: tables — 21% of profiles put two or more images in one; on a phone GitHub either squeezes (640px cards measured at **76px** in a four-column table, 9% of profiles) or keeps them full width and scrolls the table sideways (7%); *"both outcomes are worse than one column, so don't lay out with tables."* Illegible by service — lowlighter/metrics 83%, github-profile-summary-cards 60%, readme-typing-svg 54%, self-hosted github-readme-stats 20%; shields.io's 53% is by design (`for-the-badge` sets 10px text on every device); desktop not immune — 15% of profiles have an illegible card at 1280px. Generated or templated — of 1,506 bespoke SVGs, 192 are Action output identifiable by generator signatures; byte-identical copying rare (29 files) but structural templates are not (four profiles share one "Index Nº 001" layout). A recent push means nothing — 54% run Actions, median "last pushed" 1.1 months ago while human content is years old. And the gap worth aiming at: *"Nobody in the 446 is both visually ambitious **and** legible at 309px… That space is empty, and it is where a profile should be designed"* — see `docs/survey/SHORTLIST.md` for the fifteen standouts.

### What survives inside the image

Referencing an SVG via `<img>` or `![]()` puts the browser in the SVG spec's **secure animated mode**: declarative animation runs, everything interactive or external does not. Verified identically in all three engines (full tables above):

| | |
|---|---|
| SMIL, CSS `@keyframes`, masks, stroke-dash, `textPath`, filters | **all animate, all engines** |
| `gradientTransform` animation | **WebKit never animates it** — animate `x1`/`x2` or stop offsets |
| `<script>`, event handlers, hover, tooltips | blocked |
| `@import`ed web fonts | blocked |
| External `<image>` href | blocked — and Chromium **paints a broken-image icon** |
| Inline `<svg>` in markdown | stripped by the sanitizer |
| `@media (prefers-reduced-motion)` inside the SVG | **never applies** — gate a `<picture>` source instead |

*"This also caught out the survey tooling once, which read the icon as a successful load."*

### Fonts: your web font is not loading

An SVG referenced as an image cannot load anything external, so `font-family: 'JetBrains Mono', monospace` renders as JetBrains Mono only for viewers who already have it installed — everyone else silently gets the next entry, with no error. **The stack is therefore the design decision, not the first name in it.**

- **Design for the fallback stack**, e.g. `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` (`ui-monospace` is the real token; `-apple-system-ui-monospace` is not valid CSS).
- **Embed a subset as base64** for full fidelity — subset aggressively, a whole font is 100KB+. 13 surveyed profiles do this.
- **Convert text to paths** for a wordmark. Perfect, unsearchable, painful to regenerate.

Because the face varies per viewer, never let a layout depend on exact text width — where it must (typing effect, right-aligned label), use `textLength`.

### Dark and light, plus asset routing

```html
<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-light.svg">
  <img alt="describe the content, not the word banner" src="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-dark.svg" width="600">
</picture>
```

Prefer `<picture>` because one theme per file is easy to verify. Use absolute raw URLs — identical in a repo README, a profile README, anywhere the markdown is read — while noting relative paths also resolve correctly on profile pages (33 of 33 checked), so don't treat someone else's relative srcset as a bug. Point the `<img>` fallback at the variant you'd rather have seen, and make sure that file exists.

Routing, measured from the live DOM: repo-relative `./assets/banner-dark.svg` → rewritten to `https://github.com/{owner}/{repo}/raw/main/...` (hostname `github.com`, **not** Camo); third-party → `camo.githubusercontent.com/<hmac>/<hex-encoded-url>`. Camo URLs are HMAC-SHA1 signed — *"you cannot hand-construct or warm a Camo URL"*; the only lever is changing the source URL (new URL → new digest → fresh fetch). Camo caches external responses far more aggressively and does not reliably self-heal when the origin recovers. `raw.githubusercontent.com` serves `Cache-Control: max-age=300` with Fastly in front; open question, not settled: whether Fastly soft-purges on push or distant edges serve the full 300s.

### The process, as written in the skill

1. **Measure the target first.** 846 / 309. Write down the viewBox, run the formula, only then draw.
2. **Design the first frame as the finished composition.** Anything that starts at `opacity="0"` and animates in is invisible to every static renderer — and was caught doing exactly that, at phone width, during this research.
3. **Commit every asset.** Generated and committed, never rented.
4. **Respect reduced motion where the page can see it.** A guard inside the SVG does nothing; a `<source media="(prefers-reduced-motion: reduce)">` pointing at a still file works in all three engines. Best of all, design so the still frame is the whole composition and the question is moot.
5. **Decide generated vs static honestly.** CI only if a value genuinely changes; a cron rewriting identical bytes is noise. If generated, run it twice with no input change and diff — non-deterministic output (timestamps, dict order, random ids) means a commit every run, forever.
6. **Verify on GitHub, not locally.** Push to a branch, open the rendered page, and measure: each image's rendered width, its smallest text × (width ÷ viewBox), both schemes, 390px and 1280px. *"Local preview shows you neither the sanitizer, nor the column width, nor a broken image."*
7. **Wait five minutes.** `max-age=300`: a pushed change takes ~302s to appear on a branch URL. Half of "my SVG didn't update" is this.

### Anti-patterns

- A 1200px+ viewBox with sub-40 type — the most common failure there is.
- Third-party image services on the critical path of a first impression.
- Badge walls; fake metrics; claims that outrun the evidence. *"All three read as dishonest to exactly the people who look closely."*
- Tables used for layout.
- `<script>` or `onclick` in an SVG — stripped, always.
- Copying a stat card because it is popular. *"The most-copied one has been dead for months and its repository metadata still says 'active'."*

### Copy-paste recipes (`references/svg-recipes.md`)

Patterns verified to render inside a GitHub README; all use system font stacks and declarative-only features. The reference banner — 900×300 (3:1), mobile-legible, every type size clearing the 32-unit floor for a 900 viewBox:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" width="900" height="300"
     role="img" aria-label="Ada Lovelace, distributed systems engineer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0"   stop-color="#111827"/>
      <stop offset="1"   stop-color="#0b1020"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#38bdf8"/>
      <stop offset="1" stop-color="#818cf8"/>
    </linearGradient>
  </defs>

  <rect width="900" height="300" rx="14" fill="url(#bg)"/>
  <rect y="292" width="900" height="8" fill="url(#accent)"/>

  <!-- 4% safe margin = 36 units -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
    <text x="36" y="132" font-size="64" font-weight="800" fill="#f8fafc">Ada Lovelace</text>
    <text x="36" y="186" font-size="34" font-weight="600" fill="#38bdf8">Distributed Systems Engineer</text>
    <text x="36" y="232" font-size="32" font-weight="400" fill="#94a3b8">Consensus · Storage · Observability</text>
  </g>
</svg>
```

Check: at mobile (R=309, W=900, scale 0.343) → **22px / 12px / 11px**, all legible; at desktop (R=846, scale 0.94) → 60px / 32px / 30px.

Dual-theme wiring (absolute raw URLs *"because they are unambiguous everywhere — not because relative ones break"*):

```html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/USER/REPO/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)"
          srcset="https://raw.githubusercontent.com/USER/REPO/main/assets/banner-light.svg">
  <img src="https://raw.githubusercontent.com/USER/REPO/main/assets/banner-dark.svg"
       alt="Ada Lovelace — distributed systems engineer" width="100%">
</picture>
```

Ambient motion that does not irritate — a slow accent drift, 8s cycle, low contrast:

```svg
<rect y="292" width="900" height="8" fill="url(#accent)">
  <animate attributeName="opacity"
           values="0.55; 1; 0.55" dur="8s" repeatCount="indefinite"/>
</rect>
```

A one-shot settle — plays once, then rests, usually the better choice (`fill="freeze"` holds the final state instead of snapping back):

```svg
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" dur="0.6s" fill="freeze"/>
  <!-- content -->
</g>
```

Progress / meter bar, with the clamp rule (`width = min(track, track * value / 100)` — a value over 100% will overflow the track otherwise):

```svg
<g>
  <rect x="36" y="200" width="300" height="6" rx="3" fill="#1e293b"/>
  <rect x="36" y="200" width="222" height="6" rx="3" fill="#38bdf8"/>
  <text x="348" y="207" font-size="32" fill="#94a3b8"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">74%</text>
</g>
```

Determinism guard for generated SVGs:

```bash
python harness/engine.py build && cp assets/banner-dark.svg /tmp/a.svg
python harness/engine.py build && diff -q /tmp/a.svg assets/banner-dark.svg
```

Common sources of drift, all of which must be pinned: a timestamp rendered into the SVG (exclude it, or quantise to the day); `json.load` into a plain dict then iterating (sort keys); float formatting `0.30000000000000004` (round and format explicitly); random or uuid gradient/filter ids (derive them from content instead); `set` iteration order (sort before emitting).

Accessibility recipe: `<svg role="img" aria-label="…">` **plus a real `alt` on the `<img>`** — screen readers get the `alt`, the `aria-label` covers direct navigation to the file. *"Do not write `alt="banner"` — describe the content."*

---

## Mechanical enforcement — `profile-lint`

Track 4, [`docs/research/PROFILE-LINT.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/PROFILE-LINT.md): six phases of measurement, expressed as thirteen rules that run against any profile in about a minute.

```
python tools/lint/profile_lint.py torvalds
python tools/lint/profile_lint.py --file profile/README.md --owner me --repo me
python tools/lint/profile_lint.py --json user1 user2     # for CI
```

It fetches the README, resolves and fetches every image, reads the source of the profile's own committed SVGs, and reports findings at three levels. Exit status is 1 if anything error-level fired, so it can gate a workflow. *"Every finding carries the measurement behind it — a linter that can't say why is an opinion with an exit code."*

### The rules

| Rule | Level | What it catches | Evidence |
|---|---|---|---|
| `broken-image` | error | any image that doesn't load | 41% of profiles have one |
| `dead-service` | error | images from services measured as dead | the most-copied stat card loads 0% |
| `phone-illegible` | error / warn | error when the *largest* text falls below 11px at 309px; warn when only some text does | 55% of 1,730 cards fail |
| `image-table` | error | two or more images in one table | cards measured at 76px on a phone |
| `missing-alt` | error | an SVG that carries text with absent, empty, filename or generic alt | 37.8% of text cards |
| `stripped-script` | error | `<script>` inside an SVG | blocked in all three engines |
| `external-ref` | error / warn | external `<image>` or `@import` inside an SVG | blocked; Chromium draws a broken icon |
| `no-theme` | warn | no dark/light switching | 80% ship one theme |
| `badge-wall` | warn | more than half the images are badges | 42% of profiles |
| `dead-motion-guard` | warn | `prefers-reduced-motion` *inside* an SVG | never applies — Track 2 |
| `webkit-gradient` | warn | animated `gradientTransform` | WebKit never animates it |
| `hidden-first-frame` | warn | elements at `opacity="0"` that animate in | a static renderer shows nothing |
| `unguarded-motion` | note | animation with no still alternative | Track 2's `<picture>` recipe |

### Does it agree with the survey it came from?

*"A linter derived from a 446-profile survey should, run over profiles from that survey, reproduce its rates."* 80 sampled at random (`tools/lint/validate.py`, fixed seed), 79 reachable:

| Rule | profile-lint | The survey |
|---|--:|--:|
| `broken-image` | 43% | 41% |
| `badge-wall` | 46% | 42% |
| `no-theme` | 77% | 80% |
| `image-table` | 18% | 21% |
| `phone-illegible` (error) | 7% curated / 74% search | 15% / 70% |

*"Close enough to trust, and the two don't measure identically: the survey rendered each page in a real browser, the linter reads the markdown and the files. They are independent implementations of the same rules agreeing, which is the useful part."*

**Two bugs the validation caught**, both found because the numbers disagreed:

- *Badge walls under-reported (32% vs 42%).* The linter's badge pattern covered four hosts; the survey counts badges **and icons** — skill-icons, simple-icons, devicon, visitor counters, donation buttons. Widened to match, and the rate moved to 46%.
- *Illegibility wildly over-reported (63% vs ~40% expected).* The linter was measuring shields.io badges, whose `for-the-badge` style sets 10px text on every device. Every profile with one badge fired. The survey excludes badges from its 1,730 cards for exactly this reason; so does the linter now, which brought the cohort rates in line.

*"Both were the linter being wrong, not the survey. Neither would have been visible without a number to check against — which is the argument for validating a tool against the data that produced it."*

### Calibration: does it flag the good profiles?

If every exemplary profile drowns in errors, the severities are wrong. Four from the shortlist:

| Profile | What fired |
|---|---|
| marcizhu | `no-theme` only |
| BrunnerLivio | one table, one alt, one legibility |
| ayxn07 | 31 × `dead-motion-guard`, no errors |
| JGit705 | 9 × `phone-illegible`, 9 × `dead-motion-guard` |

*"This matches the survey's own reading: JGit705 is the profile the survey singled out for turning to specks on a phone, and ayxn07 is one of the conscientious ones from Track 2 whose reduced-motion guards do nothing. The linter reaches those conclusions from the files alone."* The profile built in Phase 5 passes every rule.

### Using it in CI

```yaml
- run: python tools/lint/profile_lint.py ${{ github.repository_owner }}
```

*"Worth saying plainly: the rules are about whether a page **works**, not whether it is any good. Nothing here can tell you the writing is dull or the design is derivative."*

### The five-minute phone check

Track 5's companion, [`docs/research/PHONE-CHECK.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/research/PHONE-CHECK.md): three things a desktop cannot answer — **iOS Low Power Mode**, the **GitHub mobile apps'** native renderers, and whether 11px is really readable on a physical screen — all answerable by one person with a phone. Open the page once in the browser and once in the GitHub app. Every card is drawn in a 309-unit canvas so one unit is one pixel in the README column: *"the checklist obeys the rule it is testing."*

1. **Does animation run?** — `docs/research/examples/chk-motion.svg` (a blue bar sweeping left and right). Moving in the browser → SMIL runs in iOS Safari; moving in the app → the app renders animation too. Then turn on Low Power Mode (Settings → Battery), reload, still moving?
2. **Does `<picture>` theming work?** — `chk-theme-dark.svg` / `chk-theme-light.svg` served via `(prefers-color-scheme: dark)`. The card names the file it is showing; *"if it says LIGHT on a dark phone, `<picture>` isn't being honoured."*
3. **Is reduced motion honoured?** — `chk-rm-still.svg` via `media="(prefers-reduced-motion: reduce)"` with `chk-rm-motion.svg` as fallback. Turn on Settings → Accessibility → Motion → Reduce Motion, reload, read the card — *"the only one that works"* mechanism from Track 2, tested against iOS and the app.
4. **Is a phone-specific file served?** — `w-phone.svg` via `media="(max-width: 600px)"` over `w-desktop.svg`. Should read **PHONE VARIANT** on a phone; in the GitHub app, whichever appears tells you whether the app evaluates `media` or falls back to the `<img>`.
5. **Where does text actually stop being readable?** — `chk-floor.svg` with text at 20, 15, 13, 11, 9 and 7 units. *"The 11px floor came from measurement plus judgement. Read this at arm's length and find the line where it stops being comfortable — that is the floor for real."*

Record table to close the last unverified rows of CAPABILITY-MATRIX.md:

| Check | Browser | GitHub app | Low Power Mode |
|---|---|---|---|
| 1 · animation runs | | | |
| 2 · `<picture>` theming | | | — |
| 3 · reduced motion honoured | | | — |
| 4 · width-gated source | | | — |
| 5 · lowest comfortable size | | | — |

---

## Gaps and what stays UNVERIFIED

The standing rule of this repo — from `docs/PLAN-V2.md` and repeated in `docs/TRACKS.md`: *"no claim without a citation, a measurement, or an `UNVERIFIED` tag."* What that leaves open:

### Not testable from a desktop

iOS Safari and the GitHub mobile apps cannot be driven headlessly, so the matrix ends with a hand-check list (`docs/CAPABILITY-MATRIX.md`, final section). Gallery answers readable by eye:

| Check | What you should see if it works |
|---|---|
| Animation | The dot moves along its curve; the ring spins; stars twinkle |
| `<picture>` theming | Switch the device between dark and light: the card label changes between "DARK variant" and "LIGHT variant" |
| In-SVG theming | "Theme-aware SVG" card background follows the device theme |
| Script test | Panel is **green** (red would mean scripts ran) |
| External image | A "?" or a broken-image icon, not a photo |
| `<foreignObject>` | A purple "HTML" pill next to "inside SVG"; a blank card means unsupported |
| `<details>` | The collapsed block at the bottom expands on tap |

*"Record results in this table when checked; until then these cells are **unverified**."* `docs/research/PHONE-CHECK.md` (Track 8) is the five-card version with a fill-in record table.

### The iOS residue, stated precisely

Track 5's iPhone-emulated WebKit pass found *nothing changes* — same 13 animating, same one WebKit exception, all three theme mechanisms working — but emulation leaves three genuinely unknown (from `docs/research/IOS.md`):

1. **iOS Low Power Mode** — unknown whether it stops SMIL/CSS animation.
2. **The GitHub mobile apps'** native renderers (iOS/Android) — unknown whether they evaluate `<picture>` `media`, render animation, or honour Reduce Motion; whether the app evaluates `media` or falls back to `<img>` is exactly what check 4 discriminates.
3. **Real 3× rasterisation** — whether fine SVG detail holds at physical device scale.

Emulator ≠ device: *"it won't close the question — it will shrink it, and the residue should be stated precisely rather than left blank."*

### Known mechanism limits, not bugs to fix

- **Nothing can read GitHub's own theme setting from inside an image.** All three theme mechanisms key off the OS `prefers-color-scheme`; a light-OS/GitHub-dark user sees the light asset on a dark page. Unfixable from markdown.
- **Firefox has no mobile emulation mode**, so the 390px Firefox pass in the matrix is a narrow desktop viewport — only the Chromium phone pass is true mobile emulation (see `docs/survey/FINDINGS.md`).
- **Published container-width figures disagree** with ours (830px, 894px): 830 is the same measurement at a ~1280 viewport; 894 appears to be a repo README or an older layout — profile and repo README containers are not identical, and this repo's numbers are the profile ones.
- **Cache behaviour**: `max-age=300` is measured (302.2s / 303.2s branch rounds); whether Fastly soft-purges on push or distant edges serve the full 300s is an open question, not settled. Camo URLs cannot be hand-constructed or warmed — the only lever is changing the source URL.
- **Alt-text ceiling**: "anything actually written" (48.0% / 57.2%) is a classifier ceiling, not a score; whether the true figure for useful alt text is higher or lower is unknown by an unknown margin, and where the `<img>`-alt and in-document channels agree is `UNVERIFIED` (`docs/research/ALT-TEXT.md`).
- **`rel="noopener noreferrer"`**, GIF animation under reduced motion, and other sub-questions tagged in TRACKS stay tagged.

### Open work

| # | Track | Status |
|---|---|---|
| 7 | Package profile-lint (composite GitHub Action, or a single file with no imports from `tools/survey/`) so anyone can point it at their profile | **todo** — "worth doing only once the rules have settled" |
| 8 | The five-minute real-device checklist | **built — needs a phone** (`docs/research/PHONE-CHECK.md`) |

Tracks 1–6 are closed (relative `srcset` 33/33, reduced motion dead in-SVG / alive via `<picture>`, alt text 37.8%, profile-lint built and validated, iOS narrowed, width-gating verified ×3 engines).

### Perishable numbers

Every measurement here is a date-stamped observation — widths, dead-service rates, `max-age=300` timings, engine versions (Chromium 153, Firefox 155, WebKit 26.6), the survey corpus. Treat the numbers as evidence of a *method*, re-measure before quoting them as current, and keep the skill's own discipline: *"If a claim appears in neither [evidence.md nor platform-facts.md], say it is unverified. Fluent writing that sounds researched is the failure mode this skill exists to prevent."*

---

*Part 02 of the compilation. Sibling part: [`01-survey-shortlist.md`](01-survey-shortlist.md). Sources: [`docs/techniques/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/docs/techniques) (CATALOGUE, VERIFIED, GALLERY), [`docs/CAPABILITY-MATRIX.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/CAPABILITY-MATRIX.md), [`docs/TRACKS.md`](https://github.com/hammadshakeelai/github-profile-blueprint/blob/v2/research/docs/TRACKS.md), [`docs/research/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/docs/research), [`skills/github-profile-readme/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/skills/github-profile-readme), [`docs/survey/`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/v2/research/docs/survey).*
