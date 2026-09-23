# Open tracks

The six phases of [PLAN-V2.md](PLAN-V2.md) are done. These are the questions
that work left open, each one minted from something the research could not
answer at the time, plus the tools the findings imply. Same standing rule: no
claim without a citation, a measurement, or an `UNVERIFIED` tag.

| # | Track | Status |
|---|---|---|
| 1 | Does a relative `srcset` resolve on a profile page? | **done** |
| 2 | Does `prefers-reduced-motion` reach an SVG in secure animated mode? | todo |
| 3 | Alt text and accessibility across 10,782 images | todo |
| 4 | `profile-lint` — every measured rule as a checker | todo |
| 5 | Narrow the iOS unknown with an iPhone-emulated WebKit pass | todo |

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

If it works, it belongs in the skill as a rule, not a nicety: an animated
profile is one of the few pages a reader can't stop.

## 3 · Alt text and accessibility

10,782 images were fetched and none were examined for alt text. The corpus can
answer: what share carry meaningful alt text, what share carry none or
decorative junk ("banner", "gif"), and how that splits by cohort. The survey
measured whether a card can be *read*; this asks whether it can be read by
someone who can't see it.

## 4 · `profile-lint`

Everything measured across six phases is mechanical: broken images, text below
the legibility floor at 309px, table layout, missing dark/light, badge share,
dead-service embeds, `<script>` in an SVG, animation that starts from
`opacity="0"`. A checker that runs all of it against any profile turns the
research into something reusable, and the 446-profile corpus is a ready-made
validation set — the rates it reports should reproduce the survey's.

## 5 · Narrow the iOS unknown

The capability matrix ends with a hand-check list for iOS Safari and the GitHub
mobile apps. Real iOS can't be driven from here, but WebKit *with iPhone device
emulation* (touch, mobile user agent, device scale) is a closer proxy than the
narrow desktop viewport used so far, and Playwright can do it. It won't close
the question — it will shrink it, and the residue should be stated precisely
rather than left blank.
