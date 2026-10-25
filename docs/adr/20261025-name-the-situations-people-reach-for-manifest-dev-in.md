# ADR: Name the situations people reach for manifest-dev in

## Status
Accepted

## Area
North Star

## Decided by
The user

## Context

The North Star's *Purpose* names who manifest-dev is for by their traits: quality-first
developers with five-plus years of experience, already using an agentic coding CLI, willing to
spend tokens and up-front effort. It named the end and the people, and touched on returning after
a break and on delegation, but did not list the situations in which they reach for it or what they
use today instead.

Traits describe a person; they do not say when that person chooses this workflow over
another. *Competing Against Luck* (Christensen, Hall, Dillon and Duncan, 2016) defines a job as
"the progress that a person is trying to make in a particular circumstance", and calls the usual
organizing principles, customer characteristics among them, "insufficient, and therefore not
predictive" as a basis for what people choose (both in chapter 2, "Progress, Not Products"). The same developer prompts directly for a small fix and wants a defined,
verified run for a change that would be costly to get wrong.

One of the North Star's bets, that people will choose this workflow over the alternatives,
already names the rivals in general: direct prompting, manual coordination, existing project
tools, and doing less. Its *Open* section already asks which circumstances make the workflow
worth adopting. Neither listed the moments the workflow serves today.

## Decision

Add to *Purpose*, after *For* and *Not for*, **When they reach for it**, with four situations,
each a `hypothesis` grounded in the maintainer's own use and each naming what people do
today instead:

1. **Too big to prompt** — a change where a wrong result would cost more rework than the
   tokens to get it right.
2. **Coming back** — returning to a project after a break.
3. **Away from the desk** — work that should move toward an outcome while the person is
   elsewhere, asking only about the choices they kept.
4. **Thinking it through** — a decision or problem not yet stated well, pressed until it is
   clear before anything is built.

The owner ruled to add them; each stays a `hypothesis` because it is a claim about when people
reach for the workflow, which outside use can disprove. *For* and *Not for* stay as they are. The *Open* question on circumstances stays: these are
the maintainer's situations, and outside episodes of choice, switching and continued use are
what would test them.

## Alternatives Considered

- **Keep the trait-based *For* alone, and wait for outside episodes.** Honest about the
  evidence, but later work would still be judged against traits, not against the moment it
  serves.
- **Fewer situations.** Each names a distinct moment with a distinct rival, so dropping one
  would leave work aimed at that moment with nothing named to check it against.

## Consequences

### Positive
- A proposed skill or change can be checked against a named moment and against what people
  do in that moment today, doing nothing included. figure-out's seat-taking already reads
  *Purpose* and narrows to the moment an artifact serves, so it meets these situations there.
- The four situations give the *Open* question something concrete to confirm or overturn.

### Negative
- All four rest on one person's use. An outside user may reach for the workflow in a moment
  none of them names, or never in one of them.
- Four situations invite four directions; the North Star states them, and each later choice
  still decides which one it serves.

## Enforced by
partly — figure-out's seat-taking reads *Purpose* and narrows to a moment; the rest is judgment

## Source
- Session: figure-out on applying *Competing Against Luck* to the North Star, 2026-10-25. Offered four situations; the owner chose all four.
- Related: see also 20261015-projects-drive-themselves-as-far-as-each-user-climbs, 20261023-projects-advance-toward-assigned-outcomes-within-delegated-authority, 20260914-who-its-for-is-consumed-by-figure-outs-seat-taking
