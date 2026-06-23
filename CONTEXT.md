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

**Evidence Ledger**:
The compact set of load-bearing claims — each carrying provenance and epistemic status (verified, inferred, or assumed) — that a figure-out read rests on and ships with.

**Read**:
The deliverable of a figure-out session: a named conclusion carrying confidence, the Evidence Ledger it rests on, and what would overturn it; naming the Read ends the skill.
_Avoid_: Conclusion, verdict, answer.

**Plugin**:
A Claude Code extension unit that may contain skills, agents, and optional hooks.

**Source Surface**:
A maintained implementation surface treated as authoritative for some part of manifest-dev, rather than a generated distribution copy.

**Universal Language**:
Prompt wording that names portable behavior or capability rather than a harness-specific primitive, so the same skill intent can run across Claude, Codex, OpenCode, Pi, or another host.

**Pi Package Target**:
The repo-root Pi package that installs manifest-dev's generated skills and prompt-template aliases (`/do`, `/auto`, `/babysit-pr`) without a manifest-dev TypeScript runtime extension.

**Pi Dist Target**:
The generated `dist/pi` asset set produced by `sync-tools`, containing Pi-compatible skills, prompt-template aliases, namespace metadata, and docs for the **Pi Package Target** to consume.

**Codex Plugin-native Distribution**:
The Codex distribution architecture (now shipped): a Codex plugin marketplace (`.agents/plugins/marketplace.json`) registering two native plugins (`manifest-dev`, `manifest-dev-tools`) under `dist/codex/plugins/`, each bundling skills. Codex plugins bundle skills/MCP/apps/hooks but **not** agents — which matches manifest-dev, since it ships no agents of its own: the quality reviewers ship as a progressive-disclosure `review-code` **skill** (one dimension per invocation), and the former functional agents (`check-pr`, `poll-slack`, `review-prompt`) ship as ordinary skills a general-purpose verifier activates. Replaces the install-time TOML stub generation and config merging of the retired installer.

**Codex Legacy Installer Target** (retired):
The former generated `dist/codex` installer-based distribution (`install.sh`, `install_helpers.py`, `config.toml` merge, `rules/`, `agents/*.toml`), which predated Codex plugin marketplaces and approximated reviewer agents through TOML stubs. Removed in favor of the **Codex Plugin-native Distribution**.

**OpenCode Plugin-native Distribution**:
The OpenCode distribution architecture: a generated OpenCode plugin under `dist/opencode/` that registers its bundled, OpenCode-flavored skills from package-local paths, registers slash-command wrappers for user-invocable skills via `cfg.command`, and is installed from a repo clone by file path — replacing the OpenCode global installer (`install.sh`, install-time suffix namespacing, generated command files) while keeping manifest-dev out of shared Agent Skills directories.
_Avoid_: OpenCode installer, global install, copied command files.

**Do/Verify Loop**:
The execution cycle where `/do` implements toward a **Manifest**, runs verifiers for every **Acceptance Criterion** and **Global Invariant**, routes failures or blockers, and finishes only after all gates pass.

**Host Continuation Backstop**:
A host-provided goal-setting, continuation, or completion-check capability that keeps or reopens a run until a durable completion contract is satisfied.

**Verifier Execution**:
An independent execution context launched by `/do` to evaluate exactly one **Acceptance Criterion** or **Global Invariant** from the **Manifest** using that gate's `verify.prompt` verbatim. In subagent-capable hosts it is typically a general-purpose subagent. It returns PASS, FAIL, or BLOCKED evidence to the `/do` workflow.

**Skill**:
A markdown-defined extension (`SKILL.md` + companion files) that adds a capability to Claude Code.

**Agent**:
An isolated subagent process with its own tools and context. Retained only as the generic Claude Code concept: manifest-dev ships **no agents of its own**. Verification is always a general-purpose subagent whose `verify.prompt` activates a skill (e.g. `check-pr`, `poll-slack`, `review-prompt`, `review-code`); the manifest schema has no `verify.agent` field.
_Avoid_: Subprocess, worker.

**Hook**:
A handler that responds to a Claude Code lifecycle event (e.g., Stop, SessionStart).

