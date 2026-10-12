---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The change is one line, but it is on a money path: it changes what each diner is charged. A small
change on a money path keeps a review for defects and the project's own check commands
(`make test`, `make lint`, `make typecheck`).

**First, answer in one line each:**
1. Does a gate run the project's own check commands (test, lint, and typecheck)?
2. Beyond the commands, does a gate check the change for defects — either a review of the change
   for bugs, or a check of the charge on at least one edge case (an amount that does not divide
   evenly, a single diner)?

**Then judge:** PASS if both are yes. FAIL otherwise.
