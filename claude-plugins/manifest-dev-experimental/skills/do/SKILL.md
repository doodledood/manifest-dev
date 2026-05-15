---
name: do
description: 'Experimental. Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, then verifies via /verify. Use when executing a manifest, running a plan, implementing a defined task.'
argument-hint: '<manifest-path> [--scope <ids>]'
user-invocable: true
---

# /do

Execute a Manifest: satisfy every Deliverable's Acceptance Criteria while following Process Guidance and using Approach as initial direction (adapt when reality diverges). Verify via /verify; /verify routes to /done or /escalate. Stopping requires routing through /verify or /escalate; bare statements like "Done." or "Waiting." are not valid exits.

**Input.** `<manifest-path> [--scope D1,D2,...]`. No args → halt with usage. Read the manifest fully before any execution.

**Principles.** ACs define success (manifest says WHAT, you decide HOW). Approach is initial direction (adapt freely when reality diverges; track adjustments and rationale in-context). Target failures specifically (fix the failing criterion only; don't restart, don't touch passing ones). Verify the fix before re-running full verification. Consult Trade-offs when Risks materialize. **Per-phase fix-attempt cap:** stop when attempts stop producing new diagnostic information — escalate instead. **Action-aware:** only code-change fix attempts count toward the cap; re-verifying after a wait, retriggering transient CI, posting a thread reply, pushing a sync update, routing scope-changes through Self-Amendment do NOT burn the budget.

**Default to amend.** Any user message during /do or /verify defaults to triggering Self-Amendment: invoke `manifest-dev-experimental:define` for amendment — /define infers fast-path from caller context (no summary wait) and infers the amend target from the just-written manifest in transcript. Pure questions about manifest/process answered inline. State updates that signal deferred-auto readiness (e.g., "all deployed", "staging is up", "go ahead") are NOT amendments — they're context for the next /verify's deferred-auto inference; note them in conversation and proceed. When ambiguous between amendment and other intents, amend (silent scope drift is worse than an unnecessary amendment cycle). /verify-time user messages are feedback to /do, not /verify. Amendment loop guard: consecutive Self-Amendments without external input → escalate as Proposed Amendment. Same path handles verifier-emitted out-of-scope findings.

**Track decisions in-context.** Carry surprises during implementation, divergences from Approach with rationale, fix rationales, amendment triggers, and domain knowledge discovered across the conversation. The manifest is the durable artifact; the in-session conversation is working memory. /verify returns `## /verify pass N` blocks in its tool result text — read the most recent one in conversation to drive next-pass scope decisions; skip `deferred: true` blocks. When in-tool session continuation isn't available (cross-tool, cross-session, multi-agent handoff), Invoke the `manifest-dev-tools:handoff` skill for a transfer payload. **Multi-repo:** when manifest declares `Repos:`, use absolute paths in tool calls per the path map. **Scoped execution** (`--scope D2,D3`): limits work to those deliverables; globals always verify. Re-read the manifest's deliverable section before starting a new deliverable when context has drifted. **/verify invocation patterns** and **escalation boundary** in `references/PATTERNS.md`.

**Verifier hints.** FAIL bodies carry free-form actionable hints in natural English (wait for CI, change code, retrigger transient failure, reply on a thread, push a sync update, surface out-of-scope finding). Read with LLM judgment; no required vocabulary. Unlabeled or ambiguous → treat as code-fix hint.
