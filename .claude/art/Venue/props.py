"""Stand-alone prop sprites (transparent background, pivot = base point on the ground)."""
import math
import random

import numpy as np
from PIL import Image

from lib import *
from ground import small_plant, WOOD, WOOD_LINE, STONE, STONE_LINE, FLOWERS, WARM, LEAF, LEAF2, LEAF_DARK

EUC = Pal('#7fae8a', '#98c29c', '#5d8b73', '#2c4a3c')
EUC_BACK = Pal('#699a78', '#7fae8a', '#4e7a64', '#2c4a3c')
OLIVE = Pal('#97b282', '#b2c99a', '#748f68', '#37493a')
OLIVE_BACK = Pal('#819d72', '#97b282', '#627c5a', '#37493a')
CITRUS = Pal('#4f9d4e', '#73bb63', '#387e42', '#1d4a2a')
CYPRESS = Pal('#3f8253', '#5a9e66', '#2c6642', '#173b27')
BUSH = Pal('#5aa552', '#80c46b', '#3f8546', '#224f2d')
METAL, METAL_L = C('#3a3542'), C('#6a6478')


def limb(pts, w0, w1, sub=8):
    """Tapered ribbon polygon around a spline centre line."""
    c = spline_pts(pts, closed=False, sub=sub)
    n = len(c)
    left, right = [], []
    for i, (x, y) in enumerate(c):
        x0, y0 = c[max(i - 1, 0)]
        x1, y1 = c[min(i + 1, n - 1)]
        dx, dy = x1 - x0, y1 - y0
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        w = (w0 + (w1 - w0) * i / (n - 1)) / 2
        left.append((x + nx * w, y + ny * w))
        right.append((x - nx * w, y - ny * w))
    return left + right[::-1]


def woody(ctx, limbs, fill, line, lw=0.035):
    for p in limbs:
        ctx.poly(p).stroke(line, lw * 2)
    for p in limbs:
        ctx.poly(p).fill(fill)


def bulb(ctx, x, y, r=0.07, g=0.32, a=0.55):
    glow(ctx, x, y, g, g, WARM, a, steps=8)
    ctx.ellipse(x, y, r, r * 1.2).fs(C('#fff4c8'), al(INK, 0.7), 0.012)


# -------------------------------------------------------------------- trees
def tree_eucalyptus(ctx, bx, by, seed, flip=1):
    rng = random.Random(seed)
    f = flip
    shadow(ctx, bx + 0.25, by + 0.02, 2.3, 0.62, 0.2)
    trunk = [(bx, by), (bx - 0.14 * f, by - 1.4), (bx + 0.12 * f, by - 2.8), (bx - 0.05 * f, by - 3.9)]
    L1 = [(bx - 0.02 * f, by - 3.5), (bx - 0.75 * f, by - 4.5), (bx - 1.6 * f, by - 5.3)]
    L2 = [(bx, by - 3.7), (bx + 0.55 * f, by - 4.8), (bx + 1.3 * f, by - 5.8)]
    L3 = [(bx - 0.05 * f, by - 3.8), (bx - 0.12 * f, by - 5.0), (bx + 0.1 * f, by - 6.2)]
    back = [(bx - 1.75 * f, by - 5.7, 1.2, 0.8), (bx + 1.45 * f, by - 6.1, 1.25, 0.85), (bx + 0.05 * f, by - 6.75, 1.3, 0.8)]
    front = [(bx - 0.7 * f, by - 5.05, 0.95, 0.6), (bx + 0.95 * f, by - 5.0, 0.85, 0.55), (bx - 1.9 * f, by - 5.0, 0.6, 0.45),
             (bx + 0.2 * f, by - 5.9, 0.8, 0.5)]
    for cx, cy, rx, ry in back:
        foliage(ctx, rng, cluster(rng, cx, cy, rx, ry, 13, 0.3, 0.52), EUC_BACK, lw=0.04)
    limbs = [limb(L1, 0.3, 0.1), limb(L2, 0.32, 0.1), limb(L3, 0.26, 0.09), limb(trunk, 0.56, 0.36)]
    bark, bark_line = C('#ebe1cd'), C('#6b5a48')
    # root flare
    ctx.poly([(bx - 0.5, by + 0.04), (bx - 0.24, by - 0.35), (bx + 0.24, by - 0.35), (bx + 0.5, by + 0.04),
              (bx + 0.2, by + 0.09), (bx - 0.2, by + 0.09)]).fs(bark, bark_line, 0.035)
    woody(ctx, limbs, bark, bark_line)
    ctx.poly(limb([(p[0] + 0.12, p[1]) for p in trunk], 0.2, 0.12)).fill(C('#d3c5ab'))
    for _ in range(9):                                            # peeling bark patches
        t = rng.uniform(0.05, 0.95)
        y = by - t * 3.8
        x = bx + rng.uniform(-0.14, 0.12) + (-0.14 * f if 0.2 < t < 0.5 else 0.05 * f)
        ctx.smooth(blob(rng, x, y, 0.07, 0.17, n=6, jit=0.3)).fs(rng.choice([C('#c2ae90'), C('#b79f80'), C('#d8cdb6')]), al(bark_line, 0.5), 0.012)
    for _ in range(5):
        y = by - rng.uniform(0.3, 3.4)
        ctx.move_to(bx - 0.2, y).line_to(bx - 0.08, y + 0.03)
    ctx.stroke(al(bark_line, 0.6), 0.014)
    for cx, cy, rx, ry in front:
        circ = cluster(rng, cx, cy, rx, ry, 10, 0.26, 0.46)
        for _ in range(7):                                        # drooping leaves under the clump
            lx = cx + rng.uniform(-rx, rx) * 0.9
            leaf(ctx, lx, cy + ry * 0.5, rng.uniform(0.45, 0.85), 0.07, math.pi / 2 + rng.uniform(-0.25, 0.25))
        ctx.fs(EUC.lo, EUC.line, 0.016)
        foliage(ctx, rng, circ, EUC, lw=0.04)


