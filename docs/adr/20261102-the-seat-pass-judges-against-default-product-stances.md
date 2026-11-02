# ADR: The seat pass judges each choice against eleven default product stances that Taste and project rules override

## Status
Accepted

## Area
figure-out

## Decided by
The user — the user chose the eleven stances, their general wording, and that a ratified Taste entry or a project rule always overrides them, while the Manifest for this change was written.

## Context

The seat pass (`20261102-figure-out-looks-from-the-persons-seat-in-a-fresh-pass`) puts two or three
alternatives side by side at each choice a person would notice. Comparing them needs a standard.
Without one, the pass falls back on whatever the proposal already assumed, and in replays of one
owner's product sessions, kept outside this repository, the model chose against the owner on every
call two careful people could make differently. Most of those corrections were the same few product
judgments — ask at the point of need, keep the person's place across an interruption, check what an
addition gains them, do not add a sale at a stressed moment — stated again in each session.

manifest-dev ships to many kinds of project, not only one product's screens, and the maintainer's
standing preference is a sensible default every user gets with no setup, changeable through
channels people already use (this repository's context file, *Taste*).

This decision sits inside what the North Star's *Purpose* names: work people can trust without
choosing every step or supervising every action.

## Decision

`figure-out/references/SEAT.md` states eleven default stances, worded so each applies to a
command-line tool, an API, a document or a workflow as well as a page, and so none reads the other
way round:

1. **Just in time** — each input asked for, and each capability offered, at the point the person
   needs it; at a gate, only the gate's own choice and what the gate cannot work without.
2. **Continuity** — an interruption returns the person to where they were, their work kept.
3. **A coherent model** — states that cannot make sense together cannot occur, and the model holds
   all the person can have.
4. **Familiar** — existing conventions before new ones.
5. **Respect the moment** — no request, prompt or sale where the person is committed, stressed or
   mid-task.
6. **Value first** — every addition names the person's gain; an inherited premise too.
7. **Progress, not proxy** — success counted by the person's progress, not a stand-in.
8. **Decide for them** — a changeable default over a setting or a question.
9. **First value before commitment** — a useful result before setup or sign-up.
10. **No surprises** — cost, data, audience and reversibility clear before acting; undo over
    confirmation.
11. **Finish the core job before widening.**

The pass judges each choice the person would notice against them. They are defaults: a ratified
Taste entry or a rule the project states overrides any of them, without asking; live steering that
contradicts a stored entry follows `TASTE.md`'s clash rule. The reference also states the two
rules the person meets at every step (each step shows what it needs, the rest one step away; an
error says what happened and what to do next), since figure-out cannot read the design skill or
define's task files, and points at its own *Honest figures* probe rather than restating it.

The gate half of stance 1 was kept on evidence: with no Taste entry, the changed skills passed both
gate moments of the Taste test (`20261102-taste-entry-form-is-chosen-by-a-test`) — asking nothing
beyond the sign-in choice at an account gate, and asking for the delivery address before payment at
a checkout gate.

## Alternatives Considered

- **Nine stances worded for one product's screens** — not chosen: overfitted to one owner's
  product; most of manifest-dev's users build something else.
- **One stance only** (fewest steps) — not chosen: it covers one of the recurring corrections and,
  read alone, invites the over-fire the Taste test's second moment checks.
- **A broad list of product best practice** — not chosen: a long list is read as a checklist and
  produces the long, unranked findings the seat pass exists to avoid.
- **No stances; Taste only** — not chosen: a user with no entries would get no standard at all, and
  most users never write one.

## Consequences

### Positive
- Every user gets the recurring product judgments with no setup, and keeps control of them through
  Taste and project rules.
- The alternatives at each choice have a shared standard, so the pass can rank what it finds.

### Negative
- Six stances and the placement half of the first ship with no case checking them: 4, 7, 8, 9,
  10 and 11, and the placement half of 1. The Taste test's stances arm followed 9 at an account
  gate, but no case grades it. An untested stance may over-fire or add noise.
- A stance stated as a default can still be read as a rule by a run that skips the override
  sentence.

## Enforced by
partly — `tests/test_figure_out_coverage.py` keeps the `references/SEAT.md` row naming the cases that judge the pass; whether each stance steers is judgment, and six, with half of a seventh, are unmeasured.

## Not decided here
- Whether define or the design skill should carry the stances too. Journeys reach define's work
  through `20261102-features-a-person-uses-are-driven-through-their-journeys`; the stances do not.
- Per-stance cases.

## Source
- Session: a `/define` session and a `/do` run on the resulting Manifest, 2026-11-02 (logs kept locally).
- Related: 20261102-figure-out-looks-from-the-persons-seat-in-a-fresh-pass, 20261102-taste-entry-form-is-chosen-by-a-test
