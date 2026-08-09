# ADR: figure-out budgets the whole turn, not its bold lines

## Status
Accepted

## Area
figure-out

## Context

`20260803-figure-out-turn-carries-one-concrete-claim` set the dial at claims per turn rather than words. The section that implements it states the budget in formatting terms: bold lines are "three or four at most", and the bound on prose reaches only "the prose under each bold".

Everything that is not a bold line is therefore unbudgeted — and three kinds of content live there. The closing ask, which a separate line tells to carry "the answer you would give it" with no length bound anywhere. Loose paragraphs sitting between bolds rather than under one. And reports of work performed — an inline glossary write, a recommendation delivered in passing — which read as neither findings nor claims, so "the rest of what you found waits for its own turn" does not visibly reach them.

A live session made this observable: the user's attention gave out, and in the two heavy turns the excess weight sat precisely in those unbudgeted places rather than scattered through the turn. Weight concentrating exactly where the budget does not reach is what a structural gap predicts; drift would not select for it.

## Decision

The one-claim budget covers the whole turn, not its bold lines. Bold placement remains a skimming aid rather than the unit being counted.

The ask keeps its recommendation and loses the case for it. A bare question hands the thinking back to the reader, which raises load rather than lowering it; a one-sentence answer is what makes the ask decidable.

Low cognitive load is the skill's default rather than a per-user setting. A ratified taste entry can bend it, through the standing-context hook the skill already carries — the exception path, not the home.

## Alternatives Considered

- **Persist it as a user-level taste entry**: record the preference in a memory file — Rejected by the user whose session surfaced it: the behavior belongs to everyone using the skill, and taste is the mechanism for departing from a default, not for supplying one.
- **Lower the bold-line cap**: tighten "three or four" — Rejected: it counts the wrong unit, and the observed weight was not in the bold lines.
- **Drop the ask's recommendation**: leave a bare question — Rejected: the recommendation is what makes the ask answerable in one word.

## Consequences

### Positive
- The budget now reaches where the weight actually lands.
- The ask stays decidable while getting shorter.

### Negative
- "One claim" is a judgment rather than a count, so it is less mechanically checkable than a cap on bold lines.

## Source
- Session: figure-out on ticketing-skills feedback (2026-08-09)
- Amends 20260803-figure-out-turn-carries-one-concrete-claim
- Related: 20260722-figure-out-firms-low-cognitive-load-directive, 20260727-figure-out-adopts-a-default-turn-shape