def tree_palm(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.2, by + 0.02, 1.9, 0.5, 0.2)
    trunk = [(bx, by), (bx + 0.28, by - 1.6), (bx + 0.12, by - 3.4), (bx - 0.25, by - 5.0)]
    cx, cy = bx - 0.25, by - 5.0
    greens = [C('#4f9a4a'), C('#5fae52'), C('#73bd5a')]

    def frond(a, ln, droop, col, line=C('#1f4a26')):
        n = 26
        up, lo, mid = [], [], []
        for i in range(n + 1):
            t = i / n
            x = cx + math.cos(a) * ln * t
            y = cy + math.sin(a) * ln * t + droop * ln * t * t
            dx = math.cos(a) * ln
            dy = math.sin(a) * ln + 2 * droop * ln * t
            d = math.hypot(dx, dy)
            nx, ny = -dy / d, dx / d
            w = 0.27 * math.sin(math.pi * min(1.0, t * 0.97 + 0.03)) ** 0.55
            wt = w * (1.0 if i % 2 == 0 else 0.5)
            up.append((x + nx * wt, y + ny * wt))
            lo.append((x - nx * wt, y - ny * wt))
            mid.append((x, y))
        ctx.poly(up + lo[::-1]).fs(col, line, 0.028)
        ctx.poly(mid, closed=False).stroke(lt(col, 0.35), 0.03)

    back = [(-2.75, 3.0, 0.5), (-0.4, 3.0, 0.5), (-2.2, 3.1, 0.3), (-0.95, 3.1, 0.3), (-1.57, 2.9, 0.08)]
    for a, ln, dr in back:
        frond(a + rng.uniform(-0.06, 0.06), ln, dr, greens[0])
    poly = limb(trunk, 0.46, 0.27, sub=10)
    ctx.poly(poly).fs(C('#b48d60'), C('#5a3f28'), 0.035)
    ctx.poly(limb([(p[0] + 0.1, p[1]) for p in trunk], 0.16, 0.09, sub=10)).fill(C('#9a744c'))
    cl = spline_pts(trunk, closed=False, sub=10)
    for i in range(2, len(cl) - 1, 1):                           # trunk rings
        x, y = cl[i]
        w = 0.46 + (0.27 - 0.46) * i / (len(cl) - 1)
        ctx.arc(x, y, w / 2, 0.06, 0.1, math.pi - 0.1, n=6)
    ctx.stroke(al(C('#5a3f28'), 0.75), 0.018)
    for dx, dy in ((-0.16, 0.12), (0.14, 0.14), (0.0, 0.26)):   # coconuts
        ctx.ellipse(cx + dx, cy + dy, 0.15, 0.16).fs(C('#7a5232'), INK, 0.022)
        ctx.ellipse(cx + dx - 0.04, cy + dy - 0.05, 0.05, 0.04).fill(al(C('#ffffff'), 0.3))
    front = [(-3.05, 2.9, 0.75), (-0.1, 2.9, 0.75), (-2.5, 3.0, 0.5), (-0.65, 3.0, 0.5), (-1.9, 2.7, 0.25),
             (-1.25, 2.7, 0.25), (2.75, 2.0, 0.85), (0.4, 2.0, 0.85)]
    for i, (a, ln, dr) in enumerate(front):
        frond(a + rng.uniform(-0.06, 0.06), ln * rng.uniform(0.93, 1.05), dr, greens[1 + i % 2])
    ctx.ellipse(cx, cy, 0.2, 0.17).fs(C('#8a6a3e'), INK, 0.022)


