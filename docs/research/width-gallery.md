# Width-gated `<picture>` test

Can a `<picture>` source select a different SVG by viewport width on GitHub?
If so, a card can ship a desktop canvas and a phone-scale one, instead of
compromising between them.

<picture>
  <source media="(max-width: 600px)" srcset="examples/w-phone.svg">
  <img alt="A card that should be replaced by a phone-scale version on a narrow screen" src="examples/w-desktop.svg" width="900">
</picture>

Expected if it works: **PHONE VARIANT** at 390px, **DESKTOP VARIANT** at 1280px.
