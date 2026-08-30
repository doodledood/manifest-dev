# ADR: `just-do` states the floor and keys its log to the Manifest; /do and /auto stay the control

## Status
Accepted

## Area
Prompt architecture

## Context

`just-do` and `just-auto` exist to find out how much of `/do`'s process a capable model
supplies on its own. They were written by removing process, which left two gaps that only
showed up once the skills were read as standalone files.

The first is that removal was not audited. `just-do` shipped a goal and stopped, so a run
under it inferred a gate's kind when the Manifest declared none, copied gate text into an
evaluator's prompt rather than pointing at the Manifest, and read a repository change against
a local ref that a shallow clone leaves stale. None of those is process ceremony; each is a
fact the run cannot reach from the Manifest it was handed, which is the test that decides
whether a line belongs in a prompt at all. Removing process by section removed them along with
the ceremony they sat beside.

The second is that neither skill kept execution state. `/do` has kept an append-only log since
`20260709-do-keeps-default-execution-log-manifest-stays-contract`, at a path derived from the
invocation's timestamp — so a relaunch after a run ends opens a blank file and the previous
attempt's dead ends are gone. The lean executors are the runs most exposed to that: they are
the paths taken when a full-process run is too expensive, and compacting often to hold cost
down is exactly what makes an out-of-context record load-bearing. `babysit-pr`'s journal had
already solved this by keying to the pull request rather than the run, and that key was not
carried over when the mechanism was generalized.

## Decision

Two things, in the `just-` skills only. Both land in `just-do`, which is where a Manifest is
actually executed; `just-auto` reaches them by delegating to it, and its own prose compresses
to the chain and nothing else.

**A floor, stated as mechanics.** `just-do` states the rulings a run cannot derive from the
Manifest it reads, and nothing else: a gate declares `judgment` or `deterministic` and an
undeclared kind is invalid rather than inferred; an evaluation reads a gate from the Manifest
by ID rather than from a copy; repository work reads the change as `origin/main...HEAD`; a
judgment gate reads the full change once and thereafter only prior findings' repairs and the
delta, while a deterministic gate re-runs in full; findings below a passing gate's bar are
handed over rather than fixed; a bar never moves down, and a summary claim is not evidence.
They are stated in plain terms rather than by this repository's own names for them, which
recruit nothing in a file shipped elsewhere.

**A log keyed to the Manifest.** `just-do` keeps an append-only log by default, `--no-log`
opting out, at `~/.manifest-dev/logs/do-<name>-<hash>.md`, where the hash is the first eight
hex characters of the SHA-256 of the Manifest's absolute path. Fixing the scheme rather than
leaving it to the run is what makes the same Manifest reopen the same file across launches;
including the absolute path is what keeps two manifests sharing a basename in different
repositories apart. The run reads it before resuming and appends as it goes, and it is where
the continuation goal's checkpoint notes land. Entry shape and append discipline stay in
`/do`'s existing log reference, reached by a pointer that scopes itself to those and
disclaims its path rule — the reference still names `/do`'s timestamped home, and a run
following it unscoped would resolve the very path this decision replaces.

`/do` and `/auto` are deliberately left alone. They are the control: the question the `just-`
skills exist to answer is what a model supplies unprompted, and it cannot be answered if both
arms move together. `/do` therefore keeps its timestamped log home for now, and whether the
Manifest key should replace it there is a separate decision this one does not make.

## Alternatives Considered

- **Merge `just-do` into `/do` and retire the split**: the split is a workaround for a spine
  that cannot defer its machinery, and `/do`'s event-triggered sections (a gate returning
  FAIL, a mid-run steering message, a review overlay) are cleanly disclosable behind their
  triggers. — Rejected for now: it collapses the control arm into the experiment, and the
  experiment has not yet returned a result to merge on.
- **Remove the independent verification modes from the lean path entirely**: let the executor
  decide how much checking to buy. — Rejected: evaluator independence is a topology property,
  not an instruction a model can supply for itself; a run cannot grant itself a second reader.
- **The barer variant — the goal and nothing else**: no floor at all, measuring what the model
  does unaided. — Rejected: with nothing recording which rulings the run reached on its own, a
  bare run cannot distinguish "the ruling was latent after all" from "the run quietly lowered a
  bar", so it produces no reading. The floor plus the log is what makes either outcome legible.
- **Restate `/do`'s log entry format in each skill**: — Rejected: one rule in two files is two
  texts that drift; the pointer costs a line and stays true.

## Consequences

### Positive

- A run under `just-do` recovers the whole floor from that one file, with nothing loaded from
  `/do`.
- A relaunched or compacted run re-finds the record its predecessor wrote, which is what makes
  compacting often a cost lever rather than a way to lose state.
- Both arms of the experiment are now readable against each other: the same Manifest contract,
  a stated difference in how much process each carries.

### Negative

- `just-do` grew rather than shrank: the floor and the log add more than the prose compression
  removes, so "lean" now means a stated floor rather than a bare goal.
- The two log homes differ while the experiment runs, so a user moving between `/do` and
  `just-do` on one Manifest reads two files.
- Six rulings written down are six the experiment can no longer measure the model against.

## Source

- Session: figure-out → define → goal-based execution, 2026-08-30
- Related: 20260709-do-keeps-default-execution-log-manifest-stays-contract (extended — the log
  it established for `/do` now also runs under `just-do`, keyed to the Manifest rather than to
  the invocation)
- Related: 20260814-run-visible-surfaces-carry-no-cross-option-framing (the floor states
  mechanics only, and carries no comparison against the modes a run did not select),
  20260805-ratchet-judgment-gate-reverification (the judgment-gate re-verification mechanic the
  floor states in plain terms), 20260828-continuation-goals-emit-verbatim-from-one-block (the
  shared blocks and their arming prose are unchanged by this compression),
  20260820-cost-is-a-binding-constraint-second-to-quality
