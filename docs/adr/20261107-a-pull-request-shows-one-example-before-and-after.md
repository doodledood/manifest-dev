# ADR: A pull request shows one example of the change before and after

## Status
Accepted

## Area
Task guidance

## Decided by
The user, who asked that every pull request carry, by default, a short before-and-after so a reader fully understands what the change did and what to expect: screenshots where the change can be seen, and for a change under the hood an illustrative example rather than a driven one. Its purpose is understanding, not proof. The agent chose the wording and where it lives.

## Context
`20261018-every-pull-request-shows-the-change-working` gives every pull request a top that reads in about a minute: what changed and why, how it was shown working, the decisions, and the debt left. A UI change also shows screenshots. A change with nothing to screenshot — a prompt, a rule, a library function, a workflow — tells the reader what changed in general terms, and the reader has to imagine what that means for one actual use. A single example followed through before and after answers that faster than any summary.

## Decision
- **The proof gate in define's `tasks/PR_LIFECYCLE.md` owes one short before-and-after right under the description's top.** It gives a quick feel for what the change means to the person who uses it, so the reader can tell whether the after is what they want: one line naming a task, then a sentence or two for each side saying, from that person's side, what they do and what they get or notice. A real example or an illustrative one marked as such; a screenshot or real output may carry a side but is not required. It explains rather than proves. Whether the change works stays with the gate's proof clauses.
- **Light by default.** A told example from the user's side is enough; screenshots or quoted output are one way to show a side, not a requirement.
- **It amends `20261018-every-pull-request-shows-the-change-working`**, which keeps every other clause.

## Alternatives Considered
- **A real run only, never an illustrative example.** Rejected: the purpose is understanding, and many changes, such as a prompt rule or a convention, have no cheap real run to show. A marked illustration gives the reader the picture; the proof bullets already require real runs for whether the change works.
- **A separate gate.** Rejected: the description has one owner, and splitting it would let one gate pass on a description the other fails.

## Consequences

### Positive
- A reader sees what the change does for one concrete case before reading the general account.

### Negative
- An illustrative example can mislead if it is not typical; marking it as illustrative is the guard.

## Enforced by
partly — `tests/test_pr_lifecycle_proof_gate.py` (`test_proof_gate_keeps_each_recorded_clause`, clause "one example before and after") fails when the proof gate drops the clause. Whether an example is typical and short enough stays judgment.

## Source
- Session: a hill-climb follow-up session, 2026-11-07 (log kept locally).
- Related: Amends 20261018-every-pull-request-shows-the-change-working.
