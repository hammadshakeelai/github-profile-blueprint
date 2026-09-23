# Track 4 · profile-lint

Six phases of measurement, expressed as thirteen rules that run against any
profile in about a minute.

```
python tools/lint/profile_lint.py torvalds
python tools/lint/profile_lint.py --file profile/README.md --owner me --repo me
python tools/lint/profile_lint.py --json user1 user2     # for CI
```

It fetches the README, resolves and fetches every image, reads the source of
the profile's own committed SVGs, and reports findings at three levels. Exit
status is 1 if anything error-level fired, so it can gate a workflow. Every
finding carries the measurement behind it — a linter that can't say why is an
opinion with an exit code.

## The rules

| Rule | Level | What it catches | Evidence |
|---|---|---|---|
| `broken-image` | error | any image that doesn't load | 41% of profiles have one |
| `dead-service` | error | images from services measured as dead | the most-copied stat card loads 0% |
| `phone-illegible` | error / warn | error when the *largest* text falls below 11px at 309px; warn when only some text does | 55% of 1,730 cards fail |
| `image-table` | error | two or more images in one table | cards measured at 76px on a phone |
| `missing-alt` | error | an SVG that carries text with absent, empty, filename or generic alt | 37.8% of text cards |
| `stripped-script` | error | `<script>` inside an SVG | blocked in all three engines |
| `external-ref` | error / warn | external `<image>` or `@import` inside an SVG | blocked; Chromium draws a broken icon |
| `no-theme` | warn | no dark/light switching | 80% ship one theme |
| `badge-wall` | warn | more than half the images are badges | 42% of profiles |
| `dead-motion-guard` | warn | `prefers-reduced-motion` *inside* an SVG | never applies — Track 2 |
| `webkit-gradient` | warn | animated `gradientTransform` | WebKit never animates it |
| `hidden-first-frame` | warn | elements at `opacity="0"` that animate in | a static renderer shows nothing |
| `unguarded-motion` | note | animation with no still alternative | Track 2's `<picture>` recipe |

## Does it agree with the survey it came from?

A linter derived from a 446-profile survey should, run over profiles from that
survey, reproduce its rates. 80 sampled at random (`tools/lint/validate.py`,
fixed seed), 79 reachable:

| Rule | profile-lint | The survey |
|---|--:|--:|
| `broken-image` | 43% | 41% |
| `badge-wall` | 46% | 42% |
| `no-theme` | 77% | 80% |
| `image-table` | 18% | 21% |
| `phone-illegible` (error) | 7% curated / 74% search | 15% / 70% |

Close enough to trust, and the two don't measure identically: the survey
rendered each page in a real browser, the linter reads the markdown and the
files. They are independent implementations of the same rules agreeing, which
is the useful part.

**Two bugs the validation caught**, both found because the numbers disagreed:

- *Badge walls under-reported (32% vs 42%).* The linter's badge pattern covered
  four hosts; the survey counts badges **and icons** — skill-icons, simple-icons,
  devicon, visitor counters, donation buttons. Widened to match, and the rate
  moved to 46%.
- *Illegibility wildly over-reported (63% vs ~40% expected).* The linter was
  measuring shields.io badges, whose `for-the-badge` style sets 10px text on
  every device. Every profile with one badge fired. The survey excludes badges
  from its 1,730 cards for exactly this reason; so does the linter now, which
  brought the cohort rates in line.

Both were the linter being wrong, not the survey. Neither would have been
visible without a number to check against — which is the argument for validating
a tool against the data that produced it.

## Calibration: does it flag the good profiles?

If every exemplary profile drowns in errors, the severities are wrong. Four
from the shortlist:

| Profile | What fired |
|---|---|
| marcizhu | `no-theme` only |
| BrunnerLivio | one table, one alt, one legibility |
| ayxn07 | 31 × `dead-motion-guard`, no errors |
| JGit705 | 9 × `phone-illegible`, 9 × `dead-motion-guard` |

This matches the survey's own reading: JGit705 is the profile the survey singled
out for turning to specks on a phone, and ayxn07 is one of the conscientious
ones from Track 2 whose reduced-motion guards do nothing. The linter reaches
those conclusions from the files alone.

The profile built in Phase 5 passes every rule.

## Using it in CI

```yaml
- run: python tools/lint/profile_lint.py ${{ github.repository_owner }}
```

Worth saying plainly: the rules are about whether a page *works*, not whether it
is any good. Nothing here can tell you the writing is dull or the design is
derivative.
