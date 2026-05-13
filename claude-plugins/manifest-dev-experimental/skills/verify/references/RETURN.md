# Return Contract

Every /verify invocation returns a structured block as part of its tool result text so /do (and any future /verify pass) can read what already ran:

````markdown
## /verify pass N

```yaml
scope: [<deliverable-id>, ...]    # empty list when the pass is full
result: pass|fail
failures: [<criterion-id>, ...]   # empty when result: pass; criterion IDs only, no narrative
auto_triggered_final: true|false  # true when this pass was self-invoked after a preceding true-selective green (derived from the preceding return block visible in conversation)
deferred: true|false              # true when this pass ran deferred-auto criteria (inferred from conversation context — user readiness signal detected)
```

[narrative — failed criterion details with file:line, expected vs actual, fix hint per OUTCOMES.md]
````

Pure markdown so humans can read; fenced YAML so /do and a future /verify can parse deterministically. Pass numbers are sequential within the current /do session, counted from prior /verify return blocks visible in conversation. If no prior block is visible (fresh session or context pressure), start at 1.

## Field semantics

- **`deferred` is the master interpretation flag.** Consumers MUST read `deferred` BEFORE interpreting `result` or `scope`. Under `deferred: true`, `result: pass` means "the deferred-auto criteria are green," NOT "the whole manifest is green."
- **Under `deferred: true`**, write `scope: [...]` if a `--scope` filter was applied, else `scope: []`.
- **`auto_triggered_final`** is true only when /verify self-invoked this pass after a preceding true-selective green (derived from reading the preceding return block visible in conversation — if its `result: pass`, `scope:` non-empty, `auto_triggered_final: false`, this invocation is the auto-final). /do never sets this.
- **`deferred` setting rule.** /verify reads the recent conversation context. If the user has signaled readiness (e.g., "all deployed", "staging is up", "go ahead") AND the manifest has `method: deferred-auto` criteria → include them in this pass and write `deferred: true`. Otherwise → skip deferred-auto and write `deferred: false`. Ambiguous signals default to skip.
- **Degenerated-to-full reporting.** When `--scope` is absent and no deferred-auto inclusion fires, report `scope: []`, `result: ...`, `auto_triggered_final: false`, `deferred: false`. The pass covered everything except deferred-auto.
- **`result: pass` does not imply /done was called.** A green pass may route to /escalate (Manual / Deferred-Auto Pending / Combined). Consumers asking "did /done fire?" must re-derive from the manifest's manual / deferred-auto coverage, not from `result` alone.

## Coverage determination (deferred-auto)

A deferred-auto criterion is "covered" when there exists a preceding return block in conversation where `deferred: true`, `result: pass`, AND either:
- `scope: []` (full deferred coverage), OR
- `scope:` contains the deliverable that owns the criterion.

/verify aggregates coverage across all prior deferred-pass blocks visible in conversation: a criterion is pending iff no prior block satisfies one of the above conditions. INV-G* deferred-auto criteria are deliverable-scope-independent — covered only by a block where `deferred: true` AND `scope: []`.

**Long-session / cross-session fallback.** When a normal-flow pass would route to "Deferred-Auto Pending" but no prior `deferred: true` return block is visible in conversation (compaction, context length pressure, fresh session after a prior `--deferred` run), override the normal-flow skip rule for this fallback only: run all in-scope deferred-auto verifiers inline in the current pass — same routing as `--deferred` would use, just triggered by missing coverage. Green → pass completes normally and can reach `/done`. Any failure → returns failures like any other pass. Verifiers are idempotent by design; correctness over runtime cost. Prevents the cross-session escalation loop where the user runs `/verify --deferred` in session N then `/verify` in session N+1 and gets re-escalated.

## Consumer reading rule

Consumers driving next-pass scope decisions (e.g., /do scanning recent /verify returns) MUST **skip blocks where `deferred: true`** — those reflect partial verification, not normal-flow AC/INV state.
