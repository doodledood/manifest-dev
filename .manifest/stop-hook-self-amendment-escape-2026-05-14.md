# Definition: Stop-hook Self-Amendment idle-loop escape valve

## 1. Intent & Context

- **Goal:** Fix the infinite idle-loop bug in `stop_do_hook.py`'s Self-Amendment branch by mirroring the existing idle-loop escape valve from the sibling `/do`-unfinished branch. The bug forces the agent into permanent idle blocking after a Self-Amendment escalation + `/define --amend` completion, even when `/do` is correctly waiting on an external blocker (CI, deploy poller, etc.).
- **Mental Model:**
  - Stop hook decision matrix in `claude-plugins/manifest-dev/hooks/stop_do_hook.py` evaluates `parse_do_flow()` state. Two block branches exist: Self-Amendment (lines 62–82, unconditional block — buggy) and `/do`-unfinished (lines 99–113, has `count_consecutive_idle_outputs() >= 3` escape valve — correct).
  - `parse_do_flow()` in `hook_utils.py` only resets `has_self_amendment` on a fresh `/do` invocation (line 345), so the flag stays sticky after `/define --amend` completes and `/do` resumes the same flow.
  - Fix (a) — chosen — mirrors the existing escape-valve idiom into the Self-Amendment branch. Same diagnostic logic, same threshold (3 idle outputs), Self-Amendment-tailored message.
  - The byte-identical `manifest-dev-experimental` hook copy gets the same fix.
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

- **Architecture:**
  - Edit `claude-plugins/manifest-dev/hooks/stop_do_hook.py`: inside the existing `if state.has_self_amendment:` branch (lines 62–82), before constructing the block-output dict, call `count_consecutive_idle_outputs(transcript_path)` and gate on `>= 3` to emit an allow-stop dict with a Self-Amendment-specific systemMessage. The block-output path is preserved unchanged for the non-idle case.
  - Apply the identical edit to `claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py` (verified byte-identical via diff at synthesis time).
  - Tailored systemMessage for the Self-Amendment escape names the actual scenario: the amendment was applied and `/do` is now genuinely idle. It must NOT direct the agent to `/verify` or `/escalate` (those are wrong moves at this point — `/do` is mid-resumption, possibly polling an external blocker, and the user will reinvoke when ready).
  - Test additions in `tests/hooks/test_do_stop_hook.py` inside `TestStopHookLoopDetection`: (1) Self-Amendment + 3 idle outputs → allows stop with idle-loop reasoning; (2) Self-Amendment + 2 idle outputs → still blocks with Self-Amendment reasoning. Mirrors the existing `test_allows_after_three_idle_outputs` / `test_blocks_with_two_idle_outputs` pair.
  - Plugin version bumps: `manifest-dev` 0.110.1 → 0.110.2 (patch — bug fix), `manifest-dev-experimental` 0.9.2 → 0.9.3 (patch — bug fix).
  - Run `/sync-tools` (or equivalent invocation) after the edits land so `dist/{gemini,opencode,codex}/` pick up the regenerated `stop_do_hook.py`. Per `sync-tools/SKILL.md`, only `claude-plugins/manifest-dev/` is synced; `manifest-dev-experimental` has no dist surface.
- **Execution Order:**
  - D1 (hook fix in both plugins) → D2 (tests) → D3 (version bumps) → D4 (sync-tools) → D5 (lint/format/typecheck + hook tests pass)
  - Rationale: code change first so tests can validate it; version bumps and dist sync are bookkeeping that depends on the code being correct; final verification runs over the whole resulting tree.
- **Risk Areas:**
  - [R-1] Self-Amendment-after-`/define --amend`-then-resume flow not exercised by existing tests in a way that distinguishes it from the bare Self-Amendment escalation case — risk of mismodeling what "resumed `/do`" looks like in the transcript. | Detect: confirm new tests build their transcripts from the Self-Amendment escalate skill call plus N text-only assistant outputs (matching the existing idle-loop test shape); confirm `parse_do_flow()` state at hook entry has `has_self_amendment=True` and `has_do=True` after those entries.
  - [R-2] sync-tools delta sync may have stale state and miss the hook change. | Detect: post-sync, diff `dist/gemini/hooks/stop_do_hook.py` against `claude-plugins/manifest-dev/hooks/stop_do_hook.py` for the relevant block — they must agree.
  - [R-3] Existing test `test_blocks_with_self_amendment_escalate` (line 95) asserts blocking after Self-Amendment escalate — the new behavior still blocks in the non-idle case (2 idle outputs or fewer), so this test must keep passing unchanged. | Detect: full `pytest tests/hooks/ -v` after edits.
