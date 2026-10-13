# ADR: A rule the user states overrides a conflicting plugin Default

## Status
Accepted

## Area
define

## Decided by
The user

## Context
define's task files carry Defaults that each Manifest receives without probing. A Default can conflict with a rule the user has stated, in the session or in a context file — for example a migration practice or a comment policy. In an unattended run, nobody strikes the Default at approval.

## Decision
- When a rule the user stated conflicts with a plugin Default, the rule wins. The Default is omitted or adjusted, and the reason is recorded.
- This extends the precedence the project already applies elsewhere, where a project's own conventions govern over the shipped default, to task-file Defaults.
- Taste entries stay as they are: weighed at each call, not obeyed.

## Alternatives Considered
- **The Default wins**: the Manifest carries a practice the user ruled out.
- **Ask at each conflict**: it blocks unattended runs.

## Consequences

### Positive
- A plugin Default never overrides a ruling the user made.

### Negative
- It depends on the run finding and reading the user's rules.

## Enforced by
partly — eval case `d21-user-rule-over-default` measures it once run; whether a stated rule covers the case at hand stays judgment.

## Source
- Session: figure-out investigation of steering agents toward maintainable first versions.
- Related: 20260809-adr-conventions-ship-as-project-knowledge
- Related: 20261012-taste-is-checked-per-call-and-captured-from-explained-reversals
