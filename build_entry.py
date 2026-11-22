#!/usr/bin/env python3
"""Build the entry image for make.fun news-image-20261122.

Composites one 1024x1024 PNG summing up the world news of Sunday
22 November 2026. Three AI-generated scene photos (no text baked in)
are combined with text drawn entirely by PIL in Liberation Sans.

Visual identity follows the user's Brief #2 ("Sunlit Crime-Noir"):
warm sand paper, charcoal-black masthead, vivid red accent, hard
diagonal shadow slashes, condensed-feel bold display type.

Deterministic: no randomness, no clock, no network. Running this
script twice produces a byte-identical entry.png.

Usage:  python3 build_entry.py
Output: entry.png  (1024x1024, under 1 MiB)
"""

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

W, H = 1024, 1024

# --- Palette (Brief #2: Sunlit Crime-Noir) ---
PAPER = (246, 239, 224)      # warm sand / sunlit cream
PAPER_DARK = (232, 220, 194)  # deeper sand for strip
INK = (23, 19, 14)           # charcoal black
RED = (200, 16, 46)          # vivid red accent
RED_DARK = (143, 10, 30)
AMBER = (255, 199, 95)       # warm highlight on dark bands
CREAM = (255, 253, 247)
GREY = (107, 98, 87)         # warm grey for captions
RULE = (214, 199, 166)       # sand rule lines

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_width):
    """Greedy word wrap returning a list of lines that fit max_width."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if draw.textlength(trial, font=fnt) <= max_width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_width, fill, leading=None):
    """Draw wrapped text; return the y just below the last line."""
    if leading is None:
        leading = fnt.size + 4
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def fit_text(draw, text, fnt, max_width):
    """Shrink font size until text fits max_width; return (font, width)."""
    size = fnt.size
    while size > 8 and draw.textlength(text, font=fnt) > max_width:
        size -= 1
        fnt = ImageFont.truetype(
            os.path.join(FONT_DIR, "LiberationSans-Bold.ttf"), size)
    return fnt, draw.textlength(text, font=fnt)


def fit_photo(path, size):
    """Centre-crop a photo to exactly `size` (deterministic)."""
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, size, method=Image.LANCZOS, centering=(0.5, 0.5))


# ----------------------------------------------------------------------
# News data: 32 distinct dated stories, all 22 November 2026.
# Lead (1) + photo cards (2) + grid (27) + strip (2).
# Sources are listed in README.md.
# ----------------------------------------------------------------------
TICKER = ("LVIV: 5 KILLED IN OVERNIGHT BARRAGE  •  COP31: REVISED TEXT "
          "TABLED  •  FBI PROBES CRIME-DATABASE HACK  •  HONG KONG POLLS OPEN")

GRID_ITEMS = [
    ("HONG KONG", "Polls open for the Election Committee; 856 candidates "
     "contest 723 seats."),
    ("NEPAL", "PM Shah lands in New Delhi for his first visit; talks with "
     "Modi on Monday."),
    ("AUKUS", "Marles hits back at a US report saying the pact cuts US "
     "submarine numbers."),
    ("GAZA AID", "Four nations urge Israel to open aid access as floods "
     "worsen Gaza's crisis."),
    ("VENEZUELA", "US report: oil and mineral revenue above $12bn, a year "
     "after Maduro's capture."),
    ("ISRAEL", "Eisenkot invites Likud to talks resuming Sunday; mandate "
     "ends 6 Dec."),
    ("GULF", "Saudi coalition says it downed a Houthi missile and a drone "
     "bound for Riyadh."),
    ("F1", "Las Vegas GP under the lights tonight; Verstappen on pole, "
     "Russell alongside."),
    ("ASHES", "Day two in Perth; Smith captains Australia with Cummins out "
     "injured."),
    ("NFL", "Broncos host the Raiders; rookie QB Mendoza faces Denver's "
     "pass rush."),
    ("CRICKET", "India face New Zealand in windy Wellington."),
    ("IRAN WEB", "Draft rules tie online accounts to real identities, "
     "ending anonymous use."),
    ("COP31 AI", "The summit's AI pledge fails to attract major US tech "
     "firms."),
    ("QESHM", "Iran says island blasts were US munitions disposal, not a "
     "fresh attack."),
    ("OMAN", "Tankers hit off the coast as Iran-US naval tensions escalate."),
    ("SCO", "Modi hails civilisational links as dialogue opens; Pakistan "
     "to attend."),
    ("FRANCE", "Prosecutors probe Depardieu and an author over a gang-rape "
     "claim."),
    ("SNOOKER", "Advani and Ramachandran win their openers at the world "
     "championship."),
    ("IFFI", "Goa film festival adds an animation section with five films."),
    ("HORMUZ", "ADNOC vessel attacked; one crew member reported missing."),
    ("CHIPS", "Bessent: no new curbs needed on Nvidia exports to China."),
    ("GAZA", "129 more bodies pulled from the rubble in central Gaza."),
    ("SOMALIA", "Satellite images show the UAE expanding airstrips."),
    ("CLIMATE TECH", "EU's Copernicus showcases AI's role in tracking the "
     "atmosphere."),
    ("VICTORIA", "Early voting closed Sunday; state votes 28 Nov; Coalition "
     "leads 56-44."),
    ("AUSTRALIA", "South-east heat and storms; Melbourne 31°C, Sydney 31°C."),
    ("NEW YORK", "'Turtle Lady' Lorri Cramer has taken in 680 baby turtles."),
]

STRIP_LINES = [
    ("ALSO: ", "Panama vows to block any COP31 deal without fossil-fuel "
     "language  •  AAA expects 81.5m Americans to travel 24-30 Nov"),
    ("BY THE NUMBERS: ", "550 munitions  •  496 drones  •  723 seats  •  "
     "$12bn  •  856 candidates  •  129 bodies  •  34-member delegation"),
]


def draw_grid_item(draw, x, y, kicker, body, col_w, fnt_bold, fnt_reg):
    """Draw one grid item: red bold kicker inline, then regular body.

    Returns the number of lines used (must be <= 2).
    """
    prefix = kicker + " — "
    prefix_w = draw.textlength(prefix, font=fnt_bold)
    # Line 1: prefix + as many body words as fit after it.
    words = body.split()
    line1 = ""
    i = 0
    while i < len(words):
        trial = (line1 + " " + words[i]).strip()
        if draw.textlength(trial, font=fnt_reg) <= col_w - prefix_w:
            line1 = trial
            i += 1
        else:
            break
    rest = " ".join(words[i:])
    lines2 = wrap(draw, rest, fnt_reg, col_w) if rest else []
    # Draw line 1 in two segments.
    draw.text((x, y), prefix, font=fnt_bold, fill=RED_DARK)
    draw.text((x + prefix_w, y), line1, font=fnt_reg, fill=INK)
    yy = y + fnt_reg.size + 4
    for line in lines2:
        draw.text((x, yy), line, font=fnt_reg, fill=INK)
        yy += fnt_reg.size + 4
    return 1 + len(lines2)


def build():
    canvas = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(canvas)

    # ------------------------------------------------------------------
    # Masthead: charcoal band, cream title, red diagonal slash (Brief #2)
    # ------------------------------------------------------------------
    d.rectangle([0, 0, W, 92], fill=INK)
    # Hard diagonal shadow slash: a slanted red divider between the
    # title block and the date block (Brief #2 hook).
    d.polygon([(648, 10), (664, 10), (652, 82), (636, 82)], fill=RED)
    title_fnt, _ = fit_text(d, "SUNDAY, IN FULL",
                            font("LiberationSans-Bold.ttf", 56), 640)
    d.text((24, 12), "SUNDAY, IN FULL", font=title_fnt, fill=CREAM)
    d.text((24, 70), "THE WORLD IN ONE IMAGE",
           font=font("LiberationSans-Bold.ttf", 15), fill=(196, 188, 172))
    d.text((700, 10), "SUNDAY", font=font("LiberationSans-Bold.ttf", 24),
           fill=CREAM)
    d.text((700, 40), "22 NOVEMBER 2026",
           font=font("LiberationSans-Bold.ttf", 19), fill=AMBER)
    d.text((700, 66), "32 DATED STORIES  •  6 REGIONS",
           font=font("LiberationSans-Bold.ttf", 13), fill=(196, 188, 172))
    d.rectangle([0, 92, W, 96], fill=RED)

    # ------------------------------------------------------------------
    # Ticker strip
    # ------------------------------------------------------------------
    d.rectangle([0, 98, W, 120], fill=INK)
    tick_fnt, _ = fit_text(d, TICKER, font("LiberationSans-Bold.ttf", 15),
                           W - 28)
    d.text((14, 103), TICKER, font=tick_fnt, fill=AMBER)

    # ------------------------------------------------------------------
    # Lead story: Russia's overnight barrage (Lviv photo, dawn)
    # ------------------------------------------------------------------
    lead_y = 128
    photo = fit_photo(
        os.path.join(ASSETS, "media-generation-lviv-dawn-strike-0-543a3a0c-7105-40b3-812e-411fb98e62f1.webp"),
        (600, 228))
    canvas.paste(photo, (24, lead_y))
    d.rectangle([24, lead_y, 624, lead_y + 228], outline=INK, width=2)
    # Red top edge on the photo: the Brief #2 accent.
    d.rectangle([24, lead_y, 624, lead_y + 5], fill=RED)
    d.text((24, lead_y + 234),
           "A damaged apartment block in Lviv at dawn.  Illustration: AI-generated scene.",
           font=font("LiberationSans-Italic.ttf", 12), fill=GREY)

    px, pw = 648, 352
    d.text((px, lead_y), "WAR IN EUROPE",
           font=font("LiberationSans-Bold.ttf", 17), fill=RED)
    d.line([(px, lead_y + 24), (px + pw, lead_y + 24)], fill=RED, width=2)
    y = draw_wrapped(d, px, lead_y + 32,
                     "RUSSIA'S NEW\nOVERNIGHT BARRAGE",
                     font("LiberationSans-Bold.ttf", 30), pw, INK, leading=33)
    y = draw_wrapped(d, px, y + 8,
                     "550 munitions — 496 drones, 53 missiles — rain down "
                     "overnight; 5 killed, 10 injured.",
                     font("LiberationSans-Bold.ttf", 16), pw, INK, leading=20)
    y = draw_wrapped(d, px, y + 6,
                     "A family of four dies in Lapaivka, near Lviv; one killed, "
                     "10 hurt in Zaporizhzhia.",
                     font("LiberationSans-Regular.ttf", 15), pw, INK, leading=19)
    y = draw_wrapped(d, px, y + 6,
                     "Air defences down 439 drones and 39 missiles; Russia "
                     "says it downed 62 Ukrainian drones.",
                     font("LiberationSans-Regular.ttf", 15), pw, INK, leading=19)

    # ------------------------------------------------------------------
    # Second row: two photo cards (COP31 / FBI)
    # ------------------------------------------------------------------
    row_y = 376
    card_w, card_h = 488, 126

    # --- COP31 card (left)
    cop = fit_photo(
        os.path.join(ASSETS, "media-generation-cop31-antalya-hall-0-3d974eb3-5cfb-4f9a-b064-63dad4043d89.webp"),
        (card_w, card_h))
    canvas.paste(cop, (24, row_y))
    d.rectangle([24, row_y, 24 + card_w, row_y + card_h], outline=INK, width=2)
    d.rectangle([24, row_y, 24 + card_w, row_y + 5], fill=RED)
    y = row_y + card_h + 8
    d.text((24, y), "CLIMATE  —  COP31, ANTALYA",
           font=font("LiberationSans-Bold.ttf", 16), fill=RED)
    y = draw_wrapped(d, 24, y + 22,
                     "REVISED TEXT TABLED AS GAP NARROWS",
                     font("LiberationSans-Bold.ttf", 17), 472, INK, leading=20)
    draw_wrapped(d, 24, y + 2,
                 "New draft sent to delegations; plenary 10:00. Fossil fuels "
                 "stay in; 1.5°C conceded as missed.",
                 font("LiberationSans-Regular.ttf", 14), 472, INK, leading=18)

    # --- FBI card (right)
    fbi = fit_photo(
        os.path.join(ASSETS, "media-generation-fbi-office-sunlit-0-6f182ca9-4ebd-4d44-8511-3e9adddc9c75.webp"),
        (card_w, card_h))
    canvas.paste(fbi, (512, row_y))
    d.rectangle([512, row_y, 512 + card_w, row_y + card_h], outline=INK, width=2)
    d.rectangle([512, row_y, 512 + card_w, row_y + 5], fill=RED)
    y = row_y + card_h + 8
    d.text((512, y), "CYBER  —  WASHINGTON",
           font=font("LiberationSans-Bold.ttf", 16), fill=RED)
    y = draw_wrapped(d, 512, y + 22,
                     "FBI PROBES HACK OF ITS CRIME DATABASE",
                     font("LiberationSans-Bold.ttf", 17), 472, INK, leading=20)
    draw_wrapped(d, 512, y + 2,
                 "The NCIC system, used by federal and local police to share "
                 "records, is under investigation after an apparent breach.",
                 font("LiberationSans-Regular.ttf", 14), 472, INK, leading=18)

    # ------------------------------------------------------------------
    # "Also today" grid: 27 items, three columns x nine rows
    # ------------------------------------------------------------------
    grid_y = 608
    d.rectangle([0, grid_y, W, grid_y + 26], fill=INK)
    d.rectangle([24, grid_y + 7, 38, grid_y + 19], fill=RED)
    d.text((46, grid_y + 4), "ALSO TODAY  —  SUNDAY 22 NOVEMBER 2026",
           font=font("LiberationSans-Bold.ttf", 16), fill=CREAM)

    fnt_bold = font("LiberationSans-Bold.ttf", 13)
    fnt_reg = font("LiberationSans-Regular.ttf", 13)
    col_w = 304
    col_x = [24, 360, 696]
    row_h = 36
    overflow = []
    for i, (kicker, body) in enumerate(GRID_ITEMS):
        cx = col_x[i % 3]
        cy = grid_y + 36 + (i // 3) * row_h
        n = draw_grid_item(d, cx, cy, kicker, body, col_w, fnt_bold, fnt_reg)
        if n > 2:
            overflow.append((kicker, n))
    if overflow:
        print("WARNING: grid items over 2 lines:", overflow)

    # ------------------------------------------------------------------
    # Strip + footer
    # ------------------------------------------------------------------
    strip_y = 978
    d.rectangle([0, strip_y, W, strip_y + 30], fill=PAPER_DARK)
    sy = strip_y + 3
    for prefix, text in STRIP_LINES:
        f_b = font("LiberationSans-Bold.ttf", 12)
        f_r = font("LiberationSans-Regular.ttf", 12)
        d.text((24, sy), prefix, font=f_b, fill=RED_DARK)
        d.text((24 + d.textlength(prefix, font=f_b), sy), text,
               font=f_r, fill=INK)
        sy += 14
    d.text((24, 1010),
           "All events 22 November 2026. Sources: Reuters, BBC, AP, QNA, IANS, "
           "The Hindu, Digiato, Copernicus. Photos: AI-generated scenes.",
           font=font("LiberationSans-Regular.ttf", 11), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    canvas.save(out, format="PNG", optimize=True)
    return out


if __name__ == "__main__":
    path = build()
    img = Image.open(path)
    print(f"{path}: {img.size[0]}x{img.size[1]}, {os.path.getsize(path)} bytes")
