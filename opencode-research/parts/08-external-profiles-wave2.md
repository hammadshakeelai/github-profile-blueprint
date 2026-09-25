# Part 08 — Fresh External Research, Wave 2: Motion-First Standout Profiles (2026)

**Research date:** 2026-09-26
**Method:** Every profile below was fetched live during this session from `raw.githubusercontent.com/<user>/<user>/<branch>/README.md`, probing `main` first and falling back to `master` (two profiles here live on `master`). All code blocks are verbatim from those raw files — not from memory, not from screenshots. Each username was checked against the dedupe lists before inclusion.

**Scope note:** 20 new profiles, all confirmed absent from both dedupe sources. Ratings are out of 5 and are argued across craft, motion, originality, and phone impact — with an explicit bias toward motion-first work (kinetic typography, isometric/generative art, animated terminals, pixel art, blueprint/technical layouts, SMIL/CSS animation) over plain stat cards.

**Already covered — do not re-cover:**

- `docs/survey/SHORTLIST.md`: ayxn07, ashfordeOU, JGit705, JConfessor, SergiGTAr, brandon-fryslie, marcizhu, 10ishk, SimarBhatiaSB7, adamalston, XxMasterepicxX, Dhyanesh006, getaudra, sepahead, atiketmunna, erogluyusuf, codeSTACKr, BrunnerLivio, nihalsheikh, JackLuciano, plus template family (umang-eng, harkirat-data, aniketpitre).
- `opencode-research/parts/06-external-profiles.md` (wave 1): tholman, ethomson, trueberryless, platane, Andrew6rant, chef0111, RayhanADev, JasonEtco, warengonzaga, sw-yx, nikolalsvk, Carol42, KasRoudra, eagleanurag, nilutpolkashyap, onemohrtime, PrincessAkira, 8bithemant, seuthootDev.
- Dropped from candidate mining as already-known or not profiles: DenverCoder1, peterthehan, simonw, halfrost, spiderpig86, khalby786, Ileriayo, and the template/tool authors below.

**Important filter applied:** many search hits are *tools or templates* rather than profile READMEs (terminal-generators, banner-APIs, stats services). A tool only counts here if the author's own `USER/USER` profile demonstrably uses the thing it made — that self-hosting test is what separates a standout profile from a landing page.

---

## Index

