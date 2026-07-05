# ADR: Progressive-disclosure triggers live in the loading layer, never in the deferred reference

## Status
Accepted

## Context

A figure-out audit of the figure-out skill found that docs mode eagerly loads all of `references/ADR_FORMAT.md` (172 lines): `WITH_DOCS.md` instructs "The ADR gate, format, lifecycle … live in the adjacent `ADR_FORMAT.md` — read it." The gate must be checked after every user turn, so placing it inside the deferred file forces the whole file into context at mode start — the deferral buys nothing. Only ~30 of those lines (decision-worthiness categories, Decision Test, anti-patterns) are needed per-turn; the rest (template, naming, lifecycle, immutability, cross-references) earns its place only when an ADR is actually written.

The operator named the general rule the instance violates: a deferred reference must not carry its own trigger, because a trigger inside the reference can only be evaluated after the load it was meant to gate.

A repo sweep confirmed this is the lone violation: `define`'s references are all flag-gated from its `SKILL.md`; the legacy `/adr` skill loads its `ADR_FORMAT.md` copy eagerly but its invocation *is* the trigger (writing ADRs is its whole job); `team.md` pointing to `slack-mrkdwn.md` is legitimate *nested* disclosure — the trigger it holds gates a further reference, not itself.

## Decision

Any condition that must be evaluated before or without loading a reference — a load trigger, a per-turn decision gate — lives in the loading layer (the entry prompt or an already-active reference). Deferred references carry only post-trigger mechanics.

Corollaries:

- **Nested disclosure is fine**: an active reference may hold the trigger for a *further* reference.
- **Invocation-as-trigger is fine**: a skill whose entire job begins at invocation may load its references eagerly.

First application (to be executed as a separate change): move the ADR gate criteria into `figure-out/references/WITH_DOCS.md`; slim `ADR_FORMAT.md` to write-time mechanics loaded only when an offer is accepted. Ripple: `ADR_FORMAT.md`'s "Gate (unified across capture paths)" section currently claims the gate lives there for both capture paths — reword it so the gate's criteria stay unified in substance while the inline path reads them from `WITH_DOCS.md`; the legacy `/adr` copy legitimately keeps its inline gate.

The Progressive Disclosure entry in `CONTEXT.md` was sharpened to carry this rule.

## Alternatives Considered

- **Keep the gate inside `ADR_FORMAT.md` with the eager "read it"**: Rejected — defeats the deferral; ~100 always-loaded lines earn their place only at write time, and docs mode is default-on so every session pays.
- **Duplicate the gate in both `WITH_DOCS.md` and `ADR_FORMAT.md`**: Rejected — restatement drift between spine and references is this skill's documented failure mode (see spine-owns-epistemics ADR).
- **Load `ADR_FORMAT.md` lazily but leave the gate inside it**: Rejected — the per-turn check would then run gateless until the first load, which is the trigger-in-reference contradiction restated.

## Consequences

### Positive
- Docs mode's per-turn footprint drops by the write-time bulk of `ADR_FORMAT.md`; deferral becomes real.
- The rule generalizes: future reference splits can be audited with one question — "can this file's trigger be evaluated without loading it?"

### Negative
- Gate criteria and write-time mechanics live in separate files; edits to the gate now touch `WITH_DOCS.md` while format edits touch `ADR_FORMAT.md`.
- The "unified gate" phrasing weakens to unified-in-substance across the inline and post-hoc capture paths (drift already accepted by the existing duplication note).

## Source
- Related: PR #214.
- Related: 20260611-figure-out-spine-owns-epistemics-mode-refs-thin; 20260703-figure-out-fog-discipline
