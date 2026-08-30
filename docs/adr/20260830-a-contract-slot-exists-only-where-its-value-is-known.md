# ADR: A contract slot exists only where its value is known at emission

## Status
Accepted

## Area
Goal setting

## Context

`20260828-continuation-goals-emit-verbatim-from-one-block` reduced the continuation contract to
shared blocks emitted verbatim, with `<manifest-path>` as the single remaining slot. That record
also noted, under its negative consequences, that three sites cannot fill it: `/auto`,
`/just-auto`, and `/babysit-pr` without `--manifest` arm the backstop before a Manifest exists,
so they emit the token literally and lean on a prefix clause to define it later.

A user running `/just-auto` reported the printed contract as useless, and the reason they gave is
the one that decides this: on a harness exposing no goal-setting capability the contract is
printed for a person to set at launch and forget. There is no later moment at which they revisit
it. A slot whose value arrives after emission is therefore never filled at all — the pasted
contract names a Manifest the reader cannot identify, and the run's own checkpoint note, written
minutes later, reaches nothing.

The token was also redundant where it appeared. Each of the three prefixes already carried an
instruction to record the Manifest's path in a checkpoint note as soon as it exists, which is the
mechanism that actually anchors the contract. The slot beside it was a forward reference to that
note, carrying no information of its own at the moment it was read.

`/do` and `/just-do` fill the slot correctly, because there the path is a required argument. So
the defect was never a substitution that failed; it was three sites holding a slot they are
structurally incapable of filling, governed by a per-site rule about when to leave it literal.

## Decision

**A slot exists only where its value is known at emission.** The `<manifest-path>` slot is
removed from the shared blocks entirely.

- The `goal-block`'s opening paragraph names the Manifest self-referentially — *"Work under this
  run's Manifest"* — and absorbs the path-recording instruction the prefixes carried: *"Record the
  Manifest's path in a checkpoint note as soon as it exists."* The block is then self-sufficient
  at all five sites, and the three prefixes drop the clause and the pointer at the removed token.
- No site's prose instructs substituting, filling, or leaving literal a `<manifest-path>`. The
  five emission instructions say only to emit verbatim.
- `<pr-url>` in `babysit-pr` remains, because its value is an argument the site holds when it
  emits.

Removing the slot rather than teaching each site how to handle it is what makes the defect
unrepresentable: with no slot in the text, no site can emit an unresolved one, and there is no
rule left for a future site to apply incorrectly. It also repairs `/auto` and `/babysit-pr`,
which carried the same defect unreported.

The path is still recoverable everywhere it matters — from the invocation at `/do` and
`/just-do`, and from the checkpoint note the block itself now requires at every site.

## Alternatives Considered

- **Give `/auto` and `/just-auto` their own variant of the goal block**: the shape first proposed,
  and rejected. It is exactly the drift `20260828` closed, and `tests/test_goal_contract_blocks.py`
  enforces byte-identity, so the variant fails the suite by design rather than by accident.
- **Keep the slot with two legal fillers — a path, or one canonical fixed phrase**: workable, and
  byte-checkable since neither filler is free prose. Rejected because it keeps the slot alive and
  replaces one per-site rule with another, when the property wanted is that no site has a choice
  to get wrong.
- **Emit the goal block only after the Manifest path is known, or re-emit it then**: rejected on
  the reported behavior. A contract printed later is never pasted, and arming after the
  investigation phase leaves a run that dies during it with no backstop at all.
- **Have `/just-auto` pre-decide the timestamped path and pass it to `/just-define` as a write
  target**: the only option that puts a literal path in the printed contract, and the strongest on
  information alone. Rejected because `/just-define`'s path argument already means *amend*, so the
  write target would overload one argument with two meanings distinguished by whether the file
  exists — and it moves path-naming away from the skill that owns it.
- **Leave the slot and suppress the printing where no capability exists**: rejected as a different
  decision about a different question. Whether a capability-less harness should be shown the
  contract at all is untouched here; the user ruled the printing itself acceptable.

## Consequences

### Positive

- The printed contract is complete at the moment it is read, which is the only moment a
  set-and-forget reader has.
- A site cannot emit an unresolvable token, because no token remains to emit — the property holds
  by construction rather than by five sites each applying a rule.
- Three sites are repaired by one change, two of which had not been reported.
- Each prefix loses a clause the goal block now carries, so the path-recording instruction has one
  home instead of three.
- The system-wide rule is now legible in one sentence and testable by inspection: the only
  surviving slot, `<pr-url>`, is one its site holds at emission.

### Negative

- `/do` and `/just-do` contracts no longer name the Manifest file, though both are invoked with
  its path. A host checker auditing such a run resolves the Manifest from the invocation or the
  checkpoint note rather than from the contract text. The cost was put to the user and accepted.
- `babysit-pr` invoked with `--manifest` had a path available and now does not use it, which is
  the same cost paid to keep one text rather than two.
- The chain-prefix signature in `tests/test_goal_contract_blocks.py` had to move, because the old
  signature was the sentence this decision deletes. The label, not the signature, remains the
  block's identity, so the move is routine — but it is the second time a signature has followed
  its text, and each such move is a moment where a stripped label would go unnoticed.

## Source

- Session: investigation of a `/just-auto` run whose printed contract carried an unfilled
  `<manifest-path>`, 2026-08-30.
- Related: `20260828-continuation-goals-emit-verbatim-from-one-block` — narrowed by this record:
  the one-text-per-block property and the verbatim-emission requirement both stand; the slot that
  record kept is removed.
- Related: `20260830-shared-contract-blocks-name-the-beat-not-the-skill` — the same move applied
  to a different axis: that record made the block's wording arm-neutral, this one makes it
  emission-time-complete.
- Related: `20260623-use-universal-goal-setting-language` — unchanged; the capability-based
  emission boundary still decides whether the contract is set or printed.
