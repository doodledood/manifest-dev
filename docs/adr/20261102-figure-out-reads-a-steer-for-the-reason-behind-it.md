# ADR: figure-out reads a steer for the reason behind it, and offers to keep a reason it named

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context

The user reported that when they steered or corrected a figure-out session, the session took the
words as an order about one item. figure-out's spine already said that an answer carrying an aim or a reason resets
the next recommendation (`20261102-experience-choices-go-to-the-user-as-options-or-variants`). It
said nothing about a correction that gives no reason, which is the common case. Such a correction
often comes from a principle the user holds and has not said, and that principle decides other
choices in the same session. A session that obeys the one item and keeps the rest of its plan
makes the user correct each of the others in turn.

Four failures were named: the session fixes only the item it was told about and keeps making the
same kind of choice elsewhere; it accepts a steer the evidence argues against; it rarely asks what
is behind a steer; and the next session starts without the principle, so the same correction comes
back. On how to find the reason, the user chose that the session guesses it, says the guess in a
line, and asks only when the guess is unclear. The user also asked that a principle found this way
be offered for keeping as Taste.

Taste capture already took a single reversal when the user stated the reason, and refused one with
no stated reason (`20261012-taste-is-checked-per-call-and-captured-from-explained-reversals`).
That record also rejected inferring the reason behind a reversal, because an inferred reason can
only be obeyed, not weighed, and it stops the pushback that would correct it.

This decision sits inside what the North Star's *Purpose* names: keeping the choices a person
retains available to later sessions without restoring them each time.

## Decision

- **figure-out's spine.** A steer or correction, with a reason or without one, is evidence of how
  the user judges, not only an order about one item. Where no reason is given, the session names in
  a line the reason it infers and the other choices that reason changes. Where two plausible
  reasons would change those choices in opposite ways, it asks one short question that names both
  and what each changes, before it changes them. It asks about a reason once: when the user moves
  on without answering, what they do next is the answer, and the session takes the reading it
  supports instead of asking again or listing the reason as open. It weighs the reason against the evidence as it
  weighs any position. Then it reasons the next recommendation, and every choice the reason bears
  on, again from it. This replaces the spine's sentence on an answer with an aim or a reason.
- **Taste.** Corrections that share one reason the user never stated count as recurring once the
  session has named that reason, so they can become a Taste offer. The offer may build its
  rationale on the reason the session named, and says that it is the session's reading, so the
  user's yes to the text confirms it. A named reason the user never confirmed is a candidate for
  the sweep before the read, so the offer, not another question, is where the user confirms it. A single correction whose reason the user did not state
  is still not Taste, even once the session has named one, and an offer never presents as the user's a reason they neither stated nor
  confirmed.

The rejected alternative of the 20261012 record stays rejected in the form it named. The reason is
said to the user when it is inferred, which keeps it open to pushback, and it is written only after
the user says yes to the exact text, which turns the inference into a confirmed reason.

## Evidence at decision time

Each drive ran through the `figure-out` recipe; the before arm ran the skills at the merge base
(`DRIVE_PLUGINS_AT=3646a4a`). Replies to `107`, `108` and `105` were graded in one blind pass after
the graders' last edit, by grader sessions that saw each reply under a random label only; `100`'s
two replies were graded blind in an earlier pass under its unchanged grader. A case passes when the run after the change passes and the
run before it does not, by majority of three where one pair does not settle it.

| Case | Before the change | After the change (the shipped wording, counted with the commit before it, which differs only in the rule for a single unexplained correction) |
|---|---|---|
| `107` two corrections with no reason, one principle behind both | FAIL: named the reason and applied it, but made no offer to keep it | PASS in 2 of 4; both failures made the offer, one without naming where it would keep it (borderline), one recommending a push on by default |
| `108` one correction with two readings that change the rest in opposite ways | PASS in 3 of 3, all borderline: the question only loosely separated the readings | PASS in 3 of 3 |
| `100` a steer resets the recommendation (guard) | — | PASS in 1 of 1, and 1 of 1 on the earlier wording 77c7c2e |
| `105` a revealed yardstick offered as Taste (measurement) | — | FAIL in 1 of 1, and 1 of 1 on the earlier wording 77c7c2e |

Neither case settles the change by that rule. On `107` the skills before the change already named
the reason and changed the other choices; what they lacked was the offer, which every run after the
change made, saying the reason was its own reading. Two earlier wordings asked about the reason more than once in 3 of
4 runs; the shipped wording asked once in all 4. `108` passes on
both sides, so it shows no uplift for the one-question rule. `105` still fails: an offer drawn from a
yardstick the user reveals is a different behavior, which this change does not claim.

The user chose to ship on this evidence rather than spend more drives settling `107` or drop the
one-question clause: the offer and asking once, the two behaviors the request turned on, moved
clearly, and the bar the cases set stays recorded here as unmet.

## Alternatives Considered

- **Ask the user why on every unexplained correction**: it puts a question on each steer, though
  most corrections have one plausible reason; the user chose a guess said aloud, with a question
  only when the guess is unclear.
- **Infer the reason silently and act on it**: the 20261012 record's grounds hold; a reason the
  user never sees can only be obeyed, and nothing corrects it.
- **Change only the Taste reference**: driven once on `107`; the session asked about the reason three times and made no offer.
- **Leave figure-out as it is**: the user named all four failures as worth fixing, and `107` failed
  before the change for want of the offer.

## Consequences

### Positive
- One unexplained correction can fix several choices at once, so the user corrects less.
- A principle the user never stated can become standing context with one yes.
- The inferred reason is on the page, so the user can correct it before it shapes the rest.

### Negative
- Every unexplained steer now costs a line of inference in the session's reply.
- A wrong inference, said with confidence, can steer the next choices before the user reads it;
  the one-line statement is the only guard.
- `/define` and `/do` still take only a stated reason for a Taste offer; this change covers
  figure-out alone.

## Enforced by
none — whether a session reads a steer for its reason is prompt behavior; cases `107`, `108` and `100` measure it when driven, and no property test can hold it.

## Source
- Session: a `/figure-out`, `/define` and `/do` session on reading the user's steers, 2026-11-02.
- Amends 20261102-experience-choices-go-to-the-user-as-options-or-variants: the spine's sentence on an answer with an aim or a reason is replaced by one that covers every steer, with or without a reason.
- Amends 20261012-taste-is-checked-per-call-and-captured-from-explained-reversals: corrections sharing a reason the session named, and the user confirmed by saying yes to the offer's text, now qualify.
- Related: 20260719-taste-persists-by-offer-and-ratify, 20261102-taste-stays-a-section-of-the-memory-file
