"""Outdoor ground painter for the venue map."""
import math
import random

from lib import *
import layout as L

W, H = L.W, L.H

# ------------------------------------------------------------------ palette
GRASS, GRASS_L, GRASS_D, GRASS_LINE = C('#86ba5c'), C('#97c96a'), C('#6da54d'), C('#3f7038')
MEADOW, MEADOW_L, MEADOW_D = C('#93bf62'), C('#a9d077'), C('#74a651')
GRAVEL, GRAVEL_L, GRAVEL_D, GRAVEL_LINE = C('#dfd0b0'), C('#efe4cb'), C('#c2b08d'), C('#9c8a6a')
SAND, SAND_D = C('#e8d3a0'), C('#cdb37c')
SOIL, SOIL_D, SOIL_L = C('#6e4c36'), C('#523828'), C('#866046')
WOOD = [C('#c69259'), C('#bb8650'), C('#cf9f68'), C('#b27c48')]
WOOD_LINE = C('#6b4526')
BOARD = [C('#b99b79'), C('#ad8e6c'), C('#c4a886'), C('#a38462')]
BOARD_LINE = C('#6a5038')
STONE = [C('#d3ccbf'), C('#c8c0b2'), C('#ddd7cb'), C('#cdc4b3')]
STONE_LINE = C('#8f877a')
COBBLE = [C('#bcb5a8'), C('#aaa295'), C('#cbc5ba'), C('#b3a999')]
COBBLE_LINE = C('#7b7468')
BRICK = [C('#c9775a'), C('#bd694c'), C('#d28767'), C('#b86448')]
BRICK_LINE = C('#8a4a36')
CONC, CONC_D = C('#d9d5cb'), C('#a8a397')
WATER, WATER_D, WATER_DD, WATER_L, WATER_LINE = C('#5cbccf'), C('#43a3bf'), C('#3690ad'), C('#a5e1e8'), C('#2b6f8c')
ROCK = [C('#b7b0a6'), C('#a39c92'), C('#c6c0b6')]
ROCK_LINE = C('#5f5a55')
LEAF = Pal('#5aa552', '#7cc068', '#3f8546', '#234f2e')
LEAF2 = Pal('#6fae4d', '#93c965', '#4e8f3f', '#2a5a2a')
LEAF_DARK = Pal('#3f8650', '#59a164', '#2e6a40', '#1c4027')
FOREST = Pal('#3b7447', '#4c8a56', '#2b5a38', '#183624')
FOREST2 = Pal('#467f4b', '#5c995c', '#34663c', '#1b3b26')
FLOWERS = [C('#f0679a'), C('#e8483f'), C('#f7c948'), C('#fff5e6'), C('#9d72d8'), C('#f58a3c'), C('#ff9fc0')]
WARM = C('#ffd98a')


def cells(ctx, x0, y0, x1, y1, size, seed):
    """Deterministic per-cell RNGs; skips cells the canvas cannot see."""
    iy = 0
    y = y0
    while y < y1:
        ix = 0
        x = x0
        while x < x1:
            xb, yb = min(x + size, x1), min(y + size, y1)
            if ctx.sees(x - 0.5, y - 0.5, xb + 0.5, yb + 0.5):
                yield random.Random(seed * 1000003 + ix * 9176 + iy * 131), x, y, xb, yb
            x += size
            ix += 1
        y += size
        iy += 1


def poly_area(p):
    return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))) / 2


def bbox(p):
    xs, ys = [q[0] for q in p], [q[1] for q in p]
    return min(xs), min(ys), max(xs), max(ys)


def rects(ctx, items, col):
    if items:
        for r in items:
            ctx.rect(*r)
        ctx.fill(col)


# ------------------------------------------------------------- small plants
def tuft_path(ctx, x, y, s, rng):
    for k in (-1, 0, 1):
        a = -math.pi / 2 + k * 0.45 + rng.uniform(-0.15, 0.15)
        ctx.move_to(x + k * s * 0.18, y)
        ctx.line_to(x + k * s * 0.18 + math.cos(a) * s, y + math.sin(a) * s)


def small_plant(ctx, rng, x, y, kind=None, colors=FLOWERS, scale=1.0):
    kind = kind or rng.choice(['bloom', 'bloom', 'bloom', 'blades', 'lav', 'bloom2'])
    s = scale
    if kind in ('bloom', 'bloom2'):
        pal = rng.choice([LEAF, LEAF2, LEAF_DARK])
        r = rng.uniform(0.15, 0.24) * s
        circ = [(x + rng.uniform(-r, r) * 0.7, y - r * 0.6 + rng.uniform(-r, r) * 0.35, r * rng.uniform(0.65, 1.0))
                for _ in range(3)]
        foliage(ctx, rng, circ, pal, lw=0.022, leaves=False)
        col = rng.choice(colors)
        n = rng.randint(2, 4)
        for _ in range(n):
            fx, fy = x + rng.uniform(-r, r) * 1.1, y - r * 0.7 + rng.uniform(-r, r) * 0.8
            if kind == 'bloom':
                flower(ctx, fx, fy, r * 0.42, col, petals=5, rot=rng.random(), line=dk(col, 0.5))
            else:
                ctx.ellipse(fx, fy, r * 0.3, r * 0.3).fs(col, dk(col, 0.5), 0.012)
                ctx.ellipse(fx - r * 0.08, fy - r * 0.08, r * 0.11, r * 0.11).fill(lt(col, 0.6))
    elif kind == 'blades':
        col = rng.choice([C('#7dbb55'), C('#5fa64e'), C('#9acb62')])
        n = rng.randint(5, 8)
        for i in range(n):
            a = -math.pi / 2 + (i - (n - 1) / 2) * 0.33 + rng.uniform(-0.1, 0.1)
            leaf(ctx, x, y, rng.uniform(0.3, 0.48) * s, 0.045 * s, a)
        ctx.fs(col, dk(col, 0.55), 0.014)
    elif kind == 'lav':
        n = rng.randint(4, 7)
        for i in range(n):
            a = -math.pi / 2 + (i - (n - 1) / 2) * 0.28 + rng.uniform(-0.08, 0.08)
            ln = rng.uniform(0.3, 0.46) * s
            ex, ey = x + math.cos(a) * ln, y + math.sin(a) * ln
            ctx.move_to(x, y).line_to(ex, ey)
        ctx.stroke(C('#5f9150'), 0.02)
        col = rng.choice([C('#9d72d8'), C('#b48be6'), C('#7f5fc4')])
        for i in range(n):
            a = -math.pi / 2 + (i - (n - 1) / 2) * 0.28
            for t in (0.7, 0.85, 1.0):
                ln = 0.4 * s * t
                ctx.ellipse(x + math.cos(a) * ln, y + math.sin(a) * ln, 0.035 * s, 0.045 * s)
        ctx.fs(col, dk(col, 0.45), 0.01)


