import math
import os
import sys
from PIL import Image, ImageDraw

# Separate chair sprites at the same pixel scale as Table.png (so the same PPU fits both).
# Chair_Front: seat faces the viewer, backrest behind it (use behind the table).
# Chair_Back:  seen from behind, backrest in front (use in front of the table).
# Chair_Side:  backrest on the right; flipX gives the left-hand version.
S = 4
CW, CH = 48, 72
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LINE = (40, 28, 30, 255)
OW = 7 * S // 2
gold, gold_dark = (225, 180, 70, 255), (180, 135, 45, 255)
cushion = (250, 246, 240, 255)


def sc(*v):
    return [int(x * S) for x in v]


def ell(d, box, fill):
    d.ellipse(sc(*box), fill=fill, outline=LINE, width=OW)


def rrect(d, box, r, fill):
    d.rounded_rectangle(sc(*box), radius=r * S, fill=fill, outline=LINE, width=OW)


def backrest(d, bx, by, bw, bh):
    rrect(d, (bx - bw / 2, by - bh, bx + bw / 2, by), 5, gold)
    for k in (-1, 0, 1):
        sx = bx + k * bw / 4
        d.line(sc(sx, by - bh + 7, sx, by - 4), fill=gold_dark, width=3 * S)


def legs(d, x, y, w):
    for lx in (x - w / 2 + 4, x + w / 2 - 4):
        d.line(sc(lx, y + 4, lx, y + 24), fill=LINE, width=OW)
        d.line(sc(lx, y + 4, lx, y + 23), fill=gold, width=2 * S)


def seat(d, x, y, w):
    ell(d, (x - w / 2 - 2, y - 7, x + w / 2 + 2, y + 7), cushion)


def make(kind):
    img = Image.new("RGBA", (CW * S, CH * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x, y = 24, 44  # seat centre; legs end at the bottom of the image
    if kind == "Front":
        backrest(d, x, y - 2, 30, 34)
        legs(d, x, y, 30)
        seat(d, x, y, 30)
    elif kind == "Back":
        legs(d, x, y, 30)
        seat(d, x, y, 30)
        backrest(d, x, y + 10, 30, 36)
    else:  # Side, backrest on the right
        legs(d, x - 4, y, 22)
        seat(d, x - 4, y, 22)
        rrect(d, (x + 6, y - 34, x + 18, y + 6), 4, gold)
        d.line(sc(x + 12, y - 28, x + 12, y), fill=gold_dark, width=3 * S)
    img = img.resize((CW, CH), Image.LANCZOS)
    img.save(os.path.join(OUT, f"Chair_{kind}.png"))
    return img


chairs = {k: make(k) for k in ("Front", "Back", "Side")}

# Preview: table + 8 chairs, drawn in order of their bottom edge (how Y-sorting will look in Unity)
table = Image.open(os.path.join(OUT, "Table.png"))
CX, TOP_Y = 160, 150
items = [(TOP_Y + 44 + 62, table, 32, 32)]  # (bottom y, image, left, top)
for k in range(8):
    ang = k * 45 + 22.5
    a = math.radians(ang)
    x, y = CX + 128 * math.cos(a), TOP_Y + 30 + 78 * math.sin(a)
    s = math.sin(a)
    if s > 0.7:
        img = chairs["Back"]
    elif s < -0.7:
        img = chairs["Front"]
    else:
        img = chairs["Side"]
        if math.cos(a) < 0:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
    items.append((y + 28, img, int(x - 24), int(y - 44)))
prev = Image.new("RGBA", (340, 340), (205, 170, 125, 255))
for _, img, left, top in sorted(items, key=lambda t: t[0]):
    prev.alpha_composite(img, (left + 10, top + 10))
strip = Image.new("RGBA", (3 * 60 + 20, 90), (205, 170, 125, 255))
for i, k in enumerate(("Front", "Back", "Side")):
    strip.alpha_composite(chairs[k], (10 + i * 60, 9))
prev.save(os.path.join(OUT, "chairs_preview.png"))
strip.save(os.path.join(OUT, "chairs_strip.png"))
print("done")
