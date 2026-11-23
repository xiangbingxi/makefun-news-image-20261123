#!/usr/bin/env python3
"""Draw the 23 November 2026 one-day world news page (1024x1024).

Flat hand-drawn vector style with PIL only: no photos, no network images.
Writes entry.png into the repo root (fixed path; OUT_PATH env overrides).

Revision (23 Nov evening, after user review):
- No top numbers strip and no DATE CHECK box: both duplicated story
  content and crowded the thumbnail. Space goes to bigger headlines,
  bigger story cards, a taller map and bigger briefs type.
- COP31 is written as a Monday follow-up (talks ended Sun 22 Nov).
- Marquez is flagged in its title as a Sun 22 Nov result.
- Democrats figure is "at least 258" everywhere (AP).
- Footer no longer claims every story happened on 23 Nov.
- Map: added Japan, Indonesia, Greenland, New Zealand, Central America;
  all land is clipped to the frame (lat 75 to -55).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
# Fixed output inside the repo; never derived from the script's location.
OUT = os.environ.get(
    "OUT_PATH",
    "/home/hatch/workspace/makefun/news-image-20261123/repo/entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
F_B = os.path.join(FD, "DejaVuSans-Bold.ttf")
F_R = os.path.join(FD, "DejaVuSans.ttf")

PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (18, 40, 75)
RED = (193, 39, 45)
TEAL = (14, 124, 123)
SEA = (214, 231, 240)
LAND = (196, 209, 176)
LAND_EDGE = (140, 160, 120)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
SOFT = (238, 234, 222)
LINE = (200, 196, 180)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, lines, fnt, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 3
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def halo_text(draw, xy, s, fnt, fill=INK):
    x, y = xy
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        draw.text((x + dx, y + dy), s, font=fnt, fill=(255, 255, 255))
    draw.text((x, y), s, font=fnt, fill=fill)


# ---------------- data ----------------
BIG = [
    ("1", "COP31 COLLAPSES — NO DEAL", "ANTALYA — MONDAY FOLLOW-UP", RED,
     "Talks ended Sun 22 Nov with no deal; Monday's wires led with the "
     "fallout, as the EU and ~130 parties rejected a text that never "
     "mentions fossil fuels. Longest COP ever."),
    ("2", "24 DEAD IN JAVA FACTORY FIRE", "BANTEN, INDONESIA", (200, 90, 20),
     "Indonesia confirms 24 dead, ~30 still missing after fire tore through "
     "a candy factory near Jakarta. About 300 workers were on shift."),
    ("3", "AI SELL-OFF RATTLES MARKETS", "TOKYO / NEW YORK", TEAL,
     "Fears the AI boom is overpriced sink stocks: Nikkei -5.06%, Hong Kong "
     "to a 19-month low, S&P 500 -3.7% last week."),
]

SMALL = [
    ("4", "BOY, 7, PULLED ALIVE IN DYMER", "Russian drone hits a Kyiv block; 11 dead."),
    ("5", "UKRAINE SINKS WARSHIP OFF LIBYA", "7 sea drones sink the corvette Merkury."),
    ("6", "DEMOCRATS SECURE AT LEAST 258 HOUSE SEATS", "Largest House majority since 1992."),
    ("7", "TANKERS ABLAZE NEAR HORMUZ", "Two supertankers hit mines; Bahrain hit."),
    ("8", "24 CIVILIANS KILLED IN S. SUDAN", "Overnight raid kills 7 children in Warrap."),
    ("9", "5 CHILDREN KILLED IN KHARTOUM", "Strikes hit homes and a UN building."),
    ("10", "GAZA A 'TOXIC WASTELAND'", "99% of Gaza at risk: Oxfam."),
    ("11", "BELGIUM'S AIRPORTS SHUT DOWN", "Strike cancels nearly all flights."),
    ("12", "DELTA OUTAGE DELAYS 1,600 FLIGHTS", "System failure; Thanksgiving travel."),
    ("13", "MARQUEZ SEALS 8TH TITLE (SUN 22 NOV)", "Equals Agostini with 8th in Portugal."),
]

BRIEFS = [
    ("14", "IOWA BLAST GOES AHEAD DESPITE COURT", "Army to detonate 68 barrels of lead azide by Tue."),
    ("15", "NEPAL PM MEETS MODI IN DELHI", "Balen Shah's first bilateral trip abroad as PM."),
    ("16", "HASINA TO BE JAILED IF SHE RETURNS", "Dhaka vows arrest if ex-PM comes home in Dec."),
    ("17", "VIETNAM STARTS RARE-EARTH PLANT", "High-purity materials plant starts in Haiphong."),
    ("18", "INDIA HOLDS 3RD IN ASIA POWER INDEX", "Scores 40.5 in the Lowy Institute's 2026 index."),
    ("19", "INDONESIA SEIZES CHEMICAL SHIP", "405t of sodium perchlorate bound for Bangladesh."),
    ("20", "IRAN SAYS IT DOWNED A US MQ-9 DRONE", "Tehran claims 58th US drone destroyed over Hormuz."),
    ("21", "HOUTHIS CLAIM REFINERY STRIKE", "Saudi strike on Hodeida kills 4, injures 18."),
    ("22", "GULF BOURSES RISE ON DIPLOMACY", "Saudi, Qatar and Dubai markets open higher."),
    ("23", "EBOLA FIGHT DISRUPTED IN DR CONGO", "Fighting in Ituri halts response; WHO appeals."),
    ("24", "FIVE EU STATES BACK RWANDA CENTRES", "Deportation centres for rejected asylum seekers."),
    ("25", "FRANCE'S DOWNTURN DEEPENS", "Flash PMI 46.2, a six-month low; euro zone 51.7."),
    ("26", "THOUSANDS RALLY IN ISTANBUL", "Protest over state takeover of Sozcu TV."),
    ("27", "BOLSONARO IN INTENSIVE CARE", "Ex-president stable with intestinal obstruction."),
    ("28", "BEIJING WELCOMES HONG KONG VOTE", "China hails 'patriots only' election results."),
    ("29", "TATA STEEL BUYS $1.67BN STAKE", "Buys into India's top steel pipe maker."),
    ("30", "HEDGE FUNDS' WORST WEEK SINCE APR 2025", "Lost 3%+ in the tech-led sell-off: JPMorgan."),
    ("31", "WALL STREET FUTURES BOUNCE", "Dow e-minis up 1.58% after last week's rout."),
    ("32", "FDA DRUG MAY CURE HIGH BLOOD PRESSURE", "Drug shows promise for hormone-driven cases."),
    ("33", "FEDEX HIJACK HERO DIES AT 82", "Capt. David Sanders beat the 1994 hijack bid."),
    ("34", "GEORGIA, UTAH, NOTRE DAME STAY 1-2-3", "AP Top 25 holds top three; Big Ten out of top 5."),
    ("35", "RUSSIAN OIL EXPORTS CURBED", "Storms and drone attacks delay tanker loadings."),
    ("36", "DENMARK ACCUSES RUSSIA OF MURDER PLOT", "Moscow 'plotted to kill a US rapper'."),
]

REGIONS = [("Europe", 9, (70, 110, 170)), ("North America", 7, (14, 124, 123)),
           ("Asia", 8, (198, 138, 20)), ("Middle East", 5, (193, 39, 45)),
           ("Africa", 4, (120, 90, 40)), ("South America", 1, (40, 140, 60)),
           ("Global", 2, (110, 110, 110))]

# Simplified coastlines, lon/lat. Small island groups are drawn slightly
# larger than true scale so pins sit visibly on land at this size.
CONTINENTS = [
    # North America
    [(-168, 66), (-155, 71), (-140, 70), (-128, 71), (-120, 72), (-110, 68),
     (-100, 69), (-90, 69), (-85, 66), (-80, 62), (-76, 62), (-70, 58),
     (-65, 60), (-60, 55), (-55, 52), (-60, 47), (-65, 45), (-70, 42),
     (-75, 38), (-76, 35), (-80, 32), (-81, 26), (-84, 30), (-90, 29),
     (-95, 29), (-97, 26), (-100, 22), (-105, 20), (-110, 23), (-115, 28),
     (-120, 34), (-125, 40), (-124, 48), (-130, 55), (-140, 60), (-155, 58),
     (-165, 60), (-168, 66)],
    # Central America (land bridge)
    [(-105, 21), (-100, 19), (-95, 17), (-91, 15), (-87, 14), (-84, 12),
     (-81, 10), (-79, 8), (-80, 9), (-82, 11), (-85, 12), (-88, 14),
     (-91, 15), (-95, 16), (-99, 18), (-103, 20), (-105, 21)],
    # South America
    [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-55, 6), (-52, 4),
     (-50, 0), (-45, -3), (-38, -5), (-35, -8), (-40, -15), (-42, -22),
     (-48, -28), (-55, -35), (-60, -38), (-65, -40), (-68, -50),
     (-70, -54), (-73, -50), (-73, -40), (-72, -30), (-70, -20),
     (-75, -15), (-80, -8), (-81, -3), (-80, 5), (-80, 10)],
    # Africa
    [(-17, 15), (-15, 27), (-10, 31), (-5, 35), (0, 36), (10, 37),
     (15, 32.6), (20, 32.6), (25, 32), (30, 31.5), (33, 27), (35, 28),
     (38, 22), (40, 18), (43, 12), (48, 11), (51, 10), (46, 5),
     (42, 0), (40, -5), (38, -10), (35, -18), (32, -25), (28, -32),
     (20, -35), (16, -30), (13, -20), (12, -10), (10, -2), (8, 4),
     (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12), (-17, 15)],
    # Europe
    [(-10, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 50),
     (0, 51), (3, 53), (5, 55), (8, 57), (10, 59), (12, 56), (18, 56),
     (21, 55), (24, 58), (21, 60), (18, 62), (12, 64), (8, 66),
     (12, 68), (18, 70), (25, 71), (30, 70), (35, 67), (40, 66),
     (42, 64), (40, 60), (38, 55), (35, 52), (30, 50), (28, 46),
     (25, 44), (23, 40), (20, 40), (18, 42), (15, 44), (12, 44),
     (8, 44), (3, 43), (0, 39), (-2, 37), (-6, 36), (-10, 37)],
    # Asia
    [(40, 66), (45, 68), (55, 69), (65, 69), (75, 72), (85, 73),
     (95, 76), (105, 77), (115, 76), (125, 72), (135, 72), (145, 70),
     (155, 68), (160, 62), (158, 55), (150, 60), (142, 55), (140, 50),
     (135, 45), (130, 42), (127, 40), (122, 38), (120, 32), (118, 25),
     (112, 22), (108, 18), (105, 10), (103, 8), (100, 6), (98, 10),
     (95, 15), (92, 20), (90, 22), (86, 20), (82, 16), (80, 13),
     (77, 8), (75, 12), (72, 18), (68, 22), (65, 25), (60, 25),
     (57, 26), (55, 28), (52, 28), (50, 30), (48, 30), (45, 30),
     (42, 28), (40, 30), (38, 35), (40, 40), (42, 45), (42, 50),
     (40, 55), (40, 60), (40, 66)],
    # Turkey + Levant coast (Antalya and Gaza pins sit on land)
    [(26, 39), (28, 41), (32, 42), (36, 42), (40, 41), (44, 40),
     (44, 37), (40, 36), (37, 36), (36, 34), (36, 31), (34, 31),
     (34, 35), (33, 36), (30, 36), (27, 37), (26, 39)],
    # Japan (drawn wider than true scale so the Tokyo pin sits visibly
    # on land instead of on a hairline chain)
    [(132, 31), (134, 32), (136, 34), (138, 34), (140, 35), (144, 35),
     (146, 36), (146, 39), (145, 41), (146, 43), (147, 44), (145, 45),
     (143, 45), (141, 43), (140, 41), (138, 39), (136, 37), (134, 35),
     (132, 33), (131, 32), (132, 31)],
    # Sumatra
    [(94, 6), (97, 4), (100, 1), (102, -2), (104, -4), (106, -6),
     (104, -6), (102, -3), (100, 0), (97, 3), (94, 5), (94, 6)],
    # Java (Banten pin at 106, -6.2 sits inside; drawn taller than true
    # scale so the island reads at this size)
    [(104, -3.5), (107, -3.5), (110, -4.5), (113, -5), (114, -6),
     (114, -9), (111, -9), (108, -8), (105, -7), (104, -5), (104, -3.5)],
    # Borneo
    [(109, 2), (112, 4), (115, 4), (118, 2), (119, 0), (117, -2),
     (115, -4), (112, -4), (110, -2), (109, 0), (109, 2)],
    # Sulawesi
    [(119, 1), (121, 1), (123, 0), (122, -2), (121, -4), (120, -2),
     (119, 0), (119, 1)],
    # New Guinea (western half)
    [(131, -1), (135, -2), (139, -3), (141, -4), (141, -6), (138, -7),
     (134, -5), (131, -3), (131, -1)],
    # Philippines
    [(120, 18), (122, 18), (124, 15), (123, 12), (122, 9), (121, 7),
     (120, 9), (119, 12), (120, 15), (120, 18)],
    # Taiwan
    [(120, 22), (121, 23), (122, 25), (121, 25), (120, 24), (120, 22)],
    # Greenland (clipped at 75N by the frame)
    [(-55, 60), (-48, 60), (-42, 63), (-35, 66), (-28, 69), (-22, 71),
     (-20, 74), (-25, 75), (-35, 76), (-45, 77), (-55, 78), (-60, 76),
     (-62, 72), (-58, 67), (-55, 60)],
    # New Zealand, North Island
    [(173, -35), (175, -37), (177, -38), (178, -39), (176, -41),
     (174, -41), (173, -38), (172, -36), (173, -35)],
    # New Zealand, South Island
    [(167, -45), (169, -43), (171, -42), (173, -41), (174, -42),
     (172, -44), (170, -46), (168, -46), (167, -44), (167, -45)],
    # Australia
    [(113, -22), (114, -30), (115, -34), (120, -34), (125, -32),
     (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
     (153, -32), (153, -27), (150, -23), (146, -19), (142, -15),
     (142, -11), (137, -12), (135, -15), (132, -12), (130, -13),
     (126, -14), (122, -17), (118, -20), (113, -22)],
]

# (number, lon, lat, label, label offset dx, dy, pin display offset ox, oy)
PINS = [
    ("1", 30.7, 36.9, "ANTALYA", 12, 12, 0, 0),
    ("2", 106.0, -6.2, "BANTEN", -8, 12, 0, 0),
    ("3", 139.7, 35.7, "TOKYO", 12, -4, 0, 0),
    ("4", 30.3, 50.8, "DYMER", -8, -24, 0, 0),
    ("5", 20.0, 32.1, "BENGHAZI", -72, 4, 0, 0),
    ("6", -77.0, 38.9, "WASHINGTON", -150, -4, 0, 0),
    ("7", 56.5, 26.5, "HORMUZ", 12, 4, 0, 0),
    ("8", 28.0, 7.5, "WARRAP", -12, 14, 0, 0),
    ("9", 32.5, 15.6, "KHARTOUM", 12, -2, 0, 0),
    ("10", 34.5, 31.5, "GAZA", 12, -4, 18, -18),
    ("11", 4.4, 50.8, "BRUSSELS", -76, -18, 0, 0),
    ("12", -84.4, 33.7, "ATLANTA", -14, 14, 0, 0),
    ("13", -8.5, 37.1, "PORTIMAO", -82, -4, 0, 0),
]


def clip_polygon(poly, lon_min, lon_max, lat_min, lat_max):
    """Clip a lon/lat polygon to the rectangle (Sutherland-Hodgman)."""

    def clip_edge(pts, inside, intersect):
        if not pts:
            return []
        out = []
        prev = pts[-1]
        prev_in = inside(prev)
        for cur in pts:
            cur_in = inside(cur)
            if cur_in:
                if not prev_in:
                    out.append(intersect(prev, cur))
                out.append(cur)
            elif prev_in:
                out.append(intersect(prev, cur))
            prev, prev_in = cur, cur_in
        return out

    poly = clip_edge(
        poly, lambda p: p[0] >= lon_min,
        lambda a, b: (lon_min, a[1] + (b[1] - a[1]) * (lon_min - a[0]) / (b[0] - a[0])) if b[0] != a[0] else (lon_min, a[1]))
    poly = clip_edge(
        poly, lambda p: p[0] <= lon_max,
        lambda a, b: (lon_max, a[1] + (b[1] - a[1]) * (lon_max - a[0]) / (b[0] - a[0])) if b[0] != a[0] else (lon_max, a[1]))
    poly = clip_edge(
        poly, lambda p: p[1] >= lat_min,
        lambda a, b: (a[0] + (b[0] - a[0]) * (lat_min - a[1]) / (b[1] - a[1]), lat_min) if b[1] != a[1] else (a[0], lat_min))
    poly = clip_edge(
        poly, lambda p: p[1] <= lat_max,
        lambda a, b: (a[0] + (b[0] - a[0]) * (lat_max - a[1]) / (b[1] - a[1]), lat_max) if b[1] != a[1] else (a[0], lat_max))
    return poly


def draw_icon(draw, kind, x, y, s, accent):
    """Small flat glyph inside a s x s box at (x, y)."""
    cx, cy = x + s // 2, y + s // 2
    if kind == "globe":
        draw.ellipse([x + 6, y + 4, x + s - 6, y + s - 4], fill=(70, 130, 180),
                     outline=NAVY, width=2)
        draw.ellipse([x + 16, y + 12, x + 30, y + 22], fill=(90, 170, 90))
        draw.ellipse([x + 26, y + 30, x + 44, y + 42], fill=(90, 170, 90))
        draw.line([x + 8, y + s - 6, x + s - 8, y + 6], fill=RED, width=4)
    elif kind == "fire":
        draw.rectangle([x + 8, y + 26, x + s - 8, y + s - 6], fill=(120, 120, 120))
        draw.rectangle([x + 12, y + 12, x + 18, y + 26], fill=(120, 120, 120))
        draw.polygon([(cx - 12, y + 26), (cx - 4, y + 8), (cx + 2, y + 18),
                      (cx + 8, y + 4), (cx + 14, y + 26)], fill=(230, 110, 20))
        draw.polygon([(cx - 5, y + 26), (cx, y + 16), (cx + 6, y + 26)],
                     fill=(245, 200, 40))
    elif kind == "chart":
        draw.line([(x + 6, y + 12), (x + 18, y + 22), (x + 28, y + 18),
                   (x + 40, y + 34), (x + s - 6, y + 44)], fill=RED, width=4)
        draw.polygon([(x + s - 12, y + 38), (x + s - 2, y + 44), (x + s - 12, y + 48)],
                     fill=RED)
        for i, hgt in enumerate((10, 16, 8, 20)):
            bx = x + 8 + i * 11
            draw.rectangle([bx, y + s - 6 - hgt, bx + 7, y + s - 6],
                           fill=(70, 130, 180))
    elif kind == "building":
        draw.rectangle([x + 10, y + 10, x + s - 10, y + s - 6], fill=(150, 150, 150))
        for r in range(3):
            for c in range(3):
                draw.rectangle([x + 14 + c * 11, y + 14 + r * 12,
                                x + 20 + c * 11, y + 20 + r * 12], fill=(60, 60, 60))
        draw.line([(x + 26, y + 8), (x + 22, y + 20), (x + 30, y + 28),
                   (x + 24, y + 40)], fill=RED, width=3)
    elif kind == "ship":
        draw.polygon([(x + 6, y + 30), (x + s - 6, y + 30), (x + s - 12, y + 42),
                      (x + 12, y + 42)], fill=NAVY)
        draw.rectangle([x + 24, y + 12, x + 28, y + 30], fill=NAVY)
        draw.polygon([(x + 28, y + 14), (x + 42, y + 22), (x + 28, y + 22)],
                     fill=RED)
        draw.arc([x + 4, y + 44, x + s - 4, y + 54], 0, 180, fill=(70, 130, 180),
                 width=3)
    elif kind == "dome":
        draw.pieslice([x + 14, y + 8, x + s - 14, y + 30], 180, 360, fill=NAVY)
        draw.rectangle([x + 8, y + 30, x + s - 8, y + 36], fill=NAVY)
        for i in range(4):
            bx = x + 12 + i * 10
            draw.rectangle([bx, y + 36, bx + 5, y + 46], fill=NAVY)
        draw.rectangle([x + 8, y + 46, x + s - 8, y + 50], fill=NAVY)
    elif kind == "tanker":
        draw.polygon([(x + 4, y + 28), (x + s - 4, y + 28), (x + s - 10, y + 42),
                      (x + 10, y + 42)], fill=(90, 60, 40))
        draw.rectangle([x + 12, y + 16, x + 22, y + 28], fill=(200, 60, 40))
        draw.rectangle([x + 26, y + 16, x + 36, y + 28], fill=(200, 140, 40))
        draw.polygon([(cx - 6, y + 16), (cx, y + 4), (cx + 6, y + 16)],
                     fill=(245, 200, 40))
    elif kind == "people":
        for i, px in enumerate((x + 12, x + 26, x + 38)):
            draw.ellipse([px - 4, y + 10, px + 4, y + 18], fill=INK)
            draw.polygon([(px - 6, y + 40), (px + 6, y + 40), (px + 4, y + 20),
                          (px - 4, y + 20)], fill=RED if i == 1 else INK)
    elif kind == "drone":
        draw.ellipse([x + 18, y + 16, x + 34, y + 28], fill=(90, 90, 90))
        draw.line([(x + 8, y + 12), (x + 18, y + 18)], fill=INK, width=3)
        draw.line([(x + 44, y + 12), (x + 34, y + 18)], fill=INK, width=3)
        draw.ellipse([x + 4, y + 8, x + 12, y + 14], fill=INK)
        draw.ellipse([x + 40, y + 8, x + 48, y + 14], fill=INK)
        draw.polygon([(cx - 8, y + 34), (cx, y + 46), (cx + 8, y + 34)],
                     fill=RED)
    elif kind == "toxic":
        draw.polygon([(cx, y + 6), (cx + 20, y + 44), (cx - 20, y + 44)],
                     outline=(200, 140, 20), width=3)
        draw.ellipse([cx - 3, y + 18, cx + 3, y + 30], fill=(200, 140, 20))
        draw.ellipse([cx - 3, y + 34, cx + 3, y + 40], fill=(200, 140, 20))
    elif kind == "plane":
        draw.polygon([(x + 6, y + 28), (x + 30, y + 14), (x + s - 6, y + 18),
                      (x + 30, y + 26), (x + 12, y + 34)], fill=NAVY)
        draw.polygon([(x + 24, y + 20), (x + 34, y + 34), (x + 28, y + 34)],
                     fill=NAVY)
    elif kind == "moto":
        draw.ellipse([x + 8, y + 30, x + 20, y + 42], outline=INK, width=3)
        draw.ellipse([x + 34, y + 30, x + 46, y + 42], outline=INK, width=3)
        draw.line([(x + 14, y + 36), (x + 26, y + 22), (x + 40, y + 36)],
                  fill=RED, width=3)
        draw.line([(x + 26, y + 22), (x + 22, y + 12)], fill=INK, width=3)
        draw.ellipse([x + 20, y + 8, x + 26, y + 14], fill=INK)


SMALL_ICONS = ["building", "ship", "dome", "tanker", "people", "drone",
               "toxic", "plane", "plane", "moto"]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- header: 0-52 ----------
    d.rectangle([0, 0, W, 52], fill=NAVY)
    d.text((14, 6), "THE WORLD IN ONE DAY", font=font(F_B, 24),
           fill=(255, 255, 255))
    d.text((W - 14, 10), "MONDAY, 23 NOVEMBER 2026", font=font(F_B, 20),
           fill=(245, 200, 40), anchor="ra")
    d.rectangle([0, 52, W, 56], fill=RED)

    # ---------- 3 big headlines: label 62, boxes 76-252 ----------
    d.text((14, 62), "TOP STORIES", font=font(F_B, 11), fill=NAVY)
    d.text((W - 14, 62), "36 STORIES  •  7 REGIONS  •  ONE DAY",
           font=font(F_B, 11), fill=GREY, anchor="ra")
    y0, bh, bw, gap = 76, 176, 330, 6
    big_icons = ["globe", "fire", "chart"]
    for i, (num, title, place, accent, body) in enumerate(BIG):
        x = 14 + i * (bw + gap)
        d.rectangle([x, y0, x + bw, y0 + bh], fill=CARD, outline=LINE)
        d.rectangle([x, y0, x + bw, y0 + 30], fill=accent)
        d.text((x + 8, y0 + 6), num + "  " + place, font=font(F_B, 12),
               fill=(255, 255, 255))
        ix, iy, iw, ih = x + 8, y0 + 38, 62, 54
        d.rectangle([ix, iy, ix + iw, iy + ih], fill=SOFT, outline=LINE)
        draw_icon(d, big_icons[i], ix + 3, iy, 56, accent)
        tx = x + 78
        tlines = wrap(d, title, font(F_B, 15), bw - 86)
        para(d, tx, y0 + 40, tlines[:2], font(F_B, 15), INK, 18)
        blines = wrap(d, body, font(F_R, 12), bw - 16)
        para(d, x + 8, y0 + 100, blines[:4], font(F_R, 12), (60, 60, 60), 15)

    # ---------- 10 small stories: label 260, rows 274-366, 371-463 ----------
    d.text((14, 260), "MORE OF THE DAY", font=font(F_B, 11), fill=NAVY)
    y0, bh, bw, gap = 274, 92, 194, 6
    for i, (num, title, body) in enumerate(SMALL):
        r, c = divmod(i, 5)
        x = 14 + c * (bw + gap)
        y = y0 + r * (bh + 5)
        d.rectangle([x, y, x + bw, y + bh], fill=CARD, outline=LINE)
        d.rectangle([x, y, x + 4, y + bh], fill=NAVY)
        ix, iy = x + 8, y + 8
        d.rectangle([ix, iy, ix + 44, iy + 44], fill=SOFT, outline=LINE)
        draw_icon(d, SMALL_ICONS[i], ix - 2, iy - 2, 48, NAVY)
        tx = x + 58
        d.text((tx, y + 8), num, font=font(F_B, 10), fill=RED)
        tlines = wrap(d, title, font(F_B, 11), bw - 66)
        para(d, tx, y + 21, tlines[:3], font(F_B, 11), INK, 13)
        blines = wrap(d, body, font(F_R, 10), bw - 66)
        para(d, tx, y + 62, blines[:2], font(F_R, 10), (70, 70, 70), 12)

    # ---------- map: label 471, map 485-631 ----------
    d.text((14, 471), "WHERE IT HAPPENED", font=font(F_B, 11), fill=NAVY)
    my0, mh = 485, 146
    d.rectangle([10, my0, W - 10, my0 + mh], fill=SEA, outline=(160, 180, 195))
    mx0, mw = 10, W - 20
    LON_MIN, LON_MAX, LAT_MIN, LAT_MAX = -170, 190, -55, 75

    def project(lon, lat):
        px = mx0 + (lon - LON_MIN) / (LON_MAX - LON_MIN) * mw
        py = my0 + (LAT_MAX - lat) / (LAT_MAX - LAT_MIN) * mh
        return px, py

    for poly in CONTINENTS:
        clipped = clip_polygon(poly, LON_MIN, LON_MAX, LAT_MIN, LAT_MAX)
        if len(clipped) >= 3:
            pts = [project(lon, lat) for lon, lat in clipped]
            d.polygon(pts, fill=LAND, outline=LAND_EDGE)
    f_pin = font(F_B, 9)
    f_lab = font(F_B, 9)
    for num, lon, lat, label, dx, dy, ox, oy in PINS:
        px, py = project(lon, lat)
        cx, cy = px + ox, py + oy
        if ox or oy:
            d.line([(px, py), (cx, cy)], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED,
                  outline=(255, 255, 255), width=2)
        d.text((cx, cy - 1), num, font=f_pin, fill=(255, 255, 255), anchor="mm")
        halo_text(d, (cx + dx, cy + dy), num + " " + label, f_lab)

    # ---------- region bar: label 639, bar 653-669, legend 673 ----------
    d.text((14, 639), "REGIONS — 36 STORIES", font=font(F_B, 11), fill=NAVY)
    bx, bw_tot = 14, W - 28
    x = bx
    for name, n, col in REGIONS:
        seg = bw_tot * n / 36.0
        d.rectangle([x, 653, x + seg - 2, 669], fill=col)
        x += seg
    f_reg = font(F_B, 10)
    lx = 14
    for name, n, col in REGIONS:
        d.rectangle([lx, 674, lx + 10, 684], fill=col)
        lx += 13
        item = name + " " + str(n)
        d.text((lx, 673), item, font=f_reg, fill=INK)
        lx += int(d.textlength(item, font=f_reg)) + 16

    # ---------- briefs 14-36: label 693, rows 707-947 ----------
    d.text((14, 693), "THE REST OF THE DAY — 14–36",
           font=font(F_B, 11), fill=NAVY)
    cols = [BRIEFS[0:8], BRIEFS[8:16], BRIEFS[16:23]]
    cw = 330
    for ci, col in enumerate(cols):
        cx = 14 + ci * (cw + 6)
        y = 707
        for num, title, body in col:
            d.text((cx, y), num + ".", font=font(F_B, 11), fill=RED)
            tlines = wrap(d, title, font(F_B, 11), cw - 26)
            para(d, cx + 24, y, tlines[:1], font(F_B, 11), INK, 13)
            blines = wrap(d, body, font(F_R, 10), cw - 24)
            para(d, cx + 24, y + 14, blines[:1], font(F_R, 10), (70, 70, 70), 12)
            y += 30

    # ---------- footer: 955-1000 ----------
    flines = wrap(d, "HOW THIS PAGE WAS MADE — Drawn by hand with code: no photos, "
                  "no wire images. News and follow-ups reported Mon 23 Nov 2026; "
                  "COP31 and Marquez are Sun 22 Nov results, flagged in their items.",
                  font(F_R, 10), W - 28)
    para(d, 14, 955, flines, font(F_R, 10), GREY, 13)
    slines = wrap(d, "SOURCES: AFP, AP, Reuters, CNN, The Guardian, Le Monde, WSJ, "
                  "Al Jazeera, Oxfam/CEOBS, One Turn, Inshorts, IANS, Times Now, "
                  "Dubai Standard, Addis Standard, CNBC Indonesia, SCMP, Lowy "
                  "Institute, WHO.", font(F_R, 10), W - 28)
    para(d, 14, 955 + len(flines) * 13 + 2, slines, font(F_R, 10), GREY, 13)

    img.save(OUT, optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