def rock(ctx, rng, x, y, r):
    pts = blob(rng, x, y, r, r * 0.72, n=7, jit=0.22)
    col = rng.choice(ROCK)
    ctx.ellipse(x + r * 0.1, y + r * 0.45, r * 1.0, r * 0.35).fill((0.1, 0.08, 0.15, 0.18))
    ctx.poly(pts).fs(col, ROCK_LINE, 0.022)
    ctx.poly([(x + (px - x) * 0.55 - r * 0.15, y + (py - y) * 0.5 - r * 0.2) for px, py in pts]).fill(lt(col, 0.3))


def lantern(ctx, x, y, s=1.0):
    """Little floor lantern (baked, it is tiny)."""
    glow(ctx, x, y - 0.1 * s, 0.9 * s, 0.55 * s, WARM, 0.35, steps=10)
    ctx.ellipse(x, y + 0.02, 0.17 * s, 0.06 * s).fill((0.1, 0.08, 0.15, 0.25))
    ctx.rect(x - 0.12 * s, y - 0.36 * s, 0.24 * s, 0.36 * s).fs(C('#ffe9a8'), INK, 0.018)
    ctx.ellipse(x, y - 0.14 * s, 0.045 * s, 0.09 * s).fill(C('#fff7d6'))
    ctx.move_to(x, y - 0.36 * s).line_to(x, y)
    ctx.stroke(INK, 0.014)
    ctx.poly([(x - 0.15 * s, y - 0.36 * s), (x + 0.15 * s, y - 0.36 * s), (x + 0.07 * s, y - 0.46 * s),
              (x - 0.07 * s, y - 0.46 * s)]).fs(C('#4a4050'), INK, 0.016)
    ctx.arc(x, y - 0.46 * s, 0.07 * s, 0.09 * s, math.pi, math.tau, n=8).stroke(INK, 0.014)


# ------------------------------------------------------------------ surfaces
def gravel(ctx):
    ctx.rect(2.5, 3.5, 75.2, 58).fill(GRAVEL)
    skip = [(23, 6, 65, 25), (59.3, 30.3, 77, 55.7), (4.5, 30.5, 19.5, 58.5), (65, 4, 77, 25),
            (3, 4.5, 21.5, 24.5), (41.4, 46, 46.6, 61), (22, 25.2, 66, 29.3)]
    for rng, x0, y0, x1, y1 in cells(ctx, 3, 4, 77, 61, 4, 11):
        # soft tonal patches
        for _ in range(3):
            px, py = rng.uniform(x0, x1), rng.uniform(y0, y1)
            ctx.smooth(blob(rng, px, py, rng.uniform(0.6, 1.6), rng.uniform(0.3, 0.8), n=8, jit=0.25))
            ctx.fill(al(rng.choice([GRAVEL_L, GRAVEL_D]), 0.13))
        for col, n, r0, r1 in ((GRAVEL_D, 300, 0.018, 0.04), (GRAVEL_L, 260, 0.018, 0.045), (C('#b39d78'), 90, 0.02, 0.035)):
            for _ in range(n):
                x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
                if any(a < x < c and b < y < d for a, b, c, d in skip):
                    continue
                r = rng.uniform(r0, r1)
                a0 = rng.random() * 3
                ctx.poly([(x + math.cos(a0 + k * 1.257) * r * rng.uniform(0.7, 1.15),
                           y + math.sin(a0 + k * 1.257) * r * 0.8 * rng.uniform(0.7, 1.15)) for k in range(5)])
            ctx.fill(col)
        for _ in range(9):   # a few bigger outlined pebbles
            x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
            if any(a < x < c and b < y < d for a, b, c, d in skip):
                continue
            r = rng.uniform(0.05, 0.09)
            ctx.smooth(blob(rng, x, y, r, r * 0.7, n=6, jit=0.2)).fs(rng.choice(ROCK), GRAVEL_LINE, 0.014)
            ctx.ellipse(x - r * 0.2, y - r * 0.2, r * 0.35, r * 0.2).fill(al(C('#ffffff'), 0.5))


def grass_area(ctx, pts, seed, base=GRASS, light=GRASS_L, dark=GRASS_D, stripe=None,
               flowers=0.5, smooth_=True, tufts=3.2, edge=True):
    poly = spline_pts(pts) if smooth_ else list(pts)
    x0, y0, x1, y1 = bbox(poly)
    if not ctx.sees(x0, y0, x1, y1):
        return poly
    if edge:
        ctx.poly(poly).stroke(al(GRASS_LINE, 0.55), 0.16)
    ctx.poly(poly).fill(base)
    ctx.poly(poly).clip_here()
    if stripe is not None:
        ang, bw = stripe
        ctx.save()
        ctx.translate((x0 + x1) / 2, (y0 + y1) / 2)
        ctx.rotate(ang)
        R = math.hypot(x1 - x0, y1 - y0) / 2 + 1
        k = -int(R / bw) - 1
        while k * bw < R:
            if k % 2 == 0:
                ctx.rect(-R, k * bw, 2 * R, bw)
            k += 1
        ctx.fill(al(light, 0.55))
        ctx.restore()
    for rng, cx0, cy0, cx1, cy1 in cells(ctx, x0, y0, x1, y1, 4, seed):
        for _ in range(4):
            px, py = rng.uniform(cx0, cx1), rng.uniform(cy0, cy1)
            ctx.smooth(blob(rng, px, py, rng.uniform(0.5, 1.4), rng.uniform(0.25, 0.7), n=8, jit=0.3))
            ctx.fill(al(rng.choice([dark, light]), 0.25))
        n = int((cx1 - cx0) * (cy1 - cy0) * tufts)
        for col in (dark, lt(light, 0.12)):
            for _ in range(n // 2):
                tuft_path(ctx, rng.uniform(cx0, cx1), rng.uniform(cy0, cy1), rng.uniform(0.07, 0.13), rng)
            ctx.stroke(col, 0.02)
        # tiny wild flowers in clusters
        for _ in range(int((cx1 - cx0) * (cy1 - cy0) * flowers / 4 + rng.random())):
            fx, fy = rng.uniform(cx0, cx1), rng.uniform(cy0, cy1)
            col = rng.choice([C('#fffbe8'), C('#ffe45c'), C('#fffbe8'), C('#f6a6c9'), C('#c9b2f2')])
            m = rng.randint(3, 7)
            for _ in range(m):
                ctx.ellipse(fx + rng.gauss(0, 0.22), fy + rng.gauss(0, 0.14), 0.035, 0.03)
            ctx.fill(col)
    ctx.unclip()
    if edge:
        ctx.poly(poly).stroke(GRASS_LINE, 0.028)
        # blades hanging over the border
        rng = random.Random(seed + 5)
        for x, y, a in walk(poly, 0.16, closed=True):
            if rng.random() < 0.55:
                nx, ny = math.sin(a), -math.cos(a)
                if poly_sign(poly) < 0:
                    nx, ny = -nx, -ny
                s = rng.uniform(0.05, 0.11)
                ctx.move_to(x, y).line_to(x + nx * s + rng.uniform(-0.03, 0.03), y + ny * s * 0.8)
        ctx.stroke(GRASS_LINE, 0.022)
    return poly


def poly_sign(p):
    return sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))


