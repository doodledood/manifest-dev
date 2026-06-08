# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Requirements traceability | general-purpose | no MEDIUM+ — every specified requirement maps to implementation; nothing lost between spec and code |
| Behavior completeness | general-purpose | no MEDIUM+ — all specified use cases and interactions implemented, not just the happy path |
| Error experience | general-purpose | no MEDIUM+ — feature failures produce clear, actionable feedback to the user, not silent failures or raw stack traces |

## Defaults

*Domain best practices for this task type.*

- **Document load-bearing assumptions** — Identify what must remain true for the feature to work; surface invisible dependencies
- **Identify affected consumers** — All downstream consumers of changed interfaces identified before implementation
- **Define rollback strategy** — How to reverse the feature if it fails in production; feature flags, migration rollback, or manual revert
