# ADR: Decision records name what enforces them, and that line is editable in place

## Status
Accepted

## Area
ADR conventions

## Decided by
The user

## Context
A decision recorded only in prose depends on every later contributor reading the record. In one sampled codebase, roughly half to two-thirds of the decision records pinned something that a type, a schema, an import rule, or a test could check. Few of them named such a check. The rest were metric design, deliberate non-actions, or one-time operational choices that no check can hold.

## Decision
- The record template gains `## Enforced by`. It names the strongest check that holds the decision — a type or structure, a lint or architecture test, an invariant test, or one owning site — and what the check pins. A partial case reads `partly — <check>; <what stays judgment>`. A decision that a check could hold, before anyone has built that check, reads `not yet — <the check that would hold it>`. A session that cannot write code records a decision this way. The run that implements the decision builds the check and replaces the line. A case with no possible check reads `none — <why>`.
- The check carries a comment that cites the record, so a contributor about to weaken it meets the decision first.
- The line records current enforcement, not the decision. It is editable in place, like Status and cross-references.
- Writing a record that supersedes or narrows another also retargets or retires the old record's check in the same change, and updates the old record's `Enforced by` line.
- This project's conventions file and the shipped default convention change together.

## Alternatives Considered
- **Freeze the line with the record's body**: the first supersession leaves it pointing at a retired check.
- **A separate rules table in the context file**: it is a second source that drifts from the records.
- **No field**: decisions that a check could hold stay in prose and go unenforced.

## Consequences

### Positive
- A decision becomes a check wherever one is possible, so it holds for contributors who never read the record.
- A record states plainly when it cannot be enforced, and why.

### Negative
- One more field to fill in each record.
- The in-place edit is one more exception to record immutability.

## Enforced by
`tests/test_project_conventions_forks.py` — `test_forks_reproduce_the_emitted_default` keeps this project's conventions, which carry the field, in step with the shipped default; eval case `31-record-names-what-enforces-it` measures that records carry it.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions; aggregate figures only.
- Related: 20260809-adr-conventions-ship-as-project-knowledge
- Related: 20261012-decision-records-name-who-decided
