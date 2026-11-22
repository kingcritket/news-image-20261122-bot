"""Sunday, In Full — v3 full-day edition (news-image-20261122).

Entrypoint and layout engine in ONE self-contained file: no sibling
or local imports, so the grader can run it as
``python3 -P -s /bot/main.py`` (safe-path mode, where the script's
own directory is not on sys.path) against a read-only mount.

A fully typographic front page in the Sunlit Crime-Noir system:
harsh noon light, sand and cream paper, charcoal ink, one red
accent, a hard diagonal shadow in the masthead corner, and strict
editorial type. Every story below is dated Sunday 22 November 2026;
items whose events belong to an earlier day were excluded on
purpose (see BUILD_REPORT.md).

Output: entry.png is written to $MAKEFUN_OUTPUT_DIR when that
environment variable is set, otherwise to this script's directory.
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (240, 231, 207)      # sun-bleached cream
SAND = (228, 213, 175)       # warm sand panel
INK = (26, 24, 20)           # charcoal ink
SOFT = (74, 68, 58)          # softened charcoal for standfirsts
FAINT = (133, 120, 96)       # taupe for rules and meta text
RED = (178, 32, 38)          # the single accent
BAR = (30, 28, 24)           # charcoal section bars

W, H = 1024, 1024
MARGIN = 36
RIGHT = W - MARGIN
CONTENT_W = RIGHT - MARGIN

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, int(size))


# ---------------------------------------------------------------- content
HERO_KICKER = "COP31 · ANTALYA · THE CLIMATE SUMMIT"
HERO_HEAD = "NO DEAL IN ANTALYA"
HERO_DECK = (
    "The longest climate summit ever ends in failure. After two days of "
    "overtime, the closing plenary refuses the presidents' dawn text — a "
    "ten-page package that never once names fossil fuels."
)
HERO_SIDE = [
    ("EU formally objects to the pact",
     "Ireland's O'Brien: a deal that 'does not even mention fossil fuels' "
     "fails the moment."),
    ("The dawn text: 35-by-35, minus the fuels",
     "Electrification to 35% by 2035 and a gigatonne of carbon capture — "
     "the phase-out words stripped out."),
    ("First failure since Copenhagen 2009",
     "Technical Article 6 decisions survive; the political cover deal "
     "does not. Addis Ababa inherits it."),
]

SECTIONS = {
    "EUROPE": [
        ("Estonia to close its Russian border",
         "Moscow threatens a response to the closure."),
        ("Denmark expels Russian attaché",
         "Copenhagen acts over an alleged plot; embassy silent."),
        ("Lagarde to quit ECB in February 2027",
         "She will leave the ECB presidency in February 2027."),
        ("Spain widens bank tax to fund housing",
         "Sánchez expands the levy to fund housing policies."),
        ("Finland curbs flights near the Gulf",
         "Helsinki reimposes restrictions over the eastern Gulf."),
        ("Norway fells London's Christmas tree",
         "The 69-foot Trafalgar spruce is cut outside Oslo."),
    ],
    "MIDDLE EAST": [
        ("Guards claim two Patriot systems hit",
         "Iran's IRGC says it disabled two US systems in Bahrain."),
        ("Bahrain: strike hit civilian property",
         "Manama condemns it as Tehran parades its launchers."),
        ("UAE ferries oil past Iran at Hormuz",
         "A risky shuttle moves Emirates crude past the blockade."),
        ("Four killed in Gaza City bombardment",
         "Israeli fire kills at least four amid the truce."),
        ("Settler attacks branded 'terrorism'",
         "Four West Bank sites hit in one night of raids."),
        ("Aoun: two hurdles to sovereignty",
         "Lebanon's president names Israel and Iran as obstacles."),
        ("Turkish spy chief meets Hamas team",
         "Ankara hosts a Hamas delegation in Istanbul on Sunday."),
    ],
    "ASIA-PACIFIC": [
        ("Hong Kong turnout a record 98.79%",
         "5,640 of 5,709 electors vote in the subsector polls."),
        ("Taiwan warns Carney over China ties",
         "Taipei warns Ottawa on deeper Beijing ties."),
        ("Mayon eruption stirs larger fears",
         "The Philippine volcano stirs fears of a bigger event."),
        ("Rohingya welcome genocide verdict",
         "Refugees in Bangladesh hail it — and want to go home."),
        ("Air taxi flies with no pilot aboard",
         "Japan's self-flying taxi carries its first passengers."),
    ],
    "AMERICAS": [
        ("Hegseth memo curbs Canada defence ties",
         "A secret Pentagon memo restricts Canada defence ties."),
        ("ICE training a 'catastrophic failure'",
         "Watchdogs find a cascade of problems in ICE training."),
        ("FBI probes crime-database breach",
         "A possible hack of the crime data repository is probed."),
        ("Trump: report Congress's requests",
         "Contractors ordered to flag requests from Congress."),
        ("US open to a Latin American UN chief",
         "Waltz signals flexibility amid the gridlocked race."),
        ("Bukele seeks a third term",
         "He eyes re-election while fighting gangs in Haiti."),
    ],
    "INDONESIA": [
        ("Six bodies recovered at Cikande",
         "Rescuers comb the ruins; 36 still sought (provisional)."),
        ("Fire out at dawn; DVI teams move in",
         "After 16 hours the blaze is out; forensics move in."),
        ("BMKG siaga: rain alert, 8 provinces",
         "Cyclone seed 96S drives it, Aceh to Papua Selatan."),
    ],
    "BUSINESS & TECH": [
        ("Bitcoin holds above $60,000",
         "It holds its Sunday level amid the AI sell-off."),
        ("Brent crude settles at $89.95",
         "A Hormuz risk premium builds in Sunday's snapshot."),
        ("EU and Canada team up on AI",
         "Brussels and Ottawa plan deeper AI collaboration."),
        ("Wildberries chief exits post-sanctions",
         "The CEO leaves days after EU sanctions were imposed."),
    ],
}

SPORT = [
    ("VERSTAPPEN WINS VEGAS BY 0.639s",
     "From pole: a 75th career win, a third on the Strip, after 35 lead changes."),
    ("Piastri, from 17th to the podium",
     "The McLaren man storms through the field to third, 1.529s off the win."),
    ("Antonelli 402, Verstappen 304",
     "The champion's cushion is 98 points; the fight for second rolls to Qatar."),
    ("Turin tonight: Zverev v Alcaraz",
     "The year-end No. 1 meets the unbeaten indoor king for the ATP Finals crown."),
]

BRIEFS = [
    "Nigeria: at least 24 dead as a funeral boat capsizes.",
    "Paolo Bulgari, who took the family jewellers global, dies at 89.",
    "Phumzile Mlambo-Ngcuka, former UN Women chief, dies at 71.",
]

NUMBERS = [
    ("98.79%", "Hong Kong's record EC turnout"),
    ("0.639s", "Verstappen's winning margin"),
    ("35", "lead changes on the Strip"),
    ("200", "nations, and no deal"),
    ("$60,000", "Bitcoin's Sunday line"),
    ("36", "workers still sought"),
]


# ---------------------------------------------------------------- engine
_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def tw(text, f):
    return _probe.textlength(text, font=f)


def fit(text, path, size, max_w, min_size=9):
    size = int(size)
    while size > min_size and tw(text, font(path, size)) > max_w:
        size -= 1
    return font(path, size), size


def wrap(text, f, max_w):
    lines, cur = [], ""
    for wd in text.split():
        trial = wd if not cur else cur + " " + wd
        if tw(trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    report = []

    # Masthead corner: a red sun disc cut by a hard diagonal shadow.
    # Graphic only — every text element is kept clear of it.
    d.ellipse([868, 16, 952, 100], fill=RED)
    d.polygon([(838, 0), (1024, 0), (1024, 172), (928, 28)], fill=INK)

    # Dateline row.
    f_date = font(SANS_B, 13)
    d.text((MARGIN, 26), "SUNDAY · 22 NOVEMBER 2026", font=f_date, fill=INK)
    right_txt = "THE FULL-DAY EDITION"
    d.text((836 - tw(right_txt, f_date), 26), right_txt, font=f_date, fill=INK)
    d.rectangle([MARGIN, 50, RIGHT, 53], fill=INK)

    # Masthead.
    f_mast, mast_size = fit("SUNDAY, IN FULL", SERIF_B, 92, 800)
    d.text((MARGIN - 2, 56), "SUNDAY, IN FULL", font=f_mast, fill=INK)
    y = 56 + mast_size + 4

    # Red kicker strip between rules.
    d.rectangle([MARGIN, y, RIGHT, y + 2], fill=RED)
    kick = ("42 STORIES · EVERY ITEM DATED SUNDAY 22 NOVEMBER 2026 · "
            "ANTALYA — LAS VEGAS — TURIN — HONG KONG")
    f_k, _ = fit(kick, SANS_B, 13, CONTENT_W)
    d.text((MARGIN, y + 7), kick, font=f_k, fill=RED)
    y += 26
    d.rectangle([MARGIN, y, RIGHT, y + 1], fill=INK)
    y += 10

    # Hero: the COP31 collapse.
    d.text((MARGIN, y), HERO_KICKER, font=font(SANS_B, 14), fill=RED)
    y += 19
    f_hh, hh_size = fit(HERO_HEAD, SERIF_B, 64, CONTENT_W)
    d.text((MARGIN - 1, y), HERO_HEAD, font=f_hh, fill=INK)
    y += hh_size + 5
    f_deck = font(SERIF_R, 17)
    for ln in wrap(HERO_DECK, f_deck, CONTENT_W):
        d.text((MARGIN, y), ln, font=f_deck, fill=SOFT)
        y += 22
    y += 6
    col_w = (CONTENT_W - 2 * 22) // 3
    side_bottom = y
    for i, (hd, st) in enumerate(HERO_SIDE):
        x = MARGIN + i * (col_w + 22)
        d.rectangle([x, y, x + 26, y + 4], fill=RED)
        f_sh, _ = fit(hd, SANS_B, 14, col_w)
        d.text((x, y + 9), hd, font=f_sh, fill=INK)
        yy = y + 29
        f_ss = font(SANS_R, 12)
        for ln in wrap(st, f_ss, col_w)[:2]:
            d.text((x, yy), ln, font=f_ss, fill=SOFT)
            yy += 16
        side_bottom = max(side_bottom, yy)
    y = side_bottom + 6
    d.rectangle([MARGIN, y, RIGHT, y + 2], fill=INK)
    y += 10
    report.append(("hero_bottom", round(y, 1)))

    # Main grid: three columns, two sections each.
    columns = [
        [("MIDDLE EAST", SECTIONS["MIDDLE EAST"]),
         ("INDONESIA", SECTIONS["INDONESIA"])],
        [("EUROPE", SECTIONS["EUROPE"]),
         ("BUSINESS & TECH", SECTIONS["BUSINESS & TECH"])],
        [("AMERICAS", SECTIONS["AMERICAS"]),
         ("ASIA-PACIFIC", SECTIONS["ASIA-PACIFIC"])],
    ]
    col_w = 302
    col_x = [MARGIN, MARGIN + col_w + 23, MARGIN + 2 * (col_w + 23)]
    grid_top = y
    grid_bottom = y
    for ci, secs in enumerate(columns):
        x = col_x[ci]
        yy = grid_top
        for name, items in secs:
            d.rectangle([x, yy, x + col_w, yy + 20], fill=BAR)
            d.rectangle([x, yy, x + 6, yy + 20], fill=RED)
            d.text((x + 13, yy + 3), name, font=font(SANS_B, 12), fill=PAPER)
            yy += 26
            for hd, st in items:
                f_ih, _ = fit(hd, SANS_B, 13, col_w)
                d.text((x, yy), hd, font=f_ih, fill=INK)
                yy += 15.5
                f_is = font(SANS_R, 11)
                lines = wrap(st, f_is, col_w)
                if len(lines) > 2:
                    raise ValueError(f"standfirst too long: {st!r}")
                for ln in lines:
                    d.text((x, yy), ln, font=f_is, fill=SOFT)
                    yy += 12.5
                yy += 4.0
            yy += 4
        grid_bottom = max(grid_bottom, yy)
        report.append((f"col{ci}_bottom", round(yy, 1)))
    y = grid_bottom + 4

    # Briefs ticker.
    d.rectangle([MARGIN, y, RIGHT, y + 1], fill=FAINT)
    y += 7
    f_t = font(SANS_R, 11)
    for ln in wrap("  ///  ".join(BRIEFS), f_t, CONTENT_W)[:2]:
        d.text((MARGIN, y), ln, font=f_t, fill=INK)
        y += 14
    y += 4
    report.append(("ticker_bottom", round(y, 1)))

    # Sport band.
    d.rectangle([MARGIN, y, RIGHT, y + 21], fill=BAR)
    d.rectangle([MARGIN, y, MARGIN + 6, y + 21], fill=RED)
    d.text((MARGIN + 13, y + 4), "SPORT — THE DAY IN PLAY",
           font=font(SANS_B, 12), fill=PAPER)
    y += 27
    sw = (CONTENT_W - 3 * 16) // 4
    sport_bottom = y
    for i, (hd, st) in enumerate(SPORT):
        x = MARGIN + i * (sw + 16)
        f_sh2, _ = fit(hd, SANS_B, 12, sw)
        d.text((x, y), hd, font=f_sh2, fill=INK)
        yy = y + 16
        f_ss2 = font(SANS_R, 10)
        for ln in wrap(st, f_ss2, sw)[:2]:
            d.text((x, yy), ln, font=f_ss2, fill=SOFT)
            yy += 13
        sport_bottom = max(sport_bottom, yy)
    y = sport_bottom + 8
    report.append(("sport_bottom", round(y, 1)))

    # Day in Numbers panel on sand, red top edge.
    d.rectangle([MARGIN, y, RIGHT, y + 3], fill=RED)
    d.rectangle([MARGIN, y + 3, RIGHT, y + 56], fill=SAND)
    nw = CONTENT_W // 6
    for i, (val, lab) in enumerate(NUMBERS):
        x = MARGIN + i * nw + 10
        f_v, _ = fit(val, SERIF_B, 20, nw - 16)
        d.text((x, y + 9), val, font=f_v, fill=INK)
        f_l = font(SANS_R, 9)
        yy = y + 33
        for ln in wrap(lab, f_l, nw - 16)[:2]:
            d.text((x, yy), ln, font=f_l, fill=SOFT)
            yy += 11
    y += 56
    report.append(("numbers_bottom", round(y, 1)))

    # Source line.
    y += 6
    src = ("Sources: Reuters · UNFCCC plenary reports · info.gov.hk · BMKG · "
           "FIA documents · ATP · wire reports — all dated 22 Nov 2026")
    f_src, _ = fit(src, SANS_R, 9, CONTENT_W)
    d.text((MARGIN, y), src, font=f_src, fill=FAINT)
    y += 13
    report.append(("final_bottom", round(y, 1)))
    if y > H - 8:
        raise ValueError(f"page overflow: final bottom {y}")

    img.save(path)
    return report


# ---------------------------------------------------------------- entrypoint
def output_path():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        out_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(out_dir, "entry.png")


def main():
    out = output_path()
    report = build(out)
    with Image.open(out) as im:
        assert im.size == (1024, 1024), f"unexpected size {im.size}"
        assert im.format == "PNG", f"unexpected format {im.format}"
    size = os.path.getsize(out)
    print(f"entry.png written: {size} bytes, 1024x1024 -> {out}")
    for name, bottom in report:
        print(f"  {name}: {bottom}")
    return out


if __name__ == "__main__":
    main()
