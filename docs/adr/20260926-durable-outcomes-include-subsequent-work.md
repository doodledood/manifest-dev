# ADR: Durable outcomes include making subsequent work easier to do correctly

## Status
Accepted

## Area
define / do

## Context

A task can meet its immediate requirements while leaving hidden obligations for
whoever extends it next. Repeated manual coordination transfers correctness to
future contributors and reviewers. The project's promise includes work that can
be trusted with minimal review and a project that retains useful context across
tasks; durability therefore includes the work that follows a change.

The workflow already permits justified prospective Appetite revisions, keeps
explicit exclusions fixed, and gates quality against future uses of the artifact.
A new workflow mode or universal checklist is unnecessary. Some review filters
nevertheless equate value with lines removed, treat repeated patterns as deliberate
convention, or exempt a design because its author chose it intentionally.

## Decision

Make durable outcomes and ease of subsequent correct work a default in solution
selection and acceptance. State the general goal briefly in `/do`; `/define`
encodes concrete future-use burdens in existing quality gates or relevant
Acceptance Criteria. This applies to durable artifacts beyond code. Sound
existing structure needs no redesign, and a disposable artifact need not be
prepared for uses outside its life.

Judge improvements by the obligations, coupling, and opportunities for error they
remove relative to their added complexity, migration risk, and coordination cost.
An author's rationale is evidence to evaluate; explicit owner requirements bind.
Keep the existing scope, amendment, and stopping rules. Improving subsequent work
serves the requested outcome; it does not authorize unrelated modernization or
continued repairs after the acceptance bar is met.

Keep domain judgments in their existing review references. Review unchanged
mechanisms when the current change adds or extends a dependency on them and a
concrete burden is evidenced; unrelated pre-existing debt remains outside scope.
The defect-remediation application has its own acceptance and ownership decision
in 20260926-defect-remediation-requires-justified-prevention.

## Alternatives Considered

- **Leave this as optional Process Guidance:** permits the execution to discard a
  concrete quality requirement that acceptance was meant to protect.
- **Add a reviewer, universal gate, or architectural report to every task:** adds
  process and duplicates domain judgments the existing gates already own.
- **Require restructuring on every task:** encourages unnecessary changes where
  using a sound existing design is the right solution.
- **Keep a lines-removed test and automatic deference to author intent:** these
  proxies can reject a useful owning boundary or preserve an avoidable burden.

## Consequences

### Positive

- Ordinary feature work and non-code artifacts receive the stance before review.
- Existing gates can reject concrete burdens without adding another workflow.
- Scope and proportionate design remain compatible with small changes.

### Negative

- Proportionality still requires judgment; multiple concurrent changes can make
  an otherwise useful restructuring more costly.
- A stated policy does not guarantee model adherence. Behavioral evaluation must
  distinguish improved work from persuasive explanations and unnecessary churn.

## Source

- Related: 20260907-executors-own-unattended-decisions-within-explicit-bounds,
  20260810-advisory-gates-omit-by-bearer-test,
  20260926-defect-remediation-requires-justified-prevention
- [Issue 336](https://github.com/doodledood/manifest-dev/issues/336)
