---
name: do
description: 'Manifest executor. Works through Deliverables verifying every Acceptance Criterion and Global Invariant. Use when executing a manifest, running a plan, implementing a defined task. Triggers: do, execute, run the manifest, implement plan, run plan, execute manifest, ship the manifest.'
argument-hint: '<manifest-path>'
user-invocable: true
---

Work toward the manifest's Deliverables. Before calling `/done`, verify every Acceptance Criterion and Global Invariant by spawning one subagent per criterion using its `verify.prompt:` verbatim — no rewording. (Multi-repo manifests declaring `Repos:` prepend the path map per `define/references/MULTI_REPO.md`; otherwise nothing wraps the author's prompt.) The optional `verify.agent:` names the subagent type (default: general-purpose); the optional `verify.model:` selects the model. Respect `phase:` ordering — serial across phases, parallel within. Each verifier returns PASS, FAIL, or BLOCKED; all must PASS before `/done`. Any BLOCKED routes via `/escalate`. FAIL bodies carry findings or a natural-language hint — read them and act on what they say.

Code-change fix attempts iterate until they pass or `/do` judges them genuinely unrecoverable → `/escalate`. Other retry shapes (waiting, retriggering, replying with or without resolving, mechanical syncs) aren't fix attempts — they follow the verifier's findings directly. When a hint or finding indicates a reviewer ask beyond the work's intent, route to amendment by invoking `manifest-dev:define` again with the manifest path and the amendment context — `/define` reads "manifest path in args = amend" and applies targeted changes. **When a hint or finding indicates terminal / unrecoverable / human-decision-needed, route to `/escalate` — autonomously amending the manifest to suppress the block is forbidden.**

Mid-/do user messages default to invoking `manifest-dev:define` for amendment — the manifest is the source of truth, silent scope drift is worse than an extra amendment cycle. Pure questions about the manifest or process are answered inline.

**Input.** `<manifest-path>` — required; no args → halt with usage. Read the manifest fully before any execution. Multi-repo manifests (declare `Repos: [name: path, ...]` in Intent) — use absolute paths in tool calls when working in a non-cwd repo.
