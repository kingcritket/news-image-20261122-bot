# BUILD REPORT — news-image-20261122, v3 "Sunday, In Full" (full-day edition)

Built: Sunday 22 Nov 2026, ~20:00 WIB, in one session, from scratch.
The previous version's code files were deleted unread and rewritten
in full (authorship hygiene, per the entry-checks skill).

## Artifact

- `entry.png` — 1024×1024 PNG, **194,934 bytes**
- sha256: `16e9f6e13897ee1b4077cf1775d4aeea5694eb0722511a0d30bb3b55b160ea46`
- Deterministic: two consecutive runs produced the identical hash.
- `main.py` smoke-tested: rebuilds the PNG and verifies size/format.

## Packaging fix (post-intake, same evening)

The v3 submission passed kit check but was rejected at intake on
`run_completes`: the grader runs `python3 -P -s /bot/main.py`, and
the old `main.py` was a thin wrapper importing a sibling module —
under `-P` (safe path) the script's directory is not on `sys.path`,
so the import died; it also wrote into the repo dir, ignoring
`MAKEFUN_OUTPUT_DIR`, while the grader mounts `/bot` read-only.
Fix: `main.py` is now one self-contained file (stdlib + PIL only,
no local imports) and writes `entry.png` to `$MAKEFUN_OUTPUT_DIR`
when set, falling back to the script's directory. Verified with the
grader's exact shape — read-only copy, `MAKEFUN_OUTPUT_DIR` pointed
at a scratch dir, `python3 -P -s <copy>/main.py` → exit 0 and the
PNG in the output dir byte-identical (sha256 unchanged, above).
`build_entry.py` was removed; the render itself is untouched.

## Grader exit-1: root cause and final fix (round 5)

Round 4's self-contained renderer STILL failed intake with exit 1,
so the failure was reproduced locally under a faithful sandbox:
read-only repo copy, foreign cwd, uid 65534, empty environment,
`MAKEFUN_OUTPUT_DIR` scratch dir, `systemd-run` scope with
MemoryMax=512M / MemorySwapMax=0, `taskset -c 0`, and the grader's
exact invocation `python3 -P -s <copy>/main.py`. Under those
constraints the renderer PASSED locally (exit 0, 0.33 s, PNG
byte-identical) — memory, permissions, cwd and runtime exonerated.
The remaining deltas were host resources this VM has and a bare
pinned python:3.13 grader image does not. Both were reproduced:

1. **Liberation fonts absent** (empty dir bind-mounted over
   /usr/share/fonts/truetype/liberation) → exit 1:
   `OSError: cannot open resource` from
   `ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 13)`
   at the first font load in `build()`.
2. **Pillow absent** (clean venv interpreter) → exit 1:
   `ModuleNotFoundError: No module named 'PIL'` at the module-level
   `from PIL import Image, ImageDraw, ImageFont`.

Either one alone kills a render-in-sandbox entrypoint; the grader
never shows stderr, so both present as the same bare exit 1.

**Root cause:** round 4 fixed the packaging (safe-path imports,
read-only mount, output dir) but kept the render-in-sandbox design,
which depends on Pillow and on host font files at absolute system
paths. The scored v2 entry never rendered in the sandbox at all —
its `main.py` was a standard-library-only shipper copying the
committed `entry.png` into `$MAKEFUN_OUTPUT_DIR`, which is why it
passed in the same grader.

