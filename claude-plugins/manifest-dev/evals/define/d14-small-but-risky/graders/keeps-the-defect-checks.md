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
2. Does a gate review the change for defects (bugs, wrong totals, edge cases such as amounts that
   do not divide evenly or a single diner), beyond the commands?

**Then judge:** PASS if both are yes. FAIL otherwise.