**Babysit PR**:
An author-side workflow that tends an existing pull request through CI, review threads, description sync, and mergeability without pressing merge; companion to **Review PR**.
_Avoid_: Tend PR.

**Review PR**:
A reviewer-side workflow that inspects a pull request, posts comments, and advances review threads without becoming the author-side lifecycle owner. Polymorphic on manifest presence: given `--manifest`, it skips the generic reviewer fleet and independently verifies *only* the **Manifest** — running each **Acceptance Criterion** and **Global Invariant** `verify.prompt` against the PR head and posting PASS/FAIL — which gives optionally cross-model verification of the contract; without one, it runs the generic `review-code` reviewer fleet for an ordinary PR carrying no contract.

**PR Grounding**:
The ordered evidence **Babysit PR** uses to decide whether a pull-request blocker is in scope to fix: explicit **Manifest**, PR description, commits and diff, then comments.

**CI One-Shot**:
A non-interactive **Babysit PR** run that performs every immediately actionable lifecycle step, then exits pending when only waiting remains.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A figure-out **Read** ships with the **Evidence Ledger** it rests on.
- `/define` encodes the understanding a figure-out **Read** establishes into a **Manifest** — formal **Deliverables** with verifiable gates — rather than re-deriving or re-investigating it.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** informs the workflow that owns it — `figure-out`'s probe set fuels interview probing, `/define`'s gate/Default set fuels encoding — and does not directly appear in the produced Manifest as a structural unit.
- A **Plugin** contains zero or more **Skills**, **Agents**, and optional **Hooks**.
- A **Skill** may invoke other **Skills** and spawn **Agents**.
- A **Pi Package Target** is package metadata plus generated assets, not a second runtime **Source Surface**.
- A **Pi Dist Target** is generated output, not a **Source Surface**; it packages the skills, prompt-template aliases, metadata, and docs that the **Pi Package Target** installs or loads.
- The **Pi Package Target** exposes `/do`, `/auto`, and `/babysit-pr` as prompt-template aliases over ordinary skills; the **Do/Verify Loop** follows the portable `/do` skill protocol.
- A **Host Continuation Backstop**, when available, is an outer guard for unattended runs; when absent or disabled, `/do` remains prompt-level with no continuous host enforcement.
- **Codex Plugin-native Distribution** is the live Codex distribution; the **Codex Legacy Installer Target** has been retired and removed from `dist/codex`.
- **OpenCode Plugin-native Distribution** replaces the retired OpenCode global installer; OpenCode loads manifest-dev **Skills** from the plugin's package-local paths rather than shared Agent Skills directories.
- `/do` owns the **Do/Verify Loop** in every host: it implements **Deliverables**, launches **Verifier Executions** for failed-or-unverified **Acceptance Criteria** and **Global Invariants**, repairs FAILs, and routes BLOCKED gates.
- **Babysit PR** and **Review PR** can run asynchronously on the same pull request: **Review PR** applies quality pressure through comments and thread advancement, while **Babysit PR** drives the author-side lifecycle toward green and mergeable.
- **Review PR** in manifest mode is the independent, optionally cross-model reviewer-side re-verification of a **Manifest**: it executes the same **Acceptance Criterion** and **Global Invariant** `verify.prompt`s that `/do` runs in-session, against the PR head, providing a cross-check that same-model in-session verification cannot. Generic code-quality review is preserved without an additive fleet because `/define` default-injects a `review-code` **Global Invariant** that runs as part of manifest verification.
- **Babysit PR** belongs to the `manifest-dev-tools` **Plugin** as PR tooling, while orchestrating core `manifest-dev` **Skills** for manifest synthesis and execution.
- **Babysit PR** uses a **Manifest** synthesized from an existing pull request, then `/do` executes the lifecycle **Acceptance Criterion** through a general-purpose verifier whose prompt activates the `check-pr` **Skill**.
- **PR Grounding** constrains **Babysit PR** autonomy: comments are interpreted against stronger intent sources instead of becoming the specification by recency.
- **CI One-Shot** narrows `/do` retry cadence for **Babysit PR**: wait-shaped blockers are reported as pending instead of sleeping a runner.

## Flagged ambiguities

_None yet. Grow this section as figure-out --with-docs sessions surface clashes or canonicalizations._