**Fix:** `main.py` rewritten (whole file) as a stdlib-only shipper
on the v2 mechanism: locate the committed `entry.png` via
`__file__`, sanity-check its PNG signature and IHDR dimensions
(1024×1024) with a hand-rolled header read, copy it into
`$MAKEFUN_OUTPUT_DIR` (fallback: `out/` next to the script), and
verify the copy's size before exiting 0. No third-party imports,
no fonts, no rendering — nothing host-dependent remains. The full
renderer survives in git history (commit de786b9's `main.py`) for
future build-time use.

**Verification of the fix** (same faithful sandbox as above):
exit 0 in 63 ms, output sha256 unchanged
(`16e9f6e1…a46`). Repeated under the hostile variant — Liberation
fonts hidden AND the no-Pillow venv interpreter, all other
constraints still applied: exit 0 in 51 ms, sha256 unchanged.
`entry.png` itself is untouched by this fix.

## Concept

Same Sunlit Crime-Noir identity as v2 (user brief #2): sun-bleached
cream paper, warm sand panel, charcoal ink and section bars, one red
accent (kicker, ticks, sun, panel edge), a red sun disc sliced by a
hard diagonal charcoal shadow in the masthead corner (graphic only —
no text over the shadow), condensed-feel editorial type, fully
typographic, no photos.

## What changed vs v2 (41 stories, midday build)

- **Lead replaced with the outcome:** v2's "COP31 endgame" became
  the collapse — the closing plenary adopted nothing, the EU
  formally objected, Kurum conceded no consensus (Reuters, 22 Nov).
  Hero side items updated to the objection, the dawn text's contents
  (35-by-35, 1 Gt CCUS), and "first failure since Copenhagen 2009".
- **F1 carried as a result, not a preview:** Verstappen won the Las
  Vegas GP from pole by 0.639s (75th career win, 1:27:39.624, 50
  laps); Norris 2nd; Piastri 3rd from 17th; 35 lead changes;
  standings Antonelli 402 / Verstappen 304, P2 fight to Qatar
  (RaceFans, PlanetF1, FIA classification via reports dated 22 Nov;
  race run Sunday 22 Nov WIB).
- **Hong Kong updated to the final figure:** record 98.79% turnout,
  5,640 of 5,709 ballots (info.gov.hk; China Daily Asia, 22 Nov),
  replacing v2's midday 69.61%.
- **Cikande updated to Sunday's operation:** six bodies recovered,
  36 workers still sought (provisional), fire declared out at dawn
  after ~16 hours, Polda Banten DVI identification under way
  (SAR Banten / Kompas TV / Liputan6 reports, 22 Nov).
- **Story count 41 → 42;** weaker v2 items swapped for completed-day
  stories (Estonia border closure, ICE training watchdog, Hegseth
  memo, Gaza City bombardment, EU–Canada AI plan, two obituaries,
  Nigeria boat disaster, and more).

## Date verification (event date = 22 Nov 2026, checked per item)

- COP31 collapse, EU objection, dawn package: closing plenary and
  reports all dated Sunday 22 Nov (Reuters; The Curtain; CarrZee).
- F1 race: run Saturday night Las Vegas = Sunday 22 Nov WIB;
  results coverage dated 22 Nov (RaceFans 2026/11/22; RNT updated
  22 Nov 07:05 CET). Standings per FIA documents 64/65 as reported.
- Hong Kong: polls 09:00–18:00 Sunday; final turnout release dated
  22 Nov (info.gov.hk).
- BMKG alert: issued for Sunday 22 Nov; eight siaga provinces named
  (Aceh, North Sumatra, West Sumatra, Banten, West Java, Central
  Java, East Java, South Papua); cyclone seed 96S.
- Markets (Bitcoin >$60,000; Brent $89.95): Sunday snapshot levels,
  presented as Sunday lines, not as Friday closes.
- ATP Finals: the final is scheduled tonight 18:00 CET in Turin —
  carried as a fixture; **no result invented** (the match had not
  been played at build time).
- All remaining items traced to reporting dated 22 Nov (wire feeds,
  AP world pages, OneTurn News' Sunday edition, headline roundups).

**Excluded on date discipline:** Peru M6.7 quake (event Fri 20 Nov
local); F1 qualifying (21 Nov); Sinaloa cartel capture (Fri–Sat
20–21 Nov); EU–Indonesia CEPA signing (Sat 21 Nov, Brussels —
prominent in Sunday coverage but not a Sunday event); Kryvyi Rih
strike (Sat 21 Nov); Friday's AI stock sell-off as a dated event
(only Sunday market levels used); the Cikande fire's Saturday
outbreak (only Sunday's search/recovery carried; counts labelled
provisional because agencies' figures differ).

## Self-audit trail

- **Geometry iterations (pre-render):** the layout engine asserts a
  hard page bottom. Round 0 overflowed by ~83px (final bottom 1099);
  tightened leading/padding throughout → 1024.5; final nudges →
  1010, then 996 after the ticker fix. Column bottoms: 783 / 783 /
  815 (grid), final content bottom 996 of 1024.
- **Render round 1 (visual read-back):** page clean and legible;
  two defects found — (a) the masthead sun read as a plain red dot
  because the shadow wedge was nearly off-canvas; (b) the briefs
  ticker wrapped to a second line holding a single widow word
  ("71."). Fixed: disc enlarged and repositioned, shadow polygon
  redrawn so it visibly slices the disc; briefs trimmed.
- **Render round 2 (visual read-back):** sun now clearly cut by the
  hard diagonal shadow, no text touches the graphic; ticker fits
  one line; no clipped or overlapping text anywhere; no text over
  shadow; red used only as the single accent; masthead and hero
  headline dominate at thumbnail size; numbers panel and source
  line legible; footer clearance ~28px. No further defects found.
- **Count check:** masthead "42 STORIES" verified by manual recount
  of the story list (1 hero + 3 hero side + 31 grid + 4 sport +
  3 briefs = 42).
