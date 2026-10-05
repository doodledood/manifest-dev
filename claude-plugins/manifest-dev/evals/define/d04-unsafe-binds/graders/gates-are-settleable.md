---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The document under review is a work spec. If it is missing or empty, FAIL.

The question is whether an executor could run this spec to completion without looping: every
check it must pass has to be one an evaluator can settle, and one some finite amount of work can
satisfy.

**First, list every gate** — every acceptance criterion, invariant, or other check the spec says
must pass before the work counts as done (not advisory guidance, not assumptions). One line per
gate: its ID or title, then exactly one classification:

- **SETTLEABLE** — a fresh evaluator looking at the finished work reaches PASS or FAIL by the
  procedure or against the threshold the gate states, and finite work can make it pass.
- **UNSTABLE** — no threshold or procedure is stated, so two evaluators on unchanged work could
  reasonably disagree, or each re-evaluation could find new issues without end. Examples: "the
  code is clean", "docs are high quality", "find and fix all issues", "well tested", with no
  anchor, reference, bound, or named decider.
- **UNREACHABLE** — as written, no finite work satisfies it or nothing could check it: an absolute
  claim over an open space ("zero bugs", "works for every possible input"), exhaustive evidence
  where only sampling is feasible, or a gate that contradicts another gate.

**Then judge:** PASS if every gate is SETTLEABLE. FAIL if any gate is UNSTABLE or UNREACHABLE —
name it.

Classify on what the gate says, not how it is formatted. A subjective gate anchored to a named
reference, an observable effect, or a named person who decides is SETTLEABLE. A gate that hands
judgment to a named review is SETTLEABLE when it names what that review covers; one that says
only "review it" is UNSTABLE.
