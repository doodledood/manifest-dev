# ADR: The bet is about the practice, not about whether a market adopts it

## Status
Accepted

## Area
Positioning

## Context
The Diagnosis carries one sentence naming the project's stop condition — the claim whose falsity
means pivot or stop, as distinct from an assumption whose falsity kills one lane. It read that
developers who care about quality will adopt workflows spending more tokens and more up-front
process to get output they can ship with minimal review.

That is a claim about a market. When the unit moved from the task to the project on 2026-08-20,
the sentence was deliberately left in place rather than rewritten alongside, on the grounds that
the owner had ruled the barrier text and not the bet, and that inventing a replacement would be
the silent position change the update asymmetry forbids. It was recorded as a visible seam.

Ruling Winning on 2026-08-21 made the seam a contradiction rather than a lag. Winning is our own
projects running end-to-end on all three tiers, with outside recognition welcome as a consequence
and never a target. Under that definition the market claim no longer names a risk the project
carries: if no developer outside ever adopts these workflows, the project still wins. A stop
condition that cannot stop anything is worse than none, because it occupies the one slot reserved
for the thing actually worth watching.

## Decision
The bet sentence becomes a claim about the practice: that spending more tokens and more up-front
process — on understanding, on what is worth doing next, and on what done means — leaves a project
better off than moving faster without them.

If that is false, the whole suite is ceremony and the right response is to stop, which is the
height the field requires. It is also testable by the owner alone, without any outside adopter,
which is what makes it a stop condition this project can actually reach.

The narrower line in `What this rests on` — that understanding-first workflows produce fewer
reworked results than direct prompting — stays where it is. The overlap with the bet is now
deliberate: it is the measurable fragment of a claim the bet makes in full.

## Alternatives Considered
- **Leave the bet at the market claim**: Rejected — it names a risk the project no longer carries,
  and the Winning ruling is what changed that. Leaving it would keep the document's most load-
  bearing sentence describing a project that stopped existing.
- **Delete the bet sentence entirely**: Rejected — the conventions reserve the first two fields for
  positions whose falsity means pivot or stop, and a Diagnosis with no stop condition cannot be
  checked against anything.
- **Promote the `What this rests on` line to be the bet**: Rejected — it is the narrower, testable
  fragment, and promoting it would lose the up-front-cost half of the claim that is the actual
  wager. Keeping both, at their two heights, is what this decision preserves.
- **Fold this into the positioning record written the same day**: Rejected — 20260820-the-project-
  is-the-unit-not-the-task explicitly reserved the bet sentence for its own ruling rather than a
  rewrite alongside, and honoring that means a visible record rather than a paragraph inside a
  broader one. The two are also independently reversible.

## Consequences

### Positive
- The stop condition is now reachable: it can be judged from the owner's own projects, with no
  outside adopter required.
- The seam the 2026-08-20 record left open is closed, and closed by a ruling rather than by drift.
- The Diagnosis reads as one claim throughout, at the project unit, rather than a project-unit
  problem with a task-unit wager attached.

### Negative
- "Leaves a project better off" is harder to falsify than an adoption claim, which would at least
  have failed visibly; the risk is a bet that never quite comes due.
- The project now records no wager at all on whether anyone else would want this, so an outside
  failure would carry no stated consequence.

## Source
- Session: figure-out on positioning and the documentation rewrite, 2026-08-21; owner's ruling on
  the bet sentence, taken separately from the field rulings in the same session.
- Related: 20260820-the-project-is-the-unit-not-the-task (which reserved this sentence for its own
  ruling), 20260821-winning-is-our-own-projects-running-the-full-loop, 20260821-positioning-drops-the-conversion-funnel
