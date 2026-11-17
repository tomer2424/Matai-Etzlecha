import os
import random
import sys
from PIL import Image

# Pixel-art style sample: reception area + parking, 3/4 view (top faces + front faces).
# Native resolution 480x270 (16 px tiles), shown scaled x4 with nearest neighbour.
random.seed(3)
W, H = 480, 270
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
img = Image.new("RGB", (W, H))
P = img.load()

# ---------- palette (warm late afternoon) ----------
OUTL = (38, 26, 34)
GRASS = [(86, 140, 62), (98, 154, 68), (112, 168, 74), (74, 124, 56)]
STONE = [(214, 200, 176), (204, 188, 164), (224, 212, 190)]
MORTAR = (168, 150, 126)
ASPH = [(74, 76, 86), (68, 70, 80), (82, 84, 94)]
CURB_TOP, CURB_FRONT = (196, 194, 188), (140, 136, 132)
HEDGE_TOP, HEDGE_MID, HEDGE_DARK = (92, 150, 70), (66, 118, 54), (44, 86, 44)
WHITE, CREAM = (246, 244, 236), (226, 220, 206)
GOLD, GOLD_D = (230, 186, 80), (176, 132, 52)
PINK, PINK_D, ROSE = (240, 120, 160), (196, 80, 124), (250, 190, 210)
RED, RED_D = (176, 44, 62), (128, 30, 46)
LAMP = (255, 226, 140)


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        P[x, y] = c


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            put(xx, yy, c)


def blend(x, y, c, a):
    if 0 <= x < W and 0 <= y < H:
        o = P[x, y]
        P[x, y] = tuple(int(o[i] * (1 - a) + c[i] * a) for i in range(3))


def shadow(cx, cy, rx, ry, a=0.35):
    for yy in range(cy - ry, cy + ry + 1):
        for xx in range(cx - rx, cx + rx + 1):
            if ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1:
                blend(xx, yy, (20, 16, 30), a)


def glow(cx, cy, r, a=0.25):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
            if d <= r:
                blend(xx, yy, LAMP, a * (1 - d / r))


def sprite(rows, x, y, pal):
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch != ".":
                put(x + i, y + j, pal[ch])


