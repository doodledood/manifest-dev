# ADR: figure-out speaks about the person's subject, weighs a fact they cannot supply by what rides on it, and shows its log path only when asked

## Status
Accepted

## Area
figure-out

## Decided by
The user — the three rulings quoted under Decision. An agent wrote this record and the change
under the user's instruction to carry out the plan that holds them; the user has not reviewed the
record's text.

## Context
A developer who had a feature in mind tried figure-out and went back to another interview tool
because he liked the way it spoke more. Driven on five everyday prompts, figure-out handed over
its turns as a protocol: replies opened with labels for their own parts ("Where things stand.",
"The claim for this turn.", "The ask.", "My expected answer:"), sentences carried status tags
("verified", "inferred, not verified"), the log path sat at or near the top, and the method was
narrated. When a person in a test run answered "not sure, what do you think?" about a fact, the
next reply sent them to a colleague with three questions, although the same reply had said the
design need not depend on that fact. The findings under the labels were the best-proven of the
tools compared. Each label was a phrase of the turn paragraph or the claim-standing bullet shown
back to the person, and the "never… a fallback" wording on the ask dates from one tuning round
whose graders rewarded the marks and counted no cost to the reader.

Four cases were written before any edit and driven on the skill at the merge base, each reply
graded by a fresh context from one grader file:

- `116` (a feature request in a small repository) and `117` (a plan with no repository, held
  out) judge the manner of a reply: `speaks-about-the-subject` and `tells-checked-from-guessed`.
- `118` (a fact the person cannot supply, where a shape of the work holds under every answer)
  and `119` (one where no shape holds and a wrong step cannot be undone), several turns each.
  `118` ends with the person asking where the log is.

On the merge base `speaks-about-the-subject` failed every one of the four cases, and every reply
showed the log path unasked. `118`'s errand did not reproduce: on two drives, the second with the
contractor reachable in a day or two, the reply designed for both answers. The case is reported
as not shown to catch; its grader fails a reply written to send the person on the errand.

## Decision
The owner's rulings:

- **The manner of a reply** is the plain-colleague reply he chose from three real first replies
  to one prompt: it opens with the finding, has no label for its own parts, says where it is
  guessing and how the guess could be checked, and ends a prose ask with a question set apart and
  its own answer as a guess.
- **A fact the person cannot supply** is split by what rides on it: "Decide-what-is-safe when
  some shape holds under every answer the fact could have. Ask-for-the-fact when no shape does, or
  when a wrong step could not be undone."
- **The investigation log path** is shown only when the person asks: "its not really releavnt
  unelss asked its for interla model use basically".

What ships, in the lines that owned the old behavior:

- `figure-out/SKILL.md`'s turn paragraph states the voice as a colleague across a desk: the
  finding first, one new point per message, and the question in bold on its own line with the
  guess after it in a plain sentence. The method is how the run works, not what it says: no
  heading, lead-in or label names a part of the message or the run's work, options carry no
  badge, the conversation is not narrated, and every finding that bears on the decision goes in
  as a plain sentence or bullet that says where it came from. A four-sentence example shows it.
  The read stays a report whose headings may name its parts. The one-ask rule keeps its ban on a
  fallback; what holds when a fact is missing is a statement, not a fallback ask.
- The claim-standing bullet keeps the verified, inferred and assumed discipline and moves it into
  the sentence: a fact read says where, an inference or estimate reads as the run's own, what the
  person said stays theirs until checked, a guess says how to check it, and no tag or confidence
  label is set beside a sentence. A turn's leaning sentences are reread for footing before it goes
  out.
- `references/LOG.md` gives the path when the person running the session asks and keeps it out
  of every reply otherwise, a list of files written included; `references/autonomous.md`'s read
  line defers to that rule.

Each later wording answers a failing drive or a review finding, ten rounds in all. The first
wording stated the target with no example, and runs wrote "What I found" headings, taken from its
own phrase "open with what you found". The investigation's earlier probe shape ("the method is how
you work, not what you say") removed most labels, and a short example removed most of the rest.
Shorter turns then lost findings. A blind comparison of what each arm found, read with the tool
calls, judged them worse on `116` and `118`. Wording that kept every finding brought the labels and
unsourced claims back. Tying each finding to its source served both best of the wordings driven.

Results on the shipped text (`4334893b`): two drives per new case, each reply graded by a fresh
context from one grader file. The merge base column counts every drive of the skill before the
change on the case as it now stands.

| Case | Grader | Merge base | Shipped text |
|---|---|---|---|
| `116` | speaks about the subject / tells checked from guessed | 0 of 2 / 0 of 2 | 2 of 2 / 1 of 2 |
| `117` (held out) | speaks about the subject / tells checked from guessed | 0 of 2 / 2 of 2 | 2 of 2 / 2 of 2 |
| `118` | speaks / tells / a way forward / gives the log path | 0 of 2 / 0 of 2 / 2 of 2 / 2 of 2 | 0 of 2 / 1 of 2 / 2 of 2 / 2 of 2 |
| `119` | speaks / tells / asks for the fact | 0 of 2 / 1 of 2 / 2 of 2 | 0 of 2 / 0 of 2 / 2 of 2 |

