# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Quality Gates

No additional quality gates beyond CODING.md base.

## Defaults

*Domain best practices for this task type.*

- **Build the red loop before any theory** — One command that goes red on this exact bug and green once fixed: a failing test, a curl or CLI invocation diffed against known-good output, a replayed captured trace, a throwaway harness, a bisection or differential run. Reading code to build a hypothesis before that command exists is the classic failure — no red loop, no fix attempt
- **Tighten the loop** — Fast (seconds), sharp (asserts the exact symptom, not "didn't crash"), deterministic (pin time, seed randomness, isolate state). For intermittent bugs, raise the reproduction rate — loop the trigger, add stress, narrow the timing window — until it fails often enough to debug, rather than waiting for a clean repro
- **Minimise the repro** — Shrink to the smallest scenario that still goes red, cutting one element at a time; done when removing any remaining element turns it green. A minimal repro shrinks the hypothesis space and becomes the regression test
- **Mechanism, not shape** — The hypothesis must name the specific variable, location, value, and sequence at the bug moment. "Stale state" is a shape; a mechanism is concrete. If you cannot state it concretely, keep tracing — read the code along the execution path, follow the wrong value backwards, enumerate callers of shared APIs
- **Rank rival hypotheses before testing any** — Generate several, each with the prediction that would falsify it ("if X is the cause, changing Y makes the bug disappear"); a hypothesis with no stated prediction is a vibe. Testing the first plausible idea anchors the whole investigation on it
- **Instrument one variable at a time** — Each probe maps to a hypothesis's prediction; prefer a debugger or REPL over logs, and tag any temporary output with one unique prefix so cleanup is a single grep. For performance regressions, measure a baseline and bisect — logs mislead
- **Regression test at a correct seam, before the fix** — The test must exercise the real triggering pattern; a seam too shallow to replicate it gives false confidence, and when no correct seam exists, record that as an architecture finding instead of faking the test. Watch it fail, fix, watch it pass, then re-run the original un-minimised repro
- **Regression check** — Identify all callers/dependents of changed code; verify no behavioral regression from the fix
- **Test correctness** — Verify existing tests assert correct behavior, not the buggy behavior
- **Systemic fix assessment** — Identify the class of bug; probe whether a pattern fix prevents recurrence, and name the confirmed mechanism in the commit or PR description so the next debugger inherits it
