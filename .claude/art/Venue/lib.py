"""Tiny immediate-mode vector canvas on top of matplotlib's Agg renderer.

All coordinates are in world units, y grows DOWN (like image space).
"""
import math
import random

import numpy as np
from matplotlib.backends.backend_agg import RendererAgg
from matplotlib.path import Path
from matplotlib.transforms import Affine2D, TransformedPath

K = 0.5522847498  # bezier circle constant
F = 0.62          # ground foreshortening (circle on the floor -> ellipse)


# ----------------------------------------------------------------- colours
def C(h, a=1.0):
    h = h.lstrip('#')
    return (int(h[0:2], 16) / 255, int(h[2:4], 16) / 255, int(h[4:6], 16) / 255, a)


def mix(c1, c2, t):
    return (c1[0] + (c2[0] - c1[0]) * t, c1[1] + (c2[1] - c1[1]) * t,
            c1[2] + (c2[2] - c1[2]) * t, c1[3] if len(c1) > 3 else 1.0)


def lt(c, t):
    return mix(c, (1, 1, 1, 1), t)


def dk(c, t):
    return mix(c, (0.05, 0.03, 0.10, 1), t)


def al(c, a):
    return (c[0], c[1], c[2], a)


INK = C('#2b2233')


# ------------------------------------------------------------------ canvas
class Ctx:
    def __init__(self, w, h, ppu, ox=0.0, oy=0.0):
        self.w, self.h, self.ppu = w, h, ppu
        self.wpx, self.hpx = int(round(w * ppu)), int(round(h * ppu))
        self.r = RendererAgg(self.wpx, self.hpx, 72)
        self.base = (Affine2D().translate(-ox, -oy).scale(ppu, -ppu)
                     .translate(0, self.hpx).get_matrix())
        self.m = np.identity(3)
        self.stack = []
        self.clip = None
        self.gc = self.r.new_gc()
        self.gc.set_snap(False)
        self.gc.set_capstyle('round')
        self.gc.set_joinstyle('round')
        self.v = []
        self.c = []
        self.view = (ox, oy, ox + w, oy + h)

    # -- visibility helper (lets heavy scatter code skip off-screen work)
    def sees(self, x0, y0, x1, y1):
        a, b, c, d = self.view
        return not (x1 < a or x0 > c or y1 < b or y0 > d)

    # -- transform stack
    def save(self):
        self.stack.append((self.m.copy(), self.clip))

    def restore(self):
        self.m, self.clip = self.stack.pop()

    def translate(self, x, y):
        self.m = self.m @ Affine2D().translate(x, y).get_matrix()

    def rotate(self, a):
        self.m = self.m @ Affine2D().rotate(a).get_matrix()

    def scale(self, sx, sy=None):
        self.m = self.m @ Affine2D().scale(sx, sx if sy is None else sy).get_matrix()

    # -- path building
    def new(self):
        self.v, self.c = [], []
        return self

    def move_to(self, x, y):
        self.v.append((x, y)); self.c.append(1)
        return self

    def line_to(self, x, y):
        self.v.append((x, y)); self.c.append(2)
        return self

    def curve_to(self, x1, y1, x2, y2, x3, y3):
        self.v += [(x1, y1), (x2, y2), (x3, y3)]
        self.c += [4, 4, 4]
        return self

    def close(self):
        self.v.append(self.v[-1]); self.c.append(79)
        return self

    def poly(self, pts, closed=True):
        self.move_to(*pts[0])
        for p in pts[1:]:
            self.line_to(*p)
        if closed:
            self.close()
        return self

    def rect(self, x, y, w, h):
        return self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)])

    def rrect(self, x, y, w, h, r):
        r = min(r, w / 2, h / 2)
        k = r * (1 - K)
        self.move_to(x + r, y)
        self.line_to(x + w - r, y)
        self.curve_to(x + w - k, y, x + w, y + k, x + w, y + r)
        self.line_to(x + w, y + h - r)
        self.curve_to(x + w, y + h - k, x + w - k, y + h, x + w - r, y + h)
        self.line_to(x + r, y + h)
        self.curve_to(x + k, y + h, x, y + h - k, x, y + h - r)
        self.line_to(x, y + r)
        self.curve_to(x, y + k, x + k, y, x + r, y)
        return self.close()

    def ellipse(self, cx, cy, rx, ry=None):
        ry = rx if ry is None else ry
        kx, ky = rx * K, ry * K
        self.move_to(cx + rx, cy)
        self.curve_to(cx + rx, cy + ky, cx + kx, cy + ry, cx, cy + ry)
        self.curve_to(cx - kx, cy + ry, cx - rx, cy + ky, cx - rx, cy)
        self.curve_to(cx - rx, cy - ky, cx - kx, cy - ry, cx, cy - ry)
        self.curve_to(cx + kx, cy - ry, cx + rx, cy - ky, cx + rx, cy)
        return self.close()

    def arc(self, cx, cy, rx, ry, a0, a1, n=24, move=True):
        """Open elliptical arc as a polyline (angles in radians, y down)."""
        for i in range(n + 1):
            a = a0 + (a1 - a0) * i / n
            p = (cx + math.cos(a) * rx, cy + math.sin(a) * ry)
            if i == 0 and move:
                self.move_to(*p)
            else:
                self.line_to(*p)
        return self

    def smooth(self, pts, closed=True):
        """Catmull-Rom spline through pts."""
        n = len(pts)
        if n < 3:
            return self.poly(pts, closed)
        self.move_to(*pts[0])
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            if closed:
                p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            else:
                p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n - 1)]
            self.curve_to(p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6,
                          p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6,
                          p2[0], p2[1])
        if closed:
            self.close()
        return self

    # -- painting
    def _path(self):
        return Path(np.array(self.v, float), np.array(self.c, np.uint8))

    def _trans(self):
        return Affine2D(self.base @ self.m)

    def paint(self, fill=None, stroke=None, lw=0.022, keep=False, dash=None):
        if len(self.v) >= 2 and (fill is not None or stroke is not None):
            gc = self.gc
            gc.set_clip_path(self.clip)
            if stroke is not None:
                sc = math.sqrt(abs(self.m[0, 0] * self.m[1, 1] - self.m[0, 1] * self.m[1, 0]))
                gc.set_foreground(stroke, isRGBA=True)
                gc.set_linewidth(lw * self.ppu * sc)
                if dash:
                    gc.set_dashes(0, [d * self.ppu * sc for d in dash])
                else:
                    gc.set_dashes(0, None)
            else:
                gc.set_linewidth(0)
            self.r.draw_path(gc, self._path(), self._trans(), fill)
        if not keep:
            self.v, self.c = [], []
        return self

    def fill(self, col, keep=False):
        return self.paint(fill=col, keep=keep)

    def stroke(self, col, lw=0.022, keep=False, dash=None):
        return self.paint(stroke=col, lw=lw, keep=keep, dash=dash)

    def fs(self, fill, stroke=INK, lw=0.022, keep=False):
        return self.paint(fill=fill, stroke=stroke, lw=lw, keep=keep)

    def clip_here(self):
        """Use the current path as the clip region (replaces any previous clip)."""
        self.clip = TransformedPath(self._path(), self._trans())
        self.v, self.c = [], []

    def unclip(self):
        self.clip = None

    # -- output
    def rgba(self):
        return np.asarray(self.r.buffer_rgba())


