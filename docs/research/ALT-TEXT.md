# Track 3 · Alt text across the corpus

The survey measured whether a card can be *read*. This asks whether it can be
reached at all by someone who can't see it — and finds the genre's second
structural failure, after the phone.

## The shape of the problem

An SVG card puts its words inside an image. Markdown text reflows and is read
aloud; a card's text is pixels. The only channel back out is the `alt`
attribute — and that is measurably true, not assumed:

An `<img>` pointing at an SVG that declares `role="img"`, an `aria-label`, a
`<title>` **and** a `<desc>` exposes an accessible name of `""` in Chromium's
accessibility tree. Give the same `<img>` an `alt` and the name is the alt.

| What the `<img>` had | Accessible name |
|---|---|
| SVG with `role`, `aria-label`, `<title>`, `<desc>`; no `alt` | `""` |
| The same SVG, `alt="ALT ON THE IMG TAG"` | `"ALT ON THE IMG TAG"` |
| The same SVG, `alt=""` | not in the tree at all (decorative, correct) |

**Nothing inside the file crosses the boundary.** Labelling the SVG internally
is wasted effort; the `alt` is the whole interface.

## What the 446 profiles do

Re-parsed from their live READMEs (`tools/research/alt_text.py`, 439 reachable),
markdown and HTML images alike, badges counted separately because a shield with
`alt=""` is correct:

| Class | Non-badge images | Share |
|---|--:|--:|
| **absent** — no `alt` attribute | 2,258 | **34.2%** |
| **empty** — `alt=""` | 653 | 9.9% |
| **filename** — the alt is the file name | 389 | 5.9% |
| **generic** — one or two words like "banner", "gif" | 137 | 2.1% |
| descriptive — anything actually written | 3,173 | 48.0% |

Narrowed to the images where it matters most — SVG cards at least 200px wide
that the survey measured as carrying text, i.e. the ones whose content exists
nowhere else:

| Class | Text-bearing cards | Share |
|---|--:|--:|
| absent | 765 | 30.3% |
| empty | 189 | 7.5% |
| filename | 43 | 1.7% |
| generic | 84 | 3.3% |
| descriptive | 1,446 | 57.2% |

**954 cards — 37.8% — put text on screen and offer no way to hear it.** The 127
filename and generic ones are arguably worse: they occupy the slot where a
description should be, so nothing flags them as missing.

By cohort, the hand-made profiles do markedly better: **57.5% descriptive** in
the code-search cohort versus **31.1%** in the curated one. The same split as
the phone-legibility finding, but inverted — people building their own SVGs
write more alt text and smaller type.

Per profile, counting only those with at least one content image:

| | curated | search |
|---|--:|--:|
| every content image described | 38 | 63 |
| some described | 84 | 149 |
| **none described** | **32** | **29** |

61 profiles describe nothing at all.

## Rules this justifies

1. **Every content image gets a real `alt`.** Write what the card *says*, not
   what it is: `"LinuxWeb: real Alpine Linux in a browser tab"`, never
   `"banner"` or `"project card"`.
2. **`alt=""` is correct for decoration** — a divider, a wave, a badge whose
   text is also in the markdown beside it — and wrong for anything carrying
   information. Used deliberately it is the right answer; the 189 text-bearing
   cards using it are not being deliberate.
3. **Don't bother labelling inside the SVG.** `<title>`, `<desc>`,
   `aria-label` and `role="img"` do not cross into the host page. Harmless, but
   never a substitute.
4. **If the alt is hard to write, the card is carrying too much.** An alt you
   can't summarise in a sentence is a sign the information belongs in markdown,
   where it is readable, reflowable and searchable anyway.

## Method and its limits

Classification is mechanical and coarse. "Descriptive" means only *not
obviously junk* — an alt of "my github stats card showing commits" counts, and
it isn't good. So 48% and 57.2% are **ceilings**, not achievements: the real
figure for useful alt text is lower by an unknown margin. The failure classes
(absent, empty, filename, generic) are exact, which is why the findings above
lean on those.

The accessibility-tree measurement is Chromium's. Firefox and WebKit expose
trees through platform APIs that can't be read from this harness, so whether
they agree is **UNVERIFIED** — though the alt-only channel is what the HTML
spec requires of a replaced element, so disagreement would be surprising.
