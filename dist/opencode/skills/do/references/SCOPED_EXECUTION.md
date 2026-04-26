# Scoped Execution

Loaded when `/do` receives `--scope <deliverable-ids>`. Limits execution to a subset of deliverables while maintaining safety guarantees.

## Rules

1. **Execute only in-scope deliverables.** Work on deliverables listed in `--scope` (e.g. `--scope D2,D3` means only D2 and D3). Skip all others.

2. **Out-of-scope deliverables are pre-passed.** Treat their ACs as already satisfied — pull pass status from the execution log. Do not re-execute their ACs. If the execution log has no record for an out-of-scope AC, treat it as passed (the caller is asserting scope correctness). **Note:** `--scope` is designed for reruns after a prior full execution. If no execution log is provided or the log has no entries, warn: "Scoped execution without prior execution log — out-of-scope deliverables have no prior work. The selective `/verify` pass will only check in-scope ACs + globals; out-of-scope ACs will be checked by the mandatory full final gate before `/done`, and unimplemented out-of-scope deliverables will likely fail there."

3. **Global Invariants always run.** INV-G* verification runs regardless of scope. These are constitutional constraints — scoping does not exempt them. A scoped run that breaks a global invariant is a failure.

4. **Verification follows the selective-verify rules.** Per `/verify` SKILL.md (Selective vs Full Verification), a scoped `/do` invokes `/verify` with the same `--scope`, which runs only the in-scope deliverables' ACs plus all Global Invariants. Out-of-scope ACs are NOT re-verified during the fix-loop — they're verified by the mandatory full final gate that `/verify` auto-triggers before `/done`. Within the in-scope set, phases still gate execution from Phase 1 ascending. The fix-loop rule "globals always run" still applies (INV-G* are constitutional).

5. **Log scoped context.** At the start of a scoped run, log which deliverables are in-scope and which are skipped. This makes the execution log self-documenting for future readers.

## When `/tend-pr` Invokes Scoped `/do`

`/tend-pr` uses `--scope` to limit blast radius after PR review feedback. It determines affected deliverables from PR comments and passes only those. The manifest may have been amended (new regression ACs added) before this scoped run — read the manifest fresh, not from memory.
