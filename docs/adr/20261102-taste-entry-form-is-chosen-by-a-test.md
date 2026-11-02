# ADR: A Taste entry states a general principle and carries no case line

## Status
Accepted

## Area
figure-out

## Decided by
An agent in an unattended run, with no review — under the delegation in the Manifest the user approved for this change, which fixed the test and its two outcomes and left the choice between them to the result.

## Context

A Taste entry is a ratified preference in three parts: the preference, the reason, and when it
yields (`20260719-taste-persists-by-offer-and-ratify`, `20261012-taste-is-checked-per-call-and-captured-from-explained-reversals`).
In replays of one owner's product sessions, kept outside this repository, a written fewest-steps
entry was in force and a session still put three detail fields under a sign-in gate. Two readings
were open: the entry was too abstract to bind a concrete call, so a short example of the case that
prompted it would help; or the entry steered fine and the session lacked a look from the person's
seat.
The owner's standard for entries is that they state principles, not every detail they said.

This decision sits inside what the North Star's *Purpose* names: keeping the choices a person
retains available to later sessions.

## Decision

Taste drafting directs the preference to be stated as a principle that carries to calls never
discussed, rather than as the details of the case that prompted it. No case line is added to the
entry form. `figure-out/references/TASTE.md`, `define/SKILL.md` and `do/SKILL.md` say so where they
draft an entry; `do/references/HARVEST.md` drafts through `do/SKILL.md` and needs no change.

The choice rests on a test run before deciding. A fictional recipe site with a shop (`Larder`) had
two moments no case or entry named: (a) a guest saving a recipe, where an account is needed and the
business also wants dietary needs, household size and a display name — passing means asking
nothing at the account step beyond the sign-in choice; (b) checkout for a posted spice kit —
passing means asking for the delivery address before the order is paid, which a fewest-steps entry
read too far would push past payment. Three arms, each driven once per moment through the
`figure-out` recipe's `taste-*` scenarios:

- **principle** — on the skills before this change, with this entry in the project's context file:
  "Prefer the route with the fewest steps between what the person asked for and getting it: at a
  gate such as sign-in or payment, show only the gate's own choice and ask for nothing a later step
  could ask. The owner's reason: every extra step loses people. Yield when the person needs a step
  to decide, or to trust what comes next."
- **case** — the same, plus one case line from a different gate: "Case: a newsletter sign-up form
  that also asked for job title and company size was rejected: 'just the email field.'"
- **stances** — with no entry, on skills that carried a seat look with eleven default product
  stances; that look did not ship (`20261102-figure-out-keeps-its-seat-line-no-seat-look-ships`).

A grader session that saw only each reply under a letter label graded all six. Every run passed:

| Arm | (a) save | (b) checkout |
|---|---|---|
| principle | PASS — Google, Apple, email and password; diet, household and name after the save | PASS — delivery section before the payment section |
| case | PASS — Apple, Google, email and a one-time code; name at first comment, diet and household on an optional card | PASS — delivery step before the payment step |
| stances | PASS — Google, Apple, email and a code; diet, household and name asked later | PASS — delivery step before the payment step; an express wallet supplies the address |

The case line therefore did not win moment (a) where the principle alone lost it, so by the rule
fixed before the test the entry form does not change. Both entry arms also passed moment (b): the
principle's own yield clause held, and the case line did not over-fire. The stances arm passed both
moments as well, so on these two moments the stances added nothing a Taste entry on the skills
before the change did not already give.

## Alternatives Considered

- **Add an optional case line to every Taste drafting site** (the moment, what was proposed, what the
  user chose instead) — not chosen: it would win only where the principle alone lost, and here the
  principle alone passed both moments. It would also grow every entry in every session for no
  measured gain.
- **Change nothing in drafting** — not chosen: the owner's standard that entries state principles
  had no line saying so, and a session drafting from one vivid reversal tends to copy its details.

## Consequences

### Positive
- Entries stay short and carry to calls nobody discussed, which is what makes them worth keeping
  resident.

### Negative
- One run per arm per moment, on one fictional product, is a direction, not a measurement: a case
  line may still help on calls further from the principle's wording than these two.

## Enforced by
none — a drafting instruction read by the model at offer time; no check can tell a principle from an overfitted entry without judging it.

## Not decided here
- Whether entries should name the kind of product they came from.
- Whether a project-level Taste section should move out of the context file into its own file; it
  stays in the context file until there is evidence it grows too large.

## Source
- Session: a `/do` run on a Manifest the user approved, 2026-11-02 (log kept locally). Drive summaries and the grader's verdicts are in the pull request that adds this record.
- Related: 20260719-taste-persists-by-offer-and-ratify, 20261012-taste-is-checked-per-call-and-captured-from-explained-reversals, 20261102-figure-out-keeps-its-seat-line-no-seat-look-ships
