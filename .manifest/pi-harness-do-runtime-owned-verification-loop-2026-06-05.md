# Definition: Pi Harness-level Do runtime-owned verification loop

## 1. Intent & Context
- **Goal:** Make Pi Harness-level Do simple from the executor's perspective: the executor implements Manifest Deliverables, may run local checks, fixes harness-injected failed AC/INV reports, and stops; the Pi runtime owns authoritative verification, outcome gating, and repair/escalation routing.
- **Mental Model:** The **Executor Session** is a top-level worker, not the verifier orchestrator. Harness verification is lifecycle/runtime behavior, not a normal skill or LLM-visible tool. Each authoritative verification attempt starts a fresh **Verification Orchestrator Session** from zero inherited executor conversation; that clean session launches **Verifier Sessions** for the gates, and the aggregate result is injected back into the Executor Session as runtime-authored follow-up work. Local executor checks are allowed but non-authoritative; clean harness verification always runs again before done.
- **Scope Boundary:** No PR lifecycle gate is part of this manifest. `/manifest-babysit-pr` may need prompt/runtime consistency only because it is a Harness-level Do wrapper; mergeability, CI, approvals, and PR comments are out of scope.

## 2. Approach
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** Refactor the existing Pi extension so verification/outcome logic is callable by internal runtime functions. Use a lifecycle/checkpoint hook scoped to the active Executor Session to trigger a new Verification Orchestrator Session when the executor agent run ends. The orchestrator starts with only runtime-supplied run/manifest/workspace context, launches clean Verifier Sessions, returns an aggregate report to the runtime, and the runtime injects failed gate reports back into the Executor Session as a user-like/follow-up implementation message. PASS/BLOCKED outcomes are recorded through runtime state rather than executor tool calls.
- **Execution Order:**
  - D1 → D2 → D3 → D4
  - Rationale: Lock the documented boundary first, then change runtime behavior, then align prompts/docs/tests, then run cross-cutting verification.
- **Risk Areas:**
  - [R-1] Trigger fires for verifier/other child subagents instead of the Executor Session | Detect: tests or code inspection show executorSessionId guard and child-session ignore path.
  - [R-2] Runtime enters an infinite verify/repair loop or verifies while already verifying | Detect: run state has explicit lifecycle states and tests cover PASS, FAIL, BLOCKED, already-verifying guards, and repeated clean verification attempts after each repair checkpoint.
  - [R-3] Removing LLM-visible tools breaks `/manifest-auto` or `/manifest-babysit-pr` wrappers | Detect: wrapper prompts/tests show they route through the same runtime-owned lifecycle without asking the agent to call verification/outcome tools.
  - [R-4] Existing verifier guarantees regress while refactoring internals | Detect: tests preserve phase ordering, max concurrency, `verify.agent`, `verify.model`, `inheritContext: false`, multi-repo repo-map prompts, persistence, and freshness-bound done behavior.
  - [R-5] Verification results are not injected back into the Executor Session in a usable form | Detect: tests cover a runtime-authored follow-up/user-like message containing failed AC/INV evidence and repair direction.
  - [R-6] `/manifest-do` rejects the manifest path format emitted by `/define` (`~/.manifest-dev/...`) | Detect: tests cover leading-tilde expansion to the user's home directory instead of resolving `~` under the current workspace.
