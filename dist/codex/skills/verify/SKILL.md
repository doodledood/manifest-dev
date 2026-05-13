---
name: verify
description: 'Spawns parallel verifiers for Global Invariants and Acceptance Criteria from a Manifest. Normally invoked by /do; users invoke directly via /verify --deferred to run user-triggered deferred-auto criteria.'
user-invocable: true
---

# /verify - Manifest Verification Runner

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

**Input**: $ARGUMENTS

Format: `<manifest-file-path> [--mode efficient|balanced|thorough] [--scope D1,D2,...] [--deferred]`

If the manifest path is missing, halt: `Usage: /verify <manifest-file-path> [--mode efficient|balanced|thorough] [--scope D1,D2,...] [--deferred]`. If the manifest path doesn't exist, halt: `Cannot verify: manifest '<path>' not found.`

`--deferred` runs only `method: deferred-auto` criteria — see "Deferred-Auto Criteria" below.

`--final` is internal-only — see "Hard Final Gate" below. /do never passes it; users never pass it.

## Mode Resolution

Resolve mode from (highest precedence first): `--mode` argument → manifest `Mode` field → `thorough`.

Invalid `--mode` value → halt: `Invalid mode '<value>'. Valid modes: efficient | balanced | thorough`.

The resolved mode controls verifier parallelism, model routing, and reviewer-skip rules per `../do/references/execution-modes/{mode}.md`. Load that file at entry; if it cannot be loaded, halt with the load error — do not attempt verification.

## Selective vs Full Verification

/verify runs in one of two modes — selective or full — driven by the caller (/do, or a user-direct invocation):

- **Selective pass.** Runs only the ACs of the in-scope deliverables (passed via `--scope D2,D3` — /do computes the failing-deliverable scope and passes it during fix-loop) **plus all Global Invariants** (INV-G* are in scope on every pass, subject to Phased Execution gating). Used during the fix-loop and after scoped /do invocations to keep token cost bounded.
- **Full pass.** Runs every AC across every deliverable plus all globals (same phase gating). Auto-triggered by /verify itself (re-invoking with `--final`) after a true-selective pass goes green — see Hard Final Gate.

**Terminology.** *True-selective* = a selective pass where `--scope` was set (the filter actually narrowed). *Selective-degenerated-to-full* = a selective pass where `--scope` was absent (no narrowing to apply, so the pass covers everything). Outcome handling distinguishes the two — see Outcome Handling.

**When `--scope` is absent and `--final` is absent**, selective mode degenerates to full — behavior matches "verify everything." This applies to the first /verify pass on a fresh /do (no failure context yet, no scope flag) and to user-direct invocations like `/verify <manifest>` with no flags.

**Why this exists.** Re-running every AC on every fix-loop iteration costs N × loops verifier invocations. Most fixes touch one deliverable; re-verifying the rest is waste. The mandatory full final gate (Hard Final Gate) catches anything cross-deliverable that selective mode missed — that's the safety net.

## Principles

Operating principles for every pass:

| Principle | Rule |
|-----------|------|
| **Context before spawning** | Read manifest before spawning verifiers — criterion IDs and prompts drive agent composition. |
| **Orchestrate, don't verify** | Spawn agents to verify. You aggregate results and coordinate, never run checks yourself. |
| **All in-scope criteria, mode-authorized skips only** | Every criterion in the current pass's scope (selective: in-scope deliverables' ACs + all INV-G*; full: every AC + every INV-G*) MUST be verified, except where the active execution mode file explicitly authorizes a skip (e.g., quality-gate reviewers in efficient mode). Skipping any criterion not authorized by the mode file is a critical failure. |
| **Parallelism per mode** | The active execution mode defines how many verifiers to launch concurrently within each phase. Phases always run sequentially — see Phased Execution below. |
| **Actionable feedback** | Pass through file:line, expected vs actual, fix hints. |
| **Don't handle user feedback during a pass** | **While /verify is running**, any user message arriving mid-pass is semantically feedback to the caller (/do, or the user who invoked /verify --deferred directly) — /verify never amends, never re-prompts, never deviates from its current pass. It returns results; the caller interprets new user input per its own rules (e.g., /do's Mid-Execution Amendment). User-direct invocations of /verify --deferred run to completion the same way. |

## Verification Routing

Route by criterion `method:`:

| Method | Verifier |
|--------|----------|
| `bash`, `codebase`, `research` | criteria-checker (mode-routed model) |
| `subagent` | the named agent in the criterion's `agent:` field |
| `manual` | /escalate (no automated check exists) |
| `deferred-auto` | skipped on normal passes (see Deferred-Auto Criteria); under `--deferred`, routed by the inner nested `method:` field |
| (none / unrecognized) | criteria-checker |

**Deferred-auto requires an explicit inner method.** A `method: deferred-auto` verify block MUST declare a sibling `inner_method:` field (`subagent` | `bash` | `codebase` | `research`). Under `--deferred`, /verify routes the criterion identically to a non-deferred criterion of that `inner_method`. If `inner_method` is missing, halt: `Deferred-auto criterion <ID> missing inner_method.` Field shape (canonical example):

```yaml
verify:
  method: deferred-auto
  inner_method: subagent
  agent: general-purpose
  prompt: "..."
```

## Agent Prompt Composition

Pass each verifier exactly three sections, **in this order, each on its own line**:

1. **Cross-repo prefix** (only when the manifest declares `Repos:`) — the verbatim string defined in `define/references/MULTI_REPO.md` §e (single source of truth). Single-repo manifests skip this line.
2. **Optional context line** — `Optional context — manifest: <path>`. Informational, not directive — agents decide whether the manifest is relevant.
3. **Criterion content** — the criterion's manifest data: ID, description, verification method, and the verify block's `command:` or `prompt:` field verbatim. If `prompt:` is absent (e.g., bash criteria), pass the criterion's description as the agent prompt instead. Add file scope when the criterion targets specific files.

The cross-repo prefix is the one prescribed exception to "do not add framing" — it is manifest-driven (derived from `Repos:`), not orchestrator opinion.

**Never add to the criterion content:**

- Severity thresholds ("only report medium+ issues", "focus on critical findings")
- Implementation context ("the code was refactored to...", "this was implemented by...")
- Opinions or expectations ("this should pass", "this is likely fine")
- Leading language ("verify this important constraint", "carefully check this critical rule")
- Task summaries ("check that the auth module correctly handles...")
- Suggested outcomes ("confirm that X works correctly")
- Interpretations of manifest intent ("the goal is to...", "this change is about...")

The verify block's `prompt:` field is manifest-authored — pass it verbatim. These rules target language you add beyond what the manifest specifies. The optional context line is a raw reference, not framing — it provides access to source material without steering the agent's analysis.

## Criterion Types

| Type | Pattern | Failure Impact |
|------|---------|----------------|
| Global Invariant | INV-G{N} | Task fails |
| Acceptance Criteria | AC-{D}.{N} | Deliverable incomplete |
| Process Guidance | PG-{N} | Not verified (guidance only) |

`{D}` = deliverable number; `{N}` = ordinal within scope (1-based). PG-* items guide HOW to work — followed during /do, not checked by /verify.

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

**Phase and scope are orthogonal.** `phase:` gates execution order (ascending); selective vs full filters the universe of criteria. Within a selective pass, the filter applies first (which deliverables' ACs + all globals), then phases gate the filtered set.

**Backward compatibility:** Manifests without any `phase:` fields have all criteria in phase 1 — identical to the prior behavior (all criteria run together per mode parallelism).

## Gotchas

- **Mode parallelism is bidirectional** — launching all at once when mode says sequential is wrong, but so is going sequential when mode says parallel. Follow the mode file exactly.
- **Agent crash ≠ criterion pass** — if a verifier fails to run, the criterion fails too. Never treat "couldn't check" as "passed."

## Outcome Handling

Group results by phase, then Global Invariants first, then by Deliverable.

| Condition | Action |
|-----------|--------|
| **Any Global Invariant failed** | **Return all failures, globals highlighted** |
| **Any AC failed** (no global failures) | **Return failures grouped by deliverable** |
| **All in-scope pass; true-selective pass (`--scope` was set)** | **Auto-trigger a full pass** (re-invoke /verify internally with `--final`). Do NOT call /done. Manual escalation and Deferred-Auto Pending escalation are both deferred to the auto-triggered full pass. |
| **All pass; full or selective-degenerated-to-full; manual criteria exist; no pending deferred-auto** | **/escalate "Manual Criteria Review"** with each manual criterion + its how-to-verify. Do NOT call /done. |
| **All pass; full or selective-degenerated-to-full; pending deferred-auto exist; no manual criteria** | **/escalate "Deferred-Auto Pending"** — see Deferred-Auto Pending Escalation. Do NOT call /done. |
| **All pass; full or selective-degenerated-to-full; manual AND pending deferred-auto** | **Combined /escalate** (Manual Criteria Review + Deferred-Auto Pending). Do NOT call /done. |
| **All pass; full or selective-degenerated-to-full; no manual; no pending deferred-auto** | **Call /done** |

**Selective-degenerated-to-full** = a selective pass where `--scope` was absent. The pass already covered every criterion, so it's treated as full for outcome handling. There is no "auto-trigger another full pass" — that would be redundant.

**Manual criteria in true selective mode** (where `--scope` was set). Manual escalation is **deferred** to the auto-triggered full pass so that escalation fires exactly once per /verify chain — at the end of the full pass. Surfacing partial manual criteria from a true selective pass would fragment the user-facing escalation.

**On phase failure**: Show the failed phase, then for each failed criterion: ID, description, verification method, failure details (location, expected vs actual, fix hint). Note later phases not run and their pending criteria count.

### Hard Final Gate

- **/done is unreachable from selective-mode green alone.** Per project directive ("Done means nothing more to do"), only a full-mode green pass — every AC across every deliverable + every Global Invariant — **with no pending manual criteria and no pending deferred-auto criteria** calls /done.
- **Pending manual blocks /done.** When manual criteria exist (and the pass is the kind that can call /done), /verify routes to /escalate ("Manual Criteria Review") instead — the user verifies manually, then re-invokes /verify.
- **Pending deferred-auto blocks /done.** When deferred-auto criteria are pending, /verify routes to /escalate ("Deferred-Auto Pending") instead — see Deferred-Auto Pending Escalation.
- **Both pending → combined /escalate.** Surface both types in one block (see Deferred-Auto Pending Escalation § "When BOTH").
- **Once a true-selective pass goes green, the auto-trigger fires unconditionally** — no mode override, no opt-out.
- **Auto-final failure → standard fix-loop.** /verify returns failures to /do, which fixes; /verify then runs a fresh selective pass scoped to the failing deliverable, then auto-triggers full again.
- **`--final` is internal-only.** /verify uses `--final` to re-invoke itself after a true-selective green; /do never passes it. /do invokes /verify either with no scope flags (degenerates to full on first pass) or with `--scope D2,D3` (selective). This preserves the gate: /do can never bypass the selective→full chain.
- **Mode is preserved across the auto-final re-invocation.** /verify carries forward the active `--mode <X>` (efficient | balanced | thorough). The auto-final pass runs at the same intensity as the selective pass that triggered it — never forced to thorough. The "full suite" guarantee is unconditional; the *intensity per criterion* follows the active mode.

## Deferred-Auto Criteria

`method: deferred-auto` marks a criterion as **automatically verifiable but user-triggered** — typically a cross-repo gate the user signals readiness for (e.g., "all PRs deployed"). The verifier itself runs automatically (bash command, subagent prompt, etc.); only the *triggering* is user-controlled. Deferred-auto verify blocks MUST declare an explicit sibling `inner_method:` (subagent | bash | codebase | research) — see Verification Routing for the field shape.

**Normal flow skips them.** Selective and full passes (with or without `--scope`/`--final`) ignore `deferred-auto` criteria entirely during the pass — they never appear in the failure list of a normal pass. **However, uncovered deferred-auto criteria block /done — a normal-flow green pass with pending deferred-auto routes to /escalate ("Deferred-Auto Pending"), not /done.** See Deferred-Auto Pending Escalation below.

**`--deferred` runs them.** When `/verify ... --deferred` is invoked, /verify runs **only** `deferred-auto` criteria (everything else is skipped, including INV-Gs and ACs of other methods).

**Flag interactions:**

- `--deferred` + `--scope` is supported. `--scope` narrows the deferred-auto set to in-scope deliverables.
- `--deferred` does not interact with `--final` — never enters the final-gate machinery, never auto-triggers a follow-up pass, never calls /done.
- `--deferred` inherits `--mode` — same parallelism / model routing as the parent invocation.
- `--deferred` invoked without `--scope` covers all `deferred-auto` criteria across the manifest.
- A manifest with no `deferred-auto` criteria sees `--deferred` as a clean no-op ("no deferred-auto criteria in manifest").

**Coverage determination.** A deferred-auto criterion is "covered" when there exists a preceding `/verify` return block in the current session where `deferred: true`, `result: pass`, and either (a) `scope:` is empty (full deferred coverage), or (b) `scope:` contains the deliverable that owns the criterion. /verify reads prior return blocks from conversation context: a criterion is pending iff no prior deferred-pass block satisfies (a) or (b). INV-G* deferred-auto criteria are deliverable-scope-independent — covered only by a block where `deferred: true` and `scope: []`.

**Long-session / cross-session fallback.** When a normal-flow pass would route to "Deferred-Auto Pending" but no prior `deferred: true` return block is visible in conversation context (compaction, context length pressure, fresh session after the user ran `/verify --deferred` in an earlier session), /verify **overrides the normal-flow skip rule for this fallback** and runs all in-scope `deferred-auto` verifiers inline in the current pass — same routing as `--deferred` would use, just triggered by missing coverage rather than the flag. If they pass green, the pass completes normally and can reach `/done` (subject to the usual manual / non-deferred AC gating). If any fail, the pass returns failures like any other. Deferred-auto verifiers are idempotent by design; correctness over runtime cost. This prevents the cross-session escalation loop where the user runs `/verify --deferred` in session N then `/verify` in session N+1 and gets re-escalated.

### Deferred-Auto Pending Escalation

When a normal-flow `/verify` pass (selective or full) completes green but the manifest contains `deferred-auto` criteria not yet covered, /verify routes to `/escalate` with type `"Deferred-Auto Pending"`. The escalation message lists the pending criteria and instructs the user to invoke `/verify --deferred` once prerequisites are in place. Once those criteria pass via `--deferred`, a subsequent normal `/verify` pass can call `/done`.

**When BOTH manual criteria AND pending deferred-auto exist** after a normal full-mode green pass, surface BOTH in a single combined escalation block: list the manual criteria + their how-to-verify, AND list the pending deferred-auto criteria + the `/verify --deferred` instruction. /done remains unreachable until both are resolved.

**After `/verify --deferred` completes green** (all deferred-auto criteria pass), close the user-as-coordinator loop with an explicit next-step instruction: emit a message like *"Deferred-auto criteria green. Re-invoke `/verify <manifest>` (no flags) to reach /done."* Do NOT call /done from the `--deferred` pass itself — `--deferred` only verifies the deferred-auto subset; the final /done decision belongs to a normal-flow pass that confirms the full criterion universe is still green AND the deferred coverage now satisfies the gate.

### Cross-Repo Path Delivery

When the manifest declares `Repos:`, every /verify pass (selective, full, and `--deferred`) prepends a verbatim cross-repo prefix to each verifier's prompt. Format and full convention: `define/references/MULTI_REPO.md` §e (single source of truth). The prefix injection fires on every pass, not just `--deferred`, so cross-repo verifiers can run during normal `/do→/verify` flow — that's what makes /done reachable for multi-repo manifests without per-repo /done independence. Single-repo manifests (no `Repos:` field) get no prefix injection.

## Return Contract

Every /verify invocation returns a structured block as part of its tool result text so /do (and any future /verify pass) can parse what already ran. Format:

````markdown
## /verify pass N

```yaml
mode: selective|full             # under deferred:true, reflects --scope filter only — see Deferred-Auto Criteria
scope: [<deliverable-id>, ...]   # empty list when mode is full
result: pass|fail
failures: [<criterion-id>, ...]  # empty when pass; criterion IDs only, no narrative
auto_triggered_final: true|false # true only when this pass was auto-triggered by /verify after a true-selective green; false for first-pass-degenerated-to-full and for --deferred passes
deferred: true|false             # true when this pass ran via --deferred (only deferred-auto criteria checked); false for normal selective/full passes
```

[narrative — failed criterion details, fix hints, etc., per Outcome Handling]
````

**Pass numbers** are sequential within the current /do session, counted from the prior /verify return blocks visible in conversation. If no prior block is visible (fresh session or context pressure), start at 1.

**Field semantics:**

- **`deferred` is the master interpretation flag.** Consumers MUST read `deferred` before `mode`. Under `deferred: true`, `result: pass` means "the deferred-auto criteria are green," not "the whole manifest is green." Under `deferred: true`, write `mode: selective` if `--scope` was set, else `mode: full`.
- **Degenerated-to-full reporting.** When `--scope` and `--final` are both absent (and `--deferred` is not set), report `mode: full`, `scope: []`, `auto_triggered_final: false`. The pass already covered everything — report it as full.
- **`result: pass` does not imply /done was called.** A green pass may route to /escalate (Manual Criteria Review, Deferred-Auto Pending, or both) instead. Consumers asking "did /done fire?" must re-derive from the manifest's manual / deferred-auto coverage, not from `result` alone.
- **Consumers driving next-pass scope decisions** (e.g., /do scanning recent /verify returns) MUST skip blocks where `deferred: true` — those reflect partial verification, not normal-flow AC/INV state.

Pure markdown so humans can read; fenced YAML so /do and a future /verify can parse deterministically. /do reads the most recent block from conversation context, skipping `deferred: true` blocks per Field semantics above, to track progress and decide which pass to invoke next.
