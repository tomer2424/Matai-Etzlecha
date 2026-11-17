import math
import os
import sys
from PIL import Image, ImageDraw

# Round wedding table with 8 gold chairs, 3/4 top-down view, same style as the characters.
S = 4
W = H = 320
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LINE = (40, 28, 30, 255)
OW = 7 * S // 2

cloth, cloth_sh, cloth_dark = (252, 250, 245, 255), (226, 222, 214, 255), (200, 195, 186, 255)
gold, gold_dark = (225, 180, 70, 255), (180, 135, 45, 255)
cushion = (250, 246, 240, 255)

CX, TOP_Y, RX, RY = 160, 150, 108, 58  # table top ellipse
DROP, FLARE = 44, 8


def sc(*v):
    return [int(x * S) for x in v]


def layer():
    img = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def ell(d, box, fill, outline=True, width=None):
    d.ellipse(sc(*box), fill=fill, outline=LINE if outline else None,
              width=(width or OW) if outline else 0)


def rrect(d, box, r, fill, width=None):
    d.rounded_rectangle(sc(*box), radius=r * S, fill=fill, outline=LINE, width=width or OW)


def chair(d, x, y, angle_deg):
    """Chair whose seat centre is (x, y). The backrest is on the side away from the table."""
    side = math.cos(math.radians(angle_deg))
    front = math.sin(math.radians(angle_deg)) > 0.3   # between table and viewer
    back = math.sin(math.radians(angle_deg)) < -0.3   # behind the table
    w = 30 if (front or back) else 22  # side chairs look narrower

    def backrest(bx, by, bw, bh):
        rrect(d, (bx - bw / 2, by - bh, bx + bw / 2, by), 5, gold)
        for k in (-1, 0, 1):
            sx = bx + k * bw / 4
            d.line(sc(sx, by - bh + 7, sx, by - 4), fill=gold_dark, width=3 * S)

    def legs():
        for lx in (x - w / 2 + 4, x + w / 2 - 4):
            d.line(sc(lx, y + 4, lx, y + 24), fill=LINE, width=OW)
            d.line(sc(lx, y + 4, lx, y + 23), fill=gold, width=2 * S)

    if back:
        # backrest sticks up behind the seat
        backrest(x, y - 2, w, 34)
        legs()
        ell(d, (x - w / 2 - 2, y - 7, x + w / 2 + 2, y + 7), cushion)
    elif front:
        # we see the chair from behind: seat, then the backrest covers it
        legs()
        ell(d, (x - w / 2 - 2, y - 7, x + w / 2 + 2, y + 7), cushion)
        backrest(x, y + 10, w, 36)
    else:
        # side chair: backrest on the outer side
        bx = x + (w / 2 + 2) * (1 if side > 0 else -1)
        legs()
        ell(d, (x - w / 2 - 2, y - 7, x + w / 2 + 2, y + 7), cushion)
        rrect(d, (bx - 4, y - 34, bx + 4, y + 6), 3, gold)


def table(d):
    ell(d, (CX - RX - 10, TOP_Y + 78, CX + RX + 10, TOP_Y + 128), (0, 0, 0, 60), outline=False)
    skirt = [(CX - RX, TOP_Y)]
    for i in range(0, 181, 3):  # wavy, slightly flared hem
        a = math.radians(i)
        wave = 3.5 * math.sin(i * math.pi / 15)
        skirt.append((CX - (RX + FLARE) * math.cos(a), TOP_Y + DROP + (RY + 4) * math.sin(a) + wave))
    skirt.append((CX + RX, TOP_Y))
    p = [(x * S, y * S) for x, y in skirt]
    d.polygon(p, fill=cloth_sh)
    for k in range(1, 12):  # folds
        a = math.radians(180 * k / 12)
        x_top, y_top = CX - RX * math.cos(a), TOP_Y + RY * math.sin(a)
        x_bot, y_bot = CX - (RX + FLARE) * math.cos(a), TOP_Y + DROP + (RY + 4) * math.sin(a)
        d.line(sc(x_top, y_top + 6, x_bot, y_bot - 4), fill=cloth_dark, width=3 * S)
    d.line(p + [p[0]], fill=LINE, width=OW, joint="curve")
    ell(d, (CX - RX, TOP_Y - RY, CX + RX, TOP_Y + RY + 8), gold)
    ell(d, (CX - RX, TOP_Y - RY, CX + RX, TOP_Y + RY), cloth)
    for k in range(8):  # plates and glasses
        a = math.radians(k * 45 + 22.5)
        px, py = CX + 80 * math.cos(a), TOP_Y + 40 * math.sin(a)
        ell(d, (px - 15, py - 8, px + 15, py + 8), (255, 255, 255, 255), width=OW // 2)
        ell(d, (px - 9, py - 4.5, px + 9, py + 4.5), (235, 235, 240, 255), outline=False)
        gx, gy = CX + 62 * math.cos(a + 0.35), TOP_Y + 31 * math.sin(a + 0.35)
        ell(d, (gx - 4, gy - 10, gx + 4, gy + 2), (190, 225, 245, 230), width=OW // 3)
    # centerpiece
    ell(d, (CX - 16, TOP_Y - 6, CX + 16, TOP_Y + 8), (0, 0, 0, 40), outline=False)
    d.rounded_rectangle(sc(CX - 10, TOP_Y - 22, CX + 10, TOP_Y + 4), radius=6 * S,
                        fill=(200, 230, 245, 255), outline=LINE, width=OW // 2)
    for lx, ly in [(-20, -26), (20, -26), (-12, -40), (12, -40)]:
        ell(d, (CX + lx - 9, TOP_Y + ly - 5, CX + lx + 9, TOP_Y + ly + 5), (90, 160, 80, 255), width=OW // 2)
    for fx, fy, col in [(0, -52, (240, 90, 130, 255)), (-14, -42, (255, 255, 255, 255)),
                        (14, -42, (255, 255, 255, 255)), (-8, -28, (250, 170, 190, 255)),
                        (8, -28, (240, 90, 130, 255)), (0, -38, (255, 220, 120, 255))]:
        ell(d, (CX + fx - 10, TOP_Y + fy - 10, CX + fx + 10, TOP_Y + fy + 10), col, width=OW // 2)
        ell(d, (CX + fx - 3, TOP_Y + fy - 3, CX + fx + 3, TOP_Y + fy + 3), gold, outline=False)


behind, db = layer()
middle, dm = layer()
front, df = layer()

# chairs sit around a bigger ellipse, lined up with the plates
seats = []
for k in range(8):
    ang = k * 45 + 22.5
    a = math.radians(ang)
    x, y = CX + 128 * math.cos(a), TOP_Y + 30 + 78 * math.sin(a)
    seats.append((y, x, ang))
for y, x, ang in sorted(seats):  # far chairs first
    target = df if math.sin(math.radians(ang)) > 0.3 else db
    chair(target, x, y, ang)

table(dm)

out = Image.new("RGBA", (W * S, H * S), (0, 0, 0, 0))
for lyr in (behind, middle, front):
    out.alpha_composite(lyr)
out = out.resize((W, H), Image.LANCZOS)
out.save(os.path.join(OUT, "TableWithChairs.png"))

prev = Image.new("RGBA", (W + 20, H + 20), (205, 170, 125, 255))
prev.alpha_composite(out, (10, 10))
prev.save(os.path.join(OUT, "table_chairs_preview.png"))
print("done")
