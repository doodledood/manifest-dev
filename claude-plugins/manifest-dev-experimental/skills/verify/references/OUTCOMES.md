# Outcome Routing

Group results: phase first, then INV-G first, then by Deliverable.

| Condition | Action |
|-----------|--------|
| Any INV-G failed | Return failures, globals highlighted |
| Any AC failed (no global failures) | Return failures grouped by deliverable |
| All in-scope pass; **true-selective** (`--scope` was set) | Auto-trigger full pass (`--final` self-invocation). Do NOT call /done. Manual / Deferred-Auto Pending escalations are deferred to the auto-triggered full pass. |
| All pass; full or selective-degenerated-to-full; manual criteria exist; no pending deferred-auto | /escalate "Manual Criteria Review" with each manual criterion + how-to-verify. Do NOT call /done. |
| All pass; full or selective-degenerated-to-full; pending deferred-auto exist; no manual | /escalate "Deferred-Auto Pending" listing pending criteria + `/verify --deferred` instruction. Do NOT call /done. |
| All pass; manual AND pending deferred-auto | Combined /escalate "Manual Review + Deferred-Auto Pending" — both inline. Do NOT call /done. |
| All pass; full; no manual; no pending deferred-auto | Call /done |

## Hard final gate

- **/done is unreachable from selective-mode green alone.** Per project directive ("Done means nothing more to do"): only a full-mode green pass — every AC across every deliverable + every Global Invariant — with no pending manual + no pending deferred-auto calls /done.
- **Pending manual blocks /done** → /escalate "Manual Criteria Review".
- **Pending deferred-auto blocks /done** → /escalate "Deferred-Auto Pending".
- **Both pending → combined /escalate.**
- **Once a true-selective pass goes green, the auto-trigger fires unconditionally** — no opt-out.
- **Auto-final failure → standard fix-loop.** /verify returns failures to /do; /do fixes; /verify then runs a fresh selective pass scoped to the failing deliverable, then auto-triggers full again.
- **`--final` is internal-only.** /verify uses it to re-invoke itself after a true-selective green; /do never passes it.

## Selective-degenerated-to-full

When `--scope` and `--final` are both absent (and `--deferred` is not set), selective degenerates to full. The pass already covered everything; treat as full for outcome handling. No "auto-trigger another full pass" — that would be redundant.

## Phase failure reporting

When a phase fails, include the phase number and note which later phases were not run (e.g., "Phase 1: 2 failures. Phase 2: not run (3 criteria pending)."). Do not run later phases — let /do enter the fix loop faster.

## Phase + scope orthogonality

`phase:` gates execution order (ascending). Selective vs full filters the universe of criteria. Within a selective pass, the scope filter applies first, then phases gate the filtered set.
