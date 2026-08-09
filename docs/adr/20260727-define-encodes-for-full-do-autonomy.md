# ADR: /define encodes for full /do autonomy

## Status
Accepted

## Area
define

## Context

Mid-run human interaction is the costliest event in the workflow: an unattended `/do` run that stalls on an avoidable escalation forfeits the value unattended execution exists to provide — the practical cost is closer to losing development days than to the minutes the question takes. Meanwhile a question asked at `/define` time, while the user is already in the interview, is nearly free. That asymmetry says avoidable escalations should be manufactured out of the manifest before execution starts, not handled gracefully after.

Two mechanical facts locate where `/define` currently manufactures them:

1. **Gate text is immutable to `/do`.** Per `20260727-gate-text-changes-on-the-users-say-so`, a gate that misdescribes what it judges routes to `/escalate` — the run may not rewrite its own binding layer. So a gate pinned to a *mechanism* `/do` could legitimately pivot away from is a pre-committed escalation: the moment the pivot happens, the gate goes false about the work for reasons the user never cared about.
2. **Known Assumptions record impact but nothing routes on it.** An ASM entry carries "impact if wrong," but an assumption whose failure would invalidate a Deliverable's whole approach passes through the same slot as a harmless default — and detonates mid-run. This is Shape Up's named failure ("betting on a rabbit hole"): its one project-abandonment case study was a bet on an assumed-to-exist design solution nobody had produced.

`/do` itself already treats escalation as a last resort, so nothing on the execution side is left to tighten; the leverage is all at encoding time.

## Decision

`/define` adopts escalation-minimizing encoding as a stated discipline, with two rules — one principle applied at the two places the encoder manufactures future escalations:

1. **Gate altitude.** Acceptance Criteria and Global Invariants bind *outcomes* at the altitude of the Problem and Appetite; mechanisms the executor may legitimately change are recorded in the Initial Approach as decided-but-advisory elements. The overfit test at write time: *if `/do` found a better way to satisfy the intent, would this gate go false anyway?* If yes, the gate is pinning the how. Under-specification remains guarded from the other side by the existing exercisable-slice rule.
2. **Upstream triage of load-bearing unknowns.** A leftover gap whose impact-if-wrong is a failed *approach* (the run would re-plan, not merely re-do work) is un-assumable: `/define` either bounces it to figure-out for resolution or settles it deliberately — dictating a good-enough patch on the record, Shape Up's hole-patching move. The settled choice is routed by whether it must hold: a gate when it binds, Initial Approach direction when it is guidance, since the Initial Approach stays departable by design and adds no slot for decisions meant to survive execution. Ordinary defaults continue to flow to ASM entries unchanged.

Autonomy is never bought by weakening safety: the safety-critical routing (violations that would be unsafe or irreversible become Global Invariants) is untouched, even where a stop is the price.

The two rules are recorded as one decision because each is the friction asymmetry acting on a different encoding artifact — gates and assumptions — and either alone leaves the other half of the escalation surface in place.

The principle lives in the skills rather than in user memory: a taste entry would steer only sessions that load it, while skill content serves every user of the workflow, and the preference is a design property of the system rather than of one operator.

## Alternatives Considered

- **Tolerate risky ASMs because agent runs are cheap and retryable**: — Rejected: the retry is not the cost; the stall is. Cheap re-execution does not compensate for an unattended run parking on a question.
- **Enforce autonomy on the `/do` side**: — Rejected: `/do` already escalates only as a last resort and is forbidden from amending gate text, so by the time a manufactured escalation reaches it, its options are exhausted. The defect is created at encoding time and must be prevented there.
- **Persist the principle as a personal taste entry**: — Rejected: taste is for steering the system does not encode; once the skills encode it, the entry is redundant where it matters and invisible everywhere else.

## Consequences

### Positive
- A whole class of redundant escalations — mechanism-pinned gates invalidated by legitimate pivots — is removed at the source.
- Load-bearing unknowns surface while the user is present to resolve them, instead of mid-run with nobody watching.
- Autonomy improves without touching the safety-critical layer.

### Negative
- `/define` sessions carry more questions and occasional bounces back to figure-out; upstream friction is deliberately purchased with downstream freedom.
- The triage threshold — approach-fails versus redo-work — is a judgment call and may bounce too eagerly until calibrated.
- Outcome-altitude gates demand more of verifiers than mechanism checks would; verifier prompts must name the evidence that makes an outcome judgeable.

## Source
- Related: [20260727-gate-text-changes-on-the-users-say-so](20260727-gate-text-changes-on-the-users-say-so.md)
- Related: [20260726-only-gates-bind-process-guidance-is-advisory](20260726-only-gates-bind-process-guidance-is-advisory.md)
- Related: [20260727-manifest-intent-leads-with-problem-appetite-and-bounds](20260727-manifest-intent-leads-with-problem-appetite-and-bounds.md)
