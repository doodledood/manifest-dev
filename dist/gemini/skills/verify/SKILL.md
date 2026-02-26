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
| **Maximize parallelism** | Launch all verifiers in a SINGLE message with multiple Task tool calls. Never launch one at a time. |
| **Globals are critical** | Global Invariant failures mean task failure. Highlight prominently. |
| **Actionable feedback** | Pass through file:line, expected vs actual, fix hints. |

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