def tile_field(ctx, rng, x0, y0, x1, y1, tw, th, cols, grout, gap=0.035, stagger=0.5):
    if not ctx.sees(x0, y0, x1, y1):
        return
    ctx.rect(x0, y0, x1 - x0, y1 - y0).fill(grout)
    buckets = [[] for _ in cols]
    row, y = 0, y0
    while y < y1 - 1e-6:
        x = x0 - (row % 2) * stagger * tw
        while x < x1 - 1e-6:
            xa, xb, yb = max(x, x0), min(x + tw, x1), min(y + th, y1)
            k = rng.randrange(len(cols))
            if xb - xa > gap * 2 and yb - y > gap * 2:
                buckets[k].append((xa + gap / 2, y + gap / 2, xb - xa - gap, yb - y - gap))
            x += tw
        y += th
        row += 1
    for b, c in zip(buckets, cols):
        rects(ctx, b, c)


def boardwalk(ctx, seed, x0, y0, x1, y1, w, pw=0.36, cols=BOARD, line=BOARD_LINE):
    if not ctx.sees(min(x0, x1) - w, min(y0, y1) - w, max(x0, x1) + w, max(y0, y1) + w):
        return
    rng = random.Random(seed)
    ln = math.hypot(x1 - x0, y1 - y0)
    ang = math.atan2(y1 - y0, x1 - x0)
    # drop shadow gives it a little thickness
    ctx.save()
    ctx.translate(x0 + 0.05, y0 + 0.13)
    ctx.rotate(ang)
    ctx.rect(-0.03, -w / 2, ln + 0.06, w).fill(al(dk(line, 0.3), 0.55))
    ctx.restore()
    ctx.save()
    ctx.translate(x0, y0)
    ctx.rotate(ang)
    ctx.rect(0, -w / 2, ln, w).fs(dk(line, 0.1), line, 0.03)
    buckets = [[] for _ in cols]
    x = 0.0
    n = max(1, round(ln / pw))
    pw = ln / n
    for i in range(n):
        buckets[rng.randrange(len(cols))].append((i * pw + 0.018, -w / 2 + 0.03, pw - 0.036, w - 0.06))
    for b, c in zip(buckets, cols):
        rects(ctx, b, c)
    for i in range(n):          # grain + nails
        xx = i * pw
        if rng.random() < 0.6:
            gy = rng.uniform(-w / 2 + 0.2, w / 2 - 0.5)
            gx = xx + rng.uniform(0.1, pw - 0.1)
            ctx.move_to(gx, gy).line_to(gx + rng.uniform(-0.02, 0.02), gy + rng.uniform(0.2, 0.5))
        ctx.stroke(al(line, 0.45), 0.014)
        for sy in (-w / 2 + 0.16, w / 2 - 0.16):
            ctx.ellipse(xx + pw / 2, sy, 0.022, 0.022)
        ctx.fill(al(line, 0.75))
    # side stringers highlight
    ctx.rect(0, -w / 2, ln, 0.035).fill(al(C('#fff3dc'), 0.35))
    ctx.restore()


# ----------------------------------------------------------------- features
def flowerbed(ctx, pts, seed, colors=FLOWERS, dens=4.2, edge=STONE[0], smooth_=True, soil=SOIL, kinds=None,
              border=True):
    poly = spline_pts(pts) if smooth_ else list(pts)
    x0, y0, x1, y1 = bbox(poly)
    if not ctx.sees(x0 - 1, y0 - 1, x1 + 1, y1 + 1):
        return
    rng = random.Random(seed)
    if border:
        ctx.poly(poly).stroke(dk(edge, 0.5), 0.27)
        ctx.poly(poly).stroke(edge, 0.2)
        for x, y, a in walk(poly, 0.3, closed=True):
            ctx.move_to(x - math.sin(a) * 0.1, y + math.cos(a) * 0.1).line_to(x + math.sin(a) * 0.1, y - math.cos(a) * 0.1)
        ctx.stroke(dk(edge, 0.42), 0.014)
    ctx.poly(poly).fs(soil, dk(soil, 0.4), 0.02)
    ctx.poly(poly).clip_here()
    for _ in range(int(poly_area(poly) * 9)):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        ctx.ellipse(x, y, rng.uniform(0.02, 0.05), rng.uniform(0.015, 0.03))
    ctx.fill(al(SOIL_D, 0.8))
    for _ in range(int(poly_area(poly) * 5)):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        ctx.ellipse(x, y, rng.uniform(0.02, 0.04), rng.uniform(0.015, 0.025))
    ctx.fill(al(SOIL_L, 0.9))
    ctx.unclip()
    n = int(poly_area(poly) * dens)
    cand = [(rng.uniform(x0, x1), rng.uniform(y0 + 0.12, y1)) for _ in range(n * 2)]
    ok = inside(poly, cand)
    cand = sorted([c for c, k in zip(cand, ok) if k][:n], key=lambda c: c[1])
    for x, y in cand:
        small_plant(ctx, rng, x, y, kind=rng.choice(kinds) if kinds else None, colors=colors)


def stepping_stones(ctx, pts, seed, step=1.15, r=0.42):
    rng = random.Random(seed)
    for x, y, a in walk(spline_pts(pts, closed=False), step):
        rr = r * rng.uniform(0.85, 1.15)
        p = blob(rng, x + rng.uniform(-0.08, 0.08), y, rr, rr * F, n=8, jit=0.13)
        ctx.smooth([(px + 0.03, py + 0.07) for px, py in p]).fill(al(GRASS_LINE, 0.6))
        col = rng.choice(STONE)
        ctx.smooth(p).fs(col, STONE_LINE, 0.022)
        ctx.smooth([(x + (px - x) * 0.6 - 0.04, y + (py - y) * 0.55 - 0.03) for px, py in p]).fill(lt(col, 0.25))
        if rng.random() < 0.5:
            ctx.move_to(x - rr * 0.3, y + rr * 0.1).line_to(x + rr * 0.1, y + rr * 0.25)
            ctx.stroke(al(STONE_LINE, 0.7), 0.012)


