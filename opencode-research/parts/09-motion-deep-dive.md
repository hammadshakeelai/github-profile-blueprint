# Part 09 — Motion Deep-Dive: Real Animation Code That Runs in GitHub READMEs

This part is code, not opinion. Every snippet below was pulled verbatim from a **live profile
SVG** fetched on 2026-09-26 (`raw.githubusercontent.com`) or from this repo's own verified
examples in `docs/techniques/examples/`. Nothing here is invented; where a pattern was adapted
into a recipe, it says so.

**The ground rule** (`docs/techniques/CATALOGUE.md:17-20`): an SVG in a README is displayed as
an image, which browsers run in *secure animated mode* — declarative animation runs; scripts,
interaction and external resources don't. So "animation works here" means: SMIL `<animate>`,
CSS `@keyframes` inside `<style>`, `stroke-dashoffset` drawing, masks, clip paths — all of it
runs. JavaScript does not, and neither does anything you can touch.

**How the ratings work.** Each technique gets a `/5` for *reuse value*, not beauty:

| Score | Meaning |
|---|---|
| **5/5** | Runs in all three engines, compact, adapts without surgery |
| **4/5** | Runs everywhere but needs tuning (file size, phone legibility, data) |
| **3/5** | Works, but fragile — Safari caveats, illegible at 390px, or heavy |
| **2/5** | Marginal — keep only if you can't get the effect any other way |

**Source key.** Files fetched this session and cached locally carry their GitHub URL at each
entry. Repo-internal examples (`gauge.svg`, `bars.svg`, …) are marked *repo-verified* — they
were captured frame-by-frame in Chromium, Firefox and WebKit (`docs/CAPABILITY-MATRIX.md:11-25`).

---

## 1. The baseline: what may move, and what never will

Before the techniques, the four hard edges every recipe below respects — all measured, not
assumed (`docs/CAPABILITY-MATRIX.md`):

| Check | Result | Line |
|---|---|---|
| SMIL, CSS keyframes, stroke-draw, glow, masks, typing, textPath, gauges, bars, particles, terminal | ✓ animate in Chromium, Firefox **and** WebKit | 11–25 |
| `gradientTransform` animation | ✓ Chromium, ✓ Firefox, **WebKit: no motion** | 16 |
| `<script>` inside the SVG | blocked in all three | 43 |
| External `<image>` / `@import` web font | blocked in all three | 44–46 |
| `@media (prefers-reduced-motion: reduce)` inside the SVG | **never applies** — none of the engines | 37 |
| Anything interactive (hover, click) | impossible — "Nothing inside an SVG image is interactive" (`CATALOGUE.md:397`) | — |
| Push → visible delay | ~5 minutes (CDN `max-age=300`); commit-pinned URL ~5s | 57 |

Two of these bite in the wild. Several real profile SVGs ship
`@media (prefers-reduced-motion: reduce)` blocks — umang-eng, ayxn, krishna, sepahead, skymly
all do — and **on GitHub those blocks are dead weight**: the query never reaches an image-context
SVG. Keep them anyway (they're free, and the file works correctly if you reuse it on a real
website), but never let them be the only thing standing between a visitor and your animation.

---

## 2. Typewriter / typing

### 2.1 TextPath length-grow typing (the `readme-typing-svg` family) — 4/5

The most-copied typing effect on GitHub (`CATALOGUE.md:227` — 87 profiles via
DenverCoder1's `readme-typing-svg`, plus hand-rolled copies). Mechanism: a `<path>` whose `d`
grows left-to-right with SMIL, text rides it with `<textPath>`, so letters appear one at a time
like a cursor is typing them. Multi-line versions chain the animations by ID —
`begin="0s;d2.end"` — line 2 starts when line 3's loop ends, and the whole block repeats.

Verbatim, 3-line cycle — `https://github.com/liss-bot/liss-bot/blob/main/intro.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     viewBox="0 0 450 50" style="background-color: #00000000;" width="450px" height="50px">
  <path id="path0">
    <!-- Single line -->
    <animate id="d0" attributeName="d" begin="0s;d2.end" dur="5000ms" fill="remove"
             values="m0,25 h0 ; m0,25 h450 ; m0,25 h450 ; m0,25 h0"
             keyTimes="0;0.8;0.8;1"/>
  </path>
  <text font-family="&quot;monospace&quot;, monospace" fill="#C4045D" font-size="20"
        dominant-baseline="auto" x="0%" text-anchor="start">
    <textPath xlink:href="#path0">Hello 👋</textPath>
  </text>
  <path id="path1">
    <animate id="d1" attributeName="d" begin="d0.end" dur="5000ms" fill="remove"
             values="m0,25 h0 ; m0,25 h450 ; m0,25 h450 ; m0,25 h0"
             keyTimes="0;0.8;0.8;1"/>
  </path>
  <text font-family="&quot;monospace&quot;, monospace" fill="#C4045D" font-size="20"
        dominant-baseline="auto" x="0%" text-anchor="start">
    <textPath xlink:href="#path1">I'm @Liss-Bot...</textPath>
  </text>
  <path id="path2">
    <animate id="d2" attributeName="d" begin="d1.end" dur="5000ms" fill="remove"
             values="m0,25 h0 ; m0,25 h450 ; m0,25 h450 ; m0,25 h0"
             keyTimes="0;0.8;0.8;1"/>
  </path>
  <text font-family="&quot;monospace&quot;, monospace" fill="#C4045D" font-size="20"
        dominant-baseline="auto" x="0%" text-anchor="start">
    <textPath xlink:href="#path2">and I'm automating things</textPath>
  </text>
</svg>
```

The `values` quartet is the trick: grow → hold (80% of the duration is readable) → snap shut →
restart. `fill="remove"` snaps the path back to zero between cycles so the line clears instead of
ghosting. The same pattern appears in single-line form with `fill="freeze"` in
`rroy233`, `happyren-name.svg` and `ankit-bye.svg` (3-line outro chain, same `begin="…end"` idiom).

- **Runs on:** SMIL — Chromium, Firefox, WebKit (all ✓ animate).
- **Gotchas:** the path `h450` must be at least as long as your text at its font size, or the tail
  clips; `letter-spacing` inflates text beyond the path; emoji (👋) render but shift metrics
  between engines — put them mid-line, not at the clip edge.
- **Rating:** 4/5 — the workhorse, but the path length is hand-tuned per string.

### 2.2 CSS width-clip typing with `steps()` — 4/5

Pure CSS alternative: a `width: 0 → 715px` keyframe on a wrapper, quantized by
`steps(65, end)` so width jumps one character at a time; a sibling cursor rect rides the same
step count and a separate `blink` flickers it. sepahead runs **three lines in sequence** off one
15s master timeline by splitting the percentage space (0–33% / 33–66% / 66–100%).

Verbatim (trimmed to line 1 of 3) — `https://github.com/sepahead/sepahead/blob/main/assets/hero-light.svg`:

```css
.role-cur { visibility: hidden; fill: #1f2328; }
.sweep { transform: translateX(0); animation: sweep 3.2s linear infinite; }
@keyframes sweep { from { transform: translateX(-100px); } to { transform: translateX(620px); } }
@keyframes blink { 0%, 50% { opacity: 1; } 50.01%, 100% { opacity: 0; } }

.seq1 { animation: seq1 15s linear infinite; }
.type1 { animation: type1 15s steps(65, end) infinite; }
.cur1 { animation: cursor1 15s steps(65, end) infinite, blink 1s steps(1) infinite; }
@keyframes seq1 {
  0%, 0% { opacity: 0; }
  0.0667%, 30.6667% { opacity: 1; }
  32.6667%, 100% { opacity: 0; }
}
@keyframes type1 {
  0%, 0% { width: 0; }
  12%, 32.6667% { width: 715px; }
  33.2667%, 100% { width: 0; }
}
@keyframes cursor1 {
  0%, 0% { visibility: hidden; transform: translateX(-715px); }
  0.0667% { visibility: visible; transform: translateX(-715px); }
  12%, 30.6667% { visibility: visible; transform: translateX(0); }
  32.6667%, 100% { visibility: hidden; transform: translateX(0); }
}
```

- **Runs on:** CSS keyframes in SVG — all three engines ✓.
- **Gotchas:** `steps(N)` N must equal the character count of your string (65 above, 70 on line 3
  — they recount per line); the wrapper needs `overflow: hidden; white-space: nowrap;` and an
  inline-block display for `width` to clip; font metrics change the pixel width, so measure with
  the actual font.
- **Rating:** 4/5 — no SMIL dependency, but every new string re-tunes three numbers.

### 2.3 Line-by-line discrete reveal (SMIL, no clip) — 4/5

The cheapest "typing" that still reads as boot text: each line is a `<text>` with `opacity="0"`
and an `<animate>` that fires at a later `begin`, `fill="freeze"` so it stays. From
`gitbanner.svg` (`https://github.com/…/gitbanner.svg`), three lines at 0.5s / 1.2s / 1.9s:

```svg
<text x="20" y="130" font-family="monospace" font-size="12" fill="#6272a4" opacity="0">
  <tspan x="20" dy="0">Initializing profile data...</tspan>
  <animate attributeName="opacity" values="0;1" begin="0.5s" dur="0.3s" fill="freeze" />
</text>
<!-- next line: begin="1.2s" … then begin="1.9s" -->
```

- **Runs on:** SMIL — all three engines.
- **Gotchas:** nothing animates back — reload replays the whole sequence from the top (that's
  usually what you want for a boot screen); the lines are static afterwards, so this is the
  zero-cost option for phone layouts.
- **Rating:** 4/5.

---

## 3. Blinking cursor — 5/5

Two bytes of keyframes power most cursors on GitHub. ayxn's card, verbatim (entire `<style>`):

```css
@keyframes blink{50%{opacity:0}}
.blink{animation:blink 1s steps(1) infinite}
@keyframes nudge{50%{transform:translateX(5px)}}
.nudge{animation:nudge 1.4s ease-in-out infinite}
@keyframes flow{to{stroke-dashoffset:-8}}
.flow{stroke-dasharray:4 4;animation:flow .8s linear infinite}
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
```

The same file's `.nudge` (a 5px horizontal twitch) and `.flow` (dashed line marching via
`stroke-dashoffset: -8` on a `4 4` dash) ride along — three ambient micro-motions in one line
each. sepahead composes `blink 1s steps(1) infinite` *onto* the cursor's travel animation as a
second `animation` value (see §2.2 `.cur1`).

