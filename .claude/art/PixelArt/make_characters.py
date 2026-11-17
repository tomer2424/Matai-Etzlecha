import os
import sys
from PIL import Image, ImageDraw

# Player + aunt sprite sheets. 16x24 frames, FACING LEFT (flip in Unity with SpriteRenderer.flipX).
# Frames per sheet (left to right): idle, walk1, walk2, then hit (player) / give-up (aunt).
# Fills are drawn first, then a dark outline is added automatically around the silhouette.
# Usage: python make_characters.py <output_dir>
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)
FW, FH = 16, 24

OUTL = (38, 26, 34, 255)
SKIN, SKIN_D = (240, 190, 150), (206, 150, 112)
WHITE = (246, 244, 236)
EYE = (38, 26, 34)


class Frame:
    def __init__(self):
        self.px = {}

    def put(self, x, y, c):
        if 0 <= x < FW and 0 <= y < FH:
            self.px[(x, y)] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, c)

    def grid(self, rows, x0, y0, pal):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch != ".":
                    self.put(x0 + i, y0 + j, pal[ch])

    def image(self):
        im = Image.new("RGBA", (FW, FH), (0, 0, 0, 0))
        for (x, y), c in self.px.items():
            im.putpixel((x, y), tuple(c[:3]) + (255,))
        # automatic outline: every empty pixel touching a filled pixel (4 directions) becomes outline
        filled = set(self.px)
        for (x, y) in list(filled):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < FW and 0 <= ny < FH and (nx, ny) not in filled:
                    im.putpixel((nx, ny), OUTL)
        return im


def leg(f, hip_x, hip_y, foot_dx, color, shoe, length=5):
    """2 px wide leg from the hip to the foot (foot_dx = how far forward/back the foot is), shoe points left."""
    for i in range(length):
        t = i / (length - 1)
        x = hip_x + round(foot_dx * t)
        f.rect(x, hip_y + i, 2, 1, color)
    fx = hip_x + foot_dx
    f.rect(fx - 1, hip_y + length, 3, 1, shoe)
    f.put(fx - 1, hip_y + length, tuple(min(255, c + 30) for c in shoe))  # toe highlight


def arm(f, sx, sy, hx, hy, sleeve, hand=SKIN):
    """Arm from shoulder (sx, sy) to hand (hx, hy): 1 px sleeve line, skin hand at the end."""
    steps = max(abs(hx - sx), abs(hy - sy))
    for i in range(steps):
        t = i / steps
        f.put(round(sx + (hx - sx) * t), round(sy + (hy - sy) * t), sleeve)
        f.put(round(sx + (hx - sx) * t) + 1, round(sy + (hy - sy) * t), sleeve)
    f.put(hx, hy, hand); f.put(hx + 1, hy, hand)


# =============================== PLAYER ===============================
P = {
    "H": (92, 56, 36), "h": (128, 82, 52), "S": SKIN, "s": SKIN_D, "E": EYE, "M": (150, 70, 70),
    "e": SKIN_D, "C": (176, 120, 96),
}
JACKET, JACKET_D, JACKET_L = (48, 64, 110), (34, 46, 82), (66, 86, 140)
PANTS, PANTS_FAR = (40, 52, 92), (28, 36, 66)
SHOES = (70, 50, 44)
TIE = (200, 50, 60)

PLAYER_HEAD = [
    "...HHHH...",
    "..HHHHHHh.",
    ".HHhHHHHHh",
    ".HHSSHHHHh",
    ".HSSSSsHHh",
    ".SESSSeeHh",
    ".SESSSseHh",
    ".SMSSSsHH.",
    "..SSSSs...",
]
PLAYER_HEAD_HIT = [r.replace("E", "s").replace("M", "E") for r in PLAYER_HEAD]  # eyes squeezed, mouth open


