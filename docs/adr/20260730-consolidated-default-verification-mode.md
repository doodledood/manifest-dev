# ADR: Consolidated as the default /do verification mode

## Status
Accepted

## Context

`/do` evaluates every Acceptance Criterion and Global Invariant under a
run-level verification mode selected at launch: `per-gate`, `consolidated`, or
`self` (see 20260728-move-verification-execution-policy-to-do). The omitted-flag
default was `per-gate`: one fresh independent verifier execution per gate.

Two costs of that default grew with use. First, economy: a typical manifest
carries 10–15 gates, so every verification round launched that many verifier
executions, each re-reading the same artifact. Second, stability: many
independent fresh contexts resample the findings space each round — different
verifiers surface different findings across rounds, the executor over-repairs
in response, and previously passing gates go stale or break, producing
oscillation instead of convergence.

## Decision

Flip the omitted-flag default from `per-gate` to `consolidated`. One
independent verifier execution evaluates the outstanding gate set per round —
one artifact read, one coherent view, a separate verdict and evidence record
per gate. `per-gate` remains available as an explicit opt-in for
maximum-rigor runs; `self` is unchanged. No mode is renamed, added, or
removed, and the semantics of all three modes are untouched — only the
default changes.

## Alternatives Considered

- **Keep `per-gate` as the default**: strongest per-round recall, but pays the
  N-fold artifact-read cost on every round and exhibits the cross-round
  finding oscillation described above — rejected as the wrong default now that
  a single strong verifier evaluates a full gate set reliably.
- **A fourth "dynamic" mode** (agent decides per gate whether it deserves its
  own execution): hands the executor a lever over its own verification rigor
  with an incentive gradient toward under-isolation, and adds a mode's worth
  of docs, provenance wording, and flag surface — rejected.
- **Consolidated with skill-gate carve-outs** (specialized gates such as
  review-code each get their own execution): preserves reviewer depth but
  keeps exactly the independent contexts that oscillate most — rejected.

## Consequences

### Positive
- One artifact read per verification round instead of one per gate.
- One coherent verdict set per round; less cross-round finding variance and
  less repair churn.
- Lower cost per run under the default policy.

### Negative
- Lower per-round recall than `per-gate`: a single verifier context evaluates
  every outstanding gate, so runs that want maximum independent scrutiny must
  opt in with `--verification per-gate`.

## Source
- Supersedes the omitted-flag default choice in
  20260728-move-verification-execution-policy-to-do (the policy mechanism
  there is unchanged)
- Manifest: ~/.manifest-dev/manifests/manifest-20260730-220320.md
