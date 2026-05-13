# Definition: Eliminate Session Logs + Introduce /handoff Skill

## 1. Intent & Context

- **Goal:** Remove session-log files (`/tmp/define-discovery-*.md`, `/tmp/do-log-*.md`, /verify pass-log blocks) across the manifest workflow because modern Claude Code / Codex harnesses preserve session state natively. Consolidate the only remaining use case — cross-boundary context handoff — into a single, manually-invoked `/handoff` skill in `manifest-dev-tools`. Also remove the "memento" pattern references from `manifest-dev-tools/prompt-engineering` since its rationale is precisely what this refactor deprecates.
- **Mental Model:** Logs were the memento pattern's externalization. Newer harnesses preserve in-session state, so externalization is only valuable when crossing boundaries (tool switch, fresh session, multi-agent transfer). `/handoff` is the dedicated tool for that crossing — manually invoked, pure-rewrite snapshot of epistemic state (not chronology, not summary).
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

*Initial direction. Adapt where reality diverges.*

- **Architecture:**
  - **`/handoff` skill** lives in `claude-plugins/manifest-dev-tools/skills/handoff/` with `SKILL.md` (1-3 paragraphs per prompt-engineering discipline) + `references/example.md` (doc format example). Output: `/tmp/handoff-{timestamp}.md`. Accepts optional prior-handoff path; pure rewrite to a new timestamp.
  - **`/verify` return contract** replaces the file-append pass-log contract: each invocation returns the same fields (scope, result, failures, auto_triggered_final, deferred) inline as a fenced YAML block in the tool result text. `/do` reads /verify's return turn-by-turn; no shared file.
  - **`/do` and `/define`** drop log-file creation and reading instructions. State (iteration count, scope decisions, deferred-auto coverage history) lives in-context across the conversation.
  - **Hooks**: `posttool_log_hook.py` deleted (sole purpose was log-update reminder). `post_compact_hook.py` and `pretool_verify_hook.py` simplified to manifest-only reminders (no log re-read). `stop_do_hook.py` keeps its core stop-enforcement role, log mention removed. `prompt_submit_hook.py` untouched. Same applies to `manifest-dev-experimental` hooks.
  - **ADR** (tools plugin): execution-log inputs are downgraded from "supplementary" to "no longer available." Manifest + transcript become the primary inputs.
- **Execution Order:**
  - D1 → D7 → D13 → D2 → D3 → D4 → D5 → D6 → D8 → D9 → D10 → D11 → D12
  - Rationale: /handoff (D1) is independent. **Hooks (D7) run second** so hook reminders don't fire mid-implementation with stale "update execution log" reminders during the very /do session that's removing them. **manifest-verifier agent (D13) runs third** — its input contract drops the `Log:` argument, and /define's invocation of it (in D4) must match the new contract; doing D13 before D4 avoids in-flight contract drift. /verify (D2) defines the return contract /do (D3) consumes. /define (D4) and /auto (D5) sit downstream of the /do invocation contract. /done + /escalate (D6) reference both. Memento removal (D8) and ADR adaptation (D9) are independent — could parallelize, sequenced after for safety. Reference files (D10) are the last skill-text pass. Docs sync (D11) covers READMEs, plugin.json versions, CLAUDE.md, and `dist/` regeneration. Pre-PR validation (D12) gates everything.
- **Risk Areas:**
  - [R-1] Log reference left behind in some SKILL.md, reference file, hook, test, or `dist/` copy | Detect: `grep -rE '(tmp/(do-log|define-discovery|manifest-[^ ]*log)|execution log|discovery log|pass log)' claude-plugins/ tests/ CLAUDE.md` returns no actionable matches outside `/handoff` itself
  - [R-2] `/verify` return text not deterministically parseable by `/do` | Detect: /verify SKILL.md explicitly specifies the inline YAML block shape; /do SKILL.md explicitly specifies how to read it; both ends agree on field names
  - [R-3] Deferred-auto coverage tracking breaks because file-aggregation no longer exists | Detect: /verify SKILL.md explicitly notes coverage derivation from conversation context across prior return blocks; /do mirrors the rule
  - [R-4] Hook tests fail after hook deletions/edits | Detect: `pytest tests/hooks/ -v` exit code 0
  - [R-5] `dist/` copies stale → external CLIs run old behavior | Detect: post-edit `sync-tools` invocation regenerates dist/; quick grep on dist/ for the deleted patterns shows zero matches
  - [R-6] `/handoff` symlinks missing in either `.claude/skills/` or `.agents/skills/` → skill not discoverable | Detect: `ls -L .claude/skills/handoff .agents/skills/handoff` resolves to a real directory
  - [R-7] /verify pass-log file (PASS_LOG.md reference in experimental) not deleted → reference rot | Detect: file is removed; no link to it remains
  - [R-8] Long /do session loses prior /verify return blocks from in-context window (harness compaction or simple context-length pressure) → partial deferred-auto coverage map is lost. **Detection:** /verify can't find the expected prior return block in conversation. **Mitigation:** re-running deferred-auto criteria from scratch is always safe — they're idempotent verifiers. The cost is extra verifier-agent time; correctness is preserved. /verify SKILL.md explicitly notes this fallback: when prior return blocks are not visible in-context, re-run all deferred-auto criteria from scratch in the current pass rather than attempting to aggregate. **Trade-off:** runtime cost vs eliminating a stateful ledger file (T-2 already captures this preference).
