# The visual frontier

The next phase of the research: how far can a profile README be pushed toward a
next-generation, game-quality, *3D-looking* visual — while still loading
everywhere, reading on a phone, respecting reduced motion and renting nothing?

A README can't run code, so there are exactly two roads to 3D:

1. **Fake it in SVG** — isometry, parallax, depth fog, and (new here) real SVG
   *lighting*. Tiny, crisp, themeable, legible.
2. **Render real 3D elsewhere and ship the frames** — a scene rendered in CI,
   delivered as an animated image, with vector text laid over it.

Both are built side by side, so the comparison is measured rather than argued.

| # | Step | Status |
|---|---|---|
| A | Do SVG lighting filters work inside an image, in every engine? | **done** |
| B | Which animated image formats does GitHub animate — and pause? | **done** |
| C | Real-3D render pipeline in CI | next |
| D | Pure-SVG lit 2.5D flagship | next |
| E | Side-by-side flagship page, both measured | — |

---

## A · SVG lighting

`feSpecularLighting` and `feDiffuseLighting` turn a shape's alpha into a height
map and light it — embossed metal, glass edges, foil. Nothing in the 446-profile
survey uses them, and this repository had never tested them.

Fixtures: one per light type, each with an unfiltered control
([`fixtures/`](fixtures), built by [`tools/frontier/fixtures.py`](../../tools/frontier/fixtures.py)).
Probed on github.com by [`tools/frontier/probe_gh.mjs`](../../tools/frontier/probe_gh.mjs),
screenshot-compared against the control:

| Fixture | Chromium 153 | Firefox 155 | WebKit 26.6 |
|---|---|---|---|
| specular · distant light | lit | lit | lit |
| specular · point light | lit | lit | lit |
| specular · spot light | lit | lit | lit |
| diffuse · distant light | lit | lit | lit |
| specular · **moving** point light | lit · **animates** | lit · **animates** | lit · **animates** |

**All five light, in every engine, and a light that moves animates everywhere.**
An animated `fePointLight` is a highlight that sweeps across a surface — the
single most "real-looking" effect SVG can produce — and it is safe.

## B · Animated images

One 24-frame animation, encoded four ways, then embedded inside SVGs:

| Format | Size | Served as |
|---|--:|---|
| GIF | 33.9 KB | `image/gif` |
| APNG | 29.9 KB | `image/png` |
| animated WebP | 20.9 KB | `image/webp` |
| animated AVIF | **4.5 KB** | `image/avif` |

GitHub serves all four with the correct content type. On github.com:

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| GIF | moves · **GitHub player** | moves · **GitHub player** | moves · **GitHub player** |
| APNG | moves | moves | moves |
| animated WebP | moves | moves | moves |
| animated AVIF | moves | moves | *does not decode* † |
| GIF / APNG / WebP **inside an SVG** | moves | **frozen on one frame** | moves |
| AVIF inside an SVG | moves | frozen | *does not decode* † |

And with `prefers-reduced-motion: reduce`:

| | Chromium | Firefox | WebKit |
|---|---|---|---|
| GIF | **paused** | **paused** | **paused** |
| APNG, WebP, AVIF, anything inside an SVG | keeps moving | keeps moving | keeps moving |

### What that means

1. **GitHub wraps GIFs — and only GIFs — in an `<animated-image>` player** with a
   play/pause control and a canvas still frame, and **pauses them for viewers who
   asked for reduced motion.** GIF is therefore the one animated format that is
   accessible by default.
2. **Every other format ignores reduced motion.** Ship APNG, WebP or AVIF behind a
   `<picture>` source gated on `prefers-reduced-motion`, pointing at a still —
   the mechanism [Track 2](../research/REDUCED-MOTION.md) verified.
3. **Animated WebP is the practical choice for rendered 3D**: plays in all three
   engines, a third smaller than GIF, full colour instead of GIF's 256.
4. **Frames inside an SVG work in Chromium and WebKit but freeze in Firefox.** So
   "a rendered scene with crisp SVG text on top, in one file" is viable only if
   the frozen frame is itself a finished composition.
5. **AVIF is 7× smaller than GIF but did not decode in the WebKit build tested.**
   † That build is Playwright's WebKit on Windows; Safari itself has supported
   AVIF since version 16, so this may be the build, not Safari. **UNVERIFIED** —
   and until it is, AVIF isn't safe as the only file.

### A mistake in the method, caught

The first GitHub pass reported GIF as failing to decode in all three engines.
Inspecting the DOM showed why: the `<animated-image>` player inserts a hidden,
zero-sized duplicate `<img>` with the same alt text, and the probe let it
overwrite the visible one. The probe now keeps only visible images and records
which ones GitHub wrapped — which is how finding 1 surfaced at all.
