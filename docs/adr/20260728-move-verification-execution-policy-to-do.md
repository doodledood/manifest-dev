# ADR: Move verification execution policy to `/do`

## Status
Accepted

## Context

A Manifest is the acceptance contract consumed by `/do`. It must carry enough
information to establish whether each Acceptance Criterion and Global Invariant
holds, while remaining independent of the host and execution strategy that
establishes it.

The current verify block crosses that boundary:

```yaml
verify:
  prompt: "..."
  model: "..."
  phase: 1
```

`prompt` is authored as an instruction to one fresh verifier, and `model`
selects that verifier's runtime. `/do` correspondingly has one verification
topology: one independent execution context per gate. This makes the
Manifest's meaning depend on a particular evaluator arrangement and prevents
the same ready Manifest from being executed under a different assurance and
cost trade-off.

Per-gate verification remains the strongest default because each gate receives
fresh, focused, independent judgment. It also repeats repository orientation,
tool setup, and context acquisition for every gate in every verification
round. A consolidated verifier can share that work across gates and is
therefore expected to reduce per-round calls and total context, although it may
be slower in wall-clock time where per-gate verifiers would have run in
parallel. Having the executor perform the checks itself removes verifier setup
entirely, but also removes independent artifact review.

These topology choices do not solve the aggregate convergence defect observed
in PR #239. That run spent nineteen repair rounds and roughly 130 verifier
executions because new findings kept moving between subjects; the multiplier
was repair rounds, not the fixed gate fan-out. Topology changes the cost and
assurance of a round. Aggregate stopping policy determines how many rounds are
allowed and remains a separate decision.

The lower-assurance choices also create a disposition risk if `/do` may select
them opportunistically: an executor could downgrade verification when work
becomes difficult or expensive. A verification mode must therefore be an
explicit, launch-time choice, never a runtime fallback.

## Decision

Verification semantics stay in the Manifest. Verification execution policy
moves to `/do`.

### Manifest schema

Replace the verify block with:

```yaml
verify:
  instructions: |
    <how to establish this gate, the evidence required, and its pass threshold>
  phase: 1
```

`instructions` is the topology-neutral evaluation procedure for the gate. It
contains the gate-specific context, evidence requirement, PASS / FAIL /
BLOCKED threshold, and any specialized skill activation needed to establish
the result. It does not assign an agent role, prescribe an isolated context, or
select a model. `/do` supplies the execution envelope for the selected mode.

The instructions remain self-contained. Per-gate mode may provide no other
gate context, consolidated mode must preserve each gate's own threshold, and
self-verification must not invent a different oracle. Removing the evaluation
procedure altogether would make changing `/do` mode silently change what
counts as acceptance.

`phase` remains optional, defaults to `1`, and expresses evaluation ordering
that holds under every mode. Lower phases must pass before later phases become
eligible. It is not a worker grouping or model-routing field.

This is a clean schema break. `/define` emits `verify.instructions` and never
emits `verify.prompt` or `verify.model`. `/do` rejects either removed field with
a clear instruction to redefine the Manifest. It does not translate, ignore,
or assign legacy semantics to them.

### `/do` execution policy

`/do` exposes:

```text
--verification per-gate|consolidated|self
--verifier-model <model>
```

Neither option is written back into the Manifest.

`--verification` defaults to `per-gate` when omitted:

- **`per-gate`** launches one fresh independent verifier execution for each
  eligible gate. This preserves the existing assurance model.
- **`consolidated`** launches one fresh independent verifier execution for the
  outstanding gates in a verification round. It evaluates them in phase order,
  returns a separate verdict and evidence record for every evaluated gate, and
  stops before a later phase when any gate in the current phase is not PASS.
- **`self`** has the `/do` executor follow each gate's instructions and record
  a separate verdict and evidence entry itself. No independent verifier
  execution is claimed.

All three modes use the same gate ledger, phase eligibility, evidence
freshness, repair, blocker routing, and completion condition. Every Acceptance
Criterion and Global Invariant still needs fresh PASS evidence. A mode never
waives a gate, converts FAIL to PASS by policy, or changes the gate's threshold.
A host continuation or goal capability remains an optional outer backstop and
does not add artifact-review independence to `self`.

The selected mode is immutable for a run. `/do` records it before execution and
never downgrades itself because of cost, elapsed rounds, difficult findings, or
model preference. Selecting a different mode starts a new run with a fresh
verification ledger so evidence with different provenance is not silently
mixed.

`--verifier-model` is optional and applies to `per-gate` and `consolidated`.
When omitted, verifier executions inherit the invoking context's model choice.
The value is a host model selector owned by the active execution environment;
if the host cannot honor an explicitly supplied selector, `/do` fails clearly
instead of pretending it did. Combining `--verifier-model` with `self` is an
error because self-verification necessarily uses the executor's model. There
is no per-gate model field or model map.

