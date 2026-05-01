---
description: "Tick-based manifest runner. Bootstraps branch/PR state and schedules /drive-tick (via /loop or an inline-fallback scheduler) until terminal state — all verify pass for none mode, merge-ready for github mode — or budget exhaust. Use when you want /define -> green without babysitting, or to autonomously tend a PR through review and CI."
---

Invoke the manifest-dev:drive skill with: "$ARGUMENTS"