| # | Profile | Category | Rating | Why it made the cut |
|---|---------|----------|--------|---------------------|
| 1 | [t1seo](https://github.com/t1seo) | 3D / generative-art | 4.5/5 | A walkable 3D calendar village grown from your contributions, with WASD navigation and day/night SVGs |
| 2 | [williamzujkowski](https://github.com/williamzujkowski) | terminal-style / generated SVG | 4.5/5 | Self-built `svg-terminal` renders a *living* scrolling terminal, 20 daily themes, proper reduced-motion fallback |
| 3 | [lennystepn-hue](https://github.com/lennystepn-hue) | pixel-art / arcade | 4/5 | Whole profile is arcade attract-mode art, nightly regenerated from `profile.config.json`, drawn from a hand-built 5×7 font |
| 4 | [okturan](https://github.com/okturan) | generative-art / game | 4/5 | Tower-defense battle animated *over* the contribution graph — big commit days are towers firing at bugs |
| 5 | [ryanpolasky](https://github.com/ryanpolasky) | code-editor theme | 4/5 | Entire profile as one VS Code window: header, about, skills, stats, status bar — all as local SVGs |
| 6 | [prsdx](https://github.com/prsdx) | pixel pet / kinetic | 4/5 | Author of YourTomo: a pixel cat reacting to real activity plus an isometric cat-city contribution map |
| 7 | [WJZ-P](https://github.com/WJZ-P) | isometric / bilingual | 4/5 | CommitCraft Minecraft-style isometric stat banners and a whole contribution map, self-hosted on a Worker |
| 8 | [Luc0-0](https://github.com/Luc0-0) | terminal / blueprint | 4/5 | `whoami`-style code block, hand-made SVG cursor "still typing…", custom SVG buttons, live systems status card |
| 9 | [VARDHAMANPATEL23](https://github.com/VARDHAMANPATEL23) | arcade / structured | 4/5 | Git Invaders (Space Invaders) contribution graph as hero; Python "SYSTEM IDENTITY" dict; numbered project sections |
| 10 | [GermanAndresLopez](https://github.com/GermanAndresLopez) | terminal + generated SVG | 4/5 | Own animated-stats terminal (`whoami → neofetch → languages → uptime → exit`), self-owned banner/stack SVGs, snake |
| 11 | [BerkaySevinc](https://github.com/BerkaySevinc) | fully-generated SVG set | 3.5/5 | Every band — header, typing, divider, stats, langs, footer — is a self-owned SVG, wrapped in `PROFILE:START/END` |
| 12 | [viochris](https://github.com/viochris) | ASCII portrait / motion stack | 3.5/5 | Responsive 4-way `ascii-portrait` SVG (desktop/mobile × dark/light) plus snake, 3D isometric, isocalendar |
| 13 | [OstinUA](https://github.com/OstinUA) | animated GIF / card tooling | 3.5/5 | Owns the readme-SVG tool org; animated ASCII GIF, CSS donut, bengo cards, 8-bit footer GIF |
| 14 | [Christophe1997](https://github.com/Christophe1997) | generative / data-story | 3.5/5 | Commit-history.com embed + own "Token Profile" card tracking AI token spend as a profile artifact |
| 15 | [abir2afridi](https://github.com/abir2afridi) | animated banner / collage | 3/5 | Own `github-animatedbanner` API in the hero, icon8 GIF section headers, skillicons, waving footer |
| 16 | [m3hrab](https://github.com/m3hrab) | generative-art / constellation | 3/5 | Contribution year drawn as a star constellation — brightness = intensity, lines = streaks |
| 17 | [saroo98](https://github.com/saroo98) | hero SVG / typographic | 3/5 | Self-owned `saro-hero.svg` + `saro-divider.svg`, quad-line typing SVG, deliberately curated GIF accents |
| 18 | [DhanushNehru](https://github.com/DhanushNehru) | animated dividers / kinetic | 3/5 | Own ScribeSVG typing render; animated divider GIF used as the profile's only section separator, six times |
| 19 | [Spectrewolf8](https://github.com/Spectrewolf8) | isometric | 3/5 | Self-deployed isometric 3D contribution graph (~160 users) as the hero — eat-your-own-dogfood tooling |
| 20 | [NissonCX](https://github.com/NissonCX) | capsule-render / bilingual | 2.5/5 | Borderline: localized (zh) profile with fading capsule header and GIF table — kinetic type but little originality |

**Category coverage:** 3D/generative (1, 4, 16), terminal (2, 8, 10), pixel/arcade (3, 6, 9), isometric (7, 19), code-editor (5), fully-generated SVG sets (10, 11), ASCII/portrait (12), card tooling (13, 14), banner APIs (15), typographic (17), divider motion (18), capsule-render (20).

---

## 1. t1seo — A walkable 3D calendar village grown from your contributions — **4.5/5**

- Profile: https://github.com/t1seo
- Raw README: https://raw.githubusercontent.com/t1seo/t1seo/main/README.md

**What it is:** The hero is an SVG "sky village" generated from the author's GitHub contribution history across four seasons, served light/dark via `<picture>`. Clicking it opens a real 3D tour of the *same* village (WASD to walk, Q/E to turn, drag to look), seeded from a checked-in `maeul-in-the-sky.snapshot.json`. There's a "SVG studio" to customize it, and an archive `<details>` preserving earlier landscape and island experiments. This is the most ambitious contribution-graph reinterpretation in either wave — it treats your commit history as a place you can walk through.

```html
<a href="https://t1seo.github.io/maeul-in-the-sky/tour/?snapshot=https%3A%2F%2Fraw.githubusercontent.com%2Ft1seo%2Ft1seo%2Fmain%2Fmaeul-in-the-sky.snapshot.json" aria-label="Walk inside this Calendar village in 3D">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./maeul-in-the-sky-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="./maeul-in-the-sky-light.svg">
  <img src="./maeul-in-the-sky-dark.svg" alt="My animated sky village, grown from GitHub contributions across four seasons" width="100%">
</picture>
</a>
```

```markdown
Click the picture to walk inside this same village in 3D. Use WASD to walk, Q/E to turn in place, and drag to look around. Click the map to jump to another part of the village.
```

```markdown
[🚶 Walk inside this village](https://t1seo.github.io/maeul-in-the-sky/tour/?snapshot=…) · [☀️ Day](…maeul-in-the-sky-light.svg) · [🌙 Night](…maeul-in-the-sky-dark.svg) · [🌿 Customize in the SVG studio](https://t1seo.github.io/maeul-in-the-sky/)
```

**Rating 4.5/5.** Craft: the static SVG, the 3D snapshot and the day/night variants all derive from one dataset — a coherent system, not a gimmick. Motion: the *interaction* is the motion (a first-person walk), which reads brilliantly and makes the flat SVG a teaser rather than the whole show. Originality: nothing else in this survey is a navigable 3D world of your own commit calendar. Phone: the walk needs a keyboard, so mobile gets the SVG only — hence not a 5. The archived experiments in `<details>` are a bonus sign of a tinkerer's profile.

**Style tags:** `3d-walkable`, `generative`, `contribution-graph-reimagined`, `day-night-variant`, `picture-responsive`, `snapshot-json`, `self-built-tooling`

---

## 2. williamzujkowski — A living animated terminal with live data and 20 rotating themes — **4.5/5**

- Profile: https://github.com/williamzujkowski
- Raw README: https://raw.githubusercontent.com/williamzujkowski/williamzujkowski/main/README.md

**What it is:** The hero is `./src/terminal.svg` — a scrolling terminal animation built by the author's own `svg-terminal` generator (48 blocks, zero runtime deps). It refreshes every 6 hours with live weather, live GitHub stats, language breakdown and a rotating dad joke, and rotates its theme daily through 20 OKLCH/WCAG-AAA palettes. A `terminal-static.svg` is served *only* under `prefers-reduced-motion: reduce` — a textbook accessibility pattern almost nobody implements. The page below mixes a /now-style link row, a blog list between `BLOG-POST-LIST` markers, and a clean project table.

```html
<picture>
  <source srcset="./src/terminal-static.svg" media="(prefers-reduced-motion: reduce)">
  <img src="./src/terminal.svg" alt="Animated terminal showing William's GitHub profile — security engineer, multi-agent AI builder, homelabber, dad-joke connoisseur" width="100%">
</picture>
```

```html
<em>This terminal is <strong>alive</strong> — a scrolling session that refreshes every 6 hours with live weather, live GitHub stats + language breakdown, and a rotating dad joke. The theme rotates daily through 20 palettes.
<br>Built with <a href="https://github.com/williamzujkowski/svg-terminal">svg-terminal</a> (48 blocks, zero runtime deps). Set <code>prefers-reduced-motion</code> and you get the static version automatically.</em>
```

```markdown
<!-- BLOG-POST-LIST:START -->
- [Two Processes, One Page Cache: Testing Shared State Before Blaming the VM](…)
…
<!-- BLOG-POST-LIST:END -->
```

**Rating 4.5/5.** Craft: a purpose-built SVG terminal generator with deterministic CI builds and AA-rated palettes — engineering-grade. Motion: constant, but content-bearing (live data scrolls in), not decoration. Originality: dogfooded tooling plus the reduced-motion twin is rare. Phone: an SVG terminal scales to full width and stays legible. Loses half a point only because the surrounding prose is conventional and the hero is one big raster-ish block.

**Style tags:** `animated-terminal`, `self-built-generator`, `live-data-refresh`, `20-theme-rotation`, `reduced-motion-fallback`, `dogfooding`, `oklch`

---

## 3. lennystepn-hue — Arcade attract-mode pixel art, regenerated nightly from config — **4/5**

- Profile: https://github.com/lennystepn-hue
- Raw README: https://raw.githubusercontent.com/lennystepn-hue/lennystepn-hue/main/README.md

**What it is:** The entire profile is generated from `profile.config.json` by a nightly GitHub Action into hand-drawn pixel SVGs: `hero.svg`, `player.svg` (a level/score card), `stack.svg` (a "Loadout"), `select.svg` (a project select screen), `grid.svg`, `footer.svg`. The copy commits to the bit — a `**▶ PLAY**` project row, "Attract mode", a footer crediting a reusable `attract-mode` template, and an honest colophon: the art is drawn pixel by pixel from a hand-built 5×7 font with no image editor involved.

```html
<!--
  This file is generated. Edit profile.config.json (or scripts/) and run
  `npm run build`. Hand edits here are overwritten by the nightly workflow.
  See SETUP.md to use this as a template for your own profile.
-->
```

```html
<img src="assets/player.svg" alt="Player card: level 23, score 1456, active on 76 days in the last year" width="900">
```

```markdown
**▶ PLAY** &nbsp;&nbsp; [`schichtplaner`](…) · [`openclippy`](…) · [`butlr-openclaw-platform`](…) · [`clawshield`](…) · [`inkpreview`](…) · [`agentcheck`](…)
```

```html
<sub>Every number above is real, and re-rendered from the GitHub API each night by a
workflow in this repository. The artwork is drawn pixel by pixel from a hand-built
5×7 font, with no image editor involved.</sub>
```

**Rating 4/5.** Craft: the 5×7 font pipeline and config-driven regeneration are genuinely built, and the alt text carries the data for screen readers and no-JS. Motion: "attract mode" is an *aesthetic* of motion (arcade idling) rather than literal animation — the SVGs are static but read as a paused game screen. Originality: high; the arcade metaphor is carried through copy, layout and file names. Phone: full-width SVGs, excellent. Loses a point because the actual pixels don't move.

**Style tags:** `pixel-art`, `arcade-attract-mode`, `config-generated`, `nightly-action`, `hand-built-font`, `template-reusable`, `alt-text-rich`

---

## 4. okturan — Tower-defense battle animated over your contribution graph — **4/5**

- Profile: https://github.com/okturan
- Raw README: https://raw.githubusercontent.com/okturan/okturan/main/README.md

**What it is:** Okan's own `github-blocks` tool turns public GitHub data into contribution-graph art. The centerpiece is `lane-defense.svg`: a tower-defense game staged on the contribution graph where big commit days are towers firing lasers at invading bugs, regenerated daily, dark/light aware. Around it: generated `profile-stats.svg`/`profile-languages.svg`, `profile-facts.svg` ("500 indexed public default-branch non-merge commits"), and anime cards from a MyAnimeList workflow. Text is plain but precise — DirWiz, CropSize, TinyVoice, Foljapp, claude-statusblocks, epoch-td.

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/okturan/okturan/output/lane-defense.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/okturan/okturan/output/lane-defense-light.svg">
  <img alt="Tower defense battle animated over Okan's contribution graph: big commit days are towers firing lasers at invading bugs; a fresh battle is generated daily" src="https://raw.githubusercontent.com/okturan/okturan/output/lane-defense.svg">
</picture>
```

```markdown
**[github-blocks](https://github.com/okturan/github-blocks)** — An SVG generator that turns public GitHub data into contribution graph art and profile cards. The cards on this profile come from it.
```

```html
<img alt="Recent public coding habits from 500 indexed public default-branch non-merge commits" src="https://raw.githubusercontent.com/okturan/okturan/output/profile-facts.svg">
```

**Rating 4/5.** Craft: everything visual is generated by the author's own tool — complete dogfooding loop. Motion: the battle is animated and *data-driven* (your commits decide the towers), which is the best kind of profile animation. Originality: lane-defense-over-contributions is a first in this survey. Phone: full-width SVG, dark/light handled. Loses on prose: the profile's text is competent but flat, and the anime cards add requests without much payoff.

**Style tags:** `generative`, `game-over-data`, `contribution-graph-reimagined`, `dark-light-variant`, `self-hosted-output-branch`, `dogfooding`, `daily-regeneration`

---

## 5. ryanpolasky — The whole profile as one VS Code window — **4/5**

- Profile: https://github.com/ryanpolasky
- Raw README: https://raw.githubusercontent.com/ryanpolasky/ryanpolasky/main/README.md

**What it is:** Five full-width images and one service call compose a single editor window: `header.svg` (title bar), `about.svg`, `skills.svg`, a stats render from the author's own RyMe.md service (`ryme.md/api/render/code-github-stats`), and `footer.svg` as the status bar. There is literally no prose in the README — the design *is* the content. Code-editor skeuomorphism executed end-to-end.

```html
<img src="https://raw.githubusercontent.com/ryanpolasky/ryanpolasky/main/header.svg" width="100%" alt="Code Editor">

<img src="https://raw.githubusercontent.com/ryanpolasky/ryanpolasky/main/about.svg" width="100%" alt="Code Markdown">

<img src="https://raw.githubusercontent.com/ryanpolasky/ryanpolasky/main/skills.svg" width="100%" alt="Code Stack">

<img src="https://ryme.md/api/render/code-github-stats?u=ryanpolasky&bg=1e1e1e&fg=d4d4d4&accent=569cd6&muted=6a737d&loop=0" width="100%" alt="Code GitHub">

<img src="https://raw.githubusercontent.com/ryanpolasky/ryanpolasky/main/footer.svg" width="100%" alt="Code Status Bar">
```

**Rating 4/5.** Craft: the VS Code theme is consistent across five assets — borders, accents (`#569cd6`), muted greys all match. Motion: the stats endpoint carries `loop=0`, so there *is* animation capability in the service, though the window itself is static. Originality: editor-window profiles exist, but composing it entirely from self-hosted SVGs with a status-bar footer is disciplined. Phone: five stacked full-width images are safe. Loses for having zero accessible text and zero links — beautiful but a dead end for crawlers and screen readers.

**Style tags:** `code-editor-skeuomorphism`, `vscode-theme`, `svg-suite`, `self-hosted-service`, `zero-prose`, `status-bar-footer`

---

## 6. prsdx — YourTomo's pixel cat and an isometric cat-city contribution map — **4/5**

- Profile: https://github.com/prsdx
- Raw README: https://raw.githubusercontent.com/prsdx/prsdx/main/README.md

**What it is:** The author of the YourTomo GitHub Action uses his own product twice: `dist/pet.svg` is "neko", a pixel cat that reacts to real GitHub activity (dark/light variants), and `dist/isocat.svg` renders his contribution year as an isometric city with a kitty hopping along the weekly peaks, regenerated every 6 hours. Between them: a rotating quote typing-SVG and standard generated stats. The closing line owns the whole conceit honestly.

```html
<img alt="neko - a pixel cat that reacts to my real GitHub activity" src="https://raw.githubusercontent.com/prsdx/prsdx/main/dist/pet.svg" width="100%">
```

```markdown
- 🐙 Author of **YourTomo** — an open-source **GitHub Action** (TypeScript · Bun); the pixel cat on this very profile
```

```html
<img alt="my real contribution year as an isometric city with a kitty hopping along the weekly peaks - regenerated every 6h" src="https://raw.githubusercontent.com/prsdx/prsdx/main/dist/isocat.svg" width="100%">
```

```markdown
*the cat above is **neko** — both visuals are powered by [YourTomo](https://github.com/prsdx/YourTomo), a zero-dependency state machine I built that renders my real activity to animated SVG every 6h. if neko is grumpy, that is on me.*
```

**Rating 4/5.** Craft: two distinct art directions (pixel pet, isometric city) from one state machine; dark/light handled everywhere. Motion: animated SVG driven by real activity — the cat literally reflects your week. Originality: pet-as-API is a known idea; pet *plus* isometric-cat-city is not. Phone: both full-width. Loses for the massive badge wall (a full screen of shields before content) and the quote ticker's novelty wearing thin.

**Style tags:** `pixel-pet`, `isometric`, `activity-driven-svg`, `dark-light-variant`, `dogfooding`, `6h-regeneration`, `kinetic-quote`

---

## 7. WJZ-P — CommitCraft: Minecraft-style isometric stat banners and a contribution map — **4/5**

- Profile: https://github.com/WJZ-P
- Raw README: https://raw.githubusercontent.com/WJZ-P/WJZ-P/main/README.md (bilingual, links `README.en.md`)

**What it is:** Everything visual comes from the author's own CommitCraft service on a Cloudflare Worker: seven isometric Minecraft-style stat banners (commits, stars, PRs, issues, followers, repos, merged PRs), a "Player Passport" card, per-repo isometric cards, and a full-width `api/map/wjz-p.svg` contribution map described as turning the heatmap into a "Minecraft 风格的等距像素世界" (Minecraft-style isometric pixel world). The page opens with a capsule-render header and a moe-counter, and carries an openly personal, bilingual voice — including a wistful Chinese New Year comment hidden in an HTML comment.

```html
<a href="https://commit-craft.wjz-p.workers.dev/"><img src="https://commit-craft.wjz-p.workers.dev/api/banner/wjz-p/commits.svg" alt="Commits" height="300" /></a>
<a href="https://commit-craft.wjz-p.workers.dev/"><img src="https://commit-craft.wjz-p.workers.dev/api/banner/wjz-p/stars.svg" alt="Stars" height="300" /></a>
… (prs / issues / followers / repos / merged)
```

```html
<a href="https://commit-craft.wjz-p.workers.dev/">
  <img src="https://commit-craft.wjz-p.workers.dev/api/map/wjz-p.svg" alt="CommitCraft Contribution Map" width="100%" />
</a>
```

```markdown
<em>由 <a href="https://github.com/WJZ-P/CommitCraft">CommitCraft</a> 生成 —— 将你的 GitHub 贡献热力图变成 Minecraft 风格的等距像素世界 🌍</em>
```

**Rating 4/5.** Craft: an entire self-hosted isometric asset family, consistently themed. Motion: the banners animate (they're generated SVG loops) and the map is the payoff. Originality: Minecraft-isometric-as-a-stat-language, plus bilingual warmth most profiles lack. Phone: banners at `height=300` stack fine. Loses for the broken-ish quoted `<div>` stats block near the bottom and general section sprawl.

**Style tags:** `isometric`, `minecraft-pixel`, `self-hosted-api`, `contribution-map`, `bilingual-cn-en`, `moe-counter`, `capsule-render`

---

## 8. Luc0-0 — Terminal `whoami`, hand-made SVG cursor, live systems card — **4/5**

- Profile: https://github.com/Luc0-0
- Raw README: https://raw.githubusercontent.com/Luc0-0/Luc0-0/main/README.md

**What it is:** A two-column profile: left is a fenced `user/role/stack/status` block, a hand-authored `./header/blink_cursor.svg` blinking cursor with "still typing…", bio, and custom SVG buttons (`portfolio.svg`, `linkedin.svg`, `email.svg`); right is a point-cloud `hero.png` portrait. Below: signature-project cards as custom SVGs (including **GodProfile**, the author's own MCP server that turns markdown into live profile pages), an `OSS_ORGS` marker block, `live_systems.svg` showing real uptime/latency of three services, a contribution snake, and a `LAST_UPDATED` marker. Every asset is self-owned under `./header/`.

```html
```
 user   : nipun sujesh
 role   : ai/ml engineer · full-stack developer
 stack  : python · pytorch · react · typescript
 status : building in public
```

<img src="./header/blink_cursor.svg" width="9" height="13" alt="animated cursor" /> <sub>still typing…</sub>
```

```html
<img src="./header/live_systems.svg" height="148" alt="Live status of Serenity, Pragati, and Uni-Verse — pinged daily, real uptime and latency" />
```

```html
<img src="./header/building_uniVerse.svg" alt="Currently building: Uni-Verse — honest, on-the-record platform for college life, built with Next.js and Supabase. Waitlist now open at uni-verse.co.in" width="100%" />
```

**Rating 4/5.** Craft: unusually coherent — one accent color (`#CC4631`) on near-black (`#0d0d0d`) across badges, cards, buttons. Motion: the blinking cursor and live systems card are small but *meaningful* motion. Originality: the point-cloud portrait plus a real `whoami` block is a strong blueprint-flavored combination; GodProfile being dogfooded here matters. Phone: the 52/48 two-column table degrades acceptably. Loses a point for relying on images where text would do.

**Style tags:** `terminal-whoami`, `blueprint-technical`, `hand-made-svg-cursor`, `custom-svg-buttons`, `live-status-card`, `contribution-snake`, `marker-comments`

---

## 9. VARDHAMANPATEL23 — Git Invaders hero + Python SYSTEM IDENTITY — **4/5**

- Profile: https://github.com/VARDHAMANPATEL23
- Raw README: https://raw.githubusercontent.com/VARDHAMANPATEL23/VARDHAMANPATEL23/main/README.md

**What it is:** A rigorously sectioned profile: boxed `╔═╗`-style comment dividers, a self-owned `assets/header.svg`/`footer.svg`, a typing-SVG line, then `◈ SYSTEM IDENTITY` as a literal Python dict, `◈ ACTIVE PROJECTS [4 DEPLOYED]` with numbered `PROJECT 01 — …` entries, and the hero flourish: a Git Invaders (Space Invaders) contribution graph rendered from an `output` branch. Commented-out stats blocks show deliberate restraint.

```python
vardhaman = {
    "location"   : "India 🇮🇳",
    "timezone"   : "UTC +05:30",
    "interests"  : ["IoT", "Computer Vision", "Linux Systems", "AI/ML", "Automation"],
    "current"    : "Building things that blur the line between software and hardware",
    "philosophy" : "If it runs on Linux, I'll hack it."
}
```

```markdown
### ◈ &nbsp;ACTIVE PROJECTS &nbsp;`[4 DEPLOYED]`
```

```html
<img width="100%" src="https://raw.githubusercontent.com/VARDHAMANPATEL23/VARDHAMANPATEL23/refs/heads/output/git-invader-orange-dark.svg" alt="Git Invaders contribution graph" />
```

**Rating 4/5.** Craft: the section system (◈ + boxed comments + numbered projects) is disciplined and reusable. Motion: Git Invaders animates — a literal game over your graph — plus the typing SVG. Originality: the Python dict and `[4 DEPLOYED]` chrome give it a blueprint/schematic voice that stands out. Phone: full-width hero, clean stacks. Loses for a lot of badge noise inside each project block and the header/footer SVGs being the only place the purple theme lives.

**Style tags:** `arcade`, `contribution-graph-reimagined`, `python-dict-bio`, `sectioned-blueprint`, `numbered-projects`, `output-branch-render`, `boxed-comments`

---

## 10. GermanAndresLopez — Animated stats terminal + self-owned SVG banner system — **4/5**

- Profile: https://github.com/GermanAndresLopez
- Raw README: https://raw.githubusercontent.com/GermanAndresLopez/GermanAndresLopez/main/README.md

**What it is:** A tight, dark/blue (`#007AFF`) profile: `assets/banner.svg` hero, a `terminal-readme-github-stats` embed whose commands literally script a session (`whoami → neofetch → languages → uptime → exit`) at `typingSpeed=80` with `art=photo`, a typing SVG, `assets/stack.svg`, standard stats cards, and a dark/light contribution snake. The author owns the banner and stack SVGs locally.

```html
<img src="https://terminal-readme-github-stats.vercel.app/api/stats?username=GermanAndresLopez&theme=material&headerStyle=mac&art=photo&typingSpeed=80&hostname=github.com&commands=whoami%2Cneofetch%2Clanguages%2Cuptime%2Cexit" alt="GitHub Stats Terminal" />
```

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/GermanAndresLopez/GermanAndresLopez/output/github-contribution-grid-snake-dark.svg" />
  <img src="https://raw.githubusercontent.com/GermanAndresLopez/GermanAndresLopez/output/github-contribution-grid-snake.svg" alt="Contribution snake animation" />
</picture>
```

```markdown
### 🚀 Featured Projects
*A few things I've built.*
```

**Rating 4/5.** Craft: cohesive single-accent system, self-owned SVGs, snake with dark/light handling. Motion: the scripted terminal session is genuinely kinetic and tells a mini-story (a real command sequence). Originality: the command-script parameter is the interesting bit — most people paste one default URL. Phone: terminal embed scales well. Loses a point because the rest (badge row, stats trio, markdown project table) is standard 2024-profile fare.

**Style tags:** `animated-terminal`, `scripted-commands`, `self-owned-svg`, `snake-dark-light`, `single-accent`, `typing-svg`

---

## 11. BerkaySevinc — Every band is a self-generated SVG — **3.5/5**

- Profile: https://github.com/BerkaySevinc
- Raw README: https://raw.githubusercontent.com/BerkaySevinc/BerkaySevinc/main/README.md

**What it is:** The README is nearly pure markup orchestration: `assets/header.svg`, `typing.svg`, `divider.svg` (used five times as the only separator), `stats.svg`, `langs.svg`, labeled badge groups, `contribution-snake.svg`, `footer.svg` — all self-owned — wrapped in `<!-- PROFILE:START -->` / `<!-- PROFILE:END -->` markers for programmatic updates. Zero prose; the assets carry everything.

```html
<!-- PROFILE:START -->
<img src="assets/header.svg" width="100%"/>
<img src="assets/typing.svg" width="100%"/>
<img src="assets/divider.svg" width="100%"/>
…
<img src="assets/contribution-snake.svg" width="100%"/>
<img src="assets/footer.svg" width="100%"/>
<!-- PROFILE:END -->
```

```html
<div align="center">
  <img src="assets/labels/lang.svg"/><br>
  <img src="assets/badges/csharp.svg">
  <img src="assets/badges/javascript.svg">
  …
</div>
```

**Rating 3.5/5.** Craft: impressive that *everything* is a local SVG — no third-party stat hosts at all — and the `PROFILE` markers signal a build pipeline. Motion: typing SVG + snake give it movement. Originality: moderate; it's a well-executed "SVG-only" discipline rather than a new idea. Phone: perfect full-width stacking. Loses for zero text: like ryanpolasky, it's invisible to search, screen readers and anyone who blocks images.

**Style tags:** `fully-generated-svg`, `svg-only`, `divider-motif`, `profile-markers`, `no-third-party-hosts`, `badge-labels`

---

## 12. viochris — Responsive 4-way ASCII portrait + a full motion stack — **3.5/5**

- Profile: https://github.com/viochris
- Raw README: https://raw.githubusercontent.com/viochris/viochris/main/README.md

**What it is:** Standard capsule-render/typing-SVG furniture at the top, but the standout is a hand-managed `ascii-portrait/agent-console-*.svg` served through **four** `<picture>` sources — `(min-width: 769px)` × dark/light and `(max-width: 768px)` × dark/light — an ASCII console portrait that adapts to both viewport and theme. Then it stacks an unusually deep motion toolbox: contribution snake, `profile-3d-contrib` isometric (dark rainbow / light green), a `metrics.plugin.isocalendar.svg`, activity graph, and trophies. The body is a very long structured project catalogue.

```html
<picture>
  <source media="(min-width: 769px) and (prefers-color-scheme: dark)" srcset="…/agent-console-ffa7a121-dark.svg">
  <source media="(min-width: 769px) and (prefers-color-scheme: light)" srcset="…/agent-console-ffa7a121-light.svg">
  <source media="(max-width: 768px) and (prefers-color-scheme: dark)" srcset="…/agent-console-ffa7a121-mobile-dark.svg">
  <source media="(max-width: 768px) and (prefers-color-scheme: light)" srcset="…/agent-console-ffa7a121-mobile-light.svg">
  <img src="…/agent-console-ffa7a121-light.svg" alt="ASCII Portrait Animation" width="100%">
</picture>
```

```html
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Hi%20there,%20I'm%20Vio!%20👋&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35" width="100%"/>
```

**Rating 3.5/5.** Craft: the 4-way responsive portrait is the most technically considered `<picture>` usage in this wave. Motion: capsule `fadeIn`, typing, snake, 3D isometric, isocalendar — a lot, if fairly stock. Originality: the ASCII portrait is the only bespoke asset; everything else is popular off-the-shelf. Phone: the responsive portrait proves the point. Loses on bloat — the README is enormous (50+ project rows, WakaTime dumps) and dilutes the motion.

**Style tags:** `ascii-portrait`, `responsive-picture-4way`, `capsule-render-fadein`, `motion-stack`, `snake`, `3d-isometric`, `isocalendar`, `long-form`

---

## 13. OstinUA — Animated GIFs from the author's own readme-SVG tool org — **3.5/5**

- Profile: https://github.com/OstinUA
- Raw README: https://raw.githubusercontent.com/OstinUA/OstinUA/main/README.md

**What it is:** Ostin maintains the `readme-SVG` org (ascii-text-generator, typing-generator, custom-badge-generator, wave-divider-generator, profile-bengo, Issues-heroes-badge) and wires its outputs into his own profile: an animated ASCII GIF hero, a commented-out CSS donut SVG, linked badge generators, an `issues-heroes-badge` live card, two "bengo" game-style cards, a project table, and an 8-bit footer GIF. Layout is a two-column `<table>` with capsule-render rules under headings.

```html
<a href="https://github.com/readme-SVG/ascii-text-generator">
  <img src="https://raw.githubusercontent.com/OstinUA/Image-storage/main/readme/OstinUA_github_readme_v7.gif"/>
</a>
```

```html
<a href="https://github.com/readme-SVG/readme-SVG-profile-bengo">
  <img src="https://readme-svg-profile-bengo.vercel.app/api/card?user=OstinUA&badge=1" width="495" alt="GitHub Stats"/>
</a>
```

```html
[![OstinUA 8bit](https://raw.githubusercontent.com/OstinUA/Image-storage/main/readme/OstinUA_8bit.gif)](https://github.com/OstinUA)
```

**Rating 3.5/5.** Craft: consistent `#3e80ed` accent, tools genuinely his own, GIFs self-hosted in an `Image-storage` repo. Motion: several animated GIFs plus live card endpoints. Originality: the bengo cards and the sheer number of *working* generator tools are notable, but the composition still reads as badge-collage. Phone: tables and full-width GIFs hold up. Loses for sprawl and commented-out dead code left in the source.

**Style tags:** `animated-gif`, `self-built-tooling`, `ascii-text`, `card-generators`, `capsule-rules`, `8bit-footer`, `badge-collage`

---

## 14. Christophe1997 — Token Profile: your AI spend as a profile artifact — **3.5/5**

- Profile: https://github.com/Christophe1997
- Raw README: https://raw.githubusercontent.com/Christophe1997/Christophe1997/main/README.md

**What it is:** Minimal: a commit-history.com embed (dark/light aware) plus the author's own **token-profile** — a `<details>` block whose summary is a live financial statement about his AI usage ("Tokens: 1.3B (-69%) Cost: $455.01 (-66%) Streak: 4 days") with a generated `card-light/dark.svg` underneath. It's a 2026-native idea: treating LLM consumption as a first-class, self-tracked public metric, like a streak graph but for token burn.

```html
<details open>
<summary>Token Profile — Tokens: 1.3B (-69%)   Cost: $455.01 (-66%)   Streak: 4 days</summary>

<picture><source media="(prefers-color-scheme: dark)" srcset=".token-profile/card-dark.svg"><img src=".token-profile/card-light.svg" alt="Token Profile — last 30 days. Tokens: 1.3B (-69%)   Cost: $455.01 (-66%). Streak: 4 days." width="100%"></picture>

Generated by [token-profile](https://github.com/Christophe1997/token-profile)

</details>
```

```html
<a href="https://commit-history.com/Christophe1997">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://commit-history.com/embed/Christophe1997?theme=dark" />
    <img alt="Christophe1997's commit history" src="https://commit-history.com/embed/Christophe1997" />
  </picture>
</a>
```

**Rating 3.5/5.** Craft: tidy, self-generated, marker-delimited (`token-profile:start/end`). Motion: commit-history's embed animates; the card is static. Originality: the *token* framing is the most 2026 idea in this wave — an AI-native stat that nobody else shows. Phone: full-width, fine. Loses because the profile is only two elements; there's almost no design beyond the idea.

**Style tags:** `data-story`, `ai-native-metrics`, `commit-history-embed`, `details-disclosure`, `dark-light-variant`, `self-generated`, `minimal`

---

## 15. abir2afridi — Own animated-banner API in the hero, GIF section headers — **3/5**

- Profile: https://github.com/abir2afridi
- Raw README: https://raw.githubusercontent.com/abir2afridi/abir2afridi/main/README.md

**What it is:** The hero calls the author's own `github-animatedbanner.vercel.app` with a tuned parameter string (`preset=space&pattern=checker&text=Abir&fontSize=78&animation=fadeIn`), followed by a typing SVG, and then a dense collage: tables of about/focus/what-I-do, skillicons rows, activity graph, trophy cards, project table, and every section heading prefixed with an animated icons8 GIF (verified badge, heart balloon, services, github, layers, plant). Capsule-render waving footer. The page ends with an unusual "This repository is protected" notice.

```html
<img src="https://github-animatedbanner.vercel.app/api/banner?preset=space&pattern=checker&text=Abir&fontSize=78&animation=fadeIn&desc=Welcome+to+my+profile&descFontSize=22&descColor=%23c3ad0f"/>
```

```html
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=24&pause=1000&color=3F8CFF&center=true&vCenter=true&width=600&lines=Crafting+High-Performance+Android+Apps;Architecting+Scalable+Cloud+Solutions;Innovating+with+AI+and+System+Design;Turning+Complex+Problems+into+Simple+Code" alt="Typing SVG" />
```

```markdown
### <img src="…/service/services.gif" width="35"/> **Tech Stack**
```

**Rating 3/5.** Craft: organized tables, consistent placement — but visually loud. Motion: plenty (banner animation, typing, many GIFs), though most is stock. Originality: the parameterized own-API hero is the credit; the rest is a maximalist template. Phone: tables and skillicons wrap acceptably. Loses for request weight (a dozen+ GIF endpoints) and the odd copyright/permission footer.

**Style tags:** `animated-banner-api`, `gif-section-headers`, `skillicons`, `typing-svg`, `capsule-footer`, `dogfooding`, `maximalist`

---

## 16. m3hrab — Contribution year as a star constellation — **3/5**

- Profile: https://github.com/m3hrab (README lives on `master`)
- Raw README: https://raw.githubusercontent.com/m3hrab/m3hrab/master/README.md

**What it is:** A restrained monochrome (black/white badges) profile with one bespoke piece: `constellation.svg`, which plots the year's contributions as a star map — brightness encodes commit intensity, lines connect streaks — served dark/light from an `output` branch, with a poetic caption. Above it, a dark/light-aware typing SVG inside a `<picture>` (the typing SVG itself changes text color for theme).

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/m3hrab/m3hrab/output/constellation-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/m3hrab/m3hrab/output/constellation.svg">
  <img alt="A constellation map of GitHub contributions, where each star is a day and brighter stars mean more commits" src="https://raw.githubusercontent.com/m3hrab/m3hrab/output/constellation-dark.svg">
</picture>

<sub>Every star is a day of work. Brightness is intensity, lines are streaks.</sub>
```

```html
<source media="(prefers-color-scheme: dark)" srcset="https://readme-typing-svg.demolab.com/?…&color=FFFFFF&…&lines=Backend+Software+Engineer;Python+%C2%B7+Django+%C2%B7+FastAPI;Building+systems+that+scale+cleanly">
<source media="(prefers-color-scheme: light)" srcset="https://readme-typing-svg.demolab.com/?…&color=111111&…">
```

**Rating 3/5.** Craft: the constellation generator is a genuine idea, well-captioned and theme-aware; everything else is deliberately plain. Motion: the map itself is static (it's a still star chart), the typing SVG moves. Originality: high for the single asset. Phone: perfect — it's one image. Loses because beyond the constellation there's little design system: generic badges, standard copy.

**Style tags:** `generative-art`, `constellation-map`, `theme-aware-typing`, `output-branch-render`, `monochrome`, `captioned-data-art`

---

## 17. saroo98 — Self-owned hero and divider SVGs, quad-line typing, curated GIF accents — **3/5**

- Profile: https://github.com/saroo98
- Raw README: https://raw.githubusercontent.com/saroo98/saroo98/main/README.md

**What it is:** A narrow, deliberate profile: an anime illustration beside `assets/saro-hero.svg`, a four-line typing SVG that states the practice ("Building practical software / Defensive research for real networks / Local-first tools for hard contexts / Publishing systems with memory"), and `assets/saro-divider.svg` as a repeated full-width rule between a tiny animated cat GIF and a keyboard-signature GIF. Everything visual is self-owned under `./assets/`.

```html
<img src="./assets/saro-hero.svg" width="72%" alt="Saro / saroo98 profile hero: defensive research, local tooling, and publishing systems" />
```

```html
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=21&pause=1200&color=7DD3FC&center=true&vCenter=true&width=900&lines=Building+practical+software;Defensive+research+for+real+networks;Local-first+tools+for+hard+contexts;Publishing+systems+with+memory" alt="Typing animation: Building practical software, defensive research for real networks, local-first tools for hard contexts, publishing systems with memory" />
```

```html
<img src="./assets/saro-divider.svg" width="100%" alt="" />
```

**Rating 3/5.** Craft: the restraint is the craft — one accent (`#7DD3FC`), self-made SVGs, real alt text. Motion: typing + two small GIFs; the divider itself is static. Originality: the quad-line practice statement is a good writing move more than a visual one. Phone: clean stacking. Loses for thinness — a stats card and profile-views badge are the only other substance, and the default GitHub comment scaffold is still sitting in the file.

**Style tags:** `hero-svg`, `divider-motif`, `typographic-practice-lines`, `curated-gifs`, `self-owned-assets`, `minimal`, `alt-text-rich`

---

## 18. DhanushNehru — ScribeSVG typing render + the animated divider as a motif — **3/5**

- Profile: https://github.com/DhanushNehru (README lives on `master`)
- Raw README: https://raw.githubusercontent.com/DhanushNehru/DhanushNehru/master/README.md

**What it is:** The hero is a call to the author's own **ScribeSVG** service (a readme-typing-svg alternative): three lines of kinetic copy, center-aligned, rendered by his own app. Below, `assets/animated-divider.gif` is used *six* times as the profile's only section separator — a deliberate rhythm device. The rest is long-form: article lists between `MEDIUM-BLOG-LIST` markers, YouTube embeds between marker comments, stats, Holopin/community badges.

```markdown
[![Typing SVG](https://scribesvg.vercel.app/api/render?lines=Tech+Autodidact,+Engineer,+Programmer;Loves+to+solve+technology+problems+by+code;Likes+to+build+scalable%2C+secure+applications&font=Fira+Code&size=24&color=36bcf7&center=true&width=700&height=50)](https://github.com/DhanushNehru/ScribeSVG)
```

```html
<picture>
  <img src="https://github.com/DhanushNehru/DhanushNehru/blob/master/assets/animated-divider.gif" align="center"  width="100%" alt="Animated Divider Image">
</picture>
```

**Rating 3/5.** Craft: the divider-as-only-separator is a real editorial decision; ScribeSVG is dogfooded with a credit link. Motion: typing render + always-on divider GIF — but the divider repeats so often it becomes wallpaper, and the GIF re-loads six times. Originality: moderate; ScribeSVG is a typing-SVG clone. Phone: fine, heavy. Loses for bloat (YouTube tables, article dumps) and `blob/master` image URLs that don't render as raw SVG/GIF reliably in all contexts.

**Style tags:** `kinetic-typing`, `self-built-service`, `animated-divider-motif`, `marker-comments`, `long-form`, `master-branch`

---

## 19. Spectrewolf8 — Self-deployed isometric 3D contribution graph — **3/5**

- Profile: https://github.com/Spectrewolf8
- Raw README: https://raw.githubusercontent.com/Spectrewolf8/Spectrewolf8/main/README.md

**What it is:** Almost the entire visual is one embed: `isometric-contributions-spectrewolf8.onrender.com/api/graph` — the author's own deployment of his isometric-3D-graphs project (≈160 users), rendering his year as an isometric grid with stats, dark theme, credited. The text around it is plain but characterful: he names the projects he's proud of (an RL autodriver in Unity, an ASCII video player in PyQt5, the isometric graphs themselves).

```html
<img width="700" src="https://isometric-contributions-spectrewolf8.onrender.com/api/graph?username=spectrewolf8&theme=dark&stats=true&credit=true"></img>
```

```markdown
- ✨ You can check out some of my other ambitious projects here:
  - [Isometric 3D GitHub Contribution Graphs](https://github.com/Spectrewolf8/GitHub-Contributions-Isometric-3D-Graphs-Embed) which now has ~160 users and growing. <sup>(the graph above was made by it)</sup>
```

**Rating 3/5.** Craft: the isometric graph is good and self-hosted (own Render instance, not the public service). Motion: the graph is a static render — pretty, not moving. Originality: moderate; isometric-contributions as a concept predates this, but deploying and crediting your own instance is the right move. Phone: `width=700` fixed attribute can overflow narrow screens. Loses for being a single image plus prose — no design system at all.

**Style tags:** `isometric`, `contribution-graph-reimagined`, `self-hosted-instance`, `dogfooding`, `minimal`, `fixed-width-embed`

---

## 20. NissonCX — Localized capsule-render profile with GIF table — **2.5/5**

- Profile: https://github.com/NissonCX
- Raw README: https://raw.githubusercontent.com/NissonCX/NissonCX/main/README.md

**What it is:** A Chinese-language (zh) student profile: a capsule-render waving header with `animation=fadeIn` reading "你好，我是 NissonCX 👋" plus a personalized `desc`, an animated Fluent-emoji laptop GIF, a two-cell `<table>` of Giphy loops (TypeScript learning / coding cat), standard shields, and a closing "保持好奇心，继续造轮子！" (Stay curious, keep building wheels) with a contact GIF.

```html
<img src="https://capsule-render.vercel.app/api?type=waving&height=250&color=gradient&customColorList=2,15,22,25,28&text=你好，我是%20NissonCX%20👋&fontSize=60&fontAlignY=40&animation=fadeIn&desc=一个热衷于技术细节的“全干”摸鱼王&descAlignY=65" alt="NissonCX Header" />
```

```markdown
### 💡 “保持热爱，折腾不止，把每一个技术细节发掘到极致！”
```

```html
<td width="50%"><div align="center"><img src="https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif" width="100" alt="Learning GIF"/><br/><b>TypeScript & Node.js</b>…
```

**Rating 2.5/5.** Craft: the header's gradient stops and desc positioning are tuned with care, and the voice is warm and specific (Barça, LinuxDo, a campus football run). Motion: capsule `fadeIn` plus third-party Giphy loops — all off-the-shelf. Originality: low; this is the common localized template family. Phone: fine. Loses points for hotlinked Giphy (link rot risk), heavy bilingual mismatch for non-zh readers, and no bespoke assets.

**Style tags:** `capsule-render-fadein`, `bilingual-zh-en`, `giphy-gifs`, `localized-template`, `animated-emoji`

---

## What's new in 2026 profiles (vs. the older archetype)

Comparing these 20 against the older "stats-card" archetype (and wave 1 in Part 06), several shifts are genuinely new:

1. **The profile is now a build artifact, not a document.** The strongest 2026 profiles are *generated*: `profile.config.json` + nightly Action (lennystepn-hue), an `output` branch rendering SVGs on a schedule (okturan, m3hrab, VARDHAMANPATEL23, Luc0-0), `PROFILE:START/END` marker regions (BerkaySevinc, Luc0-0, Christophe1997), or config-in → SVG-out pipelines (williamzujkowski's `svg-terminal`, t1seo's snapshot JSON). "Hand-edit the README" is increasingly wrong; the README is an artifact with a source of truth behind it.

2. **Dogfooding became the credibility signal.** The wave-1 pattern "I made the tool this profile uses" is now table stakes at the top: `svg-terminal` (williamzujkowski), `github-blocks` (okturan), YourTomo (prsdx), CommitCraft (WJZ-P), GodProfile (Luc0-0), ScribeSVG (DhanushNehru), RyMe.md (ryanpolasky), readme-SVG (OstinUA), the isometric-graph instance (Spectrewolf8), `attract-mode` (lennystepn-hue), token-profile (Christophe1997). A generic stats URL now reads as *less* credible than a self-hosted one.

3. **Contribution graphs became scenes, not heatmaps.** Beyond wave 1's snake (platane) and Game of Life (ethomson), 2026 adds: a walkable 3D village (t1seo), a lane-defense game where commit days are towers (okturan), Space Invaders (VARDHAMANPATEL23), an isometric Minecraft world (WJZ-P), a cat hopping weekly peaks (prsdx), a star constellation (m3hrab), an isometric cat-city (prsdx again). The heatmap itself is now considered boring; the graph is a canvas for a *narrative*.

4. **Motion got accessibility treatment.** The `prefers-reduced-motion` twin (williamzujkowski's `terminal-static.svg`) and viewport-aware `<picture>` sets (viochris's 4-source ASCII portrait) are new hygiene standards. Theme-awareness is now expected: nearly every bespoke SVG in this wave ships a dark *and* light variant.

5. **AI-era metrics arrived.** Christophe1997's Token Profile (tokens, dollar cost, streak) is the first profile stat that couldn't have existed before LLMs — and it's framed with the same grammar as contribution streaks. Expect more "AI usage as public stat" patterns.

6. **The collage is losing to the system.** The older archetype stacks shields.io badges, three stat cards, a snake and an activity graph (see abir2afridi, viochris, DhanushNehru — the wave's lower-rated entries). The wave's high scorers each pick *one* strong visual language (terminal, arcade, isometric, editor window, constellation) and hold a single accent color across every asset. Restraint, not accumulation, is what now reads as expensive.

7. **Localized profiles form their own template family.** zh-language profiles (WJZ-P, NissonCX) lean on capsule-render + moe-counter + Giphy in a recognizable pattern; WJZ-P breaks out of it via CommitCraft, NissonCX does not. Same dynamics as the umang-eng/harkirat-data family in SHORTLIST.md, different culture.

**Gaps / honest limitations:** Everything here was verified by raw README fetch, not by rendering — animation *quality* (frame rate, easing, whether an SVG actually loops) is inferred from source and alt text. Fixed-width embeds (Spectrewolf8's `width=700`) and 404-prone branches (profiles defaulting to `master` rather than `main`) were the two most common mobile/rot issues noticed. Several top-rated profiles (t1seo, ryanpolasky, BerkaySevinc) trade all text for images — a real accessibility and SEO cost that the ratings above call out.
