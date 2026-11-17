# CLAUDE.md — "מתי אצלך?" (Mati Etzlecha)

Read this first in every new session. The user moved to a new computer on 2026-11-16; this file plus `.claude/docs/` carry the full context from the earlier conversations (the old machine's Claude memory is copied into `.claude/memory/` for reference).

**Everything Claude-related lives in this one `.claude/` folder (the user asked for that):** this file, `docs/`, `memory/`, `art/`. Keep new Claude files (docs, art generators, previews) inside `.claude/` too, not in the project root. Exception: finished sprites the user will use in Unity go under `Assets/` only when they ask.

## Who / what
- A game-dev course student building their **final project alone**: a Survivors-like comedy in **Unity 6000.3.26f1, 2D URP**. Deadline ≈ **mid-December 2026** (about one month from 2026-11-16). The course requires a Git repo link on Moodle, a short rules doc, and a live presentation.
- Premise: you're the only single guy at a huge Israeli wedding; aunts chase you ("When is it your turn?"); you **throw food / wedding items** at them; when they give up they drop **phone-number notes** that give XP; level-ups offer 1 of 3 upgrades; survive **15 minutes** to win.

## How to work with this user (MUST follow)
1. **Reply in Hebrew.** Code comments in English. When asked for comments, only on what was asked.
2. **Do not change or write anything in the project folder unless the user explicitly asks.** Reading files to check their work is always fine ("תבדוק אותי" / "תסתכל" = read the scripts, scene and prefabs, and review).
3. **Mentor mode for gameplay code:** guide with hints, questions and direction. Don't hand over the solution. **Exception:** when the user says "תגיד לי" / "תגיד לי מה הפתרון" / "תכתוב לי", give the direct answer or code (in chat; they paste it themselves unless they ask you to write the file).
4. **Exception for ART:** the user wants Claude as a "professional sprite maker". Produce the art files directly (Python + PIL). The user places them in the scene. Art generators live in `.claude/art/`.
5. **Git:** deferred ("Git at the end") unless the user asks. Note: on the old machine git complained about "dubious ownership"; it may need `git config --global --add safe.directory <path>` (ask first).
6. "תרשום לנו" = save it for later and raise it at the right time (keep `.claude/docs/Progress_Summary.md` → "דברים שביקשתי לזכור" up to date when asked).
7. Plans change; the user reports progress and says when to switch topics. Keep `.claude/docs/Progress_Summary.md` and `.claude/docs/GDD.md` current when decisions change (only when asked to update docs).

## Where things are
- `.claude/docs/GDD.md` — game design doc **v2** (new direction). Sections 5 (map) and 7 (art) are the current focus.
- `.claude/docs/Progress_Summary.md` — what is built (every script, how it works), decisions, things to remember, next steps.
- `.claude/docs/map_plan.png` — the agreed map plan (160×120 tiles). Source: `.claude/art/PixelArt/make_map_plan.py`.
- `.claude/docs/style_sample.png` — the pixel-art style the user liked (reception + parking). Source: `.claude/art/PixelArt/make_style_sample.py`.
- `.claude/memory/` — copies of the old machine's memory notes (background detail).
- `Assets/Scenes/Prototype.unity`, `Assets/Scripts/` — the finished prototype.
- `.claude/art/VectorSprites/` — older vector-style sprite generators + `Background.png` (superseded by pixel art).
- `.claude/art/Venue/` — an older procedural vector venue map pipeline (made in a forked session; outputs in `Assets/Sprites/Venue/`). **The user does not use it** — only the art made in the main conversation matters. Kept for reference only.

## Current status (2026-11-16)
- **Prototype: DONE** (movement/camera, aunt chase, pooled spawner, first auto-weapon, notes + XP + 3-card upgrades, patience + contact damage + loss, 5-min clock + win, shared end screen, floating text). All tested by the user.
- **New direction decided** (see GDD v2): 15-minute win; huge bounded map with indoor/outdoor zones and **no objectives**; new harder enemies over time; small buffet stations that appear and heal; weapons = thrown food; **pixel art, 3/4 view**, PPU 16, 16×16 tiles, Tilemap for ground/walls (+ Rule Tiles), separate Y-sorted prefabs for objects.
- **Map plan (agreed so far):** 160×120 tiles. South: parking (100×22) + reception (48×22, player start). West building: lobby strip (64×8), MAIN HALL 64×30 (tables west half + dance floor/DJ east half, **no wall between**), back row WC (22×28) + kitchen (42×28). East outdoor: outdoor dance floor (32×28, joined to the indoor one), buffet area (30×30), lawn with chairs (46×34), chuppah area (38×32, far NE). Optional: smokers, photo corner, fountain garden (replaced kids area), bar/lounge. Doors ≥3–4 tiles, every room 2+ exits.
- **Waiting on the user:** confirm map size and which optional zones stay. Then: first pixel-art tileset (grass, pavers, asphalt, sidewalk/curb, parking lines) + reception/parking props, and teach Tilemap. Code-wise, production starts with the refactor in GDD §10 (WeaponBase/WeaponData, PlayerStats, EnemyData, WaveDirector) before adding content.

## Technical facts worth knowing
- Uses `rb.linearVelocity` (not `velocity`). New Input System (`Keyboard.current`), WASD only, no Dash.
- All sprites face LEFT; flip only with `SpriteRenderer.flipX` (`facingRight` starts false).
- Y-sorting: `Assets/Settings/Renderer2D.asset` Transparency Sort Mode = Custom Axis (0,1,0); sprites need a feet pivot and Sprite Sort Point = Pivot, same Order in Layer.
- Object pooling with `UnityEngine.Pool.ObjectPool<T>`: creator holds the pool and passes it once (SetPool) in the create callback; reset in `OnEnable`; null-check in the destroy callback (Unity 6 clears pools after scene objects are destroyed).
- UI listens to UnityEvents (`OnXPChanged(float)`, `OnLevelUp`, `onPatienceChanged(float)`, `onDeath`, `OnSecondsLeftChanged(int)`, `OnTimeUp`). Renaming a serialized field/event loses its Inspector value/wiring.
- Layers: Player 6, Enemy 7, Pickup 8 (collides only with Player). Player Mass 100; enemies use Discrete collision for performance.
- Floating text is English for now (TMP default font has no Hebrew; needs a Hebrew font + RTL, e.g. RTLTMPro).
- Python art scripts need `pip install pillow`; run as `python <script>.py <output_dir>`.
