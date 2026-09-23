# Track 5 · Narrowing the iOS unknown

The capability matrix ends with rows marked unverified: iOS Safari and the
GitHub mobile apps, neither of which can be driven from this machine. This track
shrinks that gap as far as honesty allows and states precisely what is left.

## What was run

WebKit 26.6 — Safari's engine — with **actual iPhone device emulation** rather
than a narrow window: an iOS 18 Safari user agent, `deviceScaleFactor: 3`,
`isMobile`, touch. `DEVICE=iphone` in `tools/matrix/capture.mjs`. The full
technique gallery, both schemes, on GitHub's own rendered page.

Previously the 390px WebKit pass was a narrow desktop viewport, which keeps
desktop layout semantics; this is the closer proxy the matrix said was missing.

## Results

| | Emulated iPhone (WebKit) | Desktop WebKit |
|---|---|---|
| Techniques rendered | 22 of 23 | 22 of 23 |
| Animating | 13 | 13 |
| Not animating | `gradient-transform.svg` | `gradient-transform.svg` |
| Images failing to load | none | none |
| `<picture>` theming | dark → `theme-picture-dark.svg`, light → `theme-picture-light.svg` | same |
| `#gh-dark-mode-only` fragments | both files present, fragment-selected | same |
| In-SVG `@media` theming | card differs between schemes | same |
| README column | 324px (this is a repo blob page; a profile page's is 309px) | 831px |

**Nothing changed under iPhone emulation.** Every technique that animates on a
desktop animates here; the one WebKit exception stays the exception; theme
switching works all three ways; nothing loads differently. Touch emulation
doesn't alter any of it, which is expected — none of these techniques depends
on input.

## What is still unknown, precisely

Emulation gets the engine, the viewport and the device metrics. It does not get:

1. **iOS Safari's own behaviour on top of WebKit.** Notably **Low Power Mode**,
   which is documented to throttle animation, and which no desktop build has.
   A profile that depends on motion to be legible could be still on a phone
   that is saving battery — one more argument for a first frame that is already
   the whole composition.
2. **The GitHub mobile apps.** They render READMEs in native views, not a
   browser tab, and their markdown support is their own. Whether `<picture>`
   theming, SMIL or `<details>` behave there is genuinely untested.
3. **Real device rasterisation** — subpixel text rendering at 3× on a physical
   panel, which is what actually decides whether 11px is readable in the hand.
   The legibility floor came from measurement plus judgement, and only a real
   phone can confirm the judgement.

The by-hand checklist at the end of `docs/CAPABILITY-MATRIX.md` still stands for
those three. This track removes the engine question from it, not the rest.

## Why this is worth stating at all

It would have been easy to run the emulated pass and write "verified on iOS".
The emulator is Safari's engine on a desktop OS with an iPhone's metrics —
close enough to rule out engine differences, not close enough to speak for the
device. The distinction is the whole point of the matrix.
