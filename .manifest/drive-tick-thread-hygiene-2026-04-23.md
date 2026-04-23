# Definition: Fix drive-tick bot thread resolution (FP replies + separation of thread hygiene)

## 1. Intent & Context

- **Goal:** Decouple thread hygiene from comment handling in the github platform adapter so that bot threads get resolved after they're addressed — including on FP-reply-only ticks where no code changes. Comment handling stays focused on classification + reply; thread hygiene runs every tick as its own concern.
- **Mental Model:**
  - **Bug moment**: On a /drive tick where Inbox Handling only produces FP replies (no /do code change, no CI retrigger), `drive-tick` invokes the `github` adapter's `Write Outputs` contract. That contract's body is gated at the top on "After any code change:" — no code change → entire contract is a no-op → step 6 (thread resolution) never executes → bot thread remains unresolved on GitHub.
  - **Secondary failure**: Even when code does change, step 6 ("resolve bot threads addressed this tick") sits inside the "After any code change:" frame, so "addressed" reads as "addressed by this commit" — FP-reply-only siblings are excluded in the narrow read.
  - **Spec contradiction**: `drive-tick/SKILL.md` §P Tend PR claims thread resolution runs every tick; the adapter's gate breaks that claim.
  - **Fix model**: Inbox Handling stays about comment replies (per-comment; every comment gets a reply regardless of classification or source). Thread hygiene becomes its own adapter contract that runs every tick, resolves bot/non-human threads that have been addressed, and never touches human threads.
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

- **Architecture:**
  - Add a new `## Thread Hygiene` section to `claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md`, positioned after `## CI Failure Triage` and before `## Write Outputs`. It defines the contract: when to run (every tick), what state to read (per-thread disposition from Inbox Handling + post-commit signal), resolve rules per classification, and the no-op for human threads.
  - Remove `Thread resolution` (step 6) from `## Write Outputs` — it no longer belongs there.
  - Move `### Thread resolution rules` out of `## Inbox Handling` and into the new `## Thread Hygiene` section (or cross-link). `## Inbox Handling` keeps classification + reply + amendment routing only.
  - Update `claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md` §P (Tend PR): rename/restructure so Tend PR invokes two distinct adapter contracts — Write Outputs (gated on code change; commit/push/description-sync/inbox-follow-up-replies) and Thread Hygiene (every tick). The current single invocation becomes two, with distinct gating per contract.
  - `drive/SKILL.md` `ADAPTER_CONTRACT.md` reference list: add `Thread Hygiene` to the github adapter's contract surface if that reference file enumerates contracts.

- **Execution Order:**
  - D1 → D2 → D3 → D4
  - Rationale: add the new §Thread Hygiene section first (D1) so D2/D3 can reference it when removing old content. D4 (drive-tick + adapter contract) sits last because it depends on the adapter side being final.