- **Runs on:** CSS — all three engines.
- **Gotchas:** `steps(1)` matters — without it the default `ease` makes a slow crossfade instead
  of a snap. The reduced-motion block here is inert on GitHub (§1).
- **Rating:** 5/5 — smallest effect-per-byte in the whole catalogue.

---

## 4. Entrance choreography & stagger

### 4.1 CSS class delays — draw, rise, fade — 5/5

umang-eng's header is the cleanest entrance system found in the wild: three verbs
(`.draw`, `.rise`, `.fade`) plus a delay ladder `.a1…a6`, and every element declares verb +
delay as two classes. Verbatim from
`https://raw.githubusercontent.com/umang-eng/umang-eng/main/assets/header-v1.svg`:

```css
.draw { stroke-dasharray: 1000; stroke-dashoffset: 1000; animation: draw 1.4s cubic-bezier(.6,0,.2,1) forwards; }
@keyframes draw { to { stroke-dashoffset: 0; } }
.rise { opacity: 0; animation: rise .9s cubic-bezier(.2,.7,.2,1) forwards; }
@keyframes rise { from { opacity:0;transform:translateY(12px); } to { opacity:1;transform:translateY(0); } }
.fade { opacity: 0; animation: fade .7s ease forwards; }
@keyframes fade { to { opacity: 1; } }
.a1{animation-delay:.2s} .a2{animation-delay:.5s} .a3{animation-delay:.9s} .a4{animation-delay:1.2s} .a5{animation-delay:1.4s} .a6{animation-delay:1.7s}
```

Used inline as `<line class="draw a1" …/>`, `<g class="rise a2">…</g>`, `<g class="fade a3">…</g>`:

```svg
<line class="draw a1" x1="48" y1="58" x2="952" y2="58" stroke="var(--rule)" stroke-width="1"/>
<g class="rise a2">
  <text fill="var(--bone)" class="mono" x="46" y="176" font-size="72" letter-spacing="-2">Umang Bhut</text>
</g>
<g class="fade a3">
  <text fill="var(--muted)" class="mono" x="48" y="214" font-size="19">Aspiring Data Scientist / AI-ML Engineer — Ahmedabad, India.</text>
</g>
```

Two extras worth stealing: custom properties + `@media (prefers-color-scheme: dark)` to re-theme
the same file (35 profiles do this, `CATALOGUE.md:332`), and a rotating highlight
(`.rot` with staggered delays `.r1…r4` on a 12s loop) that pops different footer labels in turn.

- **Runs on:** CSS — all three engines. `forwards` holds the end state.
- **Gotchas:** `stroke-dasharray: 1000` must exceed the line's real length (or use
  `pathLength` — §5); delays are absolute, so a long ladder (here up to 1.7s) delays the whole
  card's completeness — keep the tail under ~2s for READMEs.
- **Rating:** 5/5 — the reference pattern for entrance sequences.

### 4.2 One-shot SMIL fade with `fill="freeze"` — 4/5

jorex-glow fades three text blocks in, staggered by `begin`, and *stays* (SMIL's equivalent of
`forwards`). Verbatim from `https://raw.githubusercontent.com/Jorexdev/Jorexdev/main/img/jorex-glow-v7.svg`:

```svg
<text x="493" y="68" font-family="'DM Sans', sans-serif" font-size="46" font-weight="700"
      fill="#ffffff" text-anchor="end" opacity="0">Hola, soy
  <animate attributeName="opacity" from="0" to="1" dur="1s" fill="freeze"/>
</text>
<text x="450" y="106" font-family="'DM Mono', monospace" font-size="13"
      fill="#A3B067" letter-spacing="2" text-anchor="middle" opacity="0">// software analyst · divulgador · speaker
  <animate attributeName="opacity" from="0" to="1" dur="1s" begin="0.6s" fill="freeze"/>
</text>
```

JackLuciano's header does the same with an entrance *sequence* — height grows, opacity fades,
`stroke-dashoffset` draws, all with staggered `begin` and `fill="freeze"` — plus 20 SMIL
animations total in one file.

- **Runs on:** SMIL — all three engines.
- **Gotchas:** SMIL has no `forwards`; `fill="freeze"` *is* the hold — omit it and the element
  snaps back to its first value when the animation ends.
- **Rating:** 4/5.

### 4.3 rise / ping / route / pop — 4/5