# ------------------------------------------------------------ shape helpers
def blob(rng, cx, cy, rx, ry=None, n=10, jit=0.14):
    ry = rx if ry is None else ry
    off = rng.random() * math.tau
    pts = []
    for i in range(n):
        a = off + i * math.tau / n
        r = 1 + rng.uniform(-jit, jit)
        pts.append((cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r))
    return pts


def inside(poly_pts, pts):
    """Vectorised point-in-polygon; returns list of bools."""
    return Path(np.array(poly_pts, float)).contains_points(np.array(pts, float))


def spline_pts(pts, closed=True, sub=8):
    """Sample a Catmull-Rom spline into a dense polyline (for hit tests / walking along)."""
    n = len(pts)
    out = []
    rng = range(n) if closed else range(n - 1)
    for i in rng:
        if closed:
            p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        else:
            p0, p1, p2, p3 = pts[max(i - 1, 0)], pts[i], pts[i + 1], pts[min(i + 2, n - 1)]
        for k in range(sub):
            t = k / sub
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                       + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed:
        out.append(tuple(pts[-1]))
    return out


def walk(pts, step, closed=False):
    """Yield (x, y, angle) every `step` units along a polyline."""
    seq = list(pts) + ([pts[0]] if closed else [])
    carry = 0.0
    for (x0, y0), (x1, y1) in zip(seq, seq[1:]):
        seg = math.hypot(x1 - x0, y1 - y0)
        if seg < 1e-9:
            continue
        ang = math.atan2(y1 - y0, x1 - x0)
        d = carry
        while d < seg:
            t = d / seg
            yield (x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, ang)
            d += step
        carry = d - seg


