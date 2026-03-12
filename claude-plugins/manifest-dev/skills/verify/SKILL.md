---
name: verify
description: 'Manifest verification runner. Spawns parallel verifiers for Global Invariants and Acceptance Criteria. Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Manifest Verification Runner

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

**User request**: $ARGUMENTS

Format: `<manifest-file-path> <execution-log-path> [--scope=files]`

If paths missing: Return error "Usage: /verify <manifest-path> <log-path>"

## Principles

| Principle | Rule |
|-----------|------|
| **Orchestrate, don't verify** | Spawn agents to verify. You coordinate results, never run checks yourself. |
| **ALL criteria, no exceptions** | Every INV-G* and AC-*.* criterion MUST be verified. Skipping any criterion is a critical failure. |
| **Policy-aware fan-out** | Use the active policy to decide verification breadth. Baseline/default behavior can use broad parallel fan-out, while lower-cost policies may stage or defer reviewers. |
| **Globals are critical** | Global Invariant failures mean task failure. Highlight prominently. |
| **Actionable feedback** | Pass through file:line, expected vs actual, fix hints. |

## Policy Context

Read the execution log as the source of truth for active policy context.

If no policy context is available, use the baseline/default broad parallel behavior.

Policy may change orchestration, never completion semantics: every criterion still needs verification.

## Policy-Aware Orchestration

Baseline/default behavior: launch broad parallel verification coverage in a single message, consistent with the existing max-parallelism workflow.

Under `economy`, first pass always runs `criteria-checker` for automated `bash`, `codebase`, and `research` criteria.

Under `economy`, first pass also runs any named `subagent` verifier explicitly required by a criterion.

Under `economy`, defer this broad-reviewer set on the first pass unless a criterion explicitly requires one of them:
- `code-design-reviewer`
- `code-maintainability-reviewer`
- `code-simplicity-reviewer`
- `code-testability-reviewer`
- `docs-reviewer`
- `context-file-adherence-reviewer`
- `type-safety-reviewer`
- `code-coverage-reviewer`

This deferral never overrides criteria that explicitly require one of those named agents.

Under `economy`, if the same criterion fails twice, reintroduce the deferred broad-reviewer set.

Reintroduce deferred reviewers when multiple unrelated criteria fail.

Reintroduce deferred reviewers when a failure suggests design-level ambiguity.

For `subagent` failures under `economy`, if the failing criterion explicitly named that verifier, rerun that criterion's named-agent path first instead of immediately adding unrelated broad reviewers.

If that `subagent` criterion fails again, reintroduce the deferred reviewer set or emit stronger-model guidance when the failure suggests the named path is no longer sufficient.

For `research` failures under `economy`, treat them as potentially high-ambiguity rather than purely mechanical retries.

Retry a `research` criterion once with tighter scope or better source targeting; if it still cannot be resolved confidently, emit stronger-model guidance or escalate.

For `manual` criteria, do not invent retry or downgrade heuristics: keep surfacing them for `/escalate` exactly as manual handoff work.

Manual verification never becomes automated just because policy routing is active.

## Verification Methods

| Type | What | Handler |
|------|------|---------|
| `bash` | Shell commands (tests, lint, typecheck) | criteria-checker |
| `codebase` | Code pattern checks | criteria-checker |
| `subagent` | Specialized reviewer agents | Named agent (e.g., code-bugs-reviewer) |
| `research` | External info (API docs, dependencies) | criteria-checker |
| `manual` | Set aside for human verification | /escalate |

Note: criteria-checker handles any automated verification requiring commands, file analysis, reasoning, or web research.

## Criterion Types

| Type | Pattern | Failure Impact |
|------|---------|----------------|
| Global Invariant | INV-G{N} | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable incomplete |
| Process Guidance | PG-{N} | Not verified (guidance only) |

Note: PG-* items guide HOW to work. Followed during /do, not checked by /verify.

## Never Do

- Skip criteria (even "obvious" ones)
- Launch verifiers sequentially across multiple messages
- Verify criteria yourself instead of spawning agents

## Outcome Handling

| Condition | Action |
|-----------|--------|
| Any Global Invariant failed | Return all failures, globals highlighted |
| Any AC failed | Return failures grouped by deliverable |
| All automated pass, manual exists | Return manual criteria, hint to call /escalate |
| All pass | Call /done |

## Output Format

Report verification results grouped by Global Invariants first, then by Deliverable.

**On failure** - Show for each failed criterion:
- Criterion ID and description
- Verification method
- Failure details: location, expected vs actual, fix hint

**On success with manual** - List manual criteria with how-to-verify from manifest, suggest /escalate.

**On full success** - Call /done.

## Collaboration Mode

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, read `references/COLLABORATION_MODE.md` for full collaboration mode instructions. If no `TEAM_CONTEXT:` block is present, ignore this — all other sections apply as written.
