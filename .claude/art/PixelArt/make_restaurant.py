import os
import random
import sys
from PIL import Image, ImageDraw

# Restaurant theme style sample: chef (player), living pizza slices (basic enemy, 3 toppings),
# a thrown knife (first weapon), a tip coin (XP) and a corner of the restaurant floor.
# Same pixel-art rules as make_characters.py: PPU 16, 16x24 character frames, FACING LEFT,
# dark auto outline, light from the top-left, 3/4 view.
# Outputs (in <output_dir>):
#   Chef_sheet.png, Pizza_<topping>_sheet.png   4 frames of 16x24: idle, walk1, walk2, hit / give-up
#   Knife.png  13x6, points RIGHT (rotate it toward the flight direction in Unity)
#   Coin.png   7x7
#   restaurant_characters_x8.png   all frames enlarged with labels
#   restaurant_sample_native.png / restaurant_sample_x4.png   a 480x270 scene (one screen at PPU 16)
# Usage: python make_restaurant.py <output_dir>
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
random.seed(7)
FW, FH = 16, 24

OUTL = (38, 26, 34)
SKIN, SKIN_D = (240, 190, 150), (206, 150, 112)
EYE = (38, 26, 34)
WHITE = (250, 250, 246)


class Frame:
    def __init__(self, w=FW, h=FH):
        self.w, self.h = w, h
        self.px = {}
        self.over = {}   # drawn after the outline, so they stay 1 px thin

    def over_line(self, x0, y0, x1, y1, c):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            t = i / steps
            x, y = round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t)
            if 0 <= x < self.w and 0 <= y < self.h and (x, y) not in self.px:
                self.over[(x, y)] = c

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            self.px[(x, y)] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, c)

    def line(self, x0, y0, x1, y1, c):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(steps + 1):
            t = i / steps
            self.put(round(x0 + (x1 - x0) * t), round(y0 + (y1 - y0) * t), c)

    def grid(self, rows, x0, y0, pal):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != ".":
                    self.put(x0 + i, y0 + j, pal[ch])

    def image(self):
        im = Image.new("RGBA", (self.w, self.h), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            im.putpixel((x, y), tuple(c[:3]) + (255,))
        # automatic outline: every empty pixel touching a filled pixel (4 directions)
        filled = set(self.px)
        for (x, y) in list(filled):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.w and 0 <= ny < self.h and (nx, ny) not in filled:
                    im.putpixel((nx, ny), OUTL + (255,))
        for (x, y), c in self.over.items():
            im.putpixel((x, y), tuple(c[:3]) + (255,))
        return im


def leg(f, hip_x, hip_y, foot_dx, color, shoe, length=5):
    """2 px wide leg from the hip to the foot, shoe points left."""
    for i in range(length):
        t = i / (length - 1)
        f.rect(hip_x + round(foot_dx * t), hip_y + i, 2, 1, color)
    fx = hip_x + foot_dx
    f.rect(fx - 1, hip_y + length, 3, 1, shoe)
    f.put(fx - 1, hip_y + length, tuple(min(255, c + 30) for c in shoe))


def arm(f, sx, sy, hx, hy, sleeve, hand=SKIN):
    steps = max(abs(hx - sx), abs(hy - sy))
    for i in range(steps):
        t = i / steps
        f.put(round(sx + (hx - sx) * t), round(sy + (hy - sy) * t), sleeve)
        f.put(round(sx + (hx - sx) * t) + 1, round(sy + (hy - sy) * t), sleeve)
    f.put(hx, hy, hand); f.put(hx + 1, hy, hand)


def sheet(frames):
    im = Image.new("RGBA", (FW * len(frames), FH), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        im.paste(fr, (i * FW, 0))
    return im


# =============================== CHEF (player) ===============================
HAT, HAT_D = (252, 252, 248), (210, 208, 204)
JACKET, JACKET_D = (246, 244, 238), (204, 200, 192)
SCARF, SCARF_D = (210, 52, 56), (160, 34, 44)
BUTTON = (120, 120, 132)
PANTS, PANTS_L, PANTS_FAR = (62, 62, 74), (96, 96, 110), (44, 44, 54)
CHEF_SHOES = (34, 30, 36)
CP = {"T": HAT, "t": HAT_D, "S": SKIN, "s": SKIN_D, "E": EYE, "e": SKIN_D,
      "H": (92, 56, 36), "h": (128, 82, 52), "m": (92, 56, 36), "M": (150, 60, 60)}

CHEF_HEAD = [
    "..TTTTt...",
    ".TTTTTTTt.",
    ".TTTTTTTTt",
    "..TTTTTTt.",
    "..ttttttt.",
    ".SSSSSsHh.",
    ".SESSSeHh.",
    "SSESSSsHh.",
    ".mmmSssH..",
    "..SSSs....",
]
# hit: eyes squeezed shut, mouth open under the moustache
CHEF_HEAD_HIT = CHEF_HEAD[:6] + [".SsSSSeHh.", "SSsSSSsHh.", ".mmmSssH..", "..MMSs...."]


def chef(kind):
    f = Frame()
    bob = 1 if kind == "walk1" else 0
    legs = {"idle": (0, 0), "walk1": (-2, 2), "walk2": (2, -2), "hit": (1, 0)}[kind]
    lean = 1 if kind == "hit" else 0
    leg(f, 8 + lean, 17 + bob, legs[1], PANTS_FAR, CHEF_SHOES, length=5 - bob)
    leg(f, 6 + lean, 17 + bob, legs[0], PANTS, CHEF_SHOES, length=5 - bob)
    # checked (houndstooth-like) trousers
    for (x, y), c in list(f.px.items()):
        if c == PANTS and (x + y) % 2 == 0:
            f.px[(x, y)] = PANTS_L
    # far arm behind the body
    if kind == "hit":
        arm(f, 9 + lean, 12, 11 + lean, 9, JACKET_D)
    else:
        f.rect(10 + lean, 12 + bob, 1, 4, JACKET_D)
    # double-breasted white jacket with a red neckerchief
    f.rect(5 + lean, 11 + bob, 6, 6, JACKET)
    f.rect(10 + lean, 11 + bob, 1, 6, JACKET_D)       # shaded back edge
    f.rect(5 + lean, 16 + bob, 6, 1, JACKET_D)        # hem
    f.rect(5 + lean, 11 + bob, 3, 1, SCARF)
    f.put(5 + lean, 12 + bob, SCARF_D)
    for by in (13, 15):                               # two rows of buttons
        f.put(6 + lean, by + bob, BUTTON)
        f.put(8 + lean, by + bob, BUTTON)
    swing = {"idle": 0, "walk1": 2, "walk2": -2, "hit": 0}[kind]
    if kind != "hit":
        arm(f, 7 + lean, 12 + bob, 7 + lean - swing // 2 + (1 if swing < 0 else 0), 16 + bob, JACKET_D)
    f.grid(CHEF_HEAD_HIT if kind == "hit" else CHEF_HEAD, 3 + lean, 1 + bob, CP)
    if kind == "hit":
        arm(f, 6 + lean, 12, 3 + lean, 10, JACKET_D)  # hands up in shock
        f.put(14, 6, (150, 200, 240)); f.put(14, 7, (150, 200, 240))
    return f.image()


# =============================== PIZZA (basic enemy) ===============================
CRUST_L, CRUST, CRUST_D = (238, 188, 108), (214, 150, 72), (168, 104, 46)
SAUCE = (204, 64, 44)
CHEESE_L, CHEESE, CHEESE_D = (255, 234, 142), (252, 206, 84), (226, 160, 52)
LIMB = (150, 90, 60)
SNEAKER = (236, 236, 232)
TONGUE = (220, 90, 100)
TOPPINGS = {
    # (x, y, pattern rows) relative to the slice tip (row 0); kept away from the face
    "pepperoni": [(7, 2, ["Pp", "PP"]), (10, 8, ["Pp", "PP"]), (9, 4, ["P"])],
    "margherita": [(7, 2, ["W"]), (8, 3, ["B"]), (10, 8, ["Ww"]), (10, 9, [".B"]), (9, 4, ["W"])],
    "veggie": [(7, 2, ["Oo"]), (10, 8, ["G."]), (10, 9, [".G"]), (9, 4, ["R"])],
}
TOP_PAL = {"P": (180, 46, 42), "p": (224, 92, 72), "W": (250, 248, 238), "w": (220, 216, 204),
           "B": (70, 150, 60), "O": (46, 38, 46), "o": (96, 86, 96), "G": (96, 176, 70), "R": (220, 60, 50)}


def slice_width(i):
    """Width of the slice on row i (0 = tip at the top, 14 = crust at the bottom)."""
    return max(2, round(2 + i * 10 / 14))


def pizza(kind, topping):
    # Tip UP, wide crust at the BOTTOM: a stable base that matches a feet collider.
    f = Frame()
    y0 = {"idle": 4, "walk1": 3, "walk2": 4, "giveup": 5}[kind]   # walk1 = small hop, give-up = slumped
    edges = {}
    for i in range(15):
        w = slice_width(i)
        x0 = 8 - w // 2
        edges[i] = (x0, x0 + w - 1)
        y = y0 + i
        if i >= 12:  # crust (3 rows)
            c = (CRUST_L, CRUST, CRUST_D)[i - 12]
            f.rect(x0, y, w, 1, c)
        elif i == 11:
            f.rect(x0, y, w, 1, SAUCE)
        else:
            f.rect(x0, y, w, 1, CHEESE)
            f.put(x0, y, CHEESE_L)                 # lit left edge
            f.put(x0 + w - 1, y, CHEESE_D)         # shaded right edge
    f.put(edges[10][1], y0 + 10, SAUCE)             # sauce peeking out on the right
    if kind != "giveup":                            # melted cheese running over the crust
        f.put(10, y0 + 11, CHEESE); f.put(10, y0 + 12, CHEESE_D)
    for (tx, ty, rows) in TOPPINGS[topping]:
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != ".":
                    f.put(tx + i, y0 + ty + j, TOP_PAL[ch])
    # face (facing left), low on the slice where it is wide enough
    if kind == "giveup":
        f.put(5, y0 + 7, EYE); f.put(6, y0 + 7, EYE)     # eyes shut
        f.put(8, y0 + 7, EYE); f.put(9, y0 + 7, EYE)
        f.put(5, y0 + 10, EYE); f.put(6, y0 + 9, EYE); f.put(7, y0 + 10, EYE)  # wobbly mouth
        f.put(12, y0 + 1, (150, 200, 240)); f.put(12, y0 + 2, (150, 200, 240))  # sweat drop
    else:
        for ex in (6, 8):
            f.put(ex, y0 + 6, EYE); f.put(ex, y0 + 7, EYE)
        f.put(7, y0 + 5, CHEESE_D)                       # frown between the eyes
        f.rect(5, y0 + 9, 4, 1, EYE)                     # shouting mouth
        f.put(6, y0 + 10, EYE); f.put(7, y0 + 10, TONGUE)
    # rubber-hose arms from the wide lower part, legs from under the crust
    ay = y0 + 9
    lx, rx = edges[9]
    arm_pose = {"idle": (-2, -2, 2, 2), "walk1": (-3, -1, 2, 1), "walk2": (-2, -3, 2, 3), "giveup": (-2, 3, 2, 3)}[kind]
    f.over_line(lx - 1, ay, lx - 1 + arm_pose[0], ay + arm_pose[1], OUTL)
    f.over_line(rx + 1, ay, rx + 1 + arm_pose[2], ay + arm_pose[3], OUTL)
    f.put(lx - 1 + arm_pose[0], ay + arm_pose[1], SNEAKER)   # little white gloves
    f.put(rx + 1 + arm_pose[2], ay + arm_pose[3], SNEAKER)
    base = y0 + 15
    feet = {"idle": (-1, 1), "walk1": (-2, 2), "walk2": (0, 0), "giveup": (-1, 1)}[kind]
    foot_y = 21
    f.over_line(6, base + 1, 6 + feet[0], foot_y, OUTL)
    f.over_line(9, base + 1, 9 + feet[1], foot_y, OUTL)
    f.rect(5 + feet[0], foot_y + 1, 2, 1, SNEAKER)   # sneakers point left
    f.rect(9 + feet[1], foot_y + 1, 2, 1, SNEAKER)
    return f.image()


# =============================== KNIFE (projectile) + COIN (XP) ===============================
KNIFE = [
    ".....LLLLLL",
    "HHHHbBBBBBBL",
    "HrHrbBBBBBBBL",
    "HHHHbDDDDDD",
]
KNIFE_PAL = {"H": (70, 44, 36), "r": (210, 196, 170), "b": (150, 150, 162),
             "L": (238, 242, 248), "B": (196, 204, 216), "D": (140, 150, 166)}


def knife():
    f = Frame(15, 6)
    f.grid(KNIFE, 1, 1, KNIFE_PAL)
    return f.image()


COIN = [".YYY.", "YLLYD", "YLYYD", "YYYDD", ".DDD."]
COIN_PAL = {"Y": (246, 196, 64), "L": (255, 238, 150), "D": (198, 136, 40)}


def coin():
    f = Frame(7, 7)
    f.grid(COIN, 1, 1, COIN_PAL)
    return f.image()


# ---------- build the sprites ----------
chef_frames = [chef(k) for k in ("idle", "walk1", "walk2", "hit")]
sheet(chef_frames).save(os.path.join(OUT, "Chef_sheet.png"))
pizza_frames = {}
for t in TOPPINGS:
    pizza_frames[t] = [pizza(k, t) for k in ("idle", "walk1", "walk2", "giveup")]
    sheet(pizza_frames[t]).save(os.path.join(OUT, f"Pizza_{t}_sheet.png"))
knife_im = knife()
knife_im.save(os.path.join(OUT, "Knife.png"))
coin_im = coin()
coin_im.save(os.path.join(OUT, "Coin.png"))

# =============================== SCENE ===============================
W, H = 480, 270
img = Image.new("RGB", (W, H))
P = img.load()


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        P[x, y] = c


def rect(x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            put(xx, yy, c)


def border(x, y, w, h, c=OUTL):
    rect(x - 1, y - 1, w + 2, 1, c); rect(x - 1, y + h, w + 2, 1, c)
    rect(x - 1, y, 1, h, c); rect(x + w, y, 1, h, c)


def blend(x, y, c, a):
    if 0 <= x < W and 0 <= y < H:
        o = P[x, y]
        P[x, y] = tuple(int(o[i] * (1 - a) + c[i] * a) for i in range(3))


def ellipse(cx, cy, rx, ry, c, a=1.0):
    for yy in range(cy - ry, cy + ry + 1):
        for xx in range(cx - rx, cx + rx + 1):
            if ((xx - cx) / max(rx, 0.5)) ** 2 + ((yy - cy) / max(ry, 0.5)) ** 2 <= 1:
                if a >= 1:
                    put(xx, yy, c)
                else:
                    blend(xx, yy, c, a)


def shadow(cx, cy, rx, ry, a=0.35):
    ellipse(cx, cy, rx, ry, (20, 16, 30), a)


def glow(cx, cy, r, a=0.22):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            d = ((xx - cx) ** 2 + (yy - cy) ** 2) ** 0.5
            if d <= r:
                blend(xx, yy, (255, 226, 150), a * (1 - d / r))


def paste(sprite, x, y):
    """Paste an RGBA sprite with its top-left at (x, y)."""
    for j in range(sprite.height):
        for i in range(sprite.width):
            c = sprite.getpixel((i, j))
            if c[3] > 0:
                put(x + i, y + j, c[:3])


# ---------- floors ----------
WOOD = [(178, 118, 70), (168, 110, 64), (188, 128, 78)]
WOOD_SEAM = (122, 76, 44)


def wood_floor(x0, y0, x1, y1, ph=6):
    for r, y in enumerate(range(y0, y1, ph)):
        x = x0 - random.randint(0, 30)
        while x < x1:
            L = random.choice([44, 52, 60])
            base = random.choice(WOOD)
            for yy in range(y, min(y + ph - 1, y1)):
                for xx in range(max(x, x0), min(x + L - 1, x1)):
                    c = base
                    if yy == y:
                        c = tuple(min(255, v + 12) for v in base)   # lit top edge of the plank
                    elif random.random() < 0.06:
                        c = tuple(v - 14 for v in base)              # grain
                    put(xx, yy, c)
            if x0 <= x + L - 1 < x1:
                rect(x + L - 1, y, 1, ph - 1, WOOD_SEAM)
            x += L
        rect(x0, y + ph - 1, x1 - x0, 1, WOOD_SEAM)


TILE_W, TILE_D = (230, 224, 210), (72, 76, 92)


def checker(x0, y0, x1, y1, t=8):
    for y in range(y0, y1):
        for x in range(x0, x1):
            dark = ((x - x0) // t + (y - y0) // t) % 2
            c = TILE_D if dark else TILE_W
            if (x - x0) % t == 0 or (y - y0) % t == 0:
                c = tuple(min(255, v + 10) for v in c)
            put(x, y, c)


wood_floor(0, 0, W, H)
KX, KY = 300, 118   # kitchen zone: top-right corner
checker(KX, 0, W, KY)
rect(KX, KY, W - KX, 2, (176, 180, 190)); rect(KX, KY + 2, W - KX, 1, OUTL)    # steel floor strip
rect(KX - 2, 0, 2, KY + 2, (176, 180, 190)); rect(KX - 3, 0, 1, KY + 3, OUTL)

# warm pendant-light pools on the floor
for (gx, gy) in [(90, 175), (240, 150), (400, 205), (190, 60)]:
    glow(gx, gy, 46)

# ---------- furniture ----------
STEEL_L, STEEL, STEEL_D = (214, 218, 226), (176, 182, 194), (130, 136, 150)
CLOTH_R, CLOTH_W, CLOTH_RD, CLOTH_WD = (206, 58, 60), (248, 244, 236), (158, 40, 48), (206, 198, 190)
CHAIR_L, CHAIR, CHAIR_D = (150, 96, 56), (122, 74, 42), (88, 52, 30)


def counter(x, y, w, top_h, front_h, top, front, front_d):
    shadow(x + w // 2, y + top_h + front_h + 1, w // 2 + 2, 3)
    rect(x, y, w, top_h, top)
    rect(x, y, w, 1, tuple(min(255, v + 18) for v in top))
    rect(x, y + top_h, w, front_h, front)
    rect(x, y + top_h, w, 1, front_d)
    for px in range(x + 14, x + w - 4, 16):     # cabinet doors on the front
        rect(px, y + top_h + 2, 1, front_h - 3, front_d)
        put(px - 3, y + top_h + front_h // 2, STEEL_L)
    border(x, y, w, top_h + front_h)


def checked_cloth(x, y, w, h, light, dark):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            a = ((xx - x) // 3 + (yy - y) // 3) % 2
            put(xx, yy, dark if a else light)


def table(x, y, w=26, top_h=14, front_h=6):
    shadow(x + w // 2, y + top_h + front_h + 2, w // 2 + 3, 3)
    checked_cloth(x, y, w, top_h, CLOTH_W, CLOTH_R)
    checked_cloth(x, y + top_h, w, front_h, CLOTH_WD, CLOTH_RD)   # hanging front, in shade
    border(x, y, w, top_h + front_h)
    # plate + glass on top
    ellipse(x + 8, y + 6, 3, 2, (252, 252, 250)); ellipse(x + 8, y + 6, 1, 1, (226, 160, 52))
    rect(x + 17, y + 3, 2, 4, (190, 220, 236)); put(x + 17, y + 3, (240, 250, 255))


def chair(x, y, side):
    """3/4 chair next to a table; the back rest is on the outer side ('L' or 'R')."""
    shadow(x + 4, y + 12, 6, 2)
    rect(x, y + 5, 9, 3, CHAIR_L)           # seat top
    rect(x, y + 8, 9, 2, CHAIR_D)           # seat front
    rect(x + 1, y + 10, 1, 3, CHAIR_D); rect(x + 7, y + 10, 1, 3, CHAIR_D)   # legs
    bx = x if side == "L" else x + 7
    rect(bx, y - 4, 2, 9, CHAIR)            # back rest
    put(bx, y - 4, CHAIR_L)
    border(x, y + 5, 9, 5)
    border(bx, y - 4, 2, 9)


def plant(x, y):
    shadow(x + 5, y + 14, 6, 2)
    rect(x + 1, y + 7, 8, 6, (190, 96, 60)); rect(x + 1, y + 7, 8, 1, (220, 130, 86))
    rect(x + 1, y + 12, 8, 1, (150, 70, 44))
    border(x + 1, y + 7, 8, 6)
    for (lx, ly, c) in [(3, 0, (96, 160, 72)), (0, 2, (70, 130, 58)), (6, 1, (84, 150, 66)), (2, 4, (110, 176, 84)),
                        (5, 4, (70, 130, 58)), (8, 3, (96, 160, 72))]:
        ellipse(x + lx + 1, y + ly + 2, 2, 2, c)


# salad bar (the healing station) on the left
SBX, SBY = 34, 30
counter(SBX, SBY, 110, 14, 12, STEEL_L, (150, 100, 62), (110, 70, 40))
for i, c in enumerate([(96, 176, 70), (220, 60, 50), (246, 196, 64), (240, 140, 60), (130, 190, 90)]):
    bx = SBX + 8 + i * 20
    ellipse(bx + 5, SBY + 7, 7, 4, (250, 250, 246))      # bowl rim
    ellipse(bx + 5, SBY + 7, 5, 3, c)                    # salad
    put(bx + 3, SBY + 6, tuple(min(255, v + 50) for v in c))
for gx in range(SBX, SBX + 110):                         # sneeze guard glass
    blend(gx, SBY - 3, (190, 230, 246), 0.6); blend(gx, SBY - 2, (190, 230, 246), 0.45)
rect(SBX + 2, SBY - 4, 1, 5, STEEL_D); rect(SBX + 107, SBY - 4, 1, 5, STEEL_D)
for (px, py) in [(SBX + 52, SBY - 14), (SBX + 30, SBY - 10), (SBX + 78, SBY - 11)]:   # green heal sparkles
    rect(px, py - 2, 1, 5, (110, 220, 110)); rect(px - 2, py, 5, 1, (110, 220, 110)); put(px, py, (220, 255, 220))

# kitchen island with a stove, a pot and a cutting board
IX, IY = 330, 46
counter(IX, IY, 120, 16, 14, STEEL, STEEL_D, (100, 106, 120))
for bx in (IX + 18, IX + 44):
    ellipse(bx, IY + 8, 6, 3, (52, 52, 60)); ellipse(bx, IY + 8, 4, 2, (210, 70, 40)); ellipse(bx, IY + 8, 2, 1, (52, 52, 60))
rect(IX + 38, IY + 1, 13, 8, (200, 56, 50)); rect(IX + 38, IY + 1, 13, 2, (236, 96, 80))   # pot
border(IX + 38, IY + 1, 13, 8); rect(IX + 35, IY + 3, 2, 1, OUTL); rect(IX + 52, IY + 3, 2, 1, OUTL)
for (sx, sy) in [(IX + 42, IY - 4), (IX + 45, IY - 8), (IX + 43, IY - 12), (IX + 47, IY - 6)]:       # steam
    blend(sx, sy, (255, 255, 255), 0.7); blend(sx + 1, sy, (255, 255, 255), 0.5); blend(sx, sy - 1, (255, 255, 255), 0.4)
rect(IX + 78, IY + 4, 22, 9, (210, 160, 100)); rect(IX + 78, IY + 4, 22, 1, (236, 190, 130)); border(IX + 78, IY + 4, 22, 9)
ellipse(IX + 84, IY + 8, 2, 2, (220, 60, 50)); put(IX + 83, IY + 7, (255, 140, 120)); put(IX + 84, IY + 5, (96, 176, 70))
paste(knife_im, IX + 87, IY + 5)

# dining tables with chairs (drawn back to front)
for (tx, ty) in [(150, 92), (40, 150), (380, 150), (190, 210)]:
    chair(tx - 11, ty + 3, "L")
    chair(tx + 28, ty + 3, "R")
    table(tx, ty)
plant(272, 6)
plant(8, 236)
plant(452, 236)

# ---------- characters (feet = bottom of the 24 px frame) ----------
def actor(frame, fx, fy):
    """Draw a 16x24 frame with its feet at (fx, fy)."""
    shadow(fx, fy, 5, 2)
    paste(frame, fx - 8, fy - 23)


for (cx, cy) in [(205, 128), (213, 134), (372, 228)]:
    shadow(cx + 3, cy + 6, 3, 1, 0.25)
    paste(coin_im, cx, cy)

actor(pizza_frames["veggie"][2], 330, 150)
actor(pizza_frames["pepperoni"][0], 120, 205)
actor(pizza_frames["margherita"][1], 300, 238)
actor(chef_frames[0], 240, 168)
# a knife in flight from the chef toward the pizza on the right
paste(knife_im, 266, 150)
for i in range(4):
    blend(260 - i * 3, 153, (255, 255, 255), 0.5 - i * 0.1)
# a pizza that just gave up, dropping a coin
actor(pizza_frames["pepperoni"][3], 100, 115)
paste(coin_im, 104, 117)

img.save(os.path.join(OUT, "restaurant_sample_native.png"))
img.resize((W * 4, H * 4), Image.NEAREST).save(os.path.join(OUT, "restaurant_sample_x4.png"))

# ---------- labelled x8 sheet of all frames ----------
Z = 8
rows = [("Chef (player)", chef_frames, ["idle", "walk 1", "walk 2", "hit"])] + \
       [(f"Pizza ({t})", fr, ["idle", "walk 1", "walk 2", "give up"]) for t, fr in pizza_frames.items()]
pw = 150 + 4 * (FW * Z + 24) + 200
ph = len(rows) * (FH * Z + 40) + 20
prev = Image.new("RGB", (pw, ph), (245, 242, 235))
dr = ImageDraw.Draw(prev)
for r, (label, frames, names) in enumerate(rows):
    y = 20 + r * (FH * Z + 40)
    dr.text((10, y + FH * Z // 2), label, fill=(30, 30, 30))
    for i, fr in enumerate(frames):
        x = 150 + i * (FW * Z + 24)
        dr.rectangle((x, y, x + FW * Z - 1, y + FH * Z - 1), fill=WOOD[0])
        big = fr.resize((FW * Z, FH * Z), Image.NEAREST)
        prev.paste(big, (x, y), big)
        dr.text((x, y + FH * Z + 4), names[i], fill=(60, 60, 60))
ex = 150 + 4 * (FW * Z + 24) + 20
for k, (label, im) in enumerate([("Knife (points right)", knife_im), ("Coin (XP / tip)", coin_im)]):
    y = 40 + k * 160
    big = im.resize((im.width * Z, im.height * Z), Image.NEAREST)
    dr.rectangle((ex - 8, y - 8, ex + big.width + 7, y + big.height + 7), fill=WOOD[0])
    prev.paste(big, (ex, y), big)
    dr.text((ex - 8, y + big.height + 12), label, fill=(60, 60, 60))
prev.save(os.path.join(OUT, "restaurant_characters_x8.png"))
print("saved to", OUT)