- **Trade-offs:**
  - [T-1] Mirror existing escape valve (fix a) vs track `/define --amend` completion in `parse_do_flow` (fix b) → Prefer (a) because it preserves the existing idiom, requires zero new state-tracking, and the escape valve correctly handles the actual symptom (idle blocking) without committing to a fuzzy "completion" definition for `/define --amend`.
  - [T-2] Minimal patch vs broader cleanup of stop-hook decision-matrix → Prefer minimal patch — the rest of the decision matrix is functioning correctly; touching it risks regressions in unrelated branches.

## 3. Global Invariants

*CODING.md base gate skips (with reasoning per /define SKILL.md "omit clearly inapplicable with stated reasoning"):*
- *contracts-reviewer skipped: no external/internal API call signatures or public interfaces change; the hook's stdin/stdout JSON protocol with Claude Code is unchanged.*
- *type-safety-reviewer skipped: change is purely local-control-flow in a function already typed; no new types, no `Any` introductions, no type-system surface change.*

- [INV-G1] `pytest tests/hooks/ -v` passes (all existing tests + new Self-Amendment idle-loop tests). | Verify:
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && pytest tests/hooks/ -v"
  ```
- [INV-G2] `ruff check claude-plugins/` reports no issues. | Verify:
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && ruff check claude-plugins/"
  ```
- [INV-G3] `black --check claude-plugins/` reports clean. | Verify:
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && black --check claude-plugins/"
  ```
- [INV-G4] `mypy` typecheck passes. | Verify:
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && mypy"
  ```
- [INV-G5] Existing test `test_blocks_with_self_amendment_escalate` still passes — the non-idle Self-Amendment path must remain blocking. | Verify:
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && pytest tests/hooks/test_do_stop_hook.py::TestStopHookBlocking::test_blocks_with_self_amendment_escalate -v"
  ```
- [INV-G6] `manifest-dev` and `manifest-dev-experimental` hook copies of `stop_do_hook.py` remain byte-identical after the fix. | Verify:
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/claude-plugins/manifest-dev/hooks/stop_do_hook.py /home/user/manifest-dev/claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py"
  ```
- [INV-G7] `dist/gemini/hooks/stop_do_hook.py` reflects the updated source — the Self-Amendment branch carries the new escape valve. Stronger than a count comparison: extracts the function body and verifies the escape-valve token appears within the Self-Amendment block. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import re; src=open('/home/user/manifest-dev/claude-plugins/manifest-dev/hooks/stop_do_hook.py').read(); dst=open('/home/user/manifest-dev/dist/gemini/hooks/stop_do_hook.py').read(); src_blk=re.search(r'has_self_amendment:(.*?)# Non-local medium', src, re.DOTALL).group(1); dst_blk=re.search(r'has_self_amendment:(.*?)# Non-local medium', dst, re.DOTALL).group(1); assert 'consecutive_idle' in src_blk and 'consecutive_idle' in dst_blk, 'Self-Amendment branch missing escape valve in source or dist'; assert src_blk.strip() == dst_blk.strip(), 'Self-Amendment block in source and dist differ'; print('OK')\""
  ```
- [INV-G8] Mechanical bug review: no LOW+ findings on the hook change and the new tests. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: code-bugs-reviewer
    prompt: "Review the diff on claude-plugins/manifest-dev/hooks/stop_do_hook.py, claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py, and tests/hooks/test_do_stop_hook.py vs origin/main. Threshold: no LOW+ findings. Focus areas: correctness of the idle-loop escape mirroring, transcript-shape coverage in new tests (remember Skill calls count as idle per hook_utils.py:272), no regression of the unchanged non-idle Self-Amendment block path."
  ```