def tree_olive(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.2, by + 0.02, 1.9, 0.52, 0.2)
    trunk = [(bx, by), (bx - 0.22, by - 0.8), (bx + 0.15, by - 1.55)]
    L1 = [(bx + 0.05, by - 1.3), (bx - 0.6, by - 2.1), (bx - 1.15, by - 2.7)]
    L2 = [(bx + 0.15, by - 1.4), (bx + 0.7, by - 2.2), (bx + 1.05, by - 2.9)]
    L3 = [(bx + 0.1, by - 1.5), (bx, by - 2.4), (bx - 0.1, by - 3.2)]
    for cx, cy, rx, ry in ((bx - 1.15, by - 3.05, 1.0, 0.7), (bx + 1.05, by - 3.25, 1.0, 0.7), (bx - 0.1, by - 3.85, 1.1, 0.7)):
        foliage(ctx, rng, cluster(rng, cx, cy, rx, ry, 13, 0.26, 0.46), OLIVE_BACK, lw=0.04)
    bark, line = C('#8f7a64'), C('#3d3028')
    ctx.poly([(bx - 0.62, by + 0.05), (bx - 0.3, by - 0.4), (bx + 0.3, by - 0.4), (bx + 0.6, by + 0.05),
              (bx + 0.2, by + 0.1), (bx - 0.25, by + 0.1)]).fs(bark, line, 0.035)
    woody(ctx, [limb(L1, 0.4, 0.13), limb(L2, 0.38, 0.13), limb(L3, 0.3, 0.11), limb(trunk, 0.78, 0.5)], bark, line)
    ctx.poly(limb([(p[0] + 0.17, p[1]) for p in trunk], 0.26, 0.16)).fill(C('#756250'))
    for _ in range(8):                                            # twisted bark lines
        y0 = by - rng.uniform(0.05, 1.3)
        x0 = bx + rng.uniform(-0.25, 0.2)
        ctx.move_to(x0, y0)
        ctx.curve_to(x0 + 0.08, y0 - 0.1, x0 - 0.08, y0 - 0.2, x0 + 0.04, y0 - 0.32)
    ctx.stroke(al(line, 0.65), 0.018)
    ctx.ellipse(bx - 0.08, by - 0.75, 0.09, 0.13).fs(C('#5f4f40'), line, 0.016)
    for cx, cy, rx, ry in ((bx - 0.2, by - 2.85, 0.85, 0.5), (bx + 0.75, by - 2.7, 0.55, 0.4), (bx - 1.25, by - 2.5, 0.5, 0.38)):
        circ = cluster(rng, cx, cy, rx, ry, 9, 0.24, 0.42)
        foliage(ctx, rng, circ, OLIVE, lw=0.04)
        for x, y, r in circ:
            if rng.random() < 0.7:
                ctx.ellipse(x + rng.uniform(-r, r) * 0.6, y + rng.uniform(0, r) * 0.7, 0.04, 0.05)
        ctx.fs(C('#3a3550'), al(INK, 0.6), 0.01)


def tree_citrus(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.15, by + 0.02, 1.35, 0.4, 0.2)
    ctx.poly(limb([(bx, by), (bx + 0.06, by - 0.7), (bx, by - 1.4)], 0.32, 0.22)).fs(C('#8a6a4a'), C('#3d2c20'), 0.035)
    ctx.poly(limb([(bx + 0.07, by), (bx + 0.12, by - 0.7), (bx + 0.06, by - 1.4)], 0.1, 0.07)).fill(C('#735538'))
    circ = cluster(rng, bx, by - 2.35, 1.2, 0.95, 24, 0.3, 0.5)
    foliage(ctx, rng, circ, CITRUS, lw=0.04)
    col = C('#f7a531') if seed % 2 else C('#f7d542')
    for _ in range(13):
        a, d = rng.random() * math.tau, math.sqrt(rng.random())
        x, y = bx + math.cos(a) * 1.25 * d, by - 2.3 + math.sin(a) * 1.0 * d
        ctx.ellipse(x, y, 0.11, 0.11).fs(col, dk(col, 0.55), 0.018)
        ctx.ellipse(x - 0.035, y - 0.04, 0.035, 0.03).fill(al(C('#ffffff'), 0.7))


def tree_cypress(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.1, by + 0.02, 0.75, 0.24, 0.2)
    ctx.rect(bx - 0.09, by - 0.5, 0.18, 0.52).fs(C('#7a5a40'), C('#3d2c20'), 0.03)
    circ = []
    n = 26
    for i in range(n):
        t = i / (n - 1)
        y = by - 0.55 - t * 4.3
        w = 0.56 * math.sin(math.pi * (0.16 + 0.84 * (1 - t) ** 0.8) * 0.62) ** 1.0 * (1.0 if t < 0.9 else 0.7)
        circ.append((bx + rng.uniform(-0.12, 0.12) * (1 - t), y, max(0.1, w * rng.uniform(0.85, 1.0))))
        if w > 0.3:
            circ.append((bx + rng.choice([-1, 1]) * w * 0.4, y + 0.05, w * 0.7))
    foliage(ctx, rng, circ, CYPRESS, lw=0.04, sort=False)


# ------------------------------------------------------------------- bushes
def bush_round(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.08, by, 0.95, 0.26, 0.2)
    foliage(ctx, rng, cluster(rng, bx, by - 0.62, 0.72, 0.42, 16, 0.24, 0.4), BUSH, lw=0.04)


def bush_flower(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.08, by, 1.0, 0.27, 0.2)
    circ = cluster(rng, bx, by - 0.68, 0.76, 0.46, 16, 0.24, 0.4)
    foliage(ctx, rng, circ, LEAF_DARK, lw=0.04)
    col = C('#f0679a')
    for _ in range(11):
        a, d = rng.random() * math.tau, math.sqrt(rng.random())
        flower(ctx, bx + math.cos(a) * 0.85 * d, by - 0.72 + math.sin(a) * 0.55 * d, rng.uniform(0.1, 0.14), col,
               rot=rng.random(), line=dk(col, 0.55))


