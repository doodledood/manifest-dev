---
name: done
description: 'Completion marker for the /do workflow. Outputs hierarchical execution summary. Called by /verify after full-suite green with no pending manual or deferred-auto criteria, not directly.'
user-invocable: false
---

Output a completion summary mirroring the Manifest hierarchy: Intent → Global Invariants (all PASS) → Deliverables (each with ACs, all PASS) → key changes (files, commits, behavioral effect — not just file lists) → trade-offs applied → files modified. Adapt detail to task complexity. Multi-repo: /done fires **once per manifest**, not per repo; the summary lists which repos' deliverables were verified in this run.

**Gating** — /done is reachable only after /verify confirms a full-suite green pass + no pending manual + no pending deferred-auto.

**Mandatory trailing line** (verbatim — post-completion feedback routes off this line):

*Post-completion feedback defaults to amending this manifest. Send a message describing the change; pure questions are answered inline.*

**Post-completion two-step re-entry** when feedback arrives (both mandatory): (1) invoke `manifest-dev-experimental:define` with `<feedback>` — /define infers the amend target from the just-completed manifest in transcript context; (2) invoke `manifest-dev-experimental:do` with `<manifest-path> --scope <new-or-affected-deliverables>`. Scope inferred from the amendment's affected deliverables; omit `--scope` when amendment touches a Global Invariant or scope is unclear. Pure questions about the work answered inline. When ambiguous, amend.