No new-case reply on the shipped text showed the log path unasked; every new-case reply on the
merge base did. A single drive of these binary graders moves between runs on the same text, so the
counts are the result, not any one verdict.

The blind comparison of thinking, two pairs per case: `116`, `118` and `119` were not worse. On
`117`, held out, the shipped text was judged worse on both pairs. The merge-base replies listed the
points they would raise later (asking the team, a trial period, the day's lag before a blocker is
seen), and the shipped text, which does not narrate what comes next, raised fewer of them in its
first reply.

The nine existing cases whose graders judge the turn were driven on `04b2eb92`, which differs from
the shipped text only in the example's last sentence. No grader that passed on the merge base
failed there, after the further run each earlier flip got. `22` `offers-a-draft-not-a-feeling` and
`01` `presses-from-root` failed on both. The unasked log path dropped from five of five sampled
merge-base replies to one of eleven; it was in a reply to a prompt line saying where notes should go.

## Alternatives Considered
- **A finding-first reply that keeps one label for the ask:** shown to the owner as one of three
  real replies and not chosen.
- **A reply with no guess:** not chosen; the owner's reference keeps its own answer.
- **Leaving the ask as it was and changing the voice only:** not chosen; the ask line was where
  the errand came from.
- **Always deciding what is safe, or pressing for the fact while showing what is safe, or asking
  for the fact in every case as before:** offered to the owner and not chosen; he chose the split.
- **Showing the log path unasked, at the top of the first reply or at its end:** the second was
  the plan until the owner ruled the path is for the model's own use.
- **A block of prohibitions beside the old lines:** the investigation's probe worked that way; the
  repair carries the result inside the owning lines instead, so no two rules compete.
- **A separate design-partner mode that hands over a design without questioning it:** ruled out by
  the owner ("keep me honest"); not part of this change.

## Consequences

### Positive
- Replies read as a person talking about the person's problem: on the shipped text no reply opened
  with "Where things stand." or tagged a sentence "verified", and `speaks-about-the-subject`
  passed four of eight new-case drives against none of eight before.
- The don't-know split is in the text with both grounds for asking, and `118` and `119` passed
  their split graders on every drive on both arms.
- The existing graders that judge the turn hold.

### Negative
- The owner's bar is every reply. On the shipped text the manner and footing graders still fail
  some replies: `118` and `119` failed `speaks-about-the-subject` on both drives (a "My guess:"
  label, a lead-in naming the run's view), and one estimate stated flat under a recommendation
  still fails `tells-checked-from-guessed`. The record does not claim the bar is met.
- On `117` the comparison judged the first reply worse at disclosure: it no longer lists the points
  it will raise later. Whether a list of later points counts as disclosure is the owner's call; he
  had dropped "show the breadth" as giving only a feeling of progress.
- One drive per arm cannot settle these binary graders; deciding them needs several drives per
  case.
- `118` was never shown to catch the errand, so the decide-what-is-safe rule rests on its text and
  on `118` holding.
- `117` is tuned on: the wording changed after its first after-arm drive, though no wording was
  drawn from its replies.
- The always-loaded body grew from 3,416 to 3,888 words.

## Enforced by
partly — eval cases under `claude-plugins/manifest-dev/evals/`, driven through
`verification/recipes/figure-out.md`: `116-voice-feature-in-a-repo` and
`117-voice-plan-without-a-repo` (no label for the message's parts or method, no status tag, every
claim's footing legible), `118-not-sure-a-shape-holds` (a way forward when a shape holds; the log
path given when asked) and `119-not-sure-nothing-safe` (ask for the fact when nothing is safe).
Each carries a comment citing this record. Whether a reply reads like a colleague stays judgment.

## Revisit when
A person reports that figure-out's replies read as a protocol again, or several drives per case
on `116` to `119` show the manner graders failing on most runs, read in the eval README's results.

## Source
- Session: a figure-out investigation into why people choose other interview skills, followed
  by `/define` and `/do`, 2026-11-19 and 2026-11-20.
- Related: amends 20260803-figure-out-turn-carries-one-concrete-claim; amends
  20260611-figure-out-evidence-ledger-and-independent-rederivation; amends
  20260810-universal-discipline-belongs-in-the-prompt; amends
  20261025-figure-out-records-what-the-lean-body-rebuild-retired; see also
  20261012-figure-out-writes-in-simplified-technical-english-by-default,
  20260726-figure-out-narrows-presentation-no-trim-clause,
  20261102-an-addition-that-costs-every-run-earns-its-place-by-evidence
