# ADR: Source authority governs acceptance and revision

## Status
Accepted

## Area
define / do

## Decided by
The user decided that deliberate requirements remain protected while agent-selected details may
be revised after overall plan approval. An agent chose the schema and workflow integration under
that delegation; the implementation awaits pull-request review.

## Context
An agent can choose a measurable stand-in for a requested result, encode it as a gate, and then
preserve that stand-in more faithfully than the result. For example, a complete catalog export
can fail an agent-selected compactness target while an incomplete sample passes it. Making every
approved gate immutable protects against lowering requirements to escape failure, but also makes
correcting an agent's interpretation depend on another user intervention.

This concerns the North Star's purpose: reliable progress toward the result a person meant, with
the decisions they retain preserved. The goal is not fewer criteria by count. It is preserving
the difference between what is owed and how the agent currently proposes to reach and judge it.

## Decision
The Manifest states an **Outcome**: the source-supported result owed, for whom and in what
circumstances. Execution assesses it under judgment ID `OUTCOME`, in addition to the current
gates. This uses the existing evidence and review machinery, not a separate review phase.

Each gate separates its claim, **Authority**, and **Evidence** method. Hard authority comes from
a deliberately stated user requirement or an applicable project, safety or permission obligation.
Its source and actual obligation travel with the gate. A rationale is useful but is not needed
to make a deliberate requirement hard. A working claim is the agent's operational interpretation;
overall approval of the plan does not independently make it hard. Evidence methods remain working
unless a hard claim explicitly requires the method. Operational interpretations do not belong in
the Outcome, where they would become fixed again.

Working claims remain owed until amended through `define`. An amendment needs evidence of what
the old interpretation got wrong and why its replacement better serves the unchanged Outcome
and hard requirements. Failure or difficulty alone is insufficient. The amendment replaces old
text, receives the existing fresh review, is reported, and invalidates affected evidence. Source
authorization is still required to change the Outcome or a hard requirement. Unclear authority
is resolved from its source, never treated as permission.

Inquiry and handoffs preserve that meaning: suggestions stay suggestions, investigation scope
does not silently become a delivery exclusion, and rationale adds no hidden requirements. Review
looks for both a rejected result that passes the chosen checks and a sound result rejected only
by an unsupported working restriction. Completion remains finite: the Outcome and every current
gate need fresh evidence, with no unresolved amendment. Process Guidance stays advisory.

This is a breaking schema change. Incompatible Manifests require fresh generation; no adapter or
automatic reclassification of an old contract is provided.

## Alternatives Considered
- **Keep immutable gates and improve wording alone:** preserves the old anti-gaming boundary,
  but cannot correct an operational interpretation that execution disproves after approval.
- **Use only a broad goal:** removes false precision but loses explicit hard obligations and
  inspectable acceptance evidence.
- **Keep every requirement in a separate ledger:** can express the distinction, but adds another
  durable artifact and synchronization path when each claim can carry its own authority.
- **Make all agent-authored text revisable:** confuses authorship with authority; an agent may
  encode an actual user requirement or project obligation.
- **Require a minimum floor for each uncertain target:** the floor can itself be another
  unsupported proxy. Preserve a real floor; otherwise use the requested behavior and a working
  assessment whose limits are explicit.

## Consequences
### Positive
- A run can correct its own acceptance machinery without silently lowering what it owes.
- Explicit requirements, including a chosen method without a rationale, stay protected.
- Green checks no longer substitute for assessing the requested result.
- The existing Manifest, amendment, evidence and review paths carry the change end to end.

### Negative
- Authority classification and whole-result judgment can be wrong; the schema does not make
  them mechanically decidable. Focused drives test boundaries, not overall reliability.
- The Outcome assessment adds work, though it can share evidence and context with related gates.
- Older Manifests do not run unchanged. Reverting restores the earlier schema and requires any
  new-format work to be restated; there is no legacy implementation to maintain.

## Enforced by
partly — `tests/test_dist_skill_references.py` checks schema examples, amendment routing,
evidence invalidation and completion consumers; `tests/test_goal_contract_blocks.py` checks
continuation emission; `tests/test_ticket_automation_prompts.py` checks recovery and landing.
The `do` recipe's `working-claim-after-approval` and `hard-claim-without-rationale` scenarios
exercise the authority boundary. Correct classification and acceptance remain judgment.

## Revisit when
Normal use shows working amendments weakening deliberate requirements, repeated blocking on
agent-selected proxies, or Outcome assessment adding cost without changing acceptance decisions.
Read the concrete execution records and affected behavior scenarios before changing the boundary.

## Source
- Issue: https://github.com/doodledood/manifest-dev/issues/421
- Amends: 20260722-state-verification-sufficiency-not-only-necessity
- Amends: 20260726-only-gates-bind-process-guidance-is-advisory
- Amends: 20260727-gate-text-changes-on-the-users-say-so
- Amends: 20260727-manifest-intent-leads-with-problem-appetite-and-bounds
- Supersedes 20261018-a-target-of-unknown-reach-binds-a-floor-and-advises-an-aim
- Related: 20261018-define-reviews-each-new-manifest-in-a-fresh-context
- Related: 20261019-define-searches-each-new-manifest-for-a-wrong-result-that-passes-every-gate
