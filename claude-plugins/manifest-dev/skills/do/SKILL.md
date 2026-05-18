---
name: do
description: 'Manifest executor. Works through Deliverables verifying every Acceptance Criterion and Global Invariant. Use when executing a manifest, running a plan, implementing a defined task. Triggers: do, execute, run the manifest, implement plan, run plan, execute manifest, ship the manifest.'
argument-hint: '<manifest-path>'
user-invocable: true
---

Work toward the manifest's Deliverables. Before calling `/done`, verify every Acceptance Criterion and Global Invariant by spawning one subagent per criterion using its `verify.prompt:` verbatim — no rewording. (Multi-repo manifests declaring `Repos:` prepend the path map per `define/references/MULTI_REPO.md`; otherwise nothing wraps the author's prompt.) The optional `verify.agent:` names the subagent type (default: general-purpose); the optional `verify.model:` selects the model. Respect `phase:` ordering — serial across phases, parallel within. Each verifier returns PASS, FAIL, or BLOCKED; all must PASS before `/done`. Any BLOCKED routes via `/escalate`.

**FAIL body contract.** FAIL bodies carry either a per-gate **directive** (specialized verifiers like `github-pr-lifecycle` emit `FAIL — <directive>` lines from a fixed vocabulary: `bash sleep <N>; reinvoke`, `retrigger <check>`, `reply <thread>`, `reply-and-resolve <thread>`, `re-request-review`, `sync-description`, `escalate`) or a natural-language hint (generic verifiers describe the situation in prose). **Execute directives literally — verbatim, no substitution. Do NOT substitute `Stop`, `/loop`, `ScheduleWakeup`, or busy-waiting (re-invoking the verifier without the intervening sleep) for a `bash sleep` directive; those bypass the polling contract and the wait silently dies.** Prose hints are read with LLM judgment.

**Budget + routing.** Only code-change fix attempts count toward the budget (iterate until pass or genuinely unrecoverable → `/escalate`); other retry shapes (waiting, retriggering, replying with or without resolving, mechanical syncs) don't burn the budget. When a hint or directive indicates a reviewer ask beyond the work's intent, route to amendment via `manifest-dev:define --amend`. **When a hint indicates terminal / unrecoverable / human-decision-needed, or a directive is `escalate`, route to `/escalate` — autonomously amending the manifest to suppress the block is forbidden.**

Mid-/do user messages default to invoking `manifest-dev:define` for amendment — the manifest is the source of truth, silent scope drift is worse than an extra amendment cycle. Pure questions about the manifest or process are answered inline.

**Input.** `<manifest-path>` — required; no args → halt with usage. Read the manifest fully before any execution. Multi-repo manifests (declare `Repos: [name: path, ...]` in Intent) — use absolute paths in tool calls when working in a non-cwd repo.
