# ADR: figure-out looks from the person's seat in a separate pass before it names a read

## Status
Accepted

## Area
figure-out

## Decided by
The user — the user approved the Manifest that chose a separate seat pass over the spine line it replaces; the agent that ran it chose the fresh context, with the inline fallback, under that Manifest's delegation.

## Context

figure-out's spine carried one line for the person a read is for: start from the person the North
Star names, narrow to the slice and moment the artifact serves, then "take their seat and
enumerate every use they would make of it" (`20260914-who-its-for-is-consumed-by-figure-outs-seat-taking`,
amended by `20260924-figure-out-settles-the-artifacts-person-and-opens-visual-directions-with-variants`).
That line plateaued: on case `14` it held at about two runs in three across the October hill-climbs.

In replays of one owner's product sessions, kept outside this repository, an owner had to steer
the agent on product judgment 18 times across feature and design sessions. A page that passed its
interface checks, its tests and four code reviews failed the next morning on journeys outside the
states its proposal described: a signed-out visitor, the return after sign-in, a second item
replacing the first, a mode ignoring its setting. A Ticket marked fully decided was built without
asking what the person gains. The live product was never looked at. In those replays, any separate
review pass caught an issue the authoring agent had skipped, and every review missed the signed-out
journey; reviews listed 9 to 35 changes with the owner's points ranked anywhere from 1st to 29th.

This decision sits inside what the North Star's *Purpose* names: work trustworthy enough to use,
without the owner restoring the same context in every session.

## Decision

The spine keeps naming the person and their moment, and hands the look itself to a **seat pass**
whose mechanics live in `figure-out/references/SEAT.md`. Its trigger sits in `SKILL.md`'s
*Modes and what loads* table: it loads once the read implies making or changing something a person
will see or use, including when the work starts from a premise inherited from a Ticket, a decision
record or an earlier read; work no person meets loads nothing. The pass:

- runs in a fresh, isolated context, as the independent re-derivation does, handed the proposal,
  the person and their moment, the assignment's authority, the product's location and the default
  stances (`20261102-the-seat-pass-judges-against-default-product-stances`); inline where the host
  has no isolated context, and the read says so;
- derives the person's journeys from that person and this feature — always how they first arrive
  from outside, how they come back, and what goes wrong, then the journeys only this feature has —
  never from a fixed list;
- walks them on the running product where it can be started, otherwise through the proposal, and
  walks the whole moment the work touches rather than only the part asked about;
- puts two or three alternatives side by side at each choice the person would notice;
- ranks what it finds by what each costs the person and returns only the few findings that change
  the read; a finding that is a user's call goes to the user as options.

`figure-out/tasks/FEATURE.md`'s *Their stories, not ours* points at the pass instead of restating
the seat rule.

## Evidence at decision time

Each case was driven through the `figure-out` recipe once on the skills before this change and once
after it, and graded by a grader session that saw each reply under a letter label only. A case
passes when the run after the change passes and the run before fails; a pair that does not settle
it gets up to two more runs per arm, decided by majority of three; and a case whose run before the
change passed was replaced once by one written so that run should fail.

| Case | First version (after / before) | Replacement (after / before) |
|---|---|---|
| `94` a requested change that stops short | PASS / PASS | PASS (borderline) / PASS |
| `95` journeys outside the described states | FAIL (no return after sign-in) / PASS | PASS / PASS |
| `96` an inherited premise | three pairs: PASS (borderline) / FAIL (borderline), FAIL (borderline) / PASS (borderline), PASS / FAIL — after 2 of 3, before 1 of 3 | — |
| `97` a product nobody looked at | PASS / PASS (both drove it) | PASS / PASS |
| `98` no person-facing surface (guard) | PASS / PASS | — |
| `14` the persona seat (guard) | PASS, borderline on `takes-the-persona-seat` | — |

`96` split its first two pairs, each verdict borderline, so it got a third: there the run after
the change put the premise to the owner first — the referral card gives a customer who has just
reported a stolen card nothing towards fixing it — and the run before treated the premise as
settled and planned the build. By majority of three, `96` passes. The figure-out recipe's
`draft-is-quick-and-unchecked` guard passed three runs of three.

Apart from `96`, on these one-prompt cases the skills before the change already took the person's seat, named
signed-out arrival and the return after sign-in, drove a runnable product, and looked past a
requested change; the pass showed no uplift there and no regression. `96` — a premise inherited from a Ticket —
is the one case where it moved the result. The failures the Context describes
came from long sessions where the person's moment was one concern among many. The decision rests
on the replay evidence that a separate pass catches what the authoring context skips, not on
these drives.

## Alternatives Considered

- **Keep the spine line** — not chosen: it lived in the authoring context, whose blind spots the
  replays showed a separate pass catching, and it gave no way to rank what it found.
- **An inline seat pass** — not chosen as the default: the same context that wrote the proposal
  re-reads it. It remains the fallback where a host has no isolated context. Comparing the two was
  not run and is owed.
- **A new user-invoked product skill** — not chosen: `20261013-new-capabilities-live-inside-the-four-workflow-entry-points`;
  a capability that waits to be invoked does not run.
- **A review gate in define alone** — not chosen as the whole fix: it catches the gap after it is
  built. The journeys gate (`20261102-features-a-person-uses-are-driven-through-their-journeys`)
  is its complement.

## Consequences

### Positive
- The look from the person's seat no longer depends on the authoring context remembering it, and
  its findings arrive ranked and few.
- A product that can be run is used before the read, not only read as source.

### Negative
- Every read that implies making something a person uses starts one more context, which costs
  tokens and time.
- Uplift shows on one case of five, `96`, and by two runs of three to one. The other one-prompt
  cases do not reproduce the failure; a case that does needs a long session in which the person's
  moment competes with other work.

## Enforced by
partly — `tests/test_figure_out_coverage.py` keeps the `references/SEAT.md` row naming the cases that judge it; whether the pass changes a read is judgment, measured only by drives.

## Revisit when
A run of the `figure-out` eval suite, or drives of cases built from long sessions, shows the seat pass's cases passing no more often with the pass than without it; read in `claude-plugins/manifest-dev/evals/README.md` → *Seat pass and experience choices — 2026-11-02*.

## Not decided here
- Whether the pass is better run inline than in a fresh context; that comparison was not run.
- Cases built from long sessions, which the one-prompt cases above cannot set up.

## Source
- Session: a `/define` session and a `/do` run on the resulting Manifest, 2026-11-02 (logs kept locally). Drive summaries and blind grades are in the pull request that adds this record.
- Amends 20260914-who-its-for-is-consumed-by-figure-outs-seat-taking, 20260924-figure-out-settles-the-artifacts-person-and-opens-visual-directions-with-variants
- Related: 20261102-the-seat-pass-judges-against-default-product-stances, 20261102-features-a-person-uses-are-driven-through-their-journeys, 20261102-experience-choices-go-to-the-user-as-options-or-variants