- **Trade-offs:**
  - [T-1] Internal runtime functions vs LLM-visible tools → Prefer internal functions because the executor's action space should not include harness orchestration.
  - [T-2] `agent_end` lifecycle trigger vs explicit checkpoint tool → Prefer lifecycle trigger, guarded by Executor Session id, because the executor should simply stop when it has nothing else to do.
  - [T-3] Clean Verification Orchestrator Session vs in-process runtime fanout → Prefer a clean orchestration session because even fanout coordination should start from zero inherited executor conversation; runtime code still owns triggering and result injection.
  - [T-4] Runtime BLOCKED outcome vs executor judgment → Prefer runtime BLOCKED outcome for verifier-reported external blockers; executor repair is for FAIL results.

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Harness verification/outcome controls are not LLM-visible executor capabilities.
  ```yaml
  verify:
    prompt: |
      Inspect pi/extensions/manifest-dev.ts, pi/extensions/manifest-dev-runtime.ts, dist/pi/component-namespaces.json, README.md, dist/pi/README.md, and relevant tests.

      PASS if the /manifest-do executor prompt and active tool/action surface do not expose manifest_dev_request_verification or manifest_dev_report_outcome as actions the executor is expected to call, and docs describe verification/outcome as runtime-owned lifecycle behavior.
      FAIL if executor prompts, tool metadata, or docs still make those controls normal LLM-visible /do capabilities.
      BLOCKED only if the relevant files cannot be read.
    agent: change-intent-reviewer
    phase: 1
  ```

- [INV-G2] Existing verifier fanout semantics are preserved.
  ```yaml
  verify:
    prompt: |
      Inspect the implementation and tests for Pi verifier fanout.

      PASS if the refactor preserves: one clean verifier subagent session per manifest AC/INV gate launched from a clean Verification Orchestrator Session; inheritContext false relative to the Executor Session; gate-level verify.agent and verify.model; phase ordering with later phases skipped on FAIL/BLOCKED; bounded same-phase concurrency; multi-repo repo-map prompt prepending; PASS/FAIL/BLOCKED parsing; and persistence of the latest verification with manifest/workspace freshness data.
      FAIL if any of those semantics are removed or untested without an explicit manifest amendment.
      BLOCKED only if the files or tests cannot be inspected.
    agent: code-design-reviewer
    phase: 1
  ```

- [INV-G3] Runtime trigger is scoped to the active Executor Session, not arbitrary subagents.
  ```yaml
  verify:
    prompt: |
      Inspect the runtime state and lifecycle hook implementation.

      PASS if Harness-level verification triggers only for the active Executor Session associated with the run, records or derives an executorSessionId, starts a fresh Verification Orchestrator Session with zero inherited executor conversation, ignores verifier/other child subagent session ends, and has a guard for already-verifying/done/blocked states.
      FAIL if any agent_end / child session completion can trigger harness verification for the run without the Executor Session guard, or if verification orchestration reuses the Executor Session conversation.
      BLOCKED only if lifecycle behavior cannot be inspected from code or tests.
    agent: code-bugs-reviewer
    phase: 1
  ```

- [INV-G4] Executor-local checks remain allowed but non-authoritative.
  ```yaml
  verify:
    prompt: |
      Inspect prompts, docs, and ADR/context updates.

      PASS if the executor is allowed to run normal local checks/tests while implementing, but final AC/INV verification and done/escalate authority remain explicitly owned by the harness runtime, a clean Verification Orchestrator Session, and clean Verifier Sessions.
      FAIL if docs or prompts either forbid useful local checks or treat executor-local checks as sufficient for done.
      BLOCKED only if the relevant prompt/docs cannot be read.
    agent: prompt-reviewer
    phase: 1
  ```

- [INV-G5] No PR lifecycle verification is introduced.
  ```yaml
  verify:
    prompt: |
      Inspect the manifest execution diff and generated/updated manifest-dev docs.

      PASS if this change does not add a github-pr-lifecycle verifier gate, PR mergeability checks, CI/review-thread lifecycle scope, or PR comment handling requirements. It is acceptable to update /manifest-babysit-pr prompt text only to keep Harness-level Do runtime semantics consistent.
      FAIL if PR lifecycle behavior becomes an acceptance gate or implementation scope.
      BLOCKED only if the diff cannot be inspected.
    agent: change-intent-reviewer
    phase: 1
  ```

