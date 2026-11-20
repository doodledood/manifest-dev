# ADR: figure-out speaks about the person's subject, weighs a fact they cannot supply by what rides on it, and shows its log path only when asked

## Status
Accepted

## Area
figure-out

## Decided by
The user (the owner): the three rulings under Decision. An agent wrote this record and the
change under the owner's instruction to carry out the plan that holds them, and made the wording
choices listed under Decision within that plan. The owner has not reviewed the record's text.

## Context
A developer who had a feature in mind tried figure-out and went back to the tool they used before,
because they liked how it spoke. An investigation before this change drove figure-out on five
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
graders rewarded the labels and tags and counted no cost to the reader.

The three rulings below are one decision because they share that cause: each is a part of the
skill's own working shown to the person in place of what it found about their subject, whether a
label, a tag, an errand set by the ask rule, or the path of the run's own notes.

Four cases were written before any edit. Each was driven on the merge base, `c3e72d85`, and each
reply was graded by a fresh context from one grader file:

- `116-voice-feature-in-a-repo` (a feature request in a small repository) and
  `117-voice-plan-without-a-repo` (a plan with no repository, held out) judge the manner of a
  reply, with `speaks-about-the-subject` and `tells-checked-from-guessed`. The second grader judges
  a claim's footing: whether a reader can tell that the claim was read, inferred or assumed.
- `118-not-sure-a-shape-holds` covers a fact the person cannot supply where one shape of the work
  holds under every answer. `119-not-sure-nothing-safe` covers a fact where no shape holds and a
  wrong step cannot be undone. Each has several turns. `118` ends with the person asking where the
  log is.

On the merge base, `speaks-about-the-subject` failed every drive of the four cases, and every
reply showed the log path unasked. `118`'s errand did not reproduce. It was driven with the contractor away for a month,
then, the case repaired, twice with the contractor reachable in a day or two; every reply designed
for both answers. The case is reported as not shown to catch the errand. Its grader fails a reply written
to send the person on the errand.

## Decision
The owner's rulings:

- **The manner of a reply** follows a real first reply chosen as the reference. It opens with the
  finding, has no label for its own parts, and says where it is assuming and how the assumption
  could be checked. A prose ask ends with a question set apart and the reply's own answer as a
  guess.
- **A fact the person cannot supply** is split by what rides on it. Where some shape of the work
  holds under every answer the fact could have, the reply says what is safe and goes on. Where no
  shape does, or a wrong step could not be undone, it asks for the fact.
- **The investigation log path** is shown only when the person asks. The log serves the run's own
  continuity; its path tells the person nothing about their subject.

What ships, in the lines that owned the old behavior (wording choices made by the agent within
the plan):

- The turn paragraph states the voice as a colleague across a desk: the finding first, one new
  point per message, and, for a prose ask, the question in bold on its own line with the guess
  after it in a plain sentence, which may say what it rests on.
- The method is how the run works, not what it says. No heading, lead-in or label names a part of
  the message or the run's work, and options carry no badge; through a host's question tool, the
  guess goes in the recommended option's description. The conversation is not narrated, and
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
  - an assumption says how it could be checked.

  No tag or confidence label is set beside a sentence. "Guess" keeps one meaning: the run's own
  answer to its question.
- `references/LOG.md` gives the path when the person running the session asks for it. It keeps
  the path out of every other reply, a list of files written included. `references/autonomous.md`'s
  read line defers to that rule.
- Small edits the same rules drove: the momentum line's "brief progress messages" became "brief
  messages on what you have found"; the decision-record offer in `references/WITH_DOCS.md` no
  longer names "the Decision Test result"; and the log's entry rule names what the skill carries
  instead of a "belief register" and "ledger" it no longer has.

The wording rests on drives of the four cases. A target stated with no example led runs to copy its
phrases as headings ("What I found" from "open with what you found"). Stating the method as how the
run works, not what it says, removed most labels, and a short example removed most of the rest.
Shorter turns lost findings, and a blind comparison of the shorter wording judged it worse on `116`
and `118`; that comparison read what each side found, checked and prevented, from the replies and
the tool calls. Keeping every finding that bears on the decision, each tied to its source, served
the voice and the thinking best of the wordings driven.

### Results
Every drive below was graded the same way. The merge base column counts every drive of the skill
before the change on the case as it now stands. The changed-text column counts drives on
`57fd046d`: the pass rules set one drive per side, and each case got a second because the
thinking comparison below takes a second pair whenever one pair judges the changed text worse,
and that was run for all four cases so each has two. The last column counts drives after `main`
was merged in (`2293436d`), which added a before-and-after table to the read and left the turn
wording unchanged; each case was driven once, and `116` twice for its second thinking pair.

