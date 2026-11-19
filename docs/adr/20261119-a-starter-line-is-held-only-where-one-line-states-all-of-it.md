# ADR: A starter line is held only where one line states all of it, and a stricter fit is offered again

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
Setup fits the starter principles to a project's existing principles skills and offers only the
lines they lack. "Lack" was not defined. A project's update marked the starter line "A new need is
met by extending what already does that job" as held by two of its lines, one about reusing what
already owns a behavior and one about taking the fewest moving parts, though neither said what the
starter line asks of a new standing mechanism. A later change in that project added a new setting
beside an input that could have taken one more value, and reviews read the project's lines as
followed. The same starter line also named only standing mechanisms — a service, a job, stored
state — and nothing about a setting, an input or a term, which is where that change went wrong.

## Decision
- A skill holds a starter line only where one of its lines states all of it, in whatever words and
  for at least the cases it covers: what it asks and when it yields. For a choice, all of one side;
  an `Only where` condition decides whether the line is offered, not what it says. A starter line
  whose parts are spread over several lines is lacked, and is offered as a sharpening of the nearest
  line or as a line of its own.
- A version that changes this fit is a new surfaces version, and a project fitted before it is
  offered, once, the lines its skills carry only in part. Lines a skill lacks entirely and was
  offered before are not offered again unless the area's set changed, so a person's earlier answers
  stand.
- The architecture set gains a line of its own for widening an existing input, setting or contract
  before adding a concept beside it, with a yield for a shape others read.

## Alternatives Considered
- **Keep "held" a judgment call**: the observed case shows the call goes to "held" whenever every
  part appears somewhere, which is the failure.
- **Sharpen the existing "extending" starter line instead of adding one**: a reviewer gives each
  line one verdict, and a clause inside a long line was applied to a side point and not to the main
  choice in a blind review.
- **No re-offer to projects already fitted**: the stricter rule would then reach only new setups,
  and the project where the miss happened would never see it.

## Consequences

### Positive
- A project whose skills carry only parts of a starter line is shown the line, beside its parts.
- A review holding work to the new line names the existing input and asks to widen it, where
  without it a review on the same synthetic change did not (one run per arm).

### Evidence and its limits
- The line's wording was chosen by the maintainer on blind reviews of a real change in a private
  project, where reviews without it read the main choice as sound. That result is reported, not
  shown here.
- Here, the review scenario's grader was fixed before the runs and asked that a review on sets
  without the line raise no departure on the main choice. It did not tell the arms apart: on both
  rebuilt fixtures, today's sets read the "extending" line as followed but faulted the placement
  through another line. After those results, on the maintainer's delegation, the line was judged
  by whether only the arm holding it names the existing input and asks to widen it. That rule was
  chosen after the runs, so the result is in-sample.

### Negative
- A stricter fit offers more lines, which costs the person's attention at setup and on the re-fit.
- On the synthetic fit fixture, the earlier rule also did not mark the line held, so the stricter
  rule's difference is shown only on the observed case, not on the fixture.

## Enforced by
partly — `tests/test_setup_project_versions.py` digests the starter sets and the fit in
`PRINCIPLES_SKILLS.md` (*With skills already in place* and *When*), so a change to either without a
new surfaces version fails; the setup-project recipe's `fit-parts` scenario drives a fit on skills
that carry only parts of a starter line, though it does not by itself tell the stricter rule from
the earlier one; the review-code recipe's `widen-catch` and `widen-quiet`
scenarios drive a review holding work to the new line. Applying the held test stays judgment.

## Source
- Issue: https://github.com/doodledood/manifest-dev/issues/451
- Related: Amends [20261118-starter-principles-ship-as-sets-a-project-owns](20261118-starter-principles-ship-as-sets-a-project-owns.md): defines when a fitted skill holds a starter line, and re-offers lines once when the fit changes
