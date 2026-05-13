# Scoped Execution

Loaded when `/do` receives `--scope <deliverable-ids>`. Limits execution to a subset of deliverables while maintaining safety guarantees.

## Rules

1. **Execute only in-scope deliverables.** Work on deliverables listed in `--scope` (e.g. `--scope D2,D3` means only D2 and D3). Skip all others.

2. **Out-of-scope deliverables are pre-passed.** Treat their ACs as already satisfied — the caller is asserting scope correctness. Do not re-execute their ACs. **Note:** `--scope` is designed for reruns after a prior full execution. If this is a fresh session with no prior pass state visible in conversation, warn: "Scoped execution without prior pass context — out-of-scope deliverables have no prior work in this session. The selective `/verify` pass will only check in-scope ACs + globals; out-of-scope ACs will be checked by the mandatory full final gate before `/done`, and unimplemented out-of-scope deliverables will likely fail there."

3. **Global Invariants always run.** INV-G* verification runs regardless of scope. These are constitutional constraints — scoping does not exempt them. A scoped run that breaks a global invariant is a failure.

4. **Verification follows the selective-verify rules.** Per `/verify` SKILL.md (Selective vs Full Verification), a scoped `/do` invokes `/verify` with the same `--scope`, which runs only the in-scope deliverables' ACs plus all Global Invariants. Out-of-scope ACs are NOT re-verified during the fix-loop — they're verified by the mandatory full final gate that `/verify` auto-triggers before `/done`. Within the in-scope set, phases still gate execution from Phase 1 ascending. The fix-loop rule "globals always run" still applies (INV-G* are constitutional).

5. **Surface scoped context.** At the start of a scoped run, state which deliverables are in-scope and which are skipped, so the conversation carries the scope decision forward for future reference.

## When the User Invokes Scoped `/do`

`--scope` limits blast radius after PR review feedback or targeted regression fixes. The user (or a calling workflow) determines affected deliverables and passes only those. The manifest may have been amended (new regression ACs added) before this scoped run — read the manifest fresh, not from memory.