def tree_marks(ctx):
    rng = random.Random(77)
    for name, x, y, mark in L.PROPS:
        if mark is None or not ctx.sees(x - 5, y - 2, x + 5, y + 2):
            continue
        big = 1.25 if ('eucalyptus' in name or 'palm' in name or 'olive' in name) else 0.85
        if 'cypress' in name:
            big = 0.6
        if mark == 'mulch':
            ctx.smooth(blob(rng, x, y, big, big * F, n=10, jit=0.1)).fs(C('#7a5638'), al(GRASS_LINE, 0.9), 0.025)
            for _ in range(int(60 * big)):
                a, d = rng.random() * math.tau, math.sqrt(rng.random()) * 0.92
                px, py = x + math.cos(a) * big * d, y + math.sin(a) * big * F * d
                ctx.move_to(px, py).line_to(px + rng.uniform(-0.06, 0.06), py + rng.uniform(-0.03, 0.03))
            ctx.stroke(C('#5a3c26'), 0.022)
            for _ in range(int(25 * big)):
                a, d = rng.random() * math.tau, math.sqrt(rng.random()) * 0.92
                px, py = x + math.cos(a) * big * d, y + math.sin(a) * big * F * d
                ctx.move_to(px, py).line_to(px + rng.uniform(-0.06, 0.06), py + rng.uniform(-0.03, 0.03))
            ctx.stroke(C('#a17a52'), 0.02)
        elif mark in ('ring', 'sand'):
            rx, ry = big, big * F
            n = int(14 * big) + 6
            ctx.ellipse(x, y, rx + 0.14, ry + 0.1).fill(dk(STONE[0], 0.5))
            for i in range(n):
                a0, a1 = i * math.tau / n + 0.03, (i + 1) * math.tau / n - 0.03
                pts = [(x + math.cos(a) * (rx + d), y + math.sin(a) * (ry + d * 0.75))
                       for a, d in ((a0, 0.12), (a1, 0.12), (a1, -0.1), (a0, -0.1))]
                ctx.poly(pts).fill(rng.choice(ROCK if mark == 'sand' else STONE))
            ctx.ellipse(x, y, rx - 0.1, ry - 0.075).fs(SOIL, dk(SOIL, 0.4), 0.02)
            for _ in range(22):
                a, d = rng.random() * math.tau, math.sqrt(rng.random()) * 0.8
                ctx.ellipse(x + math.cos(a) * rx * d, y + math.sin(a) * ry * d, 0.035, 0.022)
            ctx.fill(SOIL_L)
        elif mark == 'deck':
            ctx.rrect(x - 1.25, y - 0.82, 2.5, 1.5, 0.12).fs(SOIL, WOOD_LINE, 0.05)
            ctx.rrect(x - 1.25, y - 0.82, 2.5, 0.16, 0.05).fill(al(INK, 0.3))
            for _ in range(40):
                ctx.ellipse(x + rng.uniform(-1.1, 1.1), y + rng.uniform(-0.6, 0.55), 0.04, 0.025)
            ctx.fill(SOIL_L)
            for _ in range(6):
                small_plant(ctx, rng, x + rng.choice([-1, 1]) * rng.uniform(0.55, 1.0), y + rng.uniform(-0.3, 0.55), 'blades')
        elif mark == 'foot':
            ctx.ellipse(x, y + 0.03, 0.3, 0.19).fill(al(INK, 0.25))
            ctx.ellipse(x, y, 0.26, 0.16).fs(CONC, CONC_D, 0.02)
        elif mark == 'poles':
            for dx in (-4, 4):
                ctx.ellipse(x + dx, y, 0.2, 0.12).fs(CONC, CONC_D, 0.02)
        elif mark == 'arch':
            for dx in (-3.05, 3.05):
                ctx.rrect(x + dx - 0.3, y - 0.2, 0.6, 0.36, 0.05).fs(STONE[1], STONE_LINE, 0.022)


def pond(ctx, cx, cy, rx, ry, seed):
    if not ctx.sees(cx - rx - 2, cy - ry - 2, cx + rx + 2, cy + ry + 2):
        return
    rng = random.Random(seed)
    pts = blob(rng, cx, cy, rx, ry, n=11, jit=0.15)
    poly = spline_pts(pts)
    grow = lambda s, dy=0.0: [(cx + (x - cx) * s, cy + (y - cy) * s + dy) for x, y in pts]
    ctx.smooth(grow(1.1)).fs(C('#8f7a55'), al(GRASS_LINE, 0.8), 0.025)       # muddy bank
    ctx.smooth(pts).fs(WATER, WATER_LINE, 0.04)
    ctx.smooth(grow(0.8, 0.08)).fill(WATER_D)
    ctx.smooth(grow(0.5, 0.12)).fill(WATER_DD)
    ctx.smooth(pts).clip_here()
    ctx.smooth(grow(1.0, 0.13), closed=True).stroke(al(WATER_LINE, 0.45), 0.09)   # inner bank shadow
    for _ in range(26):                                                         # ripples
        x, y = cx + rng.uniform(-rx, rx), cy + rng.uniform(-ry, ry)
        w = rng.uniform(0.25, 0.7)
        ctx.arc(x, y, w, w * 0.18, math.pi * 1.1, math.pi * 1.9, n=8)
    ctx.stroke(al(WATER_L, 0.85), 0.022)
    for _ in range(5):                                                          # koi
        x, y = cx + rng.uniform(-rx, rx) * 0.6, cy + rng.uniform(-ry, ry) * 0.6
        a = rng.random() * math.tau
        col = rng.choice([C('#f58a3c'), C('#fff2e0'), C('#e8483f')])
        leaf(ctx, x, y, 0.42, 0.09, a).fs(col, al(INK, 0.5), 0.012)
        leaf(ctx, x - math.cos(a) * 0.02, y - math.sin(a) * 0.02, -0.16, 0.08, a).fill(col)
    ctx.unclip()
    for _ in range(11):                                                         # lily pads
        a, d = rng.random() * math.tau, rng.uniform(0.25, 0.85)
        x, y = cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d
        r = rng.uniform(0.17, 0.3)
        na = rng.random() * math.tau
        ctx.move_to(x, y)
        ctx.arc(x, y, r, r * F, na + 0.35, na + math.tau - 0.35, n=14, move=False).close()
        ctx.fs(rng.choice([C('#6fba5a'), C('#57a550'), C('#86c765')]), C('#2f6a36'), 0.018)
        if rng.random() < 0.5:
            flower(ctx, x + r * 0.2, y - r * 0.15, 0.085, rng.choice([C('#ff9fc0'), C('#fff5e6')]), petals=6, line=C('#b85c82'))
    # shore stones
    for x, y, a in walk(poly, 0.42, closed=True):
        if rng.random() < 0.78:
            rock(ctx, rng, x + rng.uniform(-0.06, 0.06), y + rng.uniform(-0.05, 0.05), rng.uniform(0.13, 0.27))
    # reeds on the far (north) bank
    for x, y, a in walk(poly, 0.5, closed=True):
        if y < cy - ry * 0.35 and rng.random() < 0.8:
            n = rng.randint(4, 7)
            for i in range(n):
                aa = -math.pi / 2 + (i - (n - 1) / 2) * 0.16 + rng.uniform(-0.05, 0.05)
                leaf(ctx, x + rng.uniform(-0.1, 0.1), y, rng.uniform(0.6, 1.1), 0.04, aa)
            ctx.fs(C('#6aa84f'), C('#2f6a36'), 0.014)
            for i in range(2):
                hx, hy = x + rng.uniform(-0.2, 0.2), y - rng.uniform(0.7, 1.1)
                ctx.move_to(hx, y - 0.1).line_to(hx, hy)
                ctx.stroke(C('#4f8a45'), 0.02)
                ctx.rrect(hx - 0.04, hy - 0.2, 0.08, 0.24, 0.04).fs(C('#7a4a2a'), INK, 0.012)
    # flat stepping stones crossing the water
    for i in range(4):
        t = (i + 0.5) / 4
        x = cx - rx * 0.15 + (t - 0.5) * 1.0
        y = cy - ry * 0.8 + t * ry * 1.6
        p = blob(rng, x, y, 0.36, 0.36 * F, n=8, jit=0.12)
        ctx.smooth([(px + 0.02, py + 0.07) for px, py in p]).fill(al(WATER_LINE, 0.6))
        ctx.smooth(p).fs(rng.choice(STONE), STONE_LINE, 0.022)


