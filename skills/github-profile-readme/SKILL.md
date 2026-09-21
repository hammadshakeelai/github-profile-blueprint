---
name: github-profile-readme
description: Use when designing, building, reviewing or debugging a GitHub profile README (the username/username repo) or any README banner, hero image, stats card, or generated SVG asset. Covers the measured rendering constraints that decide whether a design actually works — content widths, mobile legibility math, which SVG features survive, font loading, Camo vs raw asset routing, and cache behaviour — plus CI patterns for self-updating profiles. Trigger on "profile README", "README banner", "hero image", "github profile", "readme svg", "profile stats card", or when a banner "looks tiny/blurry/wrong on mobile".
---

# GitHub Profile README Engineering

Most profile-README advice is aesthetic. The things that actually break a profile
are dimensional and infrastructural, and they are measurable. This skill leads
with the measurements.

## The three numbers that decide everything

Measured directly from rendered DOM on github.com (September 2026), profile
README container (`.js-profile-readme article.markdown-body`):

| Viewport | README content width |
|---|---|
| 1920px desktop | **846px** |
| 1280px laptop | **831px** |
| 390px phone | **309px** |

Images are hard-capped to the container: a 854px-natural image renders at 846px.

**309px is the number that kills banners.** Nearly every profile banner in the
wild is designed at 1200px+ and is illegible on a phone. Check it first.

## The legibility formula — apply before drawing anything

An SVG banner scales as a unit. Text does not stay put; it shrinks with the
viewBox. For text drawn at size `F` in a viewBox of width `W`, rendered into a
container of width `R`:

```
effective_px = F × (R / W)
```

Solve for the minimum size that stays legible (`11px` is the floor for
supporting text; `13px` for anything that must be read):

```
F_min = target_px × W / R
```

Worked, for a 1200-wide viewBox:

| Target | Desktop (R=846) | Mobile (R=309) |
|---|---|---|
| 11px legible | F ≥ 16 | F ≥ **43** |
| 13px comfortable | F ≥ 19 | F ≥ **51** |

So in a 1200-unit viewBox, **every piece of text must be ≥43 units** or it is
unreadable on a phone. That is much larger than it looks in a design tool, and it
is why most banners fail.

Three ways out, in order of preference:

1. **Shrink the viewBox, not the type.** A 900-unit viewBox needs only F ≥ 32 for
   mobile legibility. Design at roughly the real display width and the ratio stops
   fighting you.
2. **Cut the text.** A banner with a name and one line beats a banner with four
   lines of unreadable detail. Move detail into markdown below, where it reflows.
3. **Accept desktop-only** for one decorative line, deliberately — and never for
   the name or role.

**SVG banners do not need 2× dimensions for retina.** SVG is resolution
independent; it renders sharp at any scale. The common "export at 2× for retina"
advice applies to PNG/JPG only. For SVG the viewBox is a *coordinate system*, not
a resolution — only the ratio above matters. Getting this wrong is what leads
people to 2400px viewBoxes with 20px type.

## Fonts: your web font is not loading

An SVG referenced as an image cannot *load* anything external: `@import`,
`<link>`, and `@font-face` pointing at a URL are all blocked. So a declaration
like `font-family: 'JetBrains Mono', monospace` only renders as JetBrains Mono
for viewers who **already have it installed**. Everyone else silently gets the
next font in the stack — with no error.

That makes the stack itself the design decision. Keep the preferred face first
(it costs nothing and rewards viewers who have it), then real system fonts, so
the fallback is deliberate rather than whatever the browser defaults to.

Options:

- **Design for the fallback stack.** Simplest and most robust:
  `'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace` or
  `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`. Accept
  per-platform variation. Note `ui-monospace` is the real token;
  `-apple-system-ui-monospace` is not valid CSS and is ignored.
- **Embed the font as base64.** Subset the glyphs you actually use, base64 a
  WOFF2, inline it in an `@font-face` inside the SVG's `<style>`. Full fidelity,
  but a full font is 100KB+ — subset aggressively or the file balloons.
