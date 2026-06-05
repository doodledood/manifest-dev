# Definition: Pi clean verifier session fanout

## 1. Intent & Context
- **Goal:** Make the Pi Harness-level Do runtime actually run an independent verifier fanout before completion, instead of asking the executor to self-certify.
- **Mental Model:** `/manifest-do` owns the executor session. When the executor believes implementation is ready, it calls a runtime verification tool. That tool parses the manifest, launches clean verifier subagent sessions per Acceptance Criterion and Global Invariant, aggregates PASS / FAIL / BLOCKED reports, and only then allows the final done outcome. Failures return to the executor for repair; blockers may be escalated.

## 2. Approach
- Add a `manifest_dev_request_verification` Pi tool alongside `manifest_dev_report_outcome`.
- Parse manifest gate IDs and `verify.prompt` blocks from the manifest markdown.
- Use the installed Pi subagents service to spawn one clean verifier subagent per gate with `inheritContext: false`.
- Persist verification reports in Pi session entries and keep latest verification state in runtime memory for the done gate.
- Reject `outcome="done"` until the matching run has an all-PASS verification report.
- Document the runtime dependency and keep `/do`, `/done`, and `/escalate` out of Pi skills.

## 3. Global Invariants
- [INV-G1] Project gates pass for changed code/tests/docs.
  ```yaml
  verify:
    prompt: "Run focused automated verification for the Pi runtime change: pytest covering distribution references, JSON validation for package/metadata, TypeScript syntax/static checks where feasible, and Pi command discovery smoke tests if locally available. PASS if all available checks succeed. FAIL with command output summary if any fail. BLOCKED only if a required local tool is unavailable and no reasonable static fallback exists."
    agent: "test-quality-reviewer"
  ```
- [INV-G2] Runtime claims stay honest.
  ```yaml
  verify:
    prompt: "Inspect package metadata, Pi extension source, README files, sync-tools reference, ADR/context, and component namespace metadata. PASS only if docs claim the implemented clean verifier subagent fanout and accurately document remaining limitations. FAIL if docs imply `/do` itself is installed as a Pi skill or hide the Pi subagents runtime prerequisite."
    agent: "change-intent-reviewer"
  ```
- [INV-G3] Completion cannot bypass verification.
  ```yaml
  verify:
    prompt: "Inspect `pi/extensions/manifest-dev.ts`. PASS if `manifest_dev_report_outcome` rejects `outcome=done` unless `manifest_dev_request_verification` previously produced an all-PASS report for the same run id. FAIL if done can still be reported from executor self-assessment alone."
    agent: "contracts-reviewer"
  ```

## 4. Deliverables

### Deliverable 1: Clean verifier fanout runtime

**Acceptance Criteria:**
- [AC-1.1] The extension exposes a verification request tool.
  ```yaml
  verify:
    prompt: "Inspect the Pi extension source. PASS if it registers `manifest_dev_request_verification` with structured parameters including run id and manifest path, persists verification entries, and returns an aggregate PASS / FAIL / BLOCKED report. FAIL if verification remains prose-only or is folded into the final outcome tool."
    agent: "contracts-reviewer"
  ```
- [AC-1.2] The verifier tool launches isolated subagents per manifest gate.
  ```yaml
  verify:
    prompt: "Inspect the Pi extension source. PASS if it parses Acceptance Criteria and Global Invariants from the manifest, spawns a subagent for each gate through the Pi subagents service, passes `inheritContext: false`, waits for completion, and aggregates each subagent verdict. FAIL if the executor session itself performs the verifier work or if subagents inherit the executor conversation."
    agent: "code-design-reviewer"
  ```
- [AC-1.3] Failed verification routes back to repair instead of ending the run.
  ```yaml
  verify:
    prompt: "Inspect prompts and tool return behavior. PASS if FAIL reports instruct the executor to repair and call verification again, PASS reports instruct it to report done, and BLOCKED reports instruct it to escalate only with concrete blockers. FAIL if a failed verifier report terminates the run as done or auto-escalates without executor context."
    agent: "prompt-reviewer"
  ```

### Deliverable 2: Runtime dependency and docs

**Acceptance Criteria:**
- [AC-2.1] The package declares and validates the Pi subagents runtime dependency.
  ```yaml
  verify:
    prompt: "Inspect `package.json`, the Pi extension, and docs. PASS if `@gotgenes/pi-subagents` is declared as a runtime peer/dependency or otherwise explicitly required, the extension fails gracefully when its service is unavailable, and docs include the install/enable command. FAIL if the verifier tool assumes a missing service will exist silently."
    agent: "contracts-reviewer"
  ```
- [AC-2.2] Pi docs describe the implemented verifier loop and boundaries.
  ```yaml
  verify:
    prompt: "Inspect root README, `dist/pi/README.md`, sync-tools Pi reference, ADR/context, and `dist/pi/component-namespaces.json`. PASS if they mention `manifest_dev_request_verification`, clean subagent verifier fanout, the done gate, and continued runtime ownership of `/do`/`/done`/`/escalate`. FAIL if they still say full verifier fanout is future work."
    agent: "docs-reviewer"
  ```

### Deliverable 3: Guardrails and landing

**Acceptance Criteria:**
- [AC-3.1] Tests guard the new Pi verifier contract.
  ```yaml
  verify:
    prompt: "Inspect and run focused tests. PASS if tests assert the new verifier tool, subagent dependency, isolated spawn behavior, done-gate enforcement, updated metadata, and docs. FAIL if removing `manifest_dev_request_verification` or `inheritContext: false` would not fail tests."
    agent: "test-quality-reviewer"
  ```
- [AC-3.2] Branch is pushed with an intentional conventional commit.
  ```yaml
  verify:
    prompt: "Inspect git status, commit, and remote branch. PASS if only intentional files are committed, unrelated pre-existing untracked files remain uncommitted, the commit uses a conventional message, and the branch is pushed. FAIL if unrelated files are included or verification was skipped."
    agent: "operational-readiness-reviewer"
  ```
