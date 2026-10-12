# ADR: Decision records name who decided

## Status
Accepted

## Area
ADR conventions

## Decided by
The user

## Context
An autonomous figure-out run self-accepts a decision record when the record's bar clearly fires and the content comes from the session. The record it writes reads exactly like one a person ruled. A later agent that consults the corpus before re-deciding cannot tell the two apart, so it may treat an unreviewed agent's call as the owner's ruling and hold it against new evidence.

## Decision
The record template gains a `Decided by` field with two values: `The user`, when a person decided or reviewed the record before it was accepted, and `An agent in an unattended run, with no review`, when a run with no person present accepted its own record. Autonomous figure-out writes the unattended value when it self-accepts a record. When a person later reviews such a record and keeps its decision, the value changes to `The user` in place; a person who changes the decision writes a new record.

The field lands in this project's `docs/adr/CONVENTIONS.md` and the shipped ADR format, kept identical. It applies to new records only. Existing records stay as written, per the immutability rule.

## Alternatives Considered
- **A note in the Source field**: the Source field holds references; a decider buried there is easy to miss and has no fixed values.
- **Backfill existing records**: the corpus does not record who decided most of them, and rewriting published records breaks the immutability rule.
- **Forbid unattended runs from writing records**: this loses decisions that meet the bar while nobody is present.

## Consequences

### Positive
- A later reader can weigh an agent's unreviewed call as such.
- A person's review has a visible, one-line effect on the record.

### Negative
- Older records carry no decider, so their provenance stays unknown.
- Projects with their own conventions copy gain the field only when they take the updated default.

## Source
- Session: figure-out investigation of unattended decision-making.
- Related: 20261012-unattended-runs-flag-the-users-calls-by-disagreement-not-confidence
