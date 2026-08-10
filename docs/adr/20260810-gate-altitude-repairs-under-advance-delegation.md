# ADR: Gate altitude repairs run under advance user delegation

## Status
Accepted

## Area
define / do

## Context

The 2026-07-27 pair — `20260727-gate-text-changes-on-the-users-say-so` and `20260727-define-encodes-for-full-do-autonomy` — split the redundant-escalation problem in two: encoding-time discipline (gate altitude, upstream triage of load-bearing unknowns) removes avoidable escalations at the source, and gate text stays immutable to the run, so whatever survives encoding escalates. That reduced escalation volume but did not zero it, and the survivors concentrate in one shape: a gate whose criterion pins a *mechanism* the run legitimately pivoted away from, where the outcome the gate served is still met. These escalate on the run's most-constrained path, the user's ruling is usually one word, and the intent recorded in the manifest already implied it — a rubber stamp with an unattended-stall price. Per the cost asymmetry recorded in `20260727-define-encodes-for-full-do-autonomy`, that price is closer to losing development days than to the minutes the question takes.

The residual class is structural, not a calibration failure: `/define` writes gate text before execution reality exists, so some mechanism-pinning becomes visible only when a legitimate pivot actually happens mid-run. Encoding-time altitude discipline shrinks the class and cannot reach zero.

The immutability principle is "gate text changes on the user's say-so, not the run's." Nothing in it requires the say-so to be instance-by-instance, and the alternatives that ADR rejected were structural bounds — verifier-sourced-only, passing-gates-only — not a user-ratified delegation given in advance. That leaves room for a repair path that moves the say-so earlier rather than removing it.

## Decision

`/do` gains a bounded repair path for the over-concrete-gate class, exercised under user delegation granted at encoding time rather than instance-by-instance. It is default-on. Its bounds:

- **Reach.** Only a gate whose criterion execution (or a verifier's report) shows to be pinning a mechanism rather than the outcome that mechanism served. The repair raises the gate to that outcome, at the altitude of the manifest's Problem and Appetite — the same write-time test `/define` applies, applied late.
- **Raise-only.** The repaired gate must still catch the outcome the original claimed. A repair never weakens: no lowering a threshold, no narrowing a region, no dropping a gate. Threshold-wrong questions ("the bar costs more than it returns") stay on their existing path — escalation with a user present, record-and-continue without one.
- **Exclusion: the deliberately-chosen set.** Where a mechanism was deliberately chosen as the thing that must hold, that mechanism *is* the outcome and the envelope never reaches it: safety-critical invariants, criteria the user pinned by reacting to something concrete, bounds routed from Out of bounds, and gaps settled during Known Assumptions triage precisely because they must not be departed from. This is the same set `/define`'s gate-altitude discipline already protects from being raised away at write time; marking a mechanism deliberate at encoding time is the per-gate opt-out.
- **Mechanics.** The repair travels the normal autonomous amendment path (`/define` with the manifest path), so it inherits the existing audit machinery: the changed gate's verification identity changes, it returns to the ledger unverified and re-verifies like any amended gate, and the judgment lands as `(auto)`-marked items with matching `ASM-*` entries plus the post-amendment digest.

Default-on rather than opt-in per manifest, matching the precedent of `20260709-mid-do-steering-stays-autonomous`: autonomy is traded for an audit trail, and an opt-in interview question is ceremony whose default answer reproduces the stall this decision exists to remove.

Everything outside the envelope keeps instance-by-instance say-so: weakening, dropping, threshold moves, and any change to the deliberately-chosen set remain the user's alone.

## Alternatives Considered

- **Status quo — instance-by-instance say-so for all gate text**: — Rejected: observed escalations concentrate in a class whose ruling the recorded intent already implies; each one stalls an unattended run for a rubber stamp.
- **Free run-side gate amendment**: let `/do` amend any gate its own reading finds wrong — Rejected: the executor grading itself is the property gate immutability exists to remove; the narrowed ADR's core reasoning stands untouched for everything outside the envelope.
- **Opt-in per manifest**: `/define` asks once at encoding whether to grant the delegation — Rejected: adds interview ceremony whose default is the stall; the deliberately-chosen exclusion set already gives per-gate control, which is the granularity that matters.
- **Sharpen encoding-time altitude discipline instead**: — Rejected as the sole fix: the residual class is structural (gate text is written before execution reality exists), so upstream sharpening complements the envelope but cannot replace it.

## Consequences

### Positive
- The dominant observed rubber-stamp escalation class stops stalling unattended runs; the run repairs, records, and re-verifies instead of parking.
- The immutability principle survives narrowed rather than breached: the user's say-so moved to encoding time for one bounded class; the run still never acts on its own say-so.
- Repairs are auditable and checked: amendment records plus mandatory re-verification of the changed gate.

### Negative
- The misclassification risk is real and bounded, not zero: a run failing a gate could read it as "mechanism-pinning" to escape the failure. Raise-only, the exclusion set, and forced re-verification bound the damage; they do not eliminate the judgment.
- A wrong raise ships work the user audits only after the fact, through the digest and ASM trail.
- `/define` carries slightly more encoding care: the deliberately-chosen set must be recognizable in the manifest for the exclusion to hold at run time.

## Source
- Session: figure-out deliberation over redundant `/do` escalation classes, 2026-08-10
- Narrows: 20260727-gate-text-changes-on-the-users-say-so
- Related: 20260727-define-encodes-for-full-do-autonomy
- Related: 20260727-manifest-intent-leads-with-problem-appetite-and-bounds
- Related: 20260709-mid-do-steering-stays-autonomous
