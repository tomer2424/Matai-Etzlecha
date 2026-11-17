---
name: infinite-world-decision
description: 2026-11-17 map decision went closed 160x120 map → infinite world → FINAL huge finite ~200x200 map with no building (hand-placed islands + one-time random scatter); docs updated
metadata:
  node_type: memory
  type: project
  originSessionId: 35e047eb-a0ae-4645-8daf-0c75ddf18b98
  modified: 2026-11-17T16:26:19.935Z
---

2026-11-17, all in one day: the closed 160x120 map (building, walls) was dropped → an infinite world with prop "recycling" was chosen → a few hours later the user asked for a hybrid and that is FINAL: **a huge finite map (~200x200 units) with no building**, hedge/fence border, start entrance in the middle.

Content: grass ground; non-colliding decorations; sparse obstacles; **islands placed by hand** (dance floor + DJ, chuppah far away, 3–4 buffet islands, photo corner, bar, parking); decorations/obstacles/gifts **scattered randomly once at start** with overlap checks; breakable gifts respawn elsewhere; buffet refills; far enemies (>25 units) return to the pool; spawner rejects out-of-bounds points; camera clamps at edges. Watch performance (~1,500 decorations).

GDD (v2.2 §5), Progress_Summary, Balance.md and CLAUDE.md were updated to this on request.

**Why:** the building/walls were the biggest schedule risk; a consistent world is easier to learn and to show in the presentation, and one-time scatter is simpler than recycling.
**How to apply:** don't propose the infinite world or the closed map again unless the user reopens it. The user changes direction often and apologizes for it; reassure briefly and keep docs in sync when asked. See [[working-rules]], [[progress-docs]].
