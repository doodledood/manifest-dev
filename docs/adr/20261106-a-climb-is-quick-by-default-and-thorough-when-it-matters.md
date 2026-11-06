# ADR: A hill-climb is quick by default and thorough when the stakes call for it

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user asked for climbs that "just take this and make it better for my cause and don't do overkill stuff like judging the judge endlessly", and, asked whether a climb should be quick by default and thorough when asked or when the stakes are visible, keeping one check on its judge, answered yes. The agent drafted which stakes make a climb thorough.

## Context
A climb can spend most of its effort before the first round: proving its measure against every way it could mislead, calibrating a judge on the requester's picks, recording noise, and setting margins for each objective. That effort pays when a climb runs long, when a wrong result is costly or hard to undo, or when objectives pull against each other. It is overkill when someone wants a page, a prompt or a paragraph made better now, and it makes the common request slow enough that people stop asking for it.

Doing none of it is not an option either. A climb on a measure nobody checked can keep "improving" while the goal gets worse, and a judge that cannot tell a degraded version from the original steers at random.

## Decision
- **Quick by default.** A quick climb infers the goal and the people served and states them, asking an attended requester only when it cannot infer the goal. It keeps the parts protected by default, proves its measure with one check (a clearly worse version loses), stops at the first round with no confirmed gain, and ends with a final comparison independent of the loop. Its report says what it did not check and what a thorough climb would add.
- **Thorough when it matters.** A climb is thorough when the requester asks, or when the session sees what is at stake: a long run, such as many rounds or one that keeps running unattended under a scheduler or coordinator; a wrong result that is costly or hard to undo once the artifact is in use, judged by what the artifact is for rather than by how easily the climb's commits revert; or objectives that pull against each other. A thorough climb shows its measure good in full, involves an attended requester in defining it, and stops after two rounds with no confirmed gain.
- **Running unattended alone does not make a climb thorough.** `--autonomous` says who is asked, not how careful the climb is.
- **The climb says which, and the requester can switch.** Its first lines state whether it is quick or thorough and why, how it will try changes and how it will measure. The requester changes any of it in plain words. The line opens the Manifest's Initial Approach rather than its Outcome, since it is a working choice, and the Outcome owes the best version the climb's own rules accept, or the original kept with evidence nothing beat it, so a climb that finds no gain still finishes. Quick and thorough are depths, not flags.

## Alternatives Considered
- **Thorough by default.** Not chosen: most requests want a fast improvement, and a thorough climb's proof and calibration would make them slow and costly.
- **Quick by default with no check on the measure.** Not chosen: a measure that cannot tell a worse version from a better one steers at random, and one check costs little.
- **A `--quick` or `--thorough` flag.** Not chosen: the requester would need to know the depths exist to choose one. The climb picks from what it sees and says so, and plain words switch it.

## Consequences

### Positive
- The common request gets a fast improvement with one sanity check, and a long or costly climb gets the full proof.
- The requester sees the depth and its reason at the start and can switch it.

### Negative
- A quick climb can stop at a nearby peak a thorough climb would pass, and its one check can pass a measure a full proof would reject; its report says so.
- Inferring the stakes from the request can misjudge them; the first lines are where the requester catches that.

## Enforced by
`tests/test_hillclimb.py` (`test_a_climb_is_quick_by_default_and_autonomy_does_not_make_it_thorough`) fails when the define task file or the command drops the quick default, the rule that `--autonomous` alone does not make a climb thorough, or the quick climb's narrow asking. Whether a climb read its stakes well stays judgment, read in the first lines of the `hillclimb` recipe's quick and thorough scenarios.

## Revisit when
Requesters switch most quick climbs to thorough, or most thorough climbs to quick, after reading their first lines; read in the climbs' reports and execution logs.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261106-a-climb-runs-without-a-person-choosing-by-default, 20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record
