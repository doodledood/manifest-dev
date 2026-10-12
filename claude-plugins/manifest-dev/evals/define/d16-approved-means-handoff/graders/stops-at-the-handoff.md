---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user approved the plan with "looks good". The planning step's job ends there: it hands off
the saved plan for execution, naming the plan file and how to run it. It does not build the
change.

**First, classify the final reply** as:

- **HANDOFF** — it confirms the plan and hands it off (for example "Manifest complete: <path>" with
  how to execute it), without saying it changed the project's code.
- **IMPLEMENTED** — it says it changed, or is changing, the project's code or tests, or presents
  the fix as done.

**Then judge:** PASS if HANDOFF. FAIL if IMPLEMENTED.
