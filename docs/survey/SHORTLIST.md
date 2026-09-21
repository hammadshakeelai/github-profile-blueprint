# Shortlist

Fifteen profiles that are genuinely exceptional, plus five worth studying for one
specific idea. Chosen from 446 surveyed profiles in two steps:

1. `tools/survey/shortlist.py` ranked every profile by how much of its own
   visual work actually renders — bespoke SVGs, animation, dark/light support —
   and penalised breakage, badge walls and phone-illegible cards.
2. The top 30 from that ranking, plus the ten strongest from the curated list,
   were screenshotted at 390px and 1280px and **looked at**. Ranking is not
   judgement: several high scorers turned out competent but conventional, and
   the scorer can't see an idea.

Screenshots: `shots/<user>-390.jpg` (phone, true mobile emulation) and
`shots/<user>-1280.jpg` (desktop). Phone figures below are measured from real
layout (`tools/survey/layout.py`), counting only cards — badges and icons are
excluded.

## The pattern across all of them

**The most visually ambitious profiles are the least readable on a phone.** Of
the fifteen, thirteen have at least one card whose *largest* text renders under
11px in the 309px mobile column — most of them several. The other two can't be
scored: ayxn07 outlines its text into paths, and marcizhu's board has no text. They are designed as
desktop web pages and scaled down whole. The ones that hold up on a phone do so
for one of two reasons: display type big enough to survive the shrink
(**ayxn07**), or real markdown text doing the reading instead of SVG
(**JGit705**'s About section, **codeSTACKr**, **10ishk**'s `<details>`).

That gap — ambitious *and* legible at 309px — is empty. Nobody in the survey
occupies it convincingly.

## At a glance

