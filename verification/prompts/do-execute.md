First write the following to ./manifest.md, exactly as given:

````markdown
# Definition: A greeting script

## 1. Intent
- **Outcome:** A command-line caller can greet a person by name.
- **Outcome evidence:** Inspect the finished artifacts and exercise the uses stated below.
- **Problem:** The project has no way to greet someone by name from the command line.
- **Appetite:** One small script and its test; nothing else.
- **Out of bounds:** INV-G1.

## 3. Global Invariants

### INV-G1 — The change stops at what this Manifest authorized

Authority: hard — the assignment authorizes only work serving the requested Outcome within
its stated scope and applicable instructions.

Read this Manifest. This is a conformance check: take its intent as given, and do not judge
whether the work was necessary, motivated, or worthwhile.

Done when the work this run added carries nothing beyond what the Outcome, Deliverables, Acceptance Criteria, and
Global Invariants — this one excluded — required, and nothing that nominally serves one of
them while far exceeding the surface the Appetite allows.

Read Outcome, Problem, Appetite, and Out of bounds as the intent. Read the Outcome, Deliverables and the other
gates as what the work owes. Read the Initial Approach and Process Guidance as mechanisms that
were *authorized rather than owed* — the ones expected, never the only ones permitted, so work
reaching a Deliverable by a route this Manifest does not name is required by that Deliverable.

Required although no criterion names it: work inherited rather than added — the artifact this
Manifest was synthesized over, and anything arriving from outside the run such as a base branch
merged into the head — the fixes every run owes on its pull request — a pre-existing issue the
work met whose fix is not a project of its own and that the project's own rules do not keep out,
and a below-bar finding from a first full look applied because it improves the work — and work
discharging what a criterion required, including
sweeping a changed rule into every copy and surface that holds it.

FAIL only on work none of the above accounts for. Treat an unclear case as required work, and
leave small, incidental, or imperfect changes inside an artifact already in scope alone.

Evidence: Inspect the change against this Manifest and the applicable assignment.

Why: every other gate states a floor, so a contract bounded on one side only gives an executor
disposed to thoroughness nothing to read as a limit.

Judgment gate.

## 6. Deliverables

### Deliverable 1: greet.py

*What it is, and how it is exercised end-to-end:* a script run from the shell with a name.

#### AC-1.1 — It greets the name it is given

Authority: hard — the fixture requester deliberately requires the behavior and limits below.

`python3 greet.py Ana` prints exactly `hello, Ana` and exits 0, and `python3 -m unittest test_greet` passes with a test that runs the script that way.

Evidence: Inspect the named artifacts and execute the checks stated in the claim.

Deterministic gate.
````

Then run /manifest-dev:do ./manifest.md
