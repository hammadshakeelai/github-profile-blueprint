# 1 · The Lookbook

The best-looking profile READMEs we could find, grouped by the visual language
they speak. Chosen by eye from about a hundred profiles photographed in September
2026: the curated "best of" lists, the most-starred profile repositories on
GitHub, a code search for hand-made animated SVGs, and a web search in English,
Chinese, Korean and Japanese.

Every image below is the creator's own file, loaded from their repository and
credited — nothing here is re-hosted. If one stops loading, they changed it; the
link still goes to the source.

> [!IMPORTANT]
> **One thing every piece in this chapter has in common:** we opened each hero
> SVG and measured its smallest text as it would appear on a phone. Across all
> twenty, it lands between **2.2px and 5.2px**. The most beautiful work in the
> ecosystem is uniformly unreadable in the hand. So each entry ends with two
> lines — *steal* (the idea worth taking) and *fix* (what to change so it
> survives a 309px column). See [the arithmetic](../../skills/github-profile-readme/SKILL.md#the-legibility-formula--apply-before-drawing-anything).

**Contents** —
[Editorial & luxury](#editorial--luxury) ·
[Print & brutalist](#print--brutalist) ·
[Sci-fi instruments](#sci-fi-instruments) ·
[Ink & organic](#ink--organic) ·
[Data as design](#data-as-design) ·
[Retro, pixel & nostalgia](#retro-pixel--nostalgia) ·
[Terminal](#terminal) ·
[Illustrated & cinematic](#illustrated--cinematic) ·
[The famous ones](#the-famous-ones)

---

## Editorial & luxury

The rarest style on GitHub and the most striking: serif type, restraint,
gold, whitespace. It reads as *a firm*, not a hobby.

### ashfordeOU — a letterhead with an orrery

<img src="https://raw.githubusercontent.com/ashfordeOU/ashfordeOU/main/assets/hero-dark.svg" width="600" alt="ASHFORDE wordmark in a small-caps serif beside a gold orrery, with an italic tagline 'For the missions that cannot fail'">

[github.com/ashfordeOU](https://github.com/ashfordeOU) · 880-unit canvas · 162 KB ·
SMIL + CSS keyframes · **embeds its own font**

The only way to guarantee a serif inside an image-SVG is to embed it — web fonts
can't load there — and this is one of very few profiles that does. Small caps,
a single gold accent, a Sanskrit line under the tagline, and the orrery turning
slowly: it looks printed.

**Steal:** embed a *subset* of one display face; one accent colour; let the
motion be a single slow rotation. **Fix:** smallest label is 3.5px on a phone —
the small-caps kicker lines need to roughly triple.

### Xalzeroph — a script wordmark and a black hole

<img src="https://raw.githubusercontent.com/Xalzeroph/Xalzeroph/main/assets/profile-header-dark.svg" width="600" alt="The name Xalzeroph in a flowing script over a deep-space field with a glowing black hole">

[github.com/Xalzeroph](https://github.com/Xalzeroph) · 1200-unit canvas · 127 KB ·
`feGaussianBlur` + radial gradients · SMIL

The black hole is nothing but stacked radial gradients and one blur. The page
continues as a "portfolio galaxy" where each project is a body in orbit. This
profile also ships **separate phone variants** behind `max-width` sources — the
technique [Track 6](../research/WIDTH-GATED.md) verified.

**Steal:** a cosmos from gradients alone; per-width art direction. **Fix:** the
desktop file's micro-labels (4.1px on a phone) are fine only because the phone
never sees it — make sure yours don't either.

---

## Print & brutalist

Condensed type, flat colour, visible grids, dithering. Borrowed from zines and
Swiss posters; loud on purpose.

### ayxn07 — dithered teal and giant type

<img src="https://raw.githubusercontent.com/ayxn07/ayxn07/main/assets/portfolio-hero.png" width="600" alt="A teal page with MOHAMMED AYAAN KHAN in huge condensed black type above a dithered, halftone photograph">

[github.com/ayxn07](https://github.com/ayxn07) · raster hero + SVG section tabs

A single flat teal, black condensed display type, a halftone photo and numbered
section tabs (`01 WHOAMI ↓ 02 PROJECTS ↓`) that behave like a site nav. It's the
only profile we found that looks like a printed poster.

**Steal:** one flat background colour for the *whole* page; numbered nav tabs;
a dithered photo instead of a gradient. **Fix:** raster heroes can't adapt to
dark/light — ship a second PNG behind `<picture>`.

### harkirat-data — the blueprint index

<img src="https://raw.githubusercontent.com/harkirat-data/harkirat-data/main/assets/dark/header-v1.svg" width="600" alt="A monospace technical-drawing header reading 'Portfolio — Index Nº 001' with the name in large type and hairline rules">

[github.com/harkirat-data](https://github.com/harkirat-data) · **4 KB** · CSS keyframes · media query

Hairline rules, monospace, "Index Nº 001", a system map drawn as a node graph
further down. The whole hero is 4 KB. The survey found this exact layout in
four profiles with personalised text — it's a template, and a good one.

**Steal:** technical-drawing furniture (index numbers, rules, figure captions).
**Fix:** at 1000 units, 3.4px labels; draw it at 600.

---

## Sci-fi instruments

Glows, grids, status lines, telemetry. The most common "ambitious" style — and
the one where craft separates the best from the rest.

### getaudra — systems online

<img src="https://raw.githubusercontent.com/getaudra/getaudra/main/assets/command-center-hero.svg" width="600" alt="A teal command-center panel reading SYSTEMS ONLINE with a glowing signal line and status readouts">

[github.com/getaudra](https://github.com/getaudra) · **3 KB** · one blur + SMIL

Three kilobytes. One glowing polyline, three status lines
(`MODE: OBSERVE → TEST → ITERATE`), a heading in wide caps. Proof that the HUD
look is about typography and one light source, not weight.

**Steal:** a status line that *says something* about how you work. **Fix:** 3.9px
labels on a phone.

### SergiGTAr — the security operator

<img src="https://raw.githubusercontent.com/SergiGTAr/SergiGTAr/main/assets/pipboy-terminal-dark.svg" width="600" alt="A neon-green terminal frame reading SECURITY-FIRST ENGINEERING with a framed photo of the author">

[github.com/SergiGTAr](https://github.com/SergiGTAr) · 59 KB · embedded photo, scanline
`<pattern>`, clip paths, CSS + SMIL

A Pip-Boy-style frame with the author's photo *embedded inside the SVG* (an
external `<image>` would be blocked), a scanline pattern over everything, and a
command prompt that reads `build --harden --verify`.

**Steal:** put the photo *in* the SVG as a data URI; a scanline `<pattern>`.
**Fix:** 5.2px — the best of this set, still under half the floor.

### adamalston — an observatory

<img src="https://www.adamalston.com/observatory.svg" width="600" alt="Three elliptical orbits around a gold sun with small readouts in the corners, like a scientific instrument">

[github.com/adamalston](https://github.com/adamalston) · served from the author's own domain · static

Three orbits, a gold sun, corner readouts in tiny mono (`AA/0-01`, `OBSERVATION
SYSTEM`). Calm where most HUDs shout. Notable too for being hosted on the
author's own site rather than GitHub.

**Steal:** instrument-panel corner marks; calm. **Fix:** it's entirely decorative
microtext at 3px — fine if it's decoration, but give the page a readable name
somewhere.

### HiradEmami · JackLuciano · AlexChek51

<img src="https://raw.githubusercontent.com/HiradEmami/HiradEmami/master/docs/assets/svg/system/start_here_control_surface.svg" width="600" alt="A game-UI style panel titled README CONTROL SURFACE with glowing buttons for Website, Labs and Collaboration">

<img src="https://raw.githubusercontent.com/JackLuciano/JackLuciano/main/assets/header.svg" width="600" alt="An amber header reading Szabolcs Szabó with a small orbiting light">

<img src="https://raw.githubusercontent.com/AlexChek51/AlexChek51/main/assets/header-dark.svg" width="600" alt="A dark blue circuit-board header with a glowing BUILD chip at the centre wired to labelled modules">

[HiradEmami](https://github.com/HiradEmami) turns the profile into a game menu
(*README Control Surface → Hirad Main System → Labs*).
[JackLuciano](https://github.com/JackLuciano) goes amber-on-black with a
telemetry panel of real counts further down.
[AlexChek51](https://github.com/AlexChek51) draws a circuit board with a glowing
`BUILD` chip, then follows it with bold stat tiles — in Russian, with an
English version one click away.

---

## Ink & organic

The rarest technique family: SVG filters used for texture rather than glow.

### XxMasterepicxX — sakura and a gold eclipse

<img src="https://raw.githubusercontent.com/XxMasterepicxX/XxMasterepicxX/main/assets/header-dark.svg" width="600" alt="Soft pink blossom clouds drifting over a dark field">

[github.com/XxMasterepicxX](https://github.com/XxMasterepicxX) · 203 KB ·
**`feTurbulence` + `feDisplacementMap`**, masks, clip paths, SMIL + CSS

The page is painted: blossom clouds, ink branches that frame each project
description, a thin gold eclipse ring. The organic edges come from
`feTurbulence` noise driving `feDisplacementMap` — the same filter pair the
"liquid glass" trend uses for refraction. We saw it in no other profile.

**Steal:** turbulence-displaced edges to make vector art look hand-made.
**Fix:** 3.2px labels; and 203 KB is heavy for a header.

### JConfessor — a wind turbine

<img src="https://raw.githubusercontent.com/JConfessor/JConfessor/main/assets/hero-dark.svg" width="600" alt="A blue hero with JORGE CONFESSOR in bold type beside a white wind turbine whose blades turn">

[github.com/JConfessor](https://github.com/JConfessor) · 9 KB · SMIL rotation

The author analyses operational data for a wind-energy company, so the hero is a
turbine, turning. The most *personal* image in this chapter, and 9 KB.

**Steal:** draw the thing your work is actually about. **Fix:** 2.9px.

---

## Data as design

Charts that are the decoration, instead of stat cards bolted on.

### sepahead — the pulse

<img src="https://raw.githubusercontent.com/sepahead/sepahead/main/assets/hero-dark.svg" width="600" alt="A monospace hero for Sepehr Mahmoudian with the tagline High Energy · High Agency · Takes Initiative">

[github.com/sepahead](https://github.com/sepahead) · 6 KB · CSS keyframes

Below the hero is the best data section we found: "THE PULSE" — contributions per
year as bars, the current year highlighted, a laurel marking the "golden age" —
then "Where the week goes" as a donut. It reads like a newspaper graphic, not a
dashboard.

**Steal:** annotate your chart like a journalist would. **Fix:** 4.7px.

### garimasingh128 · leereilly

<img src="https://raw.githubusercontent.com/garimasingh128/garimasingh128/master/stats.gif" width="600" alt="A streamgraph of languages used over time in bright overlapping colours">

<img src="https://raw.githubusercontent.com/leereilly/leereilly/master/contribution-graph.svg" width="600" alt="A band of green contribution squares used as a decorative header">

[garimasingh128](https://github.com/garimasingh128) shows languages over time as
a streamgraph — the most colourful chart on any profile we saw.
[leereilly](https://github.com/leereilly) uses the contribution grid itself as a
decorative header, then a wall of posters for events they organised (Git Merge,
Game Off, Hacktoberfest) as "top ships".

---

## Retro, pixel & nostalgia

### atikulmunna — Flappy Bird, playing itself

<img src="https://raw.githubusercontent.com/atikulmunna/atikulmunna/main/assets/flappy.svg" width="600" alt="A monochrome 8-bit side-scroller: a small bird flapping between pipes over pixel clouds">

[github.com/atikulmunna](https://github.com/atikulmunna) · 106 KB · SMIL, masks, clip paths

An 8-bit side-scroller animated entirely in SMIL, captioned
`> run --game flappy`. The rest of the page follows through: terminal section
headings, pixel stat cards.

**Steal:** a tiny *game* as the hero instead of a banner. **Fix:** 2.2px — the
smallest in the set.

### BrunnerLivio — GeoCities, lovingly

<img src="https://raw.githubusercontent.com/BrunnerLivio/brunnerlivio/master/images/welcome.png" width="600" alt="Rainbow WordArt reading Welcome to my Github Profile">

[github.com/BrunnerLivio](https://github.com/BrunnerLivio) · PNG + GIFs + a live guestbook

WordArt, a spinning globe GIF, a DJ gif, "best viewed with" badges — and a
**working guestbook** whose entries are real visitors. The joke is executed so
completely that it becomes the best nostalgia piece on GitHub.

### thenolle — pastel pixel with supporters

<img src="https://raw.githubusercontent.com/thenolle/thenolle/master/images/banner.svg" width="600" alt="A pastel pink and blue pixel banner reading NOLLY with a character card and the avatars of the last six supporters">

[github.com/thenolle](https://github.com/thenolle) · **1.4 MB** · embedded raster + font

Cosy: pastel gradients, a pixel wordmark, and a row showing the **last six
supporters' avatars** baked in. Warm where most profiles are cold.

**Steal:** thank your supporters *visually*. **Fix:** 1.4 MB — compress the
embedded art.

Also here: [trinib](https://github.com/trinib) (maximal retro — pixel hearts,
ASCII rainbow wordmark, animated GIFs everywhere) and
[Carol42](https://github.com/Carol42) (purple Matrix rain behind "Welcome to my
profile!", with an English/Português switch).

---

## Terminal

### JosephQ47 · Dhyanesh006 · 10ishk

<img src="https://raw.githubusercontent.com/JosephQ47/JosephQ47/main/assets/matrix-banner.svg" width="600" alt="Green Matrix digital rain behind the name Joseph in glowing green">

<img src="https://raw.githubusercontent.com/Dhyanesh006/Dhyanesh006/main/assets/matrix-boot.svg" width="600" alt="A green terminal boot sequence with OK status lines">

<img src="https://raw.githubusercontent.com/10ishk/10ishk/main/assets/hero-ide.svg" width="600" alt="A dark IDE window with a file tree, tabs and a code editor showing the author's name and role">

[JosephQ47](https://github.com/JosephQ47) — Matrix rain, then `./whoami`,
`./tech_stack`, `./projects` sections, in Chinese. 54 KB, no third parties.
[Dhyanesh006](https://github.com/Dhyanesh006) — a boot log where each section
"mounts". [10ishk](https://github.com/10ishk) — the whole hero is an **IDE**:
file tree, tabs, a status bar.

[jcubic](https://github.com/jcubic) opens with the name as figlet ASCII art and
one line: `$ npx jcubic` — a business card you can run.

---

## Illustrated & cinematic

<img src="https://raw.githubusercontent.com/M0nica/M0nica/master/gh-header-image-cropped.png" width="600" alt="A flat vector illustration of a person working on a laptop beside the name Monica Powell">

[M0nica](https://github.com/M0nica) — a commissioned-style flat illustration of
the author; plus a rotating Octocat version. [cszach](https://github.com/cszach)
— a 3D-rendered gallery room with the domain projected on the far wall.
[MartinHeinz](https://github.com/MartinHeinz) — a brush-script banner.
[novatorem](https://github.com/novatorem) — the Spotify "now playing" card with a
live waveform, by the person who built the widget everyone copies.

---

## The famous ones

The most-starred profile repositories GitHub search could find (September 2026).
Stars on a profile repo mostly mean *people copied it*, so this is a list of the
most imitated designs, not necessarily the best.

| ★ | Profile | Based (from their GitHub profile) | What it's known for |
|--:|---|---|---|
| 2,696 | [rafaballerini](https://github.com/rafaballerini) | Santa Catarina, Brazil | The canonical Brazilian dev-creator profile; widely copied |
| 1,465 | [midudev](https://github.com/midudev) | Barcelona | Auto-updating grids of the latest YouTube thumbnails, two channels |
| 878 | [elidianaandrade](https://github.com/elidianaandrade) | not stated · writes in Portuguese | Latest videos and study material, kept current by Actions |
| 758 | [novatorem](https://github.com/novatorem) | Toronto | Author of the Spotify now-playing widget |
| 747 | [DenverCoder1](https://github.com/DenverCoder1) | not stated | Author of readme-typing-svg, streak stats, custom-icon-badges |
| 689 | [anmol098](https://github.com/anmol098) | Dubai | Waka Readme Stats author; a meeting-booking card; `npx anmol` |
| 652 | [mazassumnida](https://github.com/mazassumnida) | not stated · writes in Korean | A service rendering solved.ac / Baekjoon competitive-programming badges |
| 508 | [trinib](https://github.com/trinib) | Trinidad & Tobago | Maximal retro GIF collage |
| 443 | [simonw](https://github.com/simonw) | California | The self-updating three-column README everyone copied |
| 440 | [MartinHeinz](https://github.com/MartinHeinz) | Bratislava | Brush-script banner, blog list |
| 409 | [Carol42](https://github.com/Carol42) | not stated · English/Português toggle | Purple Matrix rain, bilingual switch |
| 290 | [andyruwruw](https://github.com/andyruwruw) | Bay Area, California | Spotify top tracks and live chess.com games rendered as boards |

The shape of that list is worth noticing: **the top three are Portuguese- and
Spanish-language creators**, and a large share of the rest are the *authors of
the widgets* — novatorem, DenverCoder1, anmol098, mazassumnida — whose profiles
double as their tools' demo pages.
