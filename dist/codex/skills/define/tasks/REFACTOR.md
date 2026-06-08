# REFACTOR Task Guidance

Restructuring without behavior change.

## Quality Gates

No additional quality gates beyond CODING.md base.

## Defaults

*Domain best practices for this task type.*

- **Establish behavior contract** — Define exactly what behavior is preserved and how preservation is verified (existing tests, characterization tests, comparison). Every refactor needs this before starting
- **Identify consumers** — All callers and dependents of refactored code identified; implicit contracts surfaced
- **Characterization tests if gaps exist** — When no tests cover the refactored area, write characterization tests as a prerequisite deliverable
