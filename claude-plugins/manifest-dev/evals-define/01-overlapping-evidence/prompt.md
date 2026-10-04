---
max_turns: 20
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 3
---
Use the define skill for this. Shared understanding is settled below; this is contract
encoding, not implementation. Keep any files in the current directory. After your digest, reproduce any Manifest you write **verbatim** in your final
message, including all gate bodies. If an owner decision blocks completion, show the
unresolved decision and keep the contract visibly pending. This lets me review the
actual contract rather than a summary or path.

Our museum has chosen an ambitious interactive river exhibit: visitors vary rainfall,
soil, slope, and vegetation, seek through a 48-hour flood, and compare two scenarios.
Keep all four controls, comparison, and seeking. The purpose is to make the causal sequence
clear and visually memorable on the museum kiosk. The curator pinned the supplied storyboard:
calm setup, rising water, visible overflow, and an explanatory recovery sequence. No live
forecasting or effects beyond 48 hours. The curator is present to decide encoding tradeoffs.

This draft Manifest captures the agreed features, but its gates were written independently.
Revise the proposed contract, preserving every feature and the explicit exclusions:

# Definition: River exhibit
## 1. Intent
- **Problem:** Visitors cannot see how landscape choices change flood progression.
- **Appetite:** One kiosk exhibit, no forecasting platform.
- **Out of bounds:** INV-G2
## 2. Initial Approach (Complex Tasks Only)
- **Architecture:** A local simulation with a rendered timeline and scenario comparison.
## 3. Global Invariants
### INV-G2 — Local educational exhibit only
No live forecasting and no modeled effects beyond 48 hours.
Judgment gate.
### INV-G3 — Defect-free visual sweep
Every combination of all four continuous controls is freshly rendered over the entire
48-hour timeline without any visual defect before every acceptance decision.
Judgment gate.
## 4. Process Guidance
- [PG-1] Implement with realistic kiosk content.
## 5. Known Assumptions
- [ASM-1] The kiosk hardware is available | Default: installed kiosk | Impact if wrong: delayed verification
## 6. Deliverables
### Deliverable 1: Interactive river exhibit
*What it is, and how it is exercised end-to-end:* A visitor changes the four controls,
compares two scenarios, and seeks through the flood sequence.
#### AC-1.1 — Clear causal narrative
Every moment of every parameter combination is gripping and cinematic; repeat complete
visual sweeps until no reviewer can suggest any change.
Judgment gate.
#### AC-1.2 — Comparison and seeking
The four controls, comparison, and seeking all work without visual defects; independently
repeat the full visual matrix on each review.
Judgment gate.

We require those interactions and the storyboard direction, but the sweep procedures and
all-reviewer wording are proposed encoding, not separately chosen obligations. Define an
acceptance plan the curator can approve; identify any decisions still needed rather than
silently discarding features or claiming the draft's impossible sweep is executable.
