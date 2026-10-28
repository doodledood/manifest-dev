# FEATURE Task Guidance

New functionality: features, APIs, enhancements.

## Quality Gates

| Aspect | Threshold |
|--------|-----------|
| Requirements traceability | no MEDIUM+ — every specified requirement maps to implementation; nothing lost between spec and code |
| Behavior completeness | no MEDIUM+ — all specified use cases and interactions implemented, not just the happy path |
| Error experience | no MEDIUM+ — feature failures produce clear, actionable feedback to the user, not silent failures or raw stack traces |
| Behavioral exercise | no MEDIUM+ — the new path is *exercised* (run, asserting the outcome), not just confirmed present in the diff |
| Bounded growth | no MEDIUM+ — whatever the feature makes grow per item or over time (stored data, state, calls, connections) has a bound or a cleanup path, or its read and write cost is shown tolerable at the largest scale the project states or the Manifest assumes |

The first three gates *inspect* the artifact; **Behavioral exercise** *runs* it — additive, not a substitute, since they catch different failure modes (a case never implemented vs. one implemented but wired wrong / doesn't run). Encode it **conditional-but-default**: emit it by default when the feature has a runnable surface (HTTP/UI/CLI/callable entry point), and skip it for pure-logic or library changes with no bootable surface. It is **modality-agnostic** — a new integration test that boots and drives the new path is the canonical way to satisfy it (durable, preferred); a live verifier drive (boot, exercise, assert, discard) is the fallback for thin-suite repos or bugs that only surface in the real wiring. The verifier returns **BLOCKED** (not a silent fall-back to inspection) when the surface cannot be booted, so the unmet exercise is visible and routed rather than hidden.

## Defaults

*Domain best practices for this task type.*

- **Document load-bearing assumptions** — Identify what must remain true for the feature to work; surface invisible dependencies
- **Identify affected consumers** — All downstream consumers of changed interfaces or data contracts identified before implementation, including services, related products, analytics/BI/reporting, data pipelines, and exports where relevant
- **Define rollback strategy** — How to reverse the feature if it fails in production; feature flags, migration rollback, or manual revert — with old and new versions able to run side by side during deploy, persisted or sent shapes versioned, and each environment's prerequisites in place first
- **One concern per change** — Keep a fix apart from experiments and unrelated improvements; each lands as its own slice with its own evidence. A pre-existing issue the work meets is no such improvement: unless fixing it is a project of its own, its fix rides the same pull request as its own commit
- **No step that depends on memory** — Where a step relies on someone remembering it, carry it in a check or in the workflow instead
