# ADR: Runtime owns Harness-level Do verification trigger

## Status
Superseded by 20260623-use-host-continuation-as-optional-do-backstop

Historical context for the former Pi runtime-owned verification trigger and done gate. The current Pi target is a skill-only package: `/do` follows the portable main-agent verifier protocol, and host continuation is an optional outer backstop.

## Context

At the time of this ADR, the Pi-native manifest-dev package treated verification as runtime-owned once requested: `manifest_dev_request_verification` parsed the Manifest, spawned clean verifier subagent sessions, aggregated PASS / FAIL / BLOCKED verdicts, and `manifest_dev_report_outcome` blocked done until verification passed. That runtime-owned direction is superseded by the host-continuation ADR.

The remaining boundary leak at the time was trigger ownership. The then-current Harness-level Do prompt told the executor to call `manifest_dev_request_verification` when it believed implementation was ready. That still asked the executor to participate in orchestration. The user clarified the intended role boundary: Do should stay simple: implement Deliverables, run whatever local checks are useful while implementing, and fix failing Acceptance Criteria or Global Invariants injected by the harness.

This matters because the Do/Verify Loop's correctness should not depend on the executor remembering a verification protocol, choosing the right moment to invoke it, or having a verify-shaped skill/tool workflow in its mental model. The harness should behave like a Stop-hook-equivalent aware loop: when implementation work reaches a completion checkpoint, a clean verification orchestration session starts from zero inherited executor conversation, launches verifier execution contexts, and injects the aggregate result back into the executor session as either repair work, blocker state, or final done permission.

## Decision

The superseded decision was that Harness-level Do would keep the executor role minimal: the executor implements Manifest Deliverables, may run ordinary local checks/tests for implementation confidence, and repairs concrete failed Acceptance Criteria / Global Invariants returned by harness verification.

Under that superseded decision, the runtime owned the authoritative verification trigger, verification orchestrator session, verifier fanout, verdict aggregation, done gate, and escalation gate. Each verification attempt started a fresh Verification Orchestrator Session with zero inherited executor conversation; that clean session launched clean verifier execution contexts for the Manifest gates. In the later superseded Pi implementation those executions were JSON subprocesses. This happened even if the executor already ran local checks or sanity-checked criteria. Failed gates were injected back into the Executor Session as a runtime-authored follow-up/user-like repair message; passed harness verification unlocked the runtime done outcome; BLOCKED reports were routed through the runtime escalation path when they required human input, access, external state, or an unrecoverable decision.

Harness verification and outcome reporting should be runtime-internal orchestration paths, not LLM-visible tools available to the `/do` executor. `/do` must not be modeled as a verify skill, and the executor should not be prompted to self-direct the harness verification protocol. Executor-local checks are non-authoritative implementation aids. Any current explicit `manifest_dev_request_verification` or `manifest_dev_report_outcome` call by the executor is an interim implementation bridge, not the target architecture.

The loop repeats after repair: when the Executor Session stops again after acting on injected failed-gate results, the runtime starts another fresh Verification Orchestrator Session and reruns authoritative verification from clean context.

## Alternatives Considered

- **Executor calls a verification tool when ready**: rejected as the target shape because it leaks orchestration responsibility into the executor prompt and makes correctness depend on agent discipline.
- **LLM-visible harness verification/outcome tools**: rejected for the `/do` executor because tool visibility still makes the verification protocol part of the executor's action space.
- **Separate verify skill**: rejected because it makes verification a normal agent capability rather than a harness-owned lifecycle step.
- **Executor local checks as final verification**: rejected because executor checks have contaminated context and incentives; they are useful implementation aids, but final AC/INV verification needs clean sessions and runtime-owned aggregation.
- **Runtime Stop-hook-equivalent loop**: accepted because it matches the desired separation: executor attempts completion, runtime starts a clean verification orchestration session, failures re-enter as implementation work, and only the runtime can finish the run.

## Consequences

### Positive

- The executor prompt can shrink to the actual work: implement Deliverables, run useful local checks, and repair failed AC/INV reports.
- Verification becomes a lifecycle guarantee rather than a remembered instruction or visible executor capability.
- Clean verification orchestration and verifier execution contexts preserve independence from the executor's reasoning and implementation context.
- Runtime-authored follow-up messages make verifier results look like new work to the executor without exposing the verifier protocol itself.
- Done/escalate authority remains deterministic and outside normal skill behavior.

### Negative

- The Pi runtime needs a lifecycle/checkpoint mechanism that can detect attempted executor completion, start a clean verification orchestration session, and inject follow-up work into the Executor Session.
- Existing explicit tool-call wiring may need to remain temporarily until Pi exposes or manifest-dev implements the required stop/checkpoint trigger, but it should be treated as compatibility scaffolding rather than the executor contract.
- Tests must cover the orchestration boundary, not only the verifier fanout tool.
- The older Pi runtime ADR contains interim executor-mediated language; future readers need this ADR to understand the refined boundary.

## Source

- Session: `figure-out --with-docs`, 2026-06-05.
- User clarification: "do should just implmeent deliverables and fix failing ac/invs thats it".
- User clarification: "i odnt care if main session does verifications but the hanress level verification wil lrun them again; do shluld be simplistic".
- User accepted that `manifest_dev_request_verification` / `manifest_dev_report_outcome` should not remain visible to the `/do` executor.
- User clarification: verification should happen in a new session from zero; that session launches verifier executions; aggregate results are injected back into the Do session as a user-like message; when Do stops again, another clean verification session runs.
- Related: `20260605-pi-native-runtime-package-source-surface`
