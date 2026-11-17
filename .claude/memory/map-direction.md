---
name: map-direction
description: "2026-11-16 design pivot: 15-min win, huge 160x120 map with indoor/outdoor zones (no objectives), new enemies over time, buffet stations, thrown food, pixel art 3/4; final state is in the project's .claude/ folder (CLAUDE.md, docs/, memory/, art/)"
metadata:
  node_type: memory
  type: project
  originSessionId: c80bc7a6-0616-4988-997e-c39a7469aff3
  modified: 2026-11-16T21:26:15.369Z
---

2026-11-16: after the prototype, the user doubted the wedding theme ("map too small, surviving a set time to win isn't fun"). I separated theme / map size / win structure and offered: (a) endless wedding (infinite tiled garden), (b) escape from the wedding (infinite world, zones by distance), (c) a huge bounded map ("wedding of 3,000 people in a field") with distinct zones and in-map objectives (e.g. reach the chuppah by 3:00, bring a gift). **User picked (c).** Theme stays a wedding.

Open design questions at that point: map size (crossing time), list of zones, objective types (mandatory/optional, rewards), win condition (timer + objectives?), how to build a map bigger than one texture (chunks / Tilemap), spawner must stay inside bounds and out of walls. Reminder I gave: map type alone won't make it fun — weapon/upgrade variety is what the genre's fun comes from. The existing venue art ([[venue-art-pipeline]], 80x64 units in chunks) would need to grow.

Follow-up same day: user does NOT want objectives — just a huge map and "survive as long as possible" (endless mode, no win by timer). Implications I raised: GameTimer counts up, end screen shows time survived + best (PlayerPrefs), difficulty must keep rising forever (spawner curve currently ends), soft reasons to move (zones with different enemies, buffet heal, pickups), check course rules for a required win condition.

Final decisions later the same day (supersede the endless idea): WIN after a set time, but longer than 10 minutes (length TBD); map stays big; distinct zones; new and harder enemy types arrive as time passes; small buffet stations appear around the map and heal; weapons are no longer "excuses" — the player THROWS FOOD / wedding items at enemies. Still open: exact game length, zone list, weapon list, enemy roster + timeline, course deadline/scope.

More decisions (2026-11-16): game length 15 minutes to start; deadline ≈ one month from 2026-11-16 (~mid-December 2026). Zones — outdoor (mostly open, connected without barriers): reception (player starts here), parking, buffet area (many stations), outdoor dance floor, chuppah area (chuppah, aisle, standing guests), lawn with chairs. Indoor (some separation but many entrances/exits): indoor dance floor with DJ booth, tables area, restrooms, kitchen. User asked me to suggest more zones. No zone-specific gameplay for now. Enemies: the GDD roster; spawn timing decided later.

Art direction (2026-11-16): user is considering switching to PIXEL ART with a 3/4 view (between top-down and side view, Stardew/Zelda-like). I made a style sample (reception + parking, 480x270 native, 16 px tiles, characters 12x20, warm palette, dark outlines) with a PIL script in the scratchpad `pixel/make_style_sample.py`. Waiting on feedback (character size, palette, detail). A switch would mean redoing the vector sprites and the venue pipeline art.

User likes the pixel style. Agreed approach: Tilemap for ground/walls (Ground, Ground Details, Walls layers; Rule Tiles from 2D Tilemap Extras), separate Y-sorted sprite prefabs for objects. User wants to settle the map plan BEFORE any tileset art. I proposed (scratchpad `pixel/make_map_plan.py` → map_plan.png): map 160x120 tiles (1 tile = 16 px = 1 unit, PPU 16; one screen ≈ 30x17 tiles at a 480x270 reference resolution); parking along the south, reception in the middle of the south (player start), indoor building in the west (lobby strip along its south, tables hall + indoor dance floor/DJ, back row WC/kitchen/bride room), outdoor in the east (outdoor dance floor next to the indoor one, buffet, lawn with chairs, chuppah in the far NE). Optional zones: smokers, photo corner, kids area, bar/lounge, bride room. Rule: openings 3–4 tiles wide and every room has 2+ exits. User revisions: bride room removed (back row = WC 22x28 + kitchen 42x28 only); no wall between tables and indoor dance floor (one MAIN HALL 64x30, tables west half, dance floor + DJ east half); kids area replaced — I put FOUNTAIN GARDEN there (alternatives offered: band stage, hookah/lounge corner, valet). Still awaiting confirmation of size and which optional zones stay.

2026-11-16 (end of day): user asked to move to another computer and to keep everything Claude-related in ONE folder. All of it now lives in `<project>/.claude/`: `CLAUDE.md` (auto-loaded), `docs/` (GDD.md v2, Progress_Summary.md, map_plan.png, style_sample.png), `memory/` (copies of these notes + old GDD v1 / old summary), `art/` (PixelArt, VectorSprites incl. Background.png, Venue). Those files are the source of truth. User does NOT use the Venue art from the forked session — only the art made in the main conversation.

**Why:** big direction change from the GDD's single-venue map; GDD needs updating once decided.
**How to apply:** continue the (c) design discussion; keep mentor mode ([[mentor-mode-no-edits]]); see [[prototype-progress]].