| Profile | Archetype | Idea to take | Phone |
|---|---|---|---|
| [ayxn07](https://github.com/ayxn07) | Editorial brutalist | One visual system, top to bottom | Display type survives; body copy doesn't |
| [ashfordeOU](https://github.com/ashfordeOU) | Luxury brand | Serif type in a sea of monospace | 11 of 21 cards illegible |
| [JGit705](https://github.com/JGit705) | Domain storytelling | Visuals drawn from the actual work | 7 of 11 cards illegible; markdown reads fine |
| [JConfessor](https://github.com/JConfessor) | Domain storytelling | A chart from the job itself | 8 of 12 illegible |
| [SergiGTAr](https://github.com/SergiGTAr) | Sci-fi HUD | Discipline inside a loud aesthetic | 6 of 7 illegible |
| [brandon-fryslie](https://github.com/brandon-fryslie) | Format concept | The profile as a daily edition | 4 of 7 illegible |
| [marcizhu](https://github.com/marcizhu) | Interactive | A game played through Issues | Board table scrolls sideways |
| [10ishk](https://github.com/10ishk) | IDE concept | SVG for polish, `<details>` for depth | 3 of 3 illegible; details read fine |
| [SimarBhatiaSB7](https://github.com/SimarBhatiaSB7) | Restrained typographic | Scale contrast, one accent | 5 of 6 illegible |
| [adamalston](https://github.com/adamalston) | One object | The whole README is a single SVG | Graphic reads; labels are texture |
| [XxMasterepicxX](https://github.com/XxMasterepicxX) | Ornamental | Illustration instead of UI | 16 of 21 illegible |
| [Dhyanesh006](https://github.com/Dhyanesh006) | Terminal, total commitment | Self-generated stats, no services | 18 of 28 illegible |
| [getaudra](https://github.com/getaudra) | Command centre | Honest labels on the data | 7 of 8 illegible |
| [sepahead](https://github.com/sepahead) | Data narrative | A graph of how the projects relate | 28 of 33 illegible |
| [atikulmunna](https://github.com/atikulmunna) | Monochrome arcade | Game animation as the banner | 10 of 14 illegible |

## The fifteen

### Editorial and brand

**[ayxn07](https://github.com/ayxn07)** — the most complete visual system in the
survey. Teal and black, huge condensed display type, numbered sections
(`01 WHOAMI`, `02 PROJECTS`, `03 STACK`) with a nav row, project cards carrying
live-status tags. It reads as a designed editorial site rather than a GitHub
profile. 31 bespoke SVGs, 23 animated. Its text is outlined into paths, so its
phone legibility can't be read from source — but looking at it, the display type
is big enough to survive 309px while the small body copy turns to specks. Take:
**make display type big enough to carry the message alone on a phone.**

**[ashfordeOU](https://github.com/ashfordeOU)** — a serif wordmark with an
orbital emblem, *"For the missions that cannot fail"* in italic serif, and a
navy-and-gold palette carried all the way to a gold contribution heatmap.
Serif type is almost absent from developer profiles, which is exactly why it
reads as premium. Embeds its font in the SVG so it renders everywhere. Take:
**the rare choice is the memorable one; carry one palette into every panel,
including the data.**

**[XxMasterepicxX](https://github.com/XxMasterepicxX)** — a serif name framed in
illustrated gold and pink vines. Ornament and illustration instead of dashboard
UI; the only profile in the survey that looks drawn rather than engineered.
Take: **illustration is an open lane.**

### Storytelling from the work itself

**[JGit705](https://github.com/JGit705)** — a mechanical engineer moving into
data. The hero is a route map of London; project cards carry small bar charts
and radar diagrams. The visuals are specific to what he does, which makes them
far more memorable than generic neon. And his About section is plain markdown —
on a phone it's the most readable thing on the page. Take: **draw from the real
work; let markdown carry the reading.**

**[JConfessor](https://github.com/JConfessor)** — a data analyst in wind energy.
An animated turbine hero, a pipeline diagram ("from raw signal to something
someone opens") and a section titled *"The chart I read for a living"* — a
turbine power curve. One chart from the actual job says more than a skills grid.
Take: **show the one artefact that defines the work.**

**[sepahead](https://github.com/sepahead)** — a contribution chart plotted as a
trajectory, a weekday donut, a repository grid, and a node graph of how his
projects connect to each other. A diagram of his own work rather than of his
tools. Take: **map relationships between projects, not proficiency in
languages.** Also the densest: 28 of 33 cards are illegible on a phone.

### Systems and HUDs

**[SergiGTAr](https://github.com/SergiGTAr)** — `SERGIGTAR OS // PUBLIC NODE`.
Neon green on black, huge condensed headline, status panels, a command line,
bordered CTA buttons. A loud aesthetic held together by strict consistency —
every panel uses the same border, type and spacing. Take: **a bold style works
when it's systematic.**

**[getaudra](https://github.com/getaudra)** — `SYSTEMS ONLINE` command centre with
a mission pipeline (idea → research → prototype → test → falsify → iterate).
Notable for honesty: it states that its language labels "describe observed
repository activity groupings, not skill percentages or proficiency claims".
Take: **label data for what it is.**

**[Dhyanesh006](https://github.com/Dhyanesh006)** — a Matrix terminal carried
through every section: boot sequence, `cat tech-stack.dat`, stats, activity,
trophies. Its README notes the stats are "auto-refreshed daily from the GitHub
API… pure SVG + SMIL, no external card services" — deliberately avoiding the
third-party generators the survey found dying. Take: **generate your own data
panels; don't rent them.**

### Concepts and formats

**[brandon-fryslie](https://github.com/brandon-fryslie)** — the header is a
newspaper masthead dated today, followed by an auto-generated changelog of the
last 24 hours and the week, written as real text. The profile as a daily
edition — and it openly says it was "hand-crafted by generative AI". Take:
**a format is a stronger idea than a style.**

**[marcizhu](https://github.com/marcizhu)** — the whole README is a playable
chess game. Moving means clicking a link that opens a GitHub Issue; an Action
plays the move and updates the board. The canonical example of the one real
input channel a README has. The board is a table of images, which on a phone
scrolls sideways rather than shrinking. Take: **Issues are the interaction
layer.**

**[atikulmunna](https://github.com/atikulmunna)** — black and white throughout;
the banner is an animated side-scrolling game, the contribution graph an
invaders-style animation. Game motion used as identity, in a disciplined
monochrome. Take: **restraint in colour lets motion carry personality.**

### Restraint

**[SimarBhatiaSB7](https://github.com/SimarBhatiaSB7)** — a huge bold name, one
red accent, monospace metadata rows, numbered sections. The clearest example of
Swiss-style typographic hierarchy. It represents a template family (see below).
Take: **scale contrast and one accent colour are enough.**

**[adamalston](https://github.com/adamalston)** — the entire README is one
orbital "observatory" SVG, with separate dark and light versions served through
`<picture>`. Its HUD labels render at 3px on a phone — but they're texture; the
orbit graphic is the message and reads fine. Take: **one strong object can be the
whole profile.**

**[10ishk](https://github.com/10ishk)** — a code-editor hero, an orbital skill
diagram and a terminal project list, then native markdown `<details>` for each
project's specifics. SVG for polish, markdown for depth and real text. Take:
**split the work between SVG and markdown on purpose.**

## A template family

**umang-eng**, **harkirat-data**, **SimarBhatiaSB7** and **aniketpitre** share one
layout — a `PORTFOLIO — INDEX Nº 001` header, numbered sections, `FIG.` captions.
umang-eng and harkirat-data carry all four markers checked in their SVG source
(`INDEX Nº`, `~/01-whoami`, `FIG. 0`, `DATA IN MOTION`); the other two share the
header. The text is personalised, so byte-hashing can't catch it — it took
looking at them side by side, then confirming in source. Listed once, via
SimarBhatiaSB7, rather than as four originals.

## Worth studying for one idea

- **[erogluyusuf](https://github.com/erogluyusuf)** — skill icons laid out as a
  keyboard, a committed PNG (`key.png`). A genuinely unexpected metaphor. The
  rest of the page is a pacman contribution graph (an Action's output) and repo
  cards from a card service he built himself on a free Vercel deployment; all
  12 cards are illegible on a phone and one image is broken. The keyboard is
  the idea worth taking.
- **[codeSTACKr](https://github.com/codeSTACKr)** — auto-updated lists of latest
  videos and blog posts as plain text. Unglamorous, and legible on every screen.
  (It still embeds the dead github-readme-stats public instance.)
- **[BrunnerLivio](https://github.com/BrunnerLivio)** — ironic 90s GeoCities:
  WordArt title, spinning globe, and a guestbook that works through Issues.
- **[nihalsheikh](https://github.com/nihalsheikh)** — a glassy dashboard card done
  with real polish; the conventional idea at its best.
- **[JackLuciano](https://github.com/JackLuciano)** — one warm orange accent held
  across a pipeline diagram, telemetry grid, heatmap and 3D contribution graph.

## What none of them do

- **Stay readable at 309px while being ambitious.** The gap noted at the top.
- **Treat dark and light as equal citizens.** Five of the fifteen have no theme
  switching at all. The rest were reviewed in dark mode only; whether their
  light versions hold up is a Phase 3 question, not yet answered.
- **Use motion sparingly.** Animation is everywhere; almost nothing settles.
- **Combine real interactivity with high design.** marcizhu is interactive but
  plain; the beautiful profiles are static.
