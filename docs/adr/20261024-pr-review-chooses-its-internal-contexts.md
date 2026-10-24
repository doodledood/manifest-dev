# ADR: PR review chooses its internal contexts

## Status
Accepted

## Area
PR review

## Decided by
The user

## Context
PR review already permits consolidation in the current session, but still requires separate
contexts for each unresolved thread, quality dimension, premise check, and Manifest gate.
Those instructions make a fixed division of work part of the review contract. A reviewer with
the relevant code and history cannot choose to assess related items together.

The caller can explicitly request an independent review. That request is distinct from
requiring a separate context for every internal inspection. Shared context also makes the
blanket exclusion of PR conversation from dimension reviews impossible to honor.

## Decision
The reviewer chooses whether required inspections run in its current session or in separate
contexts when useful. Related work may share a context. Another context remains available for
independent judgment, separable work, or substantial reading; an explicit request for independent
review remains binding.

Every required thread, dimension, and Manifest gate retains its own result and supporting
evidence. The reviewer reads canonical gate text and assesses the artifact rather than accepting
the author's success report. Requirements and permission limits establish scope; an author's
implementation preference does not establish correct behavior. Context reporting describes
what actually ran, without claiming independence from the author when none was present.

Premise questions remain distinct from defect findings and contract verdicts. Their generation
rule, non-blocking role, consolidation rules, review range, follow-up state, blockers, and
posting authority remain unchanged. The deliberate fresh-context review in `/define` stays.

## Alternatives Considered
- **Keep one context per item:** guarantees separate inputs, but prescribes the same arrangement
  for routine follow-ups, related gates, and substantial investigations.
- **Require every inspection inline:** removes handoffs but prevents useful delegation and
  conflicts with an explicit request for independent review.
- **Keep context exclusion while allowing inline review:** cannot hold once the session has
  already read the PR conversation. Evidence-based assessment remains the substantive rule.

## Consequences

### Positive
- Review organization can follow the work without changing the standards or required results.
- The reviewer can retain connected evidence and use the existing skills in either arrangement.

### Negative
- The reviewer must choose a useful division of work and describe its actual independence.
- Accuracy and performance effects are unmeasured. The user chose feedback from actual use
  rather than a separate comparison project; normal repository checks establish instruction
  consistency, not model effectiveness.

## Enforced by
partly — `tests/test_dist_skill_references.py::test_review_pr_required_inspections_keep_context_choice`
and `test_review_pr_manifest_mode_keeps_per_gate_results_without_forced_contexts` preserve context
choice, complete per-item results, canonical gate reads, and blocker rules in source and
distribution. Whether the chosen arrangement improves a real review remains judgment.

## Source
- Amends 20260619-manifest-aware-review-pr
- Amends 20260811-a-review-dimension-may-take-a-defect-as-input
- Clarifies 20260708-judgment-layer-runs-in-manifest-mode-as-a-premise-safety-net
- Clarifies 20260903-shipped-skills-are-host-neutral-and-distributions-read-source
- Extends 20261024-pr-review-consolidation-can-use-the-current-context
- Related: 20261018-define-reviews-each-new-manifest-in-a-fresh-context
