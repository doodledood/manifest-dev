# ADR: Ticket selection minimizes delay loss across the available executors

## Status
Accepted

## Area
Ticketing

## Context

The default Ticket priority is currently a fixed `urgent → unblocking → impact → cheap` order. `next-ticket` also chooses an effort before it chooses a Ticket, preferring an effort already in flight and otherwise judging which effort matters most. `sweep-tickets` uses the same store priority after first limiting its candidate set to unattended Auto work.

That shape is simple, but it mixes several proxies for the actual scheduling objective. Urgency is value lost because an outcome arrives later. Unblocking matters only to the extent that valuable downstream work actually starts later. Impact describes value created, but not how much of that value disappears when delivery waits. Cheap work matters only when its shorter completion changes the loss imposed on other work. A hard ordering can therefore prefer an urgent low-loss item over a much larger bottleneck, count many low-value dependents above one decisive dependent, or hide the best Ticket inside an effort that lost the effort-first choice.

The executor model also changed. `next-ticket` is primarily a human-facing selector, but the human is not expected to implement software unaided. The person and AI work interactively on the parts that need human knowledge, taste, or authority; once those decisions are closed, AI can usually carry implementation and verification. `sweep-tickets`, by contrast, spends unattended agent capacity and may only select Tickets carrying the Auto grant. Auto is therefore executor eligibility and authority, not intrinsic Ticket value.

Traditional software-size intuition is a poor duration proxy in that environment. Work that historically sounded like days of engineering can often complete in one agent run, while integration, external waits, migrations, slow checks, and human decisions can still dominate elapsed time. Encoding fixed human-era estimates or a fixed speedup would make the policy stale as agent capability changes.

## Decision

**Ticket selection optimizes expected project value preserved by acting now.** Among the strongest feasible candidates, compare the competing orderings directly: if A runs first, what expected project value is lost while B waits for A's relevant constrained resource; if B runs first, what is lost while A waits? Prefer the lower-loss allocation or ordering.

Delay loss includes all material consequences of receiving the outcome later:

- ongoing or expiring harm, including incidents, deadlines, security exposure, and perishable opportunities;
- durable benefit that starts later, including user value, growth, compounding, and recurring cost reduction;
- downstream work whose earliest useful start actually moves because this Ticket waits; and
- information whose later arrival delays or worsens a material downstream decision.

These are causes of delay loss, not priority classes. Do not add their full values as independent scores when they describe the same consequence, and do not persist numerical priority fields merely to make the judgment look precise.

**`next-ticket` allocates the human-plus-AI session.** Unless the conversation explicitly scopes an effort or the store declares an intentional effort order, consider ready Tickets across efforts together, using each effort's destination to judge project consequence. Account for alternative unattended capacity: similarly valuable work that genuinely needs human interaction usually beats Auto work that `sweep-tickets` can take without meaningful delay, but non-Auto never receives a hard priority. An Auto Ticket still wins when leaving it to unattended capacity would lose more project value.

For `next-ticket`, the scarce human duration is the expected interactive attention needed before the human-dependent uncertainty or authority is resolved. Do not charge the human for routine implementation that AI can continue after that point. Continuity with an effort already in flight is only a tiebreak when the expected delay-loss difference is not material; structural continuity belongs in dependency edges.

**`sweep-tickets` keeps recovery first.** Recovery of an interrupted automation-owned Ticket is lifecycle correctness rather than new-work prioritization. When starting new work, limit the candidate set to ready Auto Tickets that pass configured filters, then apply the same delay-loss objective within that eligible set.

**Duration is executor-native and current.** Estimate only the serial time on the resource whose occupation makes another candidate wait: human interactive attention for human-dependent work, or current agent end-to-end execution and landing time for unattended work. Do not infer days from traditional feature size and do not apply a fixed agent speedup. When plausible runtimes are all short relative to the value consequences, treat duration as effectively equal. Let a shorter run change the choice only when the difference is material; otherwise it is a tiebreak.

Auto and Type remain orthogonal Ticket facts. Type is never a priority input. Auto may affect `next-ticket` only because it changes which executor can take the work; `sweep-tickets` still requires it as an eligibility boundary.

## Alternatives Considered

- **Keep `urgent → unblocking → impact → cheap`**: Preserve a small deterministic rule. — Rejected because the categories can conflict with their own economic purpose; urgency, unblocking, and impact are different causal paths to delay loss rather than a justified absolute ordering.
- **Use a numeric WSJF/RICE-style score**: Divide estimated value or cost of delay by estimated effort. — Rejected because the useful scheduling insight does not require invented precision, and human-era effort estimates are especially unstable for agent-executed software work.
- **Always prefer non-Auto in `next-ticket`**: Reserve human attention for work automation cannot take. — Rejected because an Auto Ticket can still have enough time-sensitive loss that waiting for unattended capacity is the worse allocation.
- **Keep effort-first selection for continuity**: Finish one effort before comparing globally. — Rejected because a locally coherent queue can conceal a much larger delay loss in another effort; explicit effort scope remains available when concentration is itself intentional policy.
- **Choose highest lifetime impact**: Work on the biggest eventual outcome first. — Rejected because sequencing depends on what is lost by waiting, not only on the total value of eventually doing the work.

## Consequences

### Positive
- Urgency, bottlenecks, compounding impact, and information work compete on the consequence they actually impose rather than on fixed labels.
- `next-ticket` and `sweep-tickets` share one project-value objective while respecting their different executor constraints.
- Faster agents automatically make traditional size matter less without changing constants or score bands.
- A high-value Ticket in another effort can win without inventing cross-effort priority metadata.
- The store stays prose-first; the picker explains its comparison instead of persisting speculative scores.

### Negative
- Two competent runs can disagree when the evidence does not clearly separate candidates; the why-line becomes part of the auditability contract.
- A global ready-set comparison can require reading more effort destinations than effort-first selection.
- Executor duration and alternative-capacity judgments can be uncertain, so the policy must avoid pretending small estimated differences are meaningful.

## Source
- Session: figure-out on project Ticket prioritization, 2026-08-14
- Supersedes 20260809-next-ticket-derives-its-pick-instead-of-asking
- Related: 20260810-next-ticket-claims-the-ticket-it-picks, 20260810-auto-is-an-opt-in-grant-to-unattended-automation, 20260812-scheduled-ticket-sweep-is-recovery-first-and-one-ticket, 20260812-run-ticket-owns-attempt-not-dispatch
