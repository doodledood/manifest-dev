---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The request handed over a plan cut by technical layer: a model and migration, then REST
endpoints, then a UI.

**First, list every deliverable** in the spec, one line each: its name, then whether a person
could put that deliverable alone (with the ones before it) in front of its real use — an agent
saving, seeing, running, or deleting a search — and observe it working. Classify each as
**SLICE** (exercisable through real use on its own) or **LAYER** (only inspectable as present:
a schema, an endpoint set, a UI shell without the backend behind it).

**Then judge:** PASS if no deliverable is a LAYER. FAIL if any is — name it.

A single deliverable covering the whole feature end to end counts as a SLICE. The spec need not
mention the original three-part plan or explain the re-cut; only the cut it ends up with counts.
