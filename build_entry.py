#!/usr/bin/env python3
"""Sunday, In Full - v2 refresh.

Draws entry.png (1024x1024): the world news of Sunday 22 November 2026
on one sunlit front page. Sunlit Crime-Noir identity: warm sand paper,
charcoal ink, one vivid red accent, hard diagonal shadow, condensed
editorial type (Liberation Sans Bold, horizontally condensed).

Pure Pillow, no network, no randomness, no clock - deterministic.
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (243, 233, 205)
SAND_DARK = (199, 178, 128)
INK = (33, 29, 22)
INK_SOFT = (84, 75, 60)
RED = (176, 30, 20)
CREAM = (250, 244, 226)

F_DIR = "/usr/share/fonts/truetype/liberation/"
F_BOLD = F_DIR + "LiberationSans-Bold.ttf"
F_REG = F_DIR + "LiberationSans-Regular.ttf"

W = H = 1024
MARGIN = 34
SQUEEZE = 0.84

img = Image.new("RGB", (W, H), PAPER)
dr = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def tw(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, s, f, maxw):
    """Wrap string s to lines of natural width <= maxw."""
    words, lines, cur = s.split(), [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if tw(draw, trial, f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def squeezed(base, xy, lines, f, fill, lh, squeeze=SQUEEZE):
    """Draw text lines on a scratch layer, condense horizontally, paste."""
    if not lines:
        return 0
    nat_w = max(tw(dr, ln, f) for ln in lines)
    layer = Image.new("RGBA", (int(nat_w) + 4, lh * len(lines) + 4), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for i, ln in enumerate(lines):
        ld.text((0, i * lh), ln, font=f, fill=fill + (255,))
    layer = layer.resize((max(1, int(layer.width * squeeze)), layer.height),
                         Image.LANCZOS)
    base.paste(layer, (int(xy[0]), int(xy[1])), layer)
    return layer.width


def tracked(draw, xy, s, f, fill, tracking=2):
    """Draw a short label with letter tracking (no squeeze)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += tw(draw, ch, f) + tracking
    return x - tracking


# ---------------------------------------------------------------- masthead
KICK = font(F_REG, 13)
tracked(dr, (MARGIN, 14), "THE WORLD IN ONE PAGE - FULL SUNDAY EDITION", KICK, INK_SOFT, 3)
r_txt = "41 STORIES - ONE IMAGE"
dr.text((730 - tw(dr, r_txt, KICK), 14), r_txt, font=KICK, fill=RED)

# hard diagonal shadow wedge, top-right, with the red sun caught in it
dr.polygon([(742, 0), (1024, 0), (1024, 116), (872, 38)], fill=INK)
dr.ellipse([884, 10, 962, 88], fill=RED)
dr.polygon([(742, 0), (1024, 0), (1024, 46), (806, 0)], fill=INK)

TITLE_F = font(F_BOLD, 84)
squeezed(img, (MARGIN - 2, 26), ["SUNDAY, IN FULL"], TITLE_F, INK, 84)

dr.rectangle([MARGIN, 118, W - MARGIN, 122], fill=INK)
dr.rectangle([MARGIN, 125, W - MARGIN, 127], fill=RED)
DATE_F = font(F_BOLD, 14)
dr.text((MARGIN, 132), "SUNDAY - 22 NOVEMBER 2026", font=DATE_F, fill=INK)
sub = "Antalya to Hong Kong, Gaza to Las Vegas - every story dated today"
dr.text((W - MARGIN - tw(dr, sub, KICK), 133), sub, font=KICK, fill=INK_SOFT)

# ---------------------------------------------------------------- hero
HY = 156
TAG_F = font(F_BOLD, 14)
tag = "TOP STORY - CLIMATE"
tagw = tw(dr, tag, TAG_F) + 18
dr.rectangle([MARGIN, HY, MARGIN + tagw, HY + 22], fill=RED)
dr.text((MARGIN + 9, HY + 3), tag, font=TAG_F, fill=CREAM)

# hero graphic: sun disc behind hard shadow bars (no text over it)
gx0, gy0, gy1 = 756, HY + 4, HY + 118
dr.ellipse([gx0 + 126, gy0 + 16, gx0 + 216, gy0 + 106], fill=RED)
for i in range(4):
    bx = gx0 + 8 + i * 58
    dr.polygon([(bx, gy1), (bx + 26, gy1), (bx + 62, gy0), (bx + 36, gy0)], fill=INK)

HERO_F = font(F_BOLD, 40)
hero_lines = wrap(dr, "CLIMATE TALKS ON THE BRINK AS ANTALYA TABLES LAST TEXT",
                  HERO_F, 700 / SQUEEZE)
squeezed(img, (MARGIN, HY + 28), hero_lines, HERO_F, INK, 43)
BRIEF_F = font(F_REG, 15)
hero_brief = ("Two days past deadline, COP31's presidency tabled a new package "
              "at dawn - fossil-fuel wording stripped out, an approval session "
              "set for 0600 GMT, and the EU warning it would rather walk away "
              "than sign a weak deal.")