- **Trade-offs:**
  - [T-1] Comprehensive log removal vs minimal scope → Prefer comprehensive: user's stated reasoning ("logs don't have much utility anymore") applies uniformly; partial removal would leave the system half-aligned, confusing.
  - [T-2] In-context deferred-auto state vs file aggregation → Prefer in-context: matches the refactor's premise (modern harnesses retain context); avoids re-introducing the file-state pattern under a new name.
  - [T-3] Delete obsolete hooks vs keep with edits → Prefer delete for `posttool_log_hook.py` (sole purpose is log reminder); keep and simplify for hooks with other roles (post-compact manifest re-read, pre-tool manifest reminder, stop enforcement).
  - [T-4] /handoff prior-handoff arg as flag vs positional → Prefer optional positional: same shape /do uses for log path; simpler.
  - [T-5] Update PROMPTING.md memento references too vs leave them → Prefer leave: user explicitly scoped memento removal to tools plugin's prompt-engineering. PROMPTING.md memento guidance is task-domain context, not skill methodology; out of scope.

## 3. Global Invariants

- [INV-G1] Change intent achieves stated goal (no behavioral divergence between intent and outcome) | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Audit this branch's changes against the stated intent: remove session log files across the manifest workflow (define/do/verify and downstream skills/hooks/tests/references); introduce /handoff skill in manifest-dev-tools for cross-boundary context transfer; remove memento pattern references from manifest-dev-tools/prompt-engineering. Verify the refactor does what it claims, with no LOW+ findings. Particular gotchas to check: (a) /verify and /do agree on the new return-text contract; (b) deferred-auto coverage logic still works without file aggregation; (c) all log references removed including in reference files, hooks, tests, dist/ copies; (d) /handoff is genuinely a pure-rewrite cross-boundary tool, not a logging tool by another name."
  ```

- [INV-G2] No log-file references remain anywhere in the codebase outside `/handoff` itself | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "set -o pipefail; ! grep -rnEi '(/tmp/(do-log|define-discovery)|do-log-\\{|define-discovery-\\{|execution log|discovery log|pass log|/verify pass \\{N\\}|<log[-_ ]?path>)' claude-plugins/ tests/ CLAUDE.md README.md 2>/dev/null | grep -v -E '(claude-plugins/manifest-dev-tools/skills/handoff/)'"
  ```

- [INV-G3] Linters and type checker pass | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy"
  ```

- [INV-G4] Hook tests pass | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/hooks/ -v"
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only. Touch a file only when this refactor requires it. Don't reformat unrelated content, don't restructure neighboring text, don't rename things for taste.
- [PG-2] Low-arousal tone in all new/edited prompts. No urgency framing, no superlatives, no praise inflation. Match the existing voice of each plugin (manifest-dev is denser; manifest-dev-experimental is radically slim).
- [PG-3] Match existing slim discipline for `manifest-dev-experimental` edits — every word steers or scaffolds; cut scaffold. For `manifest-dev` edits, preserve the existing structure but excise the log-related content surgically.
- [PG-4] When deleting hooks or reference files, also delete their tests and any registration entries (plugin.json hook config, README listings). Don't leave dangling references.
- [PG-5] Apply prompt-engineering's slim discipline to the new `/handoff` SKILL.md — 1-3 short paragraphs, doc-format example pushed to `references/example.md`, no scaffold against in-tool resumption.
- [PG-6] **Deferred-auto coverage parsing precedence** (consumed by /verify and /do): a deferred-auto criterion is "covered" iff some prior `/verify` return block within the current session has `deferred: true`, `result: pass`, and either `scope: []` (full deferred coverage) or `scope:` contains the deliverable that owns the criterion. INV-G* deferred-auto criteria are only covered by a block with `deferred: true` AND `scope: []`. /verify aggregates across all prior return blocks; /do mirrors the rule when deciding whether to invoke `/done`. Both SKILL.md files explicitly encode this rule so the parsing is unambiguous.
- [PG-7] **`/verify` return YAML contract** (consumed by /do, /done, /escalate): each /verify invocation returns a fenced ```yaml block in the tool result text with fields `scope` (list of deliverable IDs or empty for full), `result` (`pass`|`fail`), `failures` (list of criterion IDs, empty when result is pass), `auto_triggered_final` (bool; true only when /verify self-invoked after a preceding true-selective green), `deferred` (bool; master interpretation flag — when true, `result: pass` means deferred-auto green, not the whole manifest). Field names match the prior pass-log block exactly to minimize churn.
- [PG-8] **Long-session deferred-auto fallback**: when /verify can't find a prior return block in conversation context (compaction, context length), it re-runs all in-scope deferred-auto criteria from scratch in the current pass rather than attempting partial aggregation. Idempotent by design; correctness over runtime cost.

