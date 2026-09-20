# Measured constraints

Everything here was measured, not quoted. Method included so it can be
re-measured when GitHub changes its layout — treat the numbers as perishable and
the method as durable.

Measured 2026-09-21 against `github.com`, logged out state irrelevant (layout is
the same).

## README content width

**Method.** Load a profile page, emulate a viewport, measure the rendered
container:

```js
const art = document.querySelector('.js-profile-readme article.markdown-body')
         || document.querySelector('article.markdown-body');
JSON.stringify({
  viewport: window.innerWidth,
  contentWidth: Math.round(art.getBoundingClientRect().width)
});
```

**Results.**

| Viewport | Content width | Notes |
|---|---|---|
| 1920 | 846px | Caps here; wider viewports do not widen the column |
| 1280 | 831px | Fluid below the cap |
| 390 | 309px | iPhone-class. The binding constraint |

**Image capping.** An image with `naturalWidth: 854` rendered at `846` — images
are clamped to the container, never overflow it. Oversized images cost bytes and
buy nothing.

**Why published figures disagree.** Blog posts cite 830px and 894px. 830 is this
same measurement taken at a ~1280 viewport; 894 appears to be a repo README or an
older layout. Profile README and repo README containers are not identical — if
the target is a repo README, re-measure there rather than assuming.

## Asset routing

**Method.** Load a real repo README that contains both repo-relative and external
images; read `currentSrc` off every `<img>` and group by hostname.

```js
const art = document.querySelector('article.markdown-body');
const byHost = {};
[...art.querySelectorAll('img')].forEach(i => {
  const h = new URL(i.currentSrc || i.src).hostname;
  byHost[h] = (byHost[h] || 0) + 1;
});
byHost;
```

**Results** (on a README mixing `./assets/*.svg` with a third-party typing-SVG):

```
{ "github.com": 6, "camo.githubusercontent.com": 3 }
```

- Repo-relative `./assets/banner-dark.svg` → rewritten to
  `https://github.com/{owner}/{repo}/raw/main/assets/banner-dark.svg`.
  Hostname `github.com`. **Not** Camo.
- Third-party image → `camo.githubusercontent.com/<hmac>/<hex-encoded-url>`.

Note the rewrite target is `github.com/.../raw/...`, which redirects to
`raw.githubusercontent.com` — not a direct rewrite to the raw host.

**Cache behaviour.** `raw.githubusercontent.com` serves `Cache-Control:
max-age=300` with Fastly (`Via: 1.1 varnish`) in front. So committed assets go
live within ~5 minutes on branch HEAD. Camo caches external responses far more
aggressively and does not reliably self-heal when the origin recovers.

Camo URLs are HMAC-SHA1 signed; requests without a valid GitHub-issued signature
return 403. This means you cannot hand-construct or warm a Camo URL — the only
lever on the client side is changing the source URL (new URL → new digest → fresh
fetch).

*Open question, not yet settled:* whether Fastly soft-purges `raw` on push or
whether distant edges serve the full 300s. If a banner update seems not to land,
wait 5 minutes before debugging anything else.

## Secure animated mode

Not a GitHub rule — a browser rule from the SVG integration spec, triggered by
referencing an SVG through `<img>`. Scripting off, external references off,
interactivity off, declarative animation **on**. Both SMIL and CSS keyframes
count as declarative and both run.

This is why an SVG that animates when you open the file directly still animates
in a README, but its hover states and web fonts do not work.

Inline `<svg>` in markdown is a separate case: GitHub's sanitizer removes it
entirely, because `svg` is not on the allowed-element list. The file must be
referenced, never pasted.

## Font loading

CSP blocks external font fetches for SVGs referenced as images. `@import`,
`<link>`, and bare `font-family: 'Some Web Font'` all fail silently to the
generic fallback. Only fonts installed on the viewer's machine, or embedded in
the file as base64, will render.

Practical fallback stacks that resolve well across platforms:

```
ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
```

## Re-measuring checklist

When GitHub ships a layout change, re-run in this order:

1. Content width at 1920 / 1280 / 390.
2. Whether image capping still matches the container exactly.
3. Host grouping of `<img>` — confirm repo-relative is still un-proxied.
4. `curl -I` a raw asset for the current `max-age`.
5. Spot-check that a SMIL animation still plays.
