---
name: github-profile-readme
description: Use when designing, building, reviewing or debugging a GitHub profile README (the username/username repo) or any README banner, hero image, stats card, or generated SVG asset. Built on a survey of 446 real profiles and capability captures in three browser engines — it covers what actually breaks (dead image services, phone-illegible SVG text, table layouts), the measured container widths and legibility math, which SVG features survive GitHub's renderer, theme switching, cache timing, and how to verify a design instead of guessing. Trigger on "profile README", "README banner", "hero image", "github profile", "readme svg", "profile stats card", or when a banner "looks tiny/blurry/wrong on mobile".
---

# GitHub Profile README Engineering

Most profile-README advice is aesthetic and unsourced. This skill is built from
measurement: 446 real profiles surveyed with every image fetched and every
layout measured, and every rendering claim captured in Chromium, Firefox and
WebKit inside GitHub's own page.

Two reference files carry the evidence. Read the relevant one before asserting
anything:

- [`references/evidence.md`](references/evidence.md) — what 446 profiles do, and
  the four ways they fail, with rates.
- [`references/platform-facts.md`](references/platform-facts.md) — what renders,
  per engine, plus widths, cache timing and asset routing.

If a claim appears in neither, say it is unverified. Fluent writing that sounds
researched is the failure mode this skill exists to prevent.

## Start here: the four failures

Measured across the survey. Check any new profile against these before
designing anything.

| Failure | Rate in the wild | The rule that avoids it |
|---|---|---|
| A broken image on the page | **41%** | Commit every image to the repo. Committed images load 99% of the time; the public github-readme-stats instance loads **0%** and is still embedded in 24% of profiles. |
| SVG text illegible on a phone | **55%** of 1,730 cards | Run the legibility formula below on every card, not just the banner. 90% of failures are legible at full size and die only in the 309px column. |
| Badge wall | **42%** of profiles | Badges are not information. Fifteen shields read as noise and each is a Camo fetch. |
| No dark/light | 80% don't | Two files behind `<picture>`. |

Hand-made cards fail the phone **more** than generator output (63% vs 37%) —
being the designer is not protection, it is the risk.

## The three numbers

| Viewport | README column |
|---|---|
| 1920px desktop | **846px** |
| 1280px laptop | **831px** |
| 390px phone | **309px** |

Images are hard-capped to the column. **309px is the number that kills
banners.**

## The legibility formula — apply before drawing anything

An SVG scales as a unit; text shrinks with the viewBox. For text at size `F` in
a viewBox of width `W`, rendered into a column of width `R`:

```
effective_px = F × (R / W)          F_min = target_px × W / R
```

11px is the floor for supporting text, 13px for anything that must be read. For
a 1200-wide viewBox that means **F ≥ 43 units** for phone legibility — far
larger than it looks in a design tool, and why most banners fail.

Three ways out, in order:

1. **Shrink the viewBox, not the type.** Design at roughly the real display
   width. A 600-unit viewBox needs only F ≥ 21.4; the arithmetic stops fighting
   you.
2. **Cut the text.** A name and one line beats four lines nobody can read. Put
   the detail in markdown, where it reflows.
3. **Accept desktop-only** for one decorative line, deliberately — never for the
   name.

**Enforce it in code.** A generator should refuse to emit an SVG whose smallest
text would fall below the floor; a working example is `check()` in
`tools/direction/build.py`. A rule you have to remember is a rule you will
forget on the last card.

**SVG does not need 2× dimensions for retina.** It is resolution independent.
The viewBox is a coordinate system, not a resolution — that advice is for
PNG/JPG, and following it is what produces 2400px viewBoxes with 20px type.

## Layout: markdown reads, SVG sets atmosphere

Real text reflows on a phone; an image cannot. Every sentence a visitor must
read belongs in markdown; the SVG carries identity.

**Do not lay out with tables.** 21% of profiles put images in tables, and on a
phone GitHub either crushes the cards — 640px cards measured at **76px** — or
scrolls the table sideways. One column, stacked, always.

**The only interaction available is a link.** Scripts and hover are blocked
inside the image, but wrapping a `<picture>` in an `<a>` makes an entire panel a
tap target — the largest control a README can have. Use it instead of faking
interactivity.

## Alt text is the only way out of the image

A card's words are pixels. The `alt` attribute is the only channel back out,
and that is measured: an `<img>` whose SVG declares `role="img"`, an
`aria-label`, a `<title>` *and* a `<desc>` exposes an accessible name of `""`.
Nothing inside the file crosses the boundary — so don't bother labelling in
there, and never treat it as a substitute.

In the survey, **954 of 2,527 text-bearing SVG cards (37.8%) have no usable
alt** — absent, empty, the filename, or a word like "banner". 61 profiles
describe nothing at all.

- Write what the card **says**: `"LinuxWeb: real Alpine Linux in a browser tab"`.
- `alt=""` is right for decoration and wrong for anything carrying information.
- If the alt is hard to write, the card is carrying too much — move it to
  markdown, where it is readable, reflowable and searchable anyway.

## What survives inside the image

