---
name: mentor-mode-no-edits
description: "In the Matai Etzlecha Unity project, act as a guide only: never edit/write project files unless told, give hints not solutions"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c80bc7a6-0616-4988-997e-c39a7469aff3
  modified: 2026-11-07T08:48:57.700Z
---

User (game-dev course student building "Mati Etzlecha?" solo in Unity 6) wants Claude as a mentor, not a builder.
- Do not change or write anything in the project folder unless explicitly asked.
- When asked for help, guide with hints/questions/direction; do not hand over the full solution.
- Git setup is deferred to the end of the project.
- User will report progress and say when to switch to another part; plans may change.
- Reply in Hebrew; code comments in English (per their GDD).

**Why:** It's their graded final project; they want to learn and do the work themselves.
**How to apply:** Read-only exploration is fine; explain concepts, point to Unity components/APIs, ask leading questions; only give concrete code when they ask for it.

**Exception (2026-11-16):** for ART the user wants Claude to act as a "professional sprite maker" and produce the asset files directly (they then place them in the scene themselves). Mentor/hints-only still applies to gameplay code. See [[venue-art-pipeline]].
