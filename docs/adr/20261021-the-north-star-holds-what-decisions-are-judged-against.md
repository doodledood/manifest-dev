# ADR: The North Star holds what decisions are judged against, and chosen options live in decision records

## Status
Accepted — amended by 20261021-the-north-star-opens-with-its-end-and-signposts-reopen-choices-and-deferred-work: the *Purpose* opens with the end, and the strategy list shows each title with its signpost; amended by 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance: assignment scope, delegated decisions and retained acceptance

## Area
North Star

## Decided by
The user, who accepted the form and its line test from a rendered draft and asked for the change to be made and merged; the agent run wrote the wording of the shipped conventions and of this repository's reshaped `NORTH_STAR.md`, whose lines await the owner's ruling one by one.

## Context
The North Star was meant to give every session a base to decide from: what the project is for, what guides its decisions, and the purpose that keeps work from drifting. North Stars written under the nine-field form kept filling with concrete detail instead. In a private project that uses the form, the money field grew about fourfold in seven weeks and the field holding the project's bets about threefold, while the diagnosis, the audience and the winning definition stayed near their first size. The fields that grew had absorbed owner rulings on prices, limits, channels and sequencing. About twenty commits touched the document in those seven weeks, most of them feature changes, and each new ruling made the position that held the old one false, so the next change rewrote it again.

The cause sat in manifest-dev, not in that project. The form asked for chosen options — the option a decision picks, as against what it is judged by: the money field asked for "the mechanism and price", and the context-file wiring a project installed described the North Star as holding owner decisions. figure-out's one write step wrote any ruling that touched a position into that position. The conventions' rule against concrete detail in a position — an example, a name, a number, a path — had existed since the form's first version and had not held, and a hand fix in the project that kept the same form and the same write step kept a chosen option in its money field.

Decision theory names the split that the form lacked. A decision weighs ends, measures of those ends, limits and beliefs, and picks an option; the option is the decision's output. A document of inputs changes only when an end, a limit or a belief changes. A document that also holds outputs changes with every decision.

## Decision
- **The North Star holds only decision inputs.** Every line is one of four kinds: an end (what the project is for, or whom it serves), a measure (how one part of the goal is tracked: what is counted, its direction, and a floor where the floor defines a value), a principle (a limit or trade-off the owner holds even when evidence says crossing it would pay), or a bet (a belief that, if false, would change the goal or end one part of the project). A bet the owner states is still a hypothesis until something tests it.
- **The line test.** A line the owner would re-tune when evidence moves is a chosen option and belongs in a decision record; a value a measure should reach by a date belongs with the work pursuing it — the destination of its effort where the project keeps a Ticket store, otherwise the record of the choice it serves. Live readings stay out, as before.
- **Six sections replace the nine fields:** Purpose (the problem, then For and Not for), Goal, Principles, How we know (one measure per part of the goal, `empty` where nothing measures it yet), What this rests on (the main bet first), and Open. After them comes Strategy choices in force: the titles of the decision records in effect that carry the area `Strategy`, rebuilt from those records in the same act that writes, supersedes or retires one. A provenance note keeps its state, grounding, date and record titles, and leaves the history of how a position moved to the records.
- **The `Strategy` area is reserved** in the ADR conventions for a guiding choice that the project pursues its goal through and that other decisions derive from.
- **The write step sorts first.** figure-out's docs mode sorts each finding or ruling before it touches the North Star: a chosen option goes to a decision record offer (area `Strategy` where it guides, with the list rebuilt), a dated target to the work that pursues it, and the North Star's positions stay as they are; only the remaining inputs reach the existing update branches. The sort applies to a North Star of either form.
- **Surfaces version 8** carries the change to installed projects. Its upgrade guide reshapes an existing North Star only on the owner's ruling, line by line, and a run with no person to rule flags the reshape and writes nothing.
- **Readers work on both forms.** Every skill that reads a North Star section by name also names the field it replaced, since a project keeps the nine-field form until it updates.
- This repository's own `NORTH_STAR.md` moves to the form, and its five guiding records carry the area `Strategy`.

## Alternatives Considered
- **Keep the nine fields and sharpen the rule against concrete detail**: rejected — that rule had stood since the form's first version and did not stop the growth, because the fields themselves asked for chosen options and the write step wrote rulings in.
- **A resident field holding up to three guiding choices**: rejected by the owner — a field of choices invites the next choice in; the records hold them and the list names them.
- **No pointer to the guiding choices at all**: rejected by the owner — a session would not know which standing choices to read before deciding.
- **One number watched**: rejected by the owner — a goal with several parts and one number lets the unmeasured parts drop out of every decision; each part gets a measure, `empty` where none exists.
- **Values and goal only, with no bets**: rejected by the owner — the bets are what a session checks new evidence against, and a few stay.
- **Dated targets in the North Star**: rejected by the owner — a target is a choice of when, and it lives with the effort that pursues it.

## Consequences

### Positive
- The North Star changes only when an end, a principle, a measure or a bet changes, so a session reading it meets the purpose rather than the latest tactic.
- A session can tell a standing choice from the purpose: the choice is in a record it may revisit, and the list says which records guide.
- The same sort that keeps the document small routes each ruling to a home that remembers why it was made.

### Negative
- Choices that used to sit in the resident file now need one more read, through the list.
- The sort is a judgment at each write; a line that reads as a principle but would be re-tuned can still slip in.
- Projects on the older form keep it until their owner rules the reshape, so readers must keep naming both forms until no such project remains.

## Enforced by
partly — `tests/test_north_star_strategy_list.py` holds the Strategy choices in force list equal to the titles of the records in effect with area `Strategy`; `tests/test_project_conventions_forks.py` keeps `docs/NORTH_STAR_CONVENTIONS.md` and `docs/adr/CONVENTIONS.md` in step with the shipped defaults; `tests/test_setup_project_versions.py` holds surfaces version 8 and its upgrade guide; the eval cases `84-chosen-option-goes-to-a-record` and `85-evidence-against-a-bet` measure the write step. Whether a line is a chosen option stays judgment.

## Source
- Session: figure-out and auto session, 2026-10-21 (investigation log kept locally).
- Related: amends 20260820-manifest-dev-owns-a-project-north-star; see also 20260820-north-star-lines-carry-states, 20260914-who-its-for-is-consumed-by-figure-outs-seat-taking, 20261013-set-up-projects-receive-updates-through-a-version-marker
