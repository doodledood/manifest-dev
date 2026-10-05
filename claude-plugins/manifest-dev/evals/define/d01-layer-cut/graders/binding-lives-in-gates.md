---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The document under review is a work spec. If it is missing or empty, FAIL.

An executor will work from this spec's checks alone: the acceptance criteria, invariants, or other
gates that must pass before the work counts as done. Anything the work must satisfy has to be in
one of them.

**First, list every requirement stated outside the gates** — in the problem statement, scope,
approach, guidance, notes, or assumptions. A requirement is a statement the work must satisfy: a
must, never, always, a required behavior, a limit, or an exclusion. Problem description,
rationale, suggestions marked optional, and assumptions recorded as defaults are not requirements.
One line each: quote it, then **COVERED** (some gate checks it, in its own words or broader ones)
or **UNGATED** (no gate checks it).

**Then judge:** PASS if no requirement is UNGATED. FAIL if any is, and name it.

Listing nothing is a valid result when every requirement already sits inside a gate.