- **Convert text to paths.** Perfect fidelity, no font dependency. Costs you
  selectable/searchable text and makes edits require a re-render. Good for a
  wordmark, bad for anything generated.

## What survives when an SVG is referenced as an image

Referencing an SVG via `<img>` or markdown `![]()` puts the browser in the SVG
spec's **secure animated mode**. This is browser behaviour, not a GitHub policy:

| Feature | Survives? |
|---|---|
| SMIL animation (`<animate>`, `animateMotion`) | **Yes** |
| CSS `@keyframes` inside the SVG | **Yes** |
| `<script>`, event handlers | No |
| Hover, click, tooltips, interactivity | No |
| External font / stylesheet / image refs | No |
| Inline `<svg>` pasted into markdown | Stripped by sanitizer |

So: animation yes, interaction no. Anything needing interactivity must be faked —
usually a link wrapping the image, or GitHub Issues as the input channel.

## Asset routing: repo-relative vs external

Verified on live rendered DOM:

- **Repo-relative** (`./assets/banner.svg`) → rewritten to
  `github.com/{owner}/{repo}/raw/{branch}/{path}`. **Not Camo-proxied.**
  Cache-Control `max-age=300` (5 min) on branch HEAD.
- **External** (`https://some-service/card.svg`) → proxied through
  `camo.githubusercontent.com` with an HMAC-SHA1 digest URL, cached aggressively.

Consequences:

- Committed assets update within ~5 minutes. Predictable. Prefer them.
- External services are cached hard and can serve stale content long after the
  origin changes. Bust with a changing query param (it changes the Camo digest,
  forcing a re-fetch), or send `Cache-Control: no-cache, no-store, must-revalidate`
  from the origin.
- External services are also a liveness dependency: a rate-limited or down
  third party shows a broken image on your profile. Generate and commit instead
  wherever you can.
- On the **profile** page, relative paths inside `<picture><source srcset>` can
  fail to resolve because the base URL lacks the repo slug. Use absolute
  `raw.githubusercontent.com` URLs inside `<picture>`; relative paths are fine for
  plain `<img>`.

## Dark and light

```html
<picture>
  <source media="(prefers-color-scheme: dark)"  srcset="<absolute-raw-url>/banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="<absolute-raw-url>/banner-light.svg">
  <img alt="<describe the banner, don't say 'banner'>" src="<absolute-raw-url>/banner-dark.svg" width="100%">
</picture>
```

Do not try to do this with CSS media queries *inside* one SVG — in secure
animated mode the SVG cannot read the host page's colour scheme reliably. Two
files and `<picture>` is the pattern that works.

## Process

1. **Measure the target first.** 846 desktop / 309 mobile. Write down the viewBox
   you will use and run the legibility formula before drawing.
2. **Decide generated vs static.** Generated (CI-built SVG committed to the repo)
   only if something genuinely changes. Static otherwise — a cron that rewrites
   identical bytes is pure noise.
3. **Build for the fallback font** unless you are embedding a subset.
4. **Verify at 309px** before shipping. Render it small and try to read it.
5. **Check idempotency** if generated: run the generator twice with no input
   change and diff. Non-deterministic output (timestamps, dict order, random ids)
   means a commit every run, forever.

## Anti-patterns

- A 1200px+ viewBox with sub-40 type — illegible on mobile, the single most
  common failure.
- Badge walls. Fifteen shields.io badges read as noise and each is a Camo fetch.
- Fake metrics. Invented "99.8% reliability" or seeded guestbook entries with
  `@octocat` read as dishonest to anyone who looks closely, and are worse than no
  metrics.
- Claims that outrun the evidence ("formally verified Raft") — the profile is
  read by people who will ask about them in an interview.
- `<script>` or `onclick` in SVG — silently stripped, wasted effort.
- Third-party stats services on the critical path of your first impression.
- Cron every 6h on content that changes monthly.

## References

- `references/measured-constraints.md` — the raw measurements, method, and how to
  re-measure when GitHub changes its layout.
- `references/banner-craft.md` — composition, type scale, and the legibility
  worksheet.
- `references/svg-recipes.md` — copy-paste SVG patterns verified to render.
