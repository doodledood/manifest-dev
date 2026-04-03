# manifest-dev Agents

## Workflow

This project uses a **define -> do -> verify -> done** workflow, powered by skills:

1. **/define** -- Interview-driven manifest creation. Produces a structured specification with deliverables, acceptance criteria, global invariants, and verification methods.
2. **/do** -- Execute against the manifest. Implements deliverables, runs fix-verify loops, escalates blockers.
3. **/verify** -- Parallel verification of all criteria. Spawns agents (listed below) for quality gate checks.
4. **/done** -- Completion checkpoint. Confirms all criteria pass and produces a summary.

Skills handle the workflow orchestration. Agents listed below are used for verification and analysis.

## Code Review Agents

- **change-intent-reviewer**: Adversarially analyzes whether code changes achieve their stated intent. Reconstructs intent from diff context, then attacks the logic for behavioral divergences.
- **code-bugs-reviewer**: Audits for mechanical defects -- race conditions, data loss, edge cases, resource leaks, dangerous defaults, error handling gaps.
- **code-coverage-reviewer**: Derives test scenarios from code logic and reports coverage gaps with concrete inputs and expected outputs.
- **code-design-reviewer**: Design fitness -- reinvented wheels, misplaced responsibilities, under-engineering, short-sighted interfaces, concept misuse, incoherent changes.
- **code-maintainability-reviewer**: DRY violations, structural complexity, dead code, consistency, coupling, cohesion, boundary leakage, migration debt.
- **code-simplicity-reviewer**: Unnecessary complexity, over-engineering, premature optimization, cognitive burden, clarity over cleverness.
- **code-testability-reviewer**: Identifies code requiring excessive mocking, business logic buried in IO, non-deterministic inputs.
- **context-file-adherence-reviewer**: Verifies code changes comply with context file instructions (AGENTS.md) and project standards.
- **contracts-reviewer**: Evidence-based API and interface contract verification -- both outbound (correct API usage) and inbound (consumer impact).
- **docs-reviewer**: Audits documentation and code comments for accuracy against recent code changes.
- **type-safety-reviewer**: Type holes, invalid states representable, narrowing gaps, nullability problems across typed languages.

## Verification Agents

- **criteria-checker**: Read-only verification agent. Validates a single criterion using commands, codebase analysis, file inspection, reasoning, or web research. Spawned in parallel by /verify.
- **manifest-verifier**: Reviews /define manifests for gaps. Outputs actionable questions to continue the interview.

## Analysis Agents

- **define-session-analyzer**: Analyzes /define session transcripts to extract user preference patterns. Spawned by learn-define-patterns skill.

## How to Use

These agents are configured as TOML files in `agents/`. On Codex CLI, the multi-agent system uses these configs to approximate scoped subagent behavior. Skills invoke agents by name during verification workflows.

To enable multi-agent support, ensure your `.codex/config.toml` includes:

```toml
[features]
multi_agent = true
```

## Known Limitations

- Agents are TOML config stubs -- they approximate Claude Code's scoped agent behavior but use Codex's multi-agent paradigm.
- Without hooks, the define -> do -> verify -> done chain is advisory (nothing enforces completion order).
- Skills may not chain as reliably as on Claude Code.
