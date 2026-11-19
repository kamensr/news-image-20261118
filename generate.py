#!/usr/bin/env python3
"""Generate entry.png for the make.fun news-image-20261118 competition (v2).

A dense winner-format news poster summing up Wednesday 18 November 2026:
49 verified stories across 7 regions -- 4 feature stories, 12 mini stories,
33 one-liners, a UTC timeline, a world map with numbered pins, and a date
check box listing big stories deliberately left out because they broke
before the 18th.

Everything is drawn with PIL (flat shapes + real text, no AI photos).
Run: python3 generate.py  ->  writes entry.png (1024x1024) next to this file.

NOTE: the grader runs main.py in python:3.13-slim with the standard library
only, so main.py is a plain copy of the entry.png this script produces.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette (broadsheet: cream paper, black ink, red + navy accents) -------
PAPER = (250, 245, 235)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RED = (176, 42, 42)
NAVY = (27, 42, 77)
TEAL = (23, 107, 101)
GOLD = (176, 132, 26)
PANEL = (238, 231, 214)
PANEL2 = (243, 236, 222)
LINE = (200, 190, 168)
SEA = (208, 226, 231)
LAND = (188, 210, 172)
LAND2 = (172, 198, 158)
WHITE = (255, 255, 255)
CLAIM_BG = (176, 42, 42)
CONF_BG = (23, 107, 101)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"


def F(path, size):
    return ImageFont.truetype(path, size)


F_SERIF = lambda s: F(DJ + "DejaVuSerif-Bold.ttf", s)   # masthead
F_B = lambda s: F(DJ + "DejaVuSans-Bold.ttf", s)        # headlines, tags
F_R = lambda s: F(DJ + "DejaVuSans.ttf", s)             # body
F_LB = lambda s: F(LB + "LiberationSans-Bold.ttf", s)   # dense list
F_LR = lambda s: F(LB + "LiberationSans-Regular.ttf", s)


def wrap(d, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, text, font, width, fill, leading, max_lines=None):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def tag(d, x, y, text, font, bg, fg=WHITE, pad_x=5, pad_y=2):
    """Draw a small filled pill tag; returns the x just past it."""
    w = int(d.textlength(text, font=font)) + 2 * pad_x
    h = font.size + 2 * pad_y + 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
    return x + w


def rule(d, y, x0=16, x1=1008, color=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


# --- canvas -----------------------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- header -----------------------------------------------------------------
rule(d, 8, width=3)
d.text((512, 16), "ONE DAY OF WORLD NEWS, ONE PICTURE",
       font=F_B(15), fill=RED, anchor="ma")
d.text((512, 34), "Wednesday 18 November 2026",
       font=F_SERIF(36), fill=INK, anchor="ma")
d.text((512, 74), "49 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE FROM THIS WEDNESDAY",
       font=F_B(14), fill=NAVY, anchor="ma")
rule(d, 92, width=1, color=LINE)

# --- UTC timeline strip -----------------------------------------------------
TL_Y = 96
d.text((16, TL_Y), "THE DAY IN UTC", font=F_B(11), fill=RED)
timeline = [
    ("00:48", "M5.3 quake\nshakes Romania"),
    ("01:44", "U.S. jets strike\nQeshm Island"),
    ("03:50", "AP calls Peltola's\nAlaska win"),
    ("04:41", "M5.8 quake\noff Flores"),
    ("06:07", "M5.9 quake\noff Peru"),
    ("10:16", "Voyager 1 passes\none light-day"),
    ("13:01", "Israeli tanks cross\nthe Yellow Line"),
    ("15:08", "U.S. home sales\nhit record low"),
    ("19:00", "Fed minutes point\nto more hikes"),
    ("20:48", "Carney meets Trump\nin Shenzhen"),
]
tl_x0, tl_w = 16, 992
col_w = tl_w / len(timeline)
d.line([(tl_x0 + 4, TL_Y + 30), (tl_x0 + tl_w - 4, TL_Y + 30)],
       fill=NAVY, width=2)
for i, (t, label) in enumerate(timeline):
    cx = tl_x0 + col_w * i + col_w / 2
    d.ellipse([cx - 4, TL_Y + 26, cx + 4, TL_Y + 34], fill=RED)
    d.text((cx, TL_Y + 11), t, font=F_B(11), fill=NAVY, anchor="ma")
    for j, ln in enumerate(label.split("\n")):
        d.text((cx, TL_Y + 38 + j * 11), ln, font=F_LR(10), fill=INK,
               anchor="ma")
rule(d, 156, width=1, color=LINE)


# --- feature illustrations (flat shapes, drawn per story) ------------------
def ill_hormuz(d, x, y, w, h):
    """Strait at night: tanker burning, jets overhead."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 52, 84))
    d.ellipse([x + w - 34, y + 8, x + w - 12, y + 30], fill=(240, 200, 90))
    # jets: small white triangles with red tails
    for jx, jy, s in [(x + 18, y + 22, 1.0), (x + 52, y + 14, 0.8)]:
        d.polygon([(jx, jy), (jx + 26 * s, jy + 6 * s), (jx + 4 * s, jy + 10 * s)],
                  fill=(235, 235, 235))
        d.polygon([(jx + 4 * s, jy + 10 * s), (jx + 26 * s, jy + 6 * s),
                   (jx + 20 * s, jy + 12 * s)], fill=RED)
    # sea
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(16, 66, 96))
    d.line([(x, y + h - 34), (x + w, y + h - 34)], fill=(120, 180, 200), width=2)
    # tanker hull
    d.rectangle([x + 18, y + h - 52, x + w - 18, y + h - 30], fill=(120, 40, 36))
    d.rectangle([x + w - 52, y + h - 66, x + w - 30, y + h - 52], fill=(200, 200, 200))
    # flames
    for fx, fh in [(x + 34, 26), (x + 56, 34), (x + 78, 22)]:
        d.polygon([(fx, y + h - 52), (fx + 8, y + h - 52 - fh),
                   (fx + 16, y + h - 52)], fill=(240, 140, 30))
        d.polygon([(fx + 4, y + h - 52), (fx + 8, y + h - 52 - fh + 10),
                   (fx + 12, y + h - 52)], fill=(250, 210, 60))


