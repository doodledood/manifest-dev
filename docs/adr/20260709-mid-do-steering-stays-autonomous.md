# ADR: Mid-/do steering stays autonomous, audited through Known Assumptions

## Status
Accepted

## Context
Mid-/do user messages default to manifest amendment via /define, and /define treats any amendment whose caller is /do as autonomous — it skips the Summary-for-Approval wait and propagates `--autonomous` to figure-out. A suite-alignment scan flagged this as a seam: a user who is present and just spoke gets an amendment that self-answers ambiguities instead of asking them. The counter-model surfaced during review: mid-run messages are not conversation openers — users say something and leave immediately, using the message as a steering mechanism.

## Decision
Mid-/do user messages are **Steering Messages**: fire-and-forget direction. Amendment stays fully autonomous even though a user triggered it — /define does not ask back, does not wait for approval, and figure-out (when needed) self-answers. The trade is interaction for audit trail: every judgment call made while encoding a steering message lands as a `(auto)`-marked item with a matching `ASM-*` Known Assumptions entry, and /do surfaces a one-line digest in chat after amending so the user sees what was assumed when they return.

## Alternatives Considered
- **Presence-keyed interactivity**: amendments triggered by a live user message ask the user when something is ambiguous and show a digest before proceeding. — Rejected: users bounce immediately after steering; questions back stall the run against nobody and defeat the mechanism.
- **Full interactive amendment**: restore the Summary-for-Approval wait for user-triggered amendments. — Rejected: reintroduces per-tweak ceremony the steering model exists to avoid.

## Consequences

### Positive
- The run keeps moving; steering costs the user one message.
- Guesses are auditable: ASM entries name what was assumed, the default chosen, and the impact if wrong — the amend-later hook.

### Negative
- A wrong guess gets built until the user notices it via the digest or ASM review; steering an ambiguous ask trades precision for speed.

## Source
- Grounding: suite-alignment review of the mid-/do amendment path (define's caller-keyed amendment autonomy and escalate's scope-change routing) against attended-use expectations.
- Related: 20260709-do-keeps-default-execution-log-manifest-stays-contract
