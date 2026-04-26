---
name: verify
description: 'Spawns parallel verifiers for Global Invariants and Acceptance Criteria from a Manifest.'
user-invocable: false
---

# /verify - Manifest Verification Runner

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

**Input**: $ARGUMENTS

Format: `<manifest-file-path> <execution-log-path> [--mode efficient|balanced|thorough] [--scope D1,D2,...] [--final]`

Both paths required — return usage error if missing. Mode defaults to `thorough` if not provided. `--scope` and `--final` are mutually exclusive (final is full by definition); when both appear, treat as final.

## Selective vs Full Verification

/verify runs in one of two modes — selective or full — driven by the caller (/do):

- **Selective pass.** Runs only the ACs of the in-scope deliverables (passed via `--scope D2,D3`, or computed by /do as the deliverable owning a failed criterion in fix-loop) **plus all Global Invariants** (INV-G* always run). Used during the fix-loop and after scoped /do invocations to keep token cost bounded.
- **Full pass.** Runs every AC across every deliverable plus all globals. Triggered by `--final` from /do, or auto-triggered by /verify itself after a selective pass goes green (see Outcome Handling).

**When `--scope` is absent and `--final` is absent**, selective mode degenerates to full — there's no narrowing to apply, so behavior matches today's "verify everything." This is also the first /verify pass on a fresh /do (no failure context yet, no scope flag).

**Why this exists.** Re-running every AC on every fix-loop iteration costs N × loops verifier invocations. Most fixes touch one deliverable; re-verifying the rest is waste. The mandatory full final gate (Outcome Handling) catches anything cross-deliverable that selective mode missed — that's the safety net.

## Principles

| Principle | Rule |
|-----------|------|
| **Context before spawning** | Read manifest and execution log before spawning verifiers — criterion IDs and prompts drive agent composition. |
| **Orchestrate, don't verify** | Spawn agents to verify. You aggregate results and coordinate, never run checks yourself. |
| **All in-scope criteria, no exceptions** | Every criterion in the current pass's scope (selective: in-scope deliverables' ACs + all INV-G*; full: every AC + every INV-G*) MUST be verified. Skipping any in-scope criterion is a critical failure. |
| **Parallelism per mode** | The active execution mode defines how many verifiers to launch concurrently within each phase. Phases always run sequentially — see Phased Execution below. |
| **Actionable feedback** | Pass through file:line, expected vs actual, fix hints. |
| **Don't handle user feedback** | /verify is non-user-invocable. Any user message arriving while /verify is running is semantically feedback to /do (the caller). /verify never amends, never re-prompts, never deviates from its current pass — it returns results; /do interprets new user input per its own default-to-amend rule (`do/SKILL.md` Mid-Execution Amendment). |

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

**Phase and scope are orthogonal.** `phase:` gates execution order (ascending); selective vs full filters the universe of criteria. Within a selective pass, the filter applies first (which deliverables' ACs + all globals), then phases gate the filtered set. Conflating them is wrong — phase ordering is unchanged by selection.

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
| All in-scope pass, **selective mode that actually narrowed** (`--scope` was set) | **Auto-trigger a full pass** (re-invoke /verify internally with `--final`). Do NOT call /done. Manual criteria in scope are NOT escalated yet — they're deferred to the auto-triggered full pass per the rule below. |
| All pass, **full mode**, manual criteria exist | List manual criteria with how-to-verify, suggest /escalate |
| All pass, **full mode** | Call /done |

**Selective that degenerated to full = full mode for outcome handling.** When `--scope` is absent and `--final` is absent, the pass covered every criterion already. Treat as a full pass: if manual criteria exist → escalate (do not skip the manual row); otherwise → call /done. There is no "auto-trigger another full pass" for degenerated-to-full — that's redundant since the pass already covered everything.

**Manual criteria in selective mode.** When a selective pass encounters manual criteria within its in-scope deliverables and all automated checks pass, manual escalation is **deferred** to the auto-triggered full pass. Rationale: the full pass surfaces every manual criterion across every deliverable, so escalating partial manual criteria from a selective pass would fragment the user-facing escalation. Manual escalation fires exactly once per /verify chain — at the end of the full pass — never from a selective pass.

**Hard final gate.** /done is unreachable from selective-mode green alone. Per project directive ("Done means nothing more to do"), only a full-mode green pass — every AC across every deliverable + every Global Invariant — calls /done. The auto-triggered full pass is unconditional: no mode override, no opt-out. If the auto-triggered full pass fails, /verify returns the failures to /do, which enters the standard fix-loop. Failure during a final pass behaves identically to failure during any other pass — fix, then a fresh selective pass scoped to the failing deliverable, then auto-trigger full again.

**`--final` is internal-only.** /verify uses `--final` to re-invoke itself after a selective green; /do does NOT pass `--final`. /do invokes /verify either with no scope flags (degenerates to full on first pass) or with `--scope D2,D3` (selective). The internal-only constraint preserves the gate: /do can never bypass the selective→full chain by manually requesting a final-only pass.

**Mode is preserved across the recursion.** When /verify auto-triggers itself with `--final`, it carries forward the active `--mode <X>` from the current invocation (efficient | balanced | thorough). The auto-triggered final pass runs at the same intensity (parallelism + model routing + skip rules) as the selective pass that triggered it — never forced to thorough. The "full suite" guarantee is unconditional; the *intensity per criterion* follows the active mode (preserves the orthogonality between selective/full and mode established earlier in this skill).

**On phase failure**: Show the failed phase, then for each failed criterion: ID, description, verification method, failure details (location, expected vs actual, fix hint). Note later phases not run and their pending criteria count.

## /verify Pass Logging Contract

Every /verify invocation appends a structured block to the execution log so /do (and any future /verify pass) can read what already ran. Format:

````markdown
## /verify pass {N}

```yaml
mode: selective|full
scope: [<deliverable-id>, ...]   # empty list when mode is full
result: pass|fail
failures: [<criterion-id>, ...]  # empty when pass; criterion IDs only, no narrative
auto_triggered_final: true|false # true when this pass was auto-triggered after selective green
```

[narrative — failed criterion details, fix hints, etc., per Outcome Handling]
````

Pure markdown so humans can read; fenced YAML so /do and a future /verify can parse deterministically. Pass numbers are sequential within the execution log. /do uses the most recent block to track progress and decide which pass to invoke next.
