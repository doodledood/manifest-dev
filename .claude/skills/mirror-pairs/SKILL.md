---
name: mirror-pairs
description: 'The red-flag lists mirrored between figure-out''s and define''s task files, so a change to one side lands on the other. Use when editing a task file under figure-out/tasks/ or define/tasks/.'
user-invocable: true
metadata:
  internal: true
---

# Red-flag mirror pairs

figure-out's task files and define's task files are decoupled, so a red-flag list both need lives in both. Change one, change the other:

- `figure-out/tasks/CODING.md` (*Shape before build*, *Already provided*, *Earned depth*, *A second shape*, *What the next agent copies*, *Design discipline*, *Recorded intent*, *Drivable and debuggable*, *Failure visibility*, *Silent regression*, *Verification design*'s independent expected values and whether example tests can reach the case that breaks, and *The verification harness*'s fit-to-trust question) ↔ `define/tasks/CODING.md` Defaults (*Sketch the shape before implementing*, *Use what is already provided*, *Earn each module's depth*, *Screen for what the next agent copies*, *Hold the design discipline*, *Read the intent before removing or adding a guard*, *Make failure visible and the result drivable*, *Name what could regress silently*, *Agree test seams before authoring tests*, *Reshape, don't patch*, *Trust the check before relying on it*).
- `figure-out/tasks/FEATURE.md` (*Bundled concerns*, *Remembered steps*, *Rollback*, *Orphaned resources*, *Driven as the person*) ↔ `define/tasks/FEATURE.md` Defaults (*One concern per change*, *No step that depends on memory*, *Define rollback strategy*) and its *Bounded growth* and *Journeys driven as the person* gates.
- `figure-out/tasks/DOCUMENT.md` (*One mode*, *A fact restated*, *The same fact twice*) ↔ `define/tasks/DOCUMENT.md` Defaults (*One mode per document*, *Generate or link what code owns*, *One copy of each fact*).
- `figure-out/tasks/DOCUMENT.md` and `WRITING.md` (*Sources in hand*) ↔ `define/tasks/PROSE_FLOOR.md` *Accuracy* gate; `figure-out/tasks/WRITING.md` (*The author's own point*) ↔ `define/tasks/WRITING.md` gates.
- `figure-out/tasks/UI.md` (*Every state*, *Who and where*, *Honest figures*, *First look*) ↔ `define/tasks/UI.md`'s design gate, whose `review-design` standards cover functional states, access, medium, figure fidelity, and where the eye lands first and the path it follows.
- `figure-out/tasks/PROMPTING.md` (*A protocol on shared state*; *A rule in two files*, including a contradicted one; *An instruction where a check belongs*) ↔ `define/tasks/PROMPTING.md` Defaults (*Model a shared protocol before shipping it*, *One rule, one place*).
- `figure-out/tasks/MEASURE.md` ↔ `define/tasks/MEASURE.md` (the measure proven then frozen, noise floor, fair comparison, unlike scenarios, a floor on attempts).
- `figure-out/tasks/PERF.md` ↔ `define/tasks/PERF.md` (limiter, bounded gain, verdict).
- `figure-out/tasks/HILLCLIMB.md` ↔ `define/tasks/HILLCLIMB.md` (quick or thorough, the cheap check's conditions, what a round can afford, what the next round sees, a priority that moves, a judge that can be fooled, one primary with guards; define alone keeps real use against prediction, a measure that could rise without the goal and getting past the nearest peak, which the model raises unprompted in figure-out). define's file states outcomes and the user's rulings, never steps (`docs/adr/20261107-climb-guidance-states-outcomes-and-rulings-not-steps.md`).
