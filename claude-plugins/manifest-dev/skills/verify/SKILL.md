---
name: verify
description: 'Manifest verification runner. Spawns parallel verifiers for Global Invariants and Acceptance Criteria. Optional --mode efficient|balanced|thorough controls parallelism and model routing (default: thorough). Called by /do, not directly by users.'
user-invocable: false
---

# /verify - Manifest Verification Runner

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

**User request**: $ARGUMENTS

Format: `<manifest-file-path> <execution-log-path> [--mode efficient|balanced|thorough]`

If paths missing: Return error "Usage: /verify <manifest-path> <log-path> [--mode efficient|balanced|thorough]"

Mode defaults to `thorough` if not provided.

## Principles

| Principle | Rule |
|-----------|------|
| **Orchestrate, don't verify** | Spawn agents to verify. You coordinate results, never run checks yourself. |
| **ALL criteria, no exceptions** | Every INV-G* and AC-*.* criterion MUST be verified. Skipping any criterion is a critical failure. |
| **Maximize parallelism** | Launch all verifiers in a SINGLE message with multiple Task tool calls. Never launch one at a time. **Overridden by mode** — see Mode-Aware Verification below. |
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

## Agent Prompt Composition

When spawning verifier agents, pass only the criterion's manifest data. Do not add your own framing.

**Include**: Criterion ID, description, verification method, and the verify block's `command:` or `prompt:` field verbatim. Add file scope when the criterion targets specific files.

**Never add**:
- Severity thresholds ("only report medium+ issues", "focus on critical findings")
- Implementation context ("the code was refactored to...", "this was implemented by...")
- Opinions or expectations ("this should pass", "this is likely fine")
- Leading language ("verify this important constraint", "carefully check this critical rule")
- Task summaries ("check that the auth module correctly handles...")
- Suggested outcomes ("confirm that X works correctly")

The verify block's `prompt:` field is manifest-authored — pass it verbatim. These rules target language you add beyond what the manifest specifies.

## Criterion Types

| Type | Pattern | Failure Impact |
|------|---------|----------------|
| Global Invariant | INV-G{N} | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable incomplete |
| Process Guidance | PG-{N} | Not verified (guidance only) |

Note: PG-* items guide HOW to work. Followed during /do, not checked by /verify.

## Agent Failures

If a verification agent crashes, times out, or returns unusable output, treat the criterion as FAIL with a note that verification itself failed (not the criterion). Include the error in the failure details so /do can distinguish "criterion didn't pass" from "couldn't check."

## Mode-Aware Verification

When `--mode` is not `thorough`, these rules override default behavior:

| Mode | Parallelism | Criteria-checker model | Quality gate reviewers |
|------|-------------|----------------------|----------------------|
| efficient | Sequential (one at a time) | haiku | SKIPPED for deliverable-level ACs |
| balanced | Batched (max 4 concurrent) | inherit | inherit |
| thorough | All at once (default) | inherit | inherit |

**Efficient mode skipping**: Skip reviewer subagent verification (code-bugs-reviewer, type-safety-reviewer, etc.) for deliverable-level ACs. Still run: all bash/codebase checks, all INV-G* verification (regardless of method), and any AC with an explicit `model:` in its verify block.

## Never Do

- Skip criteria (even "obvious" ones) — unless mode explicitly allows (efficient mode skips deliverable-level reviewer subagents)
- Launch verifiers sequentially across multiple messages — unless mode requires it (efficient = sequential, balanced = batched)
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
