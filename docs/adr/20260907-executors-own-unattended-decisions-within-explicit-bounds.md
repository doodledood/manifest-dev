# ADR: Executors own unattended decisions within explicit bounds

## Status
Accepted

## Area
define / do

## Context

An executor that asks for routine decisions stalls an unattended run even when it
has enough information and authority to proceed. Mid-run steering already assumes
the user leaves immediately, but that rule did not govern every execution path.
`do` could escalate a non-converging design before investigating a replacement;
`just-do` stopped on any false premise and prohibited Manifest amendments. A
verifier's BLOCKED verdict or an outer continuation contract could also end a run
while independent work remained.

The Manifest already separates binding outcomes from an advisory implementation
plan. Appetite sets the size of change the problem is worth, while explicit
exclusions reserve decisions the executor may not reverse. Treating a justified
change in approach or size as equivalent to crossing an exclusion prevents the
executor from choosing a durable solution to the requested problem.

## Decision

Both executors assume the user is AFK throughout execution, including nested skill
calls and amendments following a steering message. They discover available facts,
make defensible decisions within their authority, and report material choices and
their rationale afterward. A live message does not reopen an interview.

The executor may change the approach and revise Appetite when the broader
solution's benefit to the requested outcome justifies its added complexity and
maintenance. The revision goes through the executor's authoring skill before the
broader work starts. It never authorizes unrelated improvements, crosses an
explicit exclusion, changes a binding requirement, or retroactively excuses excess
already produced. Explicit exclusions are encoded once as Global Invariants and
referenced from Intent; anticipated omissions that may change belong in the
advisory plan. The ceiling continues to judge the current authorized scope.

An amendment invalidates every affected gate's evidence, including the ceiling
when Appetite changes. It waits for active evaluations; verdicts from a raced
amendment are discarded. `just-do` gains the authoring path needed to exercise this
delegation without importing `do`'s verification topology. Existing authority over
gate changes is otherwise unchanged: an executor cannot lower a bar because
meeting it is costly, and `do` retains its bounded incidental-mechanism repair.

A blocked obligation has no viable authorized path after credible alternatives
have been investigated. Proceeding requires unavailable knowledge or access, new
authority, or a change to a binding requirement. A failed design calls for recovery
or redesign; repeating attempts without new evidence or progress is not recovery.

The executor reports an established blocker promptly and continues useful
independent work that does not depend on guessing the blocked decision. Only when
none remains does it invoke terminal escalation. This preserves existing callers
that interpret escalation as the end of an attempt. Progressing external processes
remain waits, and no-wait callers report pending after actionable work is exhausted.
Missing verification capabilities preserve the selected policy while other useful
work proceeds; they never silently downgrade verification.

## Alternatives Considered

- **Ask whenever an important decision appears:** preserves an opportunity for
  immediate correction, but assumes a present user and turns ordinary execution
  judgment into a stalled run.
- **Keep the original Appetite fixed:** limits unexpected growth, but can force a
  fragile local solution when a proportionate shared repair better serves the same
  outcome. Prospective amendment retains a reviewable scope and verification.
- **Authorize any improvement not explicitly excluded:** avoids scope questions,
  but permits unrelated modernization and indefinite expansion. The requested
  outcome and the benefit relative to added burden still justify each expansion.
- **Stop the whole run on the first blocked obligation:** makes handoff immediate,
  but strands independent implementation and verification. A progress notice
  supplies early visibility without ending the attempt.
- **Use escalation for both notices and terminal results:** avoids distinguishing
  the two reports, but callers could release a Ticket or end a chain while the
  executor still has work. Escalation remains terminal.

## Consequences

### Positive

- Both execution paths hold the same default decision authority and AFK posture.
- Scope can adapt to a durable solution without rewriting success after the fact.
- Blocked work remains visible while independent progress continues.
- Shared continuation contracts preserve the policy after a restart or through an
  outer PR workflow.

### Negative

- The executor may choose a broader solution the user would have declined;
  explicit bounds, justification, verification, and the audit trail limit that risk.
- Judging viable recovery and proportionality remains a model decision, not a
  fixed retry count or a guarantee that every unattended run completes.
- `just-do` carries additional authority and amendment rules to make its autonomy
  safe across authoring and verification boundaries.

## Source

- Amends: 20260727-manifest-intent-leads-with-problem-appetite-and-bounds,
  20260727-define-encodes-for-full-do-autonomy,
  20260807-trim-the-manifest-schema-to-fields-that-are-read,
  20260810-gate-altitude-repairs-under-advance-delegation,
  20260830-just-do-states-the-floor-and-keys-its-log-to-the-manifest
- Related: 20260709-mid-do-steering-stays-autonomous,
  20260905-executors-own-path-bearing-continuation-goals
