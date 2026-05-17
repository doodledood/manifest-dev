# BUG Task Guidance

Defect resolution, regression fixes, error corrections.

## Quality Gates

No additional quality gates beyond CODING.md base.

## Defaults

*Domain best practices for this task type.*

- **Establish reproduction** — Exact repro steps before attempting any fix; verify repro is complete and correct
- **Mechanism, not shape** — The hypothesis must name the specific variable, location, value, and sequence at the bug moment. "Stale state" is a shape; a mechanism is concrete. If you cannot state it concretely, keep tracing — read the code along the execution path, follow the wrong value backwards, enumerate callers of shared APIs
- **Regression check** — Identify all callers/dependents of changed code; verify no behavioral regression from the fix
- **Test correctness** — Verify existing tests assert correct behavior, not the buggy behavior
- **Systemic fix assessment** — Identify the class of bug; probe whether a pattern fix prevents recurrence
