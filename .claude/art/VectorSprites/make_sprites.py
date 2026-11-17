import os
import sys
from PIL import Image, ImageDraw

# Draw at 4x and downscale for smooth edges. Both characters face LEFT.
S = 4
SIZE = 256
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
LINE = (40, 28, 30, 255)
OW = 7 * S // 2  # outline width


def sc(*v):
    return [int(x * S) for x in v]


def ell(d, box, fill, outline=True):
    d.ellipse(sc(*box), fill=fill, outline=LINE if outline else None, width=OW if outline else 0)


def rrect(d, box, r, fill, outline=True):
    d.rounded_rectangle(sc(*box), radius=r * S, fill=fill, outline=LINE if outline else None, width=OW if outline else 0)


def poly(d, pts, fill, outline=True):
    p = [(x * S, y * S) for x, y in pts]
    d.polygon(p, fill=fill)
    if outline:
        d.line(p + [p[0]], fill=LINE, width=OW, joint="curve")


def finish(img, name):
    img = img.resize((SIZE, SIZE), Image.LANCZOS)
    img.save(os.path.join(OUT, name))
    return img


def player():
    img = Image.new("RGBA", (SIZE * S, SIZE * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    skin, skin_sh = (244, 200, 162, 255), (222, 168, 128, 255)
    suit, suit_dark = (44, 62, 102, 255), (31, 44, 74, 255)
    hair = (78, 48, 30, 255)
    shirt, tie = (248, 248, 248, 255), (200, 50, 50, 255)

    # legs and shoes
    rrect(d, (100, 196, 122, 238), 6, suit_dark)
    rrect(d, (134, 196, 156, 238), 6, suit_dark)
    ell(d, (88, 228, 124, 246), (25, 25, 25, 255))
    ell(d, (122, 228, 158, 246), (25, 25, 25, 255))
    # back arm
    rrect(d, (150, 132, 174, 196), 11, suit_dark)
    ell(d, (150, 186, 172, 206), skin_sh)
    # body
    rrect(d, (88, 122, 166, 208), 20, suit)
    # shirt V and tie
    poly(d, [(108, 124), (146, 124), (127, 160)], shirt, outline=False)
    poly(d, [(121, 128), (133, 128), (130, 136), (124, 136)], tie, outline=False)
    poly(d, [(124, 136), (130, 136), (134, 162), (127, 170), (120, 162)], tie, outline=False)
    d.line(sc(108, 124, 127, 160, 146, 124), fill=LINE, width=OW // 2)
    # front arm (slightly forward/left, like he is running)
    rrect(d, (74, 130, 98, 192), 11, suit)
    ell(d, (72, 182, 96, 204), skin)
    # neck
    rrect(d, (114, 108, 140, 128), 6, skin_sh)
    # hair back mass, head, ear
    ell(d, (78, 22, 182, 122), hair)
    ell(d, (72, 34, 170, 126), skin)
    ell(d, (152, 70, 172, 94), skin)
    ell(d, (157, 76, 166, 88), skin_sh, outline=False)
    # hair on top / fringe (swept to the left)
    poly(d, [(76, 64), (82, 34), (110, 18), (150, 18), (178, 40), (184, 72), (166, 66),
             (150, 50), (126, 56), (104, 50), (92, 62)], hair)
    # eyes looking left, eyebrows (worried)
    ell(d, (90, 76, 102, 92), (30, 30, 30, 255), outline=False)
    ell(d, (118, 76, 130, 92), (30, 30, 30, 255), outline=False)
    ell(d, (92, 78, 96, 83), (255, 255, 255, 255), outline=False)
    ell(d, (120, 78, 124, 83), (255, 255, 255, 255), outline=False)
    d.line(sc(86, 72, 102, 66), fill=hair, width=4 * S)
    d.line(sc(116, 66, 132, 70), fill=hair, width=4 * S)
    # nose and nervous mouth
    d.line(sc(94, 110, 100, 107, 106, 110, 112, 107), fill=LINE, width=OW // 2, joint="curve")
    # sweat drop
    poly(d, [(150, 46), (144, 60), (150, 66), (156, 60)], (140, 205, 255, 255))
    return finish(img, "Player.png")


def aunt():
    img = Image.new("RGBA", (SIZE * S, SIZE * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    skin, skin_sh = (240, 190, 155, 255), (215, 158, 122, 255)
    dress, dress_dark = (230, 60, 140, 255), (190, 40, 110, 255)
    hair, hair_hi = (130, 40, 70, 255), (165, 62, 98, 255)
    gold = (235, 190, 60, 255)

    # legs and shoes
    rrect(d, (104, 214, 120, 238), 6, skin_sh)
    rrect(d, (134, 214, 150, 238), 6, skin_sh)
    ell(d, (94, 230, 124, 246), (120, 30, 60, 255))
    ell(d, (128, 230, 158, 246), (120, 30, 60, 255))
    # back arm with handbag
    rrect(d, (156, 132, 178, 192), 11, dress_dark)
    rrect(d, (156, 180, 192, 214), 8, gold)
    d.arc(sc(162, 164, 186, 196), 180, 360, fill=LINE, width=OW // 2)
    # dress (A-line)
    poly(d, [(100, 124), (156, 124), (180, 220), (76, 220)], dress)
    poly(d, [(100, 124), (156, 124), (162, 150), (94, 150)], dress_dark, outline=False)
    d.line(sc(100, 124, 156, 124), fill=LINE, width=OW)
    # polka dots
    for x, y in [(104, 172), (130, 190), (152, 168), (118, 204), (160, 202), (96, 198)]:
        ell(d, (x - 5, y - 5, x + 5, y + 5), (255, 200, 225, 255), outline=False)
    # front arm reaching LEFT (for the cheek pinch)
    poly(d, [(104, 132), (60, 146), (62, 166), (108, 156)], dress)
    ell(d, (40, 140, 66, 166), skin)
    # neck and pearls
    rrect(d, (114, 108, 142, 128), 6, skin_sh)
    for i, x in enumerate(range(108, 150, 8)):
        y = 126 + (4 if 0 < i < 5 else 0)
        ell(d, (x - 4, y - 4, x + 4, y + 4), (250, 248, 240, 255))
    # big curly hair behind the head
    for cx, cy, r in [(150, 40, 30), (170, 72, 28), (164, 104, 24), (118, 32, 28),
                      (86, 36, 26), (142, 28, 22), (176, 46, 22)]:
        ell(d, (cx - r, cy - r, cx + r, cy + r), hair)
    # head and ear with gold earring
    ell(d, (74, 38, 168, 128), skin)
    ell(d, (150, 72, 168, 94), skin)
    ell(d, (155, 92, 165, 102), gold)
    # curls on top (fringe)
    for cx, cy, r in [(86, 50, 14), (104, 40, 15), (124, 36, 15), (144, 42, 15), (160, 56, 13)]:
        ell(d, (cx - r, cy - r, cx + r, cy + r), hair)
    for cx, cy in [(106, 36), (126, 32), (146, 38)]:
        ell(d, (cx - 4, cy - 4, cx + 4, cy + 4), hair_hi, outline=False)
    # glasses on the nose, eyes looking left
    ell(d, (84, 72, 106, 94), (255, 255, 255, 120))
    ell(d, (112, 72, 134, 94), (255, 255, 255, 120))
    d.line(sc(106, 82, 112, 82), fill=LINE, width=OW // 2)
    ell(d, (86, 78, 96, 90), (30, 30, 30, 255), outline=False)
    ell(d, (114, 78, 124, 90), (30, 30, 30, 255), outline=False)
    # raised eyebrows (curious), blush, red lipstick smile
    d.arc(sc(84, 60, 106, 72), 200, 340, fill=hair, width=3 * S)
    d.arc(sc(112, 60, 134, 72), 200, 340, fill=hair, width=3 * S)
    ell(d, (78, 96, 92, 106), (245, 140, 150, 200), outline=False)
    ell(d, (124, 96, 140, 106), (245, 140, 150, 200), outline=False)
    d.chord(sc(92, 100, 116, 118), 0, 180, fill=(200, 30, 60, 255), outline=LINE, width=OW // 2)
    return finish(img, "Doda.png")


p = player()
a = aunt()
# side-by-side preview on a floor colour
prev = Image.new("RGBA", (SIZE * 2 + 30, SIZE + 20), (205, 170, 125, 255))
prev.alpha_composite(p, (10, 10))
prev.alpha_composite(a, (SIZE + 20, 10))
prev.save(os.path.join(OUT, "preview.png"))
print("done")
