# ADR: The judgment layer is a review-time premise check, distinct from define's gates

## Status
Accepted

## Context

Automated code review has been defect-finding on a concrete change: the `review-code` dimension fleet audits a diff for bugs, design, simplicity, and so on, taking the change's *intent as given*. Its actionability filters deliberately drop any finding the author chose intentionally — the fleet verifies a settled intent, it does not challenge it.

A distinct capability sits above that: the **judgment layer**, which questions whether a change earns its keep against the pain it solves — is it necessary, is the pain real and stated, is the approach the right one, is the added surface proportionate. This is premise-questioning, not defect-finding.

Introducing it forced a placement decision across the figure-out → define → do → review surfaces: where does premise-questioning belong, and how does it relate to the acceptance gates that `/define` produces and `/do` verifies? Two surfaces were candidate homes beyond review — `/define` (encode a "necessity" gate) and `/do` (check the premise during execution, escalating on a miss to catch an upstream understanding error before the change is fully built).

Review is an optional stage, not a guaranteed one. For a change important enough to warrant it, the lifecycle adds an async review session (review-pr) that posts to the PR (figure-out → `/define` → `/do` → review). This optionality is not a gap to close but a property that fits the decision: a non-binding, human-facing judgment should scale with how much the change merits scrutiny, rather than run on every change — so reserving it for the review stage, invoked when warranted, is correct rather than deficient.

## Decision

Premise-questioning lives at **review time**, as the judgment layer, and nowhere else. Three surfaces carry three distinct trust roles:

- **Define's acceptance gates** (Acceptance Criteria, Global Invariants) verify that a produced change meets the *agreed spec*. They assume the premise is correct — they cannot question it, because a gate verifying its own premise is circular. Blocking (a FAIL stops `/done`).
- **The defect fleet** (review) finds defects in the concrete change, independent of premise. Blocking per each dimension's severity threshold.
- **The judgment layer** (review) questions the *premise itself* — the only surface that does. Non-blocking: each finding is an author-answerable question, never a gate. Evidence-gated and pitched at whole-PR altitude.

Premise-questioning is **not** a define gate and **not** a `/do` step. The decisive reason is the nature of the manifest itself:

- **The manifest is the binding acceptance contract.** Every Acceptance Criterion is a gate whose FAIL stops `/done`, and `/do` is the autonomous engine that exists to satisfy those gates. A premise question is definitionally *not* a completion condition: "is this necessary?" legitimately resolves as "yes, still wanted" — a human judgment no engine can adjudicate. It therefore cannot be made a binding gate (doing so would halt every PR waiting on a routine "yes"), which means it cannot be a manifest Acceptance Criterion — a non-binding AC is a contradiction — which means `/do` has no gate to satisfy by running it. Premise-questioning is inherently reviewer-nature: a non-binding judgment surfaced to a human. Its only coherent home is review, the surface built to surface judgments; it has no place in the binding-gate world of the manifest and `/do`.
- A define gate additionally presupposes the premise it would have to interrogate; it cannot verify what it assumes.
- `/do` additionally remains a faithful executor: the manifest is authority, and premise or scope concerns route *out* — to a `/define` amendment or to `/escalate` — rather than being silently re-decided.
- The judgment layer's evidence also requires the *concrete artifact* (an already-existing capability to point at, added surface with no consumer, a nameable simpler solution), which exists only once execution is complete — review's moment. There is no execution-time window that is not either pre-artifact (nothing concrete to judge) or post-artifact (duplicating review).

A premise miss originating in an upstream understanding step is still caught two ways: **proactively** by the judgment layer inspecting the concrete change at review, and **reactively** by `/do` routing any premise problem that surfaces during execution to amendment or escalation.

## Alternatives Considered

- **Premise-check inside `/do` (execution time)**: run the judgment layer while executing — as a non-blocking surface at completion, or escalating on a miss — to catch necessity/surface issues that only surface once reality is contacted during implementation, and because `/do` is the reliably-run surface while review is sometimes skipped — Rejected: `/do` is a binding-gate engine, and a non-blocking premise question is not a completion condition, so it has no gate to satisfy there; making it binding would halt every PR on a routine "yes." That a non-binding judgment is optional (run review when you want it) is correct, not a defect — the fix for wanting it reliably is to make the review stage reliable, not to put advisory work in the binding engine. The implementation-time insight still surfaces, at review, against the concrete artifact.
- **A "necessity" define gate**: encode premise-questioning as an Acceptance Criterion — Rejected: a gate assumes the premise it would need to question (circular), and it would be blocking, whereas premise questions must stay non-blocking.
- **A standalone premise pass invocable from any surface**: Rejected for placement — only the review surface has both the concrete artifact and the stated pain present together, so "any surface" collapses to review anyway while re-importing the execution-time problems above.

## Consequences

### Positive
- A clear, durable trust boundary: acceptance gates verify spec-conformance, the defect fleet finds defects, the judgment layer questions worth. Each surface keeps exactly one job.
- `/do` stays a lean faithful executor with no premise second-guessing loop.
- Premise questions stay non-blocking, so they never corrupt the acceptance contract or a merge decision — they inform the author without gating.

### Negative
- A change that never passes through any review stage receives no premise check. This is the accepted cost of keeping the check non-binding and optional: skipping review also forgoes the entire defect fleet, so it is a "no review chosen" consequence, not a gap specific to the judgment layer.
- Premise-questioning happens after the artifact is built, not before. The earliest-possible (pre-build) catch is deliberately forgone to keep `/do` faithful and to keep the check grounded in concrete evidence rather than speculation.

## Source
- Related: See also 20260606-figure-out-process-trust-vs-define-do-artifact-trust
