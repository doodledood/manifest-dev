# Definition: /drive — CI auto-retrigger + 15m default interval

## 1. Intent & Context

- **Goal:** Close two gaps surfaced by a real `/drive` run: (a) confidently-flaky CI was correctly triaged but not auto-retriggered, forcing user intervention; (b) default 30m interval is coarser than needed given how fast most ticks complete.
- **Mental Model:** `/drive` = thin wrapper (`drive/SKILL.md`) that kicks off `/loop` → `/drive-tick`. CI handling lives in the platform adapter (`drive/references/platforms/github.md`). Retrigger cap is tracked via memento counting in the execution log (same pattern as budget check and amendment-loop guard).
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

- **Architecture:** Surgical edits to existing sections. No new top-level sections, no new adapter contracts.
  - `drive/SKILL.md` — `--interval` default/min, error message, `Interval/TTL coupling` gotcha.
  - `drive-tick/SKILL.md` — lock TTL gotcha wording (TTL unchanged at 30m; correct the interval-coupling statement).
  - `github.md` — expand `## CI Failure Triage` with retrigger method order, retrigger cap, log entry format.
  - `plugin.json` — version bump 0.1.0 → 0.2.0.
  - `README.md` — sync flags table + Gotchas.

- **Execution Order:**
  - D1 → D2 → D3 → D4 → D5
  - Rationale: Content changes (D1-D3) first so the README sync (D4) reflects final wording; version bump (D5) last.

- **Risk Areas:**
  - [R-1] Retrigger logic accidentally fires on code-caused failures | Detect: change-intent-reviewer flags the triage condition; AC-1.2 requires explicit "confidently triaged as flaky/infrastructure" gate.
  - [R-2] Cap tracking drifts (tick resets, log format changes) | Detect: AC-1.4 specifies the exact log-entry header the tick counts against.
  - [R-3] Interval/TTL wording now underspecifies the actual race condition | Detect: AC-2.3 requires the new gotcha to name tick duration as the real constraint.

- **Trade-offs:**
  - [T-1] Narrow edits vs restructuring CI triage section → Prefer narrow because the existing §CI Failure Triage already has the right shape; retrigger method + cap slot in cleanly.
  - [T-2] Lower lock TTL alongside interval vs keep lock TTL → Prefer keep because lock TTL governs crash-recovery semantics (stale-lock reclaim window), which is out of scope for this change.

## 3. Global Invariants

- [INV-G1] change-intent-reviewer: no LOW+ findings. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the changes on the current branch against the stated intent: (1) add auto-retrigger for confidently-flaky CI via native check-run rerun or empty commit, capped at 10 retriggers per run, tracked in the execution log; (2) change --interval default from 30m to 15m and min from 30m to 15m. Flag any behavioral divergence between stated intent and edits in claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md, skills/drive-tick/SKILL.md, skills/drive/references/platforms/github.md, .claude-plugin/plugin.json, and README.md."
  ```

- [INV-G2] prompt-reviewer: no MEDIUM+ findings across edited skill files. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the modified prompt sections in claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md, skills/drive-tick/SKILL.md, and skills/drive/references/platforms/github.md. Apply the prompt-engineering skill principles. Focus on: clarity of the new CI retrigger rules, consistency between the interval default and the retained lock-TTL language, structure (no buried critical info), no anti-patterns."
  ```

## 4. Process Guidance

- [PG-1] Keep edits surgical — no restructuring beyond the two targeted behaviors. (auto, from PROMPTING Defaults)
- [PG-2] High-signal changes only — every diff line must serve one of the two behaviors or the README sync. (auto, from PROMPTING Defaults)
- [PG-3] Preserve existing "trusted advisor" tone — no urgency language in the new retrigger rules. (auto, from PROMPTING Defaults)
- [PG-4] Edit the `claude-plugins/` source files. The `.claude/` counterparts are hardlinked and inherit changes automatically (per project CLAUDE.md).

## 5. Known Assumptions

