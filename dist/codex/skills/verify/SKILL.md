---
name: verify
description: 'Spawns parallel verifiers for Global Invariants and Acceptance Criteria from a Manifest. Primary user-facing entry point is /verify --deferred (run user-triggered deferred-auto criteria); other invocations normally come from /do.'
user-invocable: true
---

# /verify - Manifest Verification Runner

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

**Input**: $ARGUMENTS

Format: `<manifest-file-path> <execution-log-path> [--mode efficient|balanced|thorough] [--scope D1,D2,...] [--final] [--deferred]`

Both paths required — return usage error if missing. Mode defaults to `thorough` if not provided. `--scope` and `--final` are mutually exclusive (final is full by definition); when both appear, treat as final. `--deferred` runs only `method: deferred-auto` criteria — see "Deferred-Auto Criteria" below.

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
| **Don't handle user feedback during a pass** | While /verify is running, any user message arriving mid-pass is semantically feedback to the caller (/do, or the user who invoked /verify --deferred directly) — /verify never amends, never re-prompts, never deviates from its current pass. It returns results; the caller interprets new user input per its own rules (e.g., /do's Mid-Execution Amendment). User-direct invocations of /verify --deferred run to completion the same way. |

## Verification Routing

Route `manual` criteria to /escalate. Route `subagent` criteria to the named agent specified in the criterion. Route `deferred-auto` criteria per the "Deferred-Auto Criteria" section below — they are **skipped during normal /verify flow** and only run when `--deferred` is passed; under `--deferred`, they are routed by the inner shape of their verify block (if `agent:` is set, route to that named subagent; if `command:` is set, route to criteria-checker as bash; otherwise default to criteria-checker). All other types (`bash`, `codebase`, `research`) spawn criteria-checker agents. If a criterion has no verification type, default to criteria-checker.

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

**Exception — manifest-driven `Repos:` prefix.** When the manifest declares `Repos:`, the cross-repo path prefix (`Available repos: name=/path, ...`) is prepended to every verifier's prompt per "Cross-repo path delivery to verifiers" below. This is the one prescribed exception to "Do not add your own framing" — the prefix is manifest-driven (derived from `Repos:`), not orchestrator opinion.

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
| All pass, **full mode**, manual criteria exist (no pending deferred-auto) | List manual criteria with how-to-verify, suggest /escalate |
| All pass, **full mode**, **deferred-auto criteria exist and not all verified green via prior `--deferred` pass** (no manual criteria) | /escalate with "Deferred-Auto Pending" — see "Deferred-Pending Escalation" below. Do NOT call /done. |
| All pass, **full mode**, **manual criteria AND pending deferred-auto criteria** | Combined /escalate (Manual Review + Deferred-Auto Pending) per "When BOTH" in Deferred-Pending Escalation below. Do NOT call /done. |
| All pass, **full mode**, no pending deferred-auto criteria, no manual criteria | Call /done |

**Selective that degenerated to full = full mode for outcome handling.** When `--scope` is absent and `--final` is absent, the pass covered every criterion already. Treat as a full pass: if manual criteria exist OR pending deferred-auto criteria exist → escalate (combine both per "Deferred-Pending Escalation §When BOTH"); otherwise → call /done. There is no "auto-trigger another full pass" for degenerated-to-full — that's redundant since the pass already covered everything.

**Manual criteria in selective mode.** When a selective pass encounters manual criteria within its in-scope deliverables and all automated checks pass, manual escalation is **deferred** to the auto-triggered full pass. Rationale: the full pass surfaces every manual criterion across every deliverable, so escalating partial manual criteria from a selective pass would fragment the user-facing escalation. Manual escalation fires exactly once per /verify chain — at the end of the full pass — never from a selective pass.

**Hard final gate.** /done is unreachable from selective-mode green alone. Per project directive ("Done means nothing more to do"), only a full-mode green pass — every AC across every deliverable + every Global Invariant — **with no pending deferred-auto criteria** calls /done. When deferred-auto criteria are pending (no prior `--deferred` pass covered them), /verify routes to /escalate ("Deferred-Auto Pending") instead — see Deferred-Pending Escalation. The auto-triggered full pass is unconditional: no mode override, no opt-out. If the auto-triggered full pass fails, /verify returns the failures to /do, which enters the standard fix-loop. Failure during a final pass behaves identically to failure during any other pass — fix, then a fresh selective pass scoped to the failing deliverable, then auto-trigger full again.

**`--final` is internal-only.** /verify uses `--final` to re-invoke itself after a selective green; /do does NOT pass `--final`. /do invokes /verify either with no scope flags (degenerates to full on first pass) or with `--scope D2,D3` (selective). The internal-only constraint preserves the gate: /do can never bypass the selective→full chain by manually requesting a final-only pass.

**Mode is preserved across the recursion.** When /verify auto-triggers itself with `--final`, it carries forward the active `--mode <X>` from the current invocation (efficient | balanced | thorough). The auto-triggered final pass runs at the same intensity (parallelism + model routing + skip rules) as the selective pass that triggered it — never forced to thorough. The "full suite" guarantee is unconditional; the *intensity per criterion* follows the active mode (preserves the orthogonality between selective/full and mode established earlier in this skill).

