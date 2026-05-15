---
name: do
description: 'Experimental. Manifest executor. Works through Deliverables verifying every Acceptance Criterion via subagents, calls /done when all pass, /escalate when blocked. Use when executing a manifest, running a plan, implementing a defined task.'
argument-hint: '<manifest-path>'
user-invocable: true
---

Work toward the manifest's Deliverables. Before calling `/done`, verify every Acceptance Criterion by spawning one subagent per AC using its `verify.prompt:` verbatim — no framing, no rewording. The optional `verify.agent:` field names the subagent type (default: general-purpose); the optional `verify.model:` selects the model. Respect `phase:` ordering — serial across phases, parallel within. Each verifier returns PASS, FAIL, or BLOCKED; all must PASS before `/done`. Any BLOCKED routes via `/escalate`. FAILs trigger fix-and-re-verify until pass or the criterion is genuinely unrecoverable, then `/escalate`.

Mid-/do user messages default to invoking `manifest-dev-experimental:define` for amendment — the manifest is the source of truth, silent scope drift is worse than an extra amendment cycle. Pure questions about the manifest or process are answered inline.

**Input.** `<manifest-path>` — required; no args → halt with usage. Read the manifest fully before any execution. Multi-repo manifests (declare `Repos: [name: path, ...]` in Intent) — use absolute paths in tool calls when working in a non-cwd repo.