def bush_lavender(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.05, by, 0.75, 0.2, 0.2)
    foliage(ctx, rng, cluster(rng, bx, by - 0.22, 0.5, 0.14, 8, 0.14, 0.2), Pal('#7fa878', '#a3c597', '#5f8a60', '#2f4a36'), lw=0.03, leaves=False)
    n = 17
    stems = []
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * 0.115 + rng.uniform(-0.05, 0.05)
        ln = rng.uniform(0.7, 1.05)
        x0 = bx + (i - (n - 1) / 2) * 0.05
        stems.append((x0, a, ln))
        ctx.move_to(x0, by - 0.2).line_to(x0 + math.cos(a) * ln, by - 0.2 + math.sin(a) * ln)
    ctx.stroke(C('#5f8f55'), 0.022)
    for x0, a, ln in stems:
        col = rng.choice([C('#9d72d8'), C('#b48be6'), C('#8463c9')])
        for t in (0.62, 0.72, 0.82, 0.92, 1.0):
            ctx.ellipse(x0 + math.cos(a) * ln * t, by - 0.2 + math.sin(a) * ln * t, 0.05 * (1.2 - t * 0.4), 0.06)
        ctx.fs(col, dk(col, 0.5), 0.012)


def grass_pampas(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.05, by, 0.85, 0.22, 0.2)
    n = 22
    for layer, col in ((0, C('#5f9a4c')), (1, C('#7db85a')), (2, C('#9acb6a'))):
        for i in range(n):
            if i % 3 != layer:
                continue
            a = -math.pi / 2 + (i - (n - 1) / 2) * 0.13 + rng.uniform(-0.05, 0.05)
            ln = rng.uniform(0.9, 1.4)
            x1, y1 = bx + math.cos(a) * ln, by + math.sin(a) * ln
            x2, y2 = x1 + math.cos(a) * 0.35 + (0.3 if a > -math.pi / 2 else -0.3), y1 + 0.25
            ctx.move_to(bx - 0.05, by)
            ctx.curve_to(bx - 0.03, by - ln * 0.5, x1 - 0.02, y1, x2, y2)
            ctx.curve_to(x1 + 0.05, y1 + 0.02, bx + 0.07, by - ln * 0.5, bx + 0.05, by)
            ctx.close()
        ctx.fs(col, C('#2a5a2a'), 0.016)
    for i in range(5):                                             # plumes
        a = -math.pi / 2 + (i - 2) * 0.2 + rng.uniform(-0.05, 0.05)
        ln = rng.uniform(1.5, 1.95)
        x1, y1 = bx + math.cos(a) * ln, by + math.sin(a) * ln
        ctx.move_to(bx, by - 0.2).line_to(x1, y1 + 0.3)
        ctx.stroke(C('#b9a36a'), 0.022)
        leaf(ctx, x1 - math.cos(a) * 0.1, y1 + 0.45, 0.75, 0.12, a).fs(C('#f3e7c8'), C('#9a875a'), 0.016)
        leaf(ctx, x1 - math.cos(a) * 0.1, y1 + 0.4, 0.5, 0.05, a).fill(C('#fff8e6'))


# --------------------------------------------------------------------- pots
def pot_fiddle(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.05, by, 0.55, 0.16, 0.22)
    ctx.move_to(bx, by - 0.5).line_to(bx + 0.03, by - 2.1)
    ctx.stroke(C('#6a4a30'), 0.06)
    leaves = [(-0.02, 2.15, -1.57), (0.0, 1.95, -2.5), (0.02, 1.85, -0.6), (0.0, 1.6, -2.9), (0.02, 1.5, -0.25),
              (0.0, 1.25, -2.6), (0.02, 1.15, -0.5), (0.0, 0.95, -3.05), (0.02, 0.9, -0.1)]
    for i, (dx, h, a) in enumerate(reversed(leaves)):
        col = [C('#3f8a4a'), C('#4f9d52'), C('#5aa95a')][i % 3]
        x, y = bx + dx, by - h
        ln = 0.62 + 0.05 * (i % 2)
        leaf(ctx, x, y, ln, 0.34, a).fs(col, C('#1d4a2a'), 0.022)
        ctx.move_to(x, y).line_to(x + math.cos(a) * ln * 0.85, y + math.sin(a) * ln * 0.85)
        ctx.stroke(lt(col, 0.4), 0.02)
    pot, line = C('#efe7da'), INK
    ctx.poly([(bx - 0.36, by - 0.62), (bx + 0.36, by - 0.62), (bx + 0.27, by), (bx - 0.27, by)]).fs(pot, line, 0.028)
    ctx.poly([(bx + 0.1, by - 0.62), (bx + 0.36, by - 0.62), (bx + 0.27, by), (bx + 0.06, by)]).fill(dk(pot, 0.12))
    ctx.rrect(bx - 0.4, by - 0.7, 0.8, 0.13, 0.04).fs(lt(pot, 0.3), line, 0.025)
    ctx.rect(bx - 0.3, by - 0.42, 0.6, 0.06).fill(GOLDISH)


GOLDISH = C('#d9a94a')


