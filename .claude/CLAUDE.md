# CLAUDE.md — Chef vs Junk Food (formerly "מתי אצלך?" / Mati Etzlecha)

Read this first in every new session. The user moves between computers; this file plus `.claude/docs/` carry the full context from earlier conversations (Claude memory notes from previous machines are copied into `.claude/memory/` for reference). The project travels via Git; `.claude/` is tracked. The repo/folder is still called "Matai Etzlecha".

**Everything Claude-related lives in this one `.claude/` folder (the user asked for that):** this file, `docs/`, `memory/`, `art/`. Keep new Claude files (docs, art generators, previews) inside `.claude/` too, not in the project root. Exception: finished sprites the user will use in Unity go under `Assets/Sprites/Restaurant/` only when they ask.

## Who / what
- A game-dev course student building their **final project alone**: a Survivors-like comedy in **Unity 6000.3.26f1, 2D URP**. Deadline ≈ **mid-December 2026**. The course requires a Git repo link on Moodle, a short rules doc, and a live presentation.
- **Theme (changed 2026-11-23):** you are a **chef** in the biggest restaurant in the world; **junk food came alive** and chases you. You **throw kitchen tools** at it (first weapon: knife); when food gives up it drops **coins (tips)** that give XP; level-ups offer 1 of 3 upgrades; survive **15 minutes** to win. The basic enemy is a **pizza** (3 toppings). Game title not chosen yet. Before that the theme was a single guy at a wedding chased by aunts ("Doda"); code system names from that era stay (`EnemyInsistence`, `PlayerPatience`, `NoteBehaviour`, `NotesSpawner`).

