# ADR: figure-out speaks about the person's subject, weighs a fact they cannot supply by what rides on it, and shows its log path only when asked

## Status
Accepted

## Area
figure-out

## Decided by
The user (the owner): the three rulings quoted under Decision. An agent wrote this record and the
change under the owner's instruction to carry out the plan that holds them, and made the wording
choices listed under Decision within that plan. The owner has not reviewed the record's text.

## Context
A developer who had a feature in mind tried figure-out and went back to the tool he used before,
because he liked how it spoke. An investigation before this change drove figure-out on five
everyday prompts (in a scratch folder, outside this repository). On every prompt, figure-out
handed over its turns as a protocol:

- Replies opened with labels for their own parts: "Where things stand.", "The claim for this
  turn.", "The ask.", "My expected answer:".
- Sentences carried status tags: "verified", "inferred, not verified".
- The log path sat at or near the top of a reply, and the method was narrated.

In one test run the person answered "not sure, what do you think?" about a fact. The next reply
sent them on an errand: to ask a colleague three questions before the work could go on. The same
reply had said the design need not depend on that fact.

Each label was a phrase of the skill's own text shown back to the person. Two places supplied
them: the turn paragraph of `figure-out/SKILL.md` (the paragraph that says how a turn is handed to
the person) and its claim-standing bullet (the bullet that says how a claim's standing is voiced).
The "never… a fallback" wording on the ask came from one tuning round, `c2d70f0d`. That round's
graders rewarded the marks and counted no cost to the reader.

Four cases were written before any edit. Each was driven on the merge base, `c3e72d85`, and each
reply was graded by a fresh context from one grader file:

- `116-voice-feature-in-a-repo` (a feature request in a small repository) and
  `117-voice-plan-without-a-repo` (a plan with no repository, held out) judge the manner of a
  reply, with `speaks-about-the-subject` and `tells-checked-from-guessed`. The second grader judges
  a claim's footing: whether a reader can tell that the claim was read, inferred or guessed.
- `118-not-sure-a-shape-holds` covers a fact the person cannot supply where one shape of the work
  holds under every answer. `119-not-sure-nothing-safe` covers a fact where no shape holds and a
  wrong step cannot be undone. Each has several turns. `118` ends with the person asking where the
  log is.

On the merge base, `speaks-about-the-subject` failed every drive of the four cases, and every
reply showed the log path unasked. `118`'s errand did not reproduce. It was driven twice, the
second time with the contractor reachable in a day or two, and both replies designed for both
answers. The case is reported as not shown to catch the errand. Its grader fails a reply written
to send the person on the errand.

## Decision
The owner's rulings:

- **The manner of a reply** is the reply the owner chose from three real first replies to one
  prompt. It opens with the finding, has no label for its own parts, and says where it is guessing
  and how the guess could be checked. A prose ask ends with a question set apart and the reply's
  own answer as a guess.
- **A fact the person cannot supply** is split by what rides on it: "Decide-what-is-safe when
  some shape holds under every answer the fact could have. Ask-for-the-fact when no shape does, or
  when a wrong step could not be undone."
- **The investigation log path** is shown only when the person asks: "its not really releavnt
  unelss asked its for interla model use basically" [sic].

What ships, in the lines that owned the old behavior (wording choices made by the agent within
the plan):

- The turn paragraph states the voice as a colleague across a desk: the finding first, one new
  point per message, and, for a prose ask, the question in bold on its own line with the guess
  after it in a plain sentence.
- The method is how the run works, not what it says. No heading, lead-in or label names a part of
  the message or the run's work, and options carry no badge. The conversation is not narrated, and
  the reply uses no term of the skill the person has not been given.
- Every finding that bears on the decision goes in, as a plain sentence or bullet that says where
  it came from. A five-sentence example shows the voice. The read stays a report whose headings may
  name its parts.
- The one-ask rule keeps its ban on a fallback. When a fact is missing, what holds is a statement,
  not a fallback ask. A step that cannot be undone asks for the fact even where some shape holds.
- The claim-standing bullet keeps the verified, inferred and assumed classes and moves them into
  the sentence:
  - a fact read says where it was read;
  - an inference or estimate reads as the run's own;
  - what the person said stays theirs until checked;
  - a guess says how to check it.

  No tag or confidence label is set beside a sentence. A turn's leaning sentences are reread for
  footing before it goes out.
- `references/LOG.md` gives the path when the person running the session asks for it. It keeps
  the path out of every other reply, a list of files written included. `references/autonomous.md`'s
  read line defers to that rule.
- Small edits the same rules drove: the momentum line's "brief progress messages" became "brief
  messages on what you have found"; the decision-record offer in `references/WITH_DOCS.md` no
  longer names "the Decision Test result"; and the log's entry rule names what the skill carries
  instead of a "belief register" and "ledger" it no longer has.

Ten rounds of wording ran, each answering a failing drive or a review finding. The first wording
stated the target with no example, and runs wrote "What I found" headings, copying its own phrase
"open with what you found". The investigation's earlier probe wording ("the method is how you
work, not what you say") removed most labels, and a short example removed most of the rest.
Shorter turns then lost findings, and a blind comparison judged them worse on `116` and `118`.
This comparison read what each side found, checked and prevented, from the replies and the tool
calls. Wording that kept every finding brought the labels and unsourced claims back. Of the
wordings driven, tying each finding to its source served both best.

### Results
Every drive below was graded the same way. The merge base column counts every drive of the skill
before the change on the case as it now stands; the shipped text column counts drives on
`4334893b`. `6e0bf243` changed two clauses after that, and `119`, the one case they reach, was
driven on it once more. Each case got two drives on the shipped text: the second drive was the
further run the thinking comparison takes when one pair judges the shipped text worse, and it was
run for all four cases so each has two.

| Case | Grader | Merge base | Shipped text |
|---|---|---|---|
| `116` | `speaks-about-the-subject` / `tells-checked-from-guessed` | 0 of 2 / 0 of 2 | 2 of 2 / 1 of 2 |
| `117` (held out) | `speaks-about-the-subject` / `tells-checked-from-guessed` | 0 of 2 / 2 of 2 | 2 of 2 / 2 of 2 |
| `118` | `speaks-about-the-subject` / `tells-checked-from-guessed` / `a-way-forward` / `gives-the-log-path` | 0 of 2 / 0 of 2 / 2 of 2 / 2 of 2 | 0 of 2 / 1 of 2 / 2 of 2 / 2 of 2 |
| `119` | `speaks-about-the-subject` / `tells-checked-from-guessed` / `asks-for-the-fact` | 0 of 2 / 1 of 2 / 2 of 2 | 0 of 2 / 0 of 2 / 2 of 2 (on `6e0bf243`: pass / fail / pass) |

Across the four cases, `speaks-about-the-subject` passed 4 of 8 shipped-text drives, against 0
of 8 on the merge base. `tells-checked-from-guessed` passed 4 of 8, against 3 of 8, and fell on
`119` from 1 of 2 to 0 of 2. No new-case reply on the shipped text showed the log path unasked;
every new-case reply on the merge base did. Two drives per case still cannot settle these binary
graders, which move between runs on the same text.

The blind comparison of thinking, two pairs per case: `116`, `118` and `119` were not judged
worse. On `117`, held out, the shipped text was judged worse on both pairs. Its first reply raised
fewer of the plan's hazards: asking the team, a trial period, the day's lag before a written
blocker is seen. The merge-base replies listed these as points they would raise later; the shipped
text does not narrate what comes next.

The nine existing cases whose graders judge the turn were driven on `04b2eb92`, which differs from
`4334893b` only in the example's last sentence. No grader that passed on the merge base failed
there, after the further run each earlier flip got. A flip is a grader that passes on one side and
fails on the other. `22` `offers-a-draft-not-a-feeling` and `01` `presses-from-root` failed on
both sides. A reply showed the log path unasked in five of five sampled merge-base drives of these
cases and in one of eleven on `04b2eb92`; it was a reply to a prompt line saying where notes should
go.

The keep rule set in the eval README before the first drive was not met (see *Outcome of these
rules* there). The change goes to its pull request with these results, for the owner to keep or
send back.

## Alternatives Considered
- **A finding-first reply that keeps one label for the ask:** shown to the owner as one of three
  real replies and not chosen.
- **A reply with no guess:** not chosen; the reply the owner chose keeps its own answer.
- **Leaving the ask as it was and changing the voice only:** not chosen; the errand came from the
  ask line.
- **Always deciding what is safe, pressing for the fact while showing what is safe, or asking for
  the fact in every case as before:** offered to the owner and not chosen; he chose the split.
- **Showing the log path unasked, at the top of the first reply or at its end:** the end was the
  plan until the owner ruled that the path is for the model's own use.
- **A block of prohibitions beside the old lines:** the investigation's probe worked that way. The
  change carries the result inside the owning lines instead, so no two rules compete.
- **A design-partner mode that hands over a design without questioning it:** ruled out by the
  owner ("keep me honest"); not part of this change.

## Consequences

### Positive
- No reply on the shipped text opened with "Where things stand." or tagged a sentence "verified".
- The split for a fact the person cannot supply is in the text with both grounds for asking.
  `118` passed `a-way-forward` and `119` passed `asks-for-the-fact` on every drive, before and
  after the change.
- The existing graders that judge the turn hold.

### Negative
- The owner's bar is every reply, and the shipped text does not meet it. `118` and `119` failed
  `speaks-about-the-subject` on their shipped-text drives, through a "My guess:" label and a
  lead-in naming the run's own view. `tells-checked-from-guessed` failed four of eight
  shipped-text drives, each on an estimate or a fact from a file stated with no source under a
  recommendation.
- On `117` the comparison judged the first reply worse at raising the plan's hazards. Whether a
  list of points to raise later counts as disclosure is the owner's call. He had dropped "show the
  breadth" as giving only a feeling of progress.
- `118` was never shown to catch the errand. The decide-what-is-safe rule rests on its text and on
  `118` holding.
- `117` is tuned on: the wording changed after its first drive on the changed text, though no
  wording was drawn from its replies.
- The body of `figure-out/SKILL.md` grew from 3,342 to 3,823 words.

## Enforced by
partly — eval cases under `claude-plugins/manifest-dev/evals/`, driven through
`verification/recipes/figure-out.md`:

- `116-voice-feature-in-a-repo` and `117-voice-plan-without-a-repo` hold the manner: no label for
  the message's parts or method, no term of the skill the person was not given, no status tag, and
  every claim's footing legible.
- `118-not-sure-a-shape-holds` holds a way forward when a shape holds, and the log path given
  when asked. It was not shown to catch the errand, so it guards only against a reply that sends
  the person away for the fact.
- `119-not-sure-nothing-safe` holds asking for the fact when nothing is safe.

Each case carries a comment citing this record. Whether a reply reads like a colleague stays
judgment.

## Revisit when
A person reports that figure-out's replies read as a protocol again, or several drives per case on
`116` to `119` show the manner graders failing on most runs, read in this record's results table or
in the eval README once a suite runs.

## Source
- Session: an investigation into why a person chose another interview tool, followed by `/define`
  and `/do`, 2026-11-19 and 2026-11-20.
- Related: amends 20260803-figure-out-turn-carries-one-concrete-claim; amends
  20260809-figure-out-budgets-the-whole-turn-not-its-bold-lines; amends
  20260611-figure-out-evidence-ledger-and-independent-rederivation; amends
  20260810-universal-discipline-belongs-in-the-prompt; amends
  20261025-figure-out-records-what-the-lean-body-rebuild-retired; see also
  20261012-figure-out-writes-in-simplified-technical-english-by-default,
  20260726-figure-out-narrows-presentation-no-trim-clause,
  20261102-an-addition-that-costs-every-run-earns-its-place-by-evidence