## 5. Known Assumptions

- [ASM-1] (auto) Hook deletions and edits are in scope, not just SKILL.md edits | Default: delete `posttool_log_hook.py` + tests; simplify other hooks to remove log refs while preserving other roles | Impact if wrong: hooks still execute with stale log-update reminders even though logs no longer exist — surfaces as user-visible inconsistency; user can request hooks preserved with stronger trim if they object.
- [ASM-2] (auto) ADR skill stays functional in a log-less world by treating manifest + transcript as primary inputs, with log references removed from its docs | Default: edit ADR SKILL.md and ADR_FORMAT.md to drop log-as-input references; ADR continues to work from manifest + transcript | Impact if wrong: if ADR genuinely needs log structure, it produces lower-quality ADRs; the change can be reverted if observed in practice.
- [ASM-3] (auto) `dist/` regeneration happens via the `sync-tools` skill as the doc-sync step | Default: run `sync-tools` after all source edits; do not hand-edit dist/ | Impact if wrong: external CLIs (Codex/Gemini/OpenCode) run old behavior until next regen — surfaces quickly during testing.
- [ASM-4] (auto) Plugin version bumps: minor for `manifest-dev-tools` (new skill), minor for `manifest-dev` and `manifest-dev-experimental` (workflow refactor is more than patch-level) | Default: bump per CLAUDE.md "minor for new features / new skills" guidance | Impact if wrong: semver mismatch on update — easily corrected.
- [ASM-5] (auto) PROMPTING.md (the /define task file) is OUT of scope even though it contains memento references | Default: leave untouched — user scoped memento removal explicitly to prompt-engineering skill in tools plugin | Impact if wrong: stale task guidance lingers; can be cleaned up in a follow-up.
- [ASM-6] (auto) `/verify` return YAML block lives inside the tool result text in a fenced ```yaml block; /do parses by scanning the most recent /verify return | Default: same field names as the prior pass-log block (`scope`, `result`, `failures`, `auto_triggered_final`, `deferred`) preserved for continuity | Impact if wrong: ambiguous parsing surface; can refine the contract during implementation.
- [ASM-7] (auto) Deferred-auto coverage tracking across multiple /verify calls within one /do run is recoverable from conversation context (prior tool results) without file aggregation. If a prior return block has fallen out of context, /verify re-runs the deferred-auto criteria from scratch in the current pass — see R-8 | Default: in-context aggregation works for normal-length sessions; long sessions fall through to re-run, which is correct (deferred-auto criteria are idempotent verifiers) | Impact if wrong: only extra verifier-agent runtime cost on long sessions; correctness preserved.
- [ASM-8] (auto) `/handoff` is user-invocable only; no other skill auto-invokes or even nudges it in their output | Default: `.claude-plugin/plugin.json` and SKILL frontmatter mark `user-invocable: true`; no recommendation lines in /define, /do, /figure-out output | Impact if wrong: if users expect a nudge they may not discover it — discoverable via plugin commands menu.
- [ASM-9] (auto) Branch is `claude/add-figureout-logging-v1Rnk` per session config; manifest is fresh (no amend), no branch-diff seeding needed beyond verifying no prior commits ahead of base during /do | Default: /do verifies branch state; if commits ahead, surfaces and encodes | Impact if wrong: existing work not represented in manifest — surfaces immediately.

## 6. Deliverables

### Deliverable 1: `/handoff` skill in manifest-dev-tools

Create the new skill that produces a cross-boundary context-transfer doc.

**Acceptance Criteria:**

- [AC-1.1] `claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md` exists with valid frontmatter (`name: handoff`, descriptive `description` with What+When+Triggers, `user-invocable: true`) and a body of 1-3 short paragraphs per prompt-engineering discipline | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md && head -1 claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md | grep -q '^---$' && grep -q 'name: handoff' claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md && grep -q 'user-invocable: true' claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md"
  ```