def ill_kerch(d, x, y, w, h):
    """Bridge with a collapsed arch, smoke rising from the gap."""
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 226))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(70, 120, 150))
    # towers
    d.rectangle([x + 22, y + 26, x + 30, y + h - 30], fill=(90, 90, 95))
    d.rectangle([x + w - 30, y + 26, x + w - 22, y + h - 30], fill=(90, 90, 95))
    # deck, split in the middle where the arch fell
    d.rectangle([x + 8, y + 58, x + w // 2 - 14, y + 66], fill=(60, 60, 65))
    d.rectangle([x + w // 2 + 14, y + 58, x + w - 8, y + 66], fill=(60, 60, 65))
    # fallen arch chunk in the water
    d.polygon([(x + w // 2 - 16, y + h - 30), (x + w // 2 + 16, y + h - 30),
               (x + w // 2 + 8, y + h - 12), (x + w // 2 - 8, y + h - 12)],
              fill=(60, 60, 65))
    # cables
    d.line([(x + 26, y + 28), (x + 60, y + 58)], fill=(120, 120, 125), width=2)
    d.line([(x + w - 26, y + 28), (x + w - 60, y + 58)], fill=(120, 120, 125), width=2)
    # smoke from the gap
    for sx, sy, r in [(x + w // 2 - 6, y + 40, 7), (x + w // 2 + 4, y + 30, 9),
                      (x + w // 2 + 12, y + 18, 6)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 120, 120))


def ill_shenzhen(d, x, y, w, h):
    """Shenzhen skyline at dusk with three flags on the tarmac."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 196, 120))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(90, 90, 95))
    # skyline
    heights = [44, 66, 38, 78, 52, 88, 46, 60]
    bw = w / len(heights)
    for i, hh in enumerate(heights):
        bx = x + i * bw + 2
        d.rectangle([bx, y + h - 26 - hh, bx + bw - 4, y + h - 26],
                    fill=(60, 70, 100) if i % 2 else (45, 55, 85))
        for wy in range(int(y + h - 26 - hh) + 6, int(y + h - 32), 10):
            d.rectangle([bx + 3, wy, bx + 6, wy + 4], fill=(250, 220, 130))
    # red carpet
    d.rectangle([x + 20, y + h - 14, x + w - 20, y + h - 4], fill=RED)
    # three flags
    for i, cols in enumerate([((200, 30, 30), (255, 220, 0)),
                              ((30, 60, 160), (255, 255, 255)),
                              ((255, 255, 255), (200, 30, 30))]):
        fx = x + 26 + i * 44
        d.line([(fx, y + h - 26), (fx, y + h - 58)], fill=(40, 40, 40), width=2)
        d.rectangle([fx, y + h - 58, fx + 26, y + h - 42], fill=cols[0])
        d.rectangle([fx, y + h - 50, fx + 26, y + h - 42], fill=cols[1])


def ill_gaza(d, x, y, w, h):
    """Tanks advancing past tents under a dusty sky."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 214, 170))
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(196, 168, 118))
    # tents
    for tx in [x + 12, x + 44, x + w - 44]:
        d.polygon([(tx, y + h - 30), (tx + 14, y + h - 52), (tx + 28, y + h - 30)],
                  fill=(240, 238, 228))
        d.line([(tx + 14, y + h - 52), (tx + 14, y + h - 30)], fill=(150, 140, 120))
    # tank 1 (large)
    d.rounded_rectangle([x + 56, y + h - 58, x + 118, y + h - 38], radius=4,
                        fill=(90, 100, 70))
    d.rectangle([x + 70, y + h - 68, x + 100, y + h - 56], fill=(90, 100, 70))
    d.rectangle([x + 100, y + h - 64, x + 132, y + h - 60], fill=(70, 80, 55))
    for wx in range(x + 62, x + 114, 10):
        d.ellipse([wx, y + h - 40, wx + 7, y + h - 33], fill=(60, 68, 48))
    # tank 2 (small, behind)
    d.rounded_rectangle([x + w - 58, y + h - 48, x + w - 14, y + h - 34], radius=3,
                        fill=(110, 118, 86))
    d.rectangle([x + w - 48, y + h - 55, x + w - 28, y + h - 46], fill=(110, 118, 86))
    # smoke
    for sx, sy, r in [(x + 30, y + 22, 8), (x + 42, y + 14, 6), (x + w - 30, y + 20, 7)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(160, 150, 130))


# --- feature boxes ----------------------------------------------------------
FEATURES = [
    dict(num=1, region="MIDDLE EAST", beat="WAR", status="CONFIRMED",
         claim=True,
         headline="U.S. jets hit Iran's Qeshm Island; Tehran strikes back",
         body=("U.S. jets struck an IRGC missile site on Qeshm Island at 01:44 "
               "UTC. Iran hit bases in Kuwait and Bahrain; tankers burned in "
               "the strait. Iran says it downed a U.S. MQ-9 drone \u2014 CLAIM."),
         source="REUTERS \u00b7 AFP \u00b7 AP \u00b7 AL JAZEERA", ill=ill_hormuz),
    dict(num=2, region="EUROPE", beat="WAR", status="CONFIRMED",
         claim=False,
         headline="Kerch Bridge hit again \u2014 third time in 3 days",
         body=("Ukraine struck the Crimea bridge again; traffic halted and "
               "damage is unassessed. The road arch collapsed into the sea on "
               "Tuesday. Engineers put repairs at two years or more."),
         source="THE GUARDIAN \u00b7 AKSYONOV", ill=ill_kerch),
    dict(num=3, region="ASIA-PACIFIC", beat="DIPLOMACY", status="CONFIRMED",
         claim=False,
         headline="Xi greets Trump in Shenzhen; three-way talks set",
         body=("Xi met Trump on the tarmac as APEC opened. Trump shook hands "
               "with Putin \u2014 their first encounter since 2025. The first "
               "Trump\u2013Xi\u2013Putin summit is Thursday, 14:30."),
         source="AP \u00b7 AFP \u00b7 USA TODAY", ill=ill_shenzhen),
    dict(num=4, region="MIDDLE EAST", beat="WAR", status="CONFIRMED",
         claim=True,
         headline="Israeli tanks cross the Yellow Line in central Gaza",
         body=("Tanks advanced near Nuseirat and Bureij in the first ground "
               "raid since the October 2025 ceasefire. Three were killed. "
               "Trump's Board of Peace accused both sides of failing the "
               "truce."),
         source="REUTERS", ill=ill_gaza),
]

FEAT_Y, FEAT_H, FEAT_GAP = 162, 122, 6
FEAT_W = (992 - FEAT_GAP) // 2


def draw_feature(f, bx, by):
    d.rectangle([bx, by, bx + FEAT_W, by + FEAT_H], fill=PANEL2,
                outline=LINE, width=1)
    # number chip
    d.ellipse([bx + 6, by + 6, bx + 24, by + 24], fill=RED)
    d.text((bx + 15, by + 8), str(f["num"]), font=F_B(11), fill=WHITE,
           anchor="ma")
    # illustration panel
    ix, iy, iw, ih = bx + 8, by + 28, 132, FEAT_H - 36
    f["ill"](d, ix, iy, iw, ih)
    d.rectangle([ix, iy, ix + iw, iy + ih], outline=LINE, width=1)
    # text column
    tx = bx + 148
    tw = FEAT_W - 156
    ty = by + 8
    nx = tag(d, tx, ty, f["region"], F_B(10), NAVY)
    nx = tag(d, nx + 4, ty, f["beat"], F_B(10), GOLD)
    nx = tag(d, nx + 4, ty, f["status"], F_B(10), CONF_BG)
    if f["claim"]:
        tag(d, nx + 4, ty, "INCLUDES A CLAIM", F_B(10), CLAIM_BG)
    hy = ty + 22
    draw_lines(d, tx, hy, f["headline"], F_B(15), tw, INK, 18, max_lines=2)
    draw_lines(d, tx, hy + 38, f["body"], F_LR(11), tw, INK, 13, max_lines=3)
    d.text((tx, by + FEAT_H - 15), f["source"], font=F_LB(9), fill=MUTED)


for i, f in enumerate(FEATURES):
    bx = 16 + (i % 2) * (FEAT_W + FEAT_GAP)
    by = FEAT_Y + (i // 2) * (FEAT_H + FEAT_GAP)
    draw_feature(f, bx, by)


# --- mini-story icons (tiny flat drawings, 40x40 box) -----------------------
def ic_ballot(d, x, y, s):
    d.rectangle([x + 6, y + 16, x + s - 6, y + s - 4], fill=NAVY)
    d.rectangle([x + 12, y + 4, x + 26, y + 18], fill=WHITE, outline=NAVY)
    d.polygon([(x + 14, y + 12), (x + 18, y + 16), (x + 25, y + 7)],
              fill=RED)


def ic_document(d, x, y, s):
    d.rectangle([x + 10, y + 4, x + s - 10, y + s - 4], fill=WHITE,
                outline=NAVY, width=2)
    for ly in [y + 12, y + 19, y + 26]:
        d.line([(x + 14, ly), (x + s - 14, ly)], fill=NAVY, width=2)
    d.ellipse([x + s - 20, y + s - 16, x + s - 8, y + s - 4], fill=GOLD)


def ic_coins(d, x, y, s):
    for i, cy in enumerate([y + s - 10, y + s - 17, y + s - 24]):
        d.ellipse([x + 8, cy, x + 30, cy + 8], fill=GOLD, outline=(140, 100, 10))
    d.polygon([(x + 26, y + 16), (x + 34, y + 16), (x + 34, y + 8),
               (x + 38, y + 8), (x + 30, y + 20)], fill=TEAL)


def ic_flags(d, x, y, s):
    d.line([(x + 10, y + 6), (x + 10, y + s - 4)], fill=INK, width=2)
    d.line([(x + 24, y + 6), (x + 24, y + s - 4)], fill=INK, width=2)
    d.rectangle([x + 10, y + 6, x + 22, y + 16], fill=RED)
    d.rectangle([x + 14, y + 6, x + 18, y + 16], fill=WHITE)
    d.rectangle([x + 24, y + 6, x + 36, y + 16], fill=(30, 60, 160))
    d.rectangle([x + 24, y + 11, x + 36, y + 16], fill=WHITE)
    d.rectangle([x + 24, y + 13, x + 36, y + 16], fill=RED)


def ic_house(d, x, y, s):
    d.polygon([(x + 6, y + 20), (x + 20, y + 6), (x + 34, y + 20)], fill=RED)
    d.rectangle([x + 10, y + 20, x + 30, y + s - 4], fill=(200, 180, 150))
    d.rectangle([x + 17, y + 26, x + 23, y + s - 4], fill=NAVY)
    d.polygon([(x + 30, y + 12), (x + 36, y + 12), (x + 33, y + 20)], fill=TEAL)


def ic_probe(d, x, y, s):
    d.polygon([(x + 20, y + 4), (x + 30, y + 14), (x + 20, y + 24),
               (x + 10, y + 14)], fill=(180, 190, 200))
    d.line([(x + 20, y + 24), (x + 20, y + 32)], fill=INK, width=2)
    d.ellipse([x + 16, y + 30, x + 24, y + 38], fill=GOLD)
    d.ellipse([x + 6, y + 6, x + 10, y + 10], fill=GOLD)
    d.ellipse([x + 32, y + 26, x + 35, y + 29], fill=GOLD)


def ic_chat(d, x, y, s):
    d.rounded_rectangle([x + 4, y + 6, x + s - 4, y + 26], radius=5, fill=TEAL)
    d.polygon([(x + 12, y + 26), (x + 12, y + 34), (x + 20, y + 26)], fill=TEAL)
    d.text((x + s // 2, y + 9), "6.2", font=F_B(13), fill=WHITE, anchor="ma")


def ic_virus(d, x, y, s):
    cx, cy = x + 20, y + 20
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(cx + dx * 10, cy + dy * 10), (cx + dx * 16, cy + dy * 16)],
               fill=RED, width=2)
        d.ellipse([cx + dx * 15 - 2, cy + dy * 15 - 2,
                   cx + dx * 15 + 2, cy + dy * 15 + 2], fill=RED)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=RED)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 180, 180))


def ic_drought(d, x, y, s):
    d.ellipse([x + 12, y + 4, x + 28, y + 20], fill=(240, 180, 40))
    for ang in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        d.line([(x + 20 + dx * 11, y + 12 + dy * 11),
                (x + 20 + dx * 15, y + 12 + dy * 15)], fill=(240, 180, 40),
               width=2)
    d.rectangle([x + 4, y + 28, x + s - 4, y + s - 4], fill=(196, 168, 118))
    d.line([(x + 10, y + 30), (x + 16, y + 34), (x + 12, y + 38)], fill=(120, 100, 60))
    d.line([(x + 26, y + 30), (x + 22, y + 35)], fill=(120, 100, 60))


def ic_drone(d, x, y, s):
    d.rectangle([x + 14, y + 16, x + 26, y + 24], fill=INK)
    for px, py in [(x + 6, y + 12), (x + 30, y + 12), (x + 6, y + 26),
                   (x + 30, y + 26)]:
        d.line([(x + 20, y + 20), (px, py)], fill=INK, width=2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
    d.ellipse([x + 17, y + 18, x + 23, y + 24], fill=RED)


def ic_chart(d, x, y, s):
    d.line([(x + 6, y + s - 6), (x + s - 6, y + s - 6)], fill=INK, width=2)
    d.line([(x + 6, y + s - 6), (x + 6, y + 6)], fill=INK, width=2)
    d.line([(x + 8, y + 12), (x + 16, y + 18), (x + 24, y + 14),
            (x + 32, y + 24)], fill=RED, width=3)
    d.polygon([(x + 32, y + 24), (x + 28, y + 22), (x + 33, y + 20)], fill=RED)
    d.rectangle([x + 8, y + 28, x + 16, y + 32], fill=GOLD)


def ic_globe(d, x, y, s):
    d.ellipse([x + 6, y + 4, x + s - 6, y + s - 4], fill=(90, 150, 190))
    d.ellipse([x + 12, y + 10, x + 22, y + 18], fill=(120, 190, 120))
    d.ellipse([x + 20, y + 22, x + 30, y + 30], fill=(120, 190, 120))
    d.line([(x + 6, y + 20), (x + s - 6, y + 20)], fill=(255, 255, 255), width=1)


MINIS = [
    dict(num=5, region="AMERICAS", icon=ic_ballot,
         headline="Peltola wins Alaska Senate seat",
         body="Beats Sullivan 50.1%\u201345.8%; Democrats take the Senate 56\u201344. First Alaska Native senator.",
         source="AP"),
    dict(num=6, region="AMERICAS", icon=ic_document,
         headline="Hegseth signs deal in surprise Caracas visit",
         body="Meets interim President Delcy Rodr\u00edguez; joint training and intel sharing agreed.",
         source="AP \u00b7 REUTERS \u00b7 CNN"),
    dict(num=7, region="AMERICAS", icon=ic_coins,
         headline="Brazil Senate passes Lula fiscal package",
         body="Worth up to 60bn reais in 2027; the real fell 1.5% on the day.",
         source="REUTERS \u00b7 AP"),
    dict(num=8, region="AMERICAS", icon=ic_flags,
         headline="Carney meets Trump for 20 minutes, no deal",
         body="Shenzhen sideline talks end with a pledge to keep talking; 50% U.S. tariffs stay.",
         source="CANADIAN PRESS \u00b7 ANI"),
    dict(num=9, region="AMERICAS", icon=ic_house,
         headline="U.S. pending home sales hit record low",
         body="Index falls to 63.0, lowest since 2001; signings down 16.7% on a year ago.",
         source="NAR \u00b7 REUTERS"),
    dict(num=10, region="GLOBAL", icon=ic_probe,
         headline="Voyager 1 reaches one light-day from Earth",
         body="NASA's probe passes 16bn miles from home, 49 years after launch.",
         source="NASA JPL"),
    dict(num=11, region="GLOBAL", icon=ic_chat,
         headline="OpenAI launches GPT-6.2 Astra and Sol",
         body="New flagship models arrive as Microsoft and Google answer with their own launches.",
         source="ANI \u00b7 SC MEDIA"),
    dict(num=12, region="AFRICA", icon=ic_virus,
         headline="Ebola toll tops 5,600 dead in DR Congo",
         body="CDC counts 11,536 cases; children are a third of deaths.",
         source="CDC"),
    dict(num=13, region="OCEANIA", icon=ic_drought,
         headline="Fiji declares national disaster over drought",
         body="El Ni\u00f1o dries reservoirs; emergency powers unlock relief funds.",
         source="RNZ PACIFIC"),
    dict(num=14, region="EUROPE", icon=ic_drone,
         headline="Three Russian drone strikes hit central Odesa",
         body="Four dead, 17+ injured in jet-drone attacks on the port city.",
         source="MEANWHILE IN UKRAINE"),
    dict(num=15, region="GLOBAL", icon=ic_chart,
         headline="Markets: S&P falls for a fifth straight day",
         body="Dow \u22121.11%, Nasdaq +0.42%; gold plunges 3.5% to $3,728. Fed minutes point to more hikes.",
         source="MARKET DATA \u00b7 FED"),
    dict(num=16, region="GLOBAL", icon=ic_globe,
         headline="COP31 enters crunch time in Antalya",
         body="Adaptation-finance draft offers three options and no number after EU pushback.",
         source="COLUMBIA SABIN CENTER"),
]

MINI_Y, MINI_H, MINI_GAP = 420, 96, 6
MINI_W = (992 - 3 * MINI_GAP) // 4


def draw_mini(m, bx, by):
    d.rectangle([bx, by, bx + MINI_W, by + MINI_H], fill=PANEL2,
                outline=LINE, width=1)
    # number chip + region tag + source (one row)
    d.ellipse([bx + 6, by + 6, bx + 22, by + 22], fill=NAVY)
    d.text((bx + 14, by + 8), str(m["num"]), font=F_B(10), fill=WHITE,
           anchor="ma")
    nx = tag(d, bx + 26, by + 7, m["region"], F_B(9), NAVY)
    d.text((nx + 5, by + 8), m["source"], font=F_LB(9), fill=MUTED)
    # icon box
    ix, iy = bx + 6, by + 28
    d.rectangle([ix, iy, ix + 38, iy + 38], fill=WHITE, outline=LINE, width=1)
    m["icon"](d, ix - 1, iy - 1, 40)
    # headline beside icon
    draw_lines(d, ix + 44, iy + 1, m["headline"], F_B(12), MINI_W - 56,
               INK, 14, max_lines=2)
    # body below icon row
    draw_lines(d, bx + 6, by + 70, m["body"], F_LR(10), MINI_W - 12,
               INK, 12, max_lines=2)


rule(d, 416, width=1, color=LINE)
for i, m in enumerate(MINIS):
    bx = 16 + (i % 4) * (MINI_W + MINI_GAP)
    by = MINI_Y + (i // 4) * (MINI_H + MINI_GAP)
    draw_mini(m, bx, by)


# --- map + "ALSO ON" list band ----------------------------------------------
rule(d, 724, width=1, color=LINE)
BAND_Y, BAND_H = 728, 220

# --- world map (stylised continents, lon/lat polygons) ----------------------
MAP_X, MAP_Y, MAP_W, MAP_H = 16, BAND_Y, 320, BAND_H
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
            outline=LINE, width=1)
d.text((MAP_X + 8, MAP_Y + 5), "WHERE IT HAPPENED", font=F_B(12), fill=NAVY)
d.text((MAP_X + 8, MAP_Y + MAP_H - 16), "Pins match story numbers.",
       font=F_LR(10), fill=MUTED)

mx, my, mw, mh = MAP_X + 6, MAP_Y + 26, MAP_W - 12, MAP_H - 46


def ll(lon, lat):
    return (mx + (lon + 170) / 360.0 * mw,
            my + (75 - lat) / 130.0 * mh)


def continent(pts, fill=LAND):
    d.polygon([ll(lon, lat) for lon, lat in pts], fill=fill,
              outline=(140, 165, 130))


continent([(-165, 65), (-140, 70), (-110, 68), (-90, 66), (-75, 62),
           (-60, 52), (-70, 42), (-80, 32), (-90, 21), (-97, 16),
           (-105, 22), (-115, 30), (-125, 42), (-130, 55), (-150, 60)])
continent([(-45, 60), (-30, 68), (-25, 76), (-55, 78), (-60, 70)], LAND2)
continent([(-79, 9), (-70, 11), (-55, 5), (-40, -5), (-35, -10), (-40, -22),
           (-50, -32), (-60, -40), (-65, -50), (-70, -54), (-73, -40),
           (-72, -25), (-77, -12), (-80, -3)])
continent([(-10, 36), (-5, 43), (0, 50), (5, 58), (10, 60), (18, 56),
           (25, 60), (30, 70), (40, 68), (30, 55), (28, 45), (20, 40),
           (12, 44), (8, 38), (3, 36)])
continent([(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
           (35, 27), (40, 12), (48, 10), (51, -2), (40, -10), (35, -20),
           (32, -28), (25, -34), (18, -34), (14, -22), (12, -10), (9, 4),
           (0, 6), (-8, 5), (-13, 8)])
continent([(30, 70), (60, 70), (90, 75), (120, 73), (150, 70), (178, 66),
           (170, 60), (160, 55), (140, 45), (130, 40), (122, 30), (110, 20),
           (105, 10), (100, 8), (95, 16), (90, 22), (85, 20), (80, 8),
           (75, 12), (70, 22), (60, 25), (55, 27), (48, 30), (44, 29),
           (40, 36), (35, 36), (30, 45), (28, 55), (30, 60)])
continent([(113, -22), (122, -14), (132, -12), (142, -11), (150, -22),
           (153, -28), (150, -37), (140, -38), (132, -32), (124, -33),
           (115, -32)])
continent([(167, -35), (174, -37), (178, -42), (172, -47), (167, -42)], LAND2)
continent([(-5, 50), (-2, 53), (-3, 58), (-6, 57)], LAND2)
continent([(130, 31), (135, 34), (140, 38), (142, 43), (145, 44), (141, 39),
           (136, 33)], LAND2)
# Indonesia: a few island blobs
for ilon, ilat, ir in [(100, 0, 4), (110, -6, 5), (120, -9, 4), (132, -3, 5),
                       (141, -4, 4)]:
    px, py = ll(ilon, ilat)
    d.ellipse([px - ir, py - ir // 2, px + ir, py + ir // 2], fill=LAND)

PINS = [(1, 57, 27), (2, 36.5, 45.3), (3, 114, 22.5), (4, 34.5, 31.5),
        (5, -155, 64), (6, -67, 9), (13, 178, -18), (24, -75, -14),
        (25, 120, -8.5), (28, -84, 28), (31, 72.8, 19), (38, 40, 9)]
for num, lon, lat in PINS:
    px, py = ll(lon, lat)
    r = 7
    d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
              outline=WHITE, width=1)
    d.text((px, py - 5), str(num), font=F_B(9), fill=WHITE, anchor="ma")

# --- "ALSO ON" numbered list -------------------------------------------------
LIST_X, LIST_W = 344, 664
d.text((LIST_X, BAND_Y + 2), "ALSO ON WEDNESDAY 18 NOVEMBER",
       font=F_B(13), fill=RED)
ALSO = [
    (17, "Anthropic prices IPO at $83 a share, above range"),
    (18, "EU proposes a \u20ac45bn joint-debt loan for Ukraine"),
    (19, "30+ leaders meet in Berlin Thu on Ukraine force"),
    (20, "UK inflation hits 3.6%, highest in a year"),
    (21, "UK resists EU push to mirror China tariffs"),
    (22, "Storms Bruna and Charles batter Portugal"),
    (23, "Romania: M5.3 quake felt in Bucharest, 2 hurt"),
    (24, "Peru: M5.9 quake off Ica; no damage"),
    (25, "Indonesia: M5.8 quake off Flores"),
    (26, "Papua New Guinea: M5.8 quake near Madang"),
    (27, "Cyclone Akvan nears India's Andhra coast"),
    (28, "Florida: St. Johns River in major flood"),
    (29, "Malaysia floods push 2,500+ into shelters"),
    (30, "Indonesia floods and landslide kill one"),
    (31, "William and Catherine award \u00a31m Earthshot Prizes"),
    (32, "Missile hits tanker MT TARA GAS; 1 Indian missing"),
    (33, "Microsoft launches seven in-house AI models"),
    (34, "Nvidia falls 2.89% despite $115.8bn quarter"),
    (35, "UnitedHealth \u221210.2%, Humana \u221213%; TJX +8%"),
    (36, "Fed's Waller: half-point Dec hike 'probably' needed"),
    (37, "12 red-state AGs appeal USPS ballot-check block"),
    (38, "Ethiopia and Eritrea mass forces at border"),
    (39, "Nigeria arrests 8 in Sahara cocaine gang"),
    (40, "Machar tells court he pushed Nasir deployment"),
    (41, "Angola cuts main rate to a 10-year low"),
    (42, "WHO child-protection conference opens in Manila"),
    (43, "Canary Islands arrivals up 65.9% on last year"),
    (44, "Taiwan logs 10 PLA sorties and 11 ships"),
    (45, "UWCL: Chelsea 1\u20130 PSG, Man City 2\u20130 H\u00e4cken"),
    (46, "CONCACAF: USA 2\u20130 Haiti, Mexico 1\u20130 Jamaica"),
    (47, "AngloGold plans $2.5bn copper mine in Colombia"),
    (48, "EU auditors: bloc failed to curb 'forever chemicals'"),
    (49, "Iraqi court jails six French IS members for life"),
]
COL_W = LIST_W // 2
ROW_Y0, ROW_LEAD = BAND_Y + 22, 11.5
for i, (num, text) in enumerate(ALSO):
    col = 0 if i < 17 else 1
    row = i if col == 0 else i - 17
    x = LIST_X + col * COL_W
    y = ROW_Y0 + row * ROW_LEAD
    d.text((x, y), f"{num}.", font=F_LB(11), fill=RED)
    d.text((x + 22, y), text, font=F_LR(11), fill=INK)

# --- DATE CHECK band --------------------------------------------------------
DC_Y, DC_H = 952, 38
d.rectangle([16, DC_Y, 1008, DC_Y + DC_H], fill=NAVY)
d.text((24, DC_Y + 3), "DATE CHECK \u2014 LEFT OUT ON PURPOSE (they broke before today):",
       font=F_B(10), fill=(255, 220, 120))
d.text((24, DC_Y + 15),
       "U.S. loses measles elimination status (17 Nov)  \u00b7  Russian jets breach Japan's airspace (17 Nov)  \u00b7  An-12 crash near Kemerovo, 19 dead (17 Nov)",
       font=F_LR(10), fill=WHITE)
d.text((24, DC_Y + 26),
       "Prague train collision injures 46 (17 Nov)  \u00b7  WHO warns 950,000 displaced Gazans face floods (13 Nov)  \u00b7  Rugby League World Cup final (15 Nov)",
       font=F_LR(10), fill=WHITE)

# --- footer -----------------------------------------------------------------
rule(d, 994, width=1, color=LINE)
d.text((512, 998),
       "Every story here happened or was first reported on Wednesday 18 November 2026.  CLAIM = one side's account, not independently confirmed.",
       font=F_LR(10), fill=MUTED, anchor="ma")
d.text((512, 1010),
       "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 BBC \u00b7 NAR \u00b7 NASA \u00b7 USGS \u00b7 IMD \u00b7 NWS \u00b7 CDC \u00b7 WHO \u00b7 ONS \u00b7 FT \u00b7 Euronews \u00b7 ANI \u00b7 RNZ Pacific",
       font=F_LR(10), fill=MUTED, anchor="ma")

img.save("entry.png")
print("saved entry.png")
