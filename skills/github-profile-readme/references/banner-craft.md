# Banner craft

The banner is the only element with no competition for attention, and the only
one that is read at two wildly different sizes. Design for the smaller one.

## Pick the viewBox from the aspect ratio, not from habit

The container is 846px desktop / 309px mobile. Your banner's *height* on screen is
therefore `846 / ratio` and `309 / ratio`.

| Ratio | Desktop height | Mobile height | Verdict |
|---|---|---|---|
| 5.0 : 1 (1200×240) | 169px | **62px** | Too short on mobile to hold two lines |
| 4.0 : 1 (1200×300) | 212px | 77px | Workable, tight |
| 3.0 : 1 (900×300) | 282px | 103px | **Good default.** Two lines breathe |
| 2.5 : 1 (900×360) | 338px | 124px | Generous; risks pushing content below fold |
| 2.0 : 1 | 423px | 155px | Only for image-led, text-light designs |

**Default to 3:1 with a 900-unit viewBox.** It gives mobile ~103px of height —
enough for a name and one supporting line at legible sizes — without eating the
desktop fold.

A 900-unit viewBox also improves the legibility ratio: mobile needs F ≥ 32 rather
than F ≥ 43. You get roughly 25% more effective type size for free, purely by
choosing a smaller coordinate system.

## The legibility worksheet

Fill this in before drawing. `W` = viewBox width.

```
W = ______

Mobile floor   (11px @ R=309):  F_min = 11 × W / 309 = ______
Desktop floor  (11px @ R=846):  F_min = 11 × W / 846 = ______

Element          Size (units)   Mobile px    Desktop px   OK?
name             ______         ______       ______
role / headline  ______         ______       ______
supporting line  ______         ______       ______
```

For `W = 900`: mobile floor is 32, desktop floor is 12.
For `W = 1200`: mobile floor is 43, desktop floor is 16.

Any row below its mobile floor is a decision, not an accident. Either enlarge it,
cut it, or consciously accept it is desktop-only decoration.

## Type scale that survives the squeeze

At a 900-unit viewBox, a scale that works:

| Role | Units | Mobile px | Desktop px |
|---|---|---|---|
| Name | 64 | 22 | 60 |
| Role / headline | 34 | 12 | 32 |
| Supporting line | 32 | 11 | 30 |

Note how compressed this is — the ratio between name and supporting text is 2:1,
not the 4:1 you would use in print. **Wide dynamic range in type does not survive
downscaling**; the small end falls off a cliff. Compress the scale and create
hierarchy with weight, colour, and space instead of size.

## Hierarchy without size

Since size range is constrained, lean on:

- **Weight.** 800 against 400 reads clearly even at 11px.
- **Colour/value.** A bright name against a muted supporting line separates
  instantly and costs no pixels.
- **Space.** Generous leading between the name and the rest does more at small
  sizes than a size jump does.
- **A rule or accent bar.** A 4-unit accent strip reads at any scale and anchors
  the composition.

## Composition

- **Left-align.** Centred text in a wide, short box is hard to scan and collapses
  badly when the box gets short on mobile.
- **Keep a safe margin** of ~4% of viewBox width on all sides. Edge-tight text
  looks cramped at 309px.
- **Put nothing critical in the right third.** It is the first thing that feels
  crowded at mobile height, and it is where a decorative element belongs instead.
- **Avoid fine detail.** Hairlines below ~1.5 units and grid patterns below ~20
  units turn into mud or moiré at 309px. Test them; do not assume.

## Colour

- Design **two files**, dark and light, and serve with `<picture>`. Do not try to
  adapt inside one SVG — in secure animated mode the SVG cannot read the host
  page's theme.
- Check contrast at the *rendered* size. Thin type at 11px needs more contrast
  than the same type at 60px; WCAG AA (4.5:1) is a floor, not a target, for
  supporting text.
- GitHub's dark canvas is near `#0d1117`. A pure-black banner floats oddly
  against it; a very dark blue-grey sits better. The light canvas is `#ffffff`.

## Motion, if any

SMIL and CSS keyframes both run. But:

- The banner is read in about one second. Animation that takes longer than that
  to make its point is never seen.
- Looping motion in a README is visible the entire time someone reads the page
  below it. Anything fast or high-contrast becomes an irritant. Prefer a single
  settle on load, or a very slow ambient drift.
- Animation cannot respond to `prefers-reduced-motion` reliably here. Assume it
  always plays, for everyone, forever. If that would bother you, do not add it.

## Generated vs static

Generate only if a value genuinely changes. A generated banner buys you live
data and costs you: a CI dependency, a commit stream, a cache window, and a
determinism requirement.

If generating, the output must be **byte-identical when inputs are unchanged**.
Timestamps in the SVG, unordered dict iteration, floating-point formatting, and
random gradient ids all break this and produce a commit on every run forever.
Pin them.

## Review checklist

- [ ] Rendered at 309px wide and every line still readable
- [ ] Every font in the file is either a system fallback stack or embedded base64
- [ ] Two files for dark/light, wired through `<picture>` with absolute URLs
- [ ] Meaningful `alt` text describing the content, not the word "banner"
- [ ] No `<script>`, no hover states, no external refs
- [ ] File size sane — under ~50KB unless a font is embedded
- [ ] If generated: two consecutive runs produce identical bytes
- [ ] Nothing claimed in the banner that cannot be backed up
