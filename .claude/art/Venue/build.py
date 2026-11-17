"""Build script for the venue art.

  python build.py preview <ppu> <x0> <y0> <w> <h> <out.png> [props]   quick look at a region
  python build.py all <assets_dir> <preview_dir>                      final export
"""
import os
import sys
import time

import numpy as np
from PIL import Image

import layout as L
from lib import *


def render_ground(ppu, region=None):
    import ground
    import hall
    x0, y0, w, h = region or (0, 0, L.W, L.H)
    ctx = Ctx(w, h, ppu, x0, y0)
    ctx.rect(0, 0, L.W, L.H).fill(C('#2f5a3a'))
    ground.draw_outdoor(ctx)
    hall.draw_hall(ctx)
    hall.draw_walls(ctx)
    hall.draw_light(ctx)
    return ctx


def composite_props(img, ppu, region):
    """Paste the prop sprites (rendered at `ppu`) onto a PIL image of `region`, sorted by y."""
    import props
    x0, y0, w, h = region
    cache = {}
    for name, x, y, _ in sorted(L.PROPS, key=lambda p: p[2]):
        if name not in cache:
            cache[name] = props.render(name, ppu)
        spr, (px, py) = cache[name]
        img.alpha_composite(spr, (int(round((x - x0) * ppu - px)), int(round((y - y0) * ppu - py)))) \
            if -spr.width < (x - x0) * ppu - px < img.width and -spr.height < (y - y0) * ppu - py < img.height else None
    return img


def safe_paste(img, spr, pos):
    x, y = pos
    sx0, sy0 = max(0, -x), max(0, -y)
    sx1, sy1 = min(spr.width, img.width - x), min(spr.height, img.height - y)
    if sx1 <= sx0 or sy1 <= sy0:
        return
    img.alpha_composite(spr.crop((sx0, sy0, sx1, sy1)), (x + sx0, y + sy0))


def composite(img, ppu, region):
    import props
    x0, y0, w, h = region
    cache = {}
    for name, x, y, _ in sorted(L.PROPS, key=lambda p: p[2]):
        if name not in cache:
            cache[name] = props.render(name, ppu)
        spr, (px, py) = cache[name]
        safe_paste(img, spr, (int(round((x - x0) * ppu - px)), int(round((y - y0) * ppu - py))))
    return img


def main():
    mode = sys.argv[1]
    t = time.time()
    if mode == 'preview':
        ppu = float(sys.argv[2])
        region = tuple(float(v) for v in sys.argv[3:7])
        out = sys.argv[7]
        ctx = render_ground(ppu, region)
        img = Image.fromarray(ctx.rgba().copy(), 'RGBA')
        if len(sys.argv) > 8:
            composite(img, ppu, region)
        img.convert('RGB').save(out)
    elif mode == 'props':
        import props
        ppu = float(sys.argv[2])
        out = sys.argv[3]
        names = sys.argv[4:] or props.NAMES
        sprs = [props.render(n, ppu)[0] for n in names]
        wsum = sum(s.width for s in sprs) + 10 * (len(sprs) + 1)
        hmax = max(s.height for s in sprs) + 20
        sheet = Image.new('RGBA', (wsum, hmax), (134, 186, 92, 255))
        x = 10
        for s in sprs:
            sheet.alpha_composite(s, (x, hmax - 10 - s.height))
            x += s.width + 10
        sheet.convert('RGB').save(out)
    elif mode == 'all':
        import export
        export.run(sys.argv[2], sys.argv[3])
    print('done in %.1fs' % (time.time() - t))


if __name__ == '__main__':
    main()
