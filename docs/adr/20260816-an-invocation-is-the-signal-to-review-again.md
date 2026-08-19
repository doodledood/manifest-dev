# ADR: An invocation is the signal to review a head again

## Status
Accepted

## Area
PR lifecycle

## Context

`review-pr` did not re-review a head it had already reviewed. Two clauses produced that: the
one-shot pass skipped code verification when the head was unchanged from our latest review, and the
review range was lower-bounded by that review's head SHA, making the range empty on an unchanged
head. Both read durable GitHub state rather than session memory, which is what makes the pass
replayable in CI — and also what closed every workaround, since a fresh session on a different model
hit the same skip.

That behavior has a job. It is `review-pr`'s ratchet at the pull request boundary, the property
`20260805-ratchet-judgment-gate-reverification` relies on when it observes that a judgment over an
open finding space resurfaces new findings on an unchanged subject and therefore does not converge
under repetition. It is also what makes `--loop` terminate: the loop's exit condition is "no
unreviewed range since our latest review", and it re-runs the one-shot pass on an escalating
15-minute-to-2-hour interval for up to 24 hours.

The behavior also overrode a legitimate intent. An operator with a risky change may want a second
independent read of the same commit, often under a different model. Running the skill again is how
a person expresses that, and the skill answered by doing nothing.

## Decision

An invocation is the signal. A fresh `review-pr` invocation always verifies the change, including on
a head we have already reviewed and that has not moved since. Where the delta since our last review
is empty, that pass reviews the full pull request diff; where the head has moved, the existing
`last-reviewed-by-us..current-head` range is unchanged.

The unchanged-head skip survives in exactly one place: a `--loop` wake after that invocation's first
pass. A wake is not a decision — nobody re-chose anything — and re-reviewing one commit on every
wake is the nag the check exists to prevent. Scoping the check there keeps the loop's exit condition
reachable.

Nothing is added to pass. The discriminator is that an invocation started, which the skill already
knows, so there is no flag, no option, and no argument-hint entry. A capability reachable only by
remembering a flag is a capability most operators do not have.

The findings-bounding rule is re-keyed from "this is the first review" to "the range is the full
pull request diff". That is required rather than incidental: a repeat pass has a full-PR range but
is not a first review, so the old wording would have it read the whole pull request and then bound
its findings back to the empty delta — full cost, no output.

Everything that suppresses duplicates is untouched. The holistic pass still prunes findings already
covered on the pull request and still dedupes across reviewers; manifest mode still fingerprints
PASS/FAIL comments by criterion id and finding substance. That is what makes a repeat review the
delta rather than a duplicate wall, and it means a second read that simply concurs posts nothing.
The cycle summary gains the split between findings newly surfaced and findings dropped as already
covered, so a silent concurring pass is distinguishable from one that never ran.

The judgment pass's once-per-PR gate is deliberately left alone. A repeat review contributes defect
and contract findings; it does not re-ask a premise question a human already answered.

## Alternatives Considered

- **An explicit opt-in flag** (`--re-review`, alongside a reviewer-model selector): rejected. It
  puts the capability behind something the operator has to know exists, and re-invoking the skill
  already carries the intent unambiguously. It also grows the operator surface for a behavior that
  needs no configuration.
- **Remove the unchanged-head check everywhere, loop wakes included**: rejected. The loop's exit
  condition would never fire, and one commit would be re-reviewed for the loop's full 24-hour life —
  the unbounded verification `docs/CUSTOMER.md` (since absorbed into `NORTH_STAR.md`) names as a workflow defect rather than a cost the
  user should watch.
- **Do nothing**: rejected on evidence rather than preference. Both clauses read durable GitHub
  state, so no session-level workaround reaches them and the capability did not exist by any route.
- **Also lift the judgment pass's once-per-PR gate**, so a repeat review contributes a fresh premise
  read: rejected as a separate decision from this one. Its gate exists so an answered question is
  not re-asked, and trading that guarantee is not what a repeat review was asked for.

## Consequences

### Positive

- A risky change can be reviewed twice over the same commit, from separate invocations under
  separate models, with the second pass surfacing only what the first missed.
- No new surface: nothing to learn, nothing to pass, nothing to keep in step across distributions.
- The bounding rule now keys on the range being the full pull request diff, which covers a first
  review and a repeat review from one condition instead of two.

### Negative

- A CI or webhook trigger that fires `review-pr` on a non-commit event is also the start of an
  invocation, so it now pays for a full review of an unchanged head instead of skipping. Accepted
  deliberately: the output is still bounded — a concurring pass posts nothing — but the tokens are
  spent. An operator wiring such a trigger should fire it on commit events.
- Nothing in GitHub state records which model produced which comment, so a later reader cannot
  attribute a comment to a particular pass. The cycle summary is transcript-only and the self-marker
  must stay a fixed literal for cross-host matching. Accepted rather than solved; a model name in a
  posted body would be an AI disclosure by another route.
- Concurrent invocations cannot prune against each other, since both read pull request state before
  either posts. Repeat reviews want to be run one after another.
- A repeat review cannot contest a thread an earlier pass resolved — the per-comment verifier runs
  only over unresolved threads. Reopening a human-visible resolution is nag-shaped, so this limit is
  kept deliberately.

## Source
- Related: `20260805-ratchet-judgment-gate-reverification`,
  `20260708-judgment-layer-is-a-review-time-premise-check`,
  `20260622-mark-review-pr-comments-with-hidden-marker`,
  `20260602-coordinate-review-pr-and-babysit-pr-through-pr-state`
