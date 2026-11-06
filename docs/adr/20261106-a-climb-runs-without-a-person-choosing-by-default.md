# ADR: By default, a hill-climb runs without a person choosing between versions

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context
A climb proposes and compares many versions. If a person picks among them, the climb moves at the speed of that person's attention and stops when they step away. Most requesters who start a climb want it to finish without them. Some want to keep a hand in it: to pick a direction, to judge how a design feels, or to choose among the finalists.

`20261102-experience-choices-go-to-the-user-as-options-or-variants` sends a choice about what a person will see or do to the user as options or variants. It also has the design skill let the requester choose by looking.

## Decision
- **By default, no questions during the run.** A climb runs from its start to its stop without asking a person anything. The measure picks between versions, including choices about the experience.
- **A requester can take part.** A requester who wants to choose says so in the request, in their own stated rules or in their project's context file. They might want to pick a direction at the start, choose between versions in each round, or choose among the finalists at the end. The climb then brings those choices to them as options or variants, as `20261102-experience-choices-go-to-the-user-as-options-or-variants` describes.
- **What the requester keeps is fixed up front.** It is written down before the first round as parts that must not change. The climb changes none of them.
- **Every choice stays visible.** The report shows each choice the climb made beside the version it beat, so the requester can see any of them and reverse it after the run.
- **Narrows `20261102-experience-choices-go-to-the-user-as-options-or-variants`.** Inside a climb, by default, the measure makes those choices instead of the user, and the report shows each one beside what it beat.

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
not yet — two `hillclimb` recipe scenarios. In one, a climb runs with no person present; the scenario checks that it asks nothing and reports each choice beside the version it beat. In the other, the request asks to choose between versions, and the scenario checks that the climb brings those choices as options or variants.

## Revisit when
Requesters reverse the choices of finished climbs more often than they keep them, or most requesters ask to take part; read in the climbs' pull request reviews and descriptions.

## Source
- Session: a figure-out session, 2026-11-06 (log kept locally).
- Narrows 20261102-experience-choices-go-to-the-user-as-options-or-variants
- Related: 20261106-hill-climbing-runs-through-figure-out-define-and-do
