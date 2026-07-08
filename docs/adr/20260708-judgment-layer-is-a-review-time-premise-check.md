# ADR: The judgment layer is a review-time premise check, distinct from define's gates

## Status
Accepted

## Context

Automated code review has been defect-finding on a concrete change: the `review-code` dimension fleet audits a diff for bugs, design, simplicity, and so on, taking the change's *intent as given*. Its actionability filters deliberately drop any finding the author chose intentionally — the fleet verifies a settled intent, it does not challenge it.

A distinct capability sits above that: the **judgment layer**, which questions whether a change earns its keep against the pain it solves — is it necessary, is the pain real and stated, is the approach the right one, is the added surface proportionate. This is premise-questioning, not defect-finding.

Introducing it forced a placement decision across the figure-out → define → do → review surfaces: where does premise-questioning belong, and how does it relate to the acceptance gates that `/define` produces and `/do` verifies? Two surfaces were candidate homes beyond review — `/define` (encode a "necessity" gate) and `/do` (check the premise during execution, escalating on a miss to catch an upstream understanding error before the change is fully built).

## Decision

Premise-questioning lives at **review time**, as the judgment layer, and nowhere else. Three surfaces carry three distinct trust roles:

- **Define's acceptance gates** (Acceptance Criteria, Global Invariants) verify that a produced change meets the *agreed spec*. They assume the premise is correct — they cannot question it, because a gate verifying its own premise is circular. Blocking (a FAIL stops `/done`).
- **The defect fleet** (review) finds defects in the concrete change, independent of premise. Blocking per each dimension's severity threshold.
- **The judgment layer** (review) questions the *premise itself* — the only surface that does. Non-blocking: each finding is an author-answerable question, never a gate. Evidence-gated and pitched at whole-PR altitude.

Premise-questioning is **not** a define gate and **not** a `/do` step:

- A define gate presupposes the premise it would have to interrogate; it cannot verify what it assumes.
- `/do` is a faithful executor. The manifest is authority; premise and scope concerns route *out* — to a `/define` amendment or to `/escalate` — and `/do` never silently re-decides the premise.
- The judgment layer's evidence requires the *concrete artifact* (an already-existing capability to point at, added surface with no consumer, a nameable simpler solution). That artifact exists only once execution is complete — which is review's moment. There is no execution-time window that is not either pre-artifact (nothing concrete to judge) or post-artifact (duplicating review).

A premise miss originating in an upstream understanding step is still caught two ways: **proactively** by the judgment layer inspecting the concrete change at review, and **reactively** by `/do` routing any premise problem that surfaces during execution to amendment or escalation.

## Alternatives Considered

- **Premise-check inside `/do` (execution time)**: run the judgment layer while executing, escalating on a miss to catch it before the change is fully built — Rejected: contradicts `/do`'s faithful-executor contract (the manifest is authority; `/do` does not re-decide the premise), and the layer's evidence needs the built artifact, so there is no useful execution-time window that is not pre-artifact or a duplicate of review.
- **A "necessity" define gate**: encode premise-questioning as an Acceptance Criterion — Rejected: a gate assumes the premise it would need to question (circular), and it would be blocking, whereas premise questions must stay non-blocking.
- **A standalone premise pass invocable from any surface**: Rejected for placement — only the review surface has both the concrete artifact and the stated pain present together, so "any surface" collapses to review anyway while re-importing the execution-time problems above.

## Consequences

### Positive
- A clear, durable trust boundary: acceptance gates verify spec-conformance, the defect fleet finds defects, the judgment layer questions worth. Each surface keeps exactly one job.
- `/do` stays a lean faithful executor with no premise second-guessing loop.
- Premise questions stay non-blocking, so they never corrupt the acceptance contract or a merge decision — they inform the author without gating.

### Negative
- A change executed by `/do` that never passes through any review surface receives no premise check. Accepted: such a flow also forgoes the entire defect fleet, so it is a "no review happened" gap rather than one specific to the judgment layer.
- Premise-questioning happens after the artifact is built, not before. The earliest-possible (pre-build) catch is deliberately forgone to keep `/do` faithful and to keep the check grounded in concrete evidence rather than speculation.

## Source
- Related: See also 20260606-figure-out-process-trust-vs-define-do-artifact-trust
