# The five-minute phone check

Three things a desktop cannot answer (Track 5): **iOS Low Power Mode**, the
**GitHub mobile apps'** native renderers, and whether 11px is really readable on
a physical screen. All three are answerable by one person with a phone.

Open this page on the phone — once in the **browser** and once in the **GitHub
app** — and read the answers off. Every card below is drawn in a 309-unit
canvas, so one unit is one pixel in the README column: the checklist obeys the
rule it is testing.

---

### 1 · Does animation run?

![A blue bar sweeping left and right if animation is running](https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/chk-motion.svg)

- Moving in the browser? → SMIL runs in iOS Safari.
- Moving in the GitHub app? → the app renders animation too.
- **Now turn on Low Power Mode** (Settings → Battery) and reload. Still moving?

### 2 · Does `<picture>` theme switching work?

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/chk-theme-dark.svg">
  <img alt="A card naming which theme file was served" src="https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/chk-theme-light.svg" width="309">
</picture>

Switch the phone between light and dark. The card should name the file it is
showing. If it says LIGHT on a dark phone, `<picture>` isn't being honoured.

### 3 · Is reduced motion honoured?

<picture>
  <source media="(prefers-reduced-motion: reduce)" srcset="https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/chk-rm-still.svg">
  <img alt="A card naming whether the still or moving file was served" src="https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/chk-rm-motion.svg" width="309">
</picture>

Turn on **Settings → Accessibility → Motion → Reduce Motion**, reload, and read
the card. This is the mechanism from Track 2 — the only one that works — and
this is the test of whether iOS and the app honour it.

### 4 · Is a phone-specific file served?

<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/w-phone.svg">
  <img alt="A card that should be replaced by a phone-scale version on a narrow screen" src="https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/w-desktop.svg" width="900">
</picture>

Should read **PHONE VARIANT** on a phone (Track 6). In the GitHub app, whichever
appears tells you whether the app evaluates `media` or falls back to the
`<img>`.

### 5 · Where does text actually stop being readable?

![Text at 20, 15, 13, 11, 9 and 7 units to find the real legibility floor on a phone](https://raw.githubusercontent.com/hammadshakeelai/github-profile-blueprint/v2/research/docs/research/examples/chk-floor.svg)

The 11px floor came from measurement plus judgement. Read this at arm's length
and find the line where it stops being comfortable — that is the floor for real.

---

## Record what you find

| Check | Browser | GitHub app | Low Power Mode |
|---|---|---|---|
| 1 · animation runs | | | |
| 2 · `<picture>` theming | | | — |
| 3 · reduced motion honoured | | | — |
| 4 · width-gated source | | | — |
| 5 · lowest comfortable size | | | — |

Fill this in and the last unverified rows of
[CAPABILITY-MATRIX.md](../CAPABILITY-MATRIX.md) close.
