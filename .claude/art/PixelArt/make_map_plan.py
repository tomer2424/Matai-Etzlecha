import os
import sys
from PIL import Image, ImageDraw, ImageFont

# Map plan in tiles (1 tile = 16 px = 1 Unity unit). Origin bottom-left, y up.
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
MW, MH = 160, 120
K = 7  # pixels per tile in the plan image
M = 40  # margin
img = Image.new("RGB", (MW * K + 2 * M, MH * K + 2 * M + 70), (245, 242, 235))
d = ImageDraw.Draw(img)
try:
    F = ImageFont.truetype("arialbd.ttf", 15)
    FS = ImageFont.truetype("arial.ttf", 12)
except OSError:
    F = FS = ImageFont.load_default()


def box(x0, y0, x1, y1):
    return (M + x0 * K, M + (MH - y1) * K, M + x1 * K, M + (MH - y0) * K)


def zone(x0, y0, x1, y1, col, name, optional=False, inside=False):
    b = box(x0, y0, x1, y1)
    d.rectangle(b, fill=col)
    if optional:
        for x in range(b[0], b[2], 8):
            d.line((x, b[1], min(x + 4, b[2]), b[1]), fill=(60, 60, 60), width=2)
            d.line((x, b[3], min(x + 4, b[2]), b[3]), fill=(60, 60, 60), width=2)
        for y in range(b[1], b[3], 8):
            d.line((b[0], y, b[0], min(y + 4, b[3])), fill=(60, 60, 60), width=2)
            d.line((b[2], y, b[2], min(y + 4, b[3])), fill=(60, 60, 60), width=2)
    else:
        d.rectangle(b, outline=(40, 40, 40) if inside else (90, 90, 90), width=3 if inside else 1)
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    if not name:
        return
    d.text((cx, cy - 8), name, fill=(25, 25, 25), font=F, anchor="mm")
    d.text((cx, cy + 10), f"{x1 - x0}x{y1 - y0}", fill=(70, 70, 70), font=FS, anchor="mm")


def door(x, y, w, h):
    """Opening in an indoor wall (w,h in tiles)."""
    d.rectangle(box(x, y, x + w, y + h), fill=(255, 210, 90))


GRASS, PAVE, ASPH = (150, 200, 120), (225, 212, 185), (150, 150, 158)
WOOD, TILE, KIT = (205, 160, 110), (200, 215, 225), (215, 205, 195)

# outdoor base
d.rectangle(box(0, 0, MW, MH), fill=GRASS)

# ---- south: parking + reception (start) ----
zone(30, 2, 130, 24, ASPH, "PARKING")
zone(56, 24, 104, 46, PAVE, "RECEPTION (start)")
d.ellipse(box(78.5, 33.5, 81.5, 36.5), fill=(220, 40, 60))

# ---- optional outdoor extras ----
zone(104, 24, 128, 46, (235, 200, 215), "PHOTO CORNER", optional=True)
zone(4, 24, 30, 46, (210, 220, 190), "SMOKERS", optional=True)
zone(136, 46, 158, 82, (180, 215, 235), "FOUNTAIN GARDEN", optional=True)
zone(132, 6, 158, 40, (200, 225, 235), "BAR / LOUNGE", optional=True)

# ---- indoor building (west) ----
zone(4, 50, 68, 58, (230, 225, 215), "LOBBY / CORRIDOR", inside=True)
zone(4, 58, 68, 88, WOOD, "", inside=True)
d.rectangle(box(36, 58, 68, 88), fill=(215, 180, 120))
for y in range(box(36, 58, 68, 88)[1], box(36, 58, 68, 88)[3], 10):  # no wall, just a floor change
    d.line((box(36, 58, 68, 88)[0], y, box(36, 58, 68, 88)[0], y + 4), fill=(120, 90, 60), width=2)
d.rectangle(box(4, 58, 68, 88), outline=(40, 40, 40), width=3)
d.text(((box(4, 58, 68, 88)[0] + box(4, 58, 68, 88)[2]) / 2, box(4, 58, 68, 88)[1] + 18), "MAIN HALL  64x30", fill=(25, 25, 25), font=F, anchor="mm")
d.text(((box(4, 58, 36, 88)[0] + box(4, 58, 36, 88)[2]) / 2, (box(4, 58, 36, 88)[1] + box(4, 58, 36, 88)[3]) / 2 + 8), "tables", fill=(40, 40, 40), font=F, anchor="mm")
d.text(((box(36, 58, 68, 88)[0] + box(36, 58, 68, 88)[2]) / 2, (box(36, 58, 68, 88)[1] + box(36, 58, 68, 88)[3]) / 2 + 8), "dance floor + DJ", fill=(40, 40, 40), font=F, anchor="mm")
zone(4, 88, 26, 116, TILE, "WC", inside=True)
zone(26, 88, 68, 116, KIT, "KITCHEN", inside=True)
d.rectangle(box(4, 50, 68, 116), outline=(20, 20, 20), width=5)

