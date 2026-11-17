---
name: venue-art-pipeline
description: "How the venue (gan eruim) background art for Mati Etzlecha is generated: procedural Python generator in .claude/art/Venue, output in Assets/Sprites/Venue, style + scale decisions"
metadata:
  type: project
---

Art phase started 2026-11-16. The venue map is drawn procedurally (no image model): Python + matplotlib Agg renderer (pip install of pycairo was blocked, matplotlib/PIL/numpy/opencv are installed). Generator lives in `<project>/.claude/art/Venue/` (lib.py canvas, ground.py outdoor, hall.py hall+walls, props.py, layout.py prop positions, export.py, build.py). Re-export: `python build.py all <Assets/Sprites/Venue> <.claude/art/Venue>`; quick look: `python build.py preview <ppu> x0 y0 w h out.png props`.

Output: `Assets/Sprites/Venue/Ground/Ground_r{1-4}_c{1-5}.png` (20 chunks, 2048px, 128 PPU = 16 units each, map 80x64 units centred on 0,0) and `Assets/Sprites/Venue/Props/*.png` (20 Y-sorted props, pivot at base). export.py also writes the .meta files (PPU 128, bilinear, custom pivot) and keeps existing GUIDs on re-export. Docs/previews: `.claude/art/Venue/placement.md`, `prop_positions.csv`, `preview_with_props.png`.

Decisions: 3/4 oblique view (ground circles foreshortened x0.62, vertical things full height); clean cartoon vector with dark outlines to match player/Doda/table sprites (those are 256 PPU, ~1 unit tall); late-afternoon palette with warm lamp glows; hall is a cut-away (tall back wall, low side walls, open pillar front). User asked NOT to include big items (tables, chairs, benches, chuppah, food stations, people) - they will request those separately and place them themselves.

**Why:** user wants to feel how the final game will look; they keep continuing in fresh conversations.
**How to apply:** for new art requests reuse lib.py helpers and the same palette/outline weights/128 PPU so everything matches; tweak layout.py + re-run export rather than hand-editing PNGs. Related: [[mentor-mode-no-edits]], [[prototype-progress]].

**Update 2026-11-16:** the user said they do not use this Venue art (it was made in a forked session); the source moved to `<project>/.claude/art/Venue/`. Pixel art 3/4 replaced the vector style — see [[map-direction]].
