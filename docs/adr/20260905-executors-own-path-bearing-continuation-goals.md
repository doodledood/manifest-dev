# ADR: Executors own continuation goals with a concrete Manifest path

## Status
Accepted

## Area
Goal setting

## Context

A continuation goal can remain available after the conversation identifying its
Manifest has been lost. The previous contract named “this run’s Manifest” and
required a checkpoint note, but supplied no locator for that note. Even direct
executor invocations omitted their known Manifest path to share a contract with
chains that started before the file existed.

The chosen trade-off is to begin automatic continuation at execution. Understanding
and definition still run autonomously within the chain, but an interruption there
requires the caller to restart them.

## Decision

`auto` and `just-auto` leave continuation to `do` and `just-do`. They pass the exact
Manifest path produced by definition and emit no earlier goal. Autonomous
investigation inside `auto` retains its Read checkpoint without setting a phase
goal; standalone autonomous investigation keeps its existing backstop.

Each executor emits the same goal block with the concrete absolute Manifest path
in its opening sentence. The block instructs a resumed run to read that file. Native
and manual emission use the same text, with only the path substituted. Shared
blocks retain byte-identity checks, literal emission, and non-emitted fence labels.

`babysit-pr` retains its independent PR lifecycle ownership. Its known PR reference
identifies the work before discovery or synthesis; it continues to record the
Manifest path when available and carries a separate PR goal block plus the shared
gate-ledger clause. The PR goal has no unknown Manifest-path slot. Nested execution preserves this broader contract.

## Alternatives Considered

- **Keep chain goals and add a durable checkpoint locator:** supports continuation
  before definition, but introduces another recovery artifact when execution-only
  continuation is acceptable.
- **Update or reprint the goal after definition:** depends on mutable host goals or
  a person replacing an earlier pasted contract.
- **Choose the Manifest path before definition:** moves file naming into the chain
  and changes the definition input contract solely to retain the earlier goal.

## Consequences

### Positive

- Executor goals identify the Manifest without relying on prior conversation.
- Chains no longer need a contract for a file that does not yet exist.
- Both executor variants retain the same completion text and evidence requirements.

### Negative

- An interrupted understanding or definition phase has no chain continuation goal.
- A named local file must remain readable; the goal does not recover deleted files
  or transfer them between machines.
- PR tending retains its existing PR-based discovery and checkpoint dependency.

## Source

- Decision: accept execution-only continuation in exchange for an explicit Manifest
  path, 2026-09-05.
- Narrows 20260623-use-universal-goal-setting-language: portable emission remains;
  chains no longer own a goal.
- Narrows 20260624-use-outcome-gated-auto-continuation: artifact-gated completion and
  the investigation checkpoint remain; the full-chain goal is retired.
- Narrows 20260828-continuation-goals-emit-verbatim-from-one-block: byte identity and
  verbatim emission remain; the chain prefix is retired and executors put the concrete
  Manifest path in the goal block itself.
- Narrows 20260830-shared-contract-blocks-name-the-beat-not-the-skill: shared text
  stays neutral between workflow variants; the chain prefix is retired.
- Narrows 20260830-a-contract-slot-exists-only-where-its-value-is-known: slots still
  require known values, but executors now include their known path in the goal
  block instead of omitting it to accommodate pre-Manifest callers.