def player(kind):
    f = Frame()
    bob = 1 if kind == "walk1" else 0           # body dips on the stride frame
    legs = {"idle": (0, 0), "walk1": (-2, 2), "walk2": (2, -2), "hit": (1, 0)}[kind]
    lean = 1 if kind == "hit" else 0             # thrown back a little when hit
    # far leg (darker), then near leg
    leg(f, 8 + lean, 17 + bob, legs[1], PANTS_FAR, SHOES, length=5 - bob)
    leg(f, 6 + lean, 17 + bob, legs[0], PANTS, SHOES, length=5 - bob)
    # far arm peeks out behind the body
    if kind == "hit":
        arm(f, 9 + lean, 11, 11 + lean, 8, JACKET_D)
    else:
        f.rect(10 + lean, 12 + bob, 1, 4, JACKET_D)
    # torso: jacket, white shirt + red tie on the front (left) side
    f.rect(5 + lean, 10 + bob, 6, 7, JACKET)
    f.rect(5 + lean, 10 + bob, 1, 7, JACKET_L)
    f.rect(5 + lean, 10 + bob, 2, 3, WHITE)
    f.rect(5 + lean, 11 + bob, 1, 4, TIE)
    f.rect(6 + lean, 16 + bob, 5, 1, JACKET_D)  # jacket hem
    # near arm swings opposite to the near leg
    swing = {"idle": 0, "walk1": 2, "walk2": -2, "hit": 0}[kind]
    if kind != "hit":
        arm(f, 7 + lean, 11 + bob, 7 + lean - swing // 2 + (1 if swing < 0 else 0), 15 + bob, JACKET_D)
    # head on top
    f.grid(PLAYER_HEAD_HIT if kind == "hit" else PLAYER_HEAD, 3 + lean, 1 + bob, P)
    if kind == "hit":
        arm(f, 6 + lean, 11, 3 + lean, 9, JACKET_D)  # hands up in shock, in front of the chin
        f.put(13, 2, (150, 200, 240)); f.put(13, 3, (150, 200, 240))
    return f.image()


# =============================== AUNT ===============================
def aunt_palette(dress, dress_l, dress_d, hair, hair_l):
    return {"R": hair, "r": hair_l, "S": SKIN, "s": SKIN_D, "E": EYE, "e": SKIN_D,
            "L": (200, 40, 70), "W": WHITE, "D": dress, "d": dress_l, "k": dress_d}


AUNT_HEAD = [
    "...RRRRRr...",
    "..RRRRRRRrRR",
    ".RRRrRRRRrRr",
    ".RRSSRRRRRRr",
    ".RSSSSsRRRR.",
    ".SESSSeeRRr.",
    ".SESSSseRRr.",
    ".SLSSSsRRr..",
    "..SSSSs.....",
]
AUNT_HEAD_GIVEUP = [r.replace("E", "s").replace("L", "E") for r in AUNT_HEAD]  # eyes closed, mouth open (sigh)

VARIANTS = {
    "pink": ((240, 120, 160), (250, 190, 210), (196, 80, 124), (126, 40, 70), (160, 62, 96)),
    "blue": ((110, 170, 210), (170, 210, 235), (70, 120, 170), (60, 40, 30), (96, 64, 44)),
    "purple": ((150, 110, 190), (196, 166, 222), (110, 76, 146), (170, 170, 176), (210, 210, 214)),
    "yellow": ((230, 170, 60), (246, 210, 120), (186, 126, 36), (126, 40, 70), (160, 62, 96)),
}
AUNT_SHOES = (60, 40, 46)
BAG, BAG_D = (230, 186, 80), (176, 132, 52)


def aunt(kind, pal):
    f = Frame()
    D, d, k = pal["D"], pal["d"], pal["k"]
    bob = 1 if kind == "walk1" else 0
    feet = {"idle": (0, 0), "walk1": (-1, 1), "walk2": (1, -1), "giveup": (0, 0)}[kind]
    sway = {"idle": 0, "walk1": -1, "walk2": 1, "giveup": 0}[kind]
    # short legs under the dress
    leg(f, 8, 20, feet[1], (196, 150, 120), AUNT_SHOES, length=2)
    leg(f, 6, 20, feet[0], SKIN_D, AUNT_SHOES, length=2)
    # dress: bodice + flared skirt (hem sways when walking)
    f.rect(5, 10 + bob, 6, 4, D)
    for i, (x0, w) in enumerate([(5, 6), (4, 8), (4, 8), (3, 10), (3, 10), (3, 10)]):
        y = 14 + i + bob
        if y >= 21:
            break
        sx = sway if i >= 3 else 0
        f.rect(x0 + sx, y, w, 1, D)
        f.put(x0 + sx + w - 1, y, k)                # shaded back edge
    for (x, y) in [(6, 12), (9, 14), (5, 17), (8, 18), (11, 17), (7, 15)]:  # polka dots
        f.put(x + (sway if y >= 17 else 0), y + bob, d)
    f.rect(5, 10 + bob, 4, 1, WHITE)                 # pearl necklace
    # arm + handbag
    if kind != "giveup":
        hand_x = 7 - sway
        arm(f, 7, 11 + bob, hand_x, 15 + bob, k)
        f.rect(hand_x + 1, 16 + bob, 3, 3, BAG); f.rect(hand_x + 1, 18 + bob, 3, 1, BAG_D)  # handbag
    f.grid(AUNT_HEAD_GIVEUP if kind == "giveup" else AUNT_HEAD, 3, 1 + bob, pal)
    if kind == "giveup":
        arm(f, 7, 11, 4, 4, k)                       # hand on the forehead: "I give up"
        f.put(14, 4, (150, 200, 240)); f.put(14, 5, (150, 200, 240))  # sweat drop
    return f.image()


def sheet(frames):
    im = Image.new("RGBA", (FW * len(frames), FH), (0, 0, 0, 0))
    for i, fr in enumerate(frames):
        im.paste(fr, (i * FW, 0))
    return im


# ---------- build ----------
player_frames = [player(k) for k in ("idle", "walk1", "walk2", "hit")]
sheet(player_frames).save(os.path.join(OUT, "Player_sheet.png"))

aunt_sheets = {}
for name, (dr, dl, dd, hr, hl) in VARIANTS.items():
    pal = aunt_palette(dr, dl, dd, hr, hl)
    frames = [aunt(k, pal) for k in ("idle", "walk1", "walk2", "giveup")]
    aunt_sheets[name] = frames
    sheet(frames).save(os.path.join(OUT, f"Aunt_{name}_sheet.png"))

# ---------- preview (x8, on grass, with labels) ----------
Z = 8
rows = [("Player", player_frames, ["idle", "walk 1", "walk 2", "hit"])] + \
       [(f"Aunt ({n})", fr, ["idle", "walk 1", "walk 2", "give up"]) for n, fr in aunt_sheets.items()]
pw = 140 + 4 * (FW * Z + 24)
ph = len(rows) * (FH * Z + 40) + 20
prev = Image.new("RGB", (pw, ph), (245, 242, 235))
dr = ImageDraw.Draw(prev)
for r, (label, frames, names) in enumerate(rows):
    y = 20 + r * (FH * Z + 40)
    dr.text((10, y + FH * Z // 2), label, fill=(30, 30, 30))
    for i, fr in enumerate(frames):
        x = 140 + i * (FW * Z + 24)
        dr.rectangle((x, y, x + FW * Z - 1, y + FH * Z - 1), fill=(98, 154, 68))
        big = fr.resize((FW * Z, FH * Z), Image.NEAREST)
        prev.paste(big, (x, y), big)
        dr.text((x, y + FH * Z + 4), names[i], fill=(60, 60, 60))
prev.save(os.path.join(OUT, "characters_preview.png"))
print("done")