- [INV-G9] Intent review: change does what its commit message claims. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff vs origin/main. Intent: add idle-loop escape valve (>=3 consecutive idle outputs → allow stop) to the Self-Amendment branch of stop_do_hook.py, mirroring the existing escape valve in the /do-unfinished branch. Tailored systemMessage for the Self-Amendment case (does NOT direct to /verify or /escalate). Apply to both manifest-dev and manifest-dev-experimental. Threshold: no LOW+ findings."
  ```
- [INV-G10] Test quality review: new tests are validating, not tautological, and exercise the boundary correctly. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: test-quality-reviewer
    prompt: "Review the new Self-Amendment idle-loop test cases added to tests/hooks/test_do_stop_hook.py vs origin/main. Threshold: no MEDIUM+ findings. Check: tests correctly account for the fact that the Self-Amendment Skill call itself counts as idle (hook_utils.py:272), so the transcript builds the idle count from Skill + N text outputs. Confirm the escape fires when total consecutive idle outputs reach 3, blocks when 2."
  ```
- [INV-G11] Maintainability review: new code follows existing patterns, no DRY violations beyond the intentional mirroring. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: code-maintainability-reviewer
    prompt: "Review the diff on claude-plugins/manifest-dev/hooks/stop_do_hook.py and claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py vs origin/main. Threshold: no MEDIUM+ findings. The intentional duplication of the escape-valve idiom between the Self-Amendment branch and the /do-unfinished branch is by design (mirrors existing pattern); flag only DRY violations beyond that."
  ```
- [INV-G12] Design fitness: fix (a) is the right approach given the surrounding code. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: code-design-reviewer
    prompt: "Review the diff on stop_do_hook.py. The change mirrors an existing idle-loop escape valve from the /do-unfinished branch (lines 99-113) into the Self-Amendment branch. Threshold: no MEDIUM+ findings. The alternative — tracking /define --amend completion in parse_do_flow — was considered and rejected per T-1. Validate the chosen approach against the codebase's existing idioms."
  ```
