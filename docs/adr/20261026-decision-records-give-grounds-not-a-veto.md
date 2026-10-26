# ADR: Decision records give grounds, not a veto, and unattended runs reopen them where a need makes sense

## Status
Accepted

## Area
ADR conventions

## Decided by
The user

## Context
Sessions in a set-up project treat a decision record as a wall. With the user, they push back on
a proposal by citing a record, and they leave out options a record cuts against, so the user never
sees them. In unattended runs they almost always choose the option that follows the record, and
they do not raise a challenge where the record's reasoning no longer fits the case.

The shipped text says how a record may be changed, but not what a record is for when a session
meets one during its work:

- The context-file section that every session reads says "Open `docs/adr/README.md` before
  settling a question the project may already have settled". This presents a record as the
  answer, not as reasoning to weigh.
- The `Revisit when` guidance names one reopen route: a met condition, "only within an assignment
  and explicit authority covering it".
- figure-out classifies a stated constraint as hard or assumed, and "one already established needs
  no re-litigating". A record reads as hard and established, so it prunes options.
- Nothing tells an unattended run whether going against a record is inside its delegation. With
  the authority unclear, it takes the safe path and follows the record.

The eval suite pulls the same way. Cases `24`, `38`, `84` and `85` reward deference to a record or a
North Star line, or raising a conflict with one. No case failed a run that follows a record whose
reasoning no longer fits.

## Decision
A record gives grounds, not a veto. It keeps the reasons for a choice so that a later session
thinks twice before it decides differently. It does not stop that session from deciding
differently. A session that meets a record bearing on its work weighs the record's reasons against
the case:

- Where the reasons still hold, it follows the record and names the reason that holds. "A record
  says so" is never the whole reason.
- Where one of its premises no longer holds, or the case has a need the record did not weigh and
  that need makes sense, the choice is open again. The session shows the option beside the
  record's reasons and never drops an option because a record cuts against it.
- A person can reopen a choice at any time. A run with no person present decides for itself:
  where a premise no longer holds or such a need makes sense, it reopens the choice and writes
  the new record, naming itself as the decider. It then makes this clear: its report and any
  pull request it opens list each reopened
  record first, with the reason it set aside and what reversing would cost, counted by what
  depends on the change after it lands, not by the effort to redo it.
- Reopening is a new record that supersedes or narrows the old one, under the existing lifecycle.
  A met `Revisit when` condition is one named reason to look again, not the only one.

This rule covers records outside the `Strategy` area. `Strategy` records follow
`20261026-north-star-lines-and-strategy-records-get-a-fit-check`. The rule grants no authority to
publish, spend or delete. Where the work lands through a pull request without the Auto grant, a
person lands it, so a person sees each reopened record before it takes effect.

The rule lives in the ADR conventions (`docs/adr/CONVENTIONS.md` and the shipped
`figure-out/references/ADR_FORMAT.md`). A short form lives in the context-file section that
setup-project emits and in this repository's context file. figure-out's spine names records where
it says intent is evidence to weigh, not a veto, and its "no re-litigating" clause covers only
constraints the user has established.

## Alternatives Considered
- **Decide by stakes, leaning toward the record.** An unattended run departs only when the change
  is cheap to undo; otherwise it follows the record and raises the challenge. Rejected: a run
  that waits for a ruling on every costly choice is not autonomous. Reporting the reopened record afterwards takes the place of the hold.
- **Surface only.** An unattended run always follows the record and raises the challenge at the
  top of its report. Rejected: it keeps the adherence the user wants to stop, adding only a
  report line.
- **A general "be bolder" instruction without a rule for records.** Rejected: it changes tone
  more than decisions, and it leaves the wording that frames records as settled answers in place.
- **Leave the wording and rely on the model.** Rejected: the eval suite rewards only deference,
  so prompt tuning drifts further toward it.

## Consequences

### Positive
- Options a record cuts against stay visible, with the record's reasons beside them.
- Unattended runs make the better choice where a record's reasoning has stopped fitting, and the
  owner can still see it and reverse it.
- The corpus stays true: a reopened choice is a new record, never a silent departure.

### Negative
- Unattended runs will sometimes reopen a record the owner would have kept. That costs a reversal
  and a superseding record.
- More records over time, since each reopening writes one.
- The emitted conventions change, which needs a new surfaces version.

## Enforced by
partly — eval cases driven through `verification/recipes/figure-out.md`:
`claude-plugins/manifest-dev/evals/89-record-premise-no-longer-holds` (an unattended run reopens a
record whose premise failed, writes the superseding record and lists it first),
`91-record-against-the-users-idea` (an attended run keeps the option a record's reasons no longer
cut against in view) and `38-stated-rule-conflicts-with-a-record` (a record whose reasons still hold
is followed and not superseded); whether a need makes sense stays judgment

## Revisit when
The owner reverses an unattended reopening in more than one of the next five pull requests that
list a reopened record, read in those pull requests' reopened-record lists.

## Source
- Session: a figure-out session on records and North Star lines treated as blockers, 2026-10-26.
- Amends 20261021-the-north-star-opens-with-its-end-and-signposts-reopen-choices-and-deferred-work
- Narrows 20260714-figure-out-classifies-constraints-before-they-prune
- Related: 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance (the project's
  conventions are the trusted instruction that carries this grant), 20261026-north-star-lines-and-strategy-records-get-a-fit-check
