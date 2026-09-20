# Research log — research/claude

Counterpart to `docs/RESEARCH-LOG.md` (research/antigravity). Rendering,
visual-design, and verification side.

## Ledger

| # | Topic | Status | Date |
|---|---|---|---|
| C0 | **P0 BUG: three generated SVGs are malformed XML** | done | 2026-09-21 |
| C1 | **P1 BUG: linter reports success on broken output** | done | 2026-09-21 |
| C2 | Measured README container widths | done | 2026-09-21 |
| C3 | Banner legibility model + verified reference | done | 2026-09-21 |
| C4 | Font loading under CSP | done | 2026-09-21 |
| C5 | Camo vs raw routing (corroborates AG Track 2) | done | 2026-09-21 |
| C6 | Skill packaged: `skills/github-profile-readme/` | done | 2026-09-21 |

---

## C0 — P0: three generated SVGs are malformed XML

**Severity: high.** These are broken images on the live profile, not a cosmetic
issue. A malformed SVG does not degrade — the browser renders nothing.

**Evidence.**

```
python -c "import xml.etree.ElementTree as ET, glob; ..."
  BROKEN  assets/banner-dark.svg  -> not well-formed (invalid token): line 23, column 147
  BROKEN  assets/banner-light.svg -> not well-formed (invalid token): line 23, column 153
  BROKEN  assets/pet.svg          -> not well-formed (invalid token): line 18, column 60
  VALID   assets/dashboard.svg, quantum-coherence.svg, spotify-mock.svg,
          synaptic-network.svg, terminal-typing.svg
```

Confirmed visually: served over HTTP and rendered in a browser, the banner shows
a broken-image icon while a well-formed control SVG renders correctly.

**Root cause.** A bare `&` in text content. XML requires `&amp;`.

- `banner-dark/light.svg:23` ← `profile.headline` =
  `"Principal Systems Architect & Distributed Systems Engineer"`
- `pet.svg:18` ← `"STATUS: EUPHORIC & THRIVING!"`

`render_svg_banners()` interpolates `profile["name"]` and `profile["headline"]`
directly into the SVG f-string with no escaping. The engine *does* write `&amp;`
correctly — but only in **hardcoded** strings (engine.py:168, 196, 292, 367).
Every value that comes from `profile.config.json` is unescaped.

So this is not a one-off typo. **Any `&`, `<`, or `>` in any config value silently
produces a broken asset**, and config is the part users are invited to edit.

**Fix** (owner: research/antigravity — `harness/**` is its path). Escape at every
interpolation boundary:

```python
from xml.sax.saxutils import escape as xml_escape, quoteattr

# text content
name     = xml_escape(profile["name"])
headline = xml_escape(profile["headline"])

# attribute values (adds its own quotes)
label = quoteattr(profile["headline"])   # -> "...&amp;..."
```

Apply to every config-derived value reaching an SVG — names, headlines, status
text, pet name, metric labels, bento block titles, terminal output lines. Grep
for `{profile[` and `{config[` inside SVG f-strings.

## C1 — P1: the linter reports success on broken output

`lint_readme()` prints **"0 Sanitizer Errors"** while three of the eight SVGs it
just generated are unparseable. That is false confidence, which is worse than no
linter: it is the reason this shipped.

Its SVG checks (engine.py:662–682) are pure string matching:

- file exists
- `"<foreignObject" in svg_text`
- `"<script" in svg_text`
- `size > 500KB`

It never parses the XML.

**Fix.** Add well-formedness as the first check, and make it an error:

```python
import xml.etree.ElementTree as ET

try:
    ET.parse(svg_file)
except ET.ParseError as e:
    errors.append(f"Malformed XML in assets/{asset}: {e}")
```

Also worth adding while there: assert the root element is `<svg>` with a
`viewBox`, and warn if any `font-family` names a non-system font (see C4).

*On parser choice:* the usual advice is `defusedxml` over stdlib
`ElementTree`, because of XXE and billion-laughs. Here the linter parses files
the engine wrote microseconds earlier, inside CI, so the threat model is thin —
and the engine is deliberately zero-dependency, which `defusedxml` would break.
Stdlib `ET` is the right call for this specific use. If the linter is ever
pointed at externally-supplied SVGs, that calculus flips and it should switch.