- [ASM-1] Retrigger cap = 10 per run, where "run" means "per execution-log-file lifetime" (github-mode run-ids are deterministic per PR, so the log persists across re-invocations unless the user manually truncates prior `### CI Retrigger` entries or deletes the log). Default: 10 (user-specified — higher than Amendment Loop Guard's 3 because CI flakiness can genuinely recur many times in a long run while still being transient). Impact if wrong: either too many wasted retriggers (lower) or premature escalation on genuinely flaky CI (raise). Doc-level clarification of "run" semantics is encoded in github.md §Per-run cap.
- [ASM-2] Lock TTL remains 30m. Default: unchanged. Impact if wrong: users wanting stricter "one active tick at a time" guarantee at 15m cadence would need lock TTL lowered too; that changes crash-recovery semantics.
- [ASM-3] Empty-commit message = `chore: retrigger CI [drive]`. Default: this format. Impact if wrong: external tooling filtering commit prefixes may need this adjusted.

## 6. Deliverables

### Deliverable 1: CI auto-retrigger in github platform adapter

File: `claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md` (§ CI Failure Triage)

**Acceptance Criteria:**

- [AC-1.1] The `## CI Failure Triage` section instructs the tick to auto-retrigger when a failure is confidently triaged as Infrastructure (flaky timeout, runner outage, transient network error) OR confidently triaged as Pre-existing-but-flaking-on-rerun. Two retrigger methods are documented, in order: (a) native check-run rerun via `mcp__github__*` for GitHub Actions runs; (b) empty-commit push (`git commit --allow-empty -m 'chore: retrigger CI [drive]'` then `git push`) for external status checks (Argo, CircleCI, Jenkins, Buildkite, etc.) that only react to push events. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md §CI Failure Triage. Confirm: (1) both retrigger methods documented; (2) native check-run rerun listed first for GitHub Actions runs; (3) empty-commit push documented as the fallback for external status checks with an example command including 'chore: retrigger CI [drive]'."
  ```

- [AC-1.2] The section explicitly gates retrigger on CONFIDENT flaky/infrastructure classification. Code-caused failures (new failure introduced by commits in this PR) are never retriggered — they remain actionable. Uncertain classifications do NOT trigger an empty-commit retrigger; they escalate via sink instead (new code `CI_UNCERTAIN`). | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md §CI Failure Triage. Confirm the retrigger rule names 'confident' (or equivalent) as the gate, lists code-caused as never-retrigger, and routes uncertain classifications to sink escalation rather than retrigger."
  ```

- [AC-1.3] Per-run cap of 10 CI retriggers is documented. Count is derived by counting `### CI Retrigger` entries in the execution log (memento pattern, consistent with budget-check and amendment-loop-guard counting). When the count reaches 10, the tick escalates via sink with code `CI_RETRIGGER_EXHAUSTED` instead of retriggering. External input (new commit from user, new push from CI fix) does NOT reset the counter — the cap is per-run, not per-external-signal. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md §CI Failure Triage. Confirm: (1) cap is stated as 10 retriggers per run; (2) count method is 'count ### CI Retrigger entries in execution log'; (3) the escalation code is CI_RETRIGGER_EXHAUSTED; (4) the cap is explicitly per-run (not reset by external input)."
  ```

- [AC-1.4] The log-entry format for retriggers is specified as `### CI Retrigger — <method: check-run-rerun | empty-commit> (count: N/10)` with timestamp and the failing check name(s) triggering it. This format is what the tick writes AND what the cap-counter reads against. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md §CI Failure Triage. Confirm the log-entry template header is exactly '### CI Retrigger — <method> (count: N/10)' (or near-identical wording) and that the tick must emit this entry before/alongside the retrigger action."
  ```

### Deliverable 2: Interval default 15m in drive wrapper + drive-tick gotcha

Files: `claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md`, `claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md`

**Acceptance Criteria:**

- [AC-2.1] `drive/SKILL.md` `--interval` documentation states default `15m`, range `15m`–`24h` inclusive, and the rationale correctly identifies tick duration (not interval) as the parallelization constraint. The "minimum matches lock TTL" language is removed or rewritten. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md §Input. Confirm --interval default is 15m, range is 15m-24h, and the rationale names tick duration (or 'a tick running longer than the lock TTL') as the race condition — not 'interval shorter than lock TTL'."
  ```

- [AC-2.2] The usage error message for out-of-range `--interval` reflects the new range: "Interval '<value>' out of range. Must be between 15m and 24h." | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -F 'Must be between 15m and 24h' /Users/aviram.kofman/Documents/Projects/manifest-dev/claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md"
  ```

- [AC-2.3] `drive/SKILL.md` Gotchas §Interval/TTL coupling is rewritten to state that the lock TTL (30m) is the parallelization ceiling — not the interval. Any mention of `--interval ≥ 30m` is removed. Replacement wording notes that a tick running longer than the 30m lock TTL can still parallelize with a fresh cron fire (accepted v0 limit); interval now has no coupling role. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md §Gotchas. Confirm the Interval/TTL gotcha does not state '--interval ≥ 30m' and correctly names tick duration > 30m lock TTL as the race condition. The gotcha still acknowledges this as an accepted v0 limit."
  ```

- [AC-2.4] `drive-tick/SKILL.md` §Concurrency Guard still documents lock TTL = 30m (unchanged). The sentence that claims the lock TTL is "mirrored by /drive's --interval ≥ 30m validation" is rewritten to remove the mirror claim — the TTL stands alone. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md §Concurrency Guard. Confirm (1) lock TTL = 30 minutes is still present, (2) the 'mirrored by /drive's --interval ≥ 30m validation' language is removed, (3) race-condition framing attributes the risk to tick duration exceeding lock TTL, independent of interval."
  ```

- [AC-2.5] `drive-tick/SKILL.md` §Gotchas §Lock TTL mismatch parallelizes ticks is updated: remove the claim that /drive enforces `--interval ≥ 30m`; retain the substantive race-condition description (tick exceeds 30m → next cron fire may acquire stale lock). | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md §Gotchas. Confirm the lock-TTL-mismatch gotcha no longer asserts '--interval ≥ 30m' is enforced; tick-duration-based race-condition description remains."
  ```

### Deliverable 3: Plugin version bump

File: `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json`

**Acceptance Criteria:**

- [AC-3.1] Version bumped from `0.1.0` to `0.2.0` (minor — new feature). | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -E '\"version\": \"0\\.2\\.0\"' /Users/aviram.kofman/Documents/Projects/manifest-dev/claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json"
  ```

### Deliverable 4: README sync

File: `claude-plugins/manifest-dev-experimental/README.md`

**Acceptance Criteria:**

- [AC-4.1] Flags table row for `--interval` reflects new default `15m` and new minimum `15m`. The existing descriptive notes about the race condition are updated to match the SKILL.md Gotcha wording. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md §Quick usage flags table. Confirm the --interval row shows default 15m and a minimum of 15m (not 30m). The descriptive note about parallel ticks attributes the risk to tick duration > lock TTL, not to --interval < lock TTL."
  ```

- [AC-4.2] README §Gotchas "Long ticks (>30m) risk parallel execution" is retained in substance but rewritten so the mitigation claim no longer points to `--interval` being bounded ≥ 30m. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md §Gotchas. Confirm the long-ticks gotcha does not claim --interval is bounded ≥ 30m as the mitigation; the race-condition description itself is preserved."
  ```

### Deliverable 5: Root repo README sync (if references change)

File: `/Users/aviram.kofman/Documents/Projects/manifest-dev/README.md` and `claude-plugins/README.md`

**Acceptance Criteria:**

- [AC-5.1] If either README references `--interval` defaults, CI retrigger behavior, or plugin version, they are updated to match. If neither references those items, no change. | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -H -E 'interval|retrigger|manifest-dev-experimental.*0\\.' /Users/aviram.kofman/Documents/Projects/manifest-dev/README.md /Users/aviram.kofman/Documents/Projects/manifest-dev/claude-plugins/README.md 2>/dev/null || echo 'no references found — no sync needed'"
  ```
