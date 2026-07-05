# ADR: Use host continuation as optional `/do` backstop, not a Pi-specific verifier runtime

## Status
Accepted

Supersedes `20260605-pi-native-runtime-package-source-surface` and the target architecture portions of `20260605-runtime-owns-harness-do-verification-trigger` and `20260610-own-pi-verifier-runner` that make Pi own deterministic Manifest parsing, verifier fanout, verdict aggregation, and done/escalation gating as a special runtime implementation. Those ADRs remain historical context for why the Pi runtime fanout existed.

## Context

manifest-dev's core `/do` contract is portable: the main agent reads the Manifest, implements Deliverables, and verifies every Acceptance Criterion and Global Invariant by launching an independent verifier execution for each gate using the gate's `verify.prompt` verbatim. Hosts differ in how much continuation they provide around that portable protocol. Codex CLI, for example, now exposes `/goal` as a durable thread-scoped objective that keeps working across turns until evidence satisfies the goal; other hosts may expose equivalent goal-setting or continuation capabilities, and some hosts may expose none or have them disabled.

Before this simplification, Pi had a heavier special implementation: a runtime extension command parsed the Manifest, ran manifest-dev-owned JSON subprocess verifiers per gate, aggregated PASS / FAIL / BLOCKED results, injected repairs, and recorded done only after an all-PASS freshness check. That bought deterministic runtime enforcement, but it also created a separate source surface and a Pi-specific `/do` behavior that had to be maintained alongside the portable skill contract.

The better host-level boundary is capability-based, not CLI-name-based: when the active environment exposes a durable goal-setting, continuation, or completion-check capability, manifest-dev should use it to keep the run alive until the normal `/do` verifier protocol is genuinely complete. When that capability is absent or disabled, the main agent still runs the verifier protocol, but there is no separate continuous enforcement loop beyond model discipline and any foreground run semantics.

This decision is about the host capability boundary, not any machine-specific setup.

## Decision

Align Pi `/do` with the portable manifest-dev `/do` model instead of treating Pi as a special deterministic verifier runtime.

The `/do` worker is responsible for executing the Manifest and running the verifier protocol: enumerate every Acceptance Criterion and Global Invariant with a `verify.prompt`, respect phase ordering, launch independent verifier executions using those prompts verbatim, repair FAIL results, route genuine BLOCKED results, and finish only after every gate has PASS evidence.

A host-provided goal-setting / continuation / durable-completion capability is an optional outer backstop. If the active host exposes such a capability, manifest-dev should set a concrete completion contract that makes the host continue or reopen the run until the ordinary `/do` verifier protocol is complete. That contract should be self-contained enough for the host checker to audit: manifest path, requirement to enumerate all AC/GI gates, independent verifier execution per gate, PASS evidence for each gate, repair-and-reverify behavior for FAILs, blocker handling for BLOCKED, and no completion while verification is missing or stale.

If no such host capability exists, manifest-dev should not fabricate a Pi-style runtime loop. It should run as prompt-level `/do`: the main agent performs the verification protocol and reports completion or blocker according to the skill contract, but no continuous host-level enforcement is guaranteed. This is a property of the active host configuration, not of a host brand; Codex with `/goal` enabled is continuation-capable, while a host or configuration without goal/continuation support is not.

Pi-specific runtime code may still provide native command wrappers, package loading, or convenience handoffs, but it should not be the authoritative Manifest verifier scheduler and done gate unless a future decision deliberately restores that stronger host-specific tier.

## Alternatives Considered

- **Keep Pi runtime-owned deterministic verifier fanout**: strongest enforcement — code parses gates, schedules subprocesses, aggregates results, and freshness-checks done — but preserves a separate Pi-specific source surface and duplicates the portable `/do` semantics.
- **Require a continuation capability on every host**: rejected because not every host provides one. Absence of a continuation capability should not make `/do` unavailable; it should simply mean no automatic cross-turn enforcement.
- **Make the continuation checker itself run the Manifest verification work**: rejected as the default boundary. A continuation checker can audit whether the worker performed required verification, but primary verifier execution belongs to the `/do` worker and its independent verifier contexts.
- **Drop verifier fanout entirely and rely on local checks**: rejected. The normal `/do` verifier protocol — one independent verifier execution per AC/GI gate — remains the artifact-trust mechanism.

## Consequences

### Positive

- Reduces Pi-specific runtime complexity and source-surface drift.
- Restores one conceptual `/do` model across Claude Code, Codex, OpenCode, Pi, and future hosts: the main agent runs the Manifest verifier protocol, and host continuation is an outer capability when present.
- Lets capable hosts provide stronger continuous execution without making that capability a hard dependency.
- Keeps the Manifest's independent verifier executions as the trust mechanism, instead of replacing them with ordinary local checks.

### Negative

- Pi loses the stronger deterministic runtime guarantee that code, rather than the worker agent, enumerates gates and aggregates verifier results.
- Correctness depends more on prompt discipline plus the host continuation checker when present.
- Without a host continuation capability, unattended runs can still stop prematurely, as in other prompt-level hosts.
- Any future implementation needs tests or review coverage for skipped gates, weak verifier evidence, phase-order drift, and premature completion under both continuation-capable and continuation-absent modes.

## Source

- Design note: host continuation is described as a generic capability rather than a machine-specific setup; when none exists or it is disabled, regular main-agent verification applies without continuous enforcement.
- External evidence: OpenAI Developers Codex docs, `Using Goals in Codex` and `Slash commands in Codex CLI`, describe `/goal` as a durable goal-setting capability that keeps a Codex thread working across turns and checks completion against evidence.
- Related: `20260605-runtime-owns-harness-do-verification-trigger`, `20260610-own-pi-verifier-runner`, `20260623-use-universal-goal-setting-language`.
