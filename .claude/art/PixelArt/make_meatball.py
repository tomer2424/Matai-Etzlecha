import os
import sys
from PIL import Image

# Meatball projectile, same pixel-art style as make_characters.py (PPU 16, dark outline, light from top-left).
# Three sizes so the user can pick (frame size in px, outline included): 8, 7, 6.
# Outputs per size N:
#   Meatball_N.png        NxN single sprite (first frame)
#   Meatball_N_sheet.png  4 spin frames side by side (texture rotates, the shine stays top-left)
#   meatball_preview.png  x8 preview: all sizes next to the player at true scale
# Usage: python make_meatball.py <output_dir>
OUT = sys.argv[1] if len(sys.argv) > 1 else "."
os.makedirs(OUT, exist_ok=True)

OUTL = (38, 26, 34)
MEAT_D = (104, 50, 30)     # shadow side (bottom-right)
MEAT = (146, 76, 42)       # base
MEAT_L = (178, 104, 60)    # lit side (top-left)
SHINE = (232, 176, 124)    # sauce gloss
SAUCE = (188, 56, 44)      # tomato sauce spot
SAUCE_L = (226, 92, 70)
HERB = (96, 150, 62)       # parsley fleck
CRUMB = (122, 62, 34)      # darker crumbs for texture
PAL = {"D": MEAT_D, "M": MEAT, "L": MEAT_L, "S": SHINE}

# Ball bodies, 1 px border left empty for the outline. Letters: D = shadow, M = base, L = lit, S = shine
# Specks: (x, y, color) in frame 0, rotated 90 degrees per spin frame.
SIZES = {
    8: (
        [
            "........",
            "..LLMM..",
            ".LSLMMM.",
            ".LLMMMD.",
            ".MMMMDD.",
            ".MMMDDD.",
            "..MDDD..",
            "........",
        ],
        [(5, 3, SAUCE), (5, 2, SAUCE_L), (3, 5, HERB), (2, 4, CRUMB), (4, 2, CRUMB)],
    ),
    7: (
        [
            ".......",
            "..LLM..",
            ".LSLMM.",
            ".LLMMD.",
            ".MMMDD.",
            "..MDD..",
            ".......",
        ],
        [(4, 2, SAUCE), (4, 3, SAUCE_L), (2, 4, HERB), (3, 3, CRUMB)],
    ),
    6: (
        [
            "......",
            ".LLMM.",
            ".LSMD.",
            ".LMMD.",
            ".MMDD.",
            "......",
        ],
        [(4, 2, SAUCE), (2, 4, HERB)],
    ),
}


def rotate(x, y, turns, n):
    """Rotate pixel (x, y) by 90 degrees clockwise `turns` times around the center of an n x n frame."""
    for _ in range(turns):
        x, y = n - 1 - y, x
    return x, y


def frame(n, turn):
    body, specks = SIZES[n]
    im = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    filled = set()
    for y, row in enumerate(body):
        for x, ch in enumerate(row):
            if ch != ".":
                im.putpixel((x, y), PAL[ch] + (255,))
                filled.add((x, y))
    for (x, y, c) in specks:
        rx, ry = rotate(x, y, turn, n)
        # keep the shine readable: specks never cover it
        if (rx, ry) in filled and body[ry][rx] != "S":
            im.putpixel((rx, ry), c + (255,))
    # automatic outline, same rule as the characters (4 directions)
    for (x, y) in list(filled):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in filled:
                im.putpixel((nx, ny), OUTL + (255,))
    return im


all_frames = {}
for n in SIZES:
    frames = [frame(n, t) for t in range(4)]
    all_frames[n] = frames
    frames[0].save(os.path.join(OUT, f"Meatball_{n}.png"))
    sheet = Image.new("RGBA", (n * 4, n), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * n, 0))
    sheet.save(os.path.join(OUT, f"Meatball_{n}_sheet.png"))

# Preview at x8: for each size, a meatball at hand height next to the player (true scale)
SCALE = 8
HERE = os.path.dirname(os.path.abspath(__file__))
player_path = os.path.join(HERE, "characters", "Player_sheet.png")
if not os.path.exists(player_path):
    # the player sheet lives in the Unity project
    player_path = os.path.join(HERE, "..", "..", "..", "Assets", "Sprites", "Player_sheet.png")
player = Image.open(player_path).convert("RGBA").crop((0, 0, 16, 24)) if os.path.exists(player_path) else None

bg = (120, 168, 88, 255)  # grass-ish background so the outline reads like in the game
prev = Image.new("RGBA", (30 * len(SIZES) + 2, 30), bg)
for i, n in enumerate(SIZES):
    x0 = 2 + i * 30
    if player:
        prev.alpha_composite(player, (x0 + 12, 3))
    # centered on the same point for every size, about hand height
    prev.alpha_composite(all_frames[n][0], (x0 + 5 - n // 2, 17 - n // 2))
prev = prev.resize((prev.width * SCALE, prev.height * SCALE), Image.NEAREST)
prev.save(os.path.join(OUT, "meatball_preview.png"))
print("saved to", OUT)