**Systemic note.** A generator whose validator cannot fail on its own output is
not a validator. Whatever else the pipeline checks, "does the artifact parse"
belongs first.

## C2 — Measured README container widths

Measured from rendered DOM on github.com, profile README container. Method and
raw numbers in `skills/github-profile-readme/references/measured-constraints.md`.

| Viewport | Content width |
|---|---|
| 1920 | 846px |
| 1280 | 831px |
| 390 | **309px** |

Images are clamped to the container (854px natural → 846px rendered).

Published figures of 830px and 894px are both wrong for this context: 830 is this
same measurement taken at a ~1280 viewport, and 894 appears to be a repo README
or an older layout.

## C3 — Banner legibility model

SVG text scales with the viewBox, so absolute font sizes are meaningless. What
matters is the ratio:

```
effective_px = F × (R / W)        F_min = target_px × W / R
```

For an 11px legibility floor at mobile (R=309), a 1200-unit viewBox requires
**F ≥ 43 units for every piece of text**.

**The current banner fails this badly.** viewBox 1200×240, type at 38 / 16 / 14:

| Element | Units | Mobile (309) | Desktop (846) |
|---|---|---|---|
| Name | 38 | 9.8px ✗ | 26.8px ✓ |
| Headline | 16 | 4.1px ✗ | 11.3px ~ |
| Supporting | 14 | 3.6px ✗ | 9.9px ✗ |

Every line is illegible on mobile, and the supporting line is too small even on
desktop. The 5:1 aspect ratio compounds it: at 309px wide the banner is only 62px
tall, which cannot hold three lines.

**Verified alternative.** 900×300 (3:1), type at 64 / 34 / 32 → 22px / 12px / 11px
on mobile. Built it, served it, rendered it at 309px, confirmed all three lines
readable. Source: `skills/github-profile-readme/examples/reference-banner-dark.svg`.

Shrinking the viewBox from 1200 → 900 buys ~25% effective type size for free.

**SVG needs no 2× export for retina** — it is resolution independent. The common
"export at 2×" advice is raster-only, and following it here is what produces
2400-unit viewBoxes with unreadable 20-unit type.

## C4 — Fonts do not load

GitHub's CSP blocks external font loading for SVGs referenced as images.
`font-family: 'JetBrains Mono', monospace` renders as **generic monospace** — the
intended typeface never arrives, silently.

The engine specifies `'JetBrains Mono'` throughout (engine.py:74, 141, and
others). None of it is rendering as designed today.

Options: design for a system fallback stack; embed a subset WOFF2 as base64; or
convert text to paths. Detail in `references/svg-recipes.md`.

## C5 — Camo vs raw routing (corroborates AG Track 2)

Antigravity concluded from docs + `curl -I` that repo-relative assets are not
Camo-proxied. **Independently confirmed by a different method** — reading
`currentSrc` off every `<img>` in the live rendered DOM of
`hammadshakeelai/github-profile-blueprint`:

```
{ "github.com": 6, "camo.githubusercontent.com": 3 }
```

Repo-relative `./assets/*.svg` → `github.com/{owner}/{repo}/raw/main/...`, not
proxied. The third-party typing-SVG → Camo. Two methods, same conclusion.

One refinement: the rewrite target is `github.com/.../raw/...` (which then
redirects to `raw.githubusercontent.com`), not a direct rewrite to the raw host.

## C6 — Skill packaged

`skills/github-profile-readme/` — SKILL.md plus three references
(measured-constraints, banner-craft, svg-recipes) and a verified example banner
with a legibility test harness. Everything in it is measured or tested, not
quoted.

## Handoff to research/antigravity

Two fixes land in your paths. Both are small:

1. **C0** — XML-escape every config-derived value in `harness/engine.py`.
2. **C1** — add `ET.parse()` well-formedness to `lint_readme()` as an error.

Do C1 first: with it in place, C0 becomes impossible to ship again.

## Open questions

- Does GitHub's own renderer reject malformed SVG identically to the browser, or
  does it sanitize-and-repair? Would change how loudly C0 fails in practice.
- Is there a size at which a base64-embedded font stops being worth it? Needs a
  real measurement of render time vs file size.
- Do animated SVGs in a profile README affect page performance scores enough to
  matter?
