# ADR: Research delegation follows the inquiry

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context
The research Default prescribed a context per source type and prohibited the coordinating
session from researching directly. Its web overlay repeated that prescription. A separate
Default also required parallel verification. Source types do not determine whether questions
are separable: a log, a mapping, and an API contract may need to be read together to explain
one failure. The coordinator can also need a decisive source to resolve conflicting findings.

These instructions shape the research guidance that `/define` puts in a Manifest. They are
distinct from the research-quality gates and from deliberate independent workflow reviews.

## Decision
The research base owns one conditional delegation Default. Delegate separable questions,
substantial reading, or independent checks when another context helps. Each delegated part
receives its question, scope, and needed evidence. The coordinator may inspect sources directly
and keeps tightly coupled reasoning together. Work inline when delegation is unavailable or
adds no value.

The web overlay carries source-specific guidance without repeating the delegation rule. The
research-quality gates and their thresholds remain unchanged, and useful independent checking
remains available. This decision introduces no new verification phase or rule for other skills.

## Alternatives Considered
- **Keep source-type delegation mandatory:** supplies a predictable division, but forces apart
  evidence that may answer one coupled question and prevents direct inspection by its synthesizer.
- **Require all research inline:** removes handoffs but also excludes useful parallel reading
  and independent checks.
- **Keep separate delegation rules in source overlays:** allows specialization, but no
  source-specific exception is needed here; duplicate rules can contradict the base.

## Consequences

### Positive
- The inquiry can determine the division of work while the quality standard stays fixed.
- One Default owns delegation across the composed research guidance.

### Negative
- The run must judge whether another context helps and retain enough evidence for synthesis.
- Research quality, encoding reliability, and performance under the changed guidance remain
  unmeasured. A repeatable planning scenario does not establish those outcomes.

## Enforced by
partly — `tests/test_dist_skill_references.py::test_research_delegation_follows_the_inquiry_in_one_owning_default`
pins direct source access, conditional delegation, and removal of the old prescriptions in
source and distribution. The `define` recipe's `research-delegation` scenario checks emitted
guidance; its model run remains unmeasured.

## Source
- [Building agents: When to fold subagents into your main agent loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop)
- Related: 20261024-pr-review-consolidation-can-use-the-current-context
- Related: 20261018-define-reviews-each-new-manifest-in-a-fresh-context
