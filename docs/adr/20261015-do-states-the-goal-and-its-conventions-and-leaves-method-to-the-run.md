# ADR: `/do` states the goal and its conventions, and leaves method to the run

## Status
Accepted

## Area
Prompt architecture

## Decided by
The user

## Context
`/do` was rebuilt from its lean body in 20260914-one-skill-per-beat-built-from-the-lean-body,
keeping only what binds: every gate declares its kind, a judgment gate reads the change once and
then the delta, gate text changes only through the authoring skill, and completion needs fresh
evidence for each gate. The floor it inherited from
20260830-just-do-states-the-floor-and-keys-its-log-to-the-manifest also said which branch a
repository change is compared against and that local changes count.

Since then, one pull request at a time, the skill and its references gained further lines on how
to verify, which branch and which local changes to include, how to build a harness step by step,
and what shape each log entry takes. Each line was reasonable when added. Together they spend
attention on every run and hold a better model to today's method. `/do` has no eval suite, so no
measurement would show the cost.

## Decision
`/do` states the goal, which is to make every Acceptance Criterion and Global Invariant hold on
fresh evidence, and the conventions other skills, tools and later sessions depend on. How it
works and how it verifies are the run's to decide.

A line stays in `/do` or its references only when one of these holds:

- it carries a ruling the owner or a decision record made;
- it fixes a convention or fact the run cannot read elsewhere, such as the log path, the goal
  block another tool parses, or where the harness bullet goes;
- it corrects a default a model has been observed to take.

What a capable model does on its own, or can read from the files it is pointed at, is left out.
That covers which branch and which local changes to compare, the order and manner of checking,
and how to use the harness, which its own `--help` explains. The two floor lines on the diff base
and local changes are dropped on these grounds.

The conventions kept include:

- the completion contract and its goal block;
- amendments only through the authoring skill;
- the execution log's path and what a resumed run needs from it;
- the ratchet, and recording findings below a gate's bar instead of repairing them;
- the user's-call and Taste rules;
- the ask-first agreement;
- locks and debt;
- the project definition.

## Alternatives Considered
- **A thin wrapper around a host goal command**: rejected for the reasons in
  20260806-verification-is-bookkeeping-and-a-stop-condition. A bare goal drops the stop
  condition, threshold discipline and the log a resumed run reads, and goal commands differ by
  host.
- **Trim only *What holds for every gate***: rejected. The references load into the same runs and
  had drifted the same way.

## Consequences

### Positive
- A newer model can verify by a better route without a sentence holding it to an old one.
- Every run spends less attention on instructions it does not need.

### Negative
- A run that does need a method line has none to fall back on, so a real failure must be observed
  before one is added back.
- Whether a new line is method or convention stays a judgment made at review.

## Enforced by
partly — `tests/test_dist_skill_references.py`, `tests/test_goal_contract_blocks.py`,
`tests/test_shared_blocks.py` and `tests/test_projectless.py` pin the conventions `/do` must keep.
Whether an added line prescribes method stays judgment, applied with the prompt-engineering
skill's provenance test at review.

## Source
- Session: the owner's steering during the surfaces v5 change, 2026-10-15
- Related: Narrows 20260914-one-skill-per-beat-built-from-the-lean-body; see also
  20260806-verification-is-bookkeeping-and-a-stop-condition