## How to work with this user (MUST follow)
1. **Reply in Hebrew.** Code comments in English. When asked for comments, only on what was asked.
2. **Do not change or write anything in the project folder unless the user explicitly asks.** Reading files to check their work is always fine ("תבדוק אותי" / "תסתכל" = read the scripts, scene and prefabs, and review).
3. **Mentor mode for gameplay code:** guide with hints, questions and direction. Don't hand over the solution. **Exception:** when the user says "תגיד לי" / "תגיד לי מה הפתרון" / "תכתוב לי", give the direct answer or code (in chat; they paste it themselves unless they ask you to write the file).
4. **Small steps.** The user gets confused when too much comes at once. Explain new concepts from zero with a simple example or analogy (e.g. ScriptableObject = recipe card, Awake vs OnEnable = an actress's first day vs every time she goes on stage).
5. **Exception for ART:** the user wants Claude as a "professional sprite maker". Produce the art files directly (Python + PIL). The user places them in the scene. Art generators live in `.claude/art/`.
6. **Git:** the user commits and pushes themselves; Claude suggests a commit title + short description. Read-only git commands may need `git -c safe.directory=* ...` (dubious ownership on this machine).
7. "תרשום לנו" = save it for later and raise it at the right time (keep `.claude/docs/Progress_Summary.md` → "דברים שביקשתי לזכור" up to date).
8. Keep `.claude/docs/Progress_Summary.md`, `GDD.md` and `Balance.md` current **only when the user asks** to update docs.

## Where things are
- `.claude/docs/GDD.md` — game design doc **v3.0** (restaurant theme, huge open map, no inner walls). Enemy/weapon/passive names other than pizza/knife/coin are proposals; each lists the old wedding name.
- `.claude/docs/Progress_Summary.md` — what is built (every script, how it works), decisions, things to remember, next steps.
- `.claude/docs/Balance.md` — starting balance numbers (not yet playtested); names updated to the restaurant theme, numbers unchanged.
- `.claude/docs/map_plan.png`, `style_sample.png` — old wedding-era references only.
- `.claude/memory/` — copies of earlier machines' memory notes (background detail, wedding era).
- `Assets/Scenes/Prototype.unity`; `Assets/Scripts/{Player,Enemies,Weapons,Pickups,Systems,UI,Debug}/`; `Assets/Data/` (`Knife.asset` = WeaponData, `Pizza.asset` = EnemyData); `Assets/Prefabs/` (`Pizza`, `KnifeProjectile`, `Coin`, `Floating Text`, `Table`).
- `.claude/art/PixelArt/make_restaurant.py` → `restaurant/`: `Chef_sheet.png`, `Pizza_{pepperoni,margherita,veggie}_sheet.png` (16×24, 4 frames: idle, walk1, walk2, hit/give-up, facing left; pizza tip UP, crust at the bottom), `Knife.png` (points RIGHT), `Coin.png`, `restaurant_sample_x4.png` (approved style sample: wood floor, checker kitchen, kitchen island, salad bar, checkered-cloth tables), `restaurant_characters_x8.png`. These six sprites are already in `Assets/Sprites/Restaurant/`.
- Old wedding-era generators (`make_characters.py`, `make_meatball.py`, `make_buffet.py`, `make_style_sample.py`, `make_map_plan.py`), `.claude/art/VectorSprites/`, `.claude/art/Venue/` — reference only, not used.

## Current status (2026-11-23)
- **Prototype: DONE** (2026-11-16).
- **Structure refactor: DONE** (18–23.11): debug keys F1/F2/F3; `PlayerStats` (base × multipliers); `WeaponBase` (abstract, `TryAttack`, levels) + `WeaponData`/`WeaponLevelUpgrade`; `KnifeWeapon` (N closest enemies); `EnemyData` (three enemy components each copy from it in `Awake`); note/coin XP from `EnemyData`; XP formula `xpRequiredPerLevel (10) × level`; `WaveDirector` + `SpawnWave` table (interval by time, insistence × (1 + 0.1 × whole minutes)); spawner cap 250; `RandomLook` (random pizza topping); projectiles rotate toward their flight direction.
- **Theme switch: DONE** for chef, pizza, knife, coin (sprites, prefab/data renames in Unity with GUIDs kept, names and comments in code). Old wedding sprites deleted from `Assets` (except `RoundTable.png` used by `Table.prefab` and `Bar background.png` used by the UI bars).
- **Next (recommended order):** (1) Animator for chef + pizza (course requirement; switch `RandomLook` to picking an `AnimatorOverrideController`); (2) second weapon: frying pan orbiting the player; (3) second enemy: burger → enemy types + percentages in `WaveDirector`, a pool per type; (4) full card system; (5) the map (floor, bounds, fixed islands incl. salad bars that heal, one-time random scatter, breakable crates); Claude makes art in parallel.
- Open questions: game title, whether the course needs approval for the theme change, story, Hebrew vs English text.

## Technical facts worth knowing
- Uses `rb.linearVelocity` (not `velocity`). New Input System (`Keyboard.current`), WASD only, no Dash.
- Characters face LEFT; flip only with `SpriteRenderer.flipX` (`facingRight` starts false). Rotating projectiles are drawn pointing RIGHT (0°).
- Y-sorting: `Assets/Settings/Renderer2D.asset` Transparency Sort Mode = Custom Axis (0,1,0); sprites need a feet pivot and Sprite Sort Point = Pivot, same Order in Layer.
- Object pooling with `UnityEngine.Pool.ObjectPool<T>`: creator holds the pool and passes it once (SetPool) in the create callback; reset in `OnEnable`; per-spawn setup (position, insistence multiplier, XP) happens from outside right after `Get()`; null-check in the destroy callback.
- Data from ScriptableObjects is copied in `Awake` and never modified at runtime. Balance numbers live in SOs or Inspector fields with a sensible default in code.
- A prefab can't reference scene objects; the spawner passes scene references/values via `Set...` methods.
- UI listens to UnityEvents (`OnXPChanged(float)`, `OnLevelUp`, `onPatienceChanged(float)`, `onDeath`, `OnSecondsLeftChanged(int)`, `OnTimeUp`). Renaming a serialized field/event loses its Inspector value/wiring. Rename scripts/prefabs/assets inside Unity (keeps the .meta GUID); after a class rename, re-pick UnityEvent targets.
- Layers: Player 6, Enemy 7, Pickup 8 (collides only with Player). Player Mass 100; enemies use Discrete collision for performance.
- Camera: URP **Pixel Perfect Camera** (PPU 16, reference 480×270 → ortho size computed by the component). Game view 1920×1080 = ×4.
- Sprite import for pixel art: PPU 16, Filter Point, Compression None; character sheets Multiple, Grid 16×24, pivot Bottom; single props/projectiles pivot Center.
- `GameTimer.gameDuration` is 900 in the scene (300 default in code). `WaveDirector` spawn intervals must be > 0.
- Floating text is English for now (TMP default font has no Hebrew; needs a Hebrew font + RTL, e.g. RTLTMPro).
- Python art scripts need `pip install pillow`; run as `python <script>.py <output_dir>`.