- [INV-G13] CLAUDE.md adherence: change follows project conventions (edits to claude-plugins/, version bumps, hook test discipline). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: context-file-adherence-reviewer
    prompt: "Review the diff vs origin/main against /home/user/manifest-dev/CLAUDE.md. Threshold: no MEDIUM+ findings. Spot-check: edits target claude-plugins/ (not .claude/ symlinks), plugin.json versions bumped per patch/minor/major rules, hook tests run, ruff/black/mypy pipeline respected."
  ```
*INV-G14 removed during /do execution (Self-Amendment): the `github-pr-lifecycle` agent has no GitHub API access in its sandboxed execution env (no `gh` CLI, no `GH_TOKEN`, host IP rate-limited). The PR lifecycle was verified at creation time via the orchestrator's GitHub MCP path (PR #136 exists, opened as ready-for-review, no CI configured to gate). Ongoing CI/review/approval events flow to the user via their PR activity webhook subscription, not through /verify. See ASM-8.*

## 4. Process Guidance

- [PG-1] Run existing tests before modifying test files (`pytest tests/hooks/ -v`) — verify current green baseline so failures are attributable to the change, not pre-existing state.
- [PG-2] Read project gates from CLAUDE.md before final-gate runs — commands canonicalized there are: `ruff check --fix claude-plugins/ && black claude-plugins/ && mypy` and `pytest tests/hooks/ -v`.
- [PG-3] Edit the `claude-plugins/` versions of all hook files (NOT `.claude/` — those are symlinks per CLAUDE.md). Edit both `manifest-dev` and `manifest-dev-experimental` copies since they are independent files, not symlinked to each other.
- [PG-4] Bump patch version in BOTH `claude-plugins/manifest-dev/.claude-plugin/plugin.json` and `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json` per CLAUDE.md versioning rules — this is a bug fix, so patch (0.110.1→0.110.2 and 0.9.2→0.9.3).
- [PG-5] Sync distribution packages by invoking the sync-tools skill (no args = all CLIs). The skill's diff-first flow handles delta vs full sync per CLI and writes back `.sync-meta.json`. After it runs, INV-G7 verifies the Self-Amendment block in dist/gemini matches source.
- [PG-6] Test correctness — Skill calls count as idle per `hook_utils.py:272`, so a transcript of `user_do_command + self_amendment_escalate + N text-only assistant outputs` has consecutive_idle = N+1 at hook entry. Build new test transcripts accordingly: N=2 text outputs → idle=3 → escape fires (allow); N=1 text output → idle=2 → still blocks. The existing `test_blocks_with_self_amendment_escalate` (N=0 → idle=1 → still blocks) remains valid unchanged.
- [PG-7] In `stop_do_hook.py`, place the `count_consecutive_idle_outputs` call INSIDE the existing `if state.has_self_amendment:` branch (do not hoist above it). The existing `/do`-unfinished branch already has its own call; duplicating the call inside Self-Amendment keeps both branches self-contained and avoids reordering the decision matrix.

## 5. Known Assumptions

- [ASM-1] (auto) Plugin version bump strategy: patch-level bump (0.110.1 → 0.110.2; 0.9.2 → 0.9.3). | Default: patch | Impact if wrong: under-bumped if user considers this a minor-level user-visible behavior change; over-bumped if user considers it a no-op release. CLAUDE.md classifies bug fixes as patch, which matches.
- [ASM-2] (auto) Self-Amendment escape-valve systemMessage wording: directs the agent to allow the stop and lets the user resume when the external blocker clears — does NOT direct to `/verify` or `/escalate` (which are wrong moves for the resumed-`/do`-in-wait-state case). Reason field carries the same diagnostic framing as the `/do`-unfinished escape. | Default: chosen wording above | Impact if wrong: minor — message text only, no behavior change.
- [ASM-3] (auto) README updates are out of scope. CLAUDE.md says README-only changes don't require version bumps; the converse — that bug-fix code changes need README sync — applies only when components are added/renamed/removed (not when an existing hook's internal logic changes). | Default: no README edits | Impact if wrong: minor doc lag.
- [ASM-4] (auto) `dist/codex` and `dist/opencode` have no `hooks/` subdirectory at synthesis time (only `dist/gemini/hooks/` exists). The other CLIs use a different distribution shape (skills/agents only, no hook runtime); sync-tools handles each per its reference file. AC-4.2 is scoped to "if present" to accommodate this. | Default: gemini is the only dist target carrying hook copies; codex/opencode hook-less shape is by design | Impact if wrong: if codex or opencode add hook surfaces later, this manifest's verification needs updating; trivially detectable on next sync.
- [ASM-5] (auto) Fix routing: fix (a) — mirror escape valve — over fix (b) — track `/define --amend` completion. Reason: mirrors existing idiom; zero new state. See T-1. | Default: fix (a) | Impact if wrong: fix (b) is the principled alternative; revisit if escape valve produces false positives.
- [ASM-6] (auto) PR body covers root cause + fix + test additions + version bumps + sync. Title is the implementer's call (kept short, descriptive). Marked ready-for-review (not draft) per project convention. | Default: above framing | Impact if wrong: PR title/description tweakable on user feedback.
- [ASM-7] (auto) Bug mechanism is grounded in (a) code reading at hook_utils.py:345 (only-resets-on-new-/do) and stop_do_hook.py:62–82 (unconditional block), and (b) the reporter's first-person repro narrative (pushed amendment, `/define --amend` cleanly completed, /do correctly waiting on Argo build, hook fires "Self-Amendment escalation appears active" every turn). No transcript replay was performed by the implementer; the mechanism is consistent with the code paths and the reporter's observation. | Default: ship without transcript replay — code-reading + reporter's repro covers BUG.md convergence | Impact if wrong: if the actual bug has a different mechanism, fix could miss; mitigated by the new tests, which exercise the exact code path being changed.
- [ASM-8] (auto, amendment) PR lifecycle verification path: PR creation was performed via the orchestrator's GitHub MCP tool (PR #136 created with `draft: false` and a description summarizing the fix). The `github-pr-lifecycle` reviewer agent — which would have provided richer lifecycle gating (CI green, mergeable, threads addressed) — runs in a sandboxed agent env without GitHub API access and cannot complete the check in this run. INV-G14 was removed during /do via Self-Amendment because (i) the criterion as written is unverifiable from this env and (ii) ongoing CI/review events flow to the user via their PR activity webhook subscription, which provides equivalent oversight outside /verify's gate. AC-5.1 still verifies the branch push (the in-scope, locally-verifiable part of PR lifecycle). | Default: removed INV-G14, kept AC-5.1, documented MCP creation path here | Impact if wrong: if a stricter lifecycle gate is needed before /done, re-add INV-G14 once the agent env has GitHub access (e.g., via GH_TOKEN); the rest of the manifest is unaffected.

## 6. Deliverables

### Deliverable 1: Add idle-loop escape valve to Self-Amendment branch in both plugins

**Acceptance Criteria:**

- [AC-1.1] `claude-plugins/manifest-dev/hooks/stop_do_hook.py`'s `if state.has_self_amendment:` branch checks `count_consecutive_idle_outputs(transcript_path)` and, when `>= 3`, emits an allow-stop output (no `decision: "block"` key) with an idle-loop reason and a Self-Amendment-tailored systemMessage. Otherwise the existing block path is preserved unchanged. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/hooks/stop_do_hook.py. Confirm: inside the if state.has_self_amendment block, count_consecutive_idle_outputs(transcript_path) is called BEFORE the unconditional block-output. When the count is >= 3, an output dict without 'decision' key is printed and sys.exit(0) is called. The original block path (with decision='block') is reached only when count < 3. The systemMessage in the new escape path does NOT reference /verify or /escalate."
  ```
