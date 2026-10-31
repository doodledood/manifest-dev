# ADR: figure-out's drafts are not verified, and are shown in minutes

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
figure-out offers a quick disposable draft when a read implies making something. Its purpose is
narrow: the user judges what they cannot put into words, the draft draws out criteria they cannot
state, and the two agree a general direction or design.

20260901-deliberation-renders-run-the-design-skill-at-prototype-weight gave such drafts a named
weight in the design skill, with one rule that kept them cheap: "the verification loop is skipped
entirely, because the reader's reaction is the verification and the artifact is disposed of
either way." 20260916-design-is-reference-calibrated-guidance retired that design-owned weight
and moved prototype fidelity and lifecycle to the calling workflow. figure-out's draft bullet did
not take the rule back, so nothing said a draft is unverified, and three nearby lines could pull
one into checks:

- figure-out's verification bullet: "a touched check that is broken or not fit to trust is
  repaired as part of the work" reads as covering a draft, which brings in scratch breaks and
  fit-to-trust checks.
- the step that invokes the design skill for a page draft passed no limit, so design's own
  done-check and its instrument catalog could run on the draft.
- define selects task files by domain, so a draft that reaches it (`/auto prototype X`) gets
  `review-design` and `review-code` gates and the review rounds they drive.

In use, a draft was pulled into UX and animation review rounds and dozens of planted-break checks,
and one iteration took about 19 hours.

The decision sits inside the North Star's Purpose: people keep control of the choices they retain
and trust the work enough to use it, and a draft is how they make a design choice quickly.

## Decision
A draft is part of figure-out and exists only to elicit criteria the user cannot put into words
and to agree a direction. Its fidelity matches what the user expects of it — rough, not sloppy —
and it is never perfected.

A draft is never verified, tested, reviewed or gated: no harness or recipe run, no scratch break,
no review skill, no design instrument or design-check round. The user's reaction is its only
check.

The time bound: the first draft is shown within about 15 minutes of agent working time after the
user accepts the offer, and each iteration takes minutes. A draft that cannot be ready in that
time is cut down to the question being judged rather than shown late. The default form is one
standalone throwaway file with fake data. Once the user picks a direction the draft is done; later
decisions go to the read, decision records or Ticket decisions, and the draft changes again only
when the user asks.

The rule has one home, figure-out's draft bullet. The verification bullet says it does not apply
to a draft. The design step passes the design skill the draft's rough fidelity and that no review
loop runs on it, so design guidance shapes the draft and nothing checks it. define, which cannot
rely on figure-out being loaded, states its own sentence: a disposable draft made only to get a
person's reaction loads no task file, and its Deliverable owes only that the draft reaches that
person with the question it poses.

## Alternatives Considered
- **Restore a prototype-weight mode in the design skill**: one home for every caller, as
  20260901 chose — not chosen because 20260916 put prototype lifecycle with callers for reasons
  that still hold (design is guidance only), and the pull-in came from figure-out's and define's
  own lines, which a design mode would not reach.
- **Soften the wording without a time bound**: a smaller change — not chosen because "quick"
  without a bound let a draft grow into hours of checks; a bound with a cut rule says what to drop.
- **Scope only define's UI task file**: closes the `review-design` gate — not chosen because an
  HTML draft also loads the coding task file and its `review-code` gates.

## Consequences

### Positive
- A draft costs minutes, so the user can see several directions in the time one verified draft
  took.
- No line in figure-out or define routes a draft into a check, review or gate.

### Negative
- A draft can show a defect nobody checked; the user may react to it. The draft is disposable and
  the real build is gated, so the defect does not ship.
- Fifteen minutes is a judgment bound, not a measured one; no eval case grades the time yet.

## Enforced by
partly — `tests/test_drafts_are_unverified.py` pins the no-verification rule, the time bound, the
verification bullet's exclusion, the design step's limit and define's task-file exclusion; how
long a draft actually takes, and how rough it is, stay judgment.

## Source
- Amends 20260916-design-is-reference-calibrated-guidance: callers own prototype lifecycle, and
  figure-out's lifecycle now states that a draft is not verified.
- Amends 20260901-deliberation-renders-run-the-design-skill-at-prototype-weight: its "verification
  skipped" rule is restored in figure-out and define, with a time bound.
- Related: 20261031-autonomous-figure-out-shows-a-draft-to-an-owner-it-can-reach,
  20260924-figure-out-settles-the-artifacts-person-and-opens-visual-directions-with-variants,
  20260905-disposable-prototypes-may-expose-behavior
