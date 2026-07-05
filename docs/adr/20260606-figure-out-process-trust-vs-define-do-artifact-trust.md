# ADR: figure-out provides process trust, kept distinct from define→do's artifact trust

## Status
Accepted

## Context

figure-out is increasingly used as an investigation/research vehicle — root-cause analysis, pre-`/define` understanding, technology evaluation — not only as a quick thinking step before `/define`. This raised two coupled questions:

1. The pre-rework `/define` had (and still has) a research task file (`define/tasks/research/RESEARCH.md`) with a deep adversarial methodology. Does that methodology apply to figure-out when figure-out is the one doing the investigating?
2. Users want to trust figure-out's output *without rechecking it* — "the engine that unravels the truth." Should figure-out therefore gain verification machinery (independent verifier fan-out, RESEARCH.md's quality gates) so its conclusions can be trusted standalone?

The tension: pulling research's full methodology in, or adding verifier fan-out, would push figure-out toward becoming a second `/do`.

## Decision

figure-out's trustworthiness is **process trust** — the rigor of the dialogic unraveling itself (wide hypothesis enumeration, belief register, pressing alternatives, verifying against code/world) — and is kept categorically distinct from define→do's **artifact trust**, which is bought by spawning *independent* verifier subagents per Acceptance Criterion and Global Invariant to attack a produced Deliverable.

figure-out produces understanding, not a Deliverable. There is no artifact for independent verifiers to gate. Therefore:

- **Do not** bolt verifier fan-out onto figure-out, and **do not** import RESEARCH.md's verifier-gate tables. That reinvents `/do` and breaks the established two-set task-file shape distinction (define's gates/Defaults vs. figure-out's probing fuel).
- Only the **process-rigor half** of the research methodology transplants (competing-hypotheses discipline, outside view, adversarial convergence). The artifact-gating half does not.
- **Non-convergence is the natural router**: when figure-out's investigation cannot settle, that is the signal the problem is artifact-grade and wants `/define` + `/do`, rather than a reason to grow figure-out.

## Alternatives Considered

- **Converge figure-out with define→do / add verifier fan-out to figure-out**: make figure-out spawn independent checkers so its output is standalone-trustable — Rejected: reinvents `/do`, and figure-out has no Deliverable to verify; breaks the shape distinction between the two task-file sets.
- **Lift RESEARCH.md wholesale into figure-out**: import the full research methodology as figure-out guidance — Rejected: most of RESEARCH.md is verifier gates for a finished report (wrong shape), and the intellectual-rigor remainder is largely already in figure-out's spine.
- **Treat figure-out and define→do as interchangeable for investigation**: pick by preference — Rejected: they buy different kinds of trust; the discriminator is whether the conclusion must be trusted by someone who will not re-derive it.

## Consequences

### Positive
- Clear, durable boundary between the two tools; figure-out stays lean and keeps its identity as an understanding engine.
- define→do remains the path when an output must be trusted as a standalone artifact (no human in the loop to re-check).
- Non-convergence gives a principled handoff point from figure-out to `/define`.

### Negative
- figure-out's `--autonomous` mode retains a self-grading limitation — with the human removed, nothing independent checks its convergence. Accepted here and partially mitigated by inline process rigor (see related ADR); full independence is deliberately deferred.

## Source
- Related: See also 20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass; 20260604-figure-out-owns-domain-probing-via-mirrored-task-files
