---
name: verify
description: 'Spawns parallel verifiers for Global Invariants and Acceptance Criteria from a Manifest.'
user-invocable: false
---

# /verify - Manifest Verification Runner

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

**Input**: $ARGUMENTS

Format: `<manifest-file-path> <execution-log-path> [--mode efficient|balanced|thorough]`

Both paths required — return usage error if missing. Mode defaults to `thorough` if not provided.

## Principles

| Principle | Rule |
|-----------|------|
| **Orchestrate, don't verify** | Spawn agents to verify. You aggregate results and coordinate, never run checks yourself. |
| **ALL criteria, no exceptions** | Every INV-G* and AC-*.* criterion MUST be verified. Skipping any criterion is a critical failure. |
| **Parallelism per mode** | The active execution mode defines how many verifiers to launch concurrently within each phase. Phases always run sequentially — see Phased Execution below. |
| **Actionable feedback** | Pass through file:line, expected vs actual, fix hints. |

## Verification Routing

Route `manual` criteria to /escalate. Route `subagent` criteria to the named agent specified in the criterion. All other types (`bash`, `codebase`, `research`) spawn criteria-checker agents. If a criterion has no verification type, default to criteria-checker.

## Agent Prompt Composition

When spawning verifier agents, pass the criterion's manifest data. Do not add your own framing.

**Include**: Criterion ID, description, verification method, and the verify block's `command:` or `prompt:` field verbatim. Add file scope when the criterion targets specific files.

**Optional context file paths**: When a manifest file, discovery log, or execution log exists, append their file paths as optional reference material. Present them neutrally — agents can read them if useful for understanding scope or context, but are not required to.

Format: `Optional context — manifest: <path>, discovery log: <path>, execution log: <path>`

Only include paths that exist. This is informational, not directive — agents decide whether the context is relevant to their review.

**Never add**:
- Severity thresholds ("only report medium+ issues", "focus on critical findings")
- Implementation context ("the code was refactored to...", "this was implemented by...")
- Opinions or expectations ("this should pass", "this is likely fine")
- Leading language ("verify this important constraint", "carefully check this critical rule")
- Task summaries ("check that the auth module correctly handles...")
- Suggested outcomes ("confirm that X works correctly")
- Interpretations of manifest intent ("the goal is to...", "this change is about...")

The verify block's `prompt:` field is manifest-authored — pass it verbatim. These rules target language you add beyond what the manifest specifies. The optional context file paths are raw references, not framing — they provide access to source material without steering the agent's analysis.

## Criterion Types

| Type | Pattern | Failure Impact |
|------|---------|----------------|
| Global Invariant | INV-G{N} | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable incomplete |
| Process Guidance | PG-{N} | Not verified (guidance only) |

Note: PG-* items guide HOW to work. Followed during /do, not checked by /verify.

## Agent Failures

If a verification agent crashes, times out, or returns unusable output, treat the criterion as FAIL with a note that verification itself failed (not the criterion). Include the error in the failure details so /do can distinguish "criterion didn't pass" from "couldn't check."

## Phased Execution

Criteria have an optional `phase:` field (numeric, default 1). Phases run in ascending order — Phase N+1 only launches when all Phase N criteria pass.

**Execution rules:**
- Group all criteria (INV-G* and AC-*) by their `phase:` value.
- Run the lowest phase first. Within that phase, apply parallelism rules (mode-dependent).
- If all criteria in the current phase pass, proceed to the next phase.
- If any criterion in the current phase fails, return failures immediately with phase context. Do not run later phases — let /do enter the fix loop faster.
- Non-contiguous phases (e.g., 1 and 3, no 2) are valid — skip to the next existing phase.

**Phase failure reporting:** When a phase fails, include the phase number in the failure report and note which later phases were not run (e.g., "Phase 1: 2 failures. Phase 2: not run (3 criteria pending).").

**Backward compatibility:** Manifests without any `phase:` fields have all criteria in phase 1 — identical to current behavior (all criteria run together per mode parallelism).

## Mode-Aware Verification

Load the mode file at `../do/references/execution-modes/{mode}.md` (default: `thorough`). Follow its rules for verification parallelism, model routing, and quality gate inclusion. The mode file defines which verifiers to skip, what model to use for criteria-checker agents, and how many concurrent verifiers to launch per phase. If mode file cannot be loaded, return an error to the caller immediately — do not attempt any verification.

## Gotchas

- **Mode parallelism is bidirectional** — launching all at once when mode says sequential is wrong, but so is going sequential when mode says parallel. Follow the mode file exactly.
- **Agent crash ≠ criterion pass** — if a verifier fails to run, the criterion fails too. Never treat "couldn't check" as "passed."

## Outcome Handling

Group results by phase, then Global Invariants first, then by Deliverable.

| Condition | Action |
|-----------|--------|
| Any Global Invariant failed | Return all failures, globals highlighted |
| Any AC failed | Return failures grouped by deliverable |
| All automated pass, manual exists | List manual criteria with how-to-verify, suggest /escalate |
| All pass | Call /done |

**On phase failure**: Show the failed phase, then for each failed criterion: ID, description, verification method, failure details (location, expected vs actual, fix hint). Note later phases not run and their pending criteria count.
