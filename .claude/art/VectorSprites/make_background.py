import math
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFilter

# Event venue floor only (no obstacles): indoor hall on the left, garden on the right.
random.seed(7)
W, H = 4096, 2730
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LINE = (40, 28, 30, 255)

img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
d = ImageDraw.Draw(img)

# ---------- garden: grass everywhere ----------
GRASS = (112, 170, 84)
d.rectangle((0, 0, W, H), fill=GRASS)
# soft light/dark patches
patch = Image.new("L", (W // 8, H // 8), 0)
pd = ImageDraw.Draw(patch)
for _ in range(220):
    x, y, r = random.randint(0, W // 8), random.randint(0, H // 8), random.randint(8, 30)
    pd.ellipse((x - r, y - r, x + r, y + r), fill=random.randint(40, 110))
patch = patch.filter(ImageFilter.GaussianBlur(10)).resize((W, H))
light = Image.new("RGBA", (W, H), (140, 196, 104, 255))
img.paste(light, (0, 0), patch)
d = ImageDraw.Draw(img)
# grass blades
for _ in range(45000):
    x, y = random.randint(0, W), random.randint(0, H)
    c = random.choice([(88, 145, 66), (96, 154, 70), (138, 192, 100), (150, 200, 110)])
    d.line((x, y, x + random.randint(-5, 5), y - random.randint(8, 16)), fill=c, width=3)
# tiny flowers in the lawn
for _ in range(900):
    x, y = random.randint(0, W), random.randint(0, H)
    c = random.choice([(255, 255, 255), (255, 230, 120), (250, 180, 200)])
    d.ellipse((x - 4, y - 4, x + 4, y + 4), fill=c)


def pavers(poly_mask, base, tile, jitter=0, gap=(160, 150, 135), line_w=3):
    """Fill a mask with square stone tiles."""
    layer = Image.new("RGBA", (W, H), gap + (255,))
    ld = ImageDraw.Draw(layer)
    for ty in range(0, H, tile):
        off = (tile // 2) if (ty // tile) % 2 else 0
        for tx in range(-tile, W, tile):
            x0, y0 = tx + off, ty
            v = random.randint(-jitter, jitter)
            col = tuple(max(0, min(255, c + v)) for c in base)
            ld.rounded_rectangle((x0 + line_w, y0 + line_w, x0 + tile - line_w, y0 + tile - line_w),
                                 radius=tile // 8, fill=col)
    img.paste(layer, (0, 0), poly_mask)


def mask_from(draw_fn):
    m = Image.new("L", (W, H), 0)
    draw_fn(ImageDraw.Draw(m))
    return m


# ---------- garden paths (curved, paved) ----------
def path_points(pts, steps=40):
    out = []
    for i in range(len(pts) - 1):
        (x0, y0), (x1, y1) = pts[i], pts[i + 1]
        for s in range(steps):
            t = s / steps
            out.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t + math.sin(t * math.pi) * (i % 2 * 2 - 1) * 60))
    out.append(pts[-1])
    return out


paths = [
    [(2300, 1360), (2700, 1150), (3100, 980), (3420, 900)],      # terrace -> ceremony deck
    [(2300, 1500), (2700, 1700), (3100, 1960), (3420, 2060)],    # terrace -> lounge
    [(3420, 1280), (3420, 1700)],                                # deck <-> lounge
    [(3700, 900), (4096, 760)],                                  # deck -> east edge
    [(2100, 2030), (2100, 2730)],                                # terrace -> south edge (entrance)
]


def draw_paths(md, width):
    for p in paths:
        pts = path_points(p)
        md.line(pts, fill=255, width=width, joint="curve")
        for x, y in (pts[0], pts[-1]):
            md.ellipse((x - width / 2, y - width / 2, x + width / 2, y + width / 2), fill=255)


edge = mask_from(lambda md: draw_paths(md, 170))
d.bitmap((0, 0), edge, fill=(90, 70, 55))  # dark border under paths
inner = mask_from(lambda md: draw_paths(md, 150))
pavers(inner, (222, 205, 170), 50, jitter=12, gap=(185, 165, 130))

# ---------- lounge / food area (round paved plaza) ----------
plaza = mask_from(lambda md: md.ellipse((3080, 1740, 3760, 2380), fill=255))
d.ellipse((3070, 1730, 3770, 2390), fill=(90, 70, 55))
pavers(plaza, (215, 200, 175), 90, jitter=10, gap=(175, 160, 135))

# ---------- ceremony deck (wooden, round) ----------
cx, cy, r = 3420, 900, 400
d.ellipse((cx - r - 12, cy - r - 12, cx + r + 12, cy + r + 12), fill=LINE)
deck = Image.new("RGBA", (W, H), (0, 0, 0, 0))
dd = ImageDraw.Draw(deck)
for y in range(cy - r, cy + r, 34):
    col = random.choice([(196, 150, 100), (186, 140, 92), (204, 158, 108)])
    dd.rectangle((cx - r, y, cx + r, y + 30), fill=col + (255,))
    dd.line((cx - r, y + 32, cx + r, y + 32), fill=(130, 90, 55, 255), width=4)
deck_mask = mask_from(lambda md: md.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255))
img.paste(deck, (0, 0), deck_mask)
d = ImageDraw.Draw(img)

# ---------- terrace next to the hall (outdoor stone tiles) ----------
TX0, TY0, TX1, TY1 = 1900, 700, 2350, 2030
d.rectangle((TX0, TY0 - 10, TX1 + 10, TY1 + 10), fill=(90, 70, 55))
terrace = mask_from(lambda md: md.rectangle((TX0, TY0, TX1, TY1), fill=255))
pavers(terrace, (232, 226, 214), 110, jitter=6, gap=(190, 182, 170), line_w=4)

# ---------- indoor hall (parquet) ----------
HX0, HY0, HX1, HY1 = 120, 200, 1900, 2530
hall = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hall)
PL = 46  # plank height
for y in range(HY0, HY1, PL):
    x = HX0 - random.randint(0, 300)
    while x < HX1:
        ln = random.randint(220, 420)
        col = random.choice([(186, 128, 78), (176, 120, 72), (196, 138, 86), (170, 114, 68)])
        hd.rectangle((x, y, x + ln, y + PL), fill=col + (255,))
        hd.line((x, y, x, y + PL), fill=(120, 78, 45, 255), width=3)
        x += ln
    hd.line((HX0, y, HX1, y), fill=(120, 78, 45, 255), width=3)
hall_mask = mask_from(lambda md: md.rectangle((HX0, HY0, HX1, HY1), fill=255))
img.paste(hall, (0, 0), hall_mask)
d = ImageDraw.Draw(img)

# dance floor in the middle of the hall
DX0, DY0, T = 640, 1010, 100
n_x, n_y = 8, 7
d.rectangle((DX0 - 22, DY0 - 22, DX0 + n_x * T + 22, DY0 + n_y * T + 22), fill=(225, 180, 70), outline=LINE, width=6)
for i in range(n_x):
    for j in range(n_y):
        col = (250, 244, 228) if (i + j) % 2 == 0 else (238, 214, 150)
        d.rectangle((DX0 + i * T, DY0 + j * T, DX0 + (i + 1) * T, DY0 + (j + 1) * T),
                    fill=col, outline=(200, 170, 110), width=3)
# little star highlights on the dance floor
for _ in range(14):
    x = random.randint(DX0 + 20, DX0 + n_x * T - 20)
    y = random.randint(DY0 + 20, DY0 + n_y * T - 20)
    d.line((x - 10, y, x + 10, y), fill=(255, 255, 255), width=4)
    d.line((x, y - 10, x, y + 10), fill=(255, 255, 255), width=4)

# carpet runner from the hall entrance to the dance floor
d.rectangle((960 - 70, DY0 + n_y * T + 22, 960 + 70, HY1), fill=(160, 40, 60), outline=LINE, width=5)
d.rectangle((960 - 52, DY0 + n_y * T + 22, 960 + 52, HY1), outline=(225, 180, 70), width=4)

# baseboard where the hall walls go (walls themselves are separate objects)
d.rectangle((HX0, HY0, HX1, HY1), outline=(235, 228, 215), width=26)
d.rectangle((HX0 - 6, HY0 - 6, HX1 + 6, HY1 + 6), outline=LINE, width=6)
# door openings: hall -> terrace (two wide doors) and hall -> south (entrance)
for y0, y1 in [(820, 1180), (1540, 1900)]:
    d.rectangle((HX1 - 20, y0, HX1 + 8, y1), fill=(232, 226, 214))
d.rectangle((960 - 120, HY1 - 20, 960 + 120, HY1 + 8), fill=(160, 40, 60))

img = img.convert("RGB")
img.save(os.path.join(OUT, "Background.png"), optimize=True)
img.resize((W // 4, H // 4), Image.LANCZOS).save(os.path.join(OUT, "background_preview.png"))
print("done")