- [INV-G6] Project verification commands pass.
  ```yaml
  verify:
    prompt: |
      From the repository root, run the relevant project checks for this change:
      1. node --experimental-strip-types --check pi/extensions/manifest-dev.ts
      2. node --experimental-strip-types --check pi/extensions/manifest-dev-runtime.ts
      3. node --experimental-strip-types --test tests/pi_extension_runtime.test.mjs
      4. .venv/bin/python -m pytest tests/test_pi_extension_runtime.py tests/test_dist_skill_references.py
      5. .venv/bin/ruff check claude-plugins/
      6. .venv/bin/black --check claude-plugins/
      7. .venv/bin/mypy

      PASS if all commands complete successfully, or if a command is skipped only because its executable/runtime is unavailable and the skip is reported with evidence.
      FAIL if any available command fails.
      BLOCKED only for missing runtime/tooling that prevents the verifier from running the commands.
    phase: 2
  ```

- [INV-G7] Code review suite has no threshold-level findings.
  ```yaml
  verify:
    prompt: |
      Review the final diff for this manifest. Apply these thresholds:
      - change-intent-reviewer: no LOW+ findings
      - code-bugs-reviewer: no LOW+ findings
      - operational-readiness-reviewer: no MEDIUM+ findings
      - code-maintainability-reviewer: no MEDIUM+ findings
      - code-simplicity-reviewer: no MEDIUM+ findings
      - test-quality-reviewer: no MEDIUM+ findings
      - code-testability-reviewer: no MEDIUM+ findings
      - docs-reviewer: no MEDIUM+ findings
      - code-design-reviewer: no MEDIUM+ findings
      - prose-value-reviewer: no MEDIUM+ findings
      - context-file-adherence-reviewer: no MEDIUM+ findings
      - type-safety-reviewer: no LOW+ findings for TypeScript/Python typed changes

      PASS if no listed reviewer would raise a threshold-level finding.
      FAIL if any threshold-level finding exists; include concrete file/line evidence and the reviewer lens.
      BLOCKED only if the diff cannot be inspected.
    phase: 2
  ```

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Read current Pi extension docs/examples before changing lifecycle behavior; use `agent_end`, `sendUserMessage`, run-state persistence, and active-tool controls according to documented Pi semantics.
- [PG-2] Preserve existing verifier fanout code by extraction/refactor where possible; do not rewrite the verifier parser/aggregation path from scratch unless tests force it.
- [PG-3] Keep executor prompts short and work-focused: implement Deliverables, run useful local checks, fix runtime-injected failed AC/INV reports, stop when done.
- [PG-4] Treat currently registered harness tools as compatibility scaffolding to remove or hide from `/do`, not as the desired executor contract.
- [PG-5] Do not add PR lifecycle gates or mergeability work to this change.
- [PG-6] Identify affected consumers before edits: `/manifest-do`, `/manifest-auto`, `/manifest-babysit-pr`, dist/pi docs/metadata, runtime tests, and sync-tools reference tests.
- [PG-7] Treat the injected verification result as a runtime-authored user/follow-up message to the Executor Session, not as hidden context the executor might miss.
- [PG-8] Normalize user-supplied manifest paths before existence checks; support leading `~`/`~/` consistently with the manifest handoff path that `/define` emits.

## 5. Known Assumptions

