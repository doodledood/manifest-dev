# Execution Modes

Execution modes control verification intensity across the manifest-dev workflow (/define, /do, /verify). The mode affects subagent model selection, quality gate inclusion, parallelism, fix-verify loop limits, and manifest validation depth. It does NOT affect what gets built — only how thoroughly the output is verified.

## Mode Routing Table

| Dimension | efficient | balanced | thorough (default) |
|-----------|-----------|----------|--------------------|
| Criteria-checker model | haiku | inherit | inherit |
| Quality gate reviewers | SKIPPED | inherit | inherit |
| Verification parallelism | Sequential (one at a time) | Batched (max 4 concurrent) | All at once (single message) |
| Fix-verify loops | Max 1 | Max 2 | Unlimited |
| /define manifest-verifier | SKIPPED | Runs once (no repeat loop) | Runs (with repeat loop) |
| Escalation | Auto-escalate after 2 failures per criterion; cap 3 total | Escalate after loop limit hit | None |

**Why these levels exist**: thorough preserves the current quality bar (default). balanced saves quota by limiting parallelism and verification cycles while keeping full model capability. efficient maximizes savings by using a cheaper model for verification and skipping reviewer agents — accept this only when iteration speed matters more than verification depth.

## Escalation Rules

**Efficient mode**: When a criterion fails twice at haiku, auto-escalate that criterion's verifier to inherit (session model). Track total escalations — after 3 in a single /do run, suggest to the user: "Efficient mode is escalating frequently. Consider switching to balanced." This prevents runaway costs from repeated escalation.

**Balanced mode**: When the fix-verify loop limit (2) is hit, escalate via /escalate. The fix isn't converging — human judgment needed.

**Thorough mode**: No escalation mechanism. Unlimited loops, full model capability.

## Verification Parallelism

Mode parallelism applies **within each phase**. Phases always run in ascending order — Phase N+1 only starts when all Phase N criteria pass. Within a phase:

- **efficient**: Launch verifiers one at a time. Minimizes concurrent quota usage.
- **balanced**: Launch in batches of max 4 concurrent verifiers. When any batch completes, launch the next batch.
- **thorough**: Launch all verifiers in a single message.

## Phase × Loop Limits

Fix-verify loop limits apply **per-phase**. Each phase has its own loop counter.

- In balanced mode (max 2 loops): Phase 1 can fail/fix twice, Phase 2 can fail/fix twice independently.
- A Phase 2 fix that regresses Phase 1 increments Phase 1's counter (the failure IS in Phase 1).
- Phase doesn't change efficient-mode skip rules — the skip/run decision is based on criterion type (INV-G* always run, deliverable-level reviewer ACs skipped in efficient), not phase number.

## Override Precedence

Three rules govern how mode interacts with other settings:

1. **Criterion-level model wins**: When a manifest criterion specifies `model:` in its verify block, that overrides the mode's model routing. Mode sets defaults; criterion-level `model:` is explicit intent.

2. **Explicit model overrides skip**: In efficient mode, quality gate reviewers are skipped. But if a criterion explicitly sets `model:` (e.g., `model: opus`), it runs even when efficient mode would otherwise skip it. The explicit model signals the user deliberately wants this verification.

3. **Global Invariants always run**: "Reviewers SKIPPED" in efficient mode applies only to deliverable-level quality gate reviewer agents (code-bugs-reviewer, type-safety-reviewer, etc.). Global Invariant (INV-G*) verification agents always run regardless of mode — they are constitutional constraints.