JGit705's hero, verbatim (entire `<style>`), from
`https://raw.githubusercontent.com/jgit705/jgit705/main/assets/hero.svg`:

```css
.rise{animation:rise 1s cubic-bezier(.16,1,.3,1) both}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.6s ease-out infinite}
@keyframes ping{0%{opacity:.75;transform:scale(1)}80%,100%{opacity:0;transform:scale(3.4)}}
.route{stroke-dasharray:1;stroke-dashoffset:0;animation:route 1.6s cubic-bezier(.65,0,.35,1) both}
@keyframes route{from{stroke-dashoffset:1}}
.pop{transform-box:fill-box;transform-origin:center;animation:pop .7s cubic-bezier(.34,1.56,.64,1) both}
@keyframes pop{from{opacity:0;transform:scale(.2)}}
```

Note `.route`'s use of `pathLength="1"` (declared on the element, `CATALOGUE.md:298` mentions
the `pathLength="100"` gauge variant): dash maths collapse to fractions — offset `1` = fully
hidden, `0` = fully drawn, no measuring. And `both` covers both directions of the hold, so
`rise`/`pop` stay at their end state without an explicit `forwards`.

- **Runs on:** CSS — all three engines (this file was captured across engines).
- **Gotchas:** any CSS `transform: scale()` on an SVG element needs
  `transform-box: fill-box; transform-origin: center` or it scales from the SVG origin and flies
  off-canvas (`CATALOGUE.md:79`: "…orbits instead of spinning").
- **Rating:** 4/5.

---

## 5. Line drawing (stroke-dash reveal) — 5/5

The signature effect of the genre — 93 profiles (`CATALOGUE.md:104`). Mechanics: set
`stroke-dasharray` = path length, `stroke-dashoffset` = same, then animate offset → 0. umang's
`.draw` (§4.1) is the canonical CSS form; JGit705's `.route` (§4.3) is the `pathLength` form.
The repo-verified SMIL form, from `docs/techniques/examples/smil-draw.svg` (✓ all engines):

```svg
<path d="M20 60 C 60 10, 140 10, 180 60" fill="none" stroke="#3fb950" stroke-width="3"
      stroke-dasharray="240" stroke-dashoffset="240">
  <animate attributeName="stroke-dashoffset" from="240" to="0" dur="2s"
           begin="0.2s" fill="freeze" repeatCount="1"/>
</path>
```

And the perpetual variant — a dashed line *marching*, not drawing — is ayxn's `.flow`
(`stroke-dasharray:4 4; animation: flow .8s linear infinite` with `to{stroke-dashoffset:-8}`,
§3): negative offsets travel toward the path start.

- **Runs on:** CSS and SMIL — all three engines ✓ (`stroke-draw.svg`, `smil-draw.svg`).
- **Gotchas:** measure the path or set `pathLength`; loops need `repeatCount="indefinite"` /
  `infinite`; animated `stroke-dashoffset` on a *filter output* is the one Safari flake to watch
  in complex files — test the gallery on a real device (`docs/CAPABILITY-MATRIX.md:65`).
- **Rating:** 5/5.

---

## 6. Orbit & rotate — 5/5

Three rings, three speeds, one moon each — SMIL `animateTransform type="rotate"` on a wrapping
`<g>`, circle offset to `cx=120 cy=0`. Verbatim from JackLuciano's header
(`https://raw.githubusercontent.com/jackluciano/jackluciano/main/assets/header.svg`):

```svg
<!-- right-side orbit motif -->
<g transform="translate(810,150)" filter="url(#hsoft)">
  <ellipse rx="120" ry="120" fill="none" stroke="#ffb454" stroke-opacity=".12"/>
  <ellipse rx="84"  ry="84"  fill="none" stroke="#ff7a5c" stroke-opacity=".12"/>
  <ellipse rx="48"  ry="48"  fill="none" stroke="#ffd9a0" stroke-opacity=".12"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="24s" repeatCount="indefinite"/>
    <circle cx="120" cy="0" r="3.5" fill="#ffb454"/>
  </g>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="16s" repeatCount="indefinite"/>
    <circle cx="84" cy="0" r="3" fill="#ff7a5c"/>
  </g>
  <!-- third: from="120" to="480", dur="9s" -->
</g>
```

Because the rotate is on the wrapper `<g>` (which carries no other transform), the parent's
`translate(810,150)` keeps the rotation centered on the motif — no `transform-box` needed, which
is exactly why SMIL orbits survive where naive CSS `transform: rotate()` spins the whole card
around the top-left corner.

- **Runs on:** SMIL — all three engines (the CSS route needs
  `transform-box: fill-box; transform-origin: center`, `CATALOGUE.md:79`).
- **Gotchas:** three different durations is the trick — equal durations look mechanical; keep
  periods ≥ 9s so a screenshot never looks "stuck mid-orbit".
- **Rating:** 5/5.

---

## 7. Scroll, marquee & travelling pulses

### 7.1 Seamless wave scroll — 5/5

An over-drawn path (drawn from `-1200` to `2400` — twice the viewBox past each edge) translates
one full wavelength per loop, and a gradient mask fades both ends so the seam never shows.
Verbatim from `https://github.com/10ishk/10ishk/blob/main/assets/wave.svg`:

```svg
<defs>
  <linearGradient id="waveFade" x1="0%" y1="0%" x2="100%" y2="0%">
    <stop offset="0%"   stop-color="#8b8b8b" stop-opacity="0" />
    <stop offset="15%"  stop-color="#8b8b8b" stop-opacity="0.7" />
    <stop offset="50%"  stop-color="#8b8b8b" stop-opacity="0.9" />
    <stop offset="85%"  stop-color="#8b8b8b" stop-opacity="0.7" />
    <stop offset="100%" stop-color="#8b8b8b" stop-opacity="0" />
  </linearGradient>
  <mask id="waveMask">
    <rect x="0" y="0" width="1200" height="40" fill="url(#waveFade)" />
  </mask>
</defs>
<g mask="url(#waveMask)">
  <path d="M -1200 20 C -1150 5, -1050 5, -1000 20 C … 2250 35, 2350 35, 2400 20"
        fill="none" stroke="#8b8b8b" stroke-width="1.5" stroke-linecap="round">
    <animateTransform attributeName="transform" type="translate" values="0 0; 1200 0"
                      dur="6s" repeatCount="indefinite" />
  </path>
</g>
```

`translate` by exactly one motif period (1200 units here) makes the loop invisible; the mask is
what keeps it from hard-cutting at the viewBox edge.

- **Runs on:** SMIL — all three engines.
- **Gotchas:** `values="0 0; 1200 0"` must equal the path's repeating period exactly, or the wave
  jumps; masks animate fine but add a layer — at 390px keep the stroke ≥1.5px or it aliases.
- **Rating:** 5/5.

### 7.2 Goo wave-strip marquee — 4/5

dhiru-banner stacks three `<use>` copies of one wave path, each on a different clock
(`3s`, `5s reverse`, `7s` at 30% opacity), and pushes them through a gooey
`feGaussianBlur + feColorMatrix` filter so the drops merge like liquid. Verbatim
(excerpts, `https://github.com/dhiru001/dhiru001`-style banner; local copy
`motion/dhiru-banner.svg`):