def plaza(ctx, cx, cy, rx):
    ry = rx * F
    if not ctx.sees(cx - rx - 1, cy - ry - 1, cx + rx + 1, cy + ry + 1):
        return
    rng = random.Random(31)
    ctx.ellipse(cx + 0.04, cy + 0.12, rx + 0.12, ry + 0.1).fill(al(INK, 0.25))
    ctx.ellipse(cx, cy, rx + 0.1, ry + 0.07).fs(COBBLE_LINE, dk(COBBLE_LINE, 0.3), 0.03)
    ring_w = 0.5
    r = rx
    k = 0
    while r > 0.9:
        r0 = r - ring_w
        band = k in (3, 4, 10)            # decorative darker rings
        curb = k == 0
        n = max(8, int(math.tau * r / (0.62 if not curb else 0.95)))
        off = rng.random()
        buckets = {}
        for i in range(n):
            a0, a1 = (i + off) * math.tau / n + 0.012 / r * 2, (i + 1 + off) * math.tau / n - 0.012 / r * 2
            pts = [(cx + math.cos(a) * rr, cy + math.sin(a) * rr * F)
                   for a, rr in ((a0, r - 0.03), ((a0 + a1) / 2, r - 0.03), (a1, r - 0.03),
                                 (a1, r0 + 0.03), ((a0 + a1) / 2, r0 + 0.03), (a0, r0 + 0.03))]
            if curb:
                col = rng.choice(STONE)
            elif band:
                col = rng.choice([C('#b9775f'), C('#a9694f'), C('#c58a70')])
            else:
                col = rng.choice(COBBLE)
            buckets.setdefault(col, []).append(pts)
        for col, lst in buckets.items():
            for pts in lst:
                ctx.poly(pts)
            ctx.fill(col)
        r = r0
        k += 1
    # centre medallion
    ctx.ellipse(cx, cy, r + 0.02, (r + 0.02) * F).fs(C('#e9e2d2'), COBBLE_LINE, 0.025)
    for i in range(16):
        a = i * math.tau / 16
        rr = r * (0.92 if i % 2 == 0 else 0.42)
        if i == 0:
            ctx.move_to(cx + math.cos(a) * rr, cy + math.sin(a) * rr * F)
        else:
            ctx.line_to(cx + math.cos(a) * rr, cy + math.sin(a) * rr * F)
    ctx.close().fs(C('#b9775f'), dk(C('#b9775f'), 0.5), 0.02)
    for i in range(8):
        a = i * math.tau / 8
        ctx.move_to(cx, cy).line_to(cx + math.cos(a) * r * 0.92, cy + math.sin(a) * r * 0.92 * F)
    ctx.stroke(al(INK, 0.35), 0.014)
    ctx.ellipse(cx, cy, 0.18, 0.18 * F).fs(C('#5fb0c4'), COBBLE_LINE, 0.02)
    # soft sheen
    ctx.ellipse(cx - rx * 0.25, cy - ry * 0.3, rx * 0.55, ry * 0.4).fill(al(C('#ffffff'), 0.07))


def entrance_path(ctx):
    x0, x1, y0, y1 = 41.0, 47.0, 44.6, 64.0
    if not ctx.sees(x0 - 2, y0 - 1, x1 + 2, y1):
        return
    rng = random.Random(41)
    ctx.rect(x0 - 0.04, y0, x1 - x0 + 0.08, y1 - y0).fill(BRICK_LINE)
    for xb in (x0, x1 - 0.42):                                   # brick borders
        y = y0
        while y < y1:
            ctx.rect(xb + 0.02, y + 0.015, 0.38, 0.215).fill(rng.choice(BRICK))
            y += 0.245
    tile_field(ctx, rng, x0 + 0.42, y0, x1 - 0.42, y1, 1.72, 1.07, [CONC, lt(CONC, 0.2), dk(CONC, 0.05)], CONC_D,
               gap=0.045, stagger=0.5)
    # centre inlay line of small dark tiles
    y = y0 + 0.1
    while y < 61:
        ctx.poly([(44, y), (44.26, y + 0.17), (44, y + 0.34), (43.74, y + 0.17)])
        y += 1.07
    ctx.fs(C('#b9775f'), BRICK_LINE, 0.015)
    for _ in range(24):                                          # hairline cracks / speckles
        x, y = rng.uniform(x0 + 0.6, x1 - 0.6), rng.uniform(y0, 61)
        ctx.move_to(x, y).line_to(x + rng.uniform(-0.2, 0.2), y + rng.uniform(0.05, 0.2))
    ctx.stroke(al(CONC_D, 0.8), 0.012)


def terrace(ctx):
    x0, x1, y0, y1 = 20.6, 67.4, 25.0, 29.5
    if not ctx.sees(x0, y0, x1, y1 + 1):
        return
    rng = random.Random(51)
    ctx.rect(x0 + 0.06, y1, x1 - x0, 0.5).fill(al(INK, 0.22))        # shadow under the step
    tile_field(ctx, rng, x0, y0, x1, y1, 1.56, 0.9, STONE, STONE_LINE, gap=0.04)
    for _ in range(40):
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        ctx.move_to(x, y).line_to(x + rng.uniform(-0.25, 0.25), y + rng.uniform(-0.1, 0.1))
    ctx.stroke(al(STONE_LINE, 0.6), 0.012)
    for _ in range(46):                                               # moss in the joints
        x = x0 + rng.random() * (x1 - x0)
        y = y0 + rng.randrange(1, 5) * 0.9
        for _ in range(3):
            ctx.ellipse(x + rng.uniform(-0.12, 0.12), y + rng.uniform(-0.02, 0.02), 0.05, 0.028)
        ctx.fill(al(GRASS_D, 0.9))
    # step face
    ctx.rect(x0, y1, x1 - x0, 0.26).fs(dk(STONE[1], 0.22), STONE_LINE, 0.022)
    x = x0
    while x < x1:
        ctx.move_to(x, y1).line_to(x, y1 + 0.26)
        x += 1.56
    ctx.stroke(al(STONE_LINE, 0.8), 0.014)
    ctx.rect(x0, y1 - 0.05, x1 - x0, 0.05).fill(al(C('#ffffff'), 0.35))
    ctx.rect(x0, y0, x1 - x0, y1 - y0).stroke(STONE_LINE, 0.025)


