---
name: done
description: 'Completion marker for the /do workflow. Outputs hierarchical execution summary showing Global Invariants respected and all Deliverables completed. Called by /verify after a full-suite green pass with no pending manual or deferred-auto criteria, not directly.'
user-invocable: false
---

Output a completion summary mirroring the Manifest hierarchy. Read the manifest and execution log; show:

- **Intent** — Goal from manifest.
- **Global Invariants** — table of every INV-G with status PASS.
- **Deliverables** — each with its ACs as a table (all PASS), plus key changes (files modified, commits made, behavioral effect — not just file lists).
- **Trade-offs applied** — how T-* preferences were used.
- **Files modified** — summary table.

Adapt detail to task complexity: simple task = condensed; complex task = full hierarchy.

**Multi-repo.** When the manifest declares `Repos:`, /done fires **once per manifest** — not once per repo. The summary additionally lists which repos' deliverables were verified in this run.

**Gating** — /done is called only after /verify confirms a full-suite green pass: every AC across every deliverable + every Global Invariant + no pending manual criteria + no pending deferred-auto criteria. Selective-mode green alone is insufficient; /verify auto-triggers a full pass before calling /done.

**Mandatory trailing line.** The output must end with this italic line so post-completion feedback routes correctly:

*Post-completion feedback defaults to amending this manifest. Send a message describing the change; pure questions are answered inline.*

**Post-completion feedback.** After /done, the manifest is still canonical for the PR/branch (or PR set / branch set in multi-repo). Feedback that changes scope or contradicts the manifest amends it via two-step re-entry (both mandatory):

1. Invoke `manifest-dev-experimental:define` with `<feedback> --amend <manifest-path>`. Wait for /define to return; note the manifest path.
2. Invoke `manifest-dev-experimental:do` with `<manifest-path> <log-path> --scope <new-or-affected-deliverables>`. `<log-path>` is the existing execution log from the original run; `--scope` is inferred from the amendment's new-or-modified deliverables. When the amendment touches a Global Invariant or scope is genuinely unclear, omit `--scope` for full execution.

Both steps mandatory — stopping after step 1 leaves the manifest amended but unimplemented. The amendment loop guard (consecutive Self-Amendments without external input → Proposed Amendment) applies to re-entry too. The /do mandatory full final gate runs unconditionally before /done — too-narrow --scope still can't land a regression.

Pure questions about the work are answered inline, not amended. When ambiguous, amend.

**Medium routing.** When medium is non-local, output flows through the calling context (/verify → /do). No special routing.
