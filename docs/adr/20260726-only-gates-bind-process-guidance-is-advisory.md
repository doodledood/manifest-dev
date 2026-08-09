# ADR: Only gates bind; Process Guidance is advisory

## Status
Accepted

## Area
do

## Context

`20260709-process-guidance-is-binding-but-unverified` made Process Guidance a binding constraint on execution: items that "must hold throughout a /do run even though no verifier checks them". The reasoning was that `/define` routes user-pinned but hard-to-verify success criteria into Process Guidance, so an advisory layer would silently drop them.

That reading puts two rules in `/do` that cannot both hold. `/do`'s termination condition states that a fresh independent PASS on every Acceptance Criterion and Global Invariant is **necessary and sufficient** for done. In the state where every gate passes and a Process Guidance item is known to be unmet, the sufficiency rule says stop and the binding rule says continue. The collision sits at the workflow's terminal decision, which is the worst place for an ambiguity.

Making Process Guidance binding also asks it to do something it structurally cannot. A binding rule that nothing evaluates has no way to hold anything open — no verifier reports it, no ledger tracks it, no verdict blocks `/done`. Its bindingness rests entirely on the executor's self-assessment, which is the failure mode inline verification exists to eliminate. Calling an unenforced layer binding does not make it enforced; it only makes the contract inconsistent about what the run owes.

## Decision

**Acceptance Criteria and Global Invariants are the only binding layer.** Gates are what the run owes and the only thing that can hold it open.

**Process Guidance is advisory** — recommendations on how to work, which `/do` weighs and may depart from when the work is better for it, naming the departure on whichever path the run exits by — completion summary, escalation payload, or pending summary — and in the Execution Log too when one is kept. The terminal-path obligation is what keeps the layer safe: the Execution Log is optional under `--no-log`, so a rule resting on it alone would let a departure surface nowhere. This makes the layer's authority match its enforcement, and it removes the collision with the termination condition: a state where all gates pass and a Process Guidance item was set aside is a legitimate completion with a visible departure, not a contradiction.

The routing gap the superseded ADR identified is closed at the encoder instead of by inflating the layer. `/define` now routes criteria the user pinned by reacting to something concrete to an **Acceptance Criterion or Global Invariant**, never to Process Guidance. Difficulty of verification is treated as a prompt-authoring problem rather than grounds for demotion: a verifier subagent can judge qualitatively — checking a result against a named reference is a legitimate gate — so a pinned criterion becomes a judgment-based gate rather than an unenforced note. Anything that must hold belongs in a gate; if it cannot be written as one, that is information about the criterion, not a reason to record it in a layer nothing checks.

`CONTEXT.md`'s glossary entry is updated to match, including its _Avoid_ list, which previously steered writers away from exactly the words that now describe the layer correctly.

## Alternatives Considered

- **Keep Process Guidance binding and scope the sufficiency rule to verification only**: reword the termination condition to "sufficient for *verification*", with a separate obligation to repair known-unmet Process Guidance before `/done` — Rejected: it resolves the textual contradiction but keeps a binding obligation whose satisfaction is self-assessed, which is the property `/do` exists to avoid. It also leaves the executor holding two classes of obligation with different enforcement, which is the complexity the single-binding-layer rule removes.
- **Keep both layers binding and add verifiers for Process Guidance**: promote every PG item to something checkable — Rejected: it erases the distinction between the layers entirely. The value of a non-gate layer is that it can carry advice too diffuse to gate; requiring a verifier for each item either forces artificial gates or empties the section.
- **Leave Process Guidance binding and accept the collision as an edge case**: rely on the executor to resolve two rules sensibly when they conflict — Rejected: the conflicting state is not exotic. Any run that weighs a process recommendation against the work reaches it, and it arrives precisely when the run is deciding whether to stop.
- **Route pinned criteria to a new binding-but-unverified section of their own**: preserve a dedicated home for must-hold-unverifiable criteria — Rejected: it reproduces the same structural problem under a new name, and adds a manifest section to do it.

## Consequences

### Positive
- `/do`'s termination condition is unambiguous: gates decide, and a fresh PASS on all of them ends the run. (Refined subsequently: a PASS whose criterion is itself under challenge is not a settled PASS, and routes to `/escalate` rather than completing — see the gate-text ADR below. Gates still decide; what changed is when a PASS counts as one.)
- The manifest's authority structure matches its enforcement structure — the layer that binds is the layer that is checked.
- Criteria the user pinned by reacting to something concrete land in gates, so they are actually verified rather than recorded in a layer nothing evaluates. This is stronger protection than the superseded ADR provided.
- Task-file Defaults, which flow into Process Guidance with light review, can no longer dictate execution — the concern the superseded ADR set aside as handled only by user review at approval time. This holds for quality defaults; a Default whose violation would be unsafe or irreversible (secrets, untrusted input, destructive actions) is carved out at the encoder and routed to a Global Invariant instead, because an advisory safety rule is not a safety rule.

### Negative
- Advice genuinely worth holding but genuinely unverifiable now has no binding home. This is deliberate: the alternative was an obligation nothing could enforce, and every run-exit surface names its departures so the user can see them.
- `/define` carries more encoding load — a pinned criterion that resists verification must be written as a judgment-based gate rather than dropped into Process Guidance, which is more demanding than the previous routing.
- Manifests written under the superseded reading treat their Process Guidance as binding. They still execute; their PG items are now weighed rather than enforced, which may be a behavior change for a manifest that relied on the stronger reading.

## Source
- Refined by: [20260727-gate-text-changes-on-the-users-say-so](20260727-gate-text-changes-on-the-users-say-so.md)
- Supersedes: [20260709-process-guidance-is-binding-but-unverified](20260709-process-guidance-is-binding-but-unverified.md)
- Related: [20260722-state-verification-sufficiency-not-only-necessity](20260722-state-verification-sufficiency-not-only-necessity.md)
- Related: [20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty](20260726-deliverables-are-exercisable-slices-ordered-by-uncertainty.md)