def pot_urn(ctx, bx, by, seed):
    rng = random.Random(seed)
    shadow(ctx, bx + 0.05, by, 0.6, 0.17, 0.22)
    st, line = STONE[2], C('#5f5a55')
    circ = cluster(rng, bx, by - 1.12, 0.5, 0.26, 10, 0.18, 0.28)
    foliage(ctx, rng, circ, LEAF, lw=0.032, leaves=False)
    for _ in range(4):                                            # trailing ivy
        x = bx + rng.uniform(-0.45, 0.45)
        for k in range(4):
            ctx.ellipse(x + rng.uniform(-0.05, 0.05), by - 0.95 + k * 0.11, 0.07, 0.06)
        ctx.fs(LEAF2.base, LEAF2.line, 0.014)
    col = rng.choice([C('#f0679a'), C('#fff5e6'), C('#f58a3c')])
    for _ in range(9):
        a, d = rng.random() * math.tau, math.sqrt(rng.random())
        flower(ctx, bx + math.cos(a) * 0.5 * d, by - 1.2 + math.sin(a) * 0.3 * d, 0.1, col, rot=rng.random(), line=dk(col, 0.55))
    ctx.rrect(bx - 0.26, by - 0.14, 0.52, 0.14, 0.03).fs(st, line, 0.026)
    ctx.poly([(bx - 0.1, by - 0.14), (bx + 0.1, by - 0.14), (bx + 0.14, by - 0.36), (bx - 0.14, by - 0.36)]).fs(dk(st, 0.1), line, 0.026)
    ctx.move_to(bx - 0.46, by - 0.92)
    ctx.curve_to(bx - 0.46, by - 0.5, bx - 0.2, by - 0.36, bx, by - 0.36)
    ctx.curve_to(bx + 0.2, by - 0.36, bx + 0.46, by - 0.5, bx + 0.46, by - 0.92)
    ctx.close().fs(st, line, 0.028)
    ctx.move_to(bx + 0.15, by - 0.92)
    ctx.curve_to(bx + 0.15, by - 0.6, bx + 0.1, by - 0.4, bx + 0.05, by - 0.37)
    ctx.curve_to(bx + 0.3, by - 0.4, bx + 0.46, by - 0.55, bx + 0.46, by - 0.92)
    ctx.close().fill(dk(st, 0.14))
    ctx.rrect(bx - 0.52, by - 1.0, 1.04, 0.12, 0.05).fs(lt(st, 0.3), line, 0.026)


def planter(ctx, bx, by, seed, w):
    rng = random.Random(seed)
    h = 0.62
    shadow(ctx, bx + 0.06, by + 0.02, w / 2 + 0.15, 0.16, 0.22)
    circ = []
    x = bx - w / 2 + 0.25
    while x < bx + w / 2 - 0.2:
        circ.append((x, by - h - 0.22 + rng.uniform(-0.06, 0.08), rng.uniform(0.24, 0.36)))
        x += rng.uniform(0.2, 0.32)
    for x in [bx - w / 2 + 0.5 + i * (w - 1.0) / max(1, int(w / 1.1)) for i in range(int(w / 1.1) + 1)]:
        n = 7
        for i in range(n):                                        # tall blades behind
            a = -math.pi / 2 + (i - (n - 1) / 2) * 0.2 + rng.uniform(-0.05, 0.05)
            leaf(ctx, x, by - h, rng.uniform(0.7, 1.0), 0.06, a)
        ctx.fs(C('#6fae4d'), C('#2a5a2a'), 0.016)
    foliage(ctx, rng, circ, LEAF, lw=0.034, leaves=False, sort=False)
    cols = [C('#f0679a'), C('#fff5e6'), C('#f7c948'), C('#9d72d8')]
    for cx, cy, r in circ:
        if rng.random() < 0.75:
            col = rng.choice(cols)
            flower(ctx, cx + rng.uniform(-0.1, 0.1), cy - rng.uniform(0, 0.15), 0.1, col, rot=rng.random(), line=dk(col, 0.55))
    ctx.rect(bx - w / 2, by - h, w, h).fs(WOOD[1], INK, 0.028)
    x = bx - w / 2 + 0.28
    while x < bx + w / 2 - 0.05:
        ctx.move_to(x, by - h + 0.1).line_to(x, by)
        x += 0.28
    ctx.stroke(al(WOOD_LINE, 0.7), 0.016)
    ctx.rect(bx - w / 2, by - 0.14, w, 0.14).fill(al(INK, 0.18))
    ctx.rrect(bx - w / 2 - 0.06, by - h - 0.06, w + 0.12, 0.17, 0.04).fs(WOOD[2], INK, 0.026)
    ctx.rect(bx - w / 2, by - h - 0.04, w, 0.04).fill(al(C('#ffffff'), 0.3))


