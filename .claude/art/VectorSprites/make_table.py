import math
import os
import sys
from PIL import Image, ImageDraw

# Round wedding table seen from a 3/4 top-down angle, same style as the characters.
S = 4
SIZE = 256
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LINE = (40, 28, 30, 255)
OW = 7 * S // 2


def sc(*v):
    return [int(x * S) for x in v]


def ell(d, box, fill, outline=True, width=None):
    d.ellipse(sc(*box), fill=fill, outline=LINE if outline else None,
              width=(width or OW) if outline else 0)


img = Image.new("RGBA", (SIZE * S, SIZE * S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

cloth, cloth_sh, cloth_dark = (252, 250, 245, 255), (226, 222, 214, 255), (200, 195, 186, 255)
gold = (225, 180, 70, 255)

# shadow on the floor
ell(d, (14, 196, 242, 246), (0, 0, 0, 60), outline=False)

# tablecloth skirt: a rounded shape hanging down from the table top
cx, top_y, rx, ry = 128, 118, 108, 58
drop, flare = 44, 8
skirt = [(cx - rx, top_y)]
hem = []
for i in range(0, 181, 3):  # wavy hem below the table, slightly flared
    a = math.radians(i)
    wave = 3.5 * math.sin(i * math.pi / 15)
    hem.append((cx - (rx + flare) * math.cos(a), top_y + drop + (ry + 4) * math.sin(a) + wave))
skirt += hem
skirt.append((cx + rx, top_y))
p = [(x * S, y * S) for x, y in skirt]
d.polygon(p, fill=cloth_sh)
# soft folds from the table edge down to the hem
for k in range(1, 12):
    t = k / 12
    a = math.radians(180 * t)
    x_top = cx - rx * math.cos(a)
    y_top = top_y + ry * math.sin(a)
    x_bot = cx - (rx + flare) * math.cos(a)
    y_bot = top_y + drop + (ry + 4) * math.sin(a)
    d.line(sc(x_top, y_top + 6, x_bot, y_bot - 4), fill=cloth_dark, width=3 * S)
d.line(p + [p[0]], fill=LINE, width=OW, joint="curve")

# gold ribbon along the edge of the table top
ell(d, (cx - rx, top_y - ry, cx + rx, top_y + ry + 8), gold)
# table top
ell(d, (cx - rx, top_y - ry, cx + rx, top_y + ry), cloth)

# plates around the edge (ellipse ring)
for k in range(8):
    a = math.radians(k * 45 + 22.5)
    px, py = cx + 80 * math.cos(a), top_y + 40 * math.sin(a)
    ell(d, (px - 15, py - 8, px + 15, py + 8), (255, 255, 255, 255), width=OW // 2)
    ell(d, (px - 9, py - 4.5, px + 9, py + 4.5), (235, 235, 240, 255), outline=False)
    # glass next to each plate
    gx, gy = cx + 62 * math.cos(a + 0.35), top_y + 31 * math.sin(a + 0.35)
    ell(d, (gx - 4, gy - 10, gx + 4, gy + 2), (190, 225, 245, 230), width=OW // 3)

# centerpiece: small vase with flowers
ell(d, (112, 112, 144, 126), (0, 0, 0, 40), outline=False)
d.rounded_rectangle(sc(118, 96, 138, 122), radius=6 * S, fill=(200, 230, 245, 255), outline=LINE, width=OW // 2)
leaves = (90, 160, 80, 255)
for lx, ly in [(108, 92), (148, 92), (116, 78), (140, 78)]:
    ell(d, (lx - 9, ly - 5, lx + 9, ly + 5), leaves, width=OW // 2)
for fx, fy, col in [(128, 66, (240, 90, 130, 255)), (114, 76, (255, 255, 255, 255)),
                    (142, 76, (255, 255, 255, 255)), (120, 90, (250, 170, 190, 255)),
                    (136, 90, (240, 90, 130, 255)), (128, 80, (255, 220, 120, 255))]:
    ell(d, (fx - 10, fy - 10, fx + 10, fy + 10), col, width=OW // 2)
    ell(d, (fx - 3, fy - 3, fx + 3, fy + 3), gold, outline=False)

img = img.resize((SIZE, SIZE), Image.LANCZOS)
img.save(os.path.join(OUT, "Table.png"))

prev = Image.new("RGBA", (SIZE + 20, SIZE + 20), (205, 170, 125, 255))
prev.alpha_composite(img, (10, 10))
prev.save(os.path.join(OUT, "table_preview.png"))
print("done")
