---
name: do
description: 'Experimental. Manifest executor. Works through Deliverables verifying every Acceptance Criterion and Global Invariant. Use when executing a manifest, running a plan, implementing a defined task. Triggers: do, execute, run the manifest, implement plan, run plan, execute manifest, ship the manifest.'
argument-hint: '<manifest-path>'
user-invocable: true
---

Work toward the manifest's Deliverables. Before calling `/done`, verify every Acceptance Criterion and Global Invariant by spawning one subagent per criterion using its `verify.prompt:` verbatim — no rewording. (Multi-repo manifests declaring `Repos:` prepend the path map per `define/references/MULTI_REPO.md`; otherwise nothing wraps the author's prompt.) The optional `verify.agent:` names the subagent type (default: general-purpose); the optional `verify.model:` selects the model. Respect `phase:` ordering — serial across phases, parallel within. Each verifier returns PASS, FAIL, or BLOCKED; all must PASS before `/done`. Any BLOCKED routes via `/escalate`. Code-change FAILs trigger fix-and-re-verify until pass or genuinely unrecoverable (then `/escalate`); wait-shaped FAILs (CI in flight, approval pending, transient retry) are dispatched to wait and re-verified without consuming the fix budget.

Mid-/do user messages default to invoking `manifest-dev-experimental:define` for amendment — the manifest is the source of truth, silent scope drift is worse than an extra amendment cycle. Pure questions about the manifest or process are answered inline.

**Input.** `<manifest-path>` — required; no args → halt with usage. Read the manifest fully before any execution. Multi-repo manifests (declare `Repos: [name: path, ...]` in Intent) — use absolute paths in tool calls when working in a non-cwd repo.
