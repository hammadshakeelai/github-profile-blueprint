# SUPER-REEL — the motion hook

`SUPER-REEL.svg` is the wave's "super SVG with a lot of motion": one 1280×720
file, a 30-second seamless loop, **zero scripts**, rendered from a plain `<img>`
tag. It is both the visual hook for the project and the proof that every
technique documented in parts 01–09 survives GitHub's sanitizer.

## Facts

| | |
|---|---|
| File | `SUPER-REEL.svg` — ~35 KB, self-contained |
| Loop | 30 s, `repeatCount="indefinite"` / infinite CSS, fractional `keyTimes` so the seam is invisible |
| Engines | SMIL + CSS keyframes + `stroke-dashoffset` + masks + `<clipPath>` typing + `textPath` |
| Fonts | system stack only — no webfonts |
| Scripts | none (GitHub strips `<script>`; this file has 0 bytes of JS) |
| Verified | 12 headless captures across all 7 scenes + the loop seam |

## Scene schedule

`e` = one-seventh of the loop (4.286 s). Every scene-synced animation uses the
same 30 s duration and `keyTimes` expressed in `e`, so scenes cut together
atomically.

| # | Scene | Window | Shows |
|---|---|---|---|
| 01 | boot | 0 – 4.29 s | terminal typing (`<clipPath>` width anim), boot bar, caret blink |
| 02 | type | 4.29 – 8.87 s | kinetic "MOTION" — six `<text>` nodes, per-letter color, `textLength` grid lock, stroke pulse |
| 03 | orbit | 8.87 – 13.16 s | counter-rotating gauge labels (upright text), three arcs, HUD gauges 41 / 55 / 24 |
| 04 | ticker | 13.16 – 17.14 s | dual-copy marquee in one `clipPath`, stacked language bar, chips, pull-quote |
| 05 | line | 17.14 – 21.43 s | self-drawing timeline spine (`pathLength=100`), milestone circles pop on keyTimes |
| 06 | stats | 21.43 – 25.71 s | defect dot-plot (img 41 / text 55 / badge 42 / stats 24 / cta 30) |
| 07 | ship | 25.71 – 30 s | outro card + gradient sweep, then loop seam back to scene 01 |

A persistent HUD rides on top of everything: title bar, right-hand engine tags,
per-scene label (`01 boot` … `07 ship`) and a segmented progress bar whose fill
is one 30 s animation — so the HUD doubles as a visible timeline scrubber.

Independent loops (caret blink, pulse) use durations that divide 30 evenly
(1 / 2.5 / 7.5 / 15 / 30 s) so nothing drifts across the loop boundary.

## Verification

Chrome's `--virtual-time-budget` screenshots SMIL documents unreliably — it
frequently captured a t≈0 frame no matter the budget (the SVG was not at
fault; the same budgets produced correct captures on other runs). Deterministic
QA uses `seek-capture.ps1`, which clones the SVG, injects a throwaway script
into the **copy** (the deliverable stays script-free), calls
`pauseAnimations()` + `setCurrentTime()` plus `document.getAnimations()` seeks,
and screenshots the frozen frame:

```powershell
.\seek-capture.ps1 3500 6500 10500 14500 16500 19500 23500 27500 29950
```

Captured evidence lives in `shots/seek_*.png` (plus earlier `shot_*.png`
runs). Verified states:

- 800 / 3500 — scene 01 mid-typing and fully typed
- 6500 — scene 02 kinetic type, HUD 22 %
- 10500 — scene 03 orbit, upright gauge labels, HUD 35 %
- 14500 / 16500 — scene 04 marquee (separator verified), bar fill, chips, quote
- 19500 — scene 05 spine drawn, milestones popped, HUD 62 %
- 23500 — scene 06 defect chart, HUD 78 %
- 27500 / 29950 — scene 07 outro and the loop seam (progress ≈ 100 %)

## Using it

```html
<img src="opencode-research/SUPER-REEL.svg" width="1280" alt="Profile motion reel" />
```

Renders in `<img>` on GitHub READMEs, in issues, and in any browser. Same
pattern as the showcase examples in `docs/techniques/`.
