"""Hall interior, walls, fences, surrounding forest and light pools."""
import math
import random

from lib import *
import layout as L
from ground import (cells, rects, tile_field, small_plant, STONE, STONE_LINE, ROCK, ROCK_LINE, WOOD, WOOD_LINE,
                    LEAF, LEAF2, LEAF_DARK, FOREST, FOREST2, FLOWERS, WARM, GRASS_LINE, CONC, CONC_D, BRICK,
                    BRICK_LINE, lantern)

HX0, HX1, HY0, HY1 = 23.0, 65.0, 7.0, 25.0
WALL_H = 5.0                    # back wall height on screen
FLOOR = [C('#716c8a'), C('#6a6583'), C('#797492')]
GROUT = C('#544f6c')
PANEL, PANEL_D, PANEL_L = C('#5e4538'), C('#4a352b'), C('#735647')
WALL_TOP, WALL_FACE = C('#4b4359'), C('#6b5346')
GOLD = C('#e0ad4a')
BOUG = Pal('#d6408f', '#ee6fb0', '#a82a70', '#5c1840')
IVY = Pal('#4f9a52', '#72b866', '#3a7a44', '#1f4a2a')
BAMBOO, BAMBOO_D, BAMBOO_L = C('#dcbf80'), C('#a98548'), C('#ecd69c')


# ------------------------------------------------------------------- pieces
def vine(ctx, rng, x, y, length, pal, flowers=None, width=0.5):
    """Hanging plant: a ragged teardrop of small leaf bumps."""
    circ = []
    rows = max(3, int(length / 0.15))
    drift = 0.0
    for i in range(rows):
        t = i / (rows - 1)
        drift += rng.uniform(-0.05, 0.05)
        half = width * (1 - t) ** 0.7 + 0.03
        for _ in range(1 + int(half / 0.13)):
            circ.append((x + drift + rng.uniform(-half, half), y + t * length + rng.uniform(-0.05, 0.05),
                         rng.uniform(0.09, 0.17) * (1.15 - 0.45 * t)))
    foliage(ctx, rng, circ, pal, lw=0.024, leaves=False, sort=False)
    if flowers:
        for cx, cy, r in circ:
            if rng.random() < 0.35:
                ctx.ellipse(cx + rng.uniform(-r, r) * 0.5, cy + rng.uniform(-r, r) * 0.5, 0.04, 0.04)
        ctx.fill(flowers)


def stone_face(ctx, seed, x0, y0, x1, y1, sx=0.62, sy=0.44, cols=ROCK, mortar=C('#857c70')):
    if not ctx.sees(x0, y0, x1, y1):
        return
    rng = random.Random(seed)
    ctx.rect(x0, y0, x1 - x0, y1 - y0).fill(mortar)
    nx, ny = max(1, round((x1 - x0) / sx)), max(1, round((y1 - y0) / sy))
    V = [[(x0 + i * (x1 - x0) / nx + (rng.uniform(-0.17, 0.17) * sx if 0 < i < nx else 0),
           y0 + j * (y1 - y0) / ny + (rng.uniform(-0.17, 0.17) * sy if 0 < j < ny else 0))
          for j in range(ny + 1)] for i in range(nx + 1)]
    buckets = {}
    hi = []
    for i in range(nx):
        for j in range(ny):
            q = [V[i][j], V[i + 1][j], V[i + 1][j + 1], V[i][j + 1]]
            cx, cy = sum(p[0] for p in q) / 4, sum(p[1] for p in q) / 4
            q = [(cx + (px - cx) * 0.9, cy + (py - cy) * 0.86) for px, py in q]
            buckets.setdefault(rng.choice(cols), []).append(q)
            hi.append((q[0], q[1]))
    for col, lst in buckets.items():
        for q in lst:
            ctx.poly(q)
        ctx.fill(col)
    for a, b in hi:
        ctx.move_to(a[0] + 0.03, a[1] + 0.035).line_to(b[0] - 0.03, b[1] + 0.035)
    ctx.stroke(al(C('#ffffff'), 0.3), 0.022)
    ctx.rect(x0, y0, x1 - x0, y1 - y0).stroke(ROCK_LINE, 0.028)


def cap(ctx, x0, y0, x1, y1, col=None, step=0.9, horizontal=True):
    col = col or STONE[2]
    ctx.rect(x0, y0, x1 - x0, y1 - y0).fs(col, STONE_LINE, 0.025)
    if horizontal:
        x = x0 + step
        while x < x1 - 0.1:
            ctx.move_to(x, y0).line_to(x, y1)
            x += step
    else:
        y = y0 + step
        while y < y1 - 0.1:
            ctx.move_to(x0, y).line_to(x1, y)
            y += step
    ctx.stroke(al(STONE_LINE, 0.8), 0.014)
    if horizontal:
        ctx.rect(x0, y0, x1 - x0, (y1 - y0) * 0.3).fill(al(C('#ffffff'), 0.3))


