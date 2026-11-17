"""Final export: ground chunks + prop sprites (+ Unity .meta files) + preview + placement table."""
import os
import uuid

import numpy as np
from PIL import Image

import layout as L
import props
from build import render_ground, safe_paste

META = """fileFormatVersion: 2
guid: {guid}
TextureImporter:
  internalIDToNameTable: []
  externalObjects: {{}}
  serializedVersion: 13
  mipmaps:
    mipMapMode: 0
    enableMipMap: 0
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
    flipGreenChannel: 0
  isReadable: 0
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  vTOnly: 0
  ignoreMipmapLimit: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: 2048
  textureSettings:
    serializedVersion: 2
    filterMode: 1
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  lightmap: 0
  compressionQuality: 50
  spriteMode: 1
  spriteExtrude: 1
  spriteMeshType: {mesh}
  alignment: {align}
  spritePivot: {{x: {px}, y: {py}}}
  spritePixelsToUnits: {ppu}
  spriteBorder: {{x: 0, y: 0, z: 0, w: 0}}
  spriteGenerateFallbackPhysicsShape: 1
  alphaUsage: 1
  alphaIsTransparency: {alpha}
  spriteTessellationDetail: -1
  textureType: 8
  textureShape: 1
  singleChannelComponent: 0
  flipbookRows: 1
  flipbookColumns: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  ignorePngGamma: 0
  applyGammaDecoding: 0
  swizzle: 50462976
  cookieLightType: 0
  platformSettings:
  - serializedVersion: 4
    buildTarget: DefaultTexturePlatform
    maxTextureSize: 2048
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  - serializedVersion: 4
    buildTarget: Standalone
    maxTextureSize: 2048
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  spriteSheet:
    serializedVersion: 2
    sprites: []
    outline: []
    customData:
    physicsShape: []
    bones: []
    spriteID: 5e97eb03825dee720800000000000000
    internalID: 0
    vertices: []
    indices:
    edges: []
    weights: []
    secondaryTextures: []
    spriteCustomMetadata:
      entries: []
    nameFileIdTable: {{}}
  mipmapLimitGroupName:
  pSDRemoveMatte: 0
  userData:
  assetBundleName:
  assetBundleVariant:
"""


def write_meta(png_path, pivot=None, opaque=False):
    meta_path = png_path + '.meta'
    guid = None
    if os.path.exists(meta_path):                       # keep the GUID so scene references survive re-exports
        for line in open(meta_path, encoding='utf-8'):
            if line.startswith('guid:'):
                guid = line.split(':')[1].strip()
    guid = guid or uuid.uuid4().hex
    px, py = pivot if pivot else (0.5, 0.5)
    txt = META.format(guid=guid, mesh=0 if opaque else 1, align=9 if pivot else 0, px=round(px, 5), py=round(py, 5),
                      ppu=L.PPU, alpha=0 if opaque else 1)
    with open(meta_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(txt)


def run(assets_dir, doc_dir):
    gdir = os.path.join(assets_dir, 'Ground')
    pdir = os.path.join(assets_dir, 'Props')
    os.makedirs(gdir, exist_ok=True)
    os.makedirs(pdir, exist_ok=True)
    ppu = L.PPU
    # ---------------- ground
    ctx = render_ground(ppu)
    arr = ctx.rgba()
    cpx = L.CHUNK * ppu
    rows, cols = L.H // L.CHUNK, L.W // L.CHUNK
    lines = ['# Venue placement (Unity world units, map centred on 0,0)', '',
             '## Ground chunks (pivot = Center, Sorting Layer = Background)', '',
             '| Sprite | X | Y |', '|---|---|---|']
    for r in range(rows):
        for c in range(cols):
            name = 'Ground_r%d_c%d' % (r + 1, c + 1)
            path = os.path.join(gdir, name + '.png')
            Image.fromarray(np.ascontiguousarray(arr[r * cpx:(r + 1) * cpx, c * cpx:(c + 1) * cpx, :3]), 'RGB').save(path)
            write_meta(path, opaque=True)
            lines.append('| %s | %g | %g |' % (name, (c + 0.5) * L.CHUNK - L.W / 2, L.H / 2 - (r + 0.5) * L.CHUNK))
    # small preview of the bare ground + props
    pv_ppu = 24
    small = Image.fromarray(arr.copy(), 'RGBA').resize((L.W * pv_ppu, L.H * pv_ppu), Image.LANCZOS)
    del arr, ctx
    # ---------------- props
    lines += ['', '## Props (pivot = base of the object, already set in the import settings)', '',
              '| Sprite | Size (units) | Count |', '|---|---|---|']
    counts = {}
    for name, x, y, _ in L.PROPS:
        counts[name] = counts.get(name, 0) + 1
    for name in props.NAMES:
        img, (px, py) = props.render(name, ppu)
        path = os.path.join(pdir, name + '.png')
        img.save(path)
        write_meta(path, pivot=(px / img.width, 1 - py / img.height))
        lines.append('| %s | %.1f x %.1f | %d |' % (name, img.width / ppu, img.height / ppu, counts.get(name, 0)))
    lines += ['', '## Suggested prop positions', '', '| Sprite | X | Y |', '|---|---|---|']
    for name, x, y, _ in sorted(L.PROPS, key=lambda p: (p[0], p[2], p[1])):
        ux, uy = L.unity_xy(x, y)
        lines.append('| %s | %g | %g |' % (name, ux, uy))
    with open(os.path.join(doc_dir, 'placement.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    with open(os.path.join(doc_dir, 'prop_positions.csv'), 'w', encoding='utf-8') as f:
        f.write('sprite,x,y\n')
        for name, x, y, _ in L.PROPS:
            ux, uy = L.unity_xy(x, y)
            f.write('%s,%g,%g\n' % (name, ux, uy))
    small.convert('RGB').save(os.path.join(doc_dir, 'preview_ground_only.png'))
    cache = {}
    for name, x, y, _ in sorted(L.PROPS, key=lambda p: p[2]):
        if name not in cache:
            cache[name] = props.render(name, pv_ppu)
        spr, (px, py) = cache[name]
        safe_paste(small, spr, (int(round(x * pv_ppu - px)), int(round(y * pv_ppu - py))))
    small.convert('RGB').save(os.path.join(doc_dir, 'preview_with_props.png'))
