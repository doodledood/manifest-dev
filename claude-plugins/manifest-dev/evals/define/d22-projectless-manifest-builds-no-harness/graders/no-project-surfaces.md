---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The work is a one-off script, defined in a folder holding only two downloaded bank exports: not
a project. No later session will change this work, so it needs no project setup.

**First, list** every Deliverable, criterion, invariant or guidance line that builds, updates,
runs or gates on a verification harness, a recipe, a decision record (ADR), a glossary or
CONTEXT.md, a North Star, a context file, or a project setup or its update. A line that only
notes these are not needed does not count.

**Then judge.** PASS only if that list is empty and the specification still has criteria that
check the script's output itself — the merged rows, the date and amount formats from both
exports, the sort order. FAIL otherwise.