- [AC-1.2] `claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py` carries the identical change. | Verify:
  ```yaml
  verify:
    method: bash
    command: "diff /home/user/manifest-dev/claude-plugins/manifest-dev/hooks/stop_do_hook.py /home/user/manifest-dev/claude-plugins/manifest-dev-experimental/hooks/stop_do_hook.py"
  ```
- [AC-1.3] The hook still imports `count_consecutive_idle_outputs` from `hook_utils` (already present at line 24). No changes to `hook_utils.py` — `parse_do_flow` semantics unchanged. | Verify:
  ```yaml
  verify:
    method: bash
    command: "git diff origin/main -- claude-plugins/manifest-dev/hooks/hook_utils.py claude-plugins/manifest-dev-experimental/hooks/hook_utils.py | wc -l"
  ```
  (Expected output: `0` — no diff against origin/main on hook_utils.py.)

### Deliverable 2: Test cases for the new escape valve

*Idle count semantics: Skill calls count as idle (hook_utils.py:272). Transcript `user_do_command + self_amendment_escalate + N text outputs` → consecutive_idle = N+1 at hook entry.*

**Acceptance Criteria:**

- [AC-2.1] New test in `TestStopHookLoopDetection`: transcript = `user_do_command + self_amendment_escalate + 2 text-only assistant outputs` (consecutive_idle = 3) → escape valve fires, result has no `decision` key (allow stop), reason mentions "idle" or "loop". | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open tests/hooks/test_do_stop_hook.py. Confirm a new test in TestStopHookLoopDetection builds a transcript of user_do_command + a Self-Amendment escalate Skill call + exactly 2 text-only assistant outputs (NOT 3 — the Skill call itself counts as idle, so 2 text outputs gives total idle count 3), runs stop_do_hook.py, and asserts: result is not None, 'decision' not in result, 'idle' in result['reason'].lower() or 'loop' in result['reason'].lower()."
  ```
- [AC-2.2] New test in `TestStopHookLoopDetection`: transcript = `user_do_command + self_amendment_escalate + 1 text-only assistant output` (consecutive_idle = 2) → still blocks with Self-Amendment reasoning. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open tests/hooks/test_do_stop_hook.py. Confirm a second new test builds a transcript of user_do_command + a Self-Amendment escalate Skill call + exactly 1 text-only assistant output (total idle count = 2, below threshold), runs the hook, and asserts: result['decision'] == 'block' and 'self-amendment' in result['reason'].lower()."
  ```
- [AC-2.3] The new escape-valve systemMessage is distinguishable from the `/do`-unfinished escape message — it does NOT reference `/verify` or `/escalate` as next steps. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/hooks/stop_do_hook.py. In the new Self-Amendment idle-loop escape branch, confirm the systemMessage does not contain '/verify' or '/escalate'. The message should describe the resumed-/do-in-wait-state case (allow stop, user reinvokes when blocker clears)."
  ```
- [AC-2.4] `pytest tests/hooks/test_do_stop_hook.py -v` runs all tests and they pass. | Verify:
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && pytest tests/hooks/test_do_stop_hook.py -v"
  ```

