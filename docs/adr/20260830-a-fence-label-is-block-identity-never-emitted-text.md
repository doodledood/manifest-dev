# ADR: A fence label is block identity, never emitted text

## Status
Accepted

## Area
Goal setting

## Context

`20260828-continuation-goals-emit-verbatim-from-one-block` gave each shared contract block a
fence label — `goal-block`, `chain-prefix`, `pr-tend-prefix`, `gate-ledger-clause` — so that a
block's identity is separable from its own text, and a drift check keying on the label cannot be
blinded by a reworded body. That reasoning is about the repository's own checks. It says nothing
about what a run prints.

Every site then instructs the model to emit the block "verbatim" and not to reword or
re-punctuate it, with the block sitting in the file inside a labelled fence. A reader following
that faithfully emits the fence and the label too. A user reported exactly that: the contract
arrived in their terminal as bracketed blocks headed by this repository's internal bookkeeping,
which is meaningless to them and belongs to the test suite.

Two sites made it worse. `auto`, `do`, and `babysit-pr` each said to emit their blocks "as one
contract"; `just-auto` and `just-do` — the lean arm, and the ones the report came from — did not.
So a `/just-auto` run had no instruction joining its two blocks and printed them as two separate
labelled units rather than one contract.

The text is only ever printed on a harness exposing no goal-setting capability; where one exists
the contract is set through it and nothing is shown. So this rendering is seen exactly when
nobody but a person is reading it.

## Decision

**A fence label identifies a block to this repository's checks; it is never part of what a run
emits.**

Every site that arms a backstop states this alongside its verbatim instruction: the fences and
their labels are the file's own markers, and the contract is printed as **one unlabeled block,
introduced by a sentence of the run's own prose** saying what is being armed. `just-auto` gains
the "as one contract" instruction the other sites already carried, so its two blocks print joined
rather than separately.

"Verbatim" continues to govern the block's text exactly as before — no summarizing, shortening,
rewording, or re-punctuating. This decision only settles what "the block" ranges over.

`tests/test_goal_contract_blocks.py` enforces the rule at every backstop site it discovers, beside
the existing check for the no-paraphrase instruction and for the same reason: both are prose
sitting next to fenced content, so a pass that tightens prose can remove either without any block
changing.

## Alternatives Considered

- **Print nothing on a harness with no goal capability**: the leading rival, and genuinely
  attractive — the contract's only reader is a host checker, so where none exists the emission
  informs nobody. Rejected for now because it is a larger change that needs new per-site prose
  saying what the run is aiming at, and because it forecloses a person pasting the contract into a
  mechanism this project does not know about. The question stays open rather than settled against.
- **Drop the prefixes and print only the goal block**: rejected on inspection. `pr-tend-prefix`
  carries `babysit-pr`'s terminal condition and its never-press-merge constraint, neither of which
  the goal block states; and removing `chain-prefix` would make `figure-out --autonomous` re-arm
  its own Read-level goal, since it suppresses that only when it can see a parent carrying the full
  Read bar. The output would not shrink and a phase checkpoint would be lost.
- **Strip the labels from the shipped files**: rejected outright. The labels are what makes the
  drift check able to see a reworded block, which is the whole mechanism `20260828` built.
- **Leave it to the model's judgment**: rejected as what produced the report. A site saying only
  "emit the block below verbatim" reads, to a careful model, as including the fence.

## Consequences

### Positive

- The contract prints as one block of contract text, introduced in the run's own words, rather
  than as labelled fences carrying repository bookkeeping.
- The lean arm stops emitting two disjoint units where the regular arm emitted one.
- The rule is a failing test rather than a convention, and the test finds its own subject, so a
  backstop site added later is covered without anyone remembering.

### Negative

- Five sites now carry one more sentence of emission mechanics, on prompts whose length is already
  the standing complaint about this machinery.
- The rule is stated per site rather than once, which is the same duplication `20260828` accepted
  for the blocks themselves and for the same reason: a shipped skill stands alone.
- It leaves the larger question — whether to print at all where nothing can consume the contract —
  open, so a reader may meet this record expecting it to settle that and find it deliberately did
  not.

## Source

- Session: a user report that `/just-auto` printed its contract as bracketed, labelled blocks,
  2026-08-30.
- Related: `20260828-continuation-goals-emit-verbatim-from-one-block` — the record that introduced
  the labels. Its standing is unchanged and it is not restatused: it never claimed the fence was
  part of the contract, so this record resolves an ambiguity it left rather than narrowing what it
  decided.
- Related: `20260830-a-contract-slot-exists-only-where-its-value-is-known` — the same surface, one
  step earlier: that record made the contract's content complete at emission, this one makes its
  rendering fit for the only reader who sees it.