blines = wrap(dr, hero_brief, BRIEF_F, 700)
by = HY + 28 + 43 * len(hero_lines) + 6
for ln in blines:
    dr.text((MARGIN, by), ln, font=BRIEF_F, fill=INK_SOFT)
    by += 19
HERO_END = by + 8

# ---------------------------------------------------------------- ticker
TY = HERO_END + 4
dr.rectangle([MARGIN, TY, W - MARGIN, TY + 26], fill=INK)
TICK_F = font(F_REG, 13)
tick = ("ALSO TODAY - SEOUL POSTS $75,000 REWARDS FOR EXAM-CHEAT TIP-OFFS"
        "  -  SAO TOME REAPPOINTS PM AMERICO RAMOS")
dr.text((MARGIN + 10, TY + 6), tick, font=TICK_F, fill=CREAM)
GRID_Y = TY + 40

# ---------------------------------------------------------------- grid
HEAD_F = font(F_BOLD, 15)
ITEM_F = font(F_BOLD, 14)
BRIEF2_F = font(F_REG, 11)
COL_W = 227
GUT = 16
COL_X = [MARGIN + i * (COL_W + GUT) for i in range(4)]

SECTIONS = [
    ("THE WORLD", [
        ("ZELENSKYY: FOUR-NATION TALKS MUST DELIVER", "Kyiv raises the bar for peace talks"),
        ("NATIONS AGREE UN PACT ON AUTONOMOUS WEAPONS", "First global rules for killer robots"),
        ("APEC ENDS WITH US-CHINA FAULT LINES OPEN", "Trade, Taiwan, tech unresolved"),
        ("FBI CRIME DATABASE HIT BY REPORTED BREACH", "Trump floats a 'positive spin'"),
        ("PANAMA VOWS TO BLOCK DEAL WITHOUT FOSSIL-FUEL WORDS", "Antalya holdout digs in"),
        ("MELANIA TRUMP HOPES FOR UKRAINE CEASEFIRE BY CHRISTMAS", "First lady voices wish aloud"),
    ]),
    ("MIDDLE EAST", [
        ("TANKERS STRUCK NEAR OMAN AS HORMUZ ATTACKS WIDEN", "UKMTO reports two ships hit"),
        ("IRAN ASSEMBLES TANKER CONVOY TO BREAK US BLOCKADE", "Tehran dares Washington at sea"),
        ("IRAQI FORCES TAKE OVER KATAIB HEZBOLLAH CHECKPOINTS", "Baghdad asserts control"),
        ("SYRIA INTERCEPTS WEAPONS BOUND FOR LEBANON", "Shipment seized, officials say"),
        ("129 BODIES PULLED FROM RUBBLE IN CENTRAL GAZA", "Recovery teams keep digging"),
    ]),
    ("ASIA-PACIFIC", [
        ("HONG KONG VOTES ON 723 ELECTION COMMITTEE SEATS", "856 candidates; 69.6% by 11am"),
        ("SEARCH FOR 36 MISSING AFTER BANTEN FACTORY FIRE", "Candy plant blaze killed three"),
        ("BMKG WARNS HEAVY RAIN FOR EIGHT PROVINCES TODAY", "Alert tied to cyclone seed 96S"),
        ("PAKISTAN'S RULING PARTY FLOATS PROVINCES REFERENDUM", "Partner PPP objects"),
        ("JAKARTA TO REVIVE FIRE-HIT KUNSTKRING MONUMENT", "Menteng landmark to be restored"),
        ("PAM JAYA TEAMS WITH SHENZHEN FIRM ON WATER TECH", "Jakarta utility swaps know-how"),
    ]),
    ("AFRICA", [
        ("GHANA UNVEILS 'HERITAGE SERIES' BANKNOTES", "Nkrumah, Annan on the new notes"),
        ("AL-SHABAAB CLAIMS HUNDREDS DEAD IN SOMALI AMBUSH", "Claim not verified independently"),
        ("KENYA DISCHARGES ITS LAST EBOLA PATIENT", "DRC death toll passes 5,300"),
        ("SAHEL STATES REOPEN TALKS WITH WEST AFRICA BLOC", "Dialogue restarts after rift"),
    ]),
    ("EUROPE", [
        ("NORWAY'S TOP COURT VOIDS DISPUTED OIL LICENCES", "Win for climate litigants"),
        ("LAGARDE EXITS: EU HUNTS FOR A NEW ECB CHIEF", "Succession race opens up"),
        ("EU FLOATS DIGITAL TAX TO FUND ITS BUDGET", "Berlin, Paris split over cuts"),
        ("DENMARK PUSHES EU CURBS ON RUSSIAN TOURISTS", "Move follows alleged murder plot"),
        ("ZAGREB RALLIES OVER PSYCHIATRIC HOSPITAL SCANDAL", "Protesters demand answers"),
        ("EU PLEDGES POLAND SUPPORT AFTER RUSSIAN AIR BREACH", "Capitals denounce incursion"),
    ]),
    ("SPORT & CULTURE", [
        ("VERSTAPPEN INHERITS POLE FOR TONIGHT'S VEGAS RACE", "Antonelli fastest, drops five"),
        ("ZVEREV v ALCARAZ IN TURIN FINAL TODAY", "Top seeds meet at 18:00 CET"),
        ("RAHUL, PANT TONS LIFT INDIA TO 720/9 IN NZ TEST", "India's highest Test total there"),
        ("AUSTRALIA BOWL FIRST AS SMITH MISSES SA DECIDER", "Injured Smith sits out finale"),
        ("AWAR ODHIANG NAMED MODEL OF THE YEAR", "Refugee-born South Sudanese star"),
    ]),
    ("BUSINESS & TECH", [
        ("ANTHROPIC'S RECORD IPO MEETS TECH'S WORST WEEK SINCE 2020", "Listing lands in a storm"),
        ("NVIDIA FINANCES FACE SEC INQUIRY, SOURCES SAY", "Probe amid scramble at top"),
        ("BITCOIN CLIMBS BACK ABOVE $60,000", "Up more than 2% on the day"),
        ("SILVER SLIDES IN INDIA AFTER BULLION CRASH", "Delhi and Mumbai rates fall"),
        ("US LAWMAKERS PUSH BAN ON CHINESE AI IN FEDERAL SYSTEMS", "Agencies in the crosshairs"),
        ("KENYA SEALS DEAL FOR 293,600 SAUDI JOBS", "Worker protections questioned"),
    ]),
]