Referencing an SVG via `<img>` or `![]()` puts the browser in the SVG spec's
**secure animated mode**: declarative animation runs, everything interactive or
external does not. Verified identically in all three engines.

| | |
|---|---|
| SMIL, CSS `@keyframes`, masks, stroke-dash, `textPath`, filters | **all animate, all engines** |
| `gradientTransform` animation | **WebKit never animates it** — animate `x1`/`x2` or stop offsets |
| `<script>`, event handlers, hover, tooltips | blocked |
| `@import`ed web fonts | blocked |
| External `<image>` href | blocked — and Chromium **paints a broken-image icon** |
| Inline `<svg>` in markdown | stripped by the sanitizer |
| `@media (prefers-reduced-motion)` inside the SVG | **never applies** — gate a `<picture>` source instead |

## Fonts: your web font is not loading

An SVG referenced as an image cannot load anything external, so
`font-family: 'JetBrains Mono', monospace` renders as JetBrains Mono only for
viewers who already have it installed. Everyone else silently gets the next
entry — with no error. The stack is therefore the design decision, not the first
name in it.

- **Design for the fallback stack**, e.g. `'JetBrains Mono', ui-monospace,
  SFMono-Regular, Menlo, Consolas, monospace`. (`ui-monospace` is the real
  token; `-apple-system-ui-monospace` is not valid CSS.)
- **Embed a subset as base64** for full fidelity — subset aggressively, a whole
  font is 100KB+. 13 surveyed profiles do this.
- **Convert text to paths** for a wordmark. Perfect, unsearchable, and painful
  to regenerate.

Because the face varies per viewer, never let a layout depend on exact text
width. Where it must — a typing effect, a right-aligned label — use `textLength`
so the glyphs are forced into the space you reserved.

## Dark and light

```html
<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-light.svg">
  <img alt="describe the content, not the word banner" src="https://raw.githubusercontent.com/OWNER/REPO/main/assets/banner-dark.svg" width="600">
</picture>
```

All three theme mechanisms work — `<picture>`, the legacy `#gh-dark-mode-only`
fragments, and `@media` inside the SVG. The real caveat is that every one of
them follows `prefers-color-scheme`, i.e. the viewer's **operating system**, not
their GitHub theme setting; nothing inside an image can read GitHub's theme.
Prefer `<picture>` because one theme per file is easy to verify.

Use absolute `raw.githubusercontent.com` URLs in `srcset` — identical in a repo
README, a profile README and anywhere else the markdown is read. Relative paths
also resolve correctly on profile pages (33 of 33 live profiles checked), so
don't treat someone else's relative srcset as a bug.

Point the `<img>` fallback at the variant you'd rather have seen, and make sure
that file exists — it is what any client ignoring `<source>` fetches.

## Process

1. **Measure the target first.** 846 / 309. Write down the viewBox, run the
   formula, and only then draw.
2. **Design the first frame as the finished composition.** Anything that starts
   at `opacity="0"` and animates in is invisible to every static renderer — and
   was caught doing exactly that, at phone width, during this research.
3. **Commit every asset.** Generated and committed, never rented.
4. **Respect reduced motion where the page can see it.** A guard inside the SVG
   does nothing; a `<source media="(prefers-reduced-motion: reduce)">` pointing
   at a still file works in all three engines. Best of all, design so the still
   frame is the whole composition and the question is moot.
5. **Decide generated vs static honestly.** CI only if a value genuinely
   changes; a cron rewriting identical bytes is noise. If generated, run it
   twice with no input change and diff — non-deterministic output (timestamps,
   dict order, random ids) means a commit every run, forever.
6. **Verify on GitHub, not locally.** Push to a branch, open the rendered page,
   and measure: each image's rendered width, its smallest text × (width ÷
   viewBox), both schemes, 390px and 1280px. Local preview shows you neither the
   sanitizer, nor the column width, nor a broken image.
7. **Wait five minutes.** `max-age=300`: a pushed change takes ~302s to appear on
   a branch URL. Half of "my SVG didn't update" is this.

## Anti-patterns

- A 1200px+ viewBox with sub-40 type — the most common failure there is.
- Third-party image services on the critical path of a first impression.
- Badge walls; fake metrics; claims that outrun the evidence. All three read as
  dishonest to exactly the people who look closely.
- Tables used for layout.
- `<script>` or `onclick` in an SVG — stripped, always.
- Copying a stat card because it is popular. The most-copied one has been dead
  for months and its repository metadata still says "active".

## References

- [`references/evidence.md`](references/evidence.md) — the survey: rates, per-service liveness, technique counts.
- [`references/platform-facts.md`](references/platform-facts.md) — per-engine capability, widths, cache timing, routing.
- [`references/measured-constraints.md`](references/measured-constraints.md) — raw measurements and how to re-measure when GitHub changes.
- [`references/banner-craft.md`](references/banner-craft.md) — composition, type scale, legibility worksheet.
- [`references/svg-recipes.md`](references/svg-recipes.md) — copy-paste patterns verified to render.

A worked end-to-end example — design rules, six generated cards, and the
measurement confirming 11.9px smallest text on a phone — is
[`docs/PROFILE.md`](../../docs/PROFILE.md), built by `tools/profile/build.py`.
