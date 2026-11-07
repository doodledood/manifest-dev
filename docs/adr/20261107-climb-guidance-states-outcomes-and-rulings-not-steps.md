# ADR: Climb guidance states outcomes and rulings, not steps

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user judged the shipped climb guidance too procedural against the prompt-engineering skill, ruled that `/hillclimb` stays a thin wrapper, and ruled that figure-out alone, asked to make something as good as it can be, should reach much the same climb, since asking questions and working things out is already its job. The user approved the shape below. The agent chose which lines to keep by the provenance test of the prompt-engineering skill.

## Context
The guidance merged with `/hillclimb` told a run how to climb as well as what a climb owes: the form of a judge's brief, how votes start and stop, how picks teach a judge, what a record line holds and how it rolls up past 50 lines, how a staged measure screens a batch and traces a failed one, how to size a test on real use. It was spread over define's `HILLCLIMB.md` (89 lines), a judge reference `define/tasks/references/AI_JUDGE.md`, and a 54-line command that restated rulings the task file already held.

The prompt-engineering skill keeps three kinds of line: what the user ruled, defaults a run observably misses without the line, and facts the run cannot reach. Spelled-out process that a capable model can work out from the goal and the material in front of it narrows the run to one path and goes stale. Drives on the code before the climb guidance existed showed what a run misses unaided: it redesigned in one shot, with no rounds, no proven measure or judge, no stop rule, no comparison against the original, and no statement of how careful it was being. A plain figure-out session reached the right core read on a sign-up page climb. The misses are outcomes; none of them is a missing procedure.

A rule restated in the command also reaches only runs that start there. A climb asked through figure-out, define or `/auto` never reads the command.

## Decision
- **define's `HILLCLIMB.md` holds what a climb owes as outcome gates, and the user's rulings as Defaults.** The gates: the measure is shown good before round 1 and then held fixed; a version is kept only on a confirmed gain with the other objectives no worse; protected parts survive; the stop rule; the final comparison against the original; no win by misleading the people served; and what the report says. The Defaults are the user's rulings: how rounds try changes follows the cost of measuring; one primary objective with the rest as guards; a behavior goal climbs offline first; the extra judge guards stay off until a proof shows the need; the record is kept findable; push only when asked; every number is a default. How a run meets the gates is the run's choice.
- **The rulings live once, in define's task file.** Every entry point that defines a climb reads it, so `/hillclimb`, `/figure-out`, `/define` and `/auto` get the same climb. figure-out's `HILLCLIMB.md` keeps only its probes.
- **`define/tasks/references/AI_JUDGE.md` is removed.** What survives from it is what the user ruled or a run was seen to miss, now in the task file: an AI judge compares two versions; it sees no example version; before use it prefers the original over a version made clearly worse, and in a thorough climb it also ties identical versions and keeps its verdict when the two swap places; its extra guards stay off until needed. The judge's brief format, the vote minimum, lead and cap, how picks teach it, and the rule that the proposer never sees the judge's words are no longer shipped.
- **`/hillclimb` holds framing and routing only.** It says this is a hill-climb on the target, passes the request as given, finds an earlier climb's record when one continues, routes attended requests to figure-out and define with the requester taking part and `--autonomous` requests to their autonomous forms, then runs `do` and, in an attended climb, asks about pushing at the end. It restates no climb rule.
- **Narrows the climb records of 2026-11-06 on mechanics they shipped.** Each keeps its decision where this record does not say otherwise.
  - `20261106-hill-climbing-runs-through-figure-out-define-and-do`: no judge reference ships; the command owns routing only.
  - `20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own`: the proof stays and is stated as an outcome; the vote mechanics, the teaching procedure, the separate-context rule for the proposer and the form nudges are retired.
  - `20261106-a-climb-designs-its-measure-and-search-for-its-task`: the staged measure is an outcome (a cheap stand-in screens only after catching a known-worse version under each condition people meet the artifact in, and the full measure confirms what it passes); changing the part whose gap matters most, tracing a failed batch and sizing a test on real use are no longer shipped.
  - `20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record`: the record's line format and its 50-line roll-up are retired; a re-run proposes nothing the record rejected.
  - `20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters`: the quick and thorough rules are stated in define's task file alone, never in the command.

## Alternatives Considered
- **Keep the procedure, trimmed.** Rejected: the drives that justified it measured outcomes. A shorter procedure still fixes one path, and every line of it needs maintaining as models change.
- **Move the rulings into the command and keep the task file to gates.** Rejected: a climb asked through figure-out, define or `/auto` never reads the command, so the same request would get different climbs by entry point.
- **Drop `/hillclimb` entirely.** Rejected for now: it is the name people reach for and it carries `--autonomous` routing, at 24 lines. The parity drive through `/auto` tests whether it adds anything beyond that.

## Consequences

### Positive
- One request gets the same climb from any entry point.
- A run is free to meet a gate the way its task calls for, and the guidance does not go stale as hosts and models change how judges and searches work best.
- About 100 fewer shipped lines to keep in step.

### Negative
- A run that would have followed a shipped procedure well may now do worse on a step it invents. The recipe's drives are the check; a gate a run misses goes back in as an outcome, not as steps.
- Research nudges for choosing a judge's form no longer reach the run.

## Enforced by
partly — `tests/test_hillclimb.py` (`test_command_routes_and_restates_no_climb_rule` and `test_the_judge_is_proven_sees_no_examples_and_ships_no_reference`) fails when the command restates a climb rule or loses its routing, or when a judge reference returns or the judge's proof and example ban leave the task file. Whether a line states an outcome rather than a step stays judgment, read with the `review-prompt` skill.

## Revisit when
A `hillclimb` recipe drive or a climb's report shows a run missing an outcome its gates state, where the cut procedure would have prevented it; read in the recipe's drive evidence.

## Source
- Session: a figure-out and review session, 2026-11-07 (log kept locally).
- Related: Narrows 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261106-an-ai-judge-decides-between-two-versions-and-each-climb-proves-its-own, 20261106-a-climb-designs-its-measure-and-search-for-its-task, 20261106-a-climb-stops-on-patience-and-a-rerun-continues-its-record and 20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters. See also 20261106-a-climb-runs-without-a-person-choosing-by-default.
