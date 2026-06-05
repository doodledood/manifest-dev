# manifest-dev

manifest-driven workflows for Claude Code. `/define` interviews you and writes a Manifest; `/do` executes it and verifies inline by spawning a subagent per Acceptance Criterion and Global Invariant.

## Language

**Manifest**:
A structured spec produced by `/define` that captures Deliverables, Acceptance Criteria, Global Invariants, Process Guidance, and an Approach.

**Deliverable**:
A discrete output a `/define` session commits to producing.
_Avoid_: Story, ticket, feature.

**Acceptance Criterion**:
A verifiable gate paired with a specific Deliverable.
_Avoid_: Test, check, requirement.

**Global Invariant**:
A property that must hold across all Deliverables in a Manifest.
_Avoid_: Constraint, rule.

**Process Guidance**:
A constraint on HOW to work during execution that isn't itself a verifiable gate.
_Avoid_: Guideline, best practice.

**Task File**:
A per-domain hint file keyed to a task type, kept as two parallel sets: `figure-out`'s carry probing fuel (the non-natural angles to press during understanding); `/define`'s carry Quality Gates and Defaults (encoder data). Each skill owns its own task-type index and loads its own set.

**Plugin**:
A Claude Code extension unit that may contain skills, agents, and optional hooks.

**Source Surface**:
A maintained implementation surface treated as authoritative for some part of manifest-dev, rather than a generated distribution copy.

**Pi-native Runtime Package**:
A Pi package that owns manifest-dev runtime entrypoints and deterministic orchestration code while reusing or generating shared manifest-dev prompt and skill assets.

**Pi Dist Target**:
The generated `dist/pi` asset set produced by `sync-tools`, containing Pi-compatible shared skills, runtime prompt assets, namespace metadata, and docs for the **Pi-native Runtime Package** to consume.

**Do/Verify Loop**:
The execution cycle where `/do` implements toward a **Manifest**, runs verifiers for every **Acceptance Criterion** and **Global Invariant**, routes failures or blockers, and finishes only after all gates pass.

**Executor Session**:
The `/do` session that performs implementation work and then yields control to the runtime for verification and adjudication.

**Harness-level Do**:
A Pi-native runtime entrypoint that replaces the portable `/do` skill. The current Pi extension provides command entrypoints, a clean verifier subagent fanout, and a structured done/escalate outcome gate. The remaining target architecture adds fuller persisted orchestration of executor checkpoints, repair-session resumption, escalation state, and optional contested-verifier handling.

**Verifier Session**:
A clean Pi subagent session spawned by Harness-level Do to evaluate exactly one **Acceptance Criterion** or **Global Invariant** from the **Manifest**. It does not inherit the **Executor Session** conversation and returns PASS, FAIL, or BLOCKED evidence to the runtime.

**Verification Judge**:
An optional fallback adjudicator with `/do`'s execution context that can review contested verifier reports or dubious blockers when the normal executor-verifier loop does not converge.

**Skill**:
A markdown-defined extension (`SKILL.md` + companion files) that adds a capability to Claude Code.

**Agent**:
An isolated subagent process with its own tools and context.
_Avoid_: Subprocess, worker.

**Hook**:
A handler that responds to a Claude Code lifecycle event (e.g., Stop, SessionStart).

**Babysit PR**:
An author-side workflow that tends an existing pull request through CI, review threads, description sync, and mergeability without pressing merge; companion to **Review PR**.
_Avoid_: Tend PR.

**Review PR**:
A reviewer-side workflow that inspects a pull request, posts comments, and advances review threads without becoming the author-side lifecycle owner.

**PR Grounding**:
The ordered evidence **Babysit PR** uses to decide whether a pull-request blocker is in scope to fix: explicit **Manifest**, PR description, commits and diff, then comments.

**CI One-Shot**:
A non-interactive **Babysit PR** run that performs every immediately actionable lifecycle step, then exits pending when only waiting remains.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** informs the workflow that owns it — `figure-out`'s probe set fuels interview probing, `/define`'s gate/Default set fuels encoding — and does not directly appear in the produced Manifest as a structural unit.
- A **Plugin** contains zero or more **Skills**, **Agents**, and optional **Hooks**.
- A **Skill** may invoke other **Skills** and spawn **Agents**.
- A **Pi-native Runtime Package** is a second **Source Surface** for runtime orchestration, not a replacement for the Claude Code **Plugin** source surface for shared prompt and skill assets.
- A **Pi Dist Target** is generated output, not a **Source Surface**; it packages the shared assets that the **Pi-native Runtime Package** installs or loads.
- A **Pi-native Runtime Package** owns deterministic behavior primarily for the **Do/Verify Loop**; `/figure-out` and `/define` remain shared prompt and skill behavior unless a future Pi-specific gap emerges.
- The current **Pi-native Runtime Package** exposes `/manifest-do`, `/manifest-auto`, `/manifest-babysit-pr`, `manifest_dev_request_verification`, and `manifest_dev_report_outcome`; verifier fanout uses clean Pi subagent sessions through `@gotgenes/pi-subagents`.
- An **Executor Session** does not own final verification; it yields after implementation, receives verifier failures for repair, and cannot report done until runtime verification passes.
- **Harness-level Do** is the Pi-specific implementation of the **Do/Verify Loop**; `/done` and `/escalate` become runtime outcomes rather than independent portable skills in that package.
- A **Verification Judge** is not part of the default **Do/Verify Loop**; it is reserved for later fallback if executor repair/escalation judgments prove unreliable.
- **Babysit PR** and **Review PR** can run asynchronously on the same pull request: **Review PR** applies quality pressure through comments and thread advancement, while **Babysit PR** drives the author-side lifecycle toward green and mergeable.
- **Babysit PR** belongs to the `manifest-dev-tools` **Plugin** as PR tooling, while orchestrating core `manifest-dev` **Skills** for manifest synthesis and execution.
- **Babysit PR** uses a **Manifest** synthesized from an existing pull request, then `/do` executes the lifecycle **Acceptance Criterion** through the `github-pr-lifecycle` **Agent**.
- **PR Grounding** constrains **Babysit PR** autonomy: comments are interpreted against stronger intent sources instead of becoming the specification by recency.
- **CI One-Shot** narrows `/do` retry cadence for **Babysit PR**: wait-shaped blockers are reported as pending instead of sleeping a runner.

## Flagged ambiguities

_None yet. Grow this section as figure-out --with-docs sessions surface clashes or canonicalizations._
