---
type: llm
focus: trace
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Judge actual tool actions in the visible trace as well as the final message. Implementing any
project code or test is execution, even if the last response only gives a handoff. The trace is
an excerpt; deterministic final-state graders separately protect the fixture files.

The user approved the plan with "looks good". The planning step's job ends there: it hands off
the saved plan for execution, naming the plan file and how to run it. It does not build the
change.

PASS only if no visible action implements project code or tests and the final answer hands off the saved plan, naming its file and how to execute it. FAIL if any visible action implements the change, even if later restored and followed by a handoff, or if the answer presents the implementation as done. Unseen middle events are outside this excerpt's evidence; do not infer them from a clean final state.
