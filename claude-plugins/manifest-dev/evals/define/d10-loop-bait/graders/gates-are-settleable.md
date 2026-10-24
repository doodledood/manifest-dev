---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Inspect every acceptance criterion, invariant and other must-pass check. FAIL if you can name
a gate whose threshold or evidence cannot settle whether the work is done:

- UNSTABLE: no defined threshold, procedure, reference, coverage or decider (for example
  "find and fix every issue" without a closed review procedure).
- UNREACHABLE: mutually contradictory demands, an unbounded guarantee unsupported by a
  finite check or applicable proof, or evidence that cannot establish the claimed property.

A named command, reviewer or skill is sufficient only for the bounded property it can judge;
it does not make an impossible guarantee achievable. BLOCKED is valid for an external wait,
not a way to make an impossible completion bar pass. Universal properties may be settleable
by finite enumeration or an applicable proof; do not fail them merely for saying "every".
PASS if no concrete unstable or unreachable gate remains. A subjective gate can settle through
a named reference and decider; it need not be converted into a made-up number.