def glow(ctx, cx, cy, rx, ry, col, a=0.5, steps=12, power=1.4):
    """Soft radial glow built from stacked translucent ellipses."""
    q = 1 - (1 - a) ** (1 / steps)
    for i in range(steps):
        t = 1 - i / steps
        t = t ** power
        ctx.ellipse(cx, cy, rx * t, ry * t).fill(al(col, q))


def shadow(ctx, cx, cy, rx, ry, a=0.22):
    ctx.ellipse(cx, cy, rx, ry).fill((0.08, 0.06, 0.16, a))


# ----------------------------------------------------------------- foliage
class Pal:
    def __init__(self, base, hi=None, lo=None, line=None):
        self.base = C(base) if isinstance(base, str) else base
        self.hi = C(hi) if isinstance(hi, str) else (hi or lt(self.base, 0.22))
        self.lo = C(lo) if isinstance(lo, str) else (lo or dk(self.base, 0.22))
        self.line = C(line) if isinstance(line, str) else (line or dk(self.base, 0.6))


def foliage(ctx, rng, circles, pal, lw=0.035, leaves=True, sort=True):
    """Bumpy cartoon leaf mass from overlapping circles [(x, y, r), ...]."""
    if sort:
        circles = sorted(circles, key=lambda c: c[1])
    for x, y, r in circles:                       # silhouette outline
        ctx.ellipse(x, y, r + lw, r + lw)
    ctx.fill(pal.line)
    for x, y, r in circles:
        ctx.ellipse(x, y, r, r).fill(pal.lo)
        ctx.ellipse(x - r * 0.07, y - r * 0.10, r * 0.90, r * 0.88).fill(pal.base)
        ctx.ellipse(x - r * 0.28, y - r * 0.33, r * 0.40, r * 0.32).fill(pal.hi)
        if leaves and r > 0.12:
            for _ in range(2 if r < 0.4 else 4):
                a = rng.uniform(0.2, 2.4)
                d = rng.uniform(0.25, 0.7) * r
                lx, ly = x + math.cos(a) * d, y + math.sin(a) * d
                s = min(0.11, r * 0.3)
                ctx.arc(lx, ly, s, s * 0.7, 0.2, 2.6, n=6)
            ctx.stroke(al(pal.line, 0.45), lw * 0.45)


def cluster(rng, cx, cy, rx, ry, n, r0, r1):
    """Random circles filling an ellipse - handy input for foliage()."""
    out = []
    for _ in range(n):
        a = rng.random() * math.tau
        d = math.sqrt(rng.random())
        out.append((cx + math.cos(a) * rx * d, cy + math.sin(a) * ry * d, rng.uniform(r0, r1)))
    return out


def flower(ctx, x, y, r, col, core=None, petals=5, rot=0.0, line=None):
    core = core or C('#ffd23f')
    for i in range(petals):
        a = rot + i * math.tau / petals
        ctx.ellipse(x + math.cos(a) * r * 0.55, y + math.sin(a) * r * 0.55, r * 0.5, r * 0.5)
    if line is not None:
        ctx.paint(fill=col, stroke=line, lw=0.012)
    else:
        ctx.fill(col)
    ctx.ellipse(x, y, r * 0.36, r * 0.36).fill(core)


def leaf(ctx, x, y, length, width, ang):
    """Pointed leaf path starting at (x, y) growing along ang."""
    c, s = math.cos(ang), math.sin(ang)
    tx, ty = x + c * length, y + s * length
    nx, ny = -s * width, c * width
    mx, my = x + c * length * 0.45, y + s * length * 0.45
    ctx.move_to(x, y)
    ctx.curve_to(mx + nx, my + ny, tx + nx * 0.3, ty + ny * 0.3, tx, ty)
    ctx.curve_to(tx - nx * 0.3, ty - ny * 0.3, mx - nx, my - ny, x, y)
    ctx.close()
    return ctx


def save_png(arr, path, rgb=False):
    from PIL import Image
    if rgb:
        Image.fromarray(np.ascontiguousarray(arr[:, :, :3]), 'RGB').save(path, optimize=False, compress_level=6)
    else:
        Image.fromarray(np.ascontiguousarray(arr), 'RGBA').save(path, compress_level=6)
