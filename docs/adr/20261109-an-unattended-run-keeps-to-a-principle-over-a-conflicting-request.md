# ADR: An unattended run keeps to a principle over a conflicting request

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
A principles skill holds how a project's people want one area's work done, written once so runs
need those people less at the steps before execution. That is the North Star's purpose applied to
the steps where a person is still asked most.

The shipped texts said only that departing from a principle is the person's call. In a drive of
`define` with nobody to ask, the request named a pop-up panel and a green leader, and the project's
design principles said own page and one neutral colour. The run kept the request, recorded two
departures, recommended the principled version, and told the person there was one thing they
needed to decide. The principle was noticed and decided nothing, so the Manifest still waited on a
person.

## Decision
Where what was asked conflicts with a principle and the line's own yield does not cover the case,
the principle holds unless the person chose the departure: they named the principle or said to set
it aside, or a decision record or a delegation that names the departure
covers it. A run's general permission to decide is not such a delegation.

- With the person present, the session asks whether the principle has moved or this is an
  exception.
- With no person present, the run builds to the principle and puts the conflict first in what it
  reports: what was asked, the principle, what it built instead, and the one change that restores
  what was asked.
- A departure the person chose is kept and named with the principle and why.

The rule is stated in the method, `setup-project/references/PRINCIPLES_SKILLS.md` → *Using one*,
and in `figure-out` and `define`, which each carry their own copy because each runs alone.

## Alternatives Considered
- **Keep the request and flag the departure**, as the texts read before: not chosen. Every such
  conflict leaves a decision open for a person, which is the outcome principles skills exist to
  remove. A request detail written in the moment is weaker evidence of what the project's people
  want than a line they ratified with its reason.
- **Always follow the principle**, even against a stated override: not chosen. A person who names
  the principle and sets it aside has made the call, and a run that overrides that takes a choice
  they kept.
- **Stop and wait for an answer**: not chosen. A run started unattended does not stall on a call
  it has ratified guidance for.

## Consequences

### Positive
- A request that drifts from the project's principles comes back built the way its people would
  accept, with one line saying how to get what was literally asked.
- The person is asked only when present, and only whether the principle moved.

### Negative
- An unattended run can build something other than a detail the request stated in so many words.
  The report leads with it, and one change restores it.
- A principle with a missing or too-narrow yield now costs more, since runs act on the line as
  written. Pruning and sharpening the lines matters more.

## Enforced by
partly — `tests/test_principles_skills.py` holds that the method, `figure-out` and `define` each
state that the principle holds unless the person chose the departure. That a run follows it is
judged by the `define` recipe's `principles-in-place` and `principles-overridden` drives.

## Source
- Session: an audit of the shipped skills against this repository's principles skills, 2026-11-09.
- Related: see also 20261109-area-principles-live-in-project-skills
