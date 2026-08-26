# ADR: Sensing the output is a precondition of naming a read

## Status
Accepted

## Area
figure-out

## Context

`20260824-undiscussed-surface-sweep-lives-in-read-naming-checkpoint` fixed one way a read reaches its end while the user is still going to be disappointed: ground the session never brought into view. Its mechanism is an enumeration — before naming a read that implies making something, list the surfaces the user will see, touch, or judge that the conversation never touched, and give each a fate.

A second way survives that fix. A thorough session can discuss ground at length, reach apparent agreement on it, and still diverge — because prose underdetermines. A sentence both parties accept admits many concrete realizations, and each fills in a different one without noticing. The maintainer met this directly: after a very thorough session had converged, rendering what the read implied surfaced several genuine disagreements on ground the session had already covered. Enumeration cannot catch this, because nothing was missing from the conversation.

The skill's own confidence discipline already says apparent alignment buys nothing while load-bearing fog sits unexplored. It says it about fog. It does not say it about agreement reached in prose, which is the case here.

Instantiating also pays before anyone reacts: committing to one concrete realization forces the agent to settle details its prose left open. This session demonstrated it five times, four of them errors the agent found in its own draft while making it concrete.

## Decision

Naming a read gains a third precondition, beside the two the checkpoint already carries (no open crumb, high-stakes ground scouted): **where a read implies making something, the output must have been stated exactly, and a rendering of it offered.**

The two halves are not equally binding, and that asymmetry is the decision:

- **Stating is owed.** It is what forces the agent to be concrete, and it is what a vague read hides behind. It requires no counterparty, so it holds in autonomous and unattended runs too.
- **Rendering is offered, never pushed.** The user's yes produces it, exactly as a UI mock has always worked. A declined offer is an answer: the read lands, with the unsensed part named as an accepted default. Not offering is the failure the precondition exists to prevent.

A read that implies no artifact has no output to state this way and skips the precondition, on the same carve-out the surface sweep already uses. The condition inherits the checkpoint's existing scaling language, so it stays proportional to what rides on the read.

With no user to offer to, an unattended run states the output exactly and renders nothing — it still gets the concreteness stating forces, and skips an artifact it has no reader for.

## Alternatives Considered

- **Leave it an offer, with no precondition on naming**: — Rejected as the whole fix. An offer the agent may skip is skipped exactly when the session feels aligned, which is the condition this addresses. Preserving user control does not require agent discretion: the gate binds the agent to ask, and the user keeps the veto.
- **Widen the existing surface-sweep line a second time**: — Rejected. That line enumerates ground; this produces a statement and an offer. Two acts, and the sweep line already carries two clauses.
- **Require the artifact, not just the offer**: — Rejected. It pushes token-heavy work onto every making-shaped read regardless of whether the user wants to look, and the maintainer's ruling is explicit that these are offered like a UI prototype rather than imposed.
- **Fire only at read-naming, never earlier**: — Rejected. The goal is to find disagreement where changing costs least, and earlier is cheaper; the precondition is the backstop, not the main event.

## Consequences

### Positive

- The failure mode the 2026-08-24 record could not reach — discussed, apparently agreed, actually divergent — now has a mechanism, at the one checkpoint every session passes.
- Reactions to a rendering are already binding downstream: `/define` encodes criteria the user pinned by reacting to something concrete as Acceptance Criteria or Global Invariants, so what this surfaces reaches execution without new machinery.
- Autonomous runs gain the instantiation benefit without producing artifacts nobody reads.

### Negative

- The read-naming checkpoint grows a third condition, and its proportionality now rests on the section's scaling language holding for all three.
- Every making-shaped read costs at least one statement and one offer, including reads where the user would rather just have the answer.
- Reactions to renderings bind as gates downstream, so more rendering means more chances a stray reaction becomes an Acceptance Criterion.

## Source
- Session: figure-out investigation of whether prototyping generalizes past UI (2026-08-26). Investigation log at `~/.manifest-dev/logs/figure-out-log-20260826-115243.md`.
- Related: [20260824-undiscussed-surface-sweep-lives-in-read-naming-checkpoint](20260824-undiscussed-surface-sweep-lives-in-read-naming-checkpoint.md) — extends its checkpoint from ground never discussed to ground discussed and only apparently agreed
- Related: [20260826-prototyping-and-scratch-are-one-mechanism](20260826-prototyping-and-scratch-are-one-mechanism.md) — the mechanism this precondition invokes
- Related: [20260727-gate-text-changes-on-the-users-say-so](20260727-gate-text-changes-on-the-users-say-so.md)
