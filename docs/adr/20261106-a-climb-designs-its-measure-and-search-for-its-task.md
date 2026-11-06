# ADR: A hill-climb's measure and search are designed for its task and the cost of measuring it

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled that figure-out and define design each climb's measure and search to best practice and to the task's nuances, aiming at the best result in the fewest rounds; that hill-climbing is not always generating several versions and judging them, so a large artifact or a measure that takes hours must be supported as well as a cheap one; that a climb toward a behavior climbs offline first and continues on tests on real use the requester runs; and that several objectives default to one primary with guards, with the alternatives as probes. The agent drafted the specific practices below from the research notes `docs/research/hillclimb-several-objectives-20261106.md` and `docs/research/hillclimb-costly-climbs-20261106.md`.

## Context
Two choices made before a climb's first round decide how good the climb can be: what counts as better, and how changes are tried.

A measure that fits one task misleads on another. A page's sign-ups, a query's latency, a prompt's pass rate on a suite and a document's clarity are each measured differently, and some can only be measured by real use. Any measure optimized hard enough rewards what it was not meant to, and what it does not mention gets spent to buy what it does.

How to try changes depends on what one measurement costs. When measuring is cheap, several independent candidates per round beat repairing one, and a bold candidate helps leave the nearest peak. When one measurement takes hours, a round can afford one change, and a change aimed at a diagnosed cause beats a random one. On a large artifact, the useful change is to the part that limits the result. A cheap check that screens candidates for a slow measure helps only where it agrees with the slow measure, and cheap checks fail at the seams where their conditions differ from real use: a still against motion, one input against all, a headless capture against a real device.

The shared rules every measured comparison needs (prove the measure, then freeze it; the noise floor; a fair comparison; a floor on attempts) were stated only in `PERF.md`.

## Decision
- **The shared measuring rules live in `MEASURE.md`.** Both task-file sets carry it; `PERF.md` and `HILLCLIMB.md` compose onto it, and `PERF.md` keeps only what is specific to performance.
- **The measure follows the kind of goal.** A number is measured directly. A behavior of the people served, such as sign-ups, is measured only by real use; offline, the climb checks what can be checked, lets a judge predict the rest, and calls any gain in the behavior a prediction. How well the artifact serves its people, and the requester's own taste, are measured by an AI judge (`20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own`). When nothing else captures the goal, an AI judge comes first, and human judgment is the measure only when the requester chooses it.
- **The measure is shown good, then frozen.** A thorough climb names the ways the measure could rise while the goal is not served and guards each, shows that a clearly worse version cannot win and that a pair about the size of the gains sought is told apart, and records the run-to-run spread; a number or suite also sets aside held-out cases no round sees, for the final comparison. A quick climb runs one check: a clearly worse version loses. A measure the requester names gets the same checks. The measure stays unchanged until the final comparison; a change to the measure, or to the priority among objectives, starts a new climb, except a behavior climb's hand-over to results from real use.
- **What must not change is written first.** What the requester names, plus by default the artifact's facts, figures, prices, legal and required text and promises, code's tested behavior and public interface, and the floors of the artifact's own task-file gates. Every kept version keeps them.
- **Several objectives: one primary, the rest guards.** By default a gain is claimed on one primary objective, every other objective is a guard that may lose no more than its margin against the original, and what no measure covers is protected. Choosing among finalists, a front of versions better on every objective, a weighted sum over stated exchange rates, floors and enough-levels are probes, each with when it fits. A climb never invents weights.
- **How a round tries changes follows the cost of measuring.** When measuring is cheap, a round tries three candidates by default, one of them bold, and more when it is cheaper still. When it is slow, a round makes one change aimed at a diagnosed cause. On an artifact too large to vary whole, a round changes the part whose gap matters most and holds the rest as guards. Proposals draw on the full record and the raw evidence of each loss.
- **A slow measure is staged behind a proven cheap check.** The cheap check screens candidates only after it has caught a known-worse version under each condition people meet the artifact in where it could see something different. Candidates it passes become the current best only once the full measure confirms them, and a failed batch is traced to its cause.
- **A test on real use is sized first.** From how many people the artifact reaches, the climb states the smallest gain such a test could detect and how long it would run, and prefers versions bold enough to show at that traffic. It never starts such a test unless asked.

## Alternatives Considered
- **One fixed protocol for every climb.** Not chosen: a protocol made for a noisy judge wastes rounds on a deterministic number, and one made for a number cannot judge a page's clarity.
- **Several versions every round, whatever measuring costs.** Not chosen: when one measurement takes hours and a version is a large change, three versions a round multiply the slowest part of the climb.
- **Refine only the current best.** Not chosen: it converges on the nearest peak and cannot leave it.
- **A weighted score over all objectives by default.** Not chosen: weights nobody stated are invented, and a weighted score lets a gain on one objective hide a loss on another.

## Consequences

### Positive
- A climb measures what its goal names, and a measurable goal never pays for judgment.
- A large or slow artifact gets a climb that fits its cost, rather than one built for cheap measures.
- A measure checked against the ways it could mislead cannot be quietly bent toward the candidate it judges.

### Negative
- Proving the measure, and a cheap check under each condition, costs time before the first round.
- Designing the measure is itself a judgment a climb can get wrong. The final comparison (`20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record`) is the guard.

## Enforced by
`tests/test_hillclimb.py` (`test_how_a_round_tries_changes_follows_the_cost_of_measuring` and `test_each_climb_and_measure_file_has_its_mirror_and_composes_onto_measure`) fails when the define task file drops the cost-driven search, the staged measure, the measure's proof or the rule that a clearly worse version cannot win, or when either set loses `MEASURE.md` or its composition. Whether a measure fits its task stays judgment, read in the `hillclimb` recipe's `slow-sim`, `thorough-number` and `unprovable-measure` scenarios.

## Revisit when
Climbs that reached their stop are overturned by their final comparison, or by later results from real use, more often than they are confirmed; read in the climbs' reports and execution logs.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Research: `docs/research/hillclimb-several-objectives-20261106.md`, `docs/research/hillclimb-costly-climbs-20261106.md`.
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261031-prompt-engineering-checks-a-runs-input-before-its-wording