# ---------- ground ----------
def grass(x0, y0, x1, y1):
    for y in range(y0, y1):
        for x in range(x0, x1):
            put(x, y, GRASS[1] if random.random() < 0.8 else random.choice(GRASS))
    for _ in range((x1 - x0) * (y1 - y0) // 40):  # small tufts
        x, y = random.randint(x0, x1 - 1), random.randint(y0 + 1, y1 - 1)
        put(x, y, GRASS[2]); put(x, y - 1, GRASS[2]); put(x + 1, y, GRASS[3])
    for _ in range((x1 - x0) * (y1 - y0) // 400):  # tiny flowers
        put(random.randint(x0, x1 - 1), random.randint(y0, y1 - 1), random.choice([WHITE, LAMP, ROSE]))


def pavers(x0, y0, x1, y1, t=16):
    for y in range(y0, y1):
        row = (y - y0) // (t // 2)
        off = (t // 2) if row % 2 else 0
        for x in range(x0, x1):
            lx, ly = (x - x0 + off) % t, (y - y0) % (t // 2)
            if lx == 0 or ly == 0:
                put(x, y, MORTAR)
            else:
                seed = ((x - x0 + off) // t * 31 + row * 17) % 3
                c = STONE[seed]
                if ly == 1 or lx == 1:
                    c = tuple(min(255, v + 10) for v in c)  # top-left highlight
                put(x, y, c)


def asphalt(x0, y0, x1, y1):
    for y in range(y0, y1):
        for x in range(x0, x1):
            put(x, y, ASPH[0] if random.random() < 0.75 else random.choice(ASPH))


def curb(x0, x1, y):
    rect(x0, y, x1 - x0, 2, CURB_TOP)
    rect(x0, y + 2, x1 - x0, 3, CURB_FRONT)
    rect(x0, y + 5, x1 - x0, 1, OUTL)


def hedge(x0, x1, y, h=10):
    """Box hedge: lighter top face, darker front face (3/4 view)."""
    top = 5
    for x in range(x0, x1):
        for yy in range(y, y + top):
            put(x, yy, HEDGE_TOP if random.random() < 0.75 else HEDGE_MID)
        for yy in range(y + top, y + h):
            put(x, yy, HEDGE_MID if random.random() < 0.7 else HEDGE_DARK)
    rect(x0, y + h, x1 - x0, 1, OUTL)
    for x in range(x0, x1):
        put(x, y - 1, OUTL)
    for yy in range(y, y + h):
        put(x0 - 1, yy, OUTL); put(x1, yy, OUTL)
    for x in range(x0, x1):
        blend(x, y + h + 1, (20, 16, 30), 0.3)


# ---------- props ----------
def lighten(c, v):
    return tuple(max(0, min(255, a + v)) for a in c)


def rrect(x, y, w, h, c, r=2):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            cx = min(xx - x, x + w - 1 - xx)
            cy = min(yy - y, y + h - 1 - yy)
            if cx + cy >= r:
                put(xx, yy, c)


def car(x, y, body, dark):
    """Car parked nose-up: hood, windshield, roof and trunk from above, rear face in front."""
    shadow(x + 11, y + 32, 14, 4)
    for wx in (x - 1, x + 20):  # tyres peeking out
        rect(wx, y + 4, 3, 6, OUTL); rect(wx, y + 21, 3, 7, OUTL)
    rrect(x - 1, y - 1, 24, 33, OUTL, 3)          # outline
    rrect(x, y, 22, 31, dark, 3)                   # rear face colour shows at the bottom
    rrect(x, y, 22, 25, body, 3)                   # top surfaces
    rrect(x + 1, y + 1, 20, 6, lighten(body, 22), 2)   # hood
    for i in range(4):                             # windshield (trapezoid)
        rect(x + 3 - (i // 2), y + 7 + i, 16 + (i // 2) * 2, 1, (120, 170, 205))
    rect(x + 4, y + 8, 3, 1, (210, 236, 250))
    rect(x + 3, y + 11, 16, 6, lighten(body, 34))  # roof
    rect(x + 1, y + 11, 2, 6, (60, 80, 104)); rect(x + 19, y + 11, 2, 6, (60, 80, 104))  # side windows
    rect(x + 3, y + 17, 16, 3, (70, 100, 130))     # rear window
    rect(x + 1, y + 20, 20, 4, body)               # trunk
    put(x - 2, y + 9, body); put(x + 23, y + 9, body)  # mirrors
    rect(x + 1, y + 25, 3, 2, (235, 64, 64)); rect(x + 18, y + 25, 3, 2, (235, 64, 64))
    rect(x + 8, y + 26, 6, 2, WHITE)               # plate
    rect(x + 1, y + 29, 20, 1, lighten(dark, -30)) # bumper


def lamp_post(x, y):
    shadow(x + 1, y + 1, 4, 2)
    rect(x, y - 30, 2, 31, (60, 56, 64))
    rect(x - 2, y - 34, 6, 4, OUTL)
    rect(x - 1, y - 33, 4, 2, LAMP)
    glow(x + 1, y - 32, 14, 0.35)


def cocktail_table(x, y):
    """Tall round cocktail table: wide oval top, cloth tied at the waist, flared hem."""
    shadow(x + 7, y + 16, 8, 3)
    rows = [(1, 13), (2, 11), (3, 9), (4, 7), (4, 7), (4, 7), (3, 9), (2, 11), (1, 13), (1, 13)]
    for i, (o, w) in enumerate(rows):          # cloth below the top
        rect(x + o, y + 5 + i, w, 1, CREAM)
        put(x + o - 1, y + 5 + i, OUTL); put(x + o + w, y + 5 + i, OUTL)
        put(x + 7, y + 5 + i, (210, 204, 190))
    rect(x + 4, y + 8, 7, 1, GOLD)             # ribbon at the waist
    rect(x, y + 15, 15, 1, OUTL)
    rrect(x - 1, y - 1, 17, 7, OUTL, 2)        # top (oval)
    rrect(x, y, 15, 5, WHITE, 2)
    put(x + 7, y + 1, PINK); put(x + 6, y + 2, ROSE); put(x + 8, y + 2, PINK); put(x + 7, y + 3, (120, 170, 90))


def potted_plant(x, y):
    shadow(x + 4, y + 12, 6, 2)
    rect(x + 1, y + 6, 7, 6, (186, 98, 64)); rect(x + 1, y + 6, 7, 1, (214, 128, 86))
    for xx in range(x + 1, x + 8):
        put(xx, y + 12, OUTL)
    for yy in range(y + 6, y + 12):
        put(x, yy, OUTL); put(x + 8, yy, OUTL)
    for yy in range(y - 2, y + 6):  # round bush
        for xx in range(x - 1, x + 10):
            dx, dy = (xx - (x + 4)) / 5.5, (yy - (y + 2)) / 4.5
            if dx * dx + dy * dy <= 1:
                c = HEDGE_TOP if dy < -0.2 else HEDGE_MID
                put(xx, yy, c if random.random() < 0.8 else HEDGE_DARK)


def welcome_sign(x, y):
    shadow(x + 9, y + 26, 9, 2)
    rect(x + 3, y + 14, 1, 12, (120, 80, 50)); rect(x + 14, y + 14, 1, 12, (120, 80, 50))
    rect(x, y, 18, 16, OUTL)
    rect(x + 1, y + 1, 16, 14, WHITE)
    for i in range(3):  # pretend handwriting
        for xx in range(x + 3 + i, x + 15 - i, 2):
            put(xx, y + 4 + i * 3, GOLD_D)
    put(x + 8, y + 12, PINK); put(x + 10, y + 12, PINK); put(x + 9, y + 13, PINK)


def flower_arch(x, y):
    """Entrance arch with flowers, 3/4 view."""
    shadow(x + 3, y + 46, 5, 2); shadow(x + 43, y + 46, 5, 2)
    for px in (x, x + 40):
        rect(px, y + 6, 6, 40, WHITE)
        rect(px + 4, y + 6, 2, 40, CREAM)
        for yy in range(y + 6, y + 46):
            put(px - 1, yy, OUTL); put(px + 6, yy, OUTL)
        rect(px - 1, y + 46, 8, 1, OUTL)
    rect(x, y, 46, 7, WHITE)
    rect(x, y + 5, 46, 2, CREAM)
    rect(x - 1, y - 1, 48, 1, OUTL); rect(x - 1, y + 7, 48, 1, OUTL)
    for _ in range(140):  # flower clusters on the beam and pillars
        if random.random() < 0.6:
            fx, fy = random.randint(x - 2, x + 47), random.randint(y - 3, y + 5)
        else:
            px = random.choice((x, x + 40))
            fx, fy = random.randint(px - 2, px + 7), random.randint(y + 6, y + 24)
        put(fx, fy, random.choice([PINK, ROSE, WHITE, PINK_D, (120, 170, 90), (120, 170, 90)]))


def gift_table(x, y):
    shadow(x + 9, y + 12, 11, 3)
    rect(x, y, 18, 4, WHITE); rect(x, y + 4, 18, 7, CREAM)
    rect(x - 1, y - 1, 20, 1, OUTL); rect(x - 1, y + 11, 20, 1, OUTL)
    rect(x + 5, y - 7, 8, 8, WHITE); rect(x + 5, y - 7, 8, 2, GOLD)  # check box
    rect(x + 8, y - 7, 2, 8, GOLD)
    for xx in range(x + 5, x + 13):
        put(xx, y - 8, OUTL)
    put(x + 8, y - 7, OUTL); put(x + 9, y - 7, OUTL)  # slot


def string_lights(x0, x1, y, sag=6):
    n = x1 - x0
    for i in range(n):
        t = i / n
        yy = int(y + sag * 4 * t * (1 - t))
        put(x0 + i, yy, OUTL)
        if i % 6 == 3:
            put(x0 + i, yy + 1, LAMP); put(x0 + i, yy + 2, LAMP)
            glow(x0 + i, yy + 2, 5, 0.25)


def light_pole(x, y):
    rect(x, y - 44, 2, 45, (90, 70, 56))
    rect(x - 1, y, 4, 1, OUTL)
    shadow(x + 1, y + 1, 3, 1)


# ---------- characters (12x20, facing left) ----------
PLAYER = [
    "....KKKK....", "..KKHHhHKK..", ".KHHHHHHHHK.", ".KHHSSSHHHK.", "KSSSSSSSHHK.",
    "KSESSESSsHK.", "KSSSSSSSsK..", ".KSSKKSSsK..", "..KKSSSKK...", ".KNNWTWNNK..",
    "KNNNWTWNNNK.", "KNNNNTNNNNK.", "KSKNNNNNKSK.", ".KKNNNNNKK..", "..KnNNNnK...",
    "..KPPKPPK...", "..KPPKPPK...", "..KPPKPPK...", ".KBBKKBBK...", ".KKK..KKK...",
]
AUNT = [
    "..KKKKKKK...", ".KRRrRRrRK..", "KRRrRRRRrRK.", "KRRSSSSRRRK.", "KRSSSSSSRRK.",
    "KSESSESSRRK.", "KSSSSSSSsRK.", ".KSSLLSSsK..", "..KKSSSKK...", ".KDwwwwwDK..",
    "KDDDDDDDDDK.", "KSDDDDDDDSK.", ".KDDdDDdDK..", ".KDDDDDDDDK.", "KDDdDDDdDDDK",
    "KDDDDDDDDDDK", ".KKKKKKKKKK.", "..KsK..KsK..", "..KBBK.KBBK.", "...KK...KK..",
]
CHAR_PAL = {
    "K": OUTL, "H": (92, 56, 36), "h": (128, 82, 52), "S": (240, 190, 150), "s": (206, 150, 112),
    "E": OUTL, "W": WHITE, "N": (48, 64, 110), "n": (34, 46, 82), "T": (200, 50, 60),
    "B": (30, 24, 28), "P": (40, 52, 92), "R": (126, 40, 70), "r": (160, 62, 96),
    "L": (200, 40, 70), "D": PINK, "d": ROSE, "w": WHITE,
}


def character(rows, x, y):
    shadow(x + 5, y + 20, 5, 2)
    sprite(rows, x, y, CHAR_PAL)


# ================= compose the scene =================
grass(0, 0, W, H)

# reception plaza
PX0, PX1, PY0, PY1 = 40, 440, 34, 150
pavers(PX0, PY0, PX1, PY1)
# red carpet from parking to the arch
rect(222, 24, 36, 136, RED)
rect(224, 24, 32, 136, (196, 58, 76))
for yy in range(24, 160):
    put(224, yy, GOLD); put(255, yy, GOLD)
# sidewalk + curb between plaza and parking
pavers(0, 150, W, 162, t=8)
curb(0, W, 162)
# parking lot
asphalt(0, 168, W, H)
for i in range(17):  # parking bays
    x = 6 + i * 28
    rect(x, 170, 2, 40, (230, 230, 220))
rect(0, 210, W, 2, (230, 230, 220))
for x in range(10, W, 24):  # lane dashes
    rect(x, 240, 10, 2, (236, 200, 90))
rect(0, 266, W, 4, CURB_FRONT)

# hedges framing the plaza (gap in the middle for the carpet)
hedge(8, 34, 40, 12); hedge(446, 472, 40, 12)
hedge(40, 200, 140, 9); hedge(280, 440, 140, 9)
hedge(8, 34, 90, 12); hedge(446, 472, 90, 12)

# ---- objects sorted by their base (y), back to front ----
objects = [
    (70, lambda: flower_arch(217, 24)),
    (70, lambda: light_pole(60, 70)), (70, lambda: light_pole(420, 70)),
    (60, lambda: welcome_sign(176, 44)),
    (60, lambda: gift_table(282, 52)),
    (78, lambda: cocktail_table(80, 64)), (78, lambda: cocktail_table(370, 64)),
    (118, lambda: cocktail_table(120, 104)), (118, lambda: cocktail_table(330, 104)),
    (72, lambda: potted_plant(196, 64)), (72, lambda: potted_plant(276, 64)),
    (106, lambda: character(PLAYER, 236, 86)),
    (100, lambda: character(AUNT, 150, 80)), (120, lambda: character(AUNT, 300, 100)),
    (208, lambda: car(13, 176, (200, 60, 60), (150, 40, 44))),
    (208, lambda: car(69, 176, (230, 230, 226), (176, 176, 172))),
    (208, lambda: car(153, 176, (70, 110, 180), (48, 78, 132))),
    (208, lambda: car(321, 176, (60, 60, 68), (40, 40, 46))),
    (208, lambda: car(405, 176, (226, 200, 120), (176, 150, 84))),
    (166, lambda: lamp_post(110, 166)), (166, lambda: lamp_post(370, 166)),
    (262, lambda: car(97, 236, (120, 170, 120), (84, 126, 84))),
    (262, lambda: car(265, 236, (220, 220, 220), (170, 170, 170))),
]
for _, draw in sorted(objects, key=lambda o: o[0]):
    draw()

# string lights over the plaza (drawn last, they hang above everything)
light_pole_tops = [(60, 26), (420, 26)]
string_lights(61, 218, 27, 10)
string_lights(263, 421, 27, 10)

img.save(os.path.join(OUT, "style_sample_native.png"))
img.resize((W * 4, H * 4), Image.NEAREST).save(os.path.join(OUT, "style_sample_x4.png"))
print("done")
