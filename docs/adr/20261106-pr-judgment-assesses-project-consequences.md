# ADR: PR judgment assesses consequences against project purpose

## Status
Accepted

## Area
PR review

## Decided by
The user

## Context

Correct implementation and a valid product request establish what a change does and why it
was commissioned. They do not establish that landing it improves the project. The existing
judgment pass assessed a change against its stated pain through a closed trigger list; a
requested feature's wider consequences could fall outside that list even when concrete
project evidence supported an objection.

The review path also needs to preserve two distinct conclusions: whether a decision-maker
has settled a trade-off and whether the reviewer recommends that decision. Treating thread
resolution as endorsement loses information. Suppressing all new judgment after one marked
finding also misses consequences introduced by later changes.

## Decision

The existing judgment pass independently assesses whether landing the whole change serves
the project's purpose after material consequences are considered. It uses the available
project direction and its reasons, without requiring the author to use a Manifest or any
particular workflow. Missing material context limits the conclusion. Supported predictions
are admissible when their causal grounds and uncertainty are clear; preference and unsupported
speculation are not.

The pass may recommend proceeding, changing the proposal or not shipping it. Its findings
remain advisory author-facing questions, separate from implementation acceptance and contract
verdicts. A broad principle informs the assessment rather than acting as an automatic veto.

An informed decision by the applicable authority can settle discussion without reversing the
reviewer's recommendation. The assessment retains that disagreement through consolidation,
thread resolution and the operator report. Prior markers prevent repeated comments, not
assessment of materially changed consequences. New evidence can reopen a root on its existing
thread; a distinct root can warrant a new comment.

The existing external-action limits remain: judgment grants no merge veto, request-changes
permission or automatic approval. Any approval still needs the operator's explicit confirmation,
with a retained reservation visible rather than replaced by an unqualified endorsement.

## Alternatives Considered

- **Limit judgment to the requested implementation's stated pain:** keeps a narrow evidence
  boundary but excludes supported project consequences that are the reason not to ship.
- **Add another reviewer layer:** duplicates context and handoffs for a responsibility already
  belonging to whole-change judgment.
- **Turn adverse judgment into a merge gate:** confuses advice with decision authority and
  changes the existing review contract.
- **Regenerate every concern on every pass:** repeatedly contests decisions already settled;
  evidence-aware continuation preserves judgment without repeated comments.

## Consequences

### Positive

- Standalone review can challenge a correct requested change on concrete project grounds.
- A decision and a recommendation remain distinguishable after discussion ends.
- Material later changes receive judgment without restarting settled arguments.

### Negative

- The review needs relevant project context and may have to report a limited conclusion.
- Predictions remain uncertain; one successful behavior drive does not establish broad review
  accuracy or freedom from noise.

## Enforced by

Partly — `verification/recipes/review-pr.md` scenarios `judgment` and `judgment-controls`
exercise consequence reasoning, replies, continuation and the Manifest boundary with local
snapshots. Their outputs require human or parent-agent grading; they do not establish live
GitHub transport or general review accuracy. The property suite holds distribution and
cross-reference integrity.

## Source

- Amends 20260708-judgment-layer-is-a-review-time-premise-check
- Clarifies 20260708-judgment-layer-runs-in-manifest-mode-as-a-premise-safety-net
- Related: 20261024-pr-review-chooses-its-internal-contexts
