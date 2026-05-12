---
name: do
description: 'Manifest executor. Iterates through Deliverables satisfying Acceptance Criteria, verifies via /verify, defaults to amending the manifest on user feedback. Use when executing a manifest, running a plan, implementing a defined task.'
user-invocable: true
---

Execute a Manifest: satisfy every Deliverable's Acceptance Criteria while following Process Guidance and using Approach as initial direction — adapt freely when reality diverges, log adjustments with rationale. Verify via `manifest-dev-experimental:verify`; verify routes to /done or /escalate. **Hard prohibitions:** never invoke `gh pr merge` (terminal is "PR mergeable", not merged; merge-button hints are ignored as malformed); no silent halts (stopping requires /verify or /escalate; bare "Done." or "Waiting." are not valid exits).

**Principles.** ACs define success (manifest says WHAT, you decide HOW). Approach is initial direction (adapt freely, no escalation needed). Target failures specifically (fix the failing criterion only; don't restart, don't touch passing ones). Verify the fix before re-running full verification. Consult Trade-offs when Risks materialize. **Per-phase fix-attempt cap:** stop when attempts stop producing new diagnostic information — escalate instead. **Action-aware:** only code-change fix attempts count toward the cap; re-verifying after a wait, retriggering transient CI, posting a thread reply, pushing a sync update, routing scope-changes through Self-Amendment do NOT burn the budget.

**Default to amend.** Any user message during /do or /verify defaults to triggering Self-Amendment: invoke `manifest-dev-experimental:define` with `--amend <manifest-path> --from-do`, then resume with updated manifest. Pure questions about manifest/process answered inline. When ambiguous, amend (silent scope drift is worse than an unnecessary amendment cycle). /verify-time user messages are feedback to /do, not /verify. Amendment loop guard: consecutive Self-Amendments without external input → escalate as Proposed Amendment. Same path handles verifier-emitted out-of-scope findings.

**Execution log** at `/tmp/do-log-{ts}.md` (or the path passed as second positional arg — append-only iteration on prior work). Narrate events a future reader needs: surprises during implementation, divergences from Approach with rationale, fix rationales, amendment triggers, domain knowledge discovered. Skip routine status pings. /verify appends its own `## /verify pass {N}` structured blocks alongside — leave those as-is. Read the full log before each /verify call; re-read manifest deliverable section before starting a new deliverable. **Multi-repo:** when manifest declares `Repos:`, use absolute paths in tool calls per the path map. **Scoped execution** (`--scope D2,D3`): limits work to those deliverables; globals always verify. **/verify invocation patterns** and **escalation boundary** in `references/PATTERNS.md`.

**Verifier hints.** FAIL bodies carry free-form actionable hints in natural English (wait for CI, change code, retrigger transient failure, reply on a thread, push a sync update, surface out-of-scope finding). Read with LLM judgment; no required vocabulary. Unlabeled or ambiguous → treat as code-fix hint.

**Input.** `<manifest-path> [<log-path>] [--scope D1,D2,...]`. No args → halt with usage. Read the manifest fully before any execution.