- [ASM-1] Pi's `agent_end` event can serve as the Stop-hook-equivalent checkpoint for the top-level Executor Session. | Default: Use `agent_end` guarded by executorSessionId. | Impact if wrong: The runtime may need a different Pi lifecycle event or a minimal checkpoint command.
- [ASM-2] Runtime-internal functions can replace LLM-visible verification/outcome tools without losing needed behavior. | Default: Refactor tool execute bodies into internal functions and stop exposing them to the `/do` executor. | Impact if wrong: A hidden/operator-only compatibility surface may be needed, but it must remain outside the executor action space.
- [ASM-3] For `/manifest-auto` and `/manifest-babysit-pr`, the runtime can know or assign the manifest path early enough to run the same lifecycle loop. | Default: Preassign a run manifest path or otherwise persist it in run state before execution verification is needed. | Impact if wrong: Wrapper commands need a narrower follow-up design before tool hiding can fully apply to them.
- [ASM-4] BLOCKED verifier reports are external/runtime blockers, not executor repair work. | Default: Runtime records a resumable escalation/blocker state and surfaces it to the user. | Impact if wrong: Some BLOCKED cases may need a future adjudication/judge path.
- [ASM-5] Pi can start or emulate a fresh Verification Orchestrator Session for each verification attempt. | Default: Use a new Pi session/SDK session or an equivalent clean subagent-like orchestration context that does not inherit the Executor Session conversation. | Impact if wrong: The implementation must find another isolation primitive before finalizing the runtime loop.
- [ASM-6] Supporting leading-tilde manifest paths belongs in the Pi command path resolver rather than requiring users to pass absolute expanded paths. | Default: Expand `~` and `~/...` against `homedir()` before resolving relative paths against `cwd`. | Impact if wrong: Users following `/define` handoff instructions can hit false `Manifest not found` errors.

## 6. Deliverables
*Ordered by execution order from Approach.*

### Deliverable 1: Documented role boundary and design intent

**Acceptance Criteria:**
- [AC-1.1] The ADR for runtime-owned Harness-level Do verification trigger exists and captures the refined decision.
  ```yaml
  verify:
    prompt: |
      Inspect docs/adr/20260605-runtime-owns-harness-do-verification-trigger.md.

      PASS if it records that Harness-level Do keeps the executor simple, permits local checks only as non-authoritative implementation aids, keeps authoritative verification/outcome runtime-owned, requires a fresh verification orchestration session per attempt whose results are injected back into the Executor Session, rejects LLM-visible harness verification/outcome tools for the /do executor, and mentions the accepted interim/scaffolding distinction.
      FAIL if any of those decision points are absent or contradicted.
      BLOCKED only if the ADR file cannot be read.
    agent: docs-reviewer
    phase: 1
  ```

- [AC-1.2] Project vocabulary reflects the Executor Session boundary.
  ```yaml
  verify:
    prompt: |
      Inspect CONTEXT.md.

      PASS if Executor Session is defined as the top-level Harness-level Do worker that implements Deliverables and repairs failed AC/INV reports; Verification Orchestrator Session is defined as the clean session that starts from zero inherited executor conversation, launches Verifier Sessions, aggregates reports, and returns results to the runtime; and relationships make clear the Executor Session does not own verification trigger, verifier fanout, adjudication, or final outcome.
      FAIL if CONTEXT.md still implies the executor owns final harness verification, lacks the verification orchestration concept, or uses ambiguous "main session" terminology as canonical language.
      BLOCKED only if CONTEXT.md cannot be read.
    agent: docs-reviewer
    phase: 1
  ```

### Deliverable 2: Runtime-owned lifecycle verification loop

**Acceptance Criteria:**
- [AC-2.1] Verification fanout and outcome reporting are callable as runtime-internal functions.
  ```yaml
  verify:
    prompt: |
      Inspect pi/extensions/manifest-dev.ts and pi/extensions/manifest-dev-runtime.ts.

      PASS if the code that parses manifests, starts or drives a clean Verification Orchestrator Session, spawns verifier subagents, records verification state, evaluates done readiness, and records done/escalate outcomes can be invoked by extension runtime code without requiring an LLM tool call from the executor.
      FAIL if the only way to perform harness verification or report outcome remains an LLM-visible tool execution, or if orchestration can only run inside the Executor Session conversation.
      BLOCKED only if the relevant code cannot be inspected.
    agent: code-design-reviewer
    phase: 1
  ```

- [AC-2.2] Harness verification triggers when the Executor Session completes an implementation/repair run.
  ```yaml
  verify:
    prompt: |
      Inspect lifecycle event handling and run-state code.

      PASS if an active /manifest-do-style run records the Executor Session identity and an agent_end or equivalent lifecycle event for that session triggers a fresh Verification Orchestrator Session when the run is in executing/repairing state.
      FAIL if the executor still has to call a verification tool/checkpoint explicitly, if verification never starts after the executor stops, or if the verification attempt inherits the Executor Session conversation.
      BLOCKED only if Pi lifecycle behavior cannot be determined from code/tests.
    agent: code-bugs-reviewer
    phase: 1
  ```

