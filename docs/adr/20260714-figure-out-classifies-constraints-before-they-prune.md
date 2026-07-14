# ADR: figure-out classifies stated constraints before they prune options

## Status
Accepted

## Context

`figure-out` weighs every genuinely-viable option before converging, and its existence challenge (20260714-figure-out-challenge-solution-existence-before-design) makes proposed solution structure earn its place. That decision deliberately carves out "goals or constraints the user has fixed" from the challenge — and names a poorly stated constraint set as residual risk.

That carve-out leaves an unguarded path into the option set: a stated constraint is often a solution in disguise ("it must be in Redis", "we can't touch the schema", "only natural remedies"), quietly encoding an answer to an unstated problem. The spine judges elements "under the full goal and constraints", so a soft constraint prunes genuinely-viable options before deliberation starts, and the option-completeness discipline never sees what was removed. Models default to accepting stated constraints; nothing in the spine, references, or task files classifies them.

This is the sibling of the arriving-frame gap (20260714-figure-out-roots-crux-tree-above-solution-shaped-topics): the XY problem entering through a constraint rather than through the topic itself.

## Decision

Add a spine-level classify-before-prune rule to `SKILL.md`: when a stated constraint would remove genuinely-viable options and its grounding is unstated, establish what kind of claim it is — hard (owned, verified, externally imposed) or assumed (inherited, habitual, a disguised preference) — before letting it prune the option set.

The rule classifies; it does not challenge the constraint's existence. A constraint established as hard prunes exactly as before. This keeps the rule composable with the existence challenge's carve-out of user-fixed constraints rather than in conflict with it. The trigger stays silent when the constraint's grounding is already established — no ritual interrogation of constraints the user demonstrably owns.

Like the crux-root decision, this lives at spine altitude and is phrased domain-neutrally: it applies to any topic shape — code, diagnosis, research, or otherwise — not only engineering requirements.

## Alternatives Considered

- **No change; rely on "weigh every genuinely-viable option":** Rejected — that discipline operates on the option set *after* constraints prune it; it cannot see options removed upstream.
- **Extend the existence challenge to cover constraints:** Rejected — challenging whether a user-fixed constraint should exist re-litigates decisions the user owns, which the companion ADR deliberately avoided; classification (what kind of claim is this?) achieves the guard without the insubordination failure mode.
- **Task-file probes only (e.g., a CODING or FEATURE angle on soft constraints):** Rejected as the primary fix — disguised-solution constraints appear in every topic shape, so the rule belongs in the spine; task files may still add domain-specific fuel.
- **Fold into the evidence taxonomy (constraints as claims needing provenance):** Rejected — the ledger governs what a read rests on, not what prunes the option set during deliberation; overloading it would blur two distinct disciplines.

## Consequences

### Positive
- Soft constraints surface as decisions instead of silently shrinking the option set, closing the residual risk the existence-challenge ADR named.
- Hard constraints are unaffected; the user's authority over fixed goals and constraints is preserved.
- Reuses the same trigger philosophy as the crux-root rule — fires only on unestablished grounding — so no new ceremony.

### Negative
- The hard-vs-assumed call is a judgment; miscalibrated wording could read as haggling over genuinely fixed constraints. Drafting must frame it as classification, not challenge.
- One more classification the model performs during deliberation on constraint-heavy topics.

## Source
- Grounding: textual analysis of the skill's spine and task files (no constraint-classification instruction exists), corroborated by the residual-risk note in the existence-challenge ADR's Consequences.
- Related: 20260714-figure-out-roots-crux-tree-above-solution-shaped-topics
- Related: 20260714-figure-out-challenge-solution-existence-before-design
