---
name: verify
description: 'Runs verifiers for Global Invariants and Acceptance Criteria from a Manifest. Spawns verifier agents in parallel within each phase, reports results, routes to /done or /escalate. Normally invoked by /do; users invoke `/verify --deferred` to run user-triggered deferred-auto criteria.'
user-invocable: true
---

# /verify

Read the manifest and execution log. Spawn verifiers for the in-scope criteria. Aggregate results. Route the outcome to /done or /escalate.

**Input.** `<manifest-path> <log-path> [--scope D1,D2,...] [--deferred]`. Either path missing → halt with usage. Manifest missing → halt. Log missing → create empty file (must always be appendable). `--final` is internal-only; /do never passes it, users never pass it.

## Routing by criterion `method:`

| Method | Verifier |
|--------|----------|
| `bash` / `codebase` / `research` | criteria-checker |
| `subagent` | the agent named in the criterion's `agent:` field |
| `manual` | /escalate (no automated check exists) |
| `deferred-auto` | skipped on normal passes; under `--deferred`, routed by the criterion's required `inner_method:` field |
| (none / unrecognized) | criteria-checker |

`method: deferred-auto` MUST declare a sibling `inner_method:` (`subagent` | `bash` | `codebase` | `research`). Missing → halt: `Deferred-auto criterion <ID> missing inner_method.`

## Selective vs full

- **Selective pass** — runs in-scope deliverables' ACs + all Global Invariants. Triggered by `--scope D2,D3` (filter narrows).
- **Full pass** — runs every AC + every INV-G. Triggered when `--scope` absent (selective degenerates to full) or when `--final` is set (internal auto-trigger).
- **After a true-selective green** (where `--scope` was set and pass went green), **auto-trigger a full pass** by re-invoking /verify internally with `--final`. Unconditional. The auto-final is the safety net for cross-deliverable regressions.
- **Selective-degenerated-to-full** (no `--scope` was set): the pass already covered everything; no auto-trigger needed.

## Phased execution

Criteria carry an optional `phase:` (default 1). Group by phase, run lowest first. Phase N+1 launches only when all Phase N criteria pass. On phase failure: return failures immediately with phase context (`Phase N failed, Phase N+1 not run`) so /do enters fix loop without running later phases. Non-contiguous phases valid. Scope filter applies first, then phases gate the filtered set.

## Verifier prompts

Pass each verifier three sections in this order, each on its own line:

1. **Cross-repo prefix** — only when manifest declares `Repos:`. Verbatim from `define/references/MULTI_REPO.md` §e (single source of truth). Skip for single-repo manifests.
2. **Optional context line** — only when at least one of manifest/discovery-log/execution-log paths exists. Format: `Optional context — manifest: <path>, discovery log: <path>, execution log: <path>`. Include only existing paths. Informational, not directive.
3. **Criterion content** — criterion's manifest data: ID, description, `method:`, and the verify block's `command:` or `prompt:` verbatim. If `prompt:` absent (e.g., bash), pass the description.

**Never add framing to criterion content** — no severity thresholds, no implementation context, no opinions, no leading language, no task summaries, no suggested outcomes, no interpretations of intent. The verify block's `prompt:` is authored by /define; pass it verbatim.

## Outcome routing

Group results by phase, then INV-G first, then by Deliverable.

| Condition | Action |
|-----------|--------|
| Any INV-G failed | Return failures, globals highlighted |
| Any AC failed (no global failures) | Return failures grouped by deliverable |
| All in-scope pass; true-selective | Auto-trigger full pass (`--final` self-invocation). Do not call /done. |
| All pass; full or degenerated-to-full; manual criteria exist; no pending deferred-auto | /escalate "Manual Criteria Review" with each manual criterion + how-to-verify. Do not call /done. |
| All pass; full or degenerated-to-full; pending deferred-auto exist; no manual | /escalate "Deferred-Auto Pending" listing pending criteria + `/verify --deferred` instruction. Do not call /done. |
| All pass; manual AND pending deferred-auto | Combined /escalate "Manual Review + Deferred-Auto Pending" |
| All pass; full; no manual; no pending deferred-auto | Call /done |

Hard final gate — /done is unreachable from selective-mode green alone. Auto-triggered full final fires unconditionally after true-selective green. Failure during auto-final → /do enters standard fix loop; /verify runs a fresh selective pass scoped to the failure, then auto-triggers full again.

## Deferred-auto

`method: deferred-auto` = automatically verifiable but user-triggered (e.g., cross-repo gates the user signals readiness for: "all PRs deployed"). The verifier runs automatically; only triggering is user-controlled.

- **Normal flow skips them.** Never appear in failure list of a normal pass. But uncovered deferred-auto blocks /done — green pass with pending deferred-auto routes to /escalate "Deferred-Auto Pending".
- **`--deferred` runs ONLY them.** Everything else (INV-Gs, non-deferred ACs) skipped. Inherits `--scope` (narrows the deferred-auto set). Never enters --final machinery, never calls /done from itself.
- After `--deferred` green, emit instruction: *"Deferred-auto criteria green. Re-invoke `/verify <manifest> <log>` (no flags) to reach /done."*

**Coverage determination.** A deferred-auto criterion is covered when a preceding pass-log block has `deferred: true`, `result: pass`, and either `scope: []` (full deferred coverage) OR `scope:` contains the criterion's owning deliverable. INV-G deferred-auto criteria are deliverable-scope-independent — covered only by a block with `deferred: true` and `scope: []`.

## Pass logging contract

Every invocation appends a structured block to the execution log:

````markdown
## /verify pass {N}

```yaml
scope: [<deliverable-id>, ...]    # empty list when pass is full
result: pass|fail
failures: [<criterion-id>, ...]   # empty when pass; criterion IDs only, no narrative
auto_triggered_final: true|false  # true only when this pass was self-triggered after a true-selective green
deferred: true|false              # true when this pass ran via --deferred
```

[narrative — failed criterion details with file:line, expected vs actual, fix hint]
````

`deferred` is the master interpretation flag — consumers MUST read it before `scope`. Under `deferred: true`, `result: pass` means deferred-auto criteria green, not the whole manifest. Consumers scanning for next-pass scope **skip blocks where `deferred: true`** (those reflect partial verification).

`result: pass` does not imply /done was called. A green pass may route to /escalate (Manual / Deferred-Auto Pending / Combined) instead. Consumers asking "did /done fire?" must re-derive from manual/deferred coverage, not from `result` alone.

## Principles

- **All in-scope criteria verify** — every criterion in the current pass's scope MUST be verified. Skipping is a critical failure.
- **Orchestrate, don't verify** — spawn agents to verify; aggregate results and coordinate; never run checks yourself.
- **Don't handle user feedback during a pass** — mid-pass user messages are feedback to the caller (/do, or the user who invoked `--deferred` directly), not /verify. /verify never amends, never re-prompts; it returns results.
- **Spawn verifiers in parallel within each phase** — phases run sequentially; criteria within a phase run concurrently.
- **Agent crash ≠ criterion pass** — verifier crash / timeout / unusable output: criterion FAIL with note that verification itself failed. /do distinguishes "didn't pass" from "couldn't check."