- [AC-2.3] Runtime routes verification outcomes without executor protocol decisions.
  ```yaml
  verify:
    prompt: |
      Inspect runtime outcome routing after verifier fanout.

      PASS if PASS records a done outcome or displays final done state without asking the executor to call a report tool; FAIL injects a runtime-authored user-like/follow-up repair message into the Executor Session containing the failed AC/INV evidence; and BLOCKED records/surfaces a resumable blocker without asking the executor to decide final escalation.
      FAIL if PASS/FAIL/BLOCKED routing still depends on the executor choosing manifest_dev_report_outcome or manifest_dev_request_verification calls, or if failed verification results are not delivered back to the Executor Session as actionable work.
      BLOCKED only if the routing code cannot be inspected.
    agent: code-bugs-reviewer
    phase: 1
  ```

- [AC-2.4] Each repair checkpoint reruns verification in a new clean session.
  ```yaml
  verify:
    prompt: |
      Inspect the lifecycle loop implementation and tests.

      PASS if after a FAIL result is injected into the Executor Session and the executor stops again, the runtime starts another fresh Verification Orchestrator Session rather than reusing the prior orchestrator/verifier context. PASS also requires that each attempt can launch its own verifier subagents.
      FAIL if repair verification reuses stale verifier/orchestrator context or does not retrigger after the executor stops again.
      BLOCKED only if the lifecycle loop cannot be inspected.
    agent: code-testability-reviewer
    phase: 1
  ```

- [AC-2.5] `/manifest-do` resolves home-relative manifest paths.
  ```yaml
  verify:
    prompt: |
      Inspect resolveManifestPath or equivalent command path handling in pi/extensions/manifest-dev.ts and its tests.

      PASS if `/manifest-do ~/.manifest-dev/manifests/example.md` resolves to `$HOME/.manifest-dev/manifests/example.md` (not `<cwd>/~/.manifest-dev/...`), quoted paths still work, ordinary relative paths still resolve against `cwd`, and missing files still produce a clear Manifest not found error with the expanded path.
      FAIL if leading `~` is treated as a literal workspace path or if relative/quoted path behavior regresses.
      BLOCKED only if command path handling cannot be inspected.
    agent: code-bugs-reviewer
    phase: 1
  ```

- [AC-2.6] The lifecycle loop avoids recursion and stale done states.
  ```yaml
  verify:
    prompt: |
      Inspect run-state transitions and tests.

      PASS if the runtime has explicit guards for already-verifying, done, blocked, missing manifest, changed manifest, changed workspace after verification, and child/subagent session completion. PASS also requires evidence that FAIL repair follow-ups can loop back to a new clean Verification Orchestrator Session after the executor stops again.
      FAIL if a plausible infinite loop, child-session trigger, stale PASS/done path, or stale verification-session reuse path remains.
      BLOCKED only if state-transition code/tests cannot be inspected.
    agent: code-testability-reviewer
    phase: 1
  ```

### Deliverable 3: Simplified Harness-level Do prompts and surfaces

**Acceptance Criteria:**
- [AC-3.1] `/manifest-do` prompt no longer teaches the executor the harness verification protocol.
  ```yaml
  verify:
    prompt: |
      Inspect buildManifestDoPrompt in pi/extensions/manifest-dev.ts.

      PASS if the prompt tells the executor to read the manifest, implement Deliverables, run useful local checks/tests, repair runtime-injected failed AC/INV reports, and stop when it has nothing else to do; and it does not mention manifest_dev_request_verification, manifest_dev_report_outcome, or any instruction to report done/escalate through a tool.
      FAIL if the prompt still teaches the executor to call harness verification/outcome tools.
      BLOCKED only if the prompt builder cannot be read.
    agent: prompt-reviewer
    phase: 1
  ```

