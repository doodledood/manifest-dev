# ADR: The design starter set asks a surface to say what each thing is through its form before a sentence does, and `review-design` stays as it is

## Status
Accepted

## Area
Project context

## Decided by
An agent in an unattended run, with no review, under the user's delegation to carry this change
through and merge it. The user ruled that the rule is added to the design starter set, that
`review-design` restates no design principle, and that its text changes only if a drive shows the
unchanged skill missing the case. The wording of the line and of the four reworded lines is the
agent's.

## Context
A project that had taken the design starter set built screens with too much text on them, and
review rounds made the screens worse. A finding of the kind "people will not understand this" was
answered by adding a sentence about the thing, and the next round found the screen crowded. Four
lines of the set leaned the same way: an element stayed "for what it does", whatever the person
would ask next was "answered right there", a state said so "and why", and every figure "states"
its unit. Each can be met by a label or a mark, and each reads as a call for a sentence. No line
said that an explaining sentence is a cost.

`review-design` was a second place the rule could live. The `design` skill, which it
reads as guidance, already names "Prose, including instructions, where a visual, a single line or
the design itself would carry the point" among the defaults to avoid.

## Decision
- The design starter set gains a line with no `Only where` condition: a surface says what each
  thing is through its form — a label on the thing, a mark, an order, a position — before a
  sentence does. A sentence about the surface itself, saying what a thing on it is or how to use
  it, stays only where no label, mark, order or position could carry what it says. A finding that
  people do not understand a thing is repaired on the thing first, and a sentence added to answer
  it is held to the same test. On the screen a person meets first, every sentence is either what
  they came for or a sentence about the surface that passes this test. The line yields for text
  the person came to read, for a term new to the person that no mark or picture can teach, and for
  what a person must be told before a costly or irreversible press.
- Four lines are reworded so that none of them asks for a sentence: an element stays only where
  its person would miss it; what the person will ask next is answered by what is shown, and by a
  note only where that cannot answer; a state says so, and why, in the fewest words that give
  both; a figure shows its unit and what it counts, on the figure or its label.
- The change ships as surfaces v20. A project whose design principles skill holds the earlier
  wording is offered the new line as one it lacks and each reworded line as a sharpening of the
  skill's line nearest it.
- `review-design` does not change. Driven on its text before this change, it already counted explaining
  sentences as a cost and asked for labels and marks, on a first case and on a harder one. The
  rule therefore has one home, the starter set and the principles skills that take it, and a
  project with no design principles is reviewed under the standards the reviewer already holds.

## Alternatives Considered
- **A limit on words or sentences per screen**: a count is easy to check — a surface whose text
  is what the person came to read would fail it, and a short sentence that explains a mark would
  pass it.
- **Sharpen an existing line instead of adding one**: the nearest line, on drawing a section's
  point before writing it out, applies only where a surface presents data, and the rule holds for
  every surface. A reviewer also gives each line one verdict, so a clause inside a long line is
  applied to a side point.
- **State the rule in `review-design` as well**: two homes for one rule drift apart, and the
  drives showed the reviewer already holding it.
- **Have `review-design` read the design starter set where a project has no design principles**: this
  was to be built only if a drive showed the unchanged reviewer missing the case. Neither drive
  did.

## Consequences

### Positive
- An agent holding the set has a line to hold a repair to: put the meaning on the thing, and keep
  a sentence only where nothing else can carry it.
- A project's review, which holds work to the project's own principles, can cite the line when a
  finding is answered with a sentence.
- Text a person needs is named in the line's own yield, so the rule does not read as "less text".

### Negative
- The set is one line longer, and a project fitted before v20 is asked about five design lines
  again.
- A project that never ran setup gets the rule only through the `design` skill's shorter wording.
- The line asks for a judgment — whether something on the surface could carry what a sentence
  says — that no check holds.

### Evidence and its limits
Each scenario below ran once per arm, by a fresh agent in the session that made the change, so
each result is one sample.

- `review-design explained` and `reading`, on the reviewer's text before this change: both passed. The
  reviewer counted the added explaining sentences as a cost and asked for labels and marks, and it
  did not ask to cut text the person came to read.
- `review-design explained-retested`, a harder case where a re-test claims the earlier findings
  are closed: passed on that same text. That result is why the reviewer does not change.
- `setup-project design-set-repair`, with the set before this change and with it: both arms
  passed. Each run repaired all six findings with words on the thing and added no explaining
  sentence. This case therefore does not show the new line changing a repair.
- `setup-project update-one-behind`: passed. A project recording v19 was offered the new line as
  one it lacks and the four rewordings as sharpenings, and recorded v20 after its answers.

None of these reproduces the failure that prompted the change: sentences added one review round
at a time, where each sentence closes a finding. That loop runs over many rounds, and no scenario
drives it.

## Enforced by
partly — `tests/test_setup_project_versions.py` digests the starter sets, so a change to the line
without a new surfaces version fails, and `tests/test_starter_principles.py` holds the set's
shape. The setup-project recipe's `design-set-repair` scenario drives a repair by an agent holding
the set, and the review-design recipe's `explained`, `explained-retested` and `reading` scenarios
drive the review; each is a paid run a person starts. Whether a given sentence could be carried by
the surface stays judgment.

## Revisit when
Projects that took the line strike it or reword it, or their design reviews still accept an added
sentence as the answer to a finding that people will not understand something — read in those
projects' design principles skills' git history and their pull request reviews. Also when a
`review-design` drive of `explained` or `explained-retested` fails on a later reviewer text or
model, read in `verification/evidence/review-design/`.

## Source
- Related: See also [20261118-starter-principles-ship-as-sets-a-project-owns](20261118-starter-principles-ship-as-sets-a-project-owns.md), under which a changed set reaches projects as a new offer in a new surfaces version; [20261119-a-starter-line-is-held-only-where-one-line-states-all-of-it](20261119-a-starter-line-is-held-only-where-one-line-states-all-of-it.md), which decides that a skill holding the earlier wording is offered the reworded lines; [20260927-design-names-the-defaults-to-avoid](20260927-design-names-the-defaults-to-avoid.md), where the `design` skill names prose that the design could carry