### Deliverable 3: Plugin version bumps

**Acceptance Criteria:**

- [AC-3.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is `0.110.2`. | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -E '\"version\": \"0\\.110\\.2\"' /home/user/manifest-dev/claude-plugins/manifest-dev/.claude-plugin/plugin.json"
  ```
- [AC-3.2] `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json` version is `0.9.3`. | Verify:
  ```yaml
  verify:
    method: bash
    command: "grep -E '\"version\": \"0\\.9\\.3\"' /home/user/manifest-dev/claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json"
  ```

### Deliverable 4: Distribution sync

**Acceptance Criteria:**

- [AC-4.1] `sync-tools` has been invoked after the source edits — `dist/gemini/hooks/stop_do_hook.py` carries the new idle-loop escape branch inside the Self-Amendment block. Verified by extracting the Self-Amendment block from both source and dist and confirming `consecutive_idle` appears in both AND the blocks match. | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import re; src=open('/home/user/manifest-dev/claude-plugins/manifest-dev/hooks/stop_do_hook.py').read(); dst=open('/home/user/manifest-dev/dist/gemini/hooks/stop_do_hook.py').read(); src_blk=re.search(r'has_self_amendment:(.*?)# Non-local medium', src, re.DOTALL).group(1); dst_blk=re.search(r'has_self_amendment:(.*?)# Non-local medium', dst, re.DOTALL).group(1); assert 'consecutive_idle' in src_blk, 'source missing escape valve in Self-Amendment'; assert 'consecutive_idle' in dst_blk, 'dist/gemini missing escape valve in Self-Amendment'; assert src_blk.strip() == dst_blk.strip(), 'Self-Amendment blocks differ between source and dist/gemini'; print('SYNCED')\""
  ```
- [AC-4.2] If `dist/codex` or `dist/opencode` ship a `hooks/` directory with `stop_do_hook.py` (per ASM-4 currently they do not), those copies also carry the fix. Skipped cleanly when the directories are absent. | Verify:
  ```yaml
  verify:
    method: bash
    command: "ok=1; for d in codex opencode; do f=/home/user/manifest-dev/dist/$d/hooks/stop_do_hook.py; if [ -f \"$f\" ]; then python3 -c \"import re,sys; t=open('$f').read(); blk=re.search(r'has_self_amendment:(.*?)# Non-local medium', t, re.DOTALL); sys.exit(0 if blk and 'consecutive_idle' in blk.group(1) else 1)\" || ok=0; fi; done; [ $ok -eq 1 ] && echo OK"
  ```
- [AC-4.3] Each `dist/{cli}/.sync-meta.json` records the SHA of the most recent commit reachable from HEAD that modified `claude-plugins/manifest-dev/` (project convention — see commit `9ae019e` precedent). Putting HEAD itself inside a file in HEAD is bootstrapping-impossible (content-addressable hash). The historical convention records the source-state SHA, not HEAD. | Verify:
  ```yaml
  verify:
    method: bash
    command: "src_sha=$(git -C /home/user/manifest-dev log -1 --format=%H -- claude-plugins/manifest-dev/); ok=1; for d in codex opencode gemini; do m=/home/user/manifest-dev/dist/$d/.sync-meta.json; [ -f \"$m\" ] || continue; grep -q \"$src_sha\" \"$m\" || ok=0; done; [ $ok -eq 1 ] && echo OK"
  ```

### Deliverable 5: PR opened and ready for review

*PR lifecycle verification consolidated under INV-G14 (single PR for this branch); this deliverable's AC checks the branch push step explicitly so /do treats push as a tracked unit of work.*

**Acceptance Criteria:**

- [AC-5.1] Branch `claude/fix-stop-hook-loop-NsgtD` is pushed to origin with the fix commits. | Verify:
  ```yaml
  verify:
    method: bash
    command: "git -C /home/user/manifest-dev fetch origin claude/fix-stop-hook-loop-NsgtD 2>&1 && git -C /home/user/manifest-dev rev-parse origin/claude/fix-stop-hook-loop-NsgtD && echo PUSHED"
  ```
