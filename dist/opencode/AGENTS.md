# AGENTS.md — manifest-dev Workflow Context

## Overview

manifest-dev provides verification-first manifest workflows for AI coding agents. The core flow is:

```
/define → manifest → /do → /verify → /done
```

- **/define** — Interactive manifest builder. Probes for requirements, quality gates, edge cases. Outputs a manifest with deliverables, acceptance criteria, and global invariants.
- **/do** — Manifest executor. Implements deliverables, follows process guidance, adapts approach when reality diverges.
- **/verify** — Spawns parallel verification agents against all criteria. Runs in phases (fast checks first).
- **/done** — Completion marker. Outputs hierarchical execution summary.
- **/escalate** — Structured escalation for blockers, scope changes, and pauses.

Supporting workflows:
- **/auto** — End-to-end autonomous: /define (autonomous interview) → /do in one command.
- **/figure-out** — Collaborative deep understanding. Investigation-first, truth-convergent. End with /stop-thinking-disciplines.
- **/drive** — Cron-driven manifest-to-green loop. Bootstraps branch/PR, schedules /drive-tick until terminal state (all verify pass for none mode, merge-ready for github mode).

Internal skills:
- **thinking-disciplines** — Core thinking disciplines invoked by /figure-out and /define. Not user-invocable.
- **/stop-thinking-disciplines** — Deactivate thinking disciplines.

## Agents

14 specialized agents, all read-only reviewers:

| Agent | Purpose |
|-------|---------|
| change-intent-reviewer | Adversarial intent-behavior divergence analysis |
| code-bugs-reviewer | Mechanical defect detection (race conditions, leaks, edge cases) |
| test-quality-reviewer | Coverage gap analysis plus tautological-test detection (mirror-impl, mock-SUT, trivial-asserts, snapshot-without-intent) |
| prose-value-reviewer | Comments and repo doc files: narrating-the-obvious, generic puffery, AI rhetorical patterns, sycophantic fragments — comments must be load-bearing-WHY |
| code-design-reviewer | Design fitness (reinvented wheels, wrong responsibility, under-engineering) |
| code-maintainability-reviewer | Code organization (DRY, coupling, cohesion, consistency) |
| code-simplicity-reviewer | Unnecessary complexity and over-engineering |
| code-testability-reviewer | Test friction analysis (mock count, logic in IO) |
| context-file-adherence-reviewer | Context file compliance (AGENTS.md/CLAUDE.md/GEMINI.md rules) |
| contracts-reviewer | API and interface contract correctness with evidence |
| criteria-checker | Single-criterion verification (bash, codebase, research) |
| docs-reviewer | Documentation accuracy against code changes |
| manifest-verifier | Manifest gap detection and continuation questions |
| type-safety-reviewer | Type system improvements across typed languages |

## Execution Modes

/do supports three modes controlling verification intensity:

| Mode | Model Routing | Parallelism | Fix Loops |
|------|--------------|-------------|-----------|
| thorough (default) | inherit | All at once | Unlimited |
| balanced | inherit | Batches of 4 | Max 2/phase |
| efficient | inherit | Sequential | Max 1/phase |

## Plugin (Hooks)

The manifest-dev plugin (`.opencode/plugins/manifest-dev.ts`) provides:
- Workflow state tracking for /do and thinking disciplines
- Post-compaction context recovery
- Pre-verify context refresh
- Amendment check guidance during /do
- Thinking disciplines reinforcement

**Known limitation**: OpenCode cannot block session stopping (session.idle is fire-and-forget). The /do workflow contract is enforced via persistent system guidance, not a hard block.