# -------------------------------------------------------------- structures
def lamp_post(ctx, bx, by, seed):
    shadow(ctx, bx + 0.05, by, 0.4, 0.12, 0.25)
    top = by - 3.1
    glow(ctx, bx, top - 0.22, 1.15, 1.15, WARM, 0.6, steps=16)
    ctx.poly([(bx - 0.2, by), (bx - 0.09, by - 0.3), (bx + 0.09, by - 0.3), (bx + 0.2, by)]).fs(METAL, INK, 0.026)
    ctx.rect(bx - 0.055, top, 0.11, 3.1 - 0.3).fs(METAL, INK, 0.024)
    ctx.rect(bx - 0.03, top, 0.03, 2.8).fill(METAL_L)
    for yy in (by - 0.45, by - 1.6, top + 0.12):
        ctx.rrect(bx - 0.09, yy, 0.18, 0.08, 0.03).fs(METAL, INK, 0.018)
    # lantern head
    ctx.poly([(bx - 0.15, top), (bx + 0.15, top), (bx + 0.23, top - 0.5), (bx - 0.23, top - 0.5)]).fs(C('#ffe9a8'), INK, 0.026)
    ctx.ellipse(bx, top - 0.24, 0.07, 0.15).fill(C('#fffbe6'))
    ctx.move_to(bx, top).line_to(bx, top - 0.5)
    ctx.stroke(al(INK, 0.6), 0.016)
    ctx.poly([(bx - 0.3, top - 0.5), (bx + 0.3, top - 0.5), (bx + 0.1, top - 0.72), (bx - 0.1, top - 0.72)]).fs(METAL, INK, 0.026)
    ctx.ellipse(bx, top - 0.78, 0.06, 0.06).fs(METAL, INK, 0.02)


def bollard_light(ctx, bx, by, seed):
    shadow(ctx, bx + 0.03, by, 0.26, 0.08, 0.25)
    glow(ctx, bx, by - 0.68, 0.5, 0.42, WARM, 0.55, steps=10)
    ctx.rrect(bx - 0.12, by - 0.92, 0.24, 0.92, 0.03).fs(WOOD[3], INK, 0.026)
    ctx.rect(bx - 0.08, by - 0.88, 0.05, 0.84).fill(al(C('#ffffff'), 0.2))
    ctx.rrect(bx - 0.075, by - 0.8, 0.15, 0.24, 0.02).fs(C('#fff0b8'), INK, 0.018)
    ctx.rrect(bx - 0.15, by - 0.97, 0.3, 0.08, 0.02).fs(WOOD_LINE, INK, 0.02)


def arch_metal(ctx, bx, by, seed):
    rng = random.Random(seed)
    cy, R = by - 1.289, 3.311
    a0, a1 = math.radians(157.1), math.radians(382.9)
    for dx in (-3.05, 3.05):
        shadow(ctx, bx + dx, by, 0.35, 0.1, 0.25)
    for r, lw in ((R, 0.13), (R - 0.3, 0.08)):
        ctx.arc(bx, cy, r, r, a0 if r == R else a0 - 0.02, a1 if r == R else a1 + 0.02, n=70).stroke(INK, lw + 0.06)
    for i in range(15):                                           # struts between the two rings
        a = a0 + (i + 0.5) * (a1 - a0) / 15
        ctx.move_to(bx + math.cos(a) * R, cy + math.sin(a) * R).line_to(bx + math.cos(a + 0.05) * (R - 0.3), cy + math.sin(a + 0.05) * (R - 0.3))
    ctx.stroke(INK, 0.06)
    for r, lw in ((R, 0.13), (R - 0.3, 0.08)):
        ctx.arc(bx, cy, r, r, a0, a1, n=70).stroke(METAL, lw)
    ctx.arc(bx, cy, R + 0.02, R + 0.02, math.radians(200), math.radians(300), n=30).stroke(METAL_L, 0.03)
    # hanging wicker lanterns
    for dx, ln in ((-1.35, 0.9), (0.0, 1.35), (1.35, 0.9)):
        ty = cy - math.sqrt((R - 0.3) ** 2 - dx * dx)
        ly = ty + ln
        ctx.move_to(bx + dx, ty).line_to(bx + dx, ly - 0.3)
        ctx.stroke(INK, 0.018)
        glow(ctx, bx + dx, ly, 0.75, 0.75, WARM, 0.5, steps=12)
        ctx.ellipse(bx + dx, ly, 0.3, 0.3).fs(C('#ffe6a0'), INK, 0.026)
        for k in (-0.6, 0.0, 0.6):
            ctx.arc(bx + dx, ly, 0.3 * abs(math.cos(k * 1.2)) + 0.02, 0.3, -math.pi / 2, math.pi / 2, n=8) if k >= 0 else \
                ctx.arc(bx + dx, ly, 0.3 * abs(math.cos(k * 1.2)), 0.3, math.pi / 2, math.pi * 1.5, n=8)
        ctx.arc(bx + dx, ly - 0.1, 0.28, 0.06, 0, math.pi, n=8)
        ctx.arc(bx + dx, ly + 0.1, 0.28, 0.06, 0, math.pi, n=8)
        ctx.stroke(al(C('#8a5a20'), 0.85), 0.018)
        ctx.ellipse(bx + dx, ly, 0.1, 0.12).fill(C('#fffbe6'))
    # climbing jasmine on the left leg, a little on the right
    for (s0, s1, dens) in ((a0, math.radians(262), 1.0), (math.radians(325), a1, 0.8)):
        circ = []
        a = s0
        while a < s1:
            circ.append((bx + math.cos(a) * (R - 0.15) + rng.uniform(-0.12, 0.12), cy + math.sin(a) * (R - 0.15) + rng.uniform(-0.1, 0.1),
                         rng.uniform(0.15, 0.27)))
            a += 0.05 / dens
        foliage(ctx, rng, circ, LEAF, lw=0.03, leaves=False, sort=False)
        for x, y, r in circ:
            if rng.random() < 0.5:
                flower(ctx, x + rng.uniform(-0.1, 0.1), y + rng.uniform(-0.1, 0.1), 0.07, C('#fff8ee'), line=C('#9a8a7a'))


