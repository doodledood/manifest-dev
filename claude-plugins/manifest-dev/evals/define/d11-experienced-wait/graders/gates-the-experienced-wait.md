---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The requirement is what a volunteer experiences: under a second from tapping "check in" to the
next screen, on the older Android phones they carry, with production's ~400 live shifts. The API
already answers in 90 ms, and the 12-shift test fixture hides the slow render.

**First, find the gate (or gates) that check the speed requirement and classify each** as:

- **EXPERIENCED** — it measures tap-to-next-screen time on an older Android phone (or a stated
  stand-in for one) with a production-sized shift list (hundreds of shifts).
- **PROXY** — it measures the server's response time, a render benchmark on a fast machine, or
  anything run against the 12-shift fixture or an unstated data size.

**Then judge:** PASS if at least one speed gate is EXPERIENCED and none of the speed gates that
the spec relies on as proof is a PROXY standing in for it. FAIL if there is no EXPERIENCED gate.
