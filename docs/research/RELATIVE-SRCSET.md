# Track 1 · Does a relative `srcset` resolve on a profile page?

**Yes.** Verified live on 33 real profiles. The claim that it fails — carried
from the archived v1 research, and repeated in the skill with an `UNVERIFIED`
tag — is false.

## Why it stayed open

Profile pages resolve relative markdown paths against a different base than repo
pages, so the concern was plausible. Testing it the obvious way means editing a
live profile README, which I wasn't going to do to someone's account. That is
what left it unverified through Phases 2–6, and what made the built profile use
absolute URLs.

## How it was answered without editing anything

Two passes, both read-only.

**Corpus pass** (`tools/research/srcset.py`). The Phase 1 survey had already
recorded, for 442 profiles, both what the markdown declared and what the browser
actually loaded on the live page. 34 profiles declared a `<picture>` dark source
with a relative path — 197 such sources once width-gated mobile sources are
excluded. **174 (88%) served exactly the declared file.**

**Live pass** (`tools/research/srcset_live.py`). The corpus is two days old and
profiles change, so the 33 of those 34 that still use a relative dark srcset
today were loaded fresh, at 1280px in the dark scheme, reading each
`<picture>`'s `currentSrc`:

| Result | Profiles |
|---|--:|
| Dark file served — relative path resolved | **32** |
| Reported mismatch | 1 |

The single mismatch is the tool's, not the platform's: SirAllap's first relative
dark source is `header-m-dark.svg`, a `max-width` mobile variant that correctly
does not apply at 1280px, and the page served `header-dark.svg` as it should.
**33 of 33 behave correctly.**

## Corrections this forces

- The skill's `platform-facts.md` carried this as an UNVERIFIED failure. It is
  now a verified success.
- `svg-recipes.md`, `banner-craft.md`, `SKILL.md` and `docs/PROFILE.md` all
  justified absolute URLs with "relative can fail on a profile page". The
  justification was wrong.

**The recommendation does not change, but its reason does.** Use absolute
`raw.githubusercontent.com` URLs because they are unambiguous, work identically
in a repo README and a profile README, and survive the file being viewed
anywhere else — not because relative paths break. Relative paths are fine, and
a profile that uses them is not carrying a bug.

## One real failure found along the way

Not the one being looked for. Xalzeroph's `<picture>` blocks set the `<img>`
fallback to the **light** file, and at survey time the dark-scheme capture
showed four of them serving that light file *broken*. The lesson generalises:
the `<img>` src is not a formality, it's what every client that ignores
`<source>` will fetch, so it should point at the variant you'd rather have seen
— and it must exist. (That profile has since switched to absolute URLs with
cache-busting query strings, and now serves its dark files correctly.)

## Method note

The corpus pass's first run reported 23 failures. All of them were
width-conditioned sources that correctly don't load at desktop width — a bug in
the classifier, not a finding, fixed before anything was written down. It is
recorded here for the same reason the survey records its corrections: the
measurement was wrong first.
