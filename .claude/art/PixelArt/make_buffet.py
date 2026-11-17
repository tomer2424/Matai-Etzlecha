import os
import random
import sys
from PIL import Image

# Buffet island preview: wooden deck with 3 buffet stations (hot food, salads, desserts - the last one EMPTY),
# string lights, cocktail tables, player + aunts at the 16x24 character size. 3/4 view, 16 px tiles.
# Native 480x270 (one screen), also saved x4. Usage: python make_buffet.py <output_dir>
random.seed(7)
W, H = 480, 270
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
img = Image.new("RGB", (W, H))
P = img.load()

# ---------- palette (same warm palette as the style sample) ----------
OUTL = (38, 26, 34)
GRASS = [(86, 140, 62), (98, 154, 68), (112, 168, 74), (74, 124, 56)]
WOOD = [(178, 126, 84), (166, 116, 76), (190, 138, 94)]
WOOD_GAP, WOOD_FRONT = (112, 74, 50), (126, 84, 56)
HEDGE_TOP, HEDGE_MID, HEDGE_DARK = (92, 150, 70), (66, 118, 54), (44, 86, 44)
WHITE, CREAM, CREAM_D = (246, 244, 236), (226, 220, 206), (204, 196, 180)
GOLD, GOLD_D = (230, 186, 80), (176, 132, 52)
PINK, PINK_D, ROSE = (240, 120, 160), (196, 80, 124), (250, 190, 210)
RED = (200, 56, 60)
LAMP = (255, 226, 140)
METAL, METAL_L, METAL_D = (168, 174, 184), (214, 220, 228), (120, 126, 138)
SALAD, SALAD_D = (110, 176, 70), (70, 132, 52)
HUMMUS, OIL = (226, 196, 140), (196, 176, 60)
PITA, PITA_D, BASKET, BASKET_D = (232, 204, 150), (204, 168, 112), (160, 108, 60), (118, 76, 42)
MEAT, MEAT_D = (150, 78, 44), (110, 52, 30)
CHOC = (110, 64, 44)
HEAL = (120, 230, 120)


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


def ellipse_blend(cx, cy, rx, ry, c, a):
    for yy in range(cy - ry, cy + ry + 1):
        for xx in range(cx - rx, cx + rx + 1):
            if ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1:
                blend(xx, yy, c, a)


def shadow(cx, cy, rx, ry, a=0.35):
    ellipse_blend(cx, cy, rx, ry, (20, 16, 30), a)


def glow(cx, cy, r, c=LAMP, a=0.25):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
            if d <= r:
                blend(xx, yy, c, a * (1 - d / r))


def rrect(x, y, w, h, c, r=2):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            cx = min(xx - x, x + w - 1 - xx)
            cy = min(yy - y, y + h - 1 - yy)
            if cx + cy >= r:
                put(xx, yy, c)