### Prompt architecture and callers

The common Do/Verify Loop remains in `/do`'s always-loaded spine. After
`--verification` is resolved — including the omitted flag becoming the default
`per-gate` value — `/do` loads exactly one of three sibling references:
per-gate, consolidated, or self. Each reference owns that mode's evaluator
topology, verifier-model compatibility, evidence provenance, and
mode-specific completion wording. The spine retains only selection plus shared
phase, ledger, staleness, verdict-routing, and completion mechanics; callers
and terminal helpers forward the selected reference's contract instead of
restating mode semantics.

`/auto` and Babysit PR accept and forward the verification mode and optional
verifier model, and their host-completion contracts describe the selected
evidence provenance. Review PR's manifest mode continues to perform independent
per-gate review; an author's cheaper `/do` choice does not lower reviewer-side
assurance, although Review PR consumes `verify.instructions` under the new
schema.

`/done` remains the common terminal marker and reports the selected mode
without overstating it:

- `per-gate`: independently verified per gate
- `consolidated`: independently verified by a consolidated verifier
- `self`: self-verified by the executor

The Execution Log records the selected mode, explicit or inherited verifier
model, and per-gate evidence provenance.

## Alternatives Considered

- **Keep per-gate verification as the only topology**: preserves maximum
  isolation and focus, but leaves users no explicit way to trade assurance for
  lower repeated setup and context cost.
- **Store topology and model in the Manifest**: rejected because they describe
  how `/do` executes a ready contract, not what the outcome must prove. It would
  also make Manifests host-specific and require redefining one merely to choose
  a different execution strategy.
- **Remove gate-level verification instructions from the Manifest**: rejected
  because a criterion statement alone does not always carry its evidence
  source, evaluation method, specialized skill, or pass threshold. Each mode
  would improvise a different oracle.
- **Expose `budget`, `balanced`, or `strict` profiles**: rejected because those
  names conceal the mechanism and do not promise a stable assurance property.
  Cost and latency are effects of topology, model, host parallelism, and repair
  rounds rather than intrinsic profile meanings.
- **Let `/do` downgrade verification after excessive spend or stalled repair
  rounds**: rejected because it turns lower assurance into an executor-owned
  escape hatch. Aggregate convergence protection may stop or escalate a run,
  but it may not silently weaken the verification contract.
- **Retain per-gate `verify.model` routing**: rejected because concrete model
  selection is execution policy and not portable across hosts. One run-level
  verifier model is sufficient until measured use cases justify a more
  expressive execution-only policy.
- **Use a different terminal marker for each mode**: rejected because terminal
  success remains all-fresh-PASS under every mode. `/done` should carry honest
  provenance rather than fragment the completion protocol.

## Consequences

### Positive

- A ready Manifest defines one acceptance contract that `/do` can execute under
  several explicit assurance topologies.
- Existing behavior and assurance remain the default.
- Lower-assurance modes are opt-in and launch-locked, so they cannot become a
  model-selected shortcut during a difficult run.
- Gate instructions become portable across isolated, consolidated, and
  executor-owned evaluation contexts.
- Model choice is exposed where it can affect execution cost without embedding
  host-specific names in a durable Manifest.
- Completion summaries and logs make evidence provenance visible instead of
  presenting every PASS as equivalent.

### Negative

- Existing Manifests using `verify.prompt` or `verify.model` become invalid and
  must be regenerated with `/define`.
- Consolidated verification trades per-gate focus and failure isolation for
  shared context, and may increase wall-clock time when independent verifiers
  could have run in parallel.
- Self-verification can miss defects the executor did not surface and provides
  no fresh-context artifact review; a host goal checker does not restore that
  property.
- A run-level verifier model loses the cheap-per-gate routing previously used
  for gates such as the acceptance ceiling. Restoring heterogeneous model
  routing would require a later execution-policy design.
- `/do`, `/done`, `/auto`, Babysit PR, Review PR manifest mode, distribution
  transforms, and public documentation must all agree on the new schema and
  provenance language.
- This decision reduces or removes per-round verifier overhead but does not
  bound aggregate repair rounds. Convergence protection still needs its own
  policy.

## Source

- Session: maintainer design discussion on verification cost, assurance, and
  Manifest ownership (2026-07-28).
- Evidence: PR #239, `Bound the acceptance contract from above, not only from
  below`.
- Related: `20260623-use-host-continuation-as-optional-do-backstop`.
- Related: `20260728-bound-the-acceptance-contract-from-above`.
- Related: `20260722-state-verification-sufficiency-not-only-necessity`.
