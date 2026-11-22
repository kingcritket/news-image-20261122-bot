# Build Report — V2 Refresh (22 Nov 2026, ~12:00 WIB)

Entry: news-image-20261122 "Sunday, In Full" — v2, a full rebuild of
the v1 page (32 stories) around the day's later developments.
Build only; submission is handled separately by the main agent.

## Final artifact

- `entry.png` — 1024×1024 PNG, 396,617 bytes
- sha256: `cdbcd6f46ef01530d59742c62e71936cc43f752ed927c3d53ae0839782098e36`
- Stories on the page: **41** (1 hero + 38 grid + 2 ticker),
  across 7 regions, plus a "Day in Numbers" panel of dated figures
- Code: `build_entry.py` (PIL composition) and `main.py` (shipper)
  both written from scratch in this session — no v1 code was read,
  copied or patched. `python3 main.py` smoke-tested: ships
  entry.png to the output dir correctly.

## What changed vs v1

- **New lead.** V1 led with the overnight barrage on Ukraine (early-
  morning news). By midday the day's centre of gravity had moved:
  v2 leads with the COP31 endgame — the presidency's dawn package,
  the 0600 GMT approval session, the EU's walk-away warning.
- **New same-day stories added:** Hong Kong's Election Committee
  poll (with the official 69.61% 11:00 turnout), the Banten
  factory-fire search for 36 missing, BMKG's eight-province rain
  alert, the ATP Finals title match, Ghana's Heritage banknotes,
  Kenya's last Ebola discharge, Lagarde's ECB exit, Anthropic's
  IPO, Bitcoin back over $60,000, and ~20 more.
- **Fully typographic build.** V1 mixed three AI scene photos into
  the page; v2 is pure editorial type and drawn geometry (sun disc
  behind hard shadow bars), which keeps every column dense without
  dead space and keeps the Sunlit Crime-Noir identity — sand paper,
  charcoal ink, single red accent, hard diagonal shadow — intact.
- **Denser grid:** 4 columns × 7 sections + a "Day in Numbers"
  panel, vs v1's 32 items.

## Date verification (per skill rules)

Every item was traced to reporting dated 22 Nov 2026, and the
*event* date was checked separately from the *publication* date.
Sources are listed per story in README.md. Notable exclusions
after checking:

- **Peru M6.7 Junín earthquake** — Sunday damage roundups are
  fresh, but the quake struck Friday ~19:09 local (20 Nov).
  Excluded, despite rival entries carrying it.
- **Las Vegas GP qualifying** — a 21 Nov event. Only the race
  itself (today, 04:00 UTC; Verstappen on inherited pole) is used.
- **Sinaloa capture / Bahrain strike follow-ups** — events of
  20–21 Nov; excluded.
- The Hong Kong turnout (69.61%) is the official 11:00 figure from
  info.gov.hk; the ATP $5.17M purse is the tournament's stated
  undefeated-champion figure, not an estimate. No figure on the
  page is presented as fact beyond its source.

## Self-audit (visual, on the rendered PNG)

Round 1 — first render overflowed: column bottoms at
1164/1091/1147/1049 against a footer at 988. Fixed by compressing
the masthead and hero and tightening grid type (headline 14px,
brief 11px, leaner section bars).
Round 2 — three defects found on inspection:
  1. The red "stories" kicker at top-right ran underneath the
     diagonal shadow wedge and was partly illegible → right-aligned
     to end at x=730, clear of the wedge.
  2. The hero sun disc protruded below its shadow bars → resized
     and centred inside the band.
  3. Columns 1 and 3 ended 1px into the footer rule → item and
     section gaps trimmed; final bottoms 970/923/970/887 (18px
     clearance).
Round 3 — final read-back: masthead count corrected from 42 to 41
after a manual recount of the page. No clipped or overlapping
text, no text over shadow, palette disciplined (paper/charcoal/
one red), headlines legible at thumbnail size, all briefs render
on a single line as designed.
