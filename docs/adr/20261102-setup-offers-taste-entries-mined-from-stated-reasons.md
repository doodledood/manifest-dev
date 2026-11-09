# ADR: setup-project offers a project, once, a few Taste entries mined from reasons the owner already stated

## Status
Accepted — amended by 20261109-area-principles-live-in-project-skills: a candidate that guides one area's work is offered for that area's principles skill and does not count toward the five

## Area
Project context

## Decided by
The user — the user asked for setup to offer Taste entries mined from the project's history, on the design proposed to them; the agent that ran the change chose the wording and where it lives, under the Manifest's delegation.

## Context

A Taste entry is a ratified steering preference — the preference, the reason its owner gave, and
when it yields — that later sessions weigh at a call two careful people could make differently
(`20260719-taste-persists-by-offer-and-ratify`, `20261012-taste-is-checked-per-call-and-captured-from-explained-reversals`).
Entries are captured one at a time, when a session sees the user reverse a call and say why. A
project new to the workflow therefore starts with none, though many of its owner's overrides are
already explained in its history: in decision records, in review threads where a proposal was
turned down with a reason, and in the owner's past sessions. In replays of one owner's sessions,
kept outside this repository, the owner restated the same few product judgments across sessions.

The workflow ships defaults every user gets — each skill's own — so an entry earns its place first
where the owner leans away from one of them.

This decision sits inside what the North Star's *Purpose* names: a person returns without restoring
the same context, and keeps control of the choices they retain.

## Decision

setup-project's seed (`setup-project/references/MINING.md` → *Taste*) also offers Taste candidates:

- only from a reversal or correction whose reason the user stated — a decision record whose
  reasoning is a preference, a review or pull request thread, and the user's past session records
  where the host keeps them, opened only after the user agrees, since they are private;
- overrides of shipped defaults first; nothing a shipped default already says, and nothing a
  decision record already settles;
- at most five, each drafted in the Taste boundary form figure-out's `references/TASTE.md` gives;
- ratified as one batch, as the glossary seed is, and written only into the `## Taste` section of
  the memory file the user picks; with nobody to ratify, nothing is written and the candidates are
  reported.

`--no-mine` skips it with the rest of the seed.

The offer reaches a project once. A project set up for the first time gets it in that setup's seed.
A project set up at an earlier version gets it as the one item of surfaces version v13, through the
update offer it already receives (`setup-project/references/upgrades/v12-to-current.md`). Once a
project records v13, setup does not offer it again, whatever the answer was; `--no-mine`, or a
project with no history to read, skips it and the version is still recorded. This is an exception
to `20261014-setup-project-audits-the-whole-setup-when-run`, under which nothing records a decline
and a declined item returns on the next run: here the recorded version marks the offer as made.

## Evidence at decision time

The `setup-project` recipe's `taste-from-history` scenario was driven once on the skills before
this change and once after, with the owner away, and graded by a grader session that saw each run
under a letter label only. After: PASS (borderline) — it reported two candidates, the two
overrides, as principles, and put forward none for the restated default, the settled storage
choice or the revert with no reason; it wrote no entry and opened no past session record. The
candidates showed no yield clause, which made the first grader borderline. Before: FAIL — it
offered no Taste candidate. Both runs also wrote decision records for the two overrides; the run
after asked the owner to keep each choice in one place. The once-only reach was not driven.

## Alternatives Considered

- **No mining** — not chosen: entries would keep arriving only as corrections happen, one session
  at a time, while the reasons sit unread in the history.
- **Mine everything the owner said** — not chosen: it yields the overfitted, case-shaped entries
  that drafting now steers away from (`20261102-taste-entry-form-is-chosen-by-a-test`), and a long
  list is read as a checklist.
- **Copy settled decisions into Taste** — not chosen: a decision record is the home of a settled
  choice, and a second copy drifts from it.
- **Offer it on every update while no `## Taste` section exists** — not chosen: a user who declined
  would be asked again on every run, and a project whose owner keeps Taste only in a user-level file
  would never stop being asked.
- **Never offer it on an update** — not chosen: projects set up before this change would never get
  it.

## Consequences

### Positive
- A newly set-up project can start with its owner's real overrides of the defaults.
- Every entry rests on a reason the owner gave and passes through their yes.

### Negative
- Reading past session records costs tokens and needs the user's agreement each time.
- A project whose owner declined, ran with `--no-mine`, or had no history yet does not get the offer
  again; its entries then come only from capture, or from asking for the mining directly.
- A few weak entries can still reach a memory file; the batch ratification is the only filter.

## Enforced by
none — which candidates deserve an entry is judgment; the `setup-project` recipe's `taste-from-history` scenario checks it by a drive.

## Not decided here
- Whether figure-out should offer the same mining outside setup.
- Whether a later version may offer it again, for example once a project has gained history.

## Source
- Session: a `/do` run on a Manifest the user amended mid-run, 2026-11-02 (log kept locally). The drive's grade is in the pull request that adds this record.
- Amends 20261014-setup-project-audits-the-whole-setup-when-run
- See also: 20260719-taste-persists-by-offer-and-ratify, 20261012-taste-is-checked-per-call-and-captured-from-explained-reversals, 20261102-taste-entry-form-is-chosen-by-a-test, 20260809-glossary-stays-resident-with-an-under-produced-seed
