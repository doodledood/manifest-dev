# ADR: A read and a plan summary show a before-and-after of the proposed change

## Status
Accepted

## Area
define / figure-out

## Decided by
The user, who asked to see the before-and-after a pull request shows "even before we have a pull request during the read", and picked its shape and placement from concrete options: a table over short bullet lines, and right after the read's conclusion line over the end of the read. The agent chose the wording and where it lives in each skill.

## Context
`20261107-a-pull-request-shows-one-example-before-and-after` gives every pull request one short before-and-after: a line naming a task, then each side saying, from the person's side, what they do and what they get or notice. That is the first place a person sees what a change will mean to the person who uses it, and it comes after the work is done. Before that, a person approving a plan reads figure-out's conclusion, its evidence and define's gates, and has to picture the end result from them. In the session that raised this, a plan summary that happened to carry a Before / After table was the part the owner reacted to.

## Decision
- **figure-out's read shows a before-and-after when it implies making something.** It sits right after the conclusion line, ahead of confidence and evidence: one line naming a task, then a table with a Before row and an After row, each saying, from the side of the person the work is for, what they do and what they get or notice. A read that leaves a choice between options open gives each option its own After row. A read that implies making nothing carries no table.
- **define's plan summary shows the same table.** Its Before row is the pain and its After row the intended result, in the part the person confirms or vetoes, replacing the separate pain and intended-result items.
- **It explains, never sells or proves.** The After row claims only what the read or plan supports, and an example made up to illustrate is marked as one.
- **Each skill states the shape itself,** since a shipped skill stands alone; one test keeps the shared clause in step across figure-out, define and the pull request rule. The pull request rule itself is unchanged.

## Alternatives Considered
- **Short bullet lines, the same form a pull request uses.** Rejected by the owner: a two-row table reads at a glance where the read is already dense with prose.
- **At the end of the read.** Rejected by the owner: the picture helps most next to the conclusion it explains, before the evidence a person may skim.
- **One shared reference file the skills point to.** Rejected: each shipped skill stands alone and a run may never load a file a pointer names; the shape is two sentences, and a test keeps the copies in step instead.

## Consequences

### Positive
- A person sees what a proposed change means for its user while the choice is still open, not only once the pull request exists.

### Negative
- Every read that implies making something, and every plan summary, carries a few more lines.
- An After row can oversell a plan; the rule that it claims only what the read or plan supports, and marks an illustration as one, is the guard.

## Enforced by
partly — `tests/test_before_and_after_shape.py` fails when figure-out's `SKILL.md`, define's `SKILL.md` or define's `tasks/PR_LIFECYCLE.md` drops the shared clause ("from that person's side, what they do and what they get or notice"); the figure-out recipe's `before-and-after-on-a-change` and `no-before-and-after-without-a-change` scenarios and the define recipe's `digest-before-and-after` scenario drive the behavior. Whether a run shows the table, and where, stays judgment.

## Source
- Issue: https://github.com/doodledood/manifest-dev/issues/453
- Related: See also [20261107-a-pull-request-shows-one-example-before-and-after](20261107-a-pull-request-shows-one-example-before-and-after.md): the pull request's before-and-after, which this record brings forward to the read and the plan summary without changing it