```css
.gooeff { filter: url(#goo); }
.wave { animation: wave 3s linear; animation-iteration-count: infinite; fill: #4447e3; }
#wave2 { animation-duration:5s; animation-direction: reverse; opacity: .6 }
#wave3 { animation-duration: 7s; opacity:.3; }
@keyframes wave { to {transform: translateX(-100%);} }
.drop { animation: drop 8.2s linear infinite normal;
        transform: translateY(25px); transform-box: fill-box; transform-origin: 50% 100%; }
.drop3 { animation-delay: -2s; animation-duration: 5.4s; }   /* negative delay = already mid-flight */
@keyframes drop {
  0%   { transform: translateY(25px); }
  30%  { transform: translateY(-10px) scale(.1); }
  30.001% { transform: translateY(25px) scale(1); }
  70%  { transform: translateY(25px); }
  100% { transform: translateY(-15px) scale(.1); }
}
```

```svg
<use id="wave3" class="wave" xlink:href="#wave" x="0" y="-2"></use>
<use id="wave2" class="wave" xlink:href="#wave" x="0" y="0"></use>
<g class="gooeff" filter="url(#goo)">
  <circle class="drop drop1" cx="95" cy="2" r="8.8"/>
  <!-- …more drops, each reusing .drop1–.drop6 delay classes -->
  <use id="wave1" class="wave" xlink:href="#wave" x="0" y="1"/>
</g>
```

Two honest notes on this file: it also ships `rect.headerRect:hover { fill: yellow; }` and
`.wave:hover` — **dead code on GitHub** (§16) — and its filter ends with `<xfeBlend …>`, a typo
for `<feBlend>`; the goo still renders because `feMerge` carries the result.

- **Runs on:** CSS + SMIL mix — all three engines; the goo filter costs the most.
- **Gotchas:** negative `animation-delay` is the standard way to desync a marquee so it isn't
  obviously looping; `transform-box: fill-box` again (§4.3); `translateX(-100%)` on a `<use>`
  refers to the *use's* bbox, not the parent — keep tiles wider than the gap.
- **Rating:** 4/5 — striking, but the filter is the heaviest thing you can put in a README SVG.

### 7.3 Falling columns (matrix rain) — 4/5

Every column is the same `<rect>`-trail translated at its own speed with a **negative `begin`**
so columns start at different phases — no CSS needed. Verbatim excerpt from
`matrix-banner.svg` (69KB, `Platane`-adjacent contribution banners):

```svg
<g>
  <animateTransform attributeName="transform" type="translate"
                    values="-512 0;0 0" dur="6.4s" repeatCount="indefinite" begin="-1.7s"/>
  <!-- …one per column: dur 6–10s, begin "-X.XXs" -->
</g>
```

- **Runs on:** SMIL — all three engines. Same desync idiom as §7.2, in SMIL form.
- **Gotchas:** one element per column inflates the file fast (that banner is 69KB); prefer
  `<use>` + `pattern` where possible.
- **Rating:** 4/5.

### 7.4 Travelling pulse / highlight sweep — 5/5

Two real profiles do the same thing: a bright segment races along a rail and *holds off-screen*
between passes, using `keyTimes` to carve "move, then park". Karthik's divider, verbatim
(`https://raw.githubusercontent.com/karthik5033/karthik5033/main/assets/custom-divider.svg`):

```svg
<rect x="0" y="6" width="800" height="2" fill="#21262d" rx="1"/>
<g filter="url(#glowY)">
  <rect x="-150" y="6" width="150" height="2" fill="url(#gradY)" rx="1">
    <animate attributeName="x" values="-150;800;800" keyTimes="0;0.5;1"
             dur="3s" repeatCount="indefinite"/>
  </rect>
  <circle cx="0" cy="7" r="2" fill="#FFFFFF">
    <animate attributeName="cx" values="0;950;950" keyTimes="0;0.5;1"
             dur="3s" repeatCount="indefinite"/>
  </circle>
</g>
<!-- second rail, right-to-left, offset in time: begin="1.5s" -->
<g filter="url(#glowB)">
  <rect x="800" y="6" width="150" height="2" fill="url(#gradB)" rx="1">
    <animate attributeName="x" values="800;-150;-150" keyTimes="0;0.5;1"
             dur="3s" repeatCount="indefinite" begin="1.5s"/>
  </rect>
  …
</g>
```

The twin pulse — same file, opposite direction, `begin="1.5s"` — turns two one-way runs into a
criss-cross. omkarrr88's "About Me" rule does the sliding-highlight variant with an opacity
gate so the bar fades in and out at the ends:

```svg
<rect x="166.0" y="27.0" width="60" height="2" rx="1" fill="#7aa2f7" opacity="0.45">
  <animate attributeName="x" from="166.0" to="840.0" dur="4.5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0;0.45;0.45;0" keyTimes="0;0.15;0.75;1"
           dur="4.5s" repeatCount="indefinite"/>
</rect>
```

- **Runs on:** SMIL — all three engines. This is also the WebKit-safe way to animate gradients:
  move the *shape* (or the `x1`/`x2` gradient attrs), never `gradientTransform` (§10).
- **Gotchas:** `keyTimes` must have the same count as `values` and always start at 0 and end at 1;
  the "park" trick (`…;800;800`) is what stops a pulse from visibly wrapping.
- **Rating:** 5/5 — the most re-usable single animation in this part.

---

## 8. Glitch — 3/5

The chromatic-aberration look: three stacked copies of the same text — red, blue (and green) —
each jittering `x`/`y`/`opacity` on its own clock, offset so the RGB channels tear apart.
Verbatim from `gitbanner.svg`:

```svg
<text x="400" y="100" font-family="Impact, Haettenschweiler, Arial Narrow Bold, sans-serif"
      font-size="38" text-anchor="middle" fill="#ff5555" opacity="0.5">
  Welcome to {Username}'s Github Profile
  <animate attributeName="x" values="400;402;397;403;400" dur="0.5s" begin="3.5s" repeatCount="indefinite"/>
  <animate attributeName="y" values="100;98;102;97;100" dur="0.35s" begin="3.5s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.5;0.0;0.6;0.0;0.5" dur="0.25s" begin="3.5s" repeatCount="indefinite"/>
</text>
<!-- Blue glitch layer: fill="#8be9fd", same animate pattern -->
<!-- Green layer: fill="#50fa7b" -->
```

The `values` array returns to its start value, so the jitter loops without drift; the three
different durations (0.5 / 0.35 / 0.25s) guarantee the layers rarely align.

- **Runs on:** SMIL — all three engines.
- **Gotchas:** **phone legibility** — jittering text at 390px is where screenshots break down;
  keep the base layer crisp at full opacity and let only the ghosts flicker; `begin="3.5s"`
  delays the whole gag until the boot sequence (§2.3) finishes.
- **Rating:** 3/5 — works everywhere, but it's the effect most likely to read as "broken image".

---

## 9. Glow pulse — 4/5

90 profiles use glow (`CATALOGUE.md:132`). The strongest form animates the *blur radius
itself* — a breathing halo. jorex-glow, verbatim:

```svg
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
  <feGaussianBlur in="SourceGraphic" result="blur">
    <animate attributeName="stdDeviation" values="2;9;2" dur="2.4s" repeatCount="indefinite"/>
  </feGaussianBlur>
  <feMerge>
    <feMergeNode in="blur"/>
    <feMergeNode in="SourceGraphic"/>
  </feMerge>
</filter>
```

Applied as `<text … fill="#A3B067" filter="url(#glow)">`. The cheaper sibling — a radar ping —
is JGit705's `.ping` (§4.3): scale one ring to 3.4× while fading it out. krishna-hero does the
same idea by animating the geometry directly in CSS keyframes:

```css
.ring{animation:ring 3.2s ease-out infinite}
@keyframes ring{0%{r:5;opacity:.85}70%{r:17;opacity:0}100%{r:17;opacity:0}}
.core{animation:core 3.2s ease-in-out infinite}
@keyframes core{0%,100%{opacity:.5}50%{opacity:1}}
```

- **Runs on:** SMIL `stdDeviation` — all three engines (this file was verified live). The CSS
  `r: 5 → 17` form animates a geometry property; it works in Chromium/Firefox — **verify on a
  real device before shipping** (WebKit has history with CSS geometry animation; the tested
  safe route is SMIL `<animate attributeName="r">`).
- **Gotchas:** animated blur is the single most expensive op in an SVG — one filtered element per
  card, not per glyph; `filter` region (`x/y/width/height`) must be widened as above or the glow
  clips to the bbox.
- **Rating:** 4/5.

---

## 10. Gradient shimmer — 4/5

Gradients are the most common technique of all — 130 profiles (`CATALOGUE.md:174`) — and the
WebKit rule decides *how* you animate them: **don't touch `gradientTransform`**
(`CAPABILITY-MATRIX.md:16` — "WebKit: no motion"; `CATALOGUE.md:190`). Three sanctioned routes,
all in real files:

1. **Animate the geometry that uses the gradient** (karthik's travelling pulse, §7.4 — the
   gradient rides a rect that moves).
2. **Animate the gradient's own coordinates** — gitbanner's metal sheen, verbatim:

```svg
<linearGradient id="metalGradient" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%"  stop-color="#ffffff" stop-opacity="0.9"/>
  <stop offset="70%" stop-color="#a0a0a0" stop-opacity="0.9"/>
  <stop offset="100%" stop-color="#808080" stop-opacity="0.7"/>
  <animate attributeName="y1" values="0%;15%;0%;10%;0%" dur="6s" repeatCount="indefinite"/>
  <animate attributeName="y2" values="100%;85%;100%;90%;100%" dur="6s" repeatCount="indefinite"/>
</linearGradient>
```

3. **Animate gradient stops / the gradient's `x1`/`x2`** — the repo's `gradient-shimmer.svg`
   (✓ all engines) and Karthik's glow rects (`fill="url(#gradY)"` sliding, §7.4).

A shimmer sheen, repo-verified minimal form:

```svg
<rect width="100%" height="40" fill="#161b22"/>
<rect width="100%" height="40" fill="url(#sheen)">
  <animate attributeName="x" values="-200;900" dur="3.2s" repeatCount="indefinite"/>
</rect>
<!-- #sheen: linearGradient x1=0 x2=1 with a transparent→white→transparent band -->
```

- **Runs on:** SMIL attribute animation of `x1`/`x2`/`y1`/`y2`/stops — all three engines;
  `gradientTransform` — Chromium and Firefox only.
- **Gotchas:** two `<rect>`s (base + sheen) is cheaper than a `filter`; sheen width ~15–20% of
  the card or it reads as a full flash.
- **Rating:** 4/5 — high impact, one hard WebKit constraint.

---

## 11. Particle drift — 4/5

Ambient particles = one shape, many clones, phase-shifted. krishna-hero's travelling dot is the
clearest real example — a single CSS keyframe path with opacity gates at both ends so it fades
in, walks the route, fades out, repeats. Verbatim:

```css
.dot{animation:trav 5.4s linear infinite}
@keyframes trav{
  0%{transform:translate(420px,62px);opacity:0}
  7%{opacity:1}
  24%{transform:translate(527px,62px)}
  46%{transform:translate(634px,110px)}
  68%{transform:translate(741px,166px)}
  92%{transform:translate(838px,110px);opacity:1}
  100%{transform:translate(838px,110px);opacity:0}
}
```

Desync comes from delay classes (`.a1…`/negative `animation-delay`, §7.2) or, in SMIL, from
**negative `begin` values** — `begin="-3.7s"` starts an animation partway through its first
cycle, which is how the repo's `particles.svg` (✓ all engines) staggers ~20 sparkles with one
definition. The repo's `grain.svg` (film grain, ✓ static) covers the static cousin — note that
"✓" with no "animates" in the matrix means it renders but doesn't move.

- **Runs on:** CSS and SMIL — all three engines.
- **Gotchas:** clone-count drives size — 10–20 particles is the sweet spot; use `<use>` of one
  `<circle>` to keep the DOM small; give every particle a different duration (6.4s, 7.1s, 9.3s)
  so the field never pulses in unison.
- **Rating:** 4/5.

---

## 12. Snake / contribution art — 5/5

Generated by Actions, everywhere: the snake game alone is 65 profiles, plus lowlighter/metrics
(17), 3D contribution graphs (12), pacman (5) (`CATALOGUE.md:316-319`). Platane/snk is the
canonical one — a ~100KB fully declarative SVG where **three parallel CSS keyframe families**
share one 104,500ms clock. Verbatim excerpts from the live output
(`https://raw.githubusercontent.com/Platane/snk/output/user-contribution-grid.svg`-style path,
fetched this session as `motion/snake.svg`):

```css
/* the head: every keyframe is a cell coordinate, timed to when it eats */
.s{shape-rendering:geometricPrecision;fill:var(--cs);
   animation:none linear 104500ms infinite}
@keyframes s0{
  0%,99.9%{transform:translate(0px,-16px)}
  0.1%{transform:translate(0px,0px)}
  0.19%{transform:translate(-16px,0px)}
  0.38%{transform:translate(-16px,32px)}
  0.48%,88.52%{transform:translate(0px,32px)}
  …}                                /* hundreds of stops = the path */

/* each body segment: scales in on X the moment it's "grown" */
.u{transform-origin:0 0;transform:scale(0,1);
   animation:none linear 104500ms infinite}
@keyframes u0{0.09%{transform:scale(0.000,1)}
  0.11%,0.47%{transform:scale(0.011,1)}
  0.49%,0.56%{transform:scale(0.022,1)}
  …}

/* each grid cell: flashes its contribution color when eaten, then rests */
.c.c0{fill:var(--c1);animation-name:c0}
@keyframes c0{0.09%{fill:var(--c1)}0.11%,100%{fill:var(--ce)}}
.c.c1{fill:var(--c3);animation-name:c1}
@keyframes c1{88.41%{fill:var(--c3)}88.43%,100%{fill:var(--ce)}}
```

The `.c` family is the contribution heatmap itself: resting cells are `--ce`, and each cell's
keyframe flashes its real level (`--c1`…`--c4`) exactly when the head passes over it. That's why
the snake "eats" your year.

- **Runs on:** CSS keyframes in SVG — all three engines ✓ (the matrix's `css-keyframes.svg`
  covers the mechanism; snk output is the 65-profile production version).
- **Gotchas:** file size (~100KB) is fine for an `<img>` but never inline it; it's a scheduled
  Action + committed output branch (survives because it's committed — survey: 93% live,
  Part 07); **phone legibility is the weak point** — contribution detail collapses under 390px,
  so treat it as decoration, not data.
- **Rating:** 5/5 — the highest-impact generated motion on the platform.

---

## 13. Gauges, meters & bars — 4/5

### 13.1 Gauge sweep — 4/5

`pathLength="100"` turns the dash length into the value itself — offset goes from 100 (empty) to
`(100 − value)` (filled), so percentages are the code (`CATALOGUE.md:298`). Repo-verified
`gauge.svg`, ✓ animates in all three engines:

```svg
<circle cx="60" cy="60" r="46" fill="none" stroke="#e6edf3" stroke-opacity=".15"
        stroke-width="10" pathLength="100"
        stroke-dasharray="100" stroke-dashoffset="100">
  <animate attributeName="stroke-dashoffset" from="100" to="12"
           dur="1.6s" begin="0.3s" fill="freeze" repeatCount="1"/>
</circle>
<!-- offset 12 = 88% filled; last 0.3s of the sweep carries an ease-out if you add calcMode="spline" -->
```

Server-telemetry gauges (itguyo's `docs/book/03-dictionary.md` family) use exactly this. The
streak-stats cards found in real profiles (rroy-streak) do the pop-in instead:
`.currstreak { animation: scale-in … }` on `font-size` — a number that *jumps* to its final size
rather than counting.

### 13.2 Bars chart — 4/5

Bars rising with a staggered `begin`, animating `height` **and** `y` together (SVG rects grow
downward from `y`, so both must move). Repo-verified `bars.svg`, ✓ all engines; used by sepahead
and JConfessor (`CATALOGUE.md:300-307`):

```svg
<rect x="20" y="90" width="24" height="10" fill="#3fb950">
  <animate attributeName="height" from="0" to="70" dur="0.9s" begin="0.2s"
           fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/>
  <animate attributeName="y"     from="90" to="20" dur="0.9s" begin="0.2s"
           fill="freeze" calcMode="spline" keySplines="0.16 1 0.3 1"/>
</rect>
<!-- next bar: begin="0.35s" … -->
```

- **Gotchas:** real data means a generator + workflow; commit the output rather than rent a
  service — hosted chart services are among the most broken embeds (Part 07); at 390px bars
  under ~6px wide read as noise.
- **Rating:** 4/5 each — solid, but real numbers need a build step.

---

## 14. Terminal boot & dot-matrix — 4/5

Two related motifs. **Terminal:** staged opacity lines (§2.3) plus a caret that blinks (§3) —
gitbanner is the full worked example (boot lines at 0.5/1.2/1.9s, then the glitch title at 3.5s).
Repo-verified `terminal.svg` ✓ animates in all three engines; JGit705's "line-by-line discrete
opacity" style is the hand-made variant. **Dot matrix:** krishna-hero's ring/core keyframes
(§9) pulse individual nodes; `matrix-banner.svg` (§7.3) is the full falling-columns treatment;
`krishMeow/Animated-Terminal-GitHub-Profile` generates the dot-matrix banner as a tool.

```css
/* caret — reuse of §3 */
@keyframes blink{50%{opacity:0}}
.caret{animation:blink 1s steps(1) infinite}
```

- **Runs on:** CSS + SMIL — all three engines.
- **Gotchas:** staged timelines (`begin="1.9s"`) mean a fresh reload replays the show — good for
  a boot screen, bad if you want content readable *immediately*; put any static essentials at
  `begin="0s"`.
- **Rating:** 4/5.

---

## 15. Waveform & path morphing — 3/5

SMIL can morph a path — animate `d` between two shapes of identical command structure. The only
*verified* shape-morph in the wild samples here is the typing family itself (§2.1's
`h0 → h450` grow/hold/shrink, plus dhiru-banner's `#nameTyping` path that grows `h0`→`h100` to
reveal text). A true wave/blob morph — one `<path>` cycling between two silhouettes — **was not
found in any live profile SVG in this pass**. The synthesized recipe below is the honest form
(SMIL supports it; it just isn't a house style yet):

```svg
<!-- RECIPE (synthesized, not observed in the wild): morph a wave between two states -->
<path id="wave" fill="none" stroke="#3fb950" stroke-width="2"
      d="M0,20 Q30,5 60,20 T120,20 T180,20 T240,20">
  <animate attributeName="d" dur="4s" repeatCount="indefinite"
           calcMode="spline"
           values="M0,20 Q30,5 60,20 T120,20 T180,20 T240,20;
                   M0,20 Q30,35 60,20 T120,20 T180,20 T240,20;
                   M0,20 Q30,5 60,20 T120,20 T180,20 T240,20"
           keyTimes="0;0.5;1" keySplines="0.4 0 0.6 1;0.4 0 0.6 1"/>
</path>
```

- **Runs on:** SMIL `d` animation — all three engines support SMIL; **test the spline timing on
  WebKit** before shipping (the matrix verifies SMIL motion, not every `calcMode` combination).
- **Gotchas:** both `values` paths must have the *same command sequence and count* or the morph
  is undefined; 10ishk's translating-wave approach (§7.1) achieves the "living wave" look with
  zero morph risk and is the better default.
- **Rating:** 3/5 — real capability, no real precedent yet.

---

## 16. Hover effects — the honest negative — n/a

**There is no hover in a README SVG.** `docs/techniques/CATALOGUE.md:397`: "Nothing inside an
SVG image is interactive." The README embeds the file as an `<img>`, browsers run it in secure
animated mode, and pointer events never reach the document — `pointer-events` cannot save you.

The wild still ships the mistake. dhiru-banner, fetched this session, contains:

```css
rect.headerRect:hover { fill: yellow; fill-opacity: 50%; }
.wave:hover { fill: #5457ff; }
.drop:hover { fill: #C9FFE5; }
```

All three rules are **dead on GitHub** — they only fire if the same file is opened directly in a
browser tab. Do not copy this. What profiles use instead (per the catalogue): entrance
animation (§4), ambient loops (§7), and *sequenced* reveals (§2/§14) — motion that happens by
itself, because nothing will ever happen to it.

---

## 17. Family-by-family scorecard

The seventeen families this part was asked to cover, with what was actually found:

| Family | Found in the wild? | Best real example | Rating |
|---|---|---|---|
| Typewriter / typing | ✓ | liss-bot, sepahead, rroy233 (§2) | 4/5 |
| Snake / contribution | ✓ | Platane/snk, 65 profiles (§12) | 5/5 |
| Line-draw | ✓ | umang `.draw`, JGit705 `.route` (§5) | 5/5 |
| Gauge / meter sweep | ✓ | `gauge.svg` repo-verified, itguyo gauges (§13.1) | 4/5 |
| Orbit / rotate | ✓ | JackLuciano triple orbit (§6) | 5/5 |
| Marquee / scroll | ✓ | 10ishk wave, dhiru goo strip, matrix rain (§7.1–7.3) | 5/5 |
| Glitch | ✓ | gitbanner RGB layers (§8) | 3/5 |
| Number ticker (no JS) | **✗ none found** | — (see §18) | n/a |
| Gradient shimmer | ✓ | gitbanner metal `y1/y2`, karthik sheen (§10) | 4/5 |
| Particle drift | ✓ | krishna `.trav`, `particles.svg` (§11) | 4/5 |
| Waveform / morph | partial | typing-path morph only (§15) | 3/5 |
| Progress bars | ✓ | `bars.svg`, stroke-dash progress (§5, §13.2) | 4/5 |
| Blinking cursor | ✓ | ayxn `.blink`, sepahead `.cur1` (§3) | 5/5 |
| Hover effects | **✗ impossible** | dead `:hover` in dhiru-banner (§16) | n/a |
| Entrance / stagger | ✓ | umang `.a1…a6`, jorex `fill="freeze"` (§4) | 5/5 |
| TextPath cycling | ✓ | liss-bot `begin="0s;d2.end"` chain (§2.1) | 4/5 |
| Dot-matrix / halftone pulse | ✓ | krishna `.ring`/`.core`, matrix rain (§9, §7.3, §14) | 4/5 |

---

## 18. What was NOT found (the gaps, stated plainly)

1. **A number ticker without JavaScript.** Two search passes and 20+ fetched files produced zero
   examples of digits counting up inside a README SVG. The reason is structural: neither SMIL nor
   CSS keyframes can change *text content* — `<text>` is immutable, so "counting" would need one
   `<text>` per digit value toggled by discrete opacity (a synthesized hack, cheap enough to write
   but never seen in use). Every live "counting number" is either generated server-side
   (github-readme-stats counters, streak-stats) or browser-side JS (which GitHub strips). The
   closest real thing: streak-stats' `.currstreak` scale-in pop (§13.1).
2. **A true text/badge marquee.** Scrolling loops exist (§7.1–7.3), but no profile ships a
   repeating strip of badges or names crossing the frame — the "marquee" family in practice is
   waves, rules and rain, not text.
3. **Hover / click / focus / drag.** Impossible by construction (§16).
4. **`prefers-reduced-motion` doing anything on GitHub.** Inert (`CAPABILITY-MATRIX.md:37`);
   five real files ship the block anyway (umang, ayxn, krishna, sepahead, skymly) — harmless
   copy-paste from website habits.
5. **A live orbit done in CSS.** Orbits in the wild are SMIL `animateTransform` (§6); the CSS
   route works but every real file reached for SMIL first — presumably because `transform-origin`
   on SVG elements is a known footgun.
6. **`observatory.svg` (adamalston.com) as an animation example.** Fetched expecting orbits;
   it's static — zero `<animate>`, zero `@keyframes`. Dropped, and worth knowing: some
   "orbital-looking" profile art is just a well-drawn still.
7. **Any JS-based SVG animation library as usable.** `oubenruing/svg-text-animate` surfaced in
   search — it generates SVGs animated by embedded scripts, which GitHub blocks
   (`CAPABILITY-MATRIX.md:43`). Generator-only, never paste its output.

---

## 19. The 2026 distribution of styles

What profiles actually run, from the catalogue's survey counts
(`docs/techniques/CATALOGUE.md`, section headers verified this session):

| Technique | Profiles | Family |
|---|--:|---|
| Gradients | 130 | §10 shimmer / static |
| SMIL animation | 129 | §2–§14 |
| CSS `@keyframes` in SVG | 101 | §3–§12 |
| Clip paths | 90 | §4/§5 reveals |
| Stroke-dash line drawing | 93 | §5 |
| Glow | 90 | §9 |
| Typing (readme-typing-svg) | 87 | §2.1 |
| `<picture>` + theme | 80 | theme switching |
| Masks | 28 | §7.1 |
| In-SVG `@media (prefers-color-scheme)` | 35 | §4.1 |
| `<foreignObject>` | 32 | risky — WebKit inconsistent |
| Text on a path | 12 | §2.1 |
| snk snake | 65 | §12 |
| lowlighter/metrics | 17 | generated |
| 3D contribution graphs | 12 | generated |
| pacman | 5 | generated |

Reading it: **SMIL and CSS keyframes are near-tied as the substrate** (129 vs 101 — most files
use both, as §7.2 and §10 show), gradients are the default dressing (130), and the "wow"
techniques split cleanly into two schools —

- **Hand-made, small, always-on** — entrance stagger, typing, line-draw, pulse sweeps. Tens of
  bytes to a few KB, authored in an editor, reused as templates. Sections 2–7, 9, 13–14 of this
  part.
- **Generated, large, scheduled** — snk (65), metrics (17), 3D graphs (12), pacman (5). Produced
  by a GitHub Action that commits the SVG, which is why they survive (93% live, Part 07) and why
  they're the worst on phones (metrics: 83% of its cards illegible at 390px).

The ecosystem around them keeps growing on the *tool* side: `Platane/snk` for snakes,
`lowlighter/metrics` for everything, `krishMeow/Animated-Terminal-GitHub-Profile` for dot-matrix
banners, `rootlinux/github-profile-svg-banner` and `cemdenizexe/github-readme-svg-hero-prompt`
for SMIL banner templates, `ryanpolasky/ryme.md` as a browser-only banner builder (its output is
a file you commit — the tool never has to stay up), plus `readme-typing-svg` (87 profiles) and
`capsule-render` for typed/animated banners. Common denominator: **they all emit declarative
SVG**, because that's the only thing GitHub renders.

And the two rules every 2026 file obeys without exception: no `gradientTransform` (WebKit shows
a frozen frame), and nothing interactive (it's an image).

---

## 20. Recipes — effect, code, gotchas

Adapted from the real files above; each is paste-ready for a committed `.svg` in your profile
repo. All are declarative — they run in the secure animated box.

### R1 — Blinking cursor (from §3)

```svg
<text x="10" y="30" font-family="monospace" font-size="20" fill="#3fb950">$ git push</text>
<rect class="caret" x="118" y="14" width="10" height="20" fill="#3fb950"/>
<style>
@keyframes blink{50%{opacity:0}}
.caret{animation:blink 1s steps(1) infinite}
</style>
```

**Gotchas:** `steps(1)` for a snap, not a fade. Position the rect by measuring your text —
monospace widths vary slightly across engines; add 2px of slack.

### R2 — Typewriter line (from §2.2)

```svg
<style>
.type{display:inline-block;overflow:hidden;white-space:nowrap;
      width:0;animation:type 3s steps(24,end) infinite alternate}
@keyframes type{to{width:288px}}
</style>
<text x="10" y="30" font-family="monospace" font-size="20" fill="#c0caf5">
  <tspan class="type">building things that ship</tspan><tspan class="caret">▍</tspan>
</text>
```

**Gotchas:** `steps` count = char count (24); width = chars × measured advance (288 = 24 × 12).
Wrap in a `<foreignObject>`-free structure — this is plain SVG `text` with a clipped `tspan`
container; test phone width before committing.

### R3 — Staggered entrance (from §4.1)

```svg
<style>
.draw{stroke-dasharray:600;stroke-dashoffset:600;animation:draw 1.2s cubic-bezier(.6,0,.2,1) forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.rise{opacity:0;animation:rise .8s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.a1{animation-delay:.15s}.a2{animation-delay:.45s}.a3{animation-delay:.75s}
</style>
<line class="draw a1" x1="20" y1="40" x2="580" y2="40" stroke="#30363d"/>
<text class="rise a2" x="20" y="90" font-size="32" fill="#e6edf3">Your Name</text>
<text class="rise a3" x="20" y="120" font-size="16" fill="#8b949e">your tagline</text>
```

**Gotchas:** `dasharray` ≥ line length; keep the ladder under ~2s total; both `forwards` holds
the end state (or use `both`).

### R4 — Gauge to 88% (from §13.1)

```svg
<circle cx="60" cy="60" r="46" fill="none" stroke="#e6edf3" stroke-opacity=".15" stroke-width="10"
        pathLength="100" stroke-dasharray="100" stroke-dashoffset="100">
  <animate attributeName="stroke-dashoffset" from="100" to="12" dur="1.6s"
           begin="0.3s" fill="freeze" repeatCount="1"/>
</circle>
<text x="60" y="66" text-anchor="middle" font-size="20" fill="#3fb950">88%</text>
```

**Gotchas:** `pathLength="100"` is the whole trick — offset = 100 − percent; rotate the circle
(`transform="rotate(-90 60 60)"`) if you want the sweep to start at 12 o'clock.

### R5 — Travelling pulse on a rule (from §7.4)

```svg
<rect x="0" y="20" width="600" height="2" fill="#21262d"/>
<rect x="-120" y="18" width="120" height="6" rx="3" fill="url(#sheen)">
  <animate attributeName="x" values="-120;600;600" keyTimes="0;0.5;1"
           dur="3s" repeatCount="indefinite"/>
</rect>
<!-- linearGradient #sheen: x1=0% x2=100%, stops transparent → #3fb950 → transparent -->
```

**Gotchas:** `keyTimes` parked at the end (`…;600;600`) prevents the visible wrap; animate `x`
on the shape, never `gradientTransform` (WebKit freezes — §10).

### R6 — Phase-shifted particles (from §11)

```svg
<style>
.spark{animation:trav 6s linear infinite}
.a1{animation-delay:0s}.a2{animation-delay:-2.3s}.a3{animation-delay:-4.1s}
@keyframes trav{
  0%{transform:translate(0,0);opacity:0}
  10%{opacity:1}
  90%{opacity:1}
  100%{transform:translate(160px,-40px);opacity:0}}
</style>
<circle class="spark a1" cx="40"  cy="60" r="2" fill="#ffd9a0"/>
<circle class="spark a2" cx="180" cy="30" r="1.5" fill="#ffb454"/>
<circle class="spark a3" cx="300" cy="70" r="2" fill="#ff7a5c"/>
```

**Gotchas:** negative delays = already mid-flight on first paint; 10–20 clones max; different
durations per particle if you have more than three.

### R7 — Orbit (from §6)

```svg
<g transform="translate(300,60)">
  <circle r="40" fill="none" stroke="#ffb454" stroke-opacity=".15"/>
  <g>
    <animateTransform attributeName="transform" type="rotate" from="0" to="360"
                      dur="14s" repeatCount="indefinite"/>
    <circle cx="40" cy="0" r="3" fill="#ffb454"/>
  </g>
</g>
```

**Gotchas:** rotate a wrapper `<g>` with the satellite offset on `cx`/`cy` — then no
`transform-box` needed; varied durations for multiple moons.

### R8 — Seamless scrolling wave (from §7.1)

```svg
<mask id="fade"><rect width="600" height="40" fill="url(#g)"/></mask>
<g mask="url(#fade)">
  <path d="M-600 20 Q-525 6 -450 20 T-300 20 T-150 20 T0 20 T150 20 T300 20 T450 20 T600 20 T750 20 T900 20 T1050 20 T1200 20"
        fill="none" stroke="#8b8b8b" stroke-width="1.5">
    <animateTransform attributeName="transform" type="translate" values="0 0;300 0"
                      dur="5s" repeatCount="indefinite"/>
  </path>
</g>
<!-- #g: horizontal gradient, opacity 0 → .9 → 0 at the edges -->
```

**Gotchas:** translate distance = exactly one wave period (300 = wavelength here, from `T`-command
spacing); overdraw beyond both edges; the mask hides the seams.

### R9 — Glitch title (from §8)

```svg
<g font-family="Impact, sans-serif" font-size="28" text-anchor="middle">
  <text x="200" y="40" fill="#ff5555" opacity=".5">PROFILE</text>
  <text x="200" y="40" fill="#8be9fd" opacity=".5">PROFILE
    <animate attributeName="x" values="200;202;197;203;200" dur="0.5s" repeatCount="indefinite"/>
  </text>
  <text x="200" y="40" fill="#50fa7b" opacity=".4">PROFILE
    <animate attributeName="y" values="40;42;38;41;40" dur="0.4s" repeatCount="indefinite"/>
  </text>
</g>
```

**Gotchas:** base layer static and crisp; ghosts only; test at 390px — jitter that reads as
glitch on desktop reads as blur on a phone.

### R10 — Terminal boot sequence (from §2.3 + §3)

```svg
<text x="10" y="20" font-family="monospace" font-size="13" fill="#8b949e" opacity="0">
  $ loading profile…<animate attributeName="opacity" values="0;1" begin="0.3s" dur="0.3s" fill="freeze"/>
</text>
<text x="10" y="40" font-family="monospace" font-size="13" fill="#3fb950" opacity="0">
  ✓ ready<tspan class="caret">▍</tspan>
  <animate attributeName="opacity" values="0;1" begin="1.1s" dur="0.3s" fill="freeze"/>
</text>
```

**Gotchas:** every `begin` is seconds from page load — the whole sequence replays on reload;
put anything essential at `begin="0s"` so a screenshot at t=0 isn't empty.

**All recipes, every time:** commit the SVG to your profile repo (branch URL updates in ~5 min —
`CAPABILITY-MATRIX.md:57`; pin the commit hash for seconds); keep total file size < 30KB unless
it's generated art; one filter per card; test on a phone before you call it done
(`docs/survey/FINDINGS.md` phone column = 309px).

---

## 21. Sources

**Fetched verbatim this session (2026-09-26, `raw.githubusercontent.com`, cached under
`motion/`):**

| File | Technique sections |
|---|---|
| `liss-bot/liss-bot` · `intro.svg` | §2.1 textPath typing chain |
| `sepahead` · `assets/hero-light.svg` | §2.2 clip typing, §7.4 sweep |
| `ayxn…` · `card.svg` | §3 blink / nudge / flow |
| `umang-eng/umang-eng` · `assets/header-v1.svg` | §4.1 entrance, §1 theme |
| `Jorexdev/Jorexdev` · `img/jorex-glow-v7.svg` | §4.2 fade, §9 glow pulse |
| `jgit705` · `assets/hero.svg` | §4.3 rise/ping/route/pop |
| JackLuciano · `assets/header.svg` | §6 orbit, §4.2 entrance |
| `10ishk/10ishk` · `assets/wave.svg` | §7.1 scroll |
| dhiru banner | §7.2 goo marquee, §16 dead hover |
| `matrix-banner.svg` | §7.3 falling columns, §14 dot-matrix |
| `karthik5033` · `assets/custom-divider.svg` | §7.4 pulse, §10 shimmer |
| `omkarrr88` · `profile/section-about.svg` | §7.4 sliding highlight |
| `gitbanner.svg` | §2.3 boot lines, §8 glitch, §10 metal gradient |
| `krishna-hero.svg` | §9 ring/core, §11 travelling dot |
| `Platane/snk` output (`snake.svg`) | §12 contribution snake |
| `rroy-streak.svg`, `ankit-bye.svg`, `happyren-name.svg`, `skymly-header.svg`, `jconfessor-hero-dark.svg`, `krishna…` | supporting samples in §2, §10, §13.1 |
| `observatory.svg` | §18 static — excluded |

**Repo docs (ground truth):** `docs/CAPABILITY-MATRIX.md` (engine captures, boundary tests,
reduced-motion, CDN timing), `docs/techniques/CATALOGUE.md` (usage counts, hover rule,
gradientTransform rule, pathLength, orbits), `docs/techniques/examples/*.svg` (repo-verified
gauge, bars, particles, stroke-draw, smil-draw, terminal, typing, textpath — all ✓ across three
engines), `docs/survey/data/technique_exemplars.json`, `docs/survey/FINDINGS.md` (phone width),
Part 07 (generator survival).