| Case | Grader | Merge base | `57fd046d` | After merging `main` |
|---|---|---|---|---|
| `116` | `speaks-about-the-subject` | 0 of 2 | 2 of 2 | 2 of 2 |
| `116` | `tells-checked-from-guessed` | 0 of 2 | 0 of 2 | 1 of 2 |
| `117` (held out, tuned on) | `speaks-about-the-subject` | 0 of 2 | 1 of 2 | 0 of 1 |
| `117` (held out, tuned on) | `tells-checked-from-guessed` | 2 of 2 | 2 of 2 | 0 of 1 |
| `118` | `speaks-about-the-subject` | 0 of 2 | 0 of 2 | 0 of 1 |
| `118` | `tells-checked-from-guessed` | 0 of 2 | 0 of 2 | 0 of 1 |
| `118` | `a-way-forward` | 2 of 2 | 1 of 2 | 1 of 1 |
| `118` | `gives-the-log-path` | 2 of 2 | 2 of 2 | 1 of 1 |
| `119` | `speaks-about-the-subject` | 0 of 2 | 1 of 2 | 0 of 1 |
| `119` | `tells-checked-from-guessed` | 1 of 2 | 0 of 2 | 0 of 1 |
| `119` | `asks-for-the-fact` | 2 of 2 | 2 of 2 | 1 of 1 |

Across the four cases, `speaks-about-the-subject` passed 6 of 13 drives on the changed text,
against 0 of 8 on the merge base, and `tells-checked-from-guessed` passed 3 of 13, against 3 of 8.
The text two edits before `57fd046d`, `4334893b`, passed `tells-checked-from-guessed` 4 of 8; the
two edits since (`6e0bf243`, and `57fd046d`, which also removed a step that reread a turn's
sentences for their footing) cannot be told apart from run-to-run variation at two drives per
case. One `118` drive on `57fd046d` failed `a-way-forward`: on the second turn its reply designed
for the fact the person could not supply, then asked them to email the contractor about a second
fact, whether notices can be faked. No new-case reply on the changed text showed the log path
unasked; every new-case reply on the merge base did.

The blind comparison of thinking judged the changed text worse on both pairs of no case, on
`57fd046d` or after the merge. It judged the changed text worse on one pair of `116` on each, and
on one pair of `117` on `57fd046d`; it judged the merge base worse on both pairs of `118`.

The nine existing cases whose graders judge the turn were driven on `57fd046d`, and the two whose
graders judge the read, `11` and `16`, again after the merge. No grader that passed on the merge
base failed. `01` `presses-from-root` passed, where it failed on the merge base; `22`
`offers-a-draft-not-a-feeling` failed on both. A generic `speaks-about-the-subject` grader passed
six of the seven attended existing cases, against none on the merge base; the one failure named
its notes file in reply to the prompt's line saying where notes should go, and that was the only
reply of the nine to name it.

The keep rule set in the eval README before the first drive was not met (see *Outcome of these
rules* there).

## Alternatives Considered
- **A finding-first reply that keeps one label for the ask:** not chosen; the label still names a
  part of the reply rather than something in the person's subject.
- **A reply with no guess:** not chosen; without the reply's own answer the person carries the
  whole decision, and the guess is where the run's judgment shows.
- **Leaving the ask as it was and changing the voice only:** not chosen; the errand came from the
  ask line's ban on anything but the one ask.
- **Always deciding what is safe:** not chosen; it would start a step that cannot be undone
  without the fact it turns on.
- **Asking for the fact in every case, as before:** not chosen; where a shape holds under every
  answer, the errand stops work that need not wait.
- **Pressing for the fact while showing what is safe:** not chosen; it is the errand with a
  softer opening, and still leaves the person with a task the work does not need.
- **Showing the log path unasked, at the top of the first reply or at its end:** not chosen; it
  puts something about the run's own notes, not the person's subject, into every reply.
- **A block of prohibitions beside the old lines:** not chosen; the change carries the result
  inside the owning lines, so no two rules compete.
- **A design-partner mode that hands over a design without questioning it:** not chosen; the
  skill's questioning of the solution is its purpose, and this change touches only how a reply
  reads.

## Consequences

### Positive
- No reply on the changed text opened with "Where things stand." or tagged a sentence "verified".
- The thinking held: the blind comparison judged the changed text worse on both pairs of no case.
- The split for a fact the person cannot supply is in the text with both grounds for asking.
  `119` passed `asks-for-the-fact` on every drive, before and after the change.
- The existing graders that judge the turn hold on the changed text.

### Negative
- The owner's bar is every reply, and the changed text does not meet it.
  `speaks-about-the-subject` failed 7 of 13 drives, through a "My guess:" label or a lead-in
  naming the run's own view. `tells-checked-from-guessed` failed 10 of 13, each on an estimate, a
  claim about the person's world, or a fact from a file stated with no source under a
  recommendation. The cause of these residual failures is not found.
- `118` failed `a-way-forward` once, by an errand about a second fact.
- `118` was never shown to catch the errand. The decide-what-is-safe rule rests on its text and on
  `118` holding.
- `117` is tuned on: the wording changed after its first drive on the changed text, though no
  wording was drawn from its replies.
- The body of `figure-out/SKILL.md` grew from 3,342 to 3,811 words.

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
`116` to `119` show the manner graders failing on most runs, read in the eval README's results for
these cases once a suite runs.

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