**On phase failure**: Show the failed phase, then for each failed criterion: ID, description, verification method, failure details (location, expected vs actual, fix hint). Note later phases not run and their pending criteria count.

## Deferred-Auto Criteria

`method: deferred-auto` marks a criterion as **automatically verifiable but user-triggered** — typically a cross-repo gate the user signals readiness for (e.g., "all PRs deployed"). The verifier itself runs automatically (bash command, subagent prompt, etc.); only the *triggering* is user-controlled.

**Normal flow skips them.** Selective and full passes (with or without `--scope`/`--final`) ignore `deferred-auto` criteria entirely during the pass — they never appear in the failure list of a normal pass. **However, their absence-of-coverage gates `/done` routing per "Deferred-Pending Escalation" below**: a normal-flow green pass with pending deferred-auto criteria routes to `/escalate` ("Deferred-Auto Pending"), not `/done`.

**`--deferred` runs them.** When `/verify ... --deferred` is invoked, /verify runs **only** `deferred-auto` criteria (everything else is skipped, including INV-Gs and ACs of other methods).

**Flag interactions:**
- `--deferred` + `--scope` is supported. `--scope` narrows the deferred-auto set to in-scope deliverables.
- `--deferred` does not interact with `--final` — never enters the final-gate machinery, never auto-triggers a follow-up pass, never calls /done.
- `--deferred` inherits `--mode` — same parallelism / model routing as the parent invocation.
- `--deferred` invoked without `--scope` covers all `deferred-auto` criteria across the manifest.
- A manifest with no `deferred-auto` criteria sees `--deferred` as a clean no-op ("no deferred-auto criteria in manifest").

**Deferred-Pending Escalation.** When a normal-flow `/verify` pass (selective or full) completes green but the manifest contains `deferred-auto` criteria that have not been verified green via a prior `/verify --deferred` run, `/verify` must NOT call `/done`. Instead, it routes to `/escalate` with type "Deferred-Auto Pending" and a message telling the user which deferred-auto criteria remain and instructing them to invoke `/verify --deferred` once prerequisites are in place. Once those criteria pass via `--deferred`, a subsequent normal `/verify` pass can call `/done`.

**Coverage determination.** A deferred-auto criterion is considered "covered" when there exists a preceding pass-log block with `deferred: true`, `result: pass`, and either (a) `scope:` is empty (full deferred coverage), or (b) `scope:` contains the deliverable that owns the criterion. /verify aggregates coverage across all prior `--deferred` blocks in the log: a criterion is pending iff no prior deferred-pass block satisfies (a) or (b) for it. INV-G* deferred-auto criteria are deliverable-scope-independent — they are covered only by a `deferred: true scope: []` block.

**When BOTH manual criteria and pending deferred-auto criteria exist** after a normal full-mode green pass, surface BOTH in a single combined escalation block: list the manual criteria + their how-to-verify, AND list the pending deferred-auto criteria + the `/verify --deferred` instruction. /done remains unreachable until both are resolved.

**After `/verify --deferred` completes green** (all deferred-auto criteria pass), close the user-as-coordinator loop with an explicit next-step instruction: emit a message like *"Deferred-auto criteria green. Re-invoke `/verify <manifest> <log>` (no flags) to reach /done."* Do NOT call /done from the `--deferred` pass itself — `--deferred` only verifies the deferred-auto subset; the final `/done` decision belongs to a normal-flow pass that confirms the full criterion universe is still green AND the deferred coverage now satisfies the gate.

**Cross-repo path delivery to verifiers.** When the manifest declares `Repos: [name: path, ...]`, **every `/verify` pass** (selective, full, and `--deferred`) prepends a verbatim string to each verifier's prompt before the criterion's own prompt:

```
Available repos: name1=/path/1, name2=/path/2, ...
```

This is the one mechanism — verifiers do not parse the manifest themselves. The injection fires on every pass, not just `--deferred`, so cross-repo verifiers can run during normal `/do→/verify` flow — that's what makes `/done` reachable for multi-repo manifests without per-repo /done independence. Single-repo manifests (no `Repos:` field) get no prefix injection. Full convention: `references/MULTI_REPO.md` (lives in `define/references/`) §e.

## /verify Pass Logging Contract

Every /verify invocation appends a structured block to the execution log so /do (and any future /verify pass) can read what already ran. Format:

````markdown
## /verify pass {N}

```yaml
mode: selective|full             # for --deferred passes: selective if --scope was set, else full
scope: [<deliverable-id>, ...]   # empty list when mode is full
result: pass|fail
failures: [<criterion-id>, ...]  # empty when pass; criterion IDs only, no narrative
auto_triggered_final: true|false # true when this pass was auto-triggered after selective green; always false for --deferred passes
deferred: true|false             # true when this pass ran via --deferred (only deferred-auto criteria checked); false for normal selective/full passes
```

[narrative — failed criterion details, fix hints, etc., per Outcome Handling]
````

When `deferred: true`, consumers should treat the pass as a partial verification (only `deferred-auto` criteria) — never as evidence that normal-flow ACs/INVs passed. The `result: pass` of a deferred pass means "the deferred-auto criteria are green," not "the whole manifest is green."

Pure markdown so humans can read; fenced YAML so /do and a future /verify can parse deterministically. Pass numbers are sequential within the execution log. /do uses the most recent block to track progress and decide which pass to invoke next.
