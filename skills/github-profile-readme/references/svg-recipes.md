# SVG recipes

Patterns verified to render inside a GitHub README. All use system font stacks
and declarative-only features, so they survive secure animated mode.

## Reference banner — 900×300 (3:1), mobile-legible

Every type size here clears the 32-unit mobile floor for a 900 viewBox.

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 300" width="900" height="300"
     role="img" aria-label="Ada Lovelace, distributed systems engineer">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0"   stop-color="#111827"/>
      <stop offset="1"   stop-color="#0b1020"/>
    </linearGradient>
    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#38bdf8"/>
      <stop offset="1" stop-color="#818cf8"/>
    </linearGradient>
  </defs>

  <rect width="900" height="300" rx="14" fill="url(#bg)"/>
  <rect y="292" width="900" height="8" fill="url(#accent)"/>

  <!-- 4% safe margin = 36 units -->
  <g font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif">
    <text x="36" y="132" font-size="64" font-weight="800" fill="#f8fafc">Ada Lovelace</text>
    <text x="36" y="186" font-size="34" font-weight="600" fill="#38bdf8">Distributed Systems Engineer</text>
    <text x="36" y="232" font-size="32" font-weight="400" fill="#94a3b8">Consensus · Storage · Observability</text>
  </g>
</svg>
```

Check: at mobile (R=309, W=900, scale 0.343) → 22px / 12px / 11px. All legible.
At desktop (R=846, scale 0.94) → 60px / 32px / 30px.

## Dual theme wiring

```html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/USER/REPO/main/assets/banner-dark.svg">
  <source media="(prefers-color-scheme: light)"
          srcset="https://raw.githubusercontent.com/USER/REPO/main/assets/banner-light.svg">
  <img src="https://raw.githubusercontent.com/USER/REPO/main/assets/banner-dark.svg"
       alt="Ada Lovelace — distributed systems engineer" width="100%">
</picture>
```

Absolute raw URLs inside `<picture>` because they are unambiguous everywhere —
not because relative ones break. Relative `srcset` resolves correctly on profile
pages; that was checked on 33 live profiles
(`docs/research/RELATIVE-SRCSET.md`).

## Ambient motion that does not irritate

A slow accent drift. Eight-second cycle, low contrast, no flashing.

```svg
<rect y="292" width="900" height="8" fill="url(#accent)">
  <animate attributeName="opacity"
           values="0.55; 1; 0.55" dur="8s" repeatCount="indefinite"/>
</rect>
```

A one-shot settle on load — plays once, then rests. Usually the better choice:

```svg
<g opacity="0">
  <animate attributeName="opacity" from="0" to="1" dur="0.6s" fill="freeze"/>
  <!-- content -->
</g>
```

`fill="freeze"` is what makes it hold its final state instead of snapping back.

## Embedded font (full fidelity)

Only if the fallback stack genuinely will not do. Subset first — a full WOFF2 is
100KB+ and every byte ships on every page view.

```svg
<defs>
  <style>
    @font-face {
      font-family: 'Subset';
      src: url('data:font/woff2;base64,d09GMgABAAAA...') format('woff2');
      font-weight: 800;
    }
    .name { font-family: 'Subset', sans-serif; font-size: 64px; font-weight: 800; }
  </style>
</defs>
<text x="36" y="132" class="name" fill="#f8fafc">Ada Lovelace</text>
```

Subset to just the glyphs used:

```bash
pyftsubset font.ttf --text="Ada Lovelace" --flavor=woff2 --output-file=sub.woff2
```

```bash
base64 -w0 sub.woff2
```

## Progress / meter bar

```svg
<g>
  <rect x="36" y="200" width="300" height="6" rx="3" fill="#1e293b"/>
  <rect x="36" y="200" width="222" height="6" rx="3" fill="#38bdf8"/>
  <text x="348" y="207" font-size="32" fill="#94a3b8"
        font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">74%</text>
</g>
```

Clamp the computed width or a value over 100% will overflow the track:
`width = min(track, track * value / 100)`.

## Determinism guard for generated SVGs

If CI regenerates assets, prove the output is stable or you will commit forever.

```bash
python harness/engine.py build && cp assets/banner-dark.svg /tmp/a.svg
python harness/engine.py build && diff -q /tmp/a.svg assets/banner-dark.svg
```

Common sources of drift, all of which must be pinned:

- A timestamp rendered into the SVG — exclude it, or quantise to the day
- `json.load` into a plain dict then iterating — sort keys
- Float formatting (`0.30000000000000004`) — round and format explicitly
- Random or uuid gradient/filter ids — derive them from content instead
- `set` iteration order — sort before emitting

## Accessibility

```svg
<svg role="img" aria-label="Short description of what this conveys"> ... </svg>
```

plus a real `alt` on the `<img>`. Screen readers get the `alt`; the `aria-label`
covers direct navigation to the file. Do not write `alt="banner"` — describe the
content. If the image is purely decorative and its content is repeated in text
below, `alt=""` is correct and better than a redundant description.

## Things that look like they should work and do not

| Attempt | Result |
|---|---|
| `<script>` in SVG | Stripped |
| `onclick`, `onmouseover` | Stripped |
| `:hover` CSS in SVG | Never fires — no interactivity |
| `<foreignObject>` with HTML | Unreliable; avoid |
| `@import url(fonts.googleapis...)` | Blocked by CSP, silent fallback |
| `<image href="https://...">` inside SVG | External ref, blocked |
| Inline `<svg>` in markdown | Removed by sanitizer |
| `prefers-color-scheme` inside the SVG | Works — verified in three engines. Follows the OS, not the GitHub theme setting, as `<picture>` also does |