# doors (yellow): every room has 2+ openings, all 3-4 tiles wide
for args in [(20, 49, 4, 2), (44, 49, 4, 2),            # lobby <-> outside (south)
             (67, 52, 2, 4),                              # lobby <-> outside (east)
             (14, 57, 4, 2), (50, 57, 4, 2),              # lobby <-> halls
             (67, 66, 2, 4), (67, 78, 2, 4),              # indoor dance <-> outdoor dance
             (3, 70, 2, 4),                               # tables <-> west lawn
             (12, 87, 4, 2), (36, 87, 4, 2), (56, 87, 4, 2),  # hall <-> WC / kitchen
             (25, 100, 2, 4),                             # WC <-> kitchen
             (45, 115, 4, 2), (67, 104, 2, 4)]:           # kitchen back doors
    door(*args)

# ---- outdoor (east) ----
zone(72, 50, 104, 78, (240, 225, 160), "OUTDOOR DANCE FLOOR")
zone(104, 50, 134, 80, (245, 205, 170), "BUFFET AREA")
zone(72, 82, 118, 116, (185, 220, 150), "LAWN WITH CHAIRS")
zone(120, 86, 158, 118, (250, 245, 235), "CHUPPAH AREA")

# paths (outdoor connections are open, these are just walkways)
for a, b in [((80, 46), (88, 50)), ((96, 64), (104, 64)), ((88, 78), (95, 82)),
             ((118, 98), (120, 98)), ((120, 80), (128, 86)), ((104, 35), (104, 35))]:
    pass

# scale reference: one screen = 30x17 tiles
sx, sy = 5, 2
d.rectangle(box(sx, sy, sx + 30, sy + 17), outline=(200, 30, 30), width=3)
d.text(box(sx, sy, sx + 30, sy + 17)[0] + 4, box(sx, sy, sx + 30, sy + 17)[1] + 4) if False else None
d.text((box(sx, sy, sx + 30, sy + 17)[0] + 6, box(sx, sy, sx + 30, sy + 17)[1] + 4),
       "1 screen", fill=(200, 30, 30), font=FS)

# grid ticks every 10 tiles
for t in range(0, MW + 1, 10):
    x = M + t * K
    d.line((x, M + MH * K, x, M + MH * K + 6), fill=(60, 60, 60))
    if t % 20 == 0:
        d.text((x, M + MH * K + 16), str(t), fill=(60, 60, 60), font=FS, anchor="mm")
for t in range(0, MH + 1, 10):
    y = M + (MH - t) * K
    d.line((M - 6, y, M, y), fill=(60, 60, 60))
    if t % 20 == 0:
        d.text((M - 18, y), str(t), fill=(60, 60, 60), font=FS, anchor="mm")
d.rectangle(box(0, 0, MW, MH), outline=(30, 90, 30), width=4)

# legend
ly = M + MH * K + 34
d.rectangle((M, ly, M + 16, ly + 12), fill=(255, 210, 90)); d.text((M + 22, ly - 1), "door / opening", fill=(30, 30, 30), font=FS)
d.rectangle((M + 150, ly, M + 166, ly + 12), outline=(20, 20, 20), width=3); d.text((M + 172, ly - 1), "indoor (walls)", fill=(30, 30, 30), font=FS)
d.rectangle((M + 290, ly, M + 306, ly + 12), outline=(60, 60, 60), width=1); d.text((M + 312, ly - 1), "outdoor (open)", fill=(30, 30, 30), font=FS)
for x in range(M + 430, M + 446, 6):
    d.line((x, ly, x + 3, ly), fill=(60, 60, 60), width=2)
d.text((M + 452, ly - 1), "optional zone (dashed)", fill=(30, 30, 30), font=FS)
d.ellipse((M + 620, ly, M + 632, ly + 12), fill=(220, 40, 60)); d.text((M + 638, ly - 1), "player start", fill=(30, 30, 30), font=FS)
d.text((M, ly + 20), "Map 160 x 120 tiles (1 tile = 16 px = 1 unit). Red box = what one screen shows.",
       fill=(30, 30, 30), font=FS)

img.save(os.path.join(OUT, "map_plan.png"))
print("done")