def patio(ctx):
    """North-east brick patio with raised herb beds."""
    if not ctx.sees(65, 4, 77.2, 30):
        return
    rng = random.Random(61)
    for (x0, y0, x1, y1) in ((65.0, 4.0, 77.05, 25.0), (67.4, 25.0, 77.05, 29.76)):
        tile_field(ctx, rng, x0, y0, x1, y1, 0.66, 0.24, BRICK, BRICK_LINE, gap=0.03)
    ctx.rect(65, 4, 12.05, 21).clip_here()
    for _ in range(26):
        ctx.smooth(blob(rng, rng.uniform(65, 77), rng.uniform(4, 29.5), rng.uniform(0.5, 1.4), rng.uniform(0.3, 0.7), n=8, jit=0.3))
        ctx.fill(al(rng.choice([C('#ffffff'), C('#5a2a1c')]), 0.07))
    ctx.unclip()
    # raised beds
    herbs = [[C('#9d72d8')], [C('#fff5e6'), C('#f7c948')], [C('#e8483f')], [C('#f58a3c'), C('#f7c948')]]
    for i, (bx, by) in enumerate(((67.0, 7.0), (71.4, 7.0), (67.0, 10.6), (71.4, 10.6))):
        w, h = 3.6, 1.5
        ctx.rect(bx + 0.06, by + h + 0.3, w, 0.22).fill(al(INK, 0.22))
        ctx.rect(bx, by + h, w, 0.36).fs(WOOD[3], WOOD_LINE, 0.025)            # front face
        ctx.move_to(bx, by + h + 0.18).line_to(bx + w, by + h + 0.18)
        ctx.stroke(al(WOOD_LINE, 0.7), 0.014)
        ctx.rect(bx, by, w, h).fs(WOOD[2], WOOD_LINE, 0.025)                    # frame top
        ctx.rect(bx + 0.14, by + 0.12, w - 0.28, h - 0.22).fs(SOIL, WOOD_LINE, 0.02)
        r2 = random.Random(600 + i)
        for row in range(3):
            for k in range(9):
                small_plant(ctx, r2, bx + 0.42 + k * 0.345, by + 0.5 + row * 0.38,
                            kind=['lav', 'bloom2', 'blades', 'bloom'][i], colors=herbs[i], scale=0.85)
    # basin under the wall fountain
    bx, by = 71.0, 4.05
    ctx.move_to(bx - 1.1, by)
    ctx.arc(bx, by, 1.1, 0.75, math.pi, 0, n=20, move=False)
    ctx.close()
    ctx.arc(bx, by, 1.1, 0.75, 0, math.pi, n=20).close().fs(STONE[2], STONE_LINE, 0.03)
    ctx.arc(bx, by, 0.9, 0.58, 0, math.pi, n=20).close().fs(WATER, WATER_LINE, 0.025)
    ctx.arc(bx, by + 0.05, 0.55, 0.3, 0.3, math.pi - 0.3, n=10).stroke(WATER_L, 0.022)
    ctx.arc(bx, by + 0.02, 0.3, 0.14, 0.2, math.pi - 0.2, n=10).stroke(WATER_L, 0.022)


def deck(ctx):
    x0, x1, y0, y1 = 59.0, 77.05, 30.0, 56.0
    if not ctx.sees(x0 - 1, y0 - 1, x1, y1 + 1.5):
        return
    rng = random.Random(71)
    ctx.rect(x0 - 0.08, y0 + 0.12, x1 - x0 + 0.1, y1 - y0 + 0.75).fill(al(INK, 0.25))
    ctx.rect(x0, y0, x1 - x0, y1 - y0).fill(WOOD_LINE)
    ph = 0.25
    buckets = [[] for _ in WOOD]
    marks = []
    y, row = y0, 0
    while y < y1 - 1e-6:
        x = x0 - rng.uniform(0, 4)
        while x < x1:
            ln = rng.uniform(3.2, 6.5)
            xa, xb = max(x, x0), min(x + ln, x1)
            if xb - xa > 0.05:
                buckets[rng.randrange(len(WOOD))].append((xa + 0.012, y + 0.014, xb - xa - 0.024, ph - 0.028))
                marks.append((xa, xb, y))
            x += ln
        y += ph
        row += 1
    for b, c in zip(buckets, WOOD):
        rects(ctx, b, c)
    for xa, xb, y in marks:                                            # grain, knots, screws
        if rng.random() < 0.5 and xb - xa > 1:
            gx = rng.uniform(xa + 0.2, xb - 0.8)
            ctx.move_to(gx, y + ph * 0.5).line_to(gx + rng.uniform(0.3, 0.7), y + ph * rng.uniform(0.35, 0.65))
    ctx.stroke(al(WOOD_LINE, 0.4), 0.014)
    for xa, xb, y in marks:
        if xa > x0 + 0.01:
            ctx.ellipse(xa + 0.07, y + ph / 2, 0.02, 0.02)
        if rng.random() < 0.08 and xb - xa > 1:
            ctx.ellipse(rng.uniform(xa + 0.3, xb - 0.3), y + ph / 2, 0.05, 0.035)
    ctx.fill(al(WOOD_LINE, 0.7))
    # light variation
    ctx.rect(x0, y0, x1 - x0, y1 - y0).clip_here()
    for _ in range(30):
        ctx.smooth(blob(rng, rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(1, 3), rng.uniform(0.5, 1.2), n=8, jit=0.3))
        ctx.fill(al(rng.choice([C('#fff0c8'), C('#4a2a14')]), 0.06))
    ctx.unclip()
    # border boards + front face
    ctx.rect(x0, y0, x1 - x0, 0.2).fs(WOOD[3], WOOD_LINE, 0.022)
    ctx.rect(x0, y0, 0.26, y1 - y0).fs(WOOD[3], WOOD_LINE, 0.022)
    ctx.rect(x0, y1 - 0.2, x1 - x0, 0.2).fs(WOOD[2], WOOD_LINE, 0.022)
    ctx.rect(x0, y1, x1 - x0, 0.42).fs(dk(WOOD[3], 0.3), WOOD_LINE, 0.025)
    x = x0
    while x < x1:
        ctx.move_to(x, y1).line_to(x, y1 + 0.42)
        x += 1.5
    ctx.move_to(x0, y1 + 0.21).line_to(x1, y1 + 0.21)
    ctx.stroke(al(WOOD_LINE, 0.75), 0.016)
    # wide steps down to the gravel on the west side
    for i, (sx, sw) in enumerate(((58.1, 0.45), (58.55, 0.45))):
        ctx.rect(sx + 0.04, 37.4 + 0.1, sw, 4.2 + 0.25).fill(al(INK, 0.2))
        ctx.rect(sx, 37.4, sw, 4.2).fs(WOOD[i], WOOD_LINE, 0.025)
        ctx.rect(sx, 41.6, sw, 0.14 + 0.1 * i).fs(dk(WOOD[3], 0.3), WOOD_LINE, 0.02)
    # planter trench along the east wall
    bx0, bx1 = 75.5, 77.0
    ctx.rect(bx0, 31.6, bx1 - bx0, 23.2).fs(SOIL, WOOD_LINE, 0.04)
    r2 = random.Random(72)
    yy = 32.0
    while yy < 54.6:
        small_plant(ctx, r2, r2.uniform(bx0 + 0.3, bx1 - 0.3), yy, kind=r2.choice(['blades', 'blades', 'bloom', 'lav']), scale=1.5)
        yy += r2.uniform(0.25, 0.5)