COLUMNS = [[0, 1], [2, 3], [4, 5], [6]]  # section indices per column


def draw_section(x, y, title, items):
    dr.rectangle([x, y, x + COL_W, y + 23], fill=INK)
    dr.rectangle([x, y, x + 7, y + 23], fill=RED)
    dr.text((x + 14, y + 4), title, font=HEAD_F, fill=CREAM)
    y += 30
    for head, brief in items:
        hl = wrap(dr, head, ITEM_F, COL_W / SQUEEZE)
        squeezed(img, (x, y), hl, ITEM_F, INK, 15)
        y += 15 * len(hl) + 1
        bl = wrap(dr, brief, BRIEF2_F, COL_W)
        for ln in bl[:1]:
            dr.text((x, y), ln, font=BRIEF2_F, fill=INK_SOFT)
            y += 12
        y += 4
    return y


col_bottoms = []
for ci, sec_ids in enumerate(COLUMNS):
    y = GRID_Y
    for si in sec_ids:
        title, items = SECTIONS[si]
        y = draw_section(COL_X[ci], y, title, items) + 4
    col_bottoms.append(y)

# ------------------------------------------------------- numbers panel (col 4)
px, py = COL_X[3], col_bottoms[3] + 2
dr.rectangle([px, py, px + COL_W, py + 23], fill=RED)
dr.text((px + 14, py + 4), "THE DAY IN NUMBERS", font=HEAD_F, fill=CREAM)
py += 31
NUM_F = font(F_BOLD, 28)
LAB_F = font(F_REG, 11)
stats = [("723", "Hong Kong seats contested today"),
         ("69.6%", "HK turnout by 11:00"),
         ("36", "workers missing in Banten"),
         ("5,300+", "Ebola deaths in DR Congo"),
         ("$5.17M", "ATP champion's purse"),
         ("~200", "nations at the COP31 table")]
for i in range(0, 6, 2):
    for j in range(2):
        num, lab = stats[i + j]
        sx = px + j * (COL_W // 2)
        squeezed(img, (sx, py), [num], NUM_F, RED, 28)
        ll = wrap(dr, lab, LAB_F, COL_W // 2 - 8)
        ly = py + 31
        for ln in ll[:2]:
            dr.text((sx, ly), ln, font=LAB_F, fill=INK_SOFT)
            ly += 13
    py += 56
col_bottoms[3] = py

# ---------------------------------------------------------------- footer
FY = 996
dr.rectangle([MARGIN, FY - 8, W - MARGIN, FY - 6], fill=SAND_DARK)
FOOT_F = font(F_REG, 11)
foot = "Every story dated Sunday 22 November 2026 - compiled 12:00 WIB, Jakarta"
dr.text((MARGIN, FY + 2), foot, font=FOOT_F, fill=INK_SOFT)
rfoot = "SUNDAY, IN FULL - V2"
dr.text((W - MARGIN - tw(dr, rfoot, FOOT_F), FY + 2), rfoot, font=FOOT_F, fill=RED)

img.save("entry.png", optimize=True)
print("column bottoms:", col_bottoms, "| grid start:", GRID_Y, "| hero end:", HERO_END)
