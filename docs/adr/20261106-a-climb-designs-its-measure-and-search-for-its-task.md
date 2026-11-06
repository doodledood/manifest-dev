# ADR: A hill-climb's measure and search are designed for its task

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled that figure-out and define design each climb's measure and search to best practice and to the task's nuances, aiming at the best result in the fewest rounds. The agent drafted the specific practices below from the cited sources.

## Context
Two choices made before a climb's first round decide how good the climb can be. The first is what counts as better. The second is how candidates are proposed.

A measure that fits one task misleads on another. A page's conversion, a query's latency, a prompt's pass rate on a suite and a document's clarity to its reader are each measured differently. Some goals have a number; others need judgment.

A search that only refines the current leader finds the nearest local peak. A search that ignores what was already tried repeats it.

Work on optimizing against a measure points the same way:
- OPRO (Yang et al., arXiv 2309.03409) improves when each step proposes several solutions informed by the scored trajectory so far. Its exploration setting trades a flat curve against ignoring that trajectory.
- Optimizing a proxy too hard eventually lowers the true result (Gao, Schulman and Hilton, *Scaling Laws for Reward Model Overoptimization*, arXiv 2210.10760).
- Choosing the best of several noisy estimates overstates the winner (Smith and Winkler, *The Optimizer's Curse*, 2006).
- The eval suite's own hill-climb keeps a change only when the climb set moves and nothing falls, with held-out cases as guards. A fault in a case is fixed outside the climb, never as one of its rounds (`20261031-prompt-engineering-checks-a-runs-input-before-its-wording`).

## Decision
figure-out and define design each climb's measure and its search for the task in hand. The aim is the best result the climb can reach in the fewest rounds. `HILLCLIMB.md` in each task-file set carries how.

- **The measure follows the goal, unless the requester names one.** A measure the requester names is used, and it is proven like any other. Otherwise, a goal with a number gets that number. A goal that a suite of checks can show gets the suite. A goal that neither can capture gets an AI judge, for any kind of artifact. When a goal has parts of each kind, its measurable parts become the measure or its guards.
- **The measure is proven, then frozen.** Before the first round, the measure must tell a known better version from a known worse one, and its run-to-run spread must be known. Nothing in the measure changes during the climb. A fault found in it is fixed outside the climb.
- **The measure's noise sets the margin.** A deterministic measure is taken once. A noisy number or suite is taken repeatedly, and a gain counts only beyond the spread. An AI judge votes as `20261106-an-ai-judge-compares-two-versions-and-never-scores` sets out.
- **What must not change is stated first.** Hard requirements, facts the person needs and protected parts are written down before the first round and checked on every candidate. No candidate wins by dropping one of them.
- **The search spreads before it refines.** Each round proposes several candidates. They differ from each other and from everything already tried, and at least one is a bold departure. Proposals draw on the full record of what won, what lost and why. A candidate that is clearly losing early is dropped before its full measurement. Refining the leader comes after distinct directions have been tried.

This record does not decide where the shared measuring rules live so that `PERF.md` and `HILLCLIMB.md` do not state them twice. That is left to the build.

## Alternatives Considered
- **One fixed protocol for every climb.** Not chosen: a protocol made for a noisy judge wastes rounds on a deterministic number, and one made for a number cannot judge a page's clarity.
- **Refine only the current best.** Not chosen: it converges on the nearest local peak and cannot leave it.
- **An AI judge for every climb.** Not chosen: where the goal has a number or a suite, a judge adds noise and cost that the direct measure avoids.

## Consequences

### Positive
- A climb measures what its goal names, and a measurable goal never pays for judgment.
- Distinct and bold candidates, plus a remembered record, give a climb a chance at a better peak than the nearest one.
- A proven, frozen measure cannot be bent toward the candidate it is judging.

### Negative
- Proving the measure costs time before the first round.
- Each round costs several candidates rather than one.
- Designing the measure is itself a judgment a climb can get wrong. The climb's final check (`20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record`) is the guard.

## Enforced by
not yet — a `hillclimb` recipe scenario that climbs a number and checks that the climb's record shows the measure proven before the first round and unchanged after it. Whether a measure fits its task stays judgment.

## Revisit when
Climbs that reached their stop are overturned by their final check, or by evidence from real use, more often than they are confirmed; read in the climbs' pull request descriptions.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261031-prompt-engineering-checks-a-runs-input-before-its-wording
