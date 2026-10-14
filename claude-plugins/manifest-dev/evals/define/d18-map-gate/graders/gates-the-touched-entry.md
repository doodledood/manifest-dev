---
type: llm
focus: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The repository keeps a verification harness, `scripts/verify`, with one recipe per feature
under `verification/recipes/`, and the change touches the overdue recipe, which has no
evidence yet (`unverified`).

**First, quote** the gate, if any, that requires the overdue recipe to be updated and run.

**Then judge:** PASS if a gate requires the touched recipe to be updated to the new behavior
and run with the harness. FAIL otherwise.
