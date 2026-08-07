# REFACTOR Task Guidance

Restructuring without behavior change.

## Quality Gates

No additional quality gates beyond CODING.md base.

## Defaults

*Domain best practices for this task type.*

- **Establish behavior contract** — Define exactly what behavior is preserved and how preservation is verified (existing tests, characterization tests, comparison). Every refactor needs this before starting
- **Identify consumers** — All callers and dependents of refactored code identified; implicit contracts surfaced
- **Characterization tests if gaps exist** — When no tests cover the refactored area, write characterization tests as a prerequisite deliverable
- **Expand–contract for wide mechanical changes** — When one rename or retype fans across the codebase so no single slice can land green: add the new form beside the old, migrate call sites in batches sized by blast radius with checks green after each, and delete the old form only when no caller remains. When even batches can't stay green alone, stage them on an integration branch verified as one merge
