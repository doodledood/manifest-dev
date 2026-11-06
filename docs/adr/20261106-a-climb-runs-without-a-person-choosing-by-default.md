# ADR: By default, a hill-climb runs without a person choosing between versions

## Status
Accepted

## Area
Task guidance

## Decided by
The user. The user ruled that a climb runs without a person by default, that it involves the requester in defining unless `--autonomous` is given, that it pushes only when the requester wants it, and that each of these is a default.

## Context
A climb tries and compares many versions. If a person picks among them, the climb moves at the speed of that person's attention and stops when they step away. Most requesters who start a climb want it to finish without them. Some want to keep a hand in it: to pick a direction, to judge how a design feels, or to choose among the finalists.

`20261102-experience-choices-go-to-the-user-as-options-or-variants` sends a choice about what a person will see or do to the user as options or variants. It also has the design skill let the requester choose by looking.

## Decision
- **By default, no person chooses between versions during the rounds.** The measure picks between versions, including choices about the experience.
- **Defining a thorough climb involves the requester, unless `--autonomous`.** Without `--autonomous`, the requester takes part while a thorough climb is defined: what counts as better, whether the measure reflects the goal, how objectives trade off, and what must not change. A quick climb asks only when it cannot infer the goal (`20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters`). With `--autonomous`, nobody is asked from start to end.
- **A requester can take part in the rounds.** A requester who wants to choose says so in the request, in their own stated rules or in their project's context file. They might pick a direction at the start, choose between versions in each round, or choose among the finalists at the end. The climb then brings those choices to them as options or variants, as `20261102-experience-choices-go-to-the-user-as-options-or-variants` describes.
- **What the requester keeps is fixed up front.** It is written down before the first round as parts that must not change. The climb changes none of them.
- **Nothing is pushed unless the requester wants it.** A climb pushes or opens a pull request only when the requester asks, in the request, their rules or their context file, even where the project's remote is on GitHub. An attended climb asks at its end; an unattended one keeps its commits local and says so.
- **Every behavior is a default.** Who chooses, how the climb measures and tries changes, its numbers, whether it pushes, and the guard against versions that win by misleading the people served are defaults the requester changes in plain words, with no setting beyond `--autonomous`.
- **Every choice stays visible.** The report shows each choice the climb made beside the version it beat, so the requester can see any of them and reverse it after the run.
- **Narrows `20261102-experience-choices-go-to-the-user-as-options-or-variants`.** Inside a climb's rounds, by default, the measure makes those choices instead of the user, and the report shows each one beside what it beat.

## Alternatives Considered
- **Ask the requester by default, at the start, in each round or at the end.** Not chosen as the default: the climb then moves at the person's attention and stops when they step away. A requester who wants any of these asks for it.
- **No person, as a fixed rule.** Not chosen: a requester who wants to judge a direction or the feel themselves would have to give up the climb to do it.

## Consequences

### Positive
- A climb can run while the requester is away and finish without them.
- A requester who wants to judge keeps that choice, through channels they already use.
- Every experience choice the climb made is visible beside the alternative it beat.

### Negative
- In a default climb, a choice the requester would have made differently stands until they read the report.
- A default climb is only as good as its measure, and no person checks the measure's blind spots until the report.

## Enforced by
`tests/test_hillclimb.py` (`test_a_climb_pushes_only_when_asked_and_its_numbers_are_defaults` and `test_a_climb_is_quick_by_default_and_autonomy_does_not_make_it_thorough`) fails when the define task file or the command drops the push default, the defaults rule, the relaxable guard against misleading, or the attended defining of a climb. Whether a climb asked nothing it should not have stays judgment, read in the `hillclimb` recipe's `quick-text`, `attended-copy` and `requester-chooses` scenarios.

## Revisit when
Requesters reverse the choices of finished climbs more often than they keep them, or most requesters ask to take part in the rounds; read in the climbs' reports and execution logs.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Narrows 20261102-experience-choices-go-to-the-user-as-options-or-variants
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do, 20261106-a-climb-is-quick-by-default-and-thorough-when-it-matters