def desert(ctx, pts, seed):
    poly = spline_pts(pts)
    x0, y0, x1, y1 = bbox(poly)
    if not ctx.sees(x0, y0, x1, y1):
        return
    rng = random.Random(seed)
    ctx.poly(poly).stroke(dk(SAND_D, 0.3), 0.16)
    ctx.poly(poly).fill(SAND)
    ctx.poly(poly).clip_here()
    for _ in range(40):                                                    # raked sand waves
        x, y = rng.uniform(x0, x1), rng.uniform(y0, y1)
        w = rng.uniform(0.8, 2.2)
        ctx.arc(x, y, w, 0.12, math.pi * 1.05, math.pi * 1.95, n=10)
    ctx.stroke(al(SAND_D, 0.8), 0.022)
    for _ in range(int(poly_area(poly) * 14)):
        ctx.ellipse(rng.uniform(x0, x1), rng.uniform(y0, y1), rng.uniform(0.02, 0.04), rng.uniform(0.015, 0.03))
    ctx.fill(al(SAND_D, 0.9))
    ctx.unclip()
    ctx.poly(poly).stroke(dk(SAND_D, 0.35), 0.025)
    cand = [(rng.uniform(x0 + 0.5, x1 - 0.5), rng.uniform(y0 + 0.5, y1 - 0.2)) for _ in range(90)]
    ok = inside([(x, y) for x, y in poly], cand)
    cand = sorted([c for c, k in zip(cand, ok) if k][:46], key=lambda c: c[1])
    for x, y in cand:
        t = rng.random()
        if t < 0.3:
            rock(ctx, rng, x, y, rng.uniform(0.15, 0.4))
        elif t < 0.62:                                                      # agave rosette
            col = rng.choice([C('#7fb7a2'), C('#6aa58f'), C('#93c7ad')])
            n = 9
            s = rng.uniform(0.35, 0.6)
            ctx.ellipse(x, y + 0.03, s * 0.8, s * 0.25).fill(al(INK, 0.18))
            for i in range(n):
                a = -math.pi + (i + 0.5) * math.pi / n
                leaf(ctx, x, y, s * (0.75 + 0.25 * math.sin((i + 0.5) * math.pi / n)), s * 0.16, a)
            ctx.fs(col, C('#2f5f55'), 0.016)
            for i in (2, 4, 6):
                a = -math.pi + (i + 0.5) * math.pi / n
                leaf(ctx, x, y, s * 0.55, s * 0.1, a)
            ctx.fill(lt(col, 0.3))
        elif t < 0.85:                                                      # barrel cactus
            r = rng.uniform(0.16, 0.27)
            ctx.ellipse(x, y + 0.02, r * 1.1, r * 0.35).fill(al(INK, 0.2))
            ctx.ellipse(x, y - r * 0.85, r, r).fs(C('#5fa56a'), C('#245233'), 0.02)
            for k in (-0.6, -0.2, 0.2, 0.6):
                ctx.arc(x, y - r * 0.85, abs(k) * r, r, -math.pi / 2, math.pi / 2, n=10) if k > 0 else \
                    ctx.arc(x, y - r * 0.85, abs(k) * r, r, math.pi / 2, math.pi * 1.5, n=10)
            ctx.stroke(al(C('#245233'), 0.7), 0.013)
            ctx.ellipse(x - r * 0.3, y - r * 1.25, r * 0.3, r * 0.2).fill(al(C('#ffffff'), 0.3))
            if rng.random() < 0.6:
                flower(ctx, x, y - r * 1.8, r * 0.3, rng.choice([C('#f0679a'), C('#f7c948')]), line=INK)
        else:
            small_plant(ctx, rng, x, y, 'blades', scale=1.2)


def dirt_path(ctx, pts, w=1.3):
    p = spline_pts(pts, closed=False, sub=10)
    ctx.poly(p, closed=False).stroke(al(GRASS_LINE, 0.7), w + 0.12)
    ctx.poly(p, closed=False).stroke(GRAVEL, w)
    ctx.poly(p, closed=False).stroke(al(GRAVEL_L, 0.5), w * 0.55)
    rng = random.Random(int(pts[0][0] * 10))
    for x, y, a in walk(p, 0.09):
        for col in (GRAVEL_D, GRAVEL_L):
            d = rng.uniform(-w / 2 + 0.06, w / 2 - 0.06)
            ctx.ellipse(x - math.sin(a) * d, y + math.cos(a) * d * 0.9, rng.uniform(0.018, 0.04), rng.uniform(0.014, 0.03))
            ctx.fill(col)


LAWN_W = [(3.2, 29.2), (10, 28.6), (17, 29.0), (20.3, 31.2), (20.8, 36.5), (20.2, 43.5), (20.8, 50), (20.2, 56),
          (16.5, 59.7), (9.5, 60.3), (3.2, 60.2), (2.8, 44)]
LAWN_SW = [(23.6, 51.8), (31, 50.8), (38.4, 51.6), (39.3, 56), (39.2, 60.4), (30, 60.6), (23.4, 60.3), (22.6, 56)]
LAWN_SE = [(48.9, 51.4), (54, 50.6), (57.6, 51.6), (58.0, 55), (56.4, 56.6), (49.2, 56.8), (48.7, 54)]
DESERT = [(48.8, 58.4), (56, 58.2), (59, 57.2), (67, 57.5), (76.9, 57.2), (77.2, 60.7), (62, 60.9), (48.8, 60.7)]
MEADOW_P = [(2.8, 3.6), (22.8, 3.6), (22.9, 13.0), (22.6, 24.6), (19.5, 26.3), (10, 26.2), (2.8, 26.6)]