- [AC-3.2] `/manifest-auto` and `/manifest-babysit-pr` wrappers do not reintroduce executor-managed verification.
  ```yaml
  verify:
    prompt: |
      Inspect buildManifestAutoPrompt and buildManifestBabysitPrompt in pi/extensions/manifest-dev.ts.

      PASS if both wrappers route execution through the runtime-owned Harness-level Do loop without telling the agent to call manifest_dev_request_verification or manifest_dev_report_outcome. The wrappers may still invoke figure-out/define or synthesize a manifest as needed.
      FAIL if either wrapper still makes the LLM responsible for invoking harness verification/outcome tools.
      BLOCKED only if the prompt builders cannot be read.
    agent: prompt-reviewer
    phase: 1
  ```

- [AC-3.3] Public docs and Pi metadata describe runtime-owned verification accurately.
  ```yaml
  verify:
    prompt: |
      Inspect README.md, dist/pi/README.md, dist/pi/component-namespaces.json, and the sync-tools Pi reference/tests if changed.

      PASS if Pi documentation no longer says the executor calls manifest_dev_request_verification or manifest_dev_report_outcome, metadata does not advertise those as LLM-facing extension tools for /do, and docs still explain verifier fanout, done gating, configuration flags, and clean subagent sessions.
      FAIL if docs/metadata still expose the old executor-called tool model or omit the replacement runtime-owned model.
      BLOCKED only if docs/metadata cannot be read.
    agent: docs-reviewer
    phase: 1
  ```

### Deliverable 4: Tests cover the runtime boundary

**Acceptance Criteria:**
- [AC-4.1] Runtime unit tests cover internal verification and outcome helpers.
  ```yaml
  verify:
    prompt: |
      Inspect tests/pi_extension_runtime.test.mjs and related Python wrappers.

      PASS if tests cover the extracted internal verification/outcome behavior, including PASS/FAIL/BLOCKED records, done readiness freshness, run-state persistence, verifier prompt construction, phase/chunk ordering, and config resolution.
      FAIL if extraction removed test coverage or key existing behaviors are now untested.
      BLOCKED only if tests cannot be inspected.
    agent: test-quality-reviewer
    phase: 1
  ```

- [AC-4.2] Runtime lifecycle tests cover executor-scoped trigger and repair loop behavior.
  ```yaml
  verify:
    prompt: |
      Inspect tests for the Pi extension/runtime lifecycle.

      PASS if tests or deterministic fixtures cover: /manifest-do starts a run with executorSessionId; leading-tilde manifest paths resolve to the user's home directory; executor-session end triggers a clean Verification Orchestrator Session; child/subagent session end does not trigger the loop; FAIL injects a repair follow-up/user-like message into the Executor Session; a second executor stop after repair starts another clean Verification Orchestrator Session; PASS records done; BLOCKED records/surfaces a resumable blocker; and already-verifying/done/blocked states do not retrigger.
      FAIL if these lifecycle behaviors are missing from tests.
      BLOCKED only if the test surface cannot be inspected.
    agent: test-quality-reviewer
    phase: 1
  ```

- [AC-4.3] Distribution/reference tests align with the new runtime-internal model.
  ```yaml
  verify:
    prompt: |
      Inspect tests/test_dist_skill_references.py and generated dist/pi files.

      PASS if tests assert the Pi package still exposes the Harness-level commands and shared skills, but no longer require manifest_dev_request_verification or manifest_dev_report_outcome to be advertised as LLM-facing extension tools. Tests should still require runtime dependencies, verifier fanout documentation, and absence of /do, /done, /escalate as normal Pi skills.
      FAIL if tests continue to encode the old LLM-visible tool contract or stop checking the runtime boundary.
      BLOCKED only if tests/dist files cannot be inspected.
    agent: test-quality-reviewer
    phase: 1
  ```