def forest(ctx, seed, x0, y0, x1, y1, dens=0.75):
    if not ctx.sees(x0 - 1.5, y0 - 1.5, x1 + 1.5, y1 + 1.5):
        return
    rng = random.Random(seed)
    n = int((x1 - x0) * (y1 - y0) * dens)
    for pal, k in ((FOREST, n), (FOREST2, n // 2)):
        circ = [(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(0.6, 1.1)) for _ in range(k)]
        circ = [c for c in circ if ctx.sees(c[0] - 1.3, c[1] - 1.3, c[0] + 1.3, c[1] + 1.3)]
        foliage(ctx, rng, circ, pal, lw=0.045)


def bottle(ctx, x, y, h, col):
    w = 0.085
    ctx.rrect(x - w / 2, y - h * 0.7, w, h * 0.7, 0.02)
    ctx.rect(x - w * 0.2, y - h, w * 0.4, h * 0.32)
    ctx.fs(col, al(INK, 0.8), 0.011)
    ctx.rect(x - w * 0.3, y - h * 0.62, w * 0.18, h * 0.4).fill(al(C('#ffffff'), 0.45))


def shelf(ctx, rng, x0, y0, w, h, cols=8, rows=4):
    glow(ctx, x0 + w / 2, y0 + h / 2, w * 0.72, h * 0.95, C('#ff9a2e'), 0.4, steps=14)
    ctx.rect(x0 - 0.12, y0 - 0.12, w + 0.24, h + 0.24).fs(C('#2a1d18'), INK, 0.03)
    cw, ch = w / cols, h / rows
    bcols = [C('#3d2a1c'), C('#2f4a2f'), C('#6b3a1e'), C('#f6efe0'), C('#274060'), C('#8a2a2a')]
    for r in range(rows):
        for c in range(cols):
            cx, cy = x0 + c * cw, y0 + r * ch
            for i in range(5):
                ctx.rect(cx + 0.035, cy + 0.035 + i * (ch - 0.07) / 5, cw - 0.07, (ch - 0.07) / 5 + 0.004)
                ctx.fill(mix(C('#ffe29a'), C('#f28a22'), i / 4))
            n = rng.randint(2, 4)
            for k in range(n):
                bx = cx + 0.16 + k * (cw - 0.32) / max(n - 1, 1)
                bottle(ctx, bx, cy + ch - 0.045, rng.uniform(0.3, 0.46), rng.choice(bcols))
            ctx.rect(cx + 0.035, cy + ch - 0.06, cw - 0.07, 0.03).fill(al(C('#7a3d10'), 0.6))


def door(ctx, x, y_floor, w=1.7, h=2.7, col=C('#d8d0c2'), sign=True):
    y = y_floor - h
    ctx.rect(x - 0.1, y - 0.1, w + 0.2, h + 0.1).fs(C('#2f2520'), INK, 0.028)
    for k in (0, 1):
        lx = x + k * w / 2
        ctx.rect(lx + 0.02, y, w / 2 - 0.04, h).fs(col, INK, 0.022)
        ctx.rect(lx + 0.12, y + h * 0.5, w / 2 - 0.24, h * 0.4).stroke(al(INK, 0.35), 0.016)
        ctx.ellipse(lx + w / 4, y + h * 0.26, 0.2, 0.2).fs(C('#9fd4e6'), INK, 0.022)
        ctx.arc(lx + w / 4, y + h * 0.26, 0.12, 0.12, math.pi * 1.1, math.pi * 1.6, n=6).stroke(C('#ffffff'), 0.02)
        hx = lx + (w / 2 - 0.14 if k == 0 else 0.14)
        ctx.rrect(hx - 0.03, y + h * 0.5, 0.06, 0.34, 0.03).fs(C('#c9c9d2'), INK, 0.014)
    if sign:
        glow(ctx, x + w / 2, y - 0.32, 0.6, 0.35, C('#6dff9a'), 0.3, steps=8)
        ctx.rrect(x + w / 2 - 0.36, y - 0.46, 0.72, 0.26, 0.04).fs(C('#2fbf6a'), INK, 0.02)
        ctx.rect(x + w / 2 - 0.24, y - 0.37, 0.2, 0.08).fill(C('#ffffff'))
        ctx.poly([(x + w / 2 + 0.02, y - 0.4), (x + w / 2 + 0.2, y - 0.33), (x + w / 2 + 0.02, y - 0.26)]).fill(C('#ffffff'))


def sconce(ctx, x, y):
    glow(ctx, x, y, 0.75, 1.15, C('#ffc875'), 0.45, steps=12)
    ctx.poly([(x - 0.13, y - 0.16), (x + 0.13, y - 0.16), (x + 0.08, y + 0.16), (x - 0.08, y + 0.16)]).fs(C('#fff1c4'), INK, 0.02)
    ctx.rect(x - 0.05, y + 0.16, 0.1, 0.1).fs(GOLD, INK, 0.016)


def curtain(ctx, x0, y0, w, h, col):
    ctx.rect(x0, y0, w, h).fill(col)
    n = int(w / 0.46)
    fw = w / n
    for i in range(n):
        xx = x0 + i * fw
        ctx.rect(xx + fw * 0.08, y0, fw * 0.34, h)
    ctx.fill(lt(col, 0.13))
    for i in range(n):
        xx = x0 + i * fw
        ctx.rect(xx + fw * 0.66, y0, fw * 0.34, h)
    ctx.fill(dk(col, 0.28))
    # fairy-light curtain
    rng = random.Random(5)
    for i in range(n * 2):
        xx = x0 + (i + 0.5) * fw / 2
        ctx.move_to(xx, y0).line_to(xx, y0 + h * rng.uniform(0.75, 0.98))
    ctx.stroke(al(C('#ffe7a8'), 0.25), 0.012)
    for i in range(n * 2):
        xx = x0 + (i + 0.5) * fw / 2
        for k in range(9):
            ctx.ellipse(xx, y0 + 0.2 + k * h / 9.6 + rng.uniform(-0.1, 0.1), 0.03, 0.03)
    ctx.fill(C('#fff3c9'))
    # valance swags
    sw = w / 7
    for i in range(7):
        ctx.move_to(x0 + i * sw, y0)
        ctx.arc(x0 + (i + 0.5) * sw, y0, sw / 2, 0.55, math.pi, 0, n=14, move=False)
        ctx.close()
    ctx.fs(dk(col, 0.12), INK, 0.022)
    for i in range(7):
        ctx.arc(x0 + (i + 0.5) * sw, y0, sw / 2 * 0.7, 0.33, math.pi, 0, n=10)
    ctx.stroke(al(INK, 0.4), 0.014)
    for i in range(8):
        ctx.ellipse(x0 + i * sw, y0 + 0.08, 0.09, 0.09)
    ctx.fs(GOLD, INK, 0.016)
    ctx.rect(x0, y0, w, h).stroke(INK, 0.03)


# ------------------------------------------------------------------- hall
def draw_hall(ctx):
    if not ctx.sees(HX0 - 1, 1, HX1 + 1, HY1 + 1):
        return
    rng = random.Random(900)
    tile_field(ctx, rng, HX0, HY0, HX1, HY1, 2.0, 1.24, FLOOR, GROUT, gap=0.03, stagger=0.0)
    # glossy reflections
    ctx.rect(HX0, HY0, HX1 - HX0, HY1 - HY0).clip_here()
    for _ in range(60):
        x, y = rng.uniform(HX0, HX1), rng.uniform(HY0, HY1)
        w = rng.uniform(0.15, 0.5)
        ctx.poly([(x, y), (x + w, y), (x + w - 0.9, y + 1.24), (x - 0.9, y + 1.24)])
    ctx.fill(al(C('#ffffff'), 0.055))
    for i in range(12):                                   # warm wash coming from the back wall
        ctx.rect(HX0, HY0, HX1 - HX0, 4.2 * (1 - i / 12)).fill(al(C('#ff9a3c'), 0.028))
    ctx.unclip()
    pools = [(28, 12.5, '#9a5cff'), (34, 20.5, '#4d8dff'), (29, 21.5, '#ff5fb5'), (54, 21, '#9a5cff'),
             (60, 12.8, '#4d8dff'), (59.5, 21.5, '#ff5fb5'), (33.5, 14.5, '#4d8dff'), (54.5, 14.5, '#ff5fb5'),
             (44, 21.6, '#9a5cff'), (25.5, 17.0, '#4d8dff'), (62.5, 17.5, '#9a5cff')]
    for x, y, col in pools:
        glow(ctx, x, y, 2.9, 1.8, C(col), 0.34, steps=16)

    # --- dance floor
    dx0, dy0, cols_, rows_ = 37.0, 12.0, 14, 12
    cw, ch = 1.0, F
    dw, dh = cols_ * cw, rows_ * ch
    ctx.rect(dx0 - 0.32, dy0 - 0.2, dw + 0.64, dh + 0.5).fill(al(INK, 0.3))
    ctx.rect(dx0 - 0.28, dy0 - 0.2, dw + 0.56, dh + 0.4).fs(GOLD, INK, 0.03)
    ctx.rect(dx0, dy0, dw, dh).fill(C('#2f2b3d'))
    for r in range(rows_):
        for c in range(cols_):
            if (r + c) % 2 == 0:
                ctx.rect(dx0 + c * cw, dy0 + r * ch, cw, ch)
    ctx.fill(C('#f4f0f8'))
    ctx.rect(dx0, dy0, dw, dh).clip_here()
    for x in (39.5, 44.5, 46.0, 50.5):
        w = 0.5 if x != 44.5 else 1.1
        ctx.poly([(x, dy0), (x + w, dy0), (x + w - 5.5, dy0 + dh), (x - 5.5, dy0 + dh)])
    ctx.fill(al(C('#ffffff'), 0.16))
    glow(ctx, 40.0, 14.0, 3.0, 1.8, C('#ff5fb5'), 0.25)
    glow(ctx, 48.0, 17.6, 3.0, 1.8, C('#4d8dff'), 0.25)
    ctx.unclip()
    ctx.rect(dx0, dy0, dw, dh).stroke(INK, 0.03)
    # monogram medallion
    mx, my = dx0 + dw / 2, dy0 + dh / 2
    ctx.ellipse(mx, my, 2.35, 2.35 * F).fs(GOLD, INK, 0.028)
    ctx.ellipse(mx, my, 2.1, 2.1 * F).fs(C('#fbf7ff'), al(INK, 0.6), 0.02)
    ctx.ellipse(mx, my, 1.85, 1.85 * F).stroke(GOLD, 0.04)
    ctx.move_to(mx, my + 0.62)                              # heart
    ctx.curve_to(mx - 1.5, my - 0.1, mx - 0.7, my - 0.95, mx, my - 0.3)
    ctx.curve_to(mx + 0.7, my - 0.95, mx + 1.5, my - 0.1, mx, my + 0.62)
    ctx.close().fs(C('#f27aa0'), C('#8a2a4f'), 0.028)
    ctx.arc(mx - 0.42, my - 0.2, 0.25, 0.16, math.pi * 1.05, math.pi * 1.7, n=8).stroke(al(C('#ffffff'), 0.8), 0.04)

    # --- red carpet from the main opening
    cx0, cx1, cy0, cy1 = 42.8, 45.2, dy0 + dh + 0.36, 24.8
    ctx.rect(cx0 + 0.05, cy0 + 0.08, cx1 - cx0, cy1 - cy0).fill(al(INK, 0.22))
    ctx.rect(cx0, cy0, cx1 - cx0, cy1 - cy0).fs(C('#a5304e'), INK, 0.025)
    ctx.rect(cx0 + 0.14, cy0, 0.1, cy1 - cy0)
    ctx.rect(cx1 - 0.24, cy0, 0.1, cy1 - cy0)
    ctx.fill(GOLD)
    y = cy0 + 0.3
    while y < cy1 - 0.3:
        ctx.poly([(44, y), (44.5, y + 0.22), (44, y + 0.44), (43.5, y + 0.22)])
        y += 0.62
    ctx.fill(C('#c14a68'))

    # --- stage
    sx0, sx1, sy1 = 37.0, 51.0, 9.3
    ctx.rect(sx0 - 1.1, sy1 - 0.3, sx1 - sx0 + 2.2, 0.95).fill(al(INK, 0.28))
    for i, (xa, xb, f) in enumerate(((sx0 - 1.1, sx0 - 0.55, 0.14), (sx0 - 0.55, sx0, 0.27),
                                     (sx1 + 0.55, sx1 + 1.1, 0.14), (sx1, sx1 + 0.55, 0.27))):
        ctx.rect(xa, HY0, xb - xa, sy1 - 0.4 - HY0).fs(C('#565066'), INK, 0.022)
        ctx.rect(xa, sy1 - 0.4, xb - xa, f).fs(C('#353041'), INK, 0.022)
    ctx.rect(sx0, HY0, sx1 - sx0, sy1 - HY0).fs(C('#474056'), INK, 0.028)
    x = sx0 + 0.7
    while x < sx1:
        ctx.move_to(x, HY0).line_to(x, sy1)
        x += 0.7
    ctx.stroke(al(INK, 0.3), 0.014)
    ctx.rect(sx0, HY0, sx1 - sx0, 1.2).fill(al(C('#b06cff'), 0.12))
    ctx.rect(sx0, sy1, sx1 - sx0, 0.42).fs(C('#2c2738'), INK, 0.028)
    glow(ctx, 44, sy1 + 0.5, 7.5, 0.7, C('#ff5fd0'), 0.3, steps=10)
    ctx.rect(sx0 + 0.12, sy1 + 0.15, sx1 - sx0 - 0.24, 0.09).fill(C('#ff9be6'))
    for x in (38.2, 40.6, 43.0, 45.0, 47.4, 49.8):          # floor uplights on the stage edge
        ctx.rrect(x - 0.16, sy1 - 0.3, 0.32, 0.2, 0.05).fs(C('#22202b'), INK, 0.018)
        ctx.ellipse(x, sy1 - 0.24, 0.1, 0.05).fill(C('#d9b8ff'))

    # thresholds of the two side doors
    for x, ya in ((HX0 - 0.15, 14.0), (HX1 - 0.75, 13.0)):
        ctx.rect(x, ya - 0.1, 0.9, 3.1).fs(STONE[1], STONE_LINE, 0.022)
    # sill + plinths along the open front
    ctx.rect(HX0, HY1 - 0.16, HX1 - HX0, 0.36).fs(STONE[3], STONE_LINE, 0.025)
    ctx.move_to(HX0, HY1 - 0.02).line_to(HX1, HY1 - 0.02)
    ctx.stroke(al(INK, 0.45), 0.02)
    for name, x, y, mark in L.PROPS:
        if mark == 'plinth':
            ctx.ellipse(x + 0.05, y + 0.12, 0.6, 0.2).fill(al(INK, 0.25))
            ctx.rrect(x - 0.46, y - 0.34, 0.92, 0.5, 0.05).fs(STONE[2], STONE_LINE, 0.025)
            ctx.rrect(x - 0.46, y + 0.02, 0.92, 0.14, 0.03).fill(al(INK, 0.15))


def back_wall(ctx):
    y0, y1 = HY0 - WALL_H, HY0
    if not ctx.sees(HX0, y0 - 1, HX1, y1):
        return
    rng = random.Random(910)
    ctx.rect(HX0, y0, HX1 - HX0, WALL_H).fill(PANEL)
    x = HX0
    i = 0
    while x < HX1:
        ctx.rect(x, y0, 0.11, WALL_H)
        x += 0.25
    ctx.fill(PANEL_D)
    x = HX0 + 0.11
    while x < HX1:
        ctx.rect(x, y0, 0.035, WALL_H)
        x += 0.25
    ctx.fill(al(PANEL_L, 0.8))
    # warm up-lighting along the bottom of the wall
    for i in range(8):
        ctx.rect(HX0, y1 - 1.6 * (1 - i / 8), HX1 - HX0, 1.6 * (1 - i / 8)).fill(al(C('#ffb060'), 0.035))
    # shelves, curtain, doors
    shelf(ctx, rng, 26.6, y0 + 1.25, 8.0, 3.0)
    shelf(ctx, rng, 53.4, y0 + 1.25, 8.0, 3.0)
    glow(ctx, 44, y0 + 2.8, 8.6, 2.9, C('#b06cff'), 0.35, steps=12)
    ctx.rect(36.7, y0 + 0.75, 14.6, 4.05).fs(GOLD, INK, 0.03)
    curtain(ctx, 36.95, y0 + 0.98, 14.1, 3.82, C('#4a2f86'))
    door(ctx, 23.95, y1, sign=True)
    door(ctx, 62.6, y1, col=C('#b9c0c8'), sign=False)
    ctx.rrect(62.95, y1 - 3.3, 1.0, 0.3, 0.04).fs(C('#2a2430'), INK, 0.018)       # little "kitchen" plate
    for k in range(4):
        ctx.rect(63.07 + k * 0.2, y1 - 3.2, 0.12, 0.1)
    ctx.fill(C('#e9e2d2'))
    for x in (26.05, 35.25, 35.95, 52.05, 52.75, 61.95):
        sconce(ctx, x, y0 + 2.5)
    # baseboard + top beam
    ctx.rect(HX0, y1 - 0.26, 0.95, 0.26)
    ctx.rect(25.75, y1 - 0.26, 10.25, 0.26)
    ctx.rect(52.0, y1 - 0.26, 10.5, 0.26)
    ctx.rect(64.4, y1 - 0.26, 0.6, 0.26)
    ctx.fs(C('#33251f'), INK, 0.02)
    ctx.rect(HX0, y0, HX1 - HX0, 0.5).fs(C('#3a2a24'), INK, 0.028)
    ctx.rect(HX0, y0 + 0.5, HX1 - HX0, 0.09).fill(al(C('#000000'), 0.25))
    cap(ctx, HX0 - 0.15, y0 - 0.55, HX1 + 0.15, y0, col=C('#8a7468'), step=1.4)
    # hanging greenery garland with bulbs
    circ = []
    x = HX0 + 0.3
    while x < HX1 - 0.2:
        circ.append((x, y0 + 0.52 + rng.uniform(0, 0.16), rng.uniform(0.22, 0.38)))
        x += rng.uniform(0.28, 0.42)
    foliage(ctx, rng, circ, IVY, lw=0.028, leaves=False, sort=False)
    x = HX0 + 0.6
    while x < HX1 - 0.4:
        if not (36.5 < x < 51.5):
            ln = rng.uniform(0.35, 1.0)
            ctx.move_to(x, y0 + 0.7).line_to(x, y0 + 0.7 + ln)
            ctx.stroke(al(INK, 0.7), 0.012)
            glow(ctx, x, y0 + 0.76 + ln, 0.3, 0.3, WARM, 0.5, steps=6)
            ctx.ellipse(x, y0 + 0.76 + ln, 0.065, 0.08).fs(C('#fff3c2'), al(INK, 0.6), 0.012)
        else:
            if rng.random() < 0.5:
                vine(ctx, rng, x, y0 + 0.7, rng.uniform(0.3, 0.6), IVY, width=0.3)
        x += rng.uniform(0.5, 0.9)
    ctx.rect(HX0, y0, HX1 - HX0, WALL_H).stroke(INK, 0.03)


def side_wall(ctx, x, ya, yb, t=0.6, cut=1.0):
    ctx.rect(x + t, ya - cut + 0.3, 0.3, yb - ya).fill(al(INK, 0.16))            # cast shadow on the floor
    ctx.rect(x, ya - cut, t, yb - ya).fs(WALL_TOP, INK, 0.028)
    ctx.rect(x + 0.1, ya - cut, 0.12, yb - ya).fill(al(C('#ffffff'), 0.12))
    y = ya - cut + 0.5
    while y < yb - cut:
        ctx.move_to(x, y).line_to(x + t, y)
        y += 1.0
    ctx.stroke(al(INK, 0.35), 0.014)
    ctx.rect(x, yb - cut, t, cut).fs(WALL_FACE, INK, 0.028)
    ctx.rect(x + 0.08, yb - cut + 0.08, t - 0.16, cut - 0.3).stroke(al(INK, 0.35), 0.016)
    ctx.rect(x, yb - 0.16, t, 0.16).fill(C('#33251f'))


def glass_front(ctx, x0, x1):
    y0, y1 = HY1 - 1.0, HY1 + 0.04
    ctx.rect(x0, y0, x1 - x0, y1 - y0).fill(al(C('#bfe9f5'), 0.3))
    x = x0 + 0.3
    while x < x1 - 0.6:
        ctx.poly([(x, y0 + 0.08), (x + 0.22, y0 + 0.08), (x - 0.25, y1 - 0.08), (x - 0.47, y1 - 0.08)])
        x += 1.1
    ctx.fill(al(C('#ffffff'), 0.4))
    n = round((x1 - x0) / 1.7)
    for i in range(n + 1):
        xx = x0 + i * (x1 - x0) / n
        ctx.rect(xx - 0.045, y0, 0.09, y1 - y0)
    ctx.rect(x0, y0 - 0.05, x1 - x0, 0.11)
    ctx.rect(x0, y1 - 0.1, x1 - x0, 0.1)
    ctx.fs(C('#3a3346'), INK, 0.016)


def bamboo_face(ctx, seed, x0, y0, x1, y1):
    if not ctx.sees(x0, y0 - 1, x1, y1):
        return
    rng = random.Random(seed)
    ctx.rect(x0, y0, x1 - x0, y1 - y0).fill(BAMBOO)
    x = x0
    while x < x1:
        t = rng.random()
        if t < 0.3:
            ctx.rect(x, y0, 0.115, y1 - y0)
        x += 0.115
    ctx.fill(BAMBOO_L)
    x = x0
    while x < x1:
        ctx.move_to(x, y0).line_to(x, y1)
        x += 0.115
    ctx.stroke(al(BAMBOO_D, 0.75), 0.016)
    for _ in range(int((x1 - x0) * 5)):                         # bamboo nodes
        x = x0 + rng.randrange(int((x1 - x0) / 0.115)) * 0.115
        y = rng.uniform(y0 + 0.1, y1 - 0.1)
        ctx.move_to(x + 0.01, y).line_to(x + 0.105, y)
    ctx.stroke(al(BAMBOO_D, 0.9), 0.02)
    for yy in (y0 + 0.5, y1 - 0.6):                             # ties
        ctx.rect(x0, yy, x1 - x0, 0.1).fs(C('#8a6a3c'), al(INK, 0.7), 0.016)
    for i in range(6):
        ctx.rect(x0, y1 - 0.5 * (1 - i / 6), x1 - x0, 0.5 * (1 - i / 6)).fill(al(C('#6a4a20'), 0.04))
    ctx.rect(x0, y0, x1 - x0, y1 - y0).stroke(INK, 0.028)
    x = x0
    n = round((x1 - x0) / 3.3)
    for i in range(n + 1):                                      # posts
        xx = x0 + i * (x1 - x0) / n
        ctx.rect(xx - 0.15, y0 - 0.2, 0.3, y1 - y0 + 0.2).fs(WOOD[3], INK, 0.025)
        ctx.rect(xx - 0.1, y0 - 0.2, 0.07, y1 - y0 + 0.2).fill(al(C('#ffffff'), 0.2))
        ctx.rrect(xx - 0.2, y0 - 0.32, 0.4, 0.16, 0.04).fs(WOOD[1], INK, 0.022)
    ctx.rect(x0, y0 - 0.06, x1 - x0, 0.14).fs(WOOD[1], INK, 0.022)


def gate_pillar(ctx, x0, x1, ytop):
    stone_face(ctx, int(x0 * 13), x0, ytop + 0.5, x1, 64.2, sx=0.45, sy=0.4, cols=STONE)
    ctx.poly([(x0 - 0.12, ytop + 0.5), (x1 + 0.12, ytop + 0.5), (x1 + 0.12, ytop + 0.2), (x1 - 0.1, ytop),
              (x0 + 0.1, ytop), (x0 - 0.12, ytop + 0.2)]).fs(STONE[2], INK, 0.028)
    ctx.move_to(x0 - 0.12, ytop + 0.2).line_to(x1 + 0.12, ytop + 0.2)
    ctx.stroke(al(INK, 0.5), 0.016)
    lantern(ctx, (x0 + x1) / 2, ytop + 0.02, 1.25)


def draw_walls(ctx):
    rng = random.Random(920)
    # ---------- north: forest, garden walls, hall back wall
    forest(ctx, 1, -0.5, -0.6, 80.5, 1.0)
    bamboo_face(ctx, 2, 2.45, 1.3, HX0, 4.0)
    stone_face(ctx, 3, HX1, 1.3, 77.6, 4.0)
    cap(ctx, HX1, 0.95, 77.75, 1.32)
    back_wall(ctx)
    if ctx.sees(0, 0, 80, 6):
        for x, ln, pal, fl in ((4.4, 1.6, IVY, None), (7.6, 1.1, BOUG, C('#ff9fd0')), (8.3, 1.9, BOUG, C('#ff9fd0')),
                               (12.2, 1.3, IVY, None), (17.2, 2.1, IVY, C('#fff5e6')), (18.0, 1.2, IVY, None),
                               (21.6, 1.7, BOUG, C('#ff9fd0')), (66.2, 2.0, BOUG, C('#ff9fd0')),
                               (67.0, 1.2, BOUG, C('#ff9fd0')), (68.6, 1.6, IVY, None), (73.6, 2.2, IVY, C('#fff5e6')),
                               (74.4, 1.3, IVY, None), (76.6, 1.9, BOUG, C('#ff9fd0'))):
            vine(ctx, rng, x, 1.15, ln, pal, fl, width=0.62)
        for x in (10.4, 14.6, 20.0):                                    # lanterns hung on the bamboo fence
            ctx.move_to(x, 1.4).line_to(x, 2.2)
            ctx.stroke(INK, 0.014)
            lantern(ctx, x, 2.72, 1.1)
        # wall fountain
        fx = 71.0
        ctx.rrect(fx - 0.75, 1.75, 1.5, 1.7, 0.7).fs(STONE[2], STONE_LINE, 0.028)
        ctx.rrect(fx - 0.55, 1.95, 1.1, 1.3, 0.5).fs(STONE[0], al(STONE_LINE, 0.7), 0.018)
        ctx.ellipse(fx, 2.6, 0.26, 0.26).fs(C('#b99a5a'), INK, 0.022)
        ctx.ellipse(fx - 0.09, 2.54, 0.04, 0.04)
        ctx.ellipse(fx + 0.09, 2.54, 0.04, 0.04)
        ctx.fill(INK)
        ctx.ellipse(fx, 2.72, 0.07, 0.05).fill(C('#3a2a1a'))
        ctx.poly([(fx - 0.06, 2.74), (fx + 0.06, 2.74), (fx + 0.11, 4.25), (fx - 0.11, 4.25)]).fill(al(C('#a5e1e8'), 0.9))
        ctx.move_to(fx - 0.01, 2.8).line_to(fx - 0.03, 4.2)
        ctx.stroke(C('#ffffff'), 0.02)
    # ---------- hall side walls + glass front
    if ctx.sees(HX0 - 1, 4, HX1 + 1, 26):
        side_wall(ctx, HX0, HY0, 14.0)
        side_wall(ctx, HX0, 17.0, HY1)
        side_wall(ctx, HX1 - 0.6, HY0, 13.0)
        side_wall(ctx, HX1 - 0.6, 16.0, HY1)
        glass_front(ctx, HX0 + 0.6, 28.55)
        glass_front(ctx, 59.45, HX1 - 0.6)
    # ---------- west fence / east wall strips (seen from above)
    if ctx.sees(0, 0, 4, 64):
        ctx.rect(2.45, 2.6, 0.55, 58.2).fs(BAMBOO, INK, 0.026)
        y = 2.7
        while y < 60.7:
            ctx.move_to(2.45, y).line_to(3.0, y)
            y += 0.115
        ctx.stroke(al(BAMBOO_D, 0.6), 0.014)
        ctx.rect(2.5, 2.6, 0.14, 58.2).fill(al(C('#ffffff'), 0.25))
        y = 4.0
        while y < 60.7:
            ctx.rrect(2.36, y - 0.5, 0.72, 0.5, 0.05).fs(WOOD[1], INK, 0.024)
            ctx.rrect(2.36, y - 0.5, 0.72, 0.16, 0.05).fill(al(C('#ffffff'), 0.25))
            y += 3.3
    if ctx.sees(76, 0, 80, 64):
        cap(ctx, 77.05, 1.0, 77.75, 60.75, step=0.85, horizontal=False)
        ctx.rect(77.12, 1.0, 0.16, 59.7).fill(al(C('#ffffff'), 0.28))
    # ---------- south wall: cap + outer face, gate in the middle
    for xa, xb, seed in ((2.3, 40.2, 5), (47.8, 77.75, 6)):
        stone_face(ctx, seed, xa, 61.2, xb, 64.2)
        cap(ctx, xa, 60.6, xb, 61.25)
    if ctx.sees(38, 58, 50, 64):
        for i in range(6):                                              # shade where the path passes the wall
            ctx.rect(41.0, 60.9, 6.0, 1.3 * (1 - i / 6)).fill(al(INK, 0.06))
        ctx.rect(40.95, 60.85, 6.1, 0.34).fs(STONE[1], STONE_LINE, 0.025)
        gate_pillar(ctx, 40.1, 41.0, 59.85)
        gate_pillar(ctx, 47.0, 47.9, 59.85)
        for xh, d in ((41.0, 1), (47.0, -1)):                          # open iron gate leaves
            pts = [(xh, 61.2), (xh + d * 0.5, 61.7), (xh + d * 0.5, 64.2), (xh, 64.2)]
            ctx.poly(pts).fs(al(C('#2a2630'), 0.35), INK, 0.03)
            for k in range(1, 5):
                xx = xh + d * 0.1 * k
                ctx.move_to(xx, 61.2 + 0.1 * k).line_to(xx, 64.2)
            ctx.stroke(INK, 0.022)
    if ctx.sees(0, 59, 80, 64):
        r2 = random.Random(930)
        x = 3.5
        while x < 77:
            if not (39 < x < 49):
                vine(ctx, r2, x, 61.2, r2.uniform(0.8, 2.4), r2.choice([IVY, IVY, BOUG]), None, width=r2.uniform(0.5, 0.8))
            x += r2.uniform(1.2, 3.6)
    # ---------- side forests go last so the canopies lean over the fences
    forest(ctx, 7, -0.5, -0.5, 1.5, 64.5)
    forest(ctx, 8, 78.6, -0.5, 80.5, 64.5)


def draw_light(ctx):
    for name, x, y, mark in L.PROPS:
        if not ctx.sees(x - 4, y - 3, x + 4, y + 3):
            continue
        if name == 'lamp_post':
            glow(ctx, x, y + 0.1, 2.6, 1.6, WARM, 0.2, steps=14)
        elif name == 'bollard_light':
            glow(ctx, x, y + 0.05, 0.9, 0.55, WARM, 0.25, steps=8)
        elif name == 'pillar_wood':
            glow(ctx, x, y + 0.5, 1.6, 0.9, WARM, 0.18, steps=10)
