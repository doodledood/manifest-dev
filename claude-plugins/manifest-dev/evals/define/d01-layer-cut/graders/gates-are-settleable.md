---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Scan the gates — every acceptance criterion, invariant, or other check the spec says must pass
before the work counts as done — for a specific gate that would send an executor round a repair
loop:

- **UNSTABLE** — it states no threshold, procedure, reference, bound, or named decider, so two
  evaluators on unchanged work could disagree or keep finding new issues: "the code is clean",
  "docs are high quality", "find and fix all issues", "well tested".
- **UNREACHABLE** — no finite work satisfies it or nothing could check it: "zero bugs", "works for
  every possible input", exhaustive evidence where only sampling is feasible, or a contradiction
  with another gate.

These are settleable, so skip them: a gate that hands judgment to a named skill or review and says
what it covers; a gate that lists what to check or names the command to run; a gate with a BLOCKED
exit for when it cannot be checked; a subjective gate anchored to a named reference or decider.

FAIL only if you can name a specific gate that is UNSTABLE or UNREACHABLE. Otherwise PASS.