- **Risk Areas:**
  - [R-1] Regression on code-change ticks — the existing working case (Tick 2 in the uniclient#2321 log resolved the actionable-fix thread correctly, i.e., before this edit) must keep working. Detect: prompt-reviewer + explicit scenario enumeration AC listing FP-only, FP+fix, actionable-only, uncertain-only, human-only ticks.
  - [R-2] Drift between `drive-tick/SKILL.md` §P and the adapter's exposed contracts — if the new contract name/invocation doesn't match, the tick silently skips hygiene. Detect: cross-file consistency check AC.
  - [R-3] Actionable-signal plumbing — Thread Hygiene needs to know "this Actionable thread has a fix committed." If the signal is vague, hygiene either over-resolves (resolves before fix lands) or under-resolves (never resolves). Detect: scenario AC covering the actionable → fix → post-commit-reply → resolve sequence.
  - [R-4] Stale-thread escalation dead-code — the existing §Stale thread escalation mentions "a fixed thread remains unresolved past that window" for bot threads. If hygiene now resolves aggressively, that branch becomes unreachable for bot threads. Acceptable (human-fix threads still use it) but must be documented.

- **Trade-offs:**
  - [T-1] Separate §Thread Hygiene step vs inline-in-Inbox-Handling → Prefer separate because the user explicitly called for decoupling comment handling from thread-state hygiene. Separation also makes the "runs every tick" gating explicit at the section level instead of sprinkled through comment-intent branches.
  - [T-2] Resolve-at-reply-time (cheap) vs resolve-after-fix-commits (correct) → Prefer resolve-after-fix-commits for Actionable (user-chosen). For FP the reply IS the fix, so resolve-at-reply-time is correct there.
  - [T-3] Small-edit vs structural-restructure → Prefer small-edit per PG — we are adding one new section + removing one step + a cross-link move. No restructuring of CI triage, merge-conflict, read-state, or other github.md content.
  - [T-4] Disposition-log signal vs follow-up-reply-trigger for Actionable resolution → Prefer per-thread disposition log (user-chosen). Log survives crashes and is read by the memento pattern in the next tick; follow-up-reply-trigger is tick-local and dies on crashes mid-tick.
  - [T-5] Thread Hygiene ordering within tick → Prefer "after Write Outputs completes" so inbox follow-up replies land before hygiene resolves (avoids resolving a thread whose confirmation reply hasn't been posted yet).
  - [T-6] Retrigger-only tick hygiene behavior → Prefer no-op (user-chosen). Keeps the contract simple; accumulated disposition log is acted on by the tick that produced each entry, not re-scanned later.

## 3. Global Invariants

- [INV-G1] Intent analysis clean on the full diff — change-intent-reviewer returns no LOW+ findings.
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the git diff for this branch against main. Intent: decouple thread hygiene from comment handling in claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md and drive-tick/SKILL.md so bot threads resolve after addressing (including FP-reply-only ticks), without regressing the existing code-change-tick resolution path. Verify every change serves that intent, no drift, no unrelated edits."
  ```

- [INV-G2] Prompt quality clean — prompt-reviewer returns no MEDIUM+ findings on edited spec files.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md and claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md for prompt quality. Flag MEDIUM+ issues."
  ```

- [INV-G3] No code path resolves human threads. The adapter never calls a thread-resolve API on a thread whose source labelling is `human`.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read github.md in full. Enumerate every instruction that triggers thread resolution. Confirm every trigger is gated on source=bot (or equivalently non-human). Report any path that could resolve a human thread."
  ```

- [INV-G4] No contradiction between drive-tick/SKILL.md and github.md about when thread resolution fires. Both agree: Thread Hygiene runs every tick, independent of code changes.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Cross-read drive-tick/SKILL.md §P and github.md §Thread Hygiene + §Write Outputs. Confirm: (a) drive-tick invokes Thread Hygiene every tick; (b) adapter's Thread Hygiene contract does not gate on code changes; (c) Write Outputs no longer lists thread resolution as a step. Report any residual contradiction."
  ```

- [INV-G5] The 'After any code change:' gate in §Write Outputs is preserved for the remaining steps (commit, push, description-sync, inbox-follow-up-replies). The edit removes thread resolution from that block, not the block itself.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Confirm github.md §Write Outputs still opens with 'After any code change:' (or equivalent phrasing) and still covers commit, push, description sync, and inbox follow-up replies. The only removed item should be thread resolution."
  ```

- [INV-G6] Existing github.md content outside the scoped edit areas is byte-identical. Scoped areas: §Inbox Handling (lose the thread-resolution-rules subsection + any per-intent resolve phrasing); §Write Outputs (lose step 6); new §Thread Hygiene inserted; §Gotchas thread-resolution line may be updated to reference the new section. Everything else (Bootstrap, Read State, Terminal States, CI Failure Triage, Merge Conflicts, PR Description Sync, Security) unchanged.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Run `git diff main -- claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md`. Inspect the diff. Confirm changes are confined to §Inbox Handling (resolve-rules subsection + per-intent resolve phrasing removal), §Write Outputs (step 6 removal + renumber), new §Thread Hygiene section insertion, and the §Gotchas thread-resolution line. Flag any edits outside those regions."
  ```

- [INV-G7] Thread Hygiene ordering — drive-tick §P invokes Thread Hygiene strictly after Write Outputs completes (not concurrently, not before). This ensures inbox follow-up replies land before hygiene resolves Actionable threads.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive-tick/SKILL.md §P. Confirm the ordering specifies Thread Hygiene is invoked AFTER Write Outputs fully completes. Flag if the ordering is loose (parallel, unspecified) or reversed."
  ```

- [INV-G8] Actionable-fix-landed signal is a per-thread disposition log, not the follow-up-reply-trigger. Inbox Handling emits one log line per classified comment including source/classification/fingerprint; Thread Hygiene reads that log (via the memento pattern) + checks for a commit addressing the fingerprint.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Inbox Handling and §Thread Hygiene in github.md. Confirm: (a) Inbox Handling specifies a per-thread disposition log format emitted on every classification; (b) Thread Hygiene consumes that log to determine Actionable resolve eligibility; (c) the follow-up-reply-trigger in Write Outputs step 5 is NOT the hygiene-resolve signal. Flag any divergence."
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only — every edit addresses the FP-resolution failure or its direct consequences. Do not opportunistically clean up unrelated github.md sections.
- [PG-2] Proportionality — add one section, remove one step, move/cross-link one subsection, update one drive-tick section. No wholesale restructuring of CI triage, merge conflicts, or read-state.
- [PG-3] WHAT-and-WHY, not HOW — the new §Thread Hygiene section states goals + constraints + classification-to-action mapping. It does NOT prescribe tool-call order or pseudocode.
- [PG-4] Preserve the adapter boundary — drive-tick describes WHEN to invoke; github.md describes HOW per platform. Do not push platform-specific resolve logic into drive-tick, and do not push tick-sequencing decisions into github.md.

## 5. Known Assumptions

- [ASM-1] Cursor Bugbot and similar code-review bots are the primary drivers of FP-reply-only ticks. Default: scoping hygiene to "bot threads" (as currently defined by `./data/known-bots.md` + `[bot]` suffix + GitHub `user.type=="Bot"`) covers the observed case. Impact if wrong: threads from edge-case bot-like accounts (e.g., service accounts without the `[bot]` marker) would be treated as human — conservative failure mode.
- [ASM-2] "Addressed = fix committed" signal for Actionable threads is tractable via the existing Inbox-follow-up-replies step trigger (a material code change addressing the thread). Thread Hygiene reads the same trigger. Impact if wrong: Actionable threads might resolve before the fix lands, or never resolve. A short explicit trigger-definition in §Thread Hygiene reduces this risk.
- [ASM-3] `drive/references/ADAPTER_CONTRACT.md` does not need to list individual contract names in a rigid schema — the per-platform adapter file is the contract surface. Impact if wrong: drive-tick's cross-reference breaks at runtime.
- [ASM-4] No code tests exist for these spec files (they're markdown prompts); verification is via subagent review (prompt-reviewer, change-intent-reviewer, general-purpose cross-reads). Impact if wrong: n/a — this is confirmed by inspection of the repo.

## 6. Deliverables

### Deliverable 1: Add §Thread Hygiene section to github.md

New section in `claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md`, positioned after `## CI Failure Triage` and before `## Write Outputs`. Defines the contract: trigger (every tick), inputs (unresolved threads on the PR + per-thread disposition log from this tick's Inbox Handling + post-commit signal for Actionable fixes), resolution rules by classification (FP → resolve after reply; Actionable → resolve after fix commits; Uncertain → never resolve; Human → never resolve), and the stale-thread escalation relationship.

**Acceptance Criteria:**

- [AC-1.1] Section exists at the correct position (between CI Failure Triage and Write Outputs) with heading `## Thread Hygiene`.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Run `grep -n '^## ' claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md`. Confirm `## Thread Hygiene` appears in the section list and falls between `## CI Failure Triage` and `## Write Outputs`."
  ```

- [AC-1.2] Section specifies it runs every tick (not gated on code change) and names the drive-tick stage that invokes it.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the new §Thread Hygiene in github.md. Confirm it states the contract runs every tick independent of code changes, and names drive-tick §P (Tend PR) as the invoker."
  ```

- [AC-1.3] Per-classification resolve rules are explicit and cover all four cases (FP, Actionable, Uncertain, Human) with the addressing-trigger for each (FP=reply posted, Actionable=fix commit landed, Uncertain=never, Human=never).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Thread Hygiene. Confirm FP, Actionable, Uncertain, Human cases are all enumerated with their resolve triggers. Actionable resolves only after the fix commit lands (not at reply time). Human is never resolved. Flag any missing case or ambiguity."
  ```

- [AC-1.4] Section specifies the thread-addressing signal for Actionable: the per-thread disposition log emitted by §Inbox Handling. Thread Hygiene reads the log (memento pattern) and resolves an Actionable thread when (a) its disposition log entry exists AND (b) a commit addressing its fingerprint has landed on HEAD. The follow-up-reply trigger in §Write Outputs step 5 is explicitly NOT the hygiene signal.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Thread Hygiene. Confirm it specifies the per-thread disposition log from §Inbox Handling as the canonical signal for Actionable-fix-landed detection. Confirm it explicitly distinguishes this from the follow-up-reply-trigger in Write Outputs step 5. Flag if the signal is ambiguous or if both sources are offered without a clear primary."
  ```

- [AC-1.6] Section specifies behavior on retrigger-only ticks: Thread Hygiene no-ops (no new disposition data → nothing to resolve). Stated explicitly so readers understand the contract.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Thread Hygiene. Confirm it explicitly specifies: on a retrigger-only tick (no inbox processing, empty-commit CI retrigger), Thread Hygiene no-ops. Flag if retrigger-only behavior is undefined."
  ```

- [AC-1.7] Section specifies ordering within the tick: Thread Hygiene is invoked after §Write Outputs completes, never before or in parallel.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Thread Hygiene. Confirm it states that the contract is invoked strictly after Write Outputs completes within a tick. Flag if ordering is implicit or ambiguous."
  ```

- [AC-1.5] Section preserves the §Stale thread escalation semantics — bot threads that never get addressed (e.g., CI uncertain, or Actionable with no fix landing) still escalate per the existing 30-min window. §Thread Hygiene clarifies that aggressive resolution does not supersede stale-thread escalation for un-addressable bot cases; human-fix threads continue to use the existing path.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Thread Hygiene and §Stale thread escalation. Confirm the two sections are coherent — stale escalation is not dead code, and hygiene does not bypass it. Flag any tension."
  ```

### Deliverable 2: Remove thread-resolution step from §Write Outputs

In `github.md` §Write Outputs, remove step 6 ("Thread resolution — resolve bot threads addressed this tick. Never resolve human threads."). Preserve the "After any code change:" gate and remaining steps (stage/commit, push, append log, PR description sync, inbox follow-up replies).

**Acceptance Criteria:**

- [AC-2.1] Step 6 is removed from §Write Outputs; no reference to thread resolution remains within the code-change-gated block.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Run `awk '/^## Write Outputs/,/^## /' claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md | grep -i 'thread resolution'`. The grep should return empty. Any match means thread-resolution text still exists inside §Write Outputs."
  ```

- [AC-2.2] Remaining §Write Outputs steps (commit, push, log append, PR description sync, inbox follow-up replies) are unchanged.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Write Outputs in the new github.md. Confirm the opening 'After any code change:' gate is preserved, and steps for stage/commit, push, append log, PR description sync, and inbox follow-up replies are present with substantively unchanged wording. Only step 6 (thread resolution) should be gone. Never-force-push and never-amend-already-pushed rules retained."
  ```

- [AC-2.3] §Write Outputs steps are contiguously numbered after the removal (no `5, 7` style gap).
  ```yaml
  verify:
    method: bash
    command: "awk '/^## Write Outputs/,/^## [^W]/' claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md | grep -E '^[0-9]+\\.' | awk -F'.' 'BEGIN{prev=0} {if ($1 != prev+1) {print \"GAP: prev=\"prev\" cur=\"$1; exit 1} prev=$1} END{print \"OK: contiguous through \"prev}'"
  ```

### Deliverable 3: Relocate §Inbox Handling's thread-resolution-rules subsection

In `github.md` §Inbox Handling, remove the `### Thread resolution rules` subsection and any per-intent resolve instructions. The section keeps classification, routing (manifest/babysit/FP/uncertain), and reply semantics. Add a one-line pointer "Thread resolution is owned by §Thread Hygiene" for cross-reference.

**Acceptance Criteria:**

- [AC-3.1] `### Thread resolution rules` subsection is no longer inside §Inbox Handling.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Run `awk '/^## Inbox Handling/,/^## /' claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md | grep -iE 'thread resolution rules|resolve after addressing'`. The grep should return empty. Any match means resolve-rules text is still embedded in §Inbox Handling."
  ```

- [AC-3.2] §Inbox Handling contains a short cross-reference pointing readers to §Thread Hygiene.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Inbox Handling. Confirm it contains a one-line reference to §Thread Hygiene indicating that thread-state changes are owned there. The reference should be concise, not a duplicate of hygiene rules."
  ```

- [AC-3.3] Per-intent branches (Actionable/FP/Uncertain manifest-mode, babysit-mode) keep their reply semantics and do NOT mention resolving threads. Human comment routing (if present) unchanged.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Inbox Handling routing subsection. Confirm no branch prescribes a resolve action. FP still says reply only; Actionable still says reply/ack + route to Amendment (manifest mode) or escalate (babysit mode); Uncertain still says reply + leave open."
  ```

### Deliverable 4: Update drive-tick §P Tend PR to invoke both Write Outputs and Thread Hygiene contracts

In `claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md` §P (Tend PR), rework the instruction so the tick explicitly invokes two adapter contracts in order: Write Outputs (only when this tick produced code changes) and Thread Hygiene (every tick). The section names both contracts, clarifies the gating difference, and drops the thread-resolution bullet from the Write-Outputs-flavored description.

**Acceptance Criteria:**

- [AC-4.1] §P Tend PR in drive-tick/SKILL.md names `Thread Hygiene` as a distinct adapter contract invocation, ordered after Write Outputs within the tick.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive-tick/SKILL.md §P. Confirm it (a) invokes the platform adapter's Write Outputs contract gated on code changes, and (b) separately invokes Thread Hygiene every tick. Flag if the two are conflated or if gating is wrong."
  ```

- [AC-4.2] The previous thread-resolution bullet inside the Tend-PR list has been rewritten or moved to reference the new Thread Hygiene invocation.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Run `awk '/^### P\\. Tend PR|^## P\\. Tend PR/,/^###|^## /' claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md | head -40`. Inspect §P. Confirm the thread-resolution content is framed as a Thread Hygiene contract invocation, not a Write Outputs sub-bullet."
  ```

- [AC-4.3] Existing gating for PR description sync is unchanged — still skipped on retrigger-only commits, still runs only when the tick produced changes.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive-tick/SKILL.md §P. Confirm PR description sync gating is unchanged (only runs on code-change ticks; skipped on retrigger-only). This AC guards against accidental regression from the restructure."
  ```

- [AC-4.4] drive-tick §P does not leak adapter-specific logic (e.g., never mentions `mcp__github__*` APIs or GitHub-specific verbs) — the adapter-boundary discipline is preserved.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read drive-tick/SKILL.md §P. Confirm the text uses contract-level language (invoke Write Outputs / Thread Hygiene) and does not describe GitHub-specific mechanics. Adapter-specific logic belongs in github.md, not here."
  ```

### Deliverable 5: Behavioral scenario regression coverage

A single AC that enumerates the five tick shapes and asserts the spec's behavior for each. Acts as a behavioral contract over the edit — any spec change that breaks one of these scenarios is a regression.

**Acceptance Criteria:**

- [AC-5.1] The edited spec, read end-to-end, produces these behaviors for each tick shape:
  1. **FP-only tick** (inbox has FP, no code change): FP comment replied + bot thread resolved (by Thread Hygiene) by end of tick.
  2. **Actionable-only tick** (inbox has actionable, /do commits fix): reply posted + fix commits + inbox follow-up reply posted + bot thread resolved (by Thread Hygiene).
  3. **Mixed tick** (FP + actionable siblings): FP bot thread resolved, actionable bot thread resolved after commit.
  4. **Uncertain-only tick**: reply posted asking for clarification + thread remains unresolved.
  5. **Human-comment tick** (regardless of classification): reply may or may not be posted per existing rules + thread is NEVER resolved by the tick.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read the edited github.md and drive-tick/SKILL.md end-to-end. For each of these five tick shapes, trace the spec and confirm the expected behavior: (1) FP-only tick → reply + resolve; (2) Actionable-only → reply + fix commit + follow-up reply + resolve; (3) Mixed FP+Actionable → both resolve on their respective triggers; (4) Uncertain-only → reply + leave open; (5) Human-comment → never resolved. Report any scenario where the spec is ambiguous or predicts the wrong outcome."
  ```

- [AC-5.2] Gotchas section in github.md — the existing bullet on "Thread resolution is permanent" is preserved and updated to reference §Thread Hygiene rather than step-6-of-Write-Outputs (if referenced).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Gotchas in github.md. Confirm the thread-resolution-is-permanent bullet is intact and any cross-reference points to §Thread Hygiene."
  ```

### Deliverable 6: Per-thread disposition log in §Inbox Handling (producer side of the hygiene signal)

Specify in `github.md` §Inbox Handling that every classified comment produces a per-thread disposition log line in the tick's execution log. The log is the single source of truth Thread Hygiene reads. Format is adapter-owned; drive-tick does not interpret it.

**Acceptance Criteria:**

- [AC-6.1] §Inbox Handling specifies an explicit disposition log format — one line per classified comment including: thread id, source (bot/human), bot name (if bot), classification (FP/Actionable/Uncertain), content fingerprint (hash), and tick number.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Inbox Handling. Confirm it specifies an explicit per-thread disposition log format. Confirm every classification path (FP / Actionable / Uncertain) emits one log line per comment. Flag if the format is vague or any classification path omits logging."
  ```

- [AC-6.2] Log entries use a stable prefix (e.g., `### Inbox —` or similar) that Thread Hygiene can grep on across ticks per the memento pattern.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Read §Inbox Handling's disposition log format. Confirm the prefix is stable and literal (no variable substitution in the anchor). §Thread Hygiene should be able to grep this prefix to enumerate prior-tick dispositions."
  ```

- [AC-6.3] Content-fingerprint method aligns with the existing §Gotchas rule "Track findings by content (hash the message), not comment ID". Disposition log reuses or references that hashing convention.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Cross-read §Inbox Handling (new disposition log) and §Gotchas (finding-content hashing). Confirm the fingerprint in the disposition log uses the same hashing rule, not a newly-invented one."
  ```

## 7. Summary

**What it is:** a spec bug fix in the github platform adapter. Right now, when a /drive tick only handles false-positive bot comments (reply, no code change), the bot threads on GitHub stay unresolved — because thread resolution lives inside a section that only runs when code changes. Fix: pull thread resolution out into its own "Thread Hygiene" step that runs every tick, keep comment handling focused purely on replies.

**What'll change (two spec files):**
- `github.md` gains a new `## Thread Hygiene` section (runs every tick, resolves bot threads after addressing, never touches human threads).
- `github.md` §Write Outputs loses its thread-resolution step (step 6).
- `github.md` §Inbox Handling loses the "thread resolution rules" subsection; gains a per-comment disposition log that Thread Hygiene reads.
- `drive-tick/SKILL.md` §P (Tend PR) invokes Write Outputs and Thread Hygiene as two distinct adapter contracts with different gating.

**Guardrails:**
- Human threads are never resolved by any code path.
- FP bot threads resolve after the reply; Actionable bot threads resolve only after the fix commits; Uncertain stays open.
- Retrigger-only ticks no-op in hygiene.
- Thread Hygiene runs strictly after Write Outputs completes.
- Edits stay confined to the three named sections + one drive-tick section; no drive-by restructuring.

**How it'll be verified:**
- change-intent-reviewer on the full diff (no LOW+).
- prompt-reviewer on both edited files (no MEDIUM+).
- A behavioral scenario AC (AC-5.1) traces five tick shapes (FP-only, Actionable-only, Mixed, Uncertain, Human) through the edited spec and confirms the expected outcome for each.
- Cross-file consistency checks that drive-tick §P and github.md agree on when hygiene fires.
- Bash grep checks confirm step-6 removal and renumbering.

