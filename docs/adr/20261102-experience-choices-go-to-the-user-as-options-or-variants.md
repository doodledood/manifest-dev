# ADR: An experience choice goes to the user as concrete options or variants, and a reason given in reply resets the recommendation

## Status
Accepted

## Area
figure-out

## Decided by
The user — the user approved the Manifest that asked for experience choices to reach them as concrete options and for a steer to reset the recommendation; the agent that ran it chose the wording and where it lives, under that Manifest's delegation.

## Context

figure-out already puts a user's call to the user with a recommendation, and a visual draft whose
direction is open already opens with two or three variants
(`20260924-figure-out-settles-the-artifacts-person-and-opens-visual-directions-with-variants`). The
design skill asks before guessing at a choice that would change the work
(`20260924-design-starts-from-the-person-and-their-moment`). Neither said what form a choice about
the experience takes: where something lives, how the person reaches it, how many steps it takes,
what a step asks of them.

In replays of one owner's product sessions, kept outside this repository, those choices reached the
owner in two shapes that cost a correction each time: decided silently inside a proposal, or asked
in the abstract ("where do you think it should go?"). When the owner answered with a reason rather
than an option, the next recommendation moved one step from the agent's earlier pick instead of
being reasoned again from that reason.

This decision sits inside what the North Star's *Purpose* names: the person keeps control of the
choices they retain, without restoring the same context in every session.

## Decision

- figure-out's spine, beside the user's-call paragraph: a user's call about what a person will see
  or do goes to the user as concrete options, each a specific placement or flow, with the
  recommendation first; or, when a draft is on offer, as draft variants that differ on that choice.
  When the user answers with an aim or a reason instead of an option, the next recommendation is
  reasoned again from that aim, as if it had been stated first.
- figure-out's draft variants may differ on where things live, how the person moves through it, or
  what each step asks, not only on feeling and visual idea.
- The design skill, where an open alternative is an experience choice, shows two or three variants
  that differ on that choice, made from the product's existing patterns, and lets the requester
  choose by looking.

## Evidence at decision time

Each case was driven once on the skills before this change and once after, through the `figure-out`
and `design` recipes, and graded by a grader session that saw each reply under a letter label only.
A case passes when the run after the change passes and the run before fails; cases whose run before
the change passed were replaced once, and `99`, which failed in both, was replaced with the parent
question its first version left open settled in the prompt.

| Case | First version (after / before) | Replacement (after / before) |
|---|---|---|
| `99` an experience choice as options | FAIL (borderline) / FAIL | FAIL / FAIL |
| `100` a steer resets the recommendation | PASS (borderline) / PASS | PASS / PASS |
| design `variants-of-an-experience-choice` | PASS (borderline) / PASS (borderline) | — |

In both versions of `99`, both arms asked a parent question first: whether a changed servings
number stays on the recipe, and, once the case settled that, whether the recipe screen has a
separate cooking mode. The grader fails any question other than the interface. A one-prompt case
leaves those parents open, so `99` measures the case, not the line; it stays in the suite marked
for rewriting. `100` and the design scenario pass on the skills before the change, so they show no
regression and no uplift. `100`'s replacement drifted from the scenario this change was specified
against and passed in both arms too, so the suite keeps its first version.

## Alternatives Considered

- **Leave the form of the ask to the existing user's-call rule** — not chosen: it says to recommend,
  not what to offer, and the replays show abstract asks under it.
- **Always render variants for an experience choice** — not chosen: a draft is an offer the user
  accepts, and a placement question with two clear candidates is answered faster as two options.
- **A rule in the design skill only** — not chosen: most of these choices arise in figure-out
  before any page is designed.

## Consequences

### Positive
- A user's call about the experience reaches the user as something they can pick, or look at and
  pick.
- A reason given in reply steers the next recommendation instead of nudging the old one.

### Negative
- No case yet shows the change moving a run: `99` needs a version whose parents are settled in the
  case, and `100` and the design scenario pass without it.
- One more paragraph in figure-out's always-loaded spine.

## Enforced by
partly — `tests/test_figure_out_coverage.py` keeps the coverage rows for the paragraph and the draft-variants line naming cases `99` and `100`; whether a run asks in options is judgment, measured only by drives.

## Revisit when
A rewritten `99`, or a long-session case, shows runs asking an experience choice as options no more often with the paragraph than without it; read in `claude-plugins/manifest-dev/evals/README.md` → *Seat pass and experience choices — 2026-11-02*.

## Not decided here
- A version of `99` whose parent questions the prompt settles.
- Whether the design skill's variants should also run when no draft is on offer.

## Source
- Session: a `/define` session and a `/do` run on the resulting Manifest, 2026-11-02 (logs kept locally). Drive summaries and blind grades are in the pull request that adds this record.
- Amends 20260924-figure-out-settles-the-artifacts-person-and-opens-visual-directions-with-variants, 20260924-design-starts-from-the-person-and-their-moment
- Related: 20261102-figure-out-looks-from-the-persons-seat-in-a-fresh-pass
