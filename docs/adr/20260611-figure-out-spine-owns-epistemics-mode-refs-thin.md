# ADR: figure-out's spine owns all epistemics; mode references thin to pure mechanics

## Status
Accepted

## Context

figure-out's trustworthiness methodology had drifted into mode references. `references/LOG.md` carried the only claim-provenance requirement ("Every factual claim needs provenance") — making audit discipline opt-in behind `--log`. `references/autonomous.md` restated spine behavior wholesale (its "What stays the same" section re-lists branch-walking, leverage ordering, verify-before-asserting). Both are scope-qualifier failures under the prompt-engineering boundary check: principles whose natural reach is the whole skill, gated behind flags — and restatements that drift as the spine evolves.

The operator's directive: trust must be identical in every mode; a mode reference exists only to add that mode's mechanics.

## Decision

All investigation epistemics — claim discipline, evidence handling, convergence rules — live in the figure-out spine (`SKILL.md`), mode-general. Mode references carry only the delta their mode introduces:

- **`LOG.md`** → thin persistence: where the log lives, append-only discipline, entry serialization. Its purpose is continuity (e.g., evidence surviving context compaction), not methodology — the provenance requirement moves to the spine.
- **`autonomous.md`** → thin self-answering: at each load-bearing question, answer with the recommended answer instead of waiting; surface resolutions (and low-confidence ones as Known Assumption candidates) for downstream consumers; stop when the read is named. No "what stays the same" restatement — everything not named is unchanged by definition.

## Alternatives Considered

- **Keep provenance in LOG.md**: provenance as a logging concern — Rejected: makes auditability opt-in; the ledger discipline is what makes reads trustworthy in every mode.
- **Per-mode hardening (duplicate the epistemics into each reference)**: Rejected: restatement drift is the observed failure, not a hypothetical.

## Consequences

### Positive
- Identical trust guarantees in interactive, `--autonomous`, `--team`, and `--log` runs.
- References stop drifting against the spine; each is auditable as "only this mode's mechanics."

### Negative
- The spine grows; it must absorb the methodology without becoming a checklist (calibrated under the prompt-engineering review discipline).

## Source
- Related: PR #189.
- Related: 20260611-figure-out-evidence-ledger-and-independent-rederivation; 20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass
