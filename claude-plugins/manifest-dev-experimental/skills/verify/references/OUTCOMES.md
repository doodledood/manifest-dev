# Outcome Routing

## Terminology

- **True-selective.** A selective pass where `--scope` was set (the filter actually narrowed the criterion universe).
- **Selective-degenerated-to-full.** A selective pass where `--scope` was absent — no narrowing applied, the pass covered everything. Treated as full for outcome handling.
- **Auto-final.** A full pass /verify self-invoked after a preceding true-selective green. /verify identifies an auto-final invocation by reading its own most recent pass log block — if the previous block had `result: pass`, `scope:` non-empty, `auto_triggered_final: false`, this pass is the auto-final.
- **Deferred-auto inclusion.** /verify includes deferred-auto criteria in a pass when the conversation context contains an explicit user readiness signal (e.g., "all deployed", "staging is up", "go ahead"). Without the signal, deferred-auto criteria are skipped (uncovered ones still block /done via escalation).

## Routing table

Group results: phase first, then INV-G first, then by Deliverable.

| Condition | Action |
|-----------|--------|
| Any INV-G failed | Return failures, globals highlighted |
| Any AC failed (no global failures) | Return failures grouped by deliverable |
| All in-scope pass; true-selective | Auto-trigger full pass (self-invoke for a full pass; /verify derives this as the auto-final). Do NOT call /done. Manual / Deferred-Auto Pending escalations are deferred to the auto-triggered full pass. |
| All pass; full or selective-degenerated-to-full; manual criteria exist; no pending deferred-auto | /escalate "Manual Criteria Review" with each manual criterion + how-to-verify. Do NOT call /done. |
| All pass; full or selective-degenerated-to-full; pending deferred-auto exist; no manual | /escalate "Deferred-Auto Pending" listing pending criteria + chat-signal instruction. Do NOT call /done. |
| All pass; manual AND pending deferred-auto | Combined /escalate "Manual Review + Deferred-Auto Pending" — both inline. Do NOT call /done. |
| All pass; full; no manual; no pending deferred-auto | Call /done |

## Hard final gate

- **/done is unreachable from selective-mode green alone.** Per project directive ("Done means nothing more to do"): only a full-mode green pass — every AC across every deliverable + every Global Invariant — with no pending manual + no pending deferred-auto calls /done.
- **Pending manual blocks /done** → /escalate "Manual Criteria Review".
- **Pending deferred-auto blocks /done** → /escalate "Deferred-Auto Pending".
- **Both pending → combined /escalate.**
- **Once a true-selective pass goes green, the auto-trigger fires unconditionally** — no opt-out.
- **Auto-final failure → standard fix-loop.** /verify returns failures to /do; /do fixes; /verify then runs a fresh selective pass scoped to the failing deliverable, then auto-triggers full again.

## Phase failure reporting

When a phase fails, include the phase number and note which later phases were not run (e.g., "Phase 1: 2 failures. Phase 2: not run (3 criteria pending)."). Do not run later phases — let /do enter the fix loop faster.

## Phase + scope orthogonality

`phase:` gates execution order (ascending). Selective vs full filters the universe of criteria. Within a selective pass, the scope filter applies first, then phases gate the filtered set.