def pillar_wood(ctx, bx, by, seed):
    top = by - 4.0
    col, line = C('#8f6846'), INK
    glow(ctx, bx, by - 2.35, 0.9, 1.1, WARM, 0.5, steps=12)
    ctx.rect(bx - 0.7, top, 1.4, 0.3).fs(C('#7a573a'), line, 0.028)             # beam stub
    ctx.rect(bx - 0.7, top, 1.4, 0.07).fill(al(C('#ffffff'), 0.22))
    for d in (-1, 1):                                                           # braces
        ctx.poly([(bx + d * 0.2, top + 1.0), (bx + d * 0.2, top + 0.78), (bx + d * 0.66, top + 0.3),
                  (bx + d * 0.7, top + 0.3), (bx + d * 0.7, top + 0.5)]).fs(C('#7a573a'), line, 0.026)
    ctx.rect(bx - 0.23, top + 0.3, 0.46, 3.7).fs(col, line, 0.03)
    ctx.rect(bx - 0.18, top + 0.3, 0.09, 3.7).fill(lt(col, 0.2))
    ctx.rect(bx + 0.1, top + 0.3, 0.13, 3.7).fill(dk(col, 0.18))
    for yy in (top + 0.9, top + 2.3, top + 3.2):
        ctx.move_to(bx - 0.02, yy).line_to(bx + 0.01, yy + 0.5)
    ctx.stroke(al(line, 0.35), 0.016)
    ctx.rect(bx - 0.29, by - 0.3, 0.58, 0.3).fs(C('#6f4f35'), line, 0.028)
    ctx.rect(bx - 0.29, top + 0.3, 0.58, 0.16).fs(C('#6f4f35'), line, 0.026)
    # lantern on the post
    ly = by - 2.35
    ctx.rect(bx - 0.03, ly - 0.42, 0.06, 0.2).fill(INK)
    ctx.poly([(bx - 0.13, ly + 0.18), (bx + 0.13, ly + 0.18), (bx + 0.17, ly - 0.2), (bx - 0.17, ly - 0.2)]).fs(C('#ffe9a8'), line, 0.022)
    ctx.ellipse(bx, ly, 0.05, 0.11).fill(C('#fffbe6'))
    ctx.poly([(bx - 0.21, ly - 0.2), (bx + 0.21, ly - 0.2), (bx + 0.08, ly - 0.34), (bx - 0.08, ly - 0.34)]).fs(METAL, line, 0.022)
    ctx.rect(bx - 0.14, ly + 0.18, 0.28, 0.05).fs(METAL, line, 0.018)


def string_lights(ctx, bx, by, seed):
    rng = random.Random(seed)
    xs = (bx - 4.0, bx + 4.0)
    top = by - 3.5
    for x in xs:
        shadow(ctx, x + 0.04, by, 0.3, 0.09, 0.25)
    sag = lambda x, s, y0: y0 + s * (1 - ((x - bx) / 4.0) ** 2)
    for s, y0, ph in ((0.95, top + 0.12, 0.0), (0.5, top + 0.02, 0.25)):
        pts = [(bx - 4 + i * 8 / 40, sag(bx - 4 + i * 8 / 40, s, y0)) for i in range(41)]
        ctx.poly(pts, closed=False).stroke(INK, 0.022)
        x = bx - 4 + 0.3 + ph
        while x < bx + 3.8:
            y = sag(x, s, y0)
            ctx.rect(x - 0.025, y, 0.05, 0.07).fill(INK)
            bulb(ctx, x, y + 0.14, 0.065, 0.3, 0.5)
            x += 0.5
    for x in xs:
        ctx.poly([(x - 0.14, by), (x - 0.06, by - 0.22), (x + 0.06, by - 0.22), (x + 0.14, by)]).fs(METAL, INK, 0.024)
        ctx.rect(x - 0.05, top - 0.1, 0.1, 3.4).fs(METAL, INK, 0.022)
        ctx.rect(x - 0.025, top - 0.1, 0.025, 3.4).fill(METAL_L)
        ctx.ellipse(x, top - 0.12, 0.085, 0.085).fs(METAL, INK, 0.02)


