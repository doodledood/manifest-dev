# ADR: Review evidence serves substantive acceptance

## Status
Accepted

## Area
define / do

## Decided by
The user chose substantive acceptance, broad review, evidenced executor dispositions and retained
Manifest output. An agent selected the connected recovery, amendment and transfer repairs under
that implementation assignment; the implementation awaits pull-request review.

## Context
A review grade can become a substitute for the quality it was meant to protect. An executor
then repairs a succession of preferences even when the intended result holds. The opposite
failure is also possible: an empty report, an intentional implementation comment or a green
sample check can hide an unmet obligation. These are source-level failure paths, not a measured
explanation of every round in a reported long review loop.

The Manifest already separates Outcome, sourced claims and evidence methods. Its task defaults
still imposed blanket review-grade gates, and internal finding dispositions were less explicit
than the external-feedback path. Some consumers lost evidence validity or decision authority
when recovering or translating the contract. This concerns the North Star's purpose: results
people can trust, with fewer avoidable interventions and the decisions they retain preserved.

## Decision
Keep the Manifest and its current schema. Define turns applicable quality concerns into claims
about the artifact's supported use and useful life. Evidence names the review dimensions and
methods. Broad review and the bearer-based omission rule remain. Reviewer grades describe
consequence; they are not default acceptance ends. A deliberately required threshold, assessment,
external approval or retained acceptance remains required with its source authority.

A finding must identify a concrete failure or material quality cost against the claim or an
applicable source obligation. The executor assesses it from evidence, records its disposition,
and can reject a false, inapplicable, already resolved or unsupported allegation without reviewer
consensus. Material uncertainty and missing necessary evidence remain unresolved. A correct
finding against a working claim is not a waiver: repair the failure or amend the mistaken claim
through define. Missing a criterion cannot erase the Outcome or a recoverable source obligation.

Review comments and implementation rationale are evidence, not authority. Existing weak patterns
do not excuse a demonstrated failure; adequate local methods do not require larger machinery
merely for uniformity. A passing check that bypasses the needed behavior supplies no proof of it.
Publication filtering does not settle acceptance. PR feedback needs an addressing signal tied
to the actual item, separate from substantive judgment and required external approval.

Keep supported dispositions, first full looks, accepted repair promises and valid evidence
through the existing execution log or Ticket attempt record. A new session or finding ID alone
does not invalidate them. Changed criteria, the actual subject including external state, or
unavailable proof require affected evidence to be refreshed. Completion requires the Outcome,
current gates and bounded mandatory build work to be settled. Preserve the existing limits on
first-look intake and follow-up repair; no new ledger, adjudicator or retry cap is added.

An amendment repairs the faulty claim, evidence method or evaluation. It adds a criterion only
for an uncovered result, not for every missed instance or changed design choice. Deliberate
delivery boundaries retain their authority. Research uses evidence sufficient for the claim's
scope and stakes; a fact about one authoritative source need not acquire an unrelated second
source, and a sound initial result need not manufacture descending review grades.

A demonstrated limiter can rule out a family of impossible approaches. Plausible distinct
alternatives that evade it remain actionable. Exhaustion preserves hard requirements and reports
a blocker, never a successful result or an arbitrary attempt count.

Tickets, goals and handoffs preserve the same claims, hard requirements, working revision freedom,
required proof and disposition authority. References are preferred when the recipient can open
them; otherwise the necessary agreement and continuation state travel in the payload. Optional
write-goal export remains an experiment, not a replacement for define's Manifest.

## Alternatives Considered
- **Keep grade defaults and rely on later amendments:** makes the executor repeatedly correct
  an avoidable mismatch introduced by definition.
- **Drop broad review:** saves work by removing scrutiny, including scrutiny of real defects.
- **Require another adjudicator or unanimous approval:** adds a compulsory review dependency
  without evidence that it improves acceptance.
- **Let the executor waive failed claims:** confuses rejecting an allegation with changing what
  is owed and can conceal real failures.
- **Stop after a fixed number of rounds:** neither proves success nor establishes exhaustion.
- **Replace the Manifest with a goal:** not selected; explicit claims, authority and evidence
  remain useful, while a standalone goal is an optional representation of the same agreement.

## Consequences

### Positive
- Quality claims name the reason review exists, while deliberate review policies still bind.
- Supported decisions survive recovery without silently reusing invalid evidence.
- Definition, execution and transfer share one acceptance meaning and existing state owners.
- Necessary proof and mandatory build work cannot disappear behind a passing grade or marker.

### Negative
- Concrete impact, evidence sufficiency and source authority remain judgments that can be wrong.
- Executor discretion can rationalize weak results; contrary evidence and recorded dispositions
  must remain inspectable. Focused scenarios cannot establish reliability in normal use.
- Bounded mandatory work remains separate from gate verdicts and must be accounted for at completion.

## Enforced by
partly — `tests/test_review_convergence.py` protects default claims, explicit-policy handling,
uncertainty, amendment, completion and recovery boundaries in source and Codex mirrors;
`tests/test_ticket_automation_prompts.py` protects attempt-state continuity;
`tests/test_check_pr_feedback_gate.py` protects item-specific addressing.
`tests/test_acceptance_fixtures.py` establishes seeded failures and controls independently of
agent output. Native scenarios in the define, do, review-code, run-ticket, ticket-up, write-goal,
handoff and check-pr recipes exercise the decision boundaries. The
[behavior report](../research/review-acceptance-20261106.md) records their results and limits;
no full paid eval or general convergence measurement is claimed.

## Revisit when
Normal execution shows supported failures dismissed, claims repeatedly missing material qualities,
or long repair loops moving into repeated amendments. Examine the actual source obligations,
review records and delivered result before changing the boundary.

## Source
- Issue: https://github.com/doodledood/manifest-dev/issues/419
- Issue: https://github.com/doodledood/manifest-dev/issues/421
- Amends: 20260810-advisory-gates-omit-by-bearer-test
- Amends: 20261105-review-severity-follows-consequence
- Amends: 20261025-define-manifests-read-as-current-state-and-every-amendment-is-reviewed
- Amends: 20260812-ticket-recovery-uses-coherent-pushed-checkpoints
- Amends: 20261018-the-tickets-attempt-record-carries-its-manifest-progress-and-run-facts
- Clarifies: 20261018-do-names-the-evidence-that-puts-a-gate-out-of-reach
- Clarifies: 20261021-check-pr-review-feedback-is-one-inbox
- Related: 20261106-source-authority-governs-acceptance-and-revision
- Related: 20261028-every-pull-request-fixes-what-its-work-meets-and-verification-converges