def lighten(c, v):
    return tuple(max(0, min(255, a + v)) for a in c)


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
    for _ in range((x1 - x0) * (y1 - y0) // 40):
        x, y = random.randint(x0, x1 - 1), random.randint(y0 + 1, y1 - 1)
        put(x, y, GRASS[2]); put(x, y - 1, GRASS[2]); put(x + 1, y, GRASS[3])
    for _ in range((x1 - x0) * (y1 - y0) // 400):
        put(random.randint(x0, x1 - 1), random.randint(y0, y1 - 1), random.choice([WHITE, LAMP, ROSE]))


def deck(x0, y0, x1, y1):
    """Wooden deck: horizontal planks (6 px), staggered seams, darker front face (3/4 view)."""
    for y in range(y0, y1):
        row = (y - y0) // 6
        for x in range(x0, x1):
            plank_len = 40
            off = (row * 17) % plank_len
            if (y - y0) % 6 == 5 or (x - x0 + off) % plank_len == 0:
                put(x, y, WOOD_GAP)
            else:
                c = WOOD[((x - x0 + off) // plank_len + row) % 3]
                if (y - y0) % 6 == 0:
                    c = lighten(c, 12)
                if random.random() < 0.04:
                    c = lighten(c, -14)  # wood grain
                put(x, y, c)
    rect(x0, y1, x1 - x0, 4, WOOD_FRONT)            # front face
    rect(x0, y1 + 4, x1 - x0, 1, OUTL)
    for yy in range(y0, y1 + 4):
        put(x0 - 1, yy, OUTL); put(x1, yy, OUTL)
    rect(x0 - 1, y0 - 1, x1 - x0 + 2, 1, OUTL)
    for x in range(x0, x1):
        blend(x, y1 + 5, (20, 16, 30), 0.3)


def confetti(x0, y0, x1, y1, n):
    for _ in range(n):
        put(random.randint(x0, x1), random.randint(y0, y1), random.choice([PINK, GOLD, WHITE, ROSE, (120, 180, 230)]))


def napkin(x, y):
    rect(x, y, 3, 2, WHITE); put(x + 1, y + 2, CREAM_D); put(x + 3, y + 1, CREAM_D)


# ---------- buffet ----------
def buffet_table(x, y, w):
    """Long table, 3/4 view: white top (10 px deep) + cream skirt with pleats (12 px tall)."""
    shadow(x + w // 2, y + 23, w // 2 + 3, 3)
    rect(x - 1, y - 1, w + 2, 24, OUTL)
    rect(x, y, w, 10, WHITE)
    rect(x, y + 8, w, 2, CREAM)                     # front edge of the top
    rect(x, y + 10, w, 12, CREAM)
    for xx in range(x + 2, x + w - 1, 4):            # pleats
        rect(xx, y + 11, 1, 11, CREAM_D)
    rect(x, y + 10, w, 1, GOLD)                      # gold trim
    for xx in range(x + 1, x + w - 1, 8):            # little swags
        put(xx + 3, y + 11, GOLD_D); put(xx + 4, y + 12, GOLD_D); put(xx + 5, y + 11, GOLD_D)


def chafer(x, y, full=True):
    """Chafing dish (16x8). Full = closed silver lid with steam. Empty = open tray with crumbs."""
    rect(x + 1, y + 7, 2, 2, OUTL); rect(x + 13, y + 7, 2, 2, OUTL)   # legs
    if full:
        rrect(x, y, 16, 8, OUTL, 2)
        rrect(x + 1, y + 1, 14, 6, METAL, 2)
        rect(x + 2, y + 5, 12, 1, METAL_D)
        rect(x + 4, y + 1, 7, 1, METAL_L); put(x + 3, y + 2, WHITE); put(x + 4, y + 2, METAL_L)
        rect(x + 7, y - 1, 2, 1, OUTL)                                 # lid handle
        for i in range(4):                                             # steam
            sx = x + 5 + i * 2 + random.randint(-1, 1)
            for k in range(2 + i % 2):
                blend(sx + (k % 2), y - 3 - k * 2, WHITE, 0.55)
    else:
        rrect(x, y + 2, 16, 6, OUTL, 2)
        rrect(x + 1, y + 3, 14, 4, METAL_D, 1)
        rect(x + 2, y + 4, 12, 2, (92, 92, 100))
        for _ in range(5):                                             # crumbs
            put(random.randint(x + 3, x + 12), random.randint(y + 4, y + 5), random.choice([MEAT, PITA_D]))
        rect(x + 2, y + 3, 12, 1, METAL_L)


def bowl(x, y, fill, dots, empty=False):
    rrect(x, y, 12, 7, OUTL, 2)
    rrect(x + 1, y + 1, 10, 5, WHITE, 1)
    if empty:
        rect(x + 2, y + 2, 8, 2, CREAM_D)
        put(x + 4, y + 3, fill); put(x + 7, y + 2, fill)
        return
    rect(x + 2, y + 1, 8, 3, fill)
    rect(x + 3, y, 6, 1, fill)                       # heaped
    for _ in range(4):
        put(random.randint(x + 3, x + 8), random.randint(y, y + 3), random.choice(dots))
    rect(x + 2, y + 4, 8, 1, CREAM_D)


def hummus(x, y):
    rrect(x, y, 12, 7, OUTL, 2)
    rrect(x + 1, y + 1, 10, 5, WHITE, 1)
    rrect(x + 2, y + 1, 8, 4, HUMMUS, 1)
    rect(x + 5, y + 2, 3, 2, OIL)
    put(x + 6, y + 2, RED); put(x + 3, y + 2, SALAD_D); put(x + 8, y + 3, SALAD_D)


def pita_basket(x, y):
    for i, (px, py) in enumerate([(x + 1, y - 2), (x + 5, y - 3), (x + 8, y - 2)]):  # pitas sticking out
        rrect(px, py, 6, 5, OUTL, 2)
        rrect(px + 1, py + 1, 4, 3, PITA if i != 1 else lighten(PITA, 10), 1)
    rect(x, y + 1, 14, 6, OUTL)
    rect(x + 1, y + 2, 12, 4, BASKET)
    for xx in range(x + 1, x + 13):
        if (xx - x) % 3 == 0:
            rect(xx, y + 2, 1, 4, BASKET_D)
    rect(x + 1, y + 2, 12, 1, lighten(BASKET, 20))


def skewers(x, y):
    rrect(x, y, 18, 7, OUTL, 2)
    rrect(x + 1, y + 1, 16, 5, WHITE, 1)
    for k in range(3):
        yy = y + 2 + k
        for i in range(12):
            c = [MEAT, MEAT_D, RED, (90, 150, 60)][(i // 2 + k) % 4]
            put(x + 3 + i, yy, c)
        put(x + 2, yy, CREAM_D); put(x + 15, yy, CREAM_D)


def plates_stack(x, y):
    for i in range(4):
        rrect(x, y + 4 - i * 2, 12, 5, OUTL, 2)
        rrect(x + 1, y + 5 - i * 2, 10, 3, WHITE, 1)
    rect(x + 2, y - 1, 8, 1, CREAM)


def cake(x, y, eaten=False):
    """Tiered wedding cake on a gold stand. Eaten = only the bottom tier, cut, with crumbs."""
    rect(x + 4, y + 13, 8, 2, GOLD_D); rect(x + 2, y + 15, 12, 1, OUTL)
    rect(x, y + 8, 16, 6, OUTL); rect(x + 1, y + 9, 14, 4, WHITE); rect(x + 1, y + 9, 14, 1, PINK)
    if eaten:
        rect(x + 9, y + 9, 6, 4, CREAM_D)            # the missing slice
        rect(x + 9, y + 10, 1, 3, CHOC); rect(x + 9, y + 9, 1, 1, PINK)
        put(x + 12, y + 12, CHOC); put(x + 14, y + 11, PINK)
        return
    rect(x + 3, y + 3, 10, 6, OUTL); rect(x + 4, y + 4, 8, 4, WHITE); rect(x + 4, y + 4, 8, 1, PINK)
    rect(x + 5, y - 1, 6, 5, OUTL); rect(x + 6, y, 4, 3, WHITE)
    put(x + 7, y - 2, RED); put(x + 8, y - 2, RED); put(x + 8, y - 3, (90, 150, 60))
    for xx in (x + 2, x + 6, x + 10, x + 13):
        put(xx, y + 11, ROSE)


def cupcakes(x, y, n=3):
    for i in range(n):
        cx = x + i * 6
        rect(cx, y + 3, 5, 3, OUTL); rect(cx + 1, y + 3, 3, 2, CHOC)
        rrect(cx, y, 5, 4, PINK if i % 2 == 0 else WHITE, 1); put(cx + 2, y, RED)


def fruit_bowl(x, y, empty=False):
    rrect(x, y + 2, 14, 6, OUTL, 2); rrect(x + 1, y + 3, 12, 4, WHITE, 1)
    if empty:
        put(x + 5, y + 4, (130, 70, 140)); put(x + 8, y + 4, (130, 70, 140))  # 2 lonely grapes
        return
    for i, c in enumerate([(240, 150, 40), (130, 70, 140), (210, 50, 60), (240, 210, 70), (130, 190, 70)]):
        rrect(x + 1 + i * 2 + (i % 2), y - (i % 2) * 2 + 1, 4, 4, c, 1)


def tent_card(x, y, color):
    rect(x, y, 8, 5, OUTL); rect(x + 1, y + 1, 6, 3, WHITE); rect(x + 2, y + 2, 4, 1, color)


def awning(x, y, w, color, dim=False):
    """Striped market-style awning above a station (3/4 view): canopy top + scalloped valance + 2 poles.
    dim=True = the station is empty (washed-out colours)."""
    if dim:
        color = tuple(int(c * 0.55 + 150 * 0.45) for c in color)
    white = WHITE if not dim else (214, 210, 202)
    for xx in (x + 2, x + w - 4):                      # poles down to the table
        rect(xx, y + 12, 2, 26, (110, 84, 64)); put(xx - 1, y + 12, OUTL)
    rect(x - 1, y - 1, w + 2, 11, OUTL)
    for xx in range(x, x + w):
        c = color if ((xx - x) // 6) % 2 == 0 else white
        rect(xx, y, 1, 5, lighten(c, 18))              # sunlit top
        rect(xx, y + 5, 1, 4, c)
    for sx in range(x, x + w, 6):                      # scalloped valance
        c = color if ((sx - x) // 6) % 2 == 0 else white
        for i, wd in enumerate((6, 6, 4, 2)):
            off = (6 - wd) // 2
            rect(sx + off, y + 9 + i, min(wd, x + w - sx - off), 1, lighten(c, -16))
        put(sx, y + 10, OUTL); put(sx + 1, y + 12, OUTL); put(sx + 4, y + 12, OUTL)


def heal_ring(cx, cy):
    import math
    ellipse_blend(cx, cy, 38, 11, (70, 220, 100), 0.30)
    for t in range(0, 360, 6):  # bright edge of the healing area
        px = int(round(cx + 38 * math.cos(math.radians(t))))
        py = int(round(cy + 11 * math.sin(math.radians(t))))
        blend(px, py, (160, 255, 170), 0.85)


def plus(x, y, a=0.95):
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1), (-2, 0), (2, 0), (0, -2), (0, 2)]:
        blend(x + dx, y + dy, (70, 210, 90), a)
    for dx, dy in [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]:
        blend(x + dx, y + dy, (200, 255, 200), a * 0.8)


# ---------- decor props ----------
def light_pole(x, y):
    rect(x, y - 44, 2, 45, (90, 70, 56))
    rect(x - 1, y, 4, 1, OUTL)
    shadow(x + 1, y + 1, 3, 1)


def string_lights(x0, x1, y, sag=6):
    n = x1 - x0
    for i in range(n):
        t = i / n
        yy = int(y + sag * 4 * t * (1 - t))
        put(x0 + i, yy, OUTL)
        if i % 6 == 3:
            put(x0 + i, yy + 1, LAMP); put(x0 + i, yy + 2, LAMP)
            glow(x0 + i, yy + 2, 5, a=0.25)


def potted_plant(x, y):
    shadow(x + 5, y + 14, 7, 2)
    rect(x + 1, y + 7, 9, 7, (186, 98, 64)); rect(x + 1, y + 7, 9, 1, (214, 128, 86))
    rect(x + 1, y + 14, 9, 1, OUTL)
    for yy in range(y + 7, y + 14):
        put(x, yy, OUTL); put(x + 10, yy, OUTL)
    for yy in range(y - 3, y + 7):
        for xx in range(x - 1, x + 12):
            dx, dy = (xx - (x + 5)) / 6.5, (yy - (y + 2)) / 5.5
            if dx * dx + dy * dy <= 1:
                c = HEDGE_TOP if dy < -0.2 else HEDGE_MID
                put(xx, yy, c if random.random() < 0.8 else HEDGE_DARK)


def cocktail_table(x, y):
    shadow(x + 8, y + 19, 9, 3)
    rows = [(1, 15), (2, 13), (3, 11), (5, 7), (5, 7), (5, 7), (5, 7), (4, 9), (3, 11), (2, 13), (1, 15), (1, 15)]
    for i, (o, w) in enumerate(rows):
        rect(x + o, y + 6 + i, w, 1, CREAM)
        put(x + o - 1, y + 6 + i, OUTL); put(x + o + w, y + 6 + i, OUTL)
        put(x + 8, y + 6 + i, CREAM_D)
    rect(x + 5, y + 9, 7, 1, GOLD)
    rect(x, y + 18, 17, 1, OUTL)
    rrect(x - 1, y - 1, 19, 8, OUTL, 2)
    rrect(x, y, 17, 6, WHITE, 2)
    put(x + 8, y + 1, PINK); put(x + 7, y + 2, ROSE); put(x + 9, y + 2, PINK); put(x + 8, y + 3, (120, 170, 90))


def chalk_sign(x, y):
    """A-frame chalkboard with pretend writing and a little fork+knife."""
    shadow(x + 8, y + 22, 9, 2)
    rect(x + 2, y + 14, 2, 8, (110, 74, 48)); rect(x + 12, y + 14, 2, 8, (110, 74, 48))
    rect(x, y, 16, 16, OUTL)
    rect(x + 1, y + 1, 14, 14, (140, 96, 60))
    rect(x + 2, y + 2, 12, 12, (52, 62, 58))
    for i, wdt in enumerate((8, 10, 6)):
        for xx in range(x + 3 + (10 - wdt) // 2, x + 3 + (10 - wdt) // 2 + wdt):
            if (xx + i) % 3:
                put(xx, y + 4 + i * 3, (220, 224, 214))
    rect(x + 6, y + 12, 1, 2, GOLD); rect(x + 9, y + 12, 1, 2, GOLD)


# ---------- characters (16x24, front view, scale reference) ----------
PLAYER = [
    "....KKKKKKK.....", "...KHHHHhHHK....", "..KHHHHHHHHHK...", "..KHHSSSSSHHK...",
    "..KHSSSSSSSHK...", "..KSSESSSESSK...", "..KSSSSSSSSsK...", "..KSSSKKSSSsK...",
    "...KSSSSSSsK....", "....KKSSSKK.....", "..KKNNWTWNNKK...", ".KNNNNWTWNNNNK..",
    ".KNNNNNTNNNNNK..", ".KNNNNNTNNNNNK..", ".KSKNNNNNNNKSK..", ".KSKNNNNNNNKSK..",
    "..KKnNNNNNnKK...", "...KPPPKPPPK....", "...KPPPKPPPK....", "...KPPPKPPPK....",
    "...KPPPKPPPK....", "...KPPPKPPPK....", "..KBBBK.KBBBK...", "..KKKK...KKKK...",
]
AUNT = [
    ".....KKKK.......", "....KRRrRK......", "...KKRRRRKK.....", "..KRRrRRRrRK....",
    ".KRRRRRRRRRRK...", ".KRRSSSSSSRRK...", ".KRSSSSSSSSRK...", ".KRSESSSSESRK...",
    ".KRSSSSSSSSRK...", "..KSSSLLSSsK....", "...KKSSSSKK.....", "..KDwwwwwwDK....",
    ".KDDDDDDDDDDK...", ".KSDDDDDDDDSK...", ".KSDDdDDdDDSK...", "..KDDDDDDDDK....",
    "..KDDdDDdDDDK...", ".KDDDDDDDDDDDK..", ".KDDDdDDDdDDDK..", "KDDDDDDDDDDDDDK.",
    ".KKKKKKKKKKKKK..", "...KsK...KsK....", "...KBBK..KBBK...", "....KK....KK....",
]
CHAR_PAL = {
    "K": OUTL, "H": (92, 56, 36), "h": (128, 82, 52), "S": (240, 190, 150), "s": (206, 150, 112),
    "E": OUTL, "W": WHITE, "N": (48, 64, 110), "n": (34, 46, 82), "T": (200, 50, 60),
    "B": (30, 24, 28), "P": (40, 52, 92), "R": (126, 40, 70), "r": (160, 62, 96),
    "L": (200, 40, 70), "D": PINK, "d": ROSE, "w": WHITE,
}


def recolor(pal, dress, dress_l, hair, hair_l):
    p = dict(pal)
    p.update({"D": dress, "d": dress_l, "R": hair, "r": hair_l})
    return p


def character(rows, x, y, pal=CHAR_PAL):
    shadow(x + 7, y + 24, 6, 2)
    sprite(rows, x, y, pal)


# ================= compose =================
grass(0, 0, W, H)
confetti(0, 0, W, H, 60)
for nx, ny in [(18, 40), (452, 70), (30, 236), (446, 250), (250, 258)]:
    napkin(nx, ny)

DX0, DX1, DY0, DY1 = 72, 408, 70, 234
deck(DX0, DY0, DX1, DY1)
confetti(DX0 + 4, DY0 + 4, DX1 - 4, DY1 - 4, 30)

# healing area under the hot-food station (the player stands in it)
T1, T2, T3, TY, TW = 96, 204, 312, 108, 72
heal_ring(T1 + TW // 2, TY + 38)

objects = []

# station 1: hot food (FULL)
objects.append((TY + 22, lambda: (awning(T1 - 4, TY - 34, TW + 8, (200, 56, 60)), buffet_table(T1, TY, TW),
                                  plates_stack(T1 + 2, TY - 2),
                                  chafer(T1 + 16, TY - 2), chafer(T1 + 34, TY - 2),
                                  skewers(T1 + 52, TY + 1) if TW >= 72 else None,
                                  tent_card(T1 + 36, TY + 6, RED))))
# station 2: salads (FULL)
objects.append((TY + 22, lambda: (awning(T2 - 4, TY - 34, TW + 8, (90, 160, 70)), buffet_table(T2, TY, TW),
                                  bowl(T2 + 3, TY, SALAD, [RED, (240, 150, 40), WHITE]),
                                  hummus(T2 + 18, TY + 1),
                                  pita_basket(T2 + 33, TY),
                                  bowl(T2 + 50, TY, (200, 60, 70), [WHITE, SALAD_D]),   # beet / tomato salad
                                                                    tent_card(T2 + 36, TY + 6, SALAD_D))))
# station 3: desserts (EMPTY - already eaten, needs to refill)
objects.append((TY + 22, lambda: (awning(T3 - 4, TY - 34, TW + 8, (230, 120, 160), dim=True), buffet_table(T3, TY, TW),
                                  cake(T3 + 4, TY - 8, eaten=True),
                                  chafer(T3 + 24, TY - 2, full=False),
                                  fruit_bowl(T3 + 44, TY - 1, empty=True),
                                  bowl(T3 + 58, TY, PINK, [], empty=True),
                                  tent_card(T3 + 36, TY + 6, PINK))))

# a full dessert table preview on the side? no - keep the island to 3 stations (Balance.md)
objects += [
    (DY0 + 4, lambda: light_pole(DX0 + 6, DY0 + 4)), (DY0 + 4, lambda: light_pole(DX1 - 8, DY0 + 4)),
    (DY0 + 92, lambda: potted_plant(DX0 + 8, DY0 + 78)), (DY0 + 92, lambda: potted_plant(DX1 - 20, DY0 + 78)),
    (DY1 - 6, lambda: potted_plant(DX0 + 12, DY1 - 20)), (DY1 - 6, lambda: potted_plant(DX1 - 24, DY1 - 20)),
    (196, lambda: cocktail_table(150, 177)), (204, lambda: cocktail_table(318, 185)),
    (244, lambda: chalk_sign(232, 222)),
    # player healing in front of the hot food
    (TY + 52, lambda: character(PLAYER, T1 + 33, TY + 28)),
    # aunts coming for him
    (178, lambda: character(AUNT, 250, 154)),
    (128, lambda: character(AUNT, 444, 120, recolor(CHAR_PAL, (110, 170, 210), (170, 210, 235), (60, 40, 30), (96, 64, 44)))),
    (250, lambda: character(AUNT, 28, 226, recolor(CHAR_PAL, (150, 110, 190), (196, 166, 222), (170, 170, 176), (210, 210, 214)))),
    (222, lambda: character(AUNT, 352, 196, recolor(CHAR_PAL, (230, 170, 60), (246, 210, 120), (126, 40, 70), (160, 62, 96)))),
]
for _, draw in sorted(objects, key=lambda o: o[0]):
    draw()

# healing "+" particles rising from the player
for px, py, a in [(T1 + 30, TY + 30, 0.95), (T1 + 52, TY + 26, 0.85), (T1 + 44, TY + 22, 0.7), (T1 + 26, TY + 20, 0.55)]:
    plus(px, py, a)

# string lights between the poles (hang above everything)
string_lights(DX0 + 7, DX1 - 7, DY0 - 40, 10)

img.save(os.path.join(OUT, "buffet_native.png"))
img.resize((W * 4, H * 4), Image.NEAREST).save(os.path.join(OUT, "buffet_x4.png"))
print("done")
