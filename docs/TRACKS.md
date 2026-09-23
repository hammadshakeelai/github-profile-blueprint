# Open tracks

The six phases of [PLAN-V2.md](PLAN-V2.md) are done. These are the questions
that work left open, each one minted from something the research could not
answer at the time, plus the tools the findings imply. Same standing rule: no
claim without a citation, a measurement, or an `UNVERIFIED` tag.

| # | Track | Status |
|---|---|---|
| 1 | Does a relative `srcset` resolve on a profile page? | **done** |
| 2 | Does `prefers-reduced-motion` reach an SVG in secure animated mode? | **done** |
| 3 | Alt text and accessibility across 10,782 images | **done** |
| 4 | `profile-lint` — every measured rule as a checker | **done** |
| 5 | Narrow the iOS unknown with an iPhone-emulated WebKit pass | **done** |
| 6 | Can a `<picture>` source be gated on **width**? | **done** |
| 7 | Package profile-lint so other people can run it | todo |
| 8 | A five-minute real-device checklist | **built — needs a phone** |

---

## 1 · Does a relative `srcset` resolve on a profile page?

**Why it's open.** The skill and the built profile both use absolute
`raw.githubusercontent.com` URLs inside `<picture>` on the strength of an
archived claim that relative paths fail on a profile page. I tagged it
`UNVERIFIED` because testing it directly means editing a live profile.

**How to answer it without editing anything.** The survey already rendered 442
profile pages and recorded, per image, what the browser actually loaded. 540
`<source srcset>` entries across the corpus were written as relative paths. If
relative srcset failed on profile pages, those profiles would be visibly falling
back to their `<img>` src — which the data can show.

**Answer:** see [research/RELATIVE-SRCSET.md](research/RELATIVE-SRCSET.md).

## 2 · Does `prefers-reduced-motion` reach an SVG?

Every animated example in the catalogue runs unconditionally. Nobody in the
survey was checked for a reduced-motion guard, and it is unknown whether the
media query even reaches an SVG in secure animated mode — the document is
rendered by the host browser, so it plausibly does, but plausible is not
measured. Two parts: run it through the three-engine harness, and count how many
of the 1,506 bespoke SVGs guard their animation at all.

**Answer:** it does not reach the SVG at all — in any engine — so the 369 files
that guard their animation are doing nothing. A `<picture>` source gated on the
query does work, because the host page evaluates it.
See [research/REDUCED-MOTION.md](research/REDUCED-MOTION.md). Now applied to the
built profile and written into the skill.

## 3 · Alt text and accessibility

10,782 images were fetched and none were examined for alt text. The corpus can
answer: what share carry meaningful alt text, what share carry none or
decorative junk ("banner", "gif"), and how that splits by cohort. The survey
measured whether a card can be *read*; this asks whether it can be read by
someone who can't see it.

**Answer:** 37.8% of text-bearing cards offer no way to reach their content, and
nothing inside an SVG — `<title>`, `<desc>`, `aria-label`, `role` — crosses into
the host page's accessibility tree. See [research/ALT-TEXT.md](research/ALT-TEXT.md).

## 4 · `profile-lint`

Everything measured across six phases is mechanical: broken images, text below
the legibility floor at 309px, table layout, missing dark/light, badge share,
dead-service embeds, `<script>` in an SVG, animation that starts from
`opacity="0"`. A checker that runs all of it against any profile turns the
research into something reusable, and the 446-profile corpus is a ready-made
validation set — the rates it reports should reproduce the survey's.

**Built:** `tools/lint/profile_lint.py`, thirteen rules, validated on 79 sampled
profiles and calibrated against the shortlist. The validation caught two bugs in
the linter. See [research/PROFILE-LINT.md](research/PROFILE-LINT.md).

## 5 · Narrow the iOS unknown

The capability matrix ends with a hand-check list for iOS Safari and the GitHub
mobile apps. Real iOS can't be driven from here, but WebKit *with iPhone device
emulation* (touch, mobile user agent, device scale) is a closer proxy than the
narrow desktop viewport used so far, and Playwright can do it. It won't close
the question — it will shrink it, and the residue should be stated precisely
rather than left blank.

**Answer:** nothing changes under iPhone emulation — same 13 animating, same one
WebKit exception, all three theme mechanisms working. What remains genuinely
unknown: iOS Low Power Mode, the GitHub mobile apps' native renderers, and real
3× rasterisation. See [research/IOS.md](research/IOS.md).

## 6 · Can a `<picture>` source be gated on width?

Track 2 proved GitHub's sanitizer keeps `media="(prefers-reduced-motion: reduce)"`
and that all three engines honour it. Two surveyed profiles (Xalzeroph,
SirAllap) ship `max-width` sources pointing at phone-specific files, and the
Track 1 pass saw those sources correctly *not* apply at 1280px — but nobody has
checked that they *do* apply at 390px.

If they do, the survey's largest finding stops being a trade-off. Today a card
must choose between a desktop-scale canvas and 309px legibility. With a
width-gated source it can ship both: one SVG drawn for 846px, another drawn in
309 units where 11px is 11px. That would change the skill's central advice, so
it needs verifying rather than assuming.

## 7 · Package profile-lint

It currently runs from a checkout of this repository. A composite GitHub Action,
or a single file with no imports from `tools/survey/`, would let anyone point it
at their profile. Worth doing only once the rules have settled.

## 8 · A five-minute real-device checklist

Track 5 left three things emulation cannot answer: iOS Low Power Mode, the
GitHub mobile apps' native renderers, and real 3x rasterisation. All three are
answerable by one person with a phone in a few minutes, if the gallery is laid
out so each answer is a yes/no you can read off. Build that page.

**Built:** [research/PHONE-CHECK.md](research/PHONE-CHECK.md) — five cards, each
drawn in a 309-unit canvas so it obeys the rule it tests, with a table to fill
in. It cannot be completed from this machine; it needs someone to open it on a
phone, in the browser and in the GitHub app, with Low Power Mode and Reduce
Motion toggled.
