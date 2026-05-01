---
description: "Single iteration of /drive. Reads full execution log, loads platform + sink adapters, checks terminal states, handles inbox, delegates implement + verify + fix to /do (intra-tick convergence), runs CI triage + PR tending, then ends or schedules the next iteration. Called by /loop via /drive; also user-invocable for single-tick runs."
---

Invoke the manifest-dev:drive-tick skill with: "$ARGUMENTS"
