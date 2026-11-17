# CLAUDE.md — "מתי אצלך?" (Mati Etzlecha)

Read this first in every new session. The user moves between computers (2026-11-16, and again after 2026-11-17); this file plus `.claude/docs/` carry the full context from the earlier conversations (Claude memory notes from previous machines are copied into `.claude/memory/` for reference). The project travels via Git; `.claude/` is tracked.

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
- `.claude/docs/GDD.md` — game design doc **v2.2** (huge finite map, no building). Sections 5 (map), 7 (art) and 10 (architecture) are the current focus.
- `.claude/docs/Progress_Summary.md` — what is built (every script, how it works), decisions, things to remember, next steps.
- `.claude/docs/Balance.md` — starting balance numbers (2026-11-17, not yet playtested): XP formula `10 × level`, 3 main weapons per level, passives (incl. suggested "מנה שנייה" +10% damage), enemies + HP ×(1 + 0.1 × minute), 15-min spawn timeline (max 250 alive), buffet and gift drops, tuning guide.
- `.claude/docs/map_plan.png` — the OLD closed-map plan (160×120 tiles), superseded on 2026-11-17. Reference only. Source: `.claude/art/PixelArt/make_map_plan.py`.
- `.claude/docs/style_sample.png` — the pixel-art style the user liked (reception + parking). Source: `.claude/art/PixelArt/make_style_sample.py`.
- `.claude/memory/` — copies of earlier machines' memory notes (background detail). `map-decision-2026-11-17.md` = how the map decision was reached.
- `Assets/Scenes/Prototype.unity`, `Assets/Scripts/` — the finished prototype.
- `.claude/art/PixelArt/` — current pixel-art generators: `make_characters.py` → `characters/` (Player + Aunt pink/blue/purple/yellow sheets, 16×24, 4 frames: idle, walk1, walk2, hit/give-up, facing left); `make_buffet.py` → `buffet_native.png` / `buffet_x4.png` (buffet island style preview, approved); `make_style_sample.py`; `make_map_plan.py` (old).
- `Assets/Sprites/Player_sheet.png`, `Assets/Sprites/Aunt_yellow_sheet.png` — the pixel sprites already in use (player in the scene, aunt in `Doda.prefab`).
- `.claude/art/VectorSprites/` — older vector-style sprite generators + `Background.png` (superseded by pixel art).
- `.claude/art/Venue/` — an older procedural vector venue map pipeline (made in a forked session; outputs in `Assets/Sprites/Venue/`). **The user does not use it** — only the art made in the main conversation matters. Kept for reference only.

## Current status (2026-11-17)
- **Prototype: DONE** (movement/camera, aunt chase, pooled spawner, first auto-weapon, notes + XP + 3-card upgrades, patience + contact damage + loss, 5-min clock + win, shared end screen, floating text). All tested by the user.
- **Direction** (see GDD v2.2): 15-minute win; **no objectives**; new harder enemies over time; buffet stations that heal; weapons = thrown food; **pixel art, 3/4 view**, PPU 16, 16×16 tiles, separate Y-sorted prefabs for objects.
- **2026-11-17: HUGE FINITE MAP, NO BUILDING** ("the biggest wedding in the world"), ~200×200 units with a hedge/fence border, start entrance in the middle. Same day it went closed 160×120 map with building → infinite world with prop recycling → this hybrid (final). Layers: grass ground → decorations (no collision) → sparse obstacles (tables, pots) → **islands** (dance floor + DJ, chuppah far away, 3–4 buffet islands with healing stations, photo corner, bar, parking) → breakable **gifts** that drop pickups (cake heal, magnet, fireworks clear, money XP). **Islands placed by hand; decorations/obstacles/gifts scattered randomly ONCE at start** (overlap check), nothing moves after. Needs: `MapBounds`, spawner rejects out-of-bounds points, gifts respawn, buffet refills, far enemies (>25 units) return to pool, camera clamps at edges. Check performance (~1,500 decorations, ~400 obstacles; Tilemap for decorations if heavy). Estimate 2–3 days.
- **Character size decided 2026-11-17: 16×24 base frame** (1×1.5 units; cousin smaller ~12×18, grandma short/wide, mom boss ~20×30; props scaled to match — see GDD §7).
- **Done 2026-11-17 (end of day), user-tested:** player + yellow aunt pixel sheets imported (PPU 16, Point, no compression, Multiple, Grid 16×24, pivot Bottom) and used (first frame only, **no Animator yet**); colliders resized (player capsule 0.43×0.71, aunt 0.45×0.5); **Pixel Perfect Camera** on Main Camera (Assets PPU 16, Ref 480×270, Crop None, Grid Snapping None; scene file still says ortho 5.6, overridden at runtime). Starting balance table done: `.claude/docs/Balance.md`.
- **Next (recommended order):** (1) user: editor-only debug keys F1/F2/F3; (2) user, mentor mode: refactor PlayerStats → WeaponData+WeaponBase (ShiftExcuse → meatballs) → EnemyData → WaveDirector, plus XP formula `10 × level`; (3) Claude in parallel: grass tile variants, decorations, round table + chairs at 16×24 scale, then help with Animator; (4) map system in week 2. Old PPU-256 table/chairs look small next to the new characters — expected until replaced.

## Technical facts worth knowing
- Uses `rb.linearVelocity` (not `velocity`). New Input System (`Keyboard.current`), WASD only, no Dash.
- All sprites face LEFT; flip only with `SpriteRenderer.flipX` (`facingRight` starts false).
- Y-sorting: `Assets/Settings/Renderer2D.asset` Transparency Sort Mode = Custom Axis (0,1,0); sprites need a feet pivot and Sprite Sort Point = Pivot, same Order in Layer.
- Object pooling with `UnityEngine.Pool.ObjectPool<T>`: creator holds the pool and passes it once (SetPool) in the create callback; reset in `OnEnable`; null-check in the destroy callback (Unity 6 clears pools after scene objects are destroyed).
- UI listens to UnityEvents (`OnXPChanged(float)`, `OnLevelUp`, `onPatienceChanged(float)`, `onDeath`, `OnSecondsLeftChanged(int)`, `OnTimeUp`). Renaming a serialized field/event loses its Inspector value/wiring.
- Layers: Player 6, Enemy 7, Pickup 8 (collides only with Player). Player Mass 100; enemies use Discrete collision for performance.
- Camera: URP **Pixel Perfect Camera** (PPU 16, reference 480×270 → ortho size 8.4375 computed by the component; don't set it by hand). Game view 1920×1080 = ×4.
- Sprite import for pixel art: PPU 16, Filter Point, Compression None, pivot at the feet (Bottom).
- Floating text is English for now (TMP default font has no Hebrew; needs a Hebrew font + RTL, e.g. RTLTMPro).
- Python art scripts need `pip install pillow`; run as `python <script>.py <output_dir>`.
