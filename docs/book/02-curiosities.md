# 2 · Cabinet of Curiosities

The strange, rare and surprisingly clever things people have put in a profile
README. Everything here was seen on a real profile we photographed or in a
verified tool repository; where a code-search probe could put a rough number on
how rare it is, the entry says so.

A note on the rarity figures: they come from GitHub code search over files named
`README.md`, counting how many of the first hundred matches were actual
`username/username` profile repositories. Code search matches loosely — when we
opened the READMEs behind the map probe, one of three named examples no longer
contained a map — so treat the numbers as "people really do this", not a census,
and trust the entries marked *confirmed*, which we opened and checked.

**Contents** — [Playable](#playable) · [Your life, live](#your-life-live) ·
[Grown, not drawn](#grown-not-drawn) · [Things GitHub renders that almost nobody uses](#things-github-renders-that-almost-nobody-uses) ·
[Collectibles & social proof](#collectibles--social-proof) · [Runnable](#runnable) ·
[Graveyard](#graveyard)

---

## Playable

A README can't run code, but a link can open a pre-filled issue, and an Action
can react to the issue by redrawing the board. Every game below works that way.

### The Royal Game of Ur

<img src="https://raw.githubusercontent.com/rossjrw/rossjrw/play/games/current/board.4710.svg" width="420" alt="The current board of a community game of the Royal Game of Ur: a wooden grid of rosette and dotted tiles with black and white pieces">

[rossjrw](https://github.com/rossjrw) · a 4,500-year-old Mesopotamian board game,
played by anyone who visits

Teams, dice (rendered as tetrahedral dice images), a move menu of links, a game
log, and *game number 30-and-counting*. Visitors join a team by making a move.
Of all the playable profiles, this is the one nobody else has: an ancient game,
played collectively, on a résumé.

### Community chess

[timburgan](https://github.com/timburgan) started it; [marcizhu](https://github.com/marcizhu)
runs an open tournament with the move list as a table of links (`A8 → A1, A2, …`)
and a leaderboard of the most moves made. Code search found chess-via-issues on
13 of the first 100 matching READMEs that were profiles.

### Connect Four with a bot

[jonathangin52](https://github.com/jonathangin52) — red vs blue teams, a
`Connect4Bot` you can request a move from, a counter of 20,000+ moves played and
a top-10 leaderboard of the humans who've played most.

### Tic-tac-toe decided by crowd vote

[DoubleGremlin181](https://github.com/DoubleGremlin181) — each empty square is an
image link that counts clicks and bounces you back; once an hour an Action plays
whichever square was clicked most. Hand-drawn X and O.

### A community word cloud

[JessicaLim8](https://github.com/JessicaLim8) — "Where are you hoping to travel
next?" Visitors add a word through an issue and the cloud regenerates; hundreds
of contributors listed underneath. The prompt changes periodically, so the page
is never finished.

### Game of Life, seeded from your contributions

[ethomson](https://github.com/ethomson) — the contribution graph becomes the
initial state of Conway's Game of Life (a four-colour "Quad Life" variant, so
intensity survives), served as an animated GIF by a small server. Viewed directly
it keeps rendering the next generation forever; through GitHub's image proxy it
stops after 20 frames, which the author explains on the page.

### A guestbook

[BrunnerLivio](https://github.com/BrunnerLivio) — a real guestbook table of
visitor avatars, dates and messages, in a profile styled as a 1998 homepage.

**Also seen:** 2048, Minesweeper, Wordle and chess-vs-AI kits in
[readme-games](https://github.com/Tech-Codes/readme-games); vote-driven multiplayer
games written up by [Leonardo Montini](https://leonardomontini.dev/4-github-games-readme-profiles/).

---

## Your life, live

Things that change because the author's *life* changed, not because they pushed.

| Item | Seen on | What it does |
|---|---|---|
| **Server telemetry** | [itgoyo](https://github.com/itgoyo) | CPU, memory and disk gauges for the author's own server, plus a "latest followers" leaderboard |
| **Live chess games** | [andyruwruw](https://github.com/andyruwruw) | Current chess.com games drawn as boards, opponent names underneath |
| **Chess rating chart in ASCII** | [sciencepal](https://github.com/sciencepal) | The last 100 blitz games as a text line chart in a code block, with a last-updated timestamp |
| **Discord presence** | [SwezyDev](https://github.com/SwezyDev) | What they're playing right now, with elapsed time. The common way to build one is [lanyard-profile-readme](https://github.com/cnrad/lanyard-profile-readme) |
| **Now playing, with a waveform** | [novatorem](https://github.com/novatorem) | The original Spotify widget; [natemoo-re](https://github.com/natemoo-re) adds top tracks |
| **Anime watched** | [lowlighter](https://github.com/lowlighter) | An AniList grid of shows and favourite characters inside a metrics infographic |
| **Latest YouTube uploads** | [midudev](https://github.com/midudev) | Thumbnail grids for two channels, kept current |
| **A meeting booking card** | [anmol098](https://github.com/anmol098) | "30 Min Meeting" — pick a slot straight from the profile |
| **A random meme per load** | [techytushar](https://github.com/techytushar) | "Refresh the page to see a new meme" |
| **Commit clock** | [productive-box](https://github.com/maxam2017/productive-box) | Early bird or night owl, from the hours you commit |
| **Competitive programming** | [mazassumnida](https://github.com/mazassumnida) · [LeetCode card](https://github.com/JacobLinCool/LeetCode-Stats-Card) · [Codeforces](https://github.com/RedHeadphone/codeforces-readme-stats) | solved.ac tiers, LeetCode heatmaps, Codeforces ratings |
| **Visitor flags** | [github-visitor-counter](https://github.com/ChanMeng666/github-visitor-counter) | Counts views and shows the country flags of visitors |

---

## Grown, not drawn

Generated art that *is* your history rather than illustrating it.

- **[Kodama](https://github.com/orijitghosh/kodama)** — a bonsai: commits grow
  foliage, merged PRs ripen into fruit, reviews hang lanterns, streaks blossom.
  One image URL, redrawn daily.
- **[Git Bonsai](https://github.com/abhisheknaiidu/awesome-github-profile-readme/pull/1755)** —
  a deterministic pixel-art bonsai as an animated GIF that keeps growing.
- **[Repo Garden](https://github.com/Aaryan1524/Bosnai)** — a botanical SVG from the
  git log: contributors bloom, long silences drop autumn leaves, **force-pushes snap
  a branch**, merges leave graft rings.
- **Arcade contribution graphs** — beyond Snake and Pac-Man, the
  [pacman-contribution-graph](https://github.com/abozanona/pacman-contribution-graph)
  engine also renders **Breakout, Galaga, Puzzle Bobble, Bomberman and
  Minesweeper** from your grid. Pac-Man appeared on 98 of the first 100 matching
  READMEs, so it is not rare — *the other five are*.
- **[Matrix-rain contributions](https://github.com/N1k0droid/matrix-svg-contrib)** —
  empty days loop as falling code; days you contributed fall and lock into
  phosphor-green cells.
- **CRT / equalizer contributions** — the same grid as a glowing CRT or a bouncing
  audio equalizer.
- **[gitfiti](https://github.com/gelstudios/gitfiti)** (8,400★) — the opposite
  direction: backdated commits that *paint* a picture or word into the real graph.
- **[GitHub Skyline](https://dev.to/github/view-your-github-contribution-graph-as-an-animated-skyline-3d-print-it-2dpl)** —
  a year of contributions as a 3D city you can rotate and export to a 3D printer.
  (Type the Konami code on the Skyline page for an easter egg.)
- **Dithered photo portraits** and **ASCII portraits that type themselves** —
  [ascii-profile-kit](https://github.com/mithun50/ascii-profile-kit),
  [gh-ascii](https://github.com/crafter-station/gh-ascii).

---

## Things GitHub renders that almost nobody uses

Native to GitHub's markdown, no image or service involved, so they can't break.
[Chapter 4](04-native.md) demonstrates each one live.

| Feature | Rarity signal | Seen on |
|---|---|---|
| **An interactive 3D model** (ASCII STL in a ```` ```stl ```` block) | confirmed on 5 profiles | [TheAdkk](https://github.com/TheAdkk), [leandrumartin](https://github.com/leandrumartin), [olorcain](https://github.com/olorcain); [readme-3d](https://github.com/nirholas/readme-3d) converts GLB/OBJ/STL to fit GitHub's 512 KB limit |
| **An interactive map** (```` ```geojson ```` / ```` ```topojson ````) | confirmed on 4 profiles | [BEPb](https://github.com/BEPb), [BagToad](https://github.com/BagToad) (GeoJSON); [Sakib-Sobaha](https://github.com/Sakib-Sobaha), [nanimm88](https://github.com/nanimm88) (TopoJSON) |
| **A mind-map of your skills** (```` ```mermaid ```` `mindmap`) | — | [pr2tik1](https://github.com/pr2tik1) |
| **LaTeX maths** | 1 profile in the sample | — |
| **Alert callouts** (`> [!NOTE]`) | 3 profiles in the sample | — |

---

## Collectibles & social proof

- **[Holopin](https://github.com/HwangTaehyun)** — collectible event badges
  (Hacktoberfest levels, DigitalOcean) arranged on a board, like enamel pins.
- **Supporters in the banner** — [thenolle](https://github.com/thenolle) bakes the
  avatars of the last six sponsors into the header art.
- **GitHub's own achievements** — the complete list of profile achievements and
  how to earn them is [maintained here](https://github.com/drknzz/GitHub-Achievements).
- **Sponsor walls** — generated by tools like `sponsorkit`, seen on 6 profiles in
  the sample.
- **A party-parrot parade** — [ashleymavericks](https://github.com/ashleymavericks).

---

## Runnable

- **`npx <your-name>`** — [jcubic](https://github.com/jcubic) and
  [anmol098](https://github.com/anmol098) publish an npm package whose only job is
  to print a business card in your terminal. The README just tells you the command.
- **An album-cover carousel** — [arkk200](https://github.com/arkk200)'s
  [record-rotate](https://github.com/arkk200/record-rotate) decorates a profile with
  a rotating row of album covers.

---

## Graveyard

Items still embedded on thousands of profiles that no longer work.

- **ClustrMaps and RevolverMaps visitor globes.** RevolverMaps shut down in late
  2024 and ClustrMaps has been unreachable in 2026; the widgets now render nothing.
  [UmamiMaps](https://github.com/Selenium39/umami-maps) is the self-hosted
  replacement.
- **The public github-readme-stats instance** — loads 0% of the time; still in 24%
  of profiles ([survey](../survey/FINDINGS.md)).
- **Keepalive workflows** — the widely used `keepalive-workflow` Action, which kept
  repositories looking active so GitHub wouldn't pause their scheduled workflows after
  60 days, was
  **disabled by GitHub for violating its Terms of Service**, according to its
  author's profile ([gautamkrishnar](https://github.com/gautamkrishnar)). Anything
  that commits just to look active is on the wrong side of that line.
