# Technique gallery

Every technique in the catalogue as an original minimal example, embedded the
way a profile README embeds an image, so GitHub's own markdown pipeline renders
it. `tools/techniques/verify.py` loads this page on github.com and records, for
each image, whether it loaded, whether it actually animates inside GitHub's
page, and what the boundary tests reveal. Results: [VERIFIED.md](VERIFIED.md).

All examples use a 600-unit viewBox with text at 24 units or more, so text
stays at or above ~12px in the 309px phone column.

## Motion

<img src="examples/smil-motion.svg" alt="A dot travelling along a curved path — SMIL animateMotion">

<img src="examples/css-keyframes.svg" alt="A rotating ring around a pulsing core — CSS keyframes">

<img src="examples/particles.svg" alt="A field of twinkling stars — staggered SMIL opacity">

## Drawing

<img src="examples/stroke-draw.svg" alt="A line drawing itself — CSS stroke-dashoffset with pathLength">

<img src="examples/smil-draw.svg" alt="An underline drawn with SMIL">

## Light and texture

<img src="examples/glow.svg" alt="Glowing neon text — feGaussianBlur">

<img src="examples/grain.svg" alt="Gradient card with film grain — feTurbulence">

<img src="examples/gradient-shimmer.svg" alt="Text with a moving shimmer — animated gradientTransform">

## Reveals and text

<img src="examples/mask-reveal.svg" alt="Headline revealed left to right by a mask">

<img src="examples/typing.svg" alt="Text typed out character by character">

<img src="examples/textpath.svg" alt="Text flowing along a wave — textPath">

<img src="examples/terminal.svg" alt="A terminal printing three lines">

## Data

<img src="examples/gauge.svg" alt="A gauge filling to 72 percent">

<img src="examples/bars.svg" alt="A bar chart rising into place">

## Theme switching

Inside the SVG — follows the viewer's operating-system scheme:

<img src="examples/theme-aware.svg" alt="A card that switches colours with the colour scheme">

`<picture>` with `prefers-color-scheme` — follows the page:

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="examples/theme-picture-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="examples/theme-picture-light.svg">
  <img src="examples/theme-picture-dark.svg" alt="Theme variant served by picture">
</picture>

Legacy URL fragments:

![Dark variant served by fragment](examples/theme-fragment-dark.svg#gh-dark-mode-only)
![Light variant served by fragment](examples/theme-fragment-light.svg#gh-light-mode-only)

## Boundary tests

Each is built so the answer is visible in the render.

<img src="examples/test-script.svg" alt="Boundary test: script inside SVG">

<img src="examples/test-external-image.svg" alt="Boundary test: external image inside SVG">

<img src="examples/test-external-font.svg" alt="Boundary test: imported web font">

<img src="examples/test-foreign-object.svg" alt="Boundary test: HTML inside foreignObject">

## Native markdown

<details>
<summary><b>Real text, collapsed by default</b> — click to expand</summary>

Markdown inside `<details>` reflows to any width, stays selectable and
searchable, and is read by screen readers. It is the one layer of a profile that
survives every screen.

</details>
