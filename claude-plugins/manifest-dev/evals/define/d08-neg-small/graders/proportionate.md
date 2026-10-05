---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

This is a mechanical rename with no behavior change. A proportionate spec is small: one
deliverable, checks that the old name is gone and the new one works (typecheck and tests pass, no
remaining references), and anything that reviews the rename itself. A disproportionate one adds
work nobody asked for.

**First, list every gate** — one line each: its ID or title, then **IN SCOPE** (checks the rename
or reviews the change itself — no leftover references, builds, typechecks, tests pass, no
behavior change, the diff is only the rename) or **SCOPE CREEP** (requires work beyond the rename:
new tests for behavior that didn't change, docs rewrites, refactors, a deprecation alias nobody
asked for, cleanup of unrelated code).

Also count the deliverables.

**Then judge:** PASS if no gate is SCOPE CREEP and there are at most two deliverables. FAIL
otherwise — name what crept.

A ceiling rule saying the work stops at what was asked is IN SCOPE.
