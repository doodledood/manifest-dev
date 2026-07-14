# ADR: figure-out keeps the do-nothing option in the option set

## Status
Accepted

## Context

`figure-out`'s option-completeness rule ("weigh every genuinely-viable option before converging, and let an option leave the set only when evidence removes it") never names the option of not solving the problem at all. Once a problem is established, deliberation carries solving momentum: the user arrived wanting to act, and recommending inaction reads as unhelpful, so models suppress the do-nothing option even when it wins on evidence. Nothing in the spine, references, or task files puts it in the set.

This is distinct from two adjacent rules. The existence challenge ("do we need this element at all?") operates on elements of a solution already being designed — one level below "should we intervene at all". The status-quo job test asks what job the existing state does when a read implies changing it — a different question from whether intervening is worth its cost even granting the problem is real.

## Decision

Extend the option-set-completeness sentence in `## Serving what's true`: once a problem is established, the option set includes not solving it — living with the cost is a real option, priced on the same evidence as any other option, and recommending it is a full answer, not a failure to deliver. It leaves the set the way every option does: on evidence.

Load-bearing wording properties:

- **Trigger scope** — "once a problem is established" prevents the option from firing as contrarian ceremony on topics that aren't problems (diagnoses, research questions).
- **Priced, not recited** — the option is weighed on evidence like any rival, blocking the ritual "we could also do nothing, but—" strawman; eviction requires evidence per the host sentence.
- **Suppression counter** — naming inaction as a legitimate full answer removes the model-side inhibition against recommending it.
- **Distinct vocabulary** — "living with the cost" rather than status-quo language keeps it lexically separate from the status-quo job test; on remove/change topics the two can both fire (do-nothing = keep the thing), which is benign because they are differently grounded (cost-benefit vs. purpose).
- **Mode propagation** — placement upstream of the section's "this completeness holds in every mode" clause carries the option into autonomous runs, where solving momentum is strongest.

## Alternatives Considered

- **No change; read "every genuinely-viable option" as already including do-nothing:** Rejected — models under solving momentum do not volunteer inaction, and no text names it; an unnamed member of the set is one that never gets weighed.
- **Graft onto the existence challenge in the loop:** Rejected — that machinery fires on solution elements mid-design; "should we intervene at all" is one level up and belongs where the option set is defined.
- **Place in the solution-shaped-topic rule:** Rejected — the do-nothing option applies to every established problem, not only topics that arrived solution-shaped.

## Consequences

### Positive
- The strongest senior-practitioner move after problem establishment — pricing inaction — becomes part of every deliberation's option set, in every mode.
- Existing anti-pre-slant language ("never because it's disfavored or cuts against what the user seems to want") automatically protects the option from eviction pressure when the user visibly wants to build.

### Negative
- Risk of calcifying into boilerplate (a reflexive do-nothing mention per problem); the skill's ceremony bans push against this, but only observed sessions confirm calibration.
- The host sentence grows longer, slightly diluting the salience of its existing clauses.

## Source
- Grounding: textual analysis of the spine (no line names the null option), corroborated by an independent re-derivation from evidence with the conclusion withheld, which converged on the same placement and guards.
- Related: 20260714-figure-out-roots-crux-tree-above-solution-shaped-topics
- Related: 20260714-figure-out-scales-read-depth-with-stakes-and-reversibility
