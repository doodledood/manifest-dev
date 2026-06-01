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
A domain hint file loaded by `/define` to inform interview probing and pre-encode Quality Gates and Defaults.

**Plugin**:
A Claude Code extension unit that may contain skills, agents, and optional hooks.

**Skill**:
A markdown-defined extension (`SKILL.md` + companion files) that adds a capability to Claude Code.

**Agent**:
An isolated subagent process with its own tools and context.
_Avoid_: Subprocess, worker.

**Hook**:
A handler that responds to a Claude Code lifecycle event (e.g., Stop, SessionStart).

**Babysit PR**:
An author-side workflow that tends an existing pull request through CI, review threads, description sync, and mergeability without pressing merge.
_Avoid_: Tend PR.

## Relationships

- A **Manifest** contains one or more **Deliverables**.
- A **Deliverable** has one or more **Acceptance Criteria**.
- A **Manifest** has zero or more **Global Invariants**, applied across all Deliverables.
- A **Task File** informs `/define`'s probing and encoding; it does not directly appear in the produced Manifest as a structural unit.
- A **Plugin** contains zero or more **Skills**, **Agents**, and optional **Hooks**.
- A **Skill** may invoke other **Skills** and spawn **Agents**.
- **Babysit PR** uses a **Manifest** synthesized from an existing pull request, then `/do` executes the lifecycle **Acceptance Criterion** through the `github-pr-lifecycle` **Agent**.

## Flagged ambiguities

_None yet. Grow this section as figure-out --with-docs sessions surface clashes or canonicalizations._