- [AC-1.2] `claude-plugins/manifest-dev-tools/skills/handoff/references/example.md` exists with a complete doc-shape example covering: topic, current read, decisions (with alternatives + why this won), verified facts (with how verified), open threads (with what closes), next move | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-tools/skills/handoff/references/example.md && grep -qiE 'topic|current read|decisions|verified facts|open threads|next move' claude-plugins/manifest-dev-tools/skills/handoff/references/example.md"
  ```
- [AC-1.3] Symlinks created and resolve correctly: `.claude/skills/handoff` → `../../claude-plugins/manifest-dev-tools/skills/handoff`; `.agents/skills/handoff` → `../../.claude/skills/handoff` | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test -L .claude/skills/handoff && test -L .agents/skills/handoff && [ \"$(readlink .claude/skills/handoff)\" = '../../claude-plugins/manifest-dev-tools/skills/handoff' ] && [ \"$(readlink .agents/skills/handoff)\" = '../../.claude/skills/handoff' ] && test -f .claude/skills/handoff/SKILL.md && test -f .agents/skills/handoff/SKILL.md"
  ```
- [AC-1.4] /handoff SKILL.md passes prompt-reviewer | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev-tools/skills/handoff/SKILL.md against prompt-engineering principles. Particular criteria: (a) 1-3 short paragraphs in SKILL.md with the doc-format example offloaded to references/example.md; (b) explicit steers against the model's defaults — not a session summary, not chronology, alternatives-considered are load-bearing, verified-vs-inferred distinction preserved; (c) output path /tmp/handoff-{timestamp}.md with optional prior-handoff path argument for pure-rewrite evolution; (d) no scaffold against in-tool resumption confusion; (e) low-arousal tone, no urgency framing. No MEDIUM+ findings allowed."
  ```

### Deliverable 2: `/verify` log removal + new return contract (both plugins)

Drop the pass-log file contract; specify a return-text contract instead.

**Acceptance Criteria:**

- [AC-2.1] `claude-plugins/manifest-dev/skills/verify/SKILL.md` no longer references log-file appends, `PASS_LOG.md`, "Pass Logging Contract," or `/tmp/do-log-*.md`. Replaces them with explicit "Return Contract" language: each /verify invocation returns a fenced ```yaml block in its tool result with fields `scope`, `result`, `failures`, `auto_triggered_final`, `deferred` plus a brief narrative. /do reads /verify's return text directly. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(Pass Logging Contract|PASS_LOG\\.md|/tmp/do-log|append.*log|## /verify pass \\{N\\})' claude-plugins/manifest-dev/skills/verify/SKILL.md && grep -qE '(Return Contract|tool result|return text)' claude-plugins/manifest-dev/skills/verify/SKILL.md"
  ```
- [AC-2.2] `claude-plugins/manifest-dev-experimental/skills/verify/SKILL.md` similarly cleaned and a return contract specified (slim style, may reference a slim `references/RETURN.md` instead of inline) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(PASS_LOG|/tmp/do-log|append.*log|pass log)' claude-plugins/manifest-dev-experimental/skills/verify/SKILL.md"
  ```
- [AC-2.3] `claude-plugins/manifest-dev-experimental/skills/verify/references/PASS_LOG.md` deleted; no references to it remain anywhere | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! test -f claude-plugins/manifest-dev-experimental/skills/verify/references/PASS_LOG.md && ! grep -rn 'PASS_LOG' claude-plugins/"
  ```
- [AC-2.4] `/verify` SKILL.md (both plugins) prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/verify/SKILL.md and claude-plugins/manifest-dev-experimental/skills/verify/SKILL.md against prompt-engineering principles after the log removal. Particular criteria: (a) /verify's new return contract matches PG-7 exactly (fenced ```yaml block in tool result with fields scope/result/failures/auto_triggered_final/deferred); (b) deferred-auto coverage tracking matches PG-6 exactly (aggregate across all prior return blocks within session, deliverable-scope rules preserved); (c) auto-final after true-selective green still works (rule moves from file-read to context-recall — /verify reads its own prior return text in conversation); (d) no orphan references to deleted files or sections. No MEDIUM+ findings."
  ```

### Deliverable 3: `/do` log removal (both plugins)

Drop execution log creation, reading, and log-path arg.

**Acceptance Criteria:**

- [AC-3.1] `claude-plugins/manifest-dev/skills/do/SKILL.md` no longer references `/tmp/do-log-*.md`, "Execution log," "Log non-trivial events," "Refresh before verify," "Refresh between deliverables," or log-path argument. /do's input contract becomes `<manifest-path> [--scope D1,D2,...]` (with `--mode` per its existing flag). /verify invocation drops the log path. /do reads /verify's return text from the tool result to drive next-pass decisions. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(Execution log|/tmp/do-log|Log non-trivial|Refresh before verify|Refresh between deliverables|log[- ]path)' claude-plugins/manifest-dev/skills/do/SKILL.md"
  ```
