# ADR: Area principles live in project skills, one per area, and stay principles only

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
When the maintainer steps out of the loop, design, product, prompt and architecture work comes back
as "not what they'd pick": it follows the visible rules, but among good options it picks one the
project's people would not. What those people hold lives in their heads, in review threads, or as
project-level Taste in the always-loaded context file, which every session pays for whatever its
work. Nothing gave each area a home of its own, nothing kept decisions, or calls a run made
on its own, out of such a home, and define's review never read one.

The North Star's *Each piece stands alone* says shared additions help colleagues who do not use
manifest-dev, and their agents (`20261109-shared-additions-help-colleagues-who-do-not-use-manifest-dev`).
Decision records and the verification harness already work that way on teams where most people do
not run manifest-dev: a plain file any agent can read.

## Decision
Each area of a project's work that its people have opinions about gets one project skill, named
`<area>-principles`, holding only principles: each line a limit or trade-off with its reason and
when it yields, drawn from a person's statement, a failure seen in that area, or a default a person
chose to depart from or hold. Decisions stay in decision records, rules a check can hold become
checks, reactions stay with their work, and nothing records history. Only a person's yes writes a
line; an unattended run reports candidates. One line in the project context file says when to load
each skill, so any agent finds it. The method lives in one shipped file,
`setup-project/references/PRINCIPLES_SKILLS.md`.

setup-project offers skills for high-signal areas and offers to move principles and Taste entries
that only one area's work needs out of the context file into them, from surfaces v15. A thin wrapper,
`create-principles-skill`, creates or refreshes one on demand through figure-out; asking figure-out
directly works too. figure-out, define and define's review load the skills the pointer lines name
before execution, and review-code loads them for the areas a change touches. A project-level Taste entry that guides one area becomes a line in that area's
skill instead.

## Alternatives Considered
- **A judge that grades each result against the area's taste**: not chosen. A calibrated judge is
  expensive to build and keep honest, and a prose standard plus the existing checks — locks, define
  gates verified by do, define's review — have not been shown to miss. Build one only if an area's
  first tries keep missing as its skill grows.
- **Handing work off by track record**, letting runs act alone in an area once their results were
  accepted often enough: dropped as a concept this need does not require.
- **Skills named after manifest-dev steps** ("how we define", "how we figure out"): not chosen. A
  colleague's agent works by area, not by this workflow's steps, and step rules belong in the
  skills themselves.
- **Plain documents with a pointer line** instead of skills: not chosen. A skill loads by its
  description when the work starts, on every host the project serves.
- **figure-out as the only way to create one**: not chosen. A named wrapper is easier to find; it
  stays a wrapper, so the method has one home.
- **Leaving area Taste in the context file**: not chosen. Every session pays for lines only one
  area's work needs, and a Taste section has no structure a colleague's agent can use per area.

## Consequences

### Positive
- Design, product, prompt and architecture work starts from what the project's people hold, for
  agents with or without manifest-dev.
- The always-loaded context file keeps only what nearly every session needs.

### Negative
- A project carries more files, each needing pruning; the entry test and prune-on-contact offer are
  the only guard against a skill filling with decisions and calls.
- The user's own and the project's Taste now have three homes to choose among, sorted by how often
  the work they guide happens.

## Enforced by
partly — `tests/test_principles_skills.py` holds that the method lives in one file, that every
shipped file working with a principles skill points to it, that the wrapper invokes figure-out and
runs attended unless asked otherwise, and that this repository's principles skills keep the shape
and their pointer lines. That only a person's yes writes a line is held by the prompts alone.

## Source
- Session: a figure-out session, 2026-11-09 (log kept locally).
- Related: narrows 20261102-taste-stays-a-section-of-the-memory-file; amends 20260719-taste-persists-by-offer-and-ratify and 20261102-setup-offers-taste-entries-mined-from-stated-reasons; amends 20261013-new-capabilities-live-inside-the-four-workflow-entry-points with one optional wrapper; see also 20261109-shared-additions-help-colleagues-who-do-not-use-manifest-dev
