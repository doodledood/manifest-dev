# Definition: Pi Harness-level Do runtime entrypoints

## 1. Intent & Context
- **Goal:** Add a real, source-owned Pi extension surface for manifest-dev Harness-level Do entrypoints so `/auto` and `/babysit-pr` no longer need to be excluded as impossible on Pi.
- **Mental Model:** `/do`, `/done`, and `/escalate` should still not be ordinary Pi skills. In Pi they are runtime behavior: a command starts the Do run, and a structured runtime tool records final completion or escalation. The first landed slice can be command/tool orchestration; full multi-session verifier fanout remains future runtime work unless implemented and tested.

## 2. Approach
- Add a source-owned Pi extension under a non-generated path and point repo-root `package.json` at it.
- Register `/manifest-do <manifest-path>` as the Harness-level Do entrypoint and `/manifest-auto` plus `/manifest-babysit-pr` as Pi-aware wrappers that route through manifest-dev skills and then `/manifest-do`.
- Register a structured `manifest_dev_report_outcome` tool for runtime-owned `done` and `escalate` outcomes, persisted with Pi session entries.
- Update Pi docs, sync-tools reference, README surfaces, namespace metadata, and tests so they describe the implemented command/tool slice without overclaiming deterministic verifier fanout.

## 3. Global Invariants
- [INV-G1] Project gates pass for changed code/tests/docs.
  ```yaml
  verify:
    prompt: "Run focused automated verification for the Pi package/runtime change: pytest covering distribution references, formatter/linter checks for touched tests, JSON validation for package/metadata, and any feasible TypeScript syntax/static check. PASS if all available checks succeed. FAIL with command output summary if any fail. BLOCKED only if a required local tool is unavailable and no reasonable static fallback exists."
    agent: "test-quality-reviewer"
  ```
- [INV-G2] Runtime claims stay honest.
  ```yaml
  verify:
    prompt: "Inspect package metadata, Pi extension source, README files, sync-tools reference, and ADR/context. PASS only if docs claim the implemented command/wrapper/outcome-tool slice and clearly reserve full deterministic verifier fanout for future work. FAIL if docs imply `/do` itself is installed as a Pi skill or that independent verifier sessions already aggregate AC/INV verdicts when they do not."
    agent: "change-intent-reviewer"
  ```
- [INV-G3] `/do`, `/done`, and `/escalate` remain runtime-owned, not normal Pi skills.
  ```yaml
  verify:
    prompt: "Inspect `dist/pi/skills`, component namespace metadata, and package docs. PASS if `do`, `done`, and `escalate` are absent from Pi skills and represented through extension command/outcome semantics. FAIL if any runtime-owned skill is copied as an ordinary Pi skill."
    agent: "contracts-reviewer"
  ```
- [INV-G4] Prompt text is minimal and edge-safe.
  ```yaml
  verify:
    prompt: "Review any prompts embedded in the Pi extension or docs. PASS if they state the goal, output contract, and escalation/done tool use without trying to encode unsupported Pi internals. FAIL if prompts are bloated, contradictory, or make the executor self-certify final success without the structured outcome tool."
    agent: "prompt-reviewer"
  ```

## 4. Deliverables

### Deliverable 1: Source-owned Pi extension

**Acceptance Criteria:**
- [AC-1.1] `package.json` installs a Pi extension from a source-owned path.
  ```yaml
  verify:
    prompt: "Inspect repo-root `package.json` and the referenced extension path. PASS if `pi.extensions` points at an existing source-owned TypeScript file outside generated `dist/pi`, existing `pi.skills` still points at `./dist/pi/skills`, and peer dependencies cover Pi/typebox imports. FAIL if package metadata references missing files or generated runtime code as source."
    agent: "contracts-reviewer"
  ```
- [AC-1.2] The extension registers `/manifest-do`, `/manifest-auto`, and `/manifest-babysit-pr`.
  ```yaml
  verify:
    prompt: "Inspect the Pi extension source. PASS if it registers command handlers for `manifest-do`, `manifest-auto`, and `manifest-babysit-pr`, validates required arguments, persists run/wrapper state with `appendEntry`, and uses `sendUserMessage` to hand work to the active Pi session. FAIL if wrappers still say they are unavailable or call portable `/do` directly."
    agent: "code-design-reviewer"
  ```
- [AC-1.3] The extension registers a structured done/escalate outcome tool.
  ```yaml
  verify:
    prompt: "Inspect the Pi extension source. PASS if it registers `manifest_dev_report_outcome` with structured parameters for `done` and `escalate`, persists outcome entries, and terminates the agent turn after final report. FAIL if completion/escalation is only prose or relies on `/done` or `/escalate` skills."
    agent: "contracts-reviewer"
  ```

### Deliverable 2: Pi target metadata and docs

**Acceptance Criteria:**
- [AC-2.1] Pi namespace metadata distinguishes compatible skills, extension commands, wrapper mappings, and runtime-owned skills.
  ```yaml
  verify:
    prompt: "Inspect `dist/pi/component-namespaces.json`. PASS if compatible skills are unchanged, `do`/`done`/`escalate` remain runtime-owned, wrapper skills map to extension commands, and extension commands/tools are recorded. FAIL if metadata still marks auto/babysit-pr merely pending."
    agent: "docs-reviewer"
  ```
- [AC-2.2] README surfaces document install/update plus the new Pi commands.
  ```yaml
  verify:
    prompt: "Inspect root README, plugin READMEs, and `dist/pi/README.md`. PASS if Pi install/update/remove/local flows remain easy to find, the new `/manifest-*` commands and outcome tool are documented where relevant, and the remaining full-verifier-fanout limitation is explicit. FAIL if docs conflict about whether Pi can start Harness-level Do."
    agent: "docs-reviewer"
  ```
- [AC-2.3] Durable architecture docs reflect the landed runtime slice.
  ```yaml
  verify:
    prompt: "Inspect `CONTEXT.md`, the Pi ADR, and the sync-tools Pi reference. PASS if they distinguish the implemented command/outcome-tool slice from future executor/verifier session orchestration, and if `sync-tools` guidance says Pi wrappers now exist as extension commands. FAIL if durable docs still say all Harness-level Do wrappers are pending."
    agent: "docs-reviewer"
  ```

### Deliverable 3: Automated guardrails

**Acceptance Criteria:**
- [AC-3.1] Tests guard the new package/runtime contract.
  ```yaml
  verify:
    prompt: "Inspect and run focused tests. PASS if tests assert package extension metadata, extension source contents, Pi skill exclusions, wrapper command mappings, outcome tool registration, and updated docs. FAIL if the old 'skills-only' assertions remain or if no test would catch removal of `/manifest-auto` or the outcome tool."
    agent: "test-quality-reviewer"
  ```
- [AC-3.2] Working tree is intentional and committed.
  ```yaml
  verify:
    prompt: "Inspect git status and final commit. PASS if only intentional task files are staged/committed, pre-existing unrelated untracked files are not included, the commit uses a conventional message, and the branch is pushed. FAIL if unrelated files are committed or verification was skipped."
    agent: "operational-readiness-reviewer"
  ```
