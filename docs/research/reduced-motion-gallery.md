# Reduced-motion test gallery

Three files, loaded by `tools/matrix/capture.mjs` in Chromium, Firefox and
WebKit with and without `prefers-reduced-motion: reduce`, to answer whether the
guard reaches an SVG referenced as an image. Not a showcase — a test fixture.

**CSS keyframes, guarded** — should stop when reduced motion is requested.

![CSS keyframes with a reduced-motion guard](examples/rm-css.svg)

**SMIL, same guard** — a media query has no hold on SMIL; expected to keep
moving either way.

![SMIL with the same guard, which should not apply](examples/rm-smil.svg)

**SMIL, swapped for a still frame** — CSS can't stop the animation, but it can
hide the layer running it and reveal a still one.

![SMIL animation swapped for a still frame under reduced motion](examples/rm-swap.svg)

**`<picture>` gated on reduced motion** — the host page evaluates this query
even though the image can't. If the sanitizer keeps the attribute, a viewer who
asked for less motion gets the still file.

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="examples/rm-still.svg">
  <img alt="A sliding square, replaced by a still one for viewers who asked for reduced motion" src="examples/rm-motion.svg" width="600">
</picture>
