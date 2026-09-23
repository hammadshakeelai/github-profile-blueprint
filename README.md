# GitHub Profile README — research

Evidence-first research into what makes an exceptional GitHub profile README:
what the best ones do, what actually renders, what breaks, and why. It feeds a
reusable skill and, eventually, a profile designed from the findings.

This is the v2 restart. The earlier infrastructure-first work (compiler, commit
dispatcher, CI research) is preserved unchanged on the
[`archive/v1`](https://github.com/hammadshakeelai/github-profile-blueprint/tree/archive/v1)
branch.

## Progress

| Phase | Status |
|---|---|
| 1 · Survey — 446 real profiles, their images, and the generators behind them | **done** |
| 2 · Technique catalogue — each technique with real users and a verified example | **done** |
| 3 · Capability matrix — Chromium, Firefox and WebKit, phone and desktop, dark and light | **done** |
| 4 · Design direction — three rendered concepts, one chosen | in progress |
| 5 · Build the profile | |
| 6 · Fold everything back into the skill | |

Plan: [docs/PLAN-V2.md](docs/PLAN-V2.md)

## What the survey found

Full detail with numbers in [docs/survey/FINDINGS.md](docs/survey/FINDINGS.md).

- **41% of profiles show a broken image.** The biggest single cause: free-tier
  Vercel deployments being switched off. The public github-readme-stats
  instance loads 0% of the time and is still embedded in 24% of profiles.
- **55% of SVG cards are unreadable on a phone**, and 90% of those are
  legible at full size — the 309px mobile column shrinks them. Hand-made cards
  fail more often than generator services (63% vs 37%).
- **The most visually ambitious profiles are the least readable on phones.**
  Nobody surveyed is both ambitious and legible at 309px — that's the gap to
  design into.
- **Only 20% switch between dark and light**, and 42% are more than half
  badges.

The fifteen standout profiles, and what to take from each:
[docs/survey/SHORTLIST.md](docs/survey/SHORTLIST.md).

## What works where

[docs/CAPABILITY-MATRIX.md](docs/CAPABILITY-MATRIX.md) — every technique tested
in Chromium, Firefox and WebKit (Safari's engine), at phone and desktop width,
dark and light.

- **Everything animates in every engine — with one exception.** WebKit never
  animates `gradientTransform`; animate the gradient's `x1`/`x2` or its stop
  offsets instead.
- **External images are blocked everywhere, but differently**: Chromium paints
  a broken-image icon, Firefox and WebKit draw nothing.
- **A pushed change takes about five minutes to appear** (the CDN serves the
  old file for `max-age=300`); a commit-pinned URL is fresh in seconds.

## What the technique catalogue verified

Every technique found in the survey, rebuilt as an original minimal example and
checked on GitHub's real renderer at desktop and phone width, dark and light:
[docs/techniques/CATALOGUE.md](docs/techniques/CATALOGUE.md).

- **All 14 animated examples run inside GitHub's page** — SMIL, CSS keyframes,
  line drawing, masks, typing, textPath, gauges, charts — confirmed by
  frame-differencing, not assumed.
- **Theme switching works three ways**: `<picture>`, the legacy
  `#gh-dark-mode-only` fragments, and media queries inside the SVG.
- **Blocked:** scripts, `@import`ed web fonts, and external images — which
  don't vanish quietly but show a broken-image icon.
- **Renders (in Chrome):** HTML inside `<foreignObject>`.

## Layout

```
docs/
  PLAN-V2.md                 the plan
  survey/                    Phase 1: findings, shortlist, tables, screenshots, data
skills/github-profile-readme/  the skill — measured constraints, banner craft, SVG recipes
tools/survey/                the survey tooling; everything re-runs from here
```
