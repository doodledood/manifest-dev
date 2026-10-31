# ADR: /do takes a reaction to a draft as direction, captures it, and locks only what reaches past it

## Status
Accepted

## Area
do

## Decided by
The user

## Context
A disposable draft is a throwaway rendering made only so a person can react to what they cannot
yet put into words. 20261031-figure-out-drafts-are-unverified-and-shown-in-minutes settled that
nothing verifies one and that later decisions go to the read, decision records or the Ticket. It
said nothing about `/do`, which a Manifest can send a draft Deliverable to, and where three lines
pulled the other way:

- `/do` loads its harvest when it "receives a correction", and the harvest turns a correction into
  a lock: a check that fails for every later contributor
  (20261013-corrections-become-scoped-locks-and-their-hits-become-reported-debt). A reaction to a
  draft arrives as steering and reads as a correction, so "B, but less dense" could become a
  repository rule.
- *Taste on reversal* drafts a Taste entry when steering reverses a call and states why
  (20261012-taste-is-checked-per-call-and-captured-from-explained-reversals). Every explained
  reaction to a draft fits, so each draft iteration could produce a Taste offer.
- "Choose solutions that make the outcome durable" reads as covering the draft, against "never
  perfect it".

figure-out's draft bullet also named "design instrument" and "design-check round", which nothing
in that skill defines.

The decision sits inside the North Star's Purpose: people keep control of the choices they retain,
and a draft is how they make a design choice quickly without it hardening into a rule they did not
make.

## Decision
A reaction to a disposable draft is not a correction. By default it steers the direction the
draft was made to settle, and the design behind it, and installs no lock and drafts no Taste entry.

Every reaction is captured: the direction picked and each criterion it surfaced go, through a
define amendment, into the Manifest — gates on the real work where they bind it, Known Assumptions
recording the person's call — into any Ticket the work is tracked on, and into a decision record
where the choice meets the project's bar for one. They never go back into the draft.

Only what the reaction shows reaches past the draft is locked. A requirement or constraint on the
real work is an invariant the person stated and goes through the harvest, locked at the strongest
rung where real work a check can cover exists; until then it is captured as that work's
requirement, naming the lock it owes, so the run that builds it installs it. A personal lean the person states as reaching
beyond this artifact, with a reason, is drafted as a Taste entry the way *Taste on reversal*
describes, whether or not it reverses a call this run made. A lean with no stated reason is
captured only.

The key assumption: when it is unclear whether a reaction reaches past the draft, it is captured
and not locked. A missed lock costs one later correction; a wrong lock binds every later
contributor to a rule nobody meant.

`/do` keeps the draft throwaway — outside the project's files, as finished as the person expects,
shown in minutes, never perfected or verified beyond reaching that person with its question —
holds work that depends on the choice until the reaction arrives, and makes durable the decision
and criteria the reaction draws out.

The rule has one home, `do/references/HARVEST.md` → *A reaction to a draft*; `do/SKILL.md` loads it
when a reaction arrives and *Taste on reversal* points to it. figure-out's `TASTE.md` and define's
*Taste on reversal* each state one sentence, since neither can read `/do`'s files. figure-out's
undefined terms become plain words: no design measuring or checking tool runs on a draft, and the
design step tells the design skill not to run its optional measuring instruments.

## Alternatives Considered
- **Treat every reaction as a correction and let the harvest's class test filter it**: no new
  rule — not chosen because a draft reaction usually does name a class ("less dense"), so the
  class test passes it and the lock binds a look the person only meant for one draft.
- **Never lock anything from a draft reaction**: simplest — not chosen because a reaction can
  reveal a real requirement ("the totals must match the ledger"), and dropping the lock loses what
  the harvest exists to keep.
- **Lock when unsure**: catches more real requirements — not chosen because a wrong lock fails
  every later contributor, while a missed one waits for one later correction.

## Consequences

### Positive
- A person can react to drafts freely without each remark becoming a rule or an offer.
- Nothing a reaction says is lost: the direction and criteria reach the Manifest and the records
  the work is tracked on.

### Negative
- A real requirement voiced ambiguously stays captured for this work but unlocked until a later
  correction.
- The line between a draft's direction and a requirement is judgment; the examples carry it.

## Enforced by
partly — `tests/test_drafts_are_unverified.py` (`test_do_keeps_the_draft_throwaway_and_makes_the_decision_durable`,
`test_do_reads_the_draft_rule_when_a_reaction_arrives`,
`test_harvest_takes_a_reaction_to_a_draft_as_direction_and_captures_it`,
`test_harvest_gives_an_example_of_each_case`,
`test_figure_out_and_define_do_not_take_a_draft_reaction_as_taste`) pins the rule's lines; how a run
routes a given reaction stays judgment, which the `do` recipe's `draft-reaction` drive covers.

## Source
- Amends 20261031-figure-out-drafts-are-unverified-and-shown-in-minutes: its quoted terms are
  replaced with plain words, and its test assertions on them are rewritten.
- Narrows 20261013-corrections-become-scoped-locks-and-their-hits-become-reported-debt: a reaction
  to a draft is not a correction.
- Narrows 20261012-taste-is-checked-per-call-and-captured-from-explained-reversals: an explained
  reaction to a draft is not a reversal to capture as Taste unless stated as reaching beyond it.
- Related: 20261031-autonomous-figure-out-shows-a-draft-to-an-owner-it-can-reach,
  20260719-taste-persists-by-offer-and-ratify