def chandelier_green(ctx, bx, by, seed):
    rng = random.Random(seed)
    cy = by - 4.4
    rx, ry = 2.1, 0.6
    for a in (math.pi * 1.15, math.pi * 1.5, math.pi * 1.85, math.pi * 0.25, math.pi * 0.75):   # cables
        ctx.move_to(bx + math.cos(a) * rx, cy + math.sin(a) * ry).line_to(bx, cy - 1.75)
    ctx.stroke(al(INK, 0.85), 0.022)
    ring = lambda a0, a1, n: [(bx + math.cos(a) * rx + rng.uniform(-0.1, 0.1), cy + math.sin(a) * ry + rng.uniform(-0.08, 0.08),
                               rng.uniform(0.26, 0.4)) for a in [a0 + (a1 - a0) * i / n for i in range(n + 1)]]
    foliage(ctx, rng, ring(math.pi * 1.02, math.pi * 1.98, 20), LEAF_DARK, lw=0.036, sort=False)
    glow(ctx, bx, cy + 0.5, 2.3, 1.2, WARM, 0.3, steps=14)
    for i in range(13):                                             # hanging bulbs
        a = rng.random() * math.tau
        d = math.sqrt(rng.random()) * 0.92
        x, y = bx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        ln = rng.uniform(0.5, 1.4)
        ctx.move_to(x, y).line_to(x, y + ln)
        ctx.stroke(al(INK, 0.8), 0.014)
        bulb(ctx, x, y + ln + 0.06, 0.075, 0.34, 0.5)
    front = ring(math.pi * 0.0, math.pi * 1.0, 20)
    for x, y, r in front[::2]:                                      # trailing strands
        n = rng.randint(2, 5)
        for k in range(n):
            ctx.ellipse(x + rng.uniform(-0.04, 0.04), y + 0.25 + k * 0.13, 0.08, 0.07)
        ctx.fs(LEAF2.base, LEAF2.line, 0.014)
    foliage(ctx, rng, front, LEAF, lw=0.036, sort=False)
    for x, y, r in front:
        if rng.random() < 0.55:
            flower(ctx, x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.12, 0.1), 0.085, C('#fff8ee'), line=C('#9a8a7a'))


# ----------------------------------------------------------------- registry
# name: (canvas w, canvas h, base x, base y, painter)
SPECS = {
    'tree_eucalyptus_a': (6.6, 8.7, 3.3, 8.15, lambda c, x, y: tree_eucalyptus(c, x, y, 1, 1)),
    'tree_eucalyptus_b': (6.6, 8.7, 3.3, 8.15, lambda c, x, y: tree_eucalyptus(c, x, y, 2, -1)),
    'tree_palm': (7.6, 9.0, 3.8, 8.5, lambda c, x, y: tree_palm(c, x, y, 3)),
    'tree_olive': (5.2, 5.6, 2.6, 5.1, lambda c, x, y: tree_olive(c, x, y, 4)),
    'tree_citrus': (3.8, 4.5, 1.9, 4.05, lambda c, x, y: tree_citrus(c, x, y, 5)),
    'tree_cypress': (2.4, 5.9, 1.2, 5.55, lambda c, x, y: tree_cypress(c, x, y, 6)),
    'bush_round': (2.4, 1.8, 1.2, 1.5, lambda c, x, y: bush_round(c, x, y, 7)),
    'bush_flower': (2.5, 1.9, 1.25, 1.6, lambda c, x, y: bush_flower(c, x, y, 8)),
    'bush_lavender': (2.2, 1.7, 1.1, 1.45, lambda c, x, y: bush_lavender(c, x, y, 9)),
    'grass_pampas': (3.2, 2.5, 1.6, 2.25, lambda c, x, y: grass_pampas(c, x, y, 10)),
    'pot_fiddle': (2.0, 3.2, 1.0, 2.95, lambda c, x, y: pot_fiddle(c, x, y, 11)),
    'pot_urn': (1.8, 2.0, 0.9, 1.75, lambda c, x, y: pot_urn(c, x, y, 12)),
    'planter_long': (5.2, 2.2, 2.6, 1.95, lambda c, x, y: planter(c, x, y, 13, 4.5)),
    'planter_small': (2.6, 2.2, 1.3, 1.95, lambda c, x, y: planter(c, x, y, 14, 1.9)),
    'lamp_post': (2.6, 5.4, 1.3, 5.15, lambda c, x, y: lamp_post(c, x, y, 15)),
    'bollard_light': (1.2, 1.5, 0.6, 1.35, lambda c, x, y: bollard_light(c, x, y, 16)),
    'arch_metal': (7.6, 5.4, 3.8, 5.15, lambda c, x, y: arch_metal(c, x, y, 17)),
    'pillar_wood': (2.0, 4.5, 1.0, 4.3, lambda c, x, y: pillar_wood(c, x, y, 18)),
    'string_lights': (9.0, 4.2, 4.5, 3.95, lambda c, x, y: string_lights(c, x, y, 19)),
    'chandelier_green': (5.4, 6.6, 2.7, 6.4, lambda c, x, y: chandelier_green(c, x, y, 20)),
}
NAMES = list(SPECS)


def render(name, ppu):
    """-> (trimmed RGBA PIL image, (pivot_x_px, pivot_y_px) measured from the image's top-left)."""
    w, h, bx, by, fn = SPECS[name]
    ctx = Ctx(w, h, ppu)
    fn(ctx, bx, by)
    arr = ctx.rgba().copy()
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 0)
    px, py = int(round(bx * ppu)), int(round(by * ppu))
    pad = 2
    x0, x1 = max(0, min(xs.min(), px) - pad), min(arr.shape[1], max(xs.max(), px) + 1 + pad)
    y0, y1 = max(0, min(ys.min(), py) - pad), min(arr.shape[0], max(ys.max(), py) + 1 + pad)
    img = Image.fromarray(arr[y0:y1, x0:x1], 'RGBA')
    return img, (px - x0, py - y0)
