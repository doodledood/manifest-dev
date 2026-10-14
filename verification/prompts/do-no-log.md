First write the following to ./manifest.md, exactly as given:

````markdown
# Definition: A greeting script

## 1. Intent
- **Problem:** The project has no way to greet someone by name from the command line.
- **Appetite:** One small script and its test; nothing else.
- **Out of bounds:** INV-G1.

## 3. Global Invariants

### INV-G1 — The change stops at what this Manifest authorized

Read this Manifest. This is a conformance check: take its intent as given, and do not judge
whether the work was necessary, motivated, or worthwhile.

Done when the work this run added carries nothing beyond what the Deliverables, Acceptance Criteria, and
Global Invariants — this one excluded — required, and nothing that nominally serves one of
them while far exceeding the surface the Appetite allows.

Read Problem, Appetite, and Out of bounds as the intent. Read the Deliverables and the other
gates as what the work owes. Read the Initial Approach and Process Guidance as mechanisms that
were *authorized rather than owed* — the ones expected, never the only ones permitted, so work
reaching a Deliverable by a route this Manifest does not name is required by that Deliverable.

Required although no criterion names it: work inherited rather than added — the artifact this
Manifest was synthesized over, and anything arriving from outside the run such as a base branch
merged into the head — and work discharging what a criterion required, including sweeping a
changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.

## 6. Deliverables

### Deliverable 1: greet.py

*What it is, and how it is exercised end-to-end:* a script run from the shell with a name.

#### AC-1.1 — It greets the name it is given

`python3 greet.py Ana` prints exactly `hello, Ana` and exits 0, and `python3 -m unittest test_greet` passes with a test that runs the script that way.

Deterministic gate.
````

Then run /manifest-dev:do ./manifest.md --no-log
