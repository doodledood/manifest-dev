# ADR: Run-visible prompt surfaces carry no comparative framing about options the run did not select

## Status
Accepted

## Area
Prompt architecture

## Context

`/do` fixes its verification mode and re-read policy at launch; a run then works under one
option. But the spine every run reads carried the full comparison: `per-gate` described as the
careful independent reader, `consolidated` priced against it, `self` labelled "marking its own
homework," and the Ratchet's miss risk weighed against exhaustive re-sampling. A run locked to
one option was told, in its own working context, how the options it did not select compare in
quality, cost, and rigor.

That framing cannot inform the run — the selection is already made and never changes
mid-run — so the only thing it can do is bias: a `self` executor told it is the cheap,
lower-assurance choice may compensate with ceremony the mode did not ask for, or slacken to
match the label; a per-gate verifier told it is the careful one inherits a posture rather
than a task. The same mechanism operates between skills: a frontmatter description carrying
another skill's framing ("for full verification, use X") hands every session that reads the
skill list a rigor comparison it should not be running under. The new goal-based executor
skill (`just-do`) was the case that surfaced this: its whole premise is measuring what a model
does *without* imported process framing, which is unmeasurable if the surrounding surfaces
keep supplying it.

The repo already isolates mode *mechanics* (each run loads exactly one mode reference,
test-enforced). The leak was comparative *framing* on always-loaded surfaces.

## Decision

Run-visible prompt surfaces — skill spines, always-loaded sections, frontmatter
descriptions — state what each option mechanically does and carry no comparative quality,
rigor, cost, or speed judgment between options, and no which-should-you-pick advice.
Selection guidance is user-facing content and lives in human docs (READMEs), where the
human choosing before launch reads it and the run does not.

Concretely in this change: `/do`'s "How much checking to buy" section becomes "Verification
settings" — each `--verification` value and each `--exhaustive-verification` setting described
by its mechanics (who evaluates, in what topology, what loads, what re-reads) with the
comparisons removed; the removed guidance lives in the root README. Operative mechanics that
bind every run stay in the spine: the Ratchet's scoping rule, Deterministic Gates re-running
in full, expensive-evaluation timing. Skill descriptions describe only their own skill.

A mode's own reference may still calibrate its own run ("the risk of grading adherence to the
plan is highest in this mode") — that is loaded only by the run it addresses and informs
rather than compares.

## Alternatives Considered

- **Keep the comparison in the spine for transparency**: rejected — the run cannot act on it
  (the policy is fixed at launch and never downgrades), so it is pure framing cost; the
  transparency belongs to the human at selection time, in the README.
- **Move the comparison into a reference loaded on demand** ("which mode should I pick?"):
  rejected for now — no run-side consumer exists, since selection happens before launch;
  READMEs already carried most of the guidance.
- **Also strip mode names from the spine**: rejected — the spine must parse and validate the
  flag values and load the selected reference; naming options is mechanics, judging them is
  framing.

## Consequences

### Positive

- A run under any mode reads only what its own configuration does — behavior stops depending
  on whether the model saw the other options' labels.
- The `just-do` experiment (goal-based execution with minimal process) can be graded without
  the surrounding surfaces re-importing the framing it removes.
- A concrete audit test for future prompt changes: mechanics of every option may be stated;
  comparisons between options may not, on any surface a run always reads.

### Negative

- A user who reads only `/do`'s SKILL.md no longer finds mode-selection advice there and must
  find the README.
- The mechanics/framing line requires judgment at the margin (a topology fact like "each in
  its own context" borders on a quality claim); the audit test above decides, but not
  mechanically.

## Source

- Session: figure-out → define → goal-based execution, 2026-08-14, alongside the `just-do`
  skill's introduction
- Related: narrows the mode-comparison-prose clause of
  20260808-restore-per-gate-default-verification-mode (the comparison that decision rewrote
  now lives in the README rather than the spine; the default flip and all mode semantics are
  untouched). See also 20260806-verification-is-bookkeeping-and-a-stop-condition,
  20260703-progressive-disclosure-triggers-live-in-loading-layer.
