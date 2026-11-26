# ADR: Climb proposals target what holds the result back most and switch approach when attempts stall

## Status
Accepted

## Area
Task guidance

## Decided by
An agent in an unattended run, with no review — under explicit user delegation (`/auto take it from here and merge it`), applying the user's rulings in this session that hill-climb wording stays domain-neutral across all artifact kinds, that measured candidates and bold moves are chosen carefully for high signal and value, and that synthetic climb drives are skipped as a one-off exception to `prompt-principles` line 10.

## Context
A reliable judge or deterministic measure can rank every candidate pair accurately while a hill-climb still plateaus prematurely. Three gaps in the shared climb guidance (`define/tasks/HILLCLIMB.md` and `figure-out/tasks/HILLCLIMB.md`) allowed that failure mode:

- **Undefined "bold attempt", firing too late.** The Stop rule required "a bold attempt" only in the last round before stopping. A proposer could satisfy that with a larger variation inside the same mechanism or with a low-signal speculative change, and small gains on minor polish reset the two-flat-round stop counter before a thorough climb ever reached its last round.
- **No pull toward what holds the result back most.** `20261107-climb-guidance-states-outcomes-and-rulings-not-steps` retired "changing the part whose gap matters most". For costly measures, the search default asked only for "one change aimed at a diagnosed cause", leaving a climb free to spend evaluation budget on minor polish or repeated variations of one stuck diagnosis.
- **Loss-only raw evidence.** Both task files asked for raw evidence of *why the last versions lost*, not of *where the current best still falls short of the goal*. When candidates tie or lose while leaving the dominant gap intact, loss deltas alone do not redirect the next proposal.

In `/do`, the out-of-reach rule (`20261018-do-names-the-evidence-that-puts-a-gate-out-of-reach`) demands materially different approaches before stopping on a *failed* gate, but a hill-climb's Stop rule *passes* on two flat rounds, so that check never fires on a plateau.

## Decision
Tighten the binding `Stop rule` Quality Gate in `define/tasks/HILLCLIMB.md` and its mirrored probes in `figure-out/tasks/HILLCLIMB.md` — using domain-neutral wording that applies equally to web pages, writing, prompts, documents, code performance, simulations, and interactive interfaces — without adding gate rows, procedural steps, duplicated defaults, or extra evaluation rounds:

- **`define/tasks/HILLCLIMB.md` (`Stop rule`, binding Quality Gate — single owning site per `CLAUDE.md`'s one-type rule):**
  - Require raw evidence of why each attempt lost rather than only its score, and of where the current best still falls short of the goal. Deliberately avoid the phrase "in real use" here so offline climbs (sign-up pages, marketing copy, prompt eval suites, local benchmarks) do not collide with `HILLCLIMB.md`'s reserved use of "real use" for live post-climb traffic unavailable offline.
  - Require every measured candidate (bold ones included, across cheap, costly, quick, and thorough climbs) to be chosen for high signal and value — big enough to matter if it wins and informative if it loses — aimed at what still holds the result back most rather than minor polish.
  - Require a thorough or costly climb whose earlier attempts leave that gap in place to challenge its diagnosis or try a different approach instead of repeating variations of the same one.
  - Place the plateau exhaustion exit (`or the record shows no distinct authorized route remains`) inside the loop stop condition as well as the last-round clause, so genuine plateaus exit cleanly without forcing low-signal filler rounds.
  - Scope the thorough last-round different-approach-or-diagnosis requirement to stopping on flat rounds (`when a thorough climb stops on flat rounds`), unless the record shows no distinct authorized route remains, so requester-capped climbs that are still gaining are not forced to abandon a winning approach on their final round.
- **`define/tasks/HILLCLIMB.md` (`Try changes the way the cost of measuring allows`, Default):**
  - Stays focused strictly on cost-driven candidate count and form (three candidates with at least one bold when cheap; one change aimed at a diagnosed cause when costly), without restating or drifting against `Stop rule`.
- **`figure-out/tasks/HILLCLIMB.md` (`What a round can afford` and `What the next round sees`):**
  - Mirror both points as branch-opening questions: whatever a round costs, what makes each measured candidate (bold ones included) high-value enough to earn a measurement rather than minor polish, and which distinct approaches are authorized if earlier attempts leave what holds the result back most in place; and whether the proposer gets raw evidence of where the current best still falls short of the goal alongside why the last versions lost so it can target what holds the result back most and tell when its diagnosis is wrong.

This keeps the existing evaluation budget (one flat round quick, two flat rounds thorough) and keeps `20261107-climb-guidance-states-outcomes-and-rulings-not-steps`'s outcome-and-ruling form.

## Alternatives Considered
- **Sharpen only the Stop rule's last-round bold attempt:** Not chosen — small wins on minor polish reset the consecutive-flat-round counter, so climbs can spend rounds inside a narrow approach before ever hitting the last round, and the rule would not prevent low-signal proposals earlier in the run.
- **Duplicate candidate selection and approach switching in `Try changes...` (`## Defaults`):** Not chosen — violates `CLAUDE.md`'s one-type rule and `prompt-principles` single-owner rule inside one file, risks scope drift between `thorough` and `costly`, and leaves advisory defaults repeating binding gates.
- **Increase patience from two flat rounds to three or more:** Not chosen — raises evaluation cost on every thorough climb, including genuine plateaus.
- **Add a fixed search procedure (mandatory mechanism list or step-by-step re-diagnosis script):** Not chosen — contradicts `20261107-climb-guidance-states-outcomes-and-rulings-not-steps`; procedures overfit one artifact class and go stale across models.
- **Wait for paid synthetic climb drives before editing:** Not chosen — multi-round synthetic climb drives consume substantial model usage; the maintainer granted a one-off exception to `prompt-principles` line 10 so live climbs judge this zero-extra-round wording directly.

## Consequences

### Positive
- Every measured candidate — bold ones included — is held in the binding gate to a concrete high-signal/value bar (big enough to matter if it wins and informative if it loses) rather than minor polish or speculative noise.
- Thorough and costly climbs have a binding reason to inspect where the current best falls short of the goal and switch approaches before exhausting their evaluation budget on one stuck diagnosis.
- Domain-neutral phrasing fits offline behavior climbs, copy, pages, prompts, code speed, and simulations without colliding with `HILLCLIMB.md`'s live "real use" terminology.
- Genuine plateaus keep an explicit exit directly in the stop condition within the same two-flat-round budget, while requester-capped winning climbs keep pursuing their gaining direction.

### Negative
- Behavioral uplift and `already-at-best` non-regression are unverified by synthetic drives at merge time (one-off exception to `prompt-principles` line 10) and rely on observation in live climbs.
- Adds a few lines to `define/tasks/HILLCLIMB.md` and `figure-out/tasks/HILLCLIMB.md`, slightly increasing prompt reading surface on climb tasks.

## Enforced by
partly — `tests/test_hillclimb.py` (`test_proposals_target_highest_value_gap_and_switch_approach_on_stall`) pins the current-best raw-evidence, high-signal/value candidate selection, approach-switching, flat-round last-attempt scoping, plateau-exit, and no-`"in real use"`-collision clauses inside their owning sections in `define/tasks/HILLCLIMB.md` and `figure-out/tasks/HILLCLIMB.md`; whether a run selects high-value candidates and escapes narrow search without churning on genuine plateaus stays judgment, read in live climb execution logs and `verification/recipes/hillclimb.md`.

## Revisit when
Live climbs or `hillclimb` recipe drives still repeat variations of a stalled approach after this guidance, or genuine-plateau climbs churn past two flat rounds despite the exit clause; read in climb execution logs and `verification/recipes/hillclimb.md` drive evidence.

## Source
- Issue: https://github.com/doodledood/manifest-dev/issues/459
- Related: Amends 20261106-a-climb-designs-its-measure-and-search-for-its-task, 20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record, and 20261107-climb-guidance-states-outcomes-and-rulings-not-steps. See also 20261018-do-names-the-evidence-that-puts-a-gate-out-of-reach.
