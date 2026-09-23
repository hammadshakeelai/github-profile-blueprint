# The profile

The built profile lives in [`profile/`](../profile) — `README.md` plus fourteen
SVGs in `profile/assets/`. It is comp C from [DIRECTION.md](DIRECTION.md): a
window header, six project windows each wrapped in a link to the running thing,
then everything else as grouped markdown lists.

Rebuild it with `python tools/profile/build.py`, which reads the same
[content.json](direction/content.json) the comps do. Changing which six are
featured is the `FEATURED` list in that script.

## Decisions made while building

- **Absolute `raw.githubusercontent.com` URLs, not relative paths.** The reason
  given when this was built — that a profile page can't resolve a relative
  `srcset` — turned out to be false; Track 1 checked 33 live profiles that use
  relative paths and all 33 resolve correctly
  ([RELATIVE-SRCSET.md](research/RELATIVE-SRCSET.md)). The choice stands on
  weaker but real grounds: one URL that works identically in a repo README, a
  profile README and anywhere the markdown is quoted.
- **Six cards, not thirteen.** The cap comes from DIRECTION; the other seven
  projects are markdown list items, which reflow and cost nothing.
- **The whole card is the link.** An SVG can't be clicked inside on GitHub, but
  `<a><picture><img></picture></a>` makes the entire 600×~230 panel a tap
  target — the largest one a README can have.
- **One animation on the page**: the caret after the header's last line, an
  `opacity` `calcMode="discrete"` blink. Nothing else moves, and the first frame
  of every file is the finished composition.
- **A still header for reduced motion.** Track 2 found that a guard *inside* an
  SVG never applies, so the still version is a separate file chosen by a
  `<picture>` source the host page can evaluate
  ([REDUCED-MOTION.md](research/REDUCED-MOTION.md)).
- **`view source` instead of `▶ open in a tab`** on the one project with no live
  demo, so the card never promises something that isn't there.

## Verified, not assumed

Rendered by GitHub from the staging copy (`profile/README.staging.md`, identical
but pointing at this repo) at 390px and 1280px in both schemes —
[shots](profile/shots/):

| Check | Result |
|---|---|
| All seven images load | 7/7, no broken-image icon |
| Rendered width on a phone | 324px in the blob column (a profile page's is 309px) |
| Smallest text on a phone | **11.9px** — above the 11px floor, and 11.3px if scaled to 309px |
| Dark and light | both render; `<picture>` picks the right file |
| Reduced motion | all four combinations correct: the still header is served to a viewer who asked for less motion, in both schemes |
| Layout on a phone | one column, no sideways scroll, no table |

The survey's headline failure — 55% of cards illegible at phone width — does not
apply here, and that is measured rather than intended: every file is generated
by code that refuses to write an SVG whose text would fall below the floor
(`check()` in `tools/direction/build.py`).

## Shipping it

The files are built for `hammadshakeelAl/hammadshakeelAl`. This session's
credentials are for the `hammadshakeelai` account and have no push access there,
so the last step is yours:

```
gh auth login                       # as hammadshakeelAl
gh auth setup-git
git clone https://github.com/hammadshakeelAl/hammadshakeelAl.git
cp -r profile/README.md profile/assets hammadshakeelAl/
cd hammadshakeelAl && git add -A && git commit -m "profile: new README" && git push
gh auth switch --user hammadshakeelai
```

`README.md` and `assets/` must sit at the repository root — the absolute URLs in
the README point at `main/assets/…`. Give it about five minutes before judging a
change: the CDN serves the previous file for `max-age=300`.
