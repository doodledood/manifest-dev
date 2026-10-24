# ADR: PR-review consolidation can use the current context

## Status
Accepted; extended by 20261024-pr-review-chooses-its-internal-contexts: the same placement choice now covers the other PR-review inspections

## Area
PR review

## Decided by
The user

## Context
`review-pr` already holds the completed findings and PR history that its consolidation skill
uses. `review-pr-holistic` edits those findings; it does not generate new ones or post them.
Requiring another isolated context for that editorial work prescribes a handoff without an
established benefit. A skill boundary can preserve the consolidation standard without also
requiring a context boundary.

The review remains a separately invoked workflow. Its placement choice does not add a review
step to `/do`, whose verification method remains its own, or change `/define`'s deliberately
required fresh-context review.

## Decision
After its inspections return, `review-pr` invokes `review-pr-holistic` in the current session
or in an isolated context when useful to the review. Both receive the same findings and context
and follow the same consolidation contract. An unresolved evaluation blocker still prevents a
clean result.

The other independent inspections, including Manifest-mode per-gate verification, keep their
current requirements. This decision concerns editorial consolidation only. It changes neither
the findings worth posting nor posting and approval authority.

## Alternatives Considered
- **Always isolate consolidation:** preserves the existing handoff, but no comparison establishes
  that it improves this editorial task.
- **Always consolidate inline:** removes the handoff but prevents the caller from using another
  context when the particular review benefits from it.
- **Remove all isolated review steps together:** changes defect discovery and independent
  contract assessment at the same time, beyond the evidence for this narrower change.

## Consequences

### Positive
- The reviewer can use the context it already holds while retaining one consolidation skill.
- Delegation remains available without a new mode or flag.

### Negative
- The caller must judge when another context helps.
- Review accuracy and performance under the two choices remain unmeasured. The local scenario
  provides repeatable inputs; fixture checks do not establish model behavior.

## Enforced by
partly — `tests/test_dist_skill_references.py::test_review_pr_required_inspections_keep_context_choice`
pins the caller's choice and blocker rule in source and distribution. The `review-pr` recipe's
`consolidation` scenario checks retained findings and context use; its model run remains unmeasured.

## Source
- [Building agents: When to fold subagents into your main agent loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)
- Related: 20260903-shipped-skills-are-host-neutral-and-distributions-read-source
- Related: 20260619-manifest-aware-review-pr
- Related: 20261018-define-reviews-each-new-manifest-in-a-fresh-context
- Related: 20261024-gate-criteria-and-evidence-travel-with-execution