- [AC-3.2] `claude-plugins/manifest-dev-experimental/skills/do/SKILL.md` analogously cleaned, preserving its slim style | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(Execution log|/tmp/do-log|<log-path>|log path|log file)' claude-plugins/manifest-dev-experimental/skills/do/SKILL.md"
  ```
- [AC-3.3] /do SKILL.md (both plugins) prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/do/SKILL.md and claude-plugins/manifest-dev-experimental/skills/do/SKILL.md against prompt-engineering principles after log removal. Particular criteria: (a) /verify invocation contract aligns with /verify's new return contract (no log path passed; tool result text parsed for state per PG-7); (b) iteration count and scope decisions tracked in-context across the conversation, explicit in the prompt; (c) deferred-auto handling follows PG-6 (aggregate prior return blocks for coverage); (d) no orphan log references. No MEDIUM+ findings."
  ```

### Deliverable 4: `/define` log removal (both plugins)

Drop discovery log creation, reading, and timestamp pairing.

**Acceptance Criteria:**

- [AC-4.1] `claude-plugins/manifest-dev/skills/define/SKILL.md` no longer references `/tmp/define-discovery-*.md`, "Discovery log" section, "Read the full log before synthesis," `Log:` argument to manifest-verifier, or "log answers to discovery file." Manifest file path stays at `/tmp/manifest-{timestamp}.md`. Synthesis runs from in-context state; manifest-verifier invoked with manifest path only. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(/tmp/define-discovery|Discovery log|define-discovery-\\{|discovery file|Log: /tmp|Read the full log)' claude-plugins/manifest-dev/skills/define/SKILL.md"
  ```
- [AC-4.2] `claude-plugins/manifest-dev-experimental/skills/define/SKILL.md` analogously cleaned in slim style | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(/tmp/define-discovery|discovery log|define-discovery|append-only.*log)' claude-plugins/manifest-dev-experimental/skills/define/SKILL.md"
  ```
- [AC-4.3] /define SKILL.md (both plugins) prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/define/SKILL.md and claude-plugins/manifest-dev-experimental/skills/define/SKILL.md against prompt-engineering principles after discovery log removal. Particular criteria: (a) manifest-verifier invocation no longer passes Log:; (b) coverage-goal convergence logic still coherent without log-as-disposition-tracker (relies on in-context state); (c) Verification Loop description still self-consistent; (d) no orphan references. No MEDIUM+ findings."
  ```

### Deliverable 5: `/auto` log cleanup (both plugins)

Strip log path references in /auto's /define→/do chain.

**Acceptance Criteria:**

- [AC-5.1] `claude-plugins/manifest-dev/skills/auto/SKILL.md` no longer references log paths in /do invocation, deferred-auto reminder, or anywhere | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(log-path|log path|<log>|log file|/tmp/do-log|/tmp/define-discovery)' claude-plugins/manifest-dev/skills/auto/SKILL.md"
  ```
- [AC-5.2] `claude-plugins/manifest-dev-experimental/skills/auto/SKILL.md` similarly cleaned | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(log-path|<log>|log file|/tmp/do-log|/tmp/define-discovery)' claude-plugins/manifest-dev-experimental/skills/auto/SKILL.md"
  ```
- [AC-5.3] /auto SKILL.md prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/auto/SKILL.md and claude-plugins/manifest-dev-experimental/skills/auto/SKILL.md after log path removal. Particular criteria: (a) /do invocation no longer takes a log positional argument; (b) deferred-auto reminder is rephrased without log file mention; (c) failure handling still coherent. No MEDIUM+ findings."
  ```

### Deliverable 6: `/done` and `/escalate` log cleanup

Remove log references in completion-and-escalation paths.

**Acceptance Criteria:**

- [AC-6.1] `claude-plugins/manifest-dev/skills/done/SKILL.md` no longer reads or references an execution log; /do re-invocation in re-execute step drops `<log-path>` | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(execution log|<log-path>|<log>|log file|/tmp/do-log)' claude-plugins/manifest-dev/skills/done/SKILL.md"
  ```
- [AC-6.2] `claude-plugins/manifest-dev/skills/escalate/SKILL.md` drops "Execution log path" field, log arguments in /verify and /do invocations, and re-execute log references | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(Execution log path|<log>|<log-path>|<execution-log-path>|/tmp/do-log)' claude-plugins/manifest-dev/skills/escalate/SKILL.md"
  ```
- [AC-6.3] `claude-plugins/manifest-dev-experimental/skills/done/SKILL.md` and `claude-plugins/manifest-dev-experimental/skills/escalate/SKILL.md` analogously cleaned | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(<log>|<log-path>|/tmp/do-log|execution log)' claude-plugins/manifest-dev-experimental/skills/done/SKILL.md claude-plugins/manifest-dev-experimental/skills/escalate/SKILL.md"
  ```
- [AC-6.4] /done + /escalate (both plugins) prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/skills/done/SKILL.md, claude-plugins/manifest-dev/skills/escalate/SKILL.md, claude-plugins/manifest-dev-experimental/skills/done/SKILL.md, claude-plugins/manifest-dev-experimental/skills/escalate/SKILL.md after log removal. Verify: (a) re-entry / re-execute contracts coherent without log path; (b) post-completion two-step chain still consistent; (c) escalation templates self-consistent. No MEDIUM+ findings."
  ```

### Deliverable 7: Hooks + tests cleanup (both plugins)

Delete log-only hooks, simplify others, update tests and plugin.json registrations.

**Acceptance Criteria:**

- [AC-7.1] `posttool_log_hook.py` deleted from both `claude-plugins/manifest-dev/hooks/` and `claude-plugins/manifest-dev-experimental/hooks/`; corresponding test `tests/hooks/test_posttool_log_hook.py` deleted; PostToolUse hook entries for it removed from both `plugin.json` files. Since deleting all three PostToolUse registrations leaves no entries, the `"PostToolUse"` key is removed from both plugin.json files entirely (not left as `"PostToolUse": []`) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! test -f claude-plugins/manifest-dev/hooks/posttool_log_hook.py && ! test -f claude-plugins/manifest-dev-experimental/hooks/posttool_log_hook.py && ! test -f tests/hooks/test_posttool_log_hook.py && ! grep -q posttool_log_hook claude-plugins/manifest-dev/.claude-plugin/plugin.json claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json && ! grep -q PostToolUse claude-plugins/manifest-dev/.claude-plugin/plugin.json claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json"
  ```
- [AC-7.2] `post_compact_hook.py` and `pretool_verify_hook.py` (both plugins) keep their manifest-related reminder logic but no longer reference execution logs or instruct re-reading log files | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(execution log|/tmp/do-log|do-log-|discovery log|/tmp/define-discovery)' claude-plugins/manifest-dev/hooks/post_compact_hook.py claude-plugins/manifest-dev/hooks/pretool_verify_hook.py claude-plugins/manifest-dev-experimental/hooks/post_compact_hook.py claude-plugins/manifest-dev-experimental/hooks/pretool_verify_hook.py"
  ```
- [AC-7.3] `stop_do_hook.py` (both plugins) message text no longer mentions execution-log path; core stop-enforcement behavior preserved | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(execution log|<log-path>)' claude-plugins/manifest-dev/hooks/stop_do_hook.py claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py"
  ```
- [AC-7.4] `tests/hooks/test_hook_integration.py` fixture strings updated to drop the `/tmp/do-log.md` positional argument from `user_do()` invocations (lines 61, 318, 324, 352, 400, 661 in current file) since /do's input contract drops the log positional. Test assertions remain functionally equivalent; only the invocation strings change | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(/tmp/do-log|do-log\\.md)' tests/hooks/test_hook_integration.py"
  ```
- [AC-7.5] `plugin.json` hook description strings in both plugins no longer mention "execution log" — the surviving PreToolUse / Stop / UserPromptSubmit / SessionStart hook descriptions are rewritten to reflect their non-log responsibilities (e.g., "Remind to read the manifest before verification"). | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(execution log|update.*log|track.*log)' claude-plugins/manifest-dev/.claude-plugin/plugin.json claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json"
  ```
- [AC-7.6] All remaining hook tests pass: `pytest tests/hooks/ -v` exits 0 | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/hooks/ -v"
  ```
- [AC-7.7] Hook code review: edits to `post_compact_hook.py`, `pretool_verify_hook.py`, `stop_do_hook.py` (both plugins) reviewed for regressions in their preserved (non-log) responsibilities | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: code-bugs-reviewer
    model: inherit
    prompt: "Review the diff for these hook files across both plugins (manifest-dev and manifest-dev-experimental): post_compact_hook.py, pretool_verify_hook.py, stop_do_hook.py. The intent: remove all references to the execution log / discovery log, but preserve every other responsibility. Check for: (a) hook still detects active /do or /define workflow correctly; (b) reminder messages still inject when expected; (c) stop_do_hook still enforces /done or /escalate before stop; (d) no regressions in transcript parsing via hook_utils.parse_do_flow(); (e) fail-open behavior preserved. No code-defect findings expected."
  ```

### Deliverable 8: Memento removal from prompt-engineering (manifest-dev-tools)

Strip memento-pattern references from the prompt-engineering skill.

**Acceptance Criteria:**

- [AC-8.1] `claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/review-checklist.md` no longer mentions "memento" in any form; surrounding text reads coherently | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -in memento claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/review-checklist.md"
  ```
- [AC-8.2] No new orphan references to memento elsewhere in the tools plugin's prompt-engineering skill (SKILL.md, other references) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -rin memento claude-plugins/manifest-dev-tools/skills/prompt-engineering/"
  ```
- [AC-8.3] prompt-engineering review-checklist.md passes prompt-reviewer | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/review-checklist.md after memento references were removed. Particular criteria: (a) surrounding sentences still read coherently — no dangling 'and X' phrasings; (b) the rigid-checklist exemption row makes sense without the parenthetical example; (c) anti-pattern example for over-engineering doesn't lose its punch. No MEDIUM+ findings."
  ```

### Deliverable 9: ADR skill adaptation to log-less inputs (manifest-dev-tools)

Adapt ADR to operate without execution-log inputs.

**Acceptance Criteria:**

- [AC-9.1] `claude-plugins/manifest-dev-tools/skills/adr/SKILL.md` no longer references execution logs as inputs; input contract becomes transcript + manifest (optionally manifest-only) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(execution log|/do.*log|<log-path>|do-log-|discovery/execution log)' claude-plugins/manifest-dev-tools/skills/adr/SKILL.md"
  ```
- [AC-9.2] `claude-plugins/manifest-dev-tools/skills/adr/references/ADR_FORMAT.md` no longer references execution-log signals; equivalent signals derived from transcript / manifest Approach noted | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(execution log|from execution logs)' claude-plugins/manifest-dev-tools/skills/adr/references/ADR_FORMAT.md"
  ```
- [AC-9.3] ADR skill prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev-tools/skills/adr/SKILL.md and references/ADR_FORMAT.md after execution-log inputs removed. Verify: (a) input contract clear (transcript + manifest); (b) decision-extraction signals still derivable without logs; (c) no orphan references; (d) graceful behavior when only one input is available. No MEDIUM+ findings."
  ```

### Deliverable 10: Reference files cleanup (all affected plugins)

Strip log references from define/do/verify reference files across both plugins.

**Acceptance Criteria:**

- [AC-10.1] All affected reference files no longer carry log-file mentions; surrounding prose coherent. Files: `claude-plugins/manifest-dev/skills/define/references/*.md`, `claude-plugins/manifest-dev/skills/define/tasks/**/*.md`, `claude-plugins/manifest-dev/skills/do/references/*.md`, `claude-plugins/manifest-dev/skills/figure-out/SKILL.md`, `claude-plugins/manifest-dev-experimental/skills/define/references/*.md`, `claude-plugins/manifest-dev-experimental/skills/define/tasks/**/*.md`, `claude-plugins/manifest-dev-experimental/skills/do/references/*.md`, `claude-plugins/manifest-dev-experimental/skills/verify/references/*.md`, `claude-plugins/manifest-dev-experimental/skills/figure-out/references/*.md`, and `claude-plugins/manifest-dev-experimental/skills/figure-out/SKILL.md`. The figure-out reference files specifically get prose rewrites where they conditionally reference a discovery log that no longer exists (e.g., `experimental/skills/figure-out/references/autonomous.md` line 26). | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -rniE '(/tmp/(do-log|define-discovery)|do-log-\\{|define-discovery-\\{|execution log|discovery log|pass log|<log-path>|<log>|/verify pass \\{)' claude-plugins/manifest-dev/skills/define/references/ claude-plugins/manifest-dev/skills/define/tasks/ claude-plugins/manifest-dev/skills/do/references/ claude-plugins/manifest-dev/skills/figure-out/ claude-plugins/manifest-dev-experimental/skills/define/references/ claude-plugins/manifest-dev-experimental/skills/define/tasks/ claude-plugins/manifest-dev-experimental/skills/do/references/ claude-plugins/manifest-dev-experimental/skills/verify/references/ claude-plugins/manifest-dev-experimental/skills/figure-out/ 2>/dev/null"
  ```
- [AC-10.2] `WRITING-REFERENCE.md` carries no actual log-file references after filtering false-positives (substrings of blog, logical, dialogue, etc.) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(execution log|discovery log|pass log|/tmp/(do-log|define-discovery)|<log-path>|<log>)' claude-plugins/manifest-dev/skills/define/references/WRITING-REFERENCE.md 2>/dev/null"
  ```
- [AC-10.3] No orphan grep matches for log file patterns across all reference directories | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -rniE '(/tmp/(do-log|define-discovery)|do-log-\\{|define-discovery-\\{)' claude-plugins/ 2>/dev/null"
  ```
- [AC-10.4] Figure-out reference files prompt-reviewer pass (rewrite, not just grep-delete) | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev-experimental/skills/figure-out/references/autonomous.md (and any other figure-out reference files touched). Particular criteria: (a) any sentence that previously conditionally referenced a discovery log has been rewritten coherently (not just deleted leaving an orphan fragment); (b) the surrounding flow makes sense end-to-end; (c) low-arousal tone preserved. No MEDIUM+ findings."
  ```

### Deliverable 11: Documentation sync (READMEs, plugin versions, CLAUDE.md, dist/)

Apply CLAUDE.md sync checklist.

**Acceptance Criteria:**

- [AC-11.1] Plugin versions bumped: `manifest-dev-tools` minor (0.3.0 → 0.4.0 — new /handoff skill), `manifest-dev` minor (0.108.0 → 0.109.0 — workflow refactor), `manifest-dev-experimental` minor (0.8.0 → 0.9.0 — workflow refactor) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -q '\"version\": \"0.4.' claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json && grep -q '\"version\": \"0.109.' claude-plugins/manifest-dev/.claude-plugin/plugin.json && grep -q '\"version\": \"0.9.' claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json"
  ```
- [AC-11.2] READMEs list /handoff in the manifest-dev-tools plugin entry: root `README.md`, `claude-plugins/README.md`, `claude-plugins/manifest-dev-tools/README.md` | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -l handoff README.md claude-plugins/README.md claude-plugins/manifest-dev-tools/README.md | wc -l | grep -q 3"
  ```
- [AC-11.3] CLAUDE.md's "Manifest Archival" section no longer states "Discovery logs and execution logs stay in /tmp/" (or any other log-related claim); references to logs throughout CLAUDE.md cleaned | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -nE '(discovery log|execution log|/tmp/(do-log|define-discovery))' CLAUDE.md"
  ```
- [AC-11.4] `dist/` regenerated via `sync-tools` skill for the codex/gemini/opencode targets it generates; resulting dist/ trees contain no log-file references | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -rniE '(/tmp/(do-log|define-discovery)|execution log|discovery log|pass log)' dist/codex/ dist/gemini/ dist/opencode/ 2>/dev/null"
  ```
- [AC-11.5] All READMEs (root, `claude-plugins/README.md`, both manifest-dev plugin READMEs) no longer reference execution log / discovery log; the hook-table descriptions in `claude-plugins/manifest-dev/README.md` and `claude-plugins/manifest-dev-experimental/README.md` are updated to reflect the post-refactor hook responsibilities (no `posttool_log_hook.py`, simplified post_compact / pretool_verify descriptions) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(execution log|update.*log|track.*log|discovery log|posttool_log_hook)' README.md claude-plugins/README.md claude-plugins/manifest-dev/README.md claude-plugins/manifest-dev-experimental/README.md"
  ```

### Deliverable 12: Pre-PR validation

Run CLAUDE.md pre-PR checks.

**Acceptance Criteria:**

- [AC-12.1] ruff + black + mypy pass | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy"
  ```
- [AC-12.2] Hook tests pass | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/hooks/ -v"
  ```

### Deliverable 13: `manifest-verifier` agent log adaptation

The `manifest-verifier` agent at `claude-plugins/manifest-dev/agents/manifest-verifier.md` carries log-dependent contract (input format `Manifest: <path> | Log: <path>`, principles phrased as "Log shows X" / "Discovery log opens threads Y" — 20+ references). Adapt to log-less world: input contract becomes `Manifest: <path>` only; principles rephrased to read from in-context state ("the conversation shows X" / "open threads in the synthesis have not reached disposition").

**Acceptance Criteria:**

- [AC-13.1] Agent input format updated: `Manifest: <path>` only (no `Log:` argument); the CONTINUE-on-missing-input clause references the manifest only; the YAML frontmatter `description:` field contains no log references | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(\\| Log:|/tmp/(do-log|define-discovery)|<log-path>|discovery log|execution log)' claude-plugins/manifest-dev/agents/manifest-verifier.md && grep -q 'Input format:' claude-plugins/manifest-dev/agents/manifest-verifier.md"
  ```
- [AC-13.2] Principles no longer reference the discovery log; phrasings like "Log shows…", "in the log narrative", "logged in discovery" are rewritten to read from in-context state (e.g., "the conversation shows…", "in the synthesis trail"). Note: phrases like "logged as ASM" remain valid manifest vocabulary — only discovery-log references are excised | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -niE '(log shows|log narrative|log opens|log fails|logged in [a-z]+ log|surface[d]? in [a-z]+ log|in the log|in [a-z]+ log narrative)' claude-plugins/manifest-dev/agents/manifest-verifier.md"
  ```
- [AC-13.3] manifest-verifier prompt-reviewer pass | Verify: subagent
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review claude-plugins/manifest-dev/agents/manifest-verifier.md after the log-dependent input/principles were rewritten. Particular criteria: (a) input contract is unambiguous (Manifest path only); (b) gap-detection principles still cover the same failure modes but phrased against in-context synthesis state; (c) no orphan or dangling clauses where 'log' references were excised; (d) low-arousal tone preserved. No MEDIUM+ findings."
  ```
