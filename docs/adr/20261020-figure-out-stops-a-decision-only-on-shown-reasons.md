# ADR: figure-out stops analysing a decision only on shown reasons

## Status
Accepted

## Area
Task guidance

## Decided by
The user

## Context

The *Value of information* probe in `figure-out/tasks/DECISION.md` (see 20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures) ended with an imperative: "If none would — or the options are close, the downside small, quitting cheap — pick, and stop analysing." It came from Duke's happiness test and quit cost, and it is there to stop a small, undoable choice from getting a full decision analysis.

Read as written, it also licenses stopping on how a choice *looks*. Options can look close and not be: two options with equal averages can differ in what their worst case does, as when one carries an outcome that ends the game. The old sentence let "the options are close" be asserted and acted on in one step. Read with the rest of the file, the risk is a read that names the stop condition and skips the work that would show whether it holds — the laziness the stop was meant to prevent in the other direction.

## Decision

- **The last sentence becomes a question whose answer needs reasons:** "If none would, or a wrong pick would cost little — the options come out close, the downside small, quitting cheap — is it time to pick, and has the work shown that, worst case included, rather than assumed it?" The head, "a wrong pick would cost little", says why the three conditions license a stop, so equal averages over a ruinous worst case do not. "Come out close" makes closeness a result of the work, not an impression, and the closing clause asks the read to show it, worst case included.
- **The stop stays.** A small choice that is cheap to undo still ends quickly; the change asks for the reason to be visible, not for more analysis.
- **Two eval cases test it from both sides.** `63-decision-close-call-is-not-close` gives equal averages over a ruinous downside and fails a read that calls it a toss-up and picks; `64-decision-small-and-undoable` gives a cheap, returnable choice whose user asks only which to order, and fails a read that wraps the pick in analysis or asks instead of picking. Each has a scenario in `verification/recipes/figure-out.md`.

## Alternatives Considered

- **Leave the imperative**: Rejected by the user — it reads as permission to stop on an impression.
- **The question followed by "Then pick, and stop analysing."**: Rejected — an imperative after the question would again let the stop be taken as an order rather than a conclusion the work reaches.
- **Delete the stop clause**: Rejected — without it the probe file has no counterweight, and a small choice gets the whole file.
- **A separate probe for "is it really close?"**: Rejected — it would add a fourteenth probe for a clause that belongs inside *Value of information*, beside the flip chance it depends on.

## Consequences

### Positive
- A read can no longer stop on "these look close" without showing it, and the pair of cases catches a change that makes figure-out either lazy or ceremonious.

### Negative
- The sentence is longer and a question, so a model may read it as one more thing to answer on a choice where the answer is plain; case 64 is there to catch that.
- Neither case has run in the suite, so the arms are not compared. Each had one drive on the final wording, and both passed their graders on reading: in `63` the read refused the coin-flip framing, showed that a bad year now risks a land sale, and recommended the contract or a partial contract; in `64`, driven on the prompt as it now stands, the read led with ordering both lamps and returning one, named the clamp-on as the single pick with a short reason, and ran no decision method. It still carried a user's-call list, overturn conditions and a note on an independent check, which is more than a lamp needs; the suite run will show whether the plugin arm reads heavier than the base model.

## Enforced by
partly — eval cases `63-decision-close-call-is-not-close` and `64-decision-small-and-undoable`, and the `decision-close-call` and `decision-small-choice` scenarios in `verification/recipes/figure-out.md`, check both directions of the stop; the wording stays judgment.

## Source
- Session: a review of whether the decision probes would make figure-out lazy (2026-10-20), followed by an autonomous run that reworded the clause and added the cases.
- Related: amends 20261019-figure-out-probes-decisions-and-plans-under-uncertain-futures; see also 20261020-every-figure-out-probe-has-an-eval-grader-or-a-stated-reason