def draw_outdoor(ctx):
    gravel(ctx)
    # ---- north-west meadow garden
    grass_area(ctx, MEADOW_P, 101, base=MEADOW, light=MEADOW_L, dark=MEADOW_D, flowers=2.6, smooth_=False, tufts=4.0)
    dirt_path(ctx, [(13.2, 27.6), (12.6, 24.0), (9.4, 21.2), (7.6, 17.0), (8.8, 12.8), (13.4, 11.0), (18.4, 12.6),
                    (21.0, 15.2), (23.4, 15.5)])
    dirt_path(ctx, [(12.6, 24.0), (16.5, 23.6), (20.4, 25.2), (22.4, 27.2)], w=1.1)
    dirt_path(ctx, [(13.4, 11.0), (13.0, 7.8), (13.6, 4.4)], w=1.0)
    pond(ctx, 13.6, 17.2, 3.7, 2.35, 7)
    flowerbed(ctx, [(3.2, 4.4), (9, 4.3), (9.6, 5.0), (3.2, 5.3)], 201, smooth_=False, dens=6)
    flowerbed(ctx, [(15.2, 4.3), (22.6, 4.3), (22.6, 5.2), (15.2, 5.0)], 202, smooth_=False, dens=6)
    flowerbed(ctx, blob(random.Random(3), 19.9, 17.9, 1.4, 0.85, n=9), 203, dens=6)
    flowerbed(ctx, blob(random.Random(4), 5.0, 14.6, 1.3, 1.0, n=9), 204, dens=6)
    flowerbed(ctx, [(3.2, 24.6), (9.5, 25.0), (9.6, 25.9), (3.2, 26.2)], 205, smooth_=False, dens=6)
    # ---- west ceremony lawn
    grass_area(ctx, LAWN_W, 102, stripe=(0.0, 1.25), flowers=0.25)
    ctx.smooth(LAWN_W).clip_here()                                   # mown aisle + petals
    ctx.rrect(10.6, 35.2, 2.8, 21.5, 1.2).fill(al(GRASS_L, 0.75))
    ctx.unclip()
    rng = random.Random(8)
    for side in (10.6, 13.4):
        for _ in range(170):
            ctx.ellipse(side + rng.gauss(0, 0.16), rng.uniform(36.2, 56.2), 0.05, 0.032)
        ctx.fill(C('#fff3f7'))
        for _ in range(90):
            ctx.ellipse(side + rng.gauss(0, 0.16), rng.uniform(36.2, 56.2), 0.05, 0.032)
        ctx.fill(C('#ffb3cf'))
    # chuppah dais (just the stone platform)
    dx, dy = 12.0, 33.4
    ctx.ellipse(dx + 0.05, dy + 0.2, 3.3, 3.3 * F).fill(al(INK, 0.22))
    ctx.ellipse(dx, dy + 0.14, 3.2, 3.2 * F).fs(dk(STONE[1], 0.25), STONE_LINE, 0.025)
    ctx.ellipse(dx, dy, 3.2, 3.2 * F).fs(STONE[2], STONE_LINE, 0.025)
    ctx.ellipse(dx, dy, 2.7, 2.7 * F).fs(STONE[0], al(STONE_LINE, 0.8), 0.018)
    ctx.ellipse(dx, dy, 1.5, 1.5 * F).fs(STONE[2], al(STONE_LINE, 0.8), 0.018)
    for i in range(24):
        a = i * math.tau / 24
        ctx.move_to(dx + math.cos(a) * 1.5, dy + math.sin(a) * 1.5 * F).line_to(dx + math.cos(a) * 2.7, dy + math.sin(a) * 2.7 * F)
    for i in range(36):
        a = (i + 0.5) * math.tau / 36
        ctx.move_to(dx + math.cos(a) * 2.7, dy + math.sin(a) * 2.7 * F).line_to(dx + math.cos(a) * 3.2, dy + math.sin(a) * 3.2 * F)
    ctx.stroke(al(STONE_LINE, 0.75), 0.014)
    flowerbed(ctx, [(dx + math.cos(a) * r, dy - 0.1 + math.sin(a) * r * F) for a, r in
                    [(math.pi * (1.08 + 0.84 * i / 9), 4.5) for i in range(10)] +
                    [(math.pi * (1.92 - 0.84 * i / 9), 3.75) for i in range(10)]], 206, dens=8)
    stepping_stones(ctx, [(20.2, 39.6), (17.5, 39.2), (15.2, 39.9), (13.6, 39.5)], 9, step=1.05)
    flowerbed(ctx, [(5.4, 59.0), (12, 59.4), (18.6, 58.8), (19.0, 59.7), (12, 60.4), (5.2, 60.2)], 207, dens=7)
    # hedge along the west fence
    rng = random.Random(12)
    y = 29.4
    circ = []
    while y < 60:
        circ.append((3.55 + rng.uniform(-0.1, 0.12), y, rng.uniform(0.5, 0.66)))
        y += 0.52
    if ctx.sees(2, 29, 5, 61):
        foliage(ctx, rng, circ, LEAF_DARK, lw=0.04)
        for x, yy, r in circ:
            for _ in range(3):
                ctx.ellipse(x + rng.uniform(-r, r) * 0.7, yy + rng.uniform(-r, r) * 0.7, 0.05, 0.05)
        ctx.fill(C('#fff9ea'))
    # ---- south lawns / desert garden
    grass_area(ctx, LAWN_SW, 103, stripe=(0.5, 1.1), flowers=0.5)
    grass_area(ctx, LAWN_SE, 104, stripe=(-0.5, 1.1), flowers=0.5)
    flowerbed(ctx, blob(random.Random(5), 29.8, 55.6, 1.7, 0.95, n=9), 208, dens=7)
    flowerbed(ctx, blob(random.Random(6), 35.2, 58.4, 1.5, 0.8, n=9), 209, dens=7)
    flowerbed(ctx, blob(random.Random(7), 55.2, 54.6, 1.3, 0.8, n=9), 210, dens=7)
    desert(ctx, DESERT, 13)
    # ---- paved things
    terrace(ctx)
    patio(ctx)
    entrance_path(ctx)
    for x0, x1 in ((39.5, 40.75), (47.25, 48.5)):                     # flower strips beside the entrance path
        flowerbed(ctx, [(x0, 46.2), (x1, 46.2), (x1, 60.4), (x0, 60.4)], int(x0 * 7), smooth_=False, dens=7.5,
                  colors=[C('#f0679a'), C('#e8483f'), C('#fff5e6'), C('#9d72d8')])
    boardwalk(ctx, 21, 44, 29.76, 44, 35.4, 3.0)
    boardwalk(ctx, 22, 20.5, 39.5, 37.0, 39.5, 2.2)
    boardwalk(ctx, 23, 51.0, 39.5, 58.2, 39.5, 2.2)
    boardwalk(ctx, 24, 39.4, 42.9, 25.2, 50.2, 1.8)
    boardwalk(ctx, 25, 48.6, 42.9, 57.6, 49.6, 1.8)
    boardwalk(ctx, 26, 44, 43.9, 44, 44.7, 3.4)
    plaza(ctx, 44, 39.5, 7.6)
    deck(ctx)
    # ---- flower islands around the eucalyptus trees + lanterns
    for i, (name, x, y, mark) in enumerate(L.PROPS):
        if mark == 'bed':
            flowerbed(ctx, blob(random.Random(300 + i), x, y + 0.1, 2.2, 1.35, n=10, jit=0.1), 310 + i, dens=6.5)
            ctx.ellipse(x, y, 0.75, 0.42).fs(C('#7a5638'), dk(SOIL, 0.4), 0.02)
    tree_marks(ctx)
    spots = [(42.2, 35.3), (45.8, 35.3), (9.0, 35.2), (15.0, 35.2), (21.0, 38.2), (21.0, 40.8), (58.0, 37.2),
             (58.0, 41.9), (16.4, 16.2), (10.2, 19.4), (40.8, 44.9), (47.2, 44.9)]
    for name, x, y, mark in L.PROPS:
        if mark == 'bed':
            spots += [(x - 2.25, y + 1.0), (x + 2.3, y - 0.75)]
    for x, y in spots:
        if ctx.sees(x - 1, y - 1, x + 1, y + 1):
            lantern(ctx, x, y)
