# Building, proving and using an AI judge in a climb

Read this when a climb's measure is an AI judge: a model that compares two versions of the
artifact and says which one better serves the goal. It applies to any artifact — a page, copy, a
prompt's outputs, a plan, a simulation's rendered behavior. Every practice below is a default;
the requester's words replace it, and the climb's report names each one changed.

## The brief

Every judge's brief has the same parts:

- **The goal**, and **the people served and their moment**: in the requester's own words, or as
  an unattended climb inferred them. Ground the people in what they want and what is at stake for
  them, not in a demographic sketch.
- **The artifact as those people meet it**: the rendered page in the states they see it in, the
  outputs a prompt produces, the text as read, the simulation as watched.
- **A verdict between two versions**: which better serves the goal for those people, or a tie.

The judge is shown no example version — neither a target to imitate nor a past pair as a worked
example. A requester's reasons reach it only as criteria. Facts, figures and other protected
parts are kept out of the verdict: they are checked on their own, since judges often miss a
quality drop inside a version they otherwise prefer.

Before the verdict, the judge may assess each version alone. Choose the form per task:

- **Criteria fixed first, each version assessed alone, then the verdict.** The default for open
  goals: committing to criteria before seeing the pair, and reasoning about each version before
  comparing, resists a version that only looks better.
- **A score per criterion** where the criteria are several and their trade-off matters to the
  report.
- **No per-version assessment** where the goal is one plain question and the proof shows the
  verdict stable without it.

Ask for evidence before the verdict, never the verdict first.

## Proving the judge before round 1

Prove the judge on the model the climb runs, with the brief frozen.

- **A degraded version loses.** Make a version clearly worse on the goal; the judge must prefer
  the original.
- **A gain-sized pair is told apart.** Record the gain sought — the requester's, or inferred and
  labeled so — and pair the original with a version carrying one known change of about that
  size; the judge picks the better one. The record names the pair and why its order is known.
- **Identical versions tie.**
- **Noise is recorded.** Note how often the verdict flips with the order of the two versions and
  between runs of the same comparison.

A quick climb runs only the first check, on one degraded version. A thorough climb runs all four.
Every comparison, in either, judges both orders and counts a win only when both agree; a split is
a tie.

From the recorded noise and the cost of a vote, the proof sets the minimum votes a comparison
takes, the lead that counts as clear, and a cap. A judge that cannot tell the gain-sized pair apart within the cap stops the
climb before round 1, and the report says what failed and what would fix it.

When the judge weighs several objectives, break each criterion on purpose before round 1: the
broken version must lose on that criterion and must not win the overall verdict.

## Guards the proof turns on

Protected parts are never left to the judge: every candidate passes plain pass-or-fail checks on
them before it can be kept.

The guards below protect against failures a fixed test may not show. They are off by default;
turn one on where the proof or the record shows the failure it prevents, or where the requester
asks:

- **Hide which version is newer, who made it, and the climb's history** — when the judge leans
  toward the newer or its own model's version, as the identical-versions check shows when one
  copy is labeled newer.
- **A fresh judge for each vote**, with no memory of earlier votes — when the record shows
  verdicts on a repeated comparison drifting as a session goes on.
- **Show several rendered states of a page**, plus its text and structure — when a single
  screenshot hides what the people meet, such as a hover, an error or a narrow screen.

## Teaching the judge, by the kind of goal

- **The requester's own taste, or how well the artifact serves its people in a climb they will
  repeat:** in a thorough climb, offer calibration to their picks. Make versions around the
  original and have the requester choose between pairs, each with a reason. Some picks teach:
  their reasons become the judge's criteria. The rest are held out and checked once, against a bar
  set before checking, and each disagreement is shown to the requester. On a miss, they re-teach
  with fresh picks or choose another measure, or the climb stops before round 1. The report states
  the agreement measured.
- **A behavior of the people served:** where the requester has past results from real use, such
  as earlier A/B tests, prove before round 1 that the judge predicts which version did better.
  Without them, the report says the judge's accuracy at predicting real outcomes was not
  measured, and calls any gain in the behavior a prediction.
- **Unattended:** use only what the request already holds; the report says what taught the judge.

Keep the judge's brief in the climb's record, so a re-run reuses it.

## Voting

Votes run to the minimum the proof set, then continue until one side leads by the clear margin or
the cap is reached. A result short of clear is a tie, and a tie keeps the current best. A new leader is confirmed on fresh votes before it
becomes the current best.

## What the proposer sees

The work that proposes changes learns from outcomes and from which of the judge's criteria each
version met or missed — never from the judge's own words, which it would learn to please. Where
the host can run the judge in a separate context, it does, and returns only the verdict and each
criterion met or missed; where it cannot, the report says the proposer saw the judge's words.

## Independent of the loop

The final comparison against the original uses a judge that took no part in the rounds and has
no climb history, its brief fixed before round 1. In a thorough climb it comes from another
model family where the host offers one; in a quick climb it is a fresh judge comparing the two
versions in both orders. A judge from another family is still only a partial guard: where real
outcomes, the requester or plain checks can audit the winner, use them too.
