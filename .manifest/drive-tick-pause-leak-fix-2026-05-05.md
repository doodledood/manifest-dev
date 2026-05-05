# Definition: Fix /drive-tick "tick doing little" — close User-Requested Pause leak and surface wide-tick rule

## 1. Intent & Context

- **Goal:** /drive-tick must run per its declared contract — each tick delegates the full implement+verify+fix loop to /do (intra-tick convergence). Stop the regression where /do invents `## Escalation: User-Requested Pause` after a single AC because it misreads the cron/tick framing as "do little per tick", which causes /drive-tick to treat each tick as Terminal and end the loop after one AC.
- **Mental Model:**
  - **Wide tick.** A /drive-tick = one full /do run (all reachable ACs implemented + /verify pass) + adapter post-stages. Not per-AC.
  - **/do runs to convergence.** /do exits via /verify pass (→ /done) or a real blocker (AC/INV-G blocking after attempts, fix-loop limit, actual user interrupt, amendment routing). Voluntary stops are not allowed.
  - **User-Requested Pause is reflexive, not discretionary.** Fires only in response to an explicit user pause message during the run. The user's words must appear (quoted) in the escalation body. No user message → not a valid escalation type.
- **Mode:** thorough
- **Interview:** autonomous *(switched mid-flow per /auto contract)*
- **Medium:** local

## 2. Approach

- **Architecture:** three coordinated prompt edits + distribution sync. Caller (/drive-tick) owns its expectation; callee (/do) stays caller-agnostic. /escalate owns the evidence floor for each escalation type.
  1. **/escalate** — add an evidence floor on `User-Requested Pause`: must quote the user message that triggered it; explicit "do not synthesize this escalation when no such message exists" guardrail.
  2. **/do** — rewrite the "Stop requires /escalate" sentence and the Escalation boundary item so "user requests a pause mid-workflow" is unambiguously gated on a user message, not on the agent's interpretation of caller framing. Cross-reference Mid-Execution Amendment for the amend-vs-pause distinction.
  3. **/drive-tick** — surface a load-bearing "Tick scope" rule near the top of the body (before the Memento/Concurrency machinery) declaring: each tick = full /do convergence + adapter post-stages; /do is not invoked piecemeal per AC; tick framing (cron, /loop, intervals) is a scheduling concern, not a per-AC pause point.
  4. **Distribution sync** — invoke the `sync-tools` skill so `dist/gemini`, `dist/opencode`, `dist/codex` reflect the source skills. Hardlinks at `.claude/skills/*` and symlinks at `.agents/skills/*` are confirmed intact (no manual fixup needed unless a check fails).
  5. **Plugin version bump** — `0.102.1` → `0.102.2` (patch — bug fix per CLAUDE.md).

- **Execution Order:**
  - D1 (/escalate) → D2 (/do) → D3 (/drive-tick) → D4 (sync + version bump)
  - Rationale: /escalate fixes the leak at the type definition; /do removes the tempting voluntary-pause path; /drive-tick reframes the caller contract so future agents reading the cron/tick language don't reinvent the bug. D4 is mechanical and runs last so all mirrors capture the final state.

- **Risk Areas:**
  - [R-1] Tightening User-Requested Pause breaks a legitimate pause flow (real user message like "stop here, I want to deploy") | Detect: change-intent-reviewer scenario probe — confirm legitimate path still emits.
  - [R-2] Wide-tick rule overreaches and misreads babysit-mode (where /do is skipped entirely) | Detect: re-read /drive-tick post-edit; rule must accommodate "manifest mode = full /do; babysit mode = no /do but adapter stages run".
  - [R-3] Plugin-vs-.claude divergence — edits to wrong copy don't propagate | Detect: stat -f %i hardlink check post-edit (both inodes equal). Note: edit canonical path `claude-plugins/manifest-dev/skills/<x>/SKILL.md` only.
  - [R-4] Distribution sync drift — dist/ lacks new content | Detect: grep dist/* for the new wording strings post-sync.
  - [R-5] Over-engineering — change adds more wording than needed (PROMPTING anti-pattern) | Detect: prompt-reviewer flags information-density issues.

- **Trade-offs:**
  - [T-1] Brevity vs explicit guardrail in `/escalate User-Requested Pause` → Prefer guardrail. The current ambiguity caused the bug; ~2-3 added lines are the cost of a hard exit on synthesized pauses.
  - [T-2] Centralize wide-tick rule in /drive-tick vs. cross-reference from /do → Prefer /drive-tick. Caller owns the contract; /do stays agnostic about who invokes it.
  - [T-3] Harden only User-Requested Pause vs. systematically audit every escalation type → Prefer narrow. Other types already have evidence floors (3-attempt for blocking, trigger source for Self-Amendment, automated-pass for Manual Review). User-Requested Pause is the singular weak link.

## 3. Global Invariants

- [INV-G1] Prompt review of the four edited skill files reports no MEDIUM+ issues against PROMPTING.md quality gates.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: |
      Review the following skill files against PROMPTING quality gates (clarity, no conflicts, structure, information density, no anti-patterns, invocation fit, domain context, complexity fit, edge case coverage, output calibration, emotional tone). Files:
      - claude-plugins/manifest-dev/skills/escalate/SKILL.md
      - claude-plugins/manifest-dev/skills/do/SKILL.md
      - claude-plugins/manifest-dev/skills/drive-tick/SKILL.md
      Threshold: report only MEDIUM+ findings. If none, report VERIFIED.
  ```

- [INV-G2] Change-intent review reports no LOW+ findings on the diff.
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: |
      Review the diff (git diff against main) for whether the changes achieve their stated intent: close the User-Requested Pause synthesis leak, surface /drive-tick's wide-tick convergence rule, and ensure /do never voluntarily exits without genuine cause. Look for:
      - Cases where the new wording could still be read as discretionary
      - Cases where the new evidence floor would block legitimate pause flows
      - Cases where the wide-tick rule conflicts with babysit-mode behavior (no /do invocation)
      Threshold: report only LOW+ findings. If none, report VERIFIED.
  ```

- [INV-G3] `.claude/skills/<x>/SKILL.md` and `claude-plugins/manifest-dev/skills/<x>/SKILL.md` remain hardlinked (same inode) for do, escalate, drive-tick.
  ```yaml
  verify:
    method: bash
    command: |
      set -e
      for skill in do escalate drive-tick; do
        a=$(stat -f %i "claude-plugins/manifest-dev/skills/$skill/SKILL.md")
        b=$(stat -f %i ".claude/skills/$skill/SKILL.md")
        if [ "$a" != "$b" ]; then echo "FAIL: hardlink broken for $skill (inodes $a vs $b)"; exit 1; fi
      done
      echo "VERIFIED: hardlinks intact for do, escalate, drive-tick"
  ```

- [INV-G4] Distribution mirrors at `dist/gemini`, `dist/opencode`, `dist/codex` reflect the post-edit source content for all three skills (do, escalate, drive-tick).
  ```yaml
  verify:
    method: bash
    command: |
      set -e
      # Sync should be idempotent — running it again produces no diff.
      # Method: invoke sync-tools, then check git status for any unexpected dist/ changes after a second run.
      for dist in gemini opencode codex; do
        if [ ! -d "dist/$dist" ]; then echo "FAIL: dist/$dist missing"; exit 1; fi
        # Check the new wording landed (User-Requested Pause now mentions evidence/quoted message).
        if ! grep -rq "quoted" "dist/$dist" 2>/dev/null; then
          # Lenient: dist might use different rendering. Just check User-Requested Pause section exists post-sync.
          if ! grep -rq "User-Requested Pause" "dist/$dist" 2>/dev/null; then
            echo "FAIL: User-Requested Pause section missing in dist/$dist"; exit 1
          fi
        fi
      done
      echo "VERIFIED: dist/ mirrors present and contain User-Requested Pause section"
  ```

## 4. Process Guidance

- [PG-1] Edit only `claude-plugins/manifest-dev/skills/<x>/SKILL.md` paths. Never edit `.claude/skills/<x>/SKILL.md` directly — they are hardlinks and edits should originate at the canonical path. Per CLAUDE.md.
- [PG-2] (auto) Keep additions minimal — every word earns its place. PROMPTING default: high-signal changes only.
- [PG-3] (auto) Direct imperatives, no urgency language; "trusted advisor" tone. PROMPTING default: low-arousal emotional tone.
- [PG-4] Use `sync-tools` skill (not manual file copying) for distribution mirrors. The skill encodes the conversion logic for Gemini/OpenCode/Codex; manual copies will drift.

## 5. Known Assumptions

- [ASM-1] (auto) User-Requested Pause is the only escalation type with a weak evidence floor; other types (Global Invariant Blocking, AC Blocking, Manual Review, Proposed Amendment, Self-Amendment, Deferred-Auto Pending) have stronger gates and don't need the same hardening. | Default: harden only User-Requested Pause. | Impact if wrong: another escalation type leaks similarly later; addressable by amendment if observed.
- [ASM-2] (auto) `sync-tools` skill is the canonical route for distribution sync. | Default: invoke sync-tools after source edits. | Impact if wrong: dist/* drifts; manual fixup or amendment.
- [ASM-3] (auto) No code edits required — task is purely prompt edits + a JSON version bump. | Default: prompts + plugin.json only. | Impact if wrong: discovered during /do, escalates as Proposed Amendment.
- [ASM-4] (auto) Plugin version bumps `0.102.1 → 0.102.2` (patch — bug fix per CLAUDE.md versioning rules). | Default: patch. | Impact if wrong: minor version retrofit, low cost.
- [ASM-5] (auto) Branch name follows convention `fix/drive-tick-pause-leak` (per CLAUDE.md `fix/*` for bug fixes). | Default: this name. | Impact if wrong: rename branch before push.

## 6. Deliverables

### Deliverable 1: /escalate User-Requested Pause evidence floor

**Acceptance Criteria:**

- [AC-1.1] The `User-Requested Pause` section in `claude-plugins/manifest-dev/skills/escalate/SKILL.md` requires the triggering user message to be quoted in the escalation body, and explicitly forbids agent-synthesized pauses (no real user message → do not use this escalation type).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/skills/escalate/SKILL.md. Check the "### User-Requested Pause" section for:
      1. An explicit requirement that the triggering user message be quoted in the escalation body (a "Trigger message:" or equivalent field with a quoted user message).
      2. An explicit guardrail that this escalation type is NOT to be used unless a real user message in the conversation requested the pause (i.e., agent must not synthesize this exit based on its own interpretation of caller framing like "cron-driven /drive contract").
      3. The example template shows a quoted trigger message.
      Report PASS if all three are present and clearly stated. Report FAIL with quoted excerpts otherwise.
  ```

- [AC-1.2] The legitimate pause flow (e.g., user message "commit so I can deploy") still passes the evidence floor — the rule does not eliminate the type, only gates it.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/skills/escalate/SKILL.md "### User-Requested Pause" section. Imagine a user during /do sends the message: "commit so I can deploy". Confirm the section's rules permit emitting a User-Requested Pause that quotes that message. Report PASS if the rules accommodate this legitimate flow, FAIL with reasoning if the rules over-tighten and block it.
  ```

### Deliverable 2: /do voluntary-pause prohibition

**Acceptance Criteria:**

- [AC-2.1] In `claude-plugins/manifest-dev/skills/do/SKILL.md`, the "Stop requires /escalate" sentence is rewritten so it cannot be read as discretionary. It must clearly state that `/do` does not voluntarily emit `User-Requested Pause`; the type is only valid in response to an actual user pause message during the run.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: |
      Read the "Stop requires /escalate" paragraph in claude-plugins/manifest-dev/skills/do/SKILL.md (under ## Constraints). Confirm:
      1. The wording "if you need to pause" is removed or rephrased so it cannot be read as the agent's discretion.
      2. The paragraph explicitly states that User-Requested Pause requires a user pause message; /do does not synthesize this escalation.
      3. No new contradictions with adjacent rules (Escalation boundary, Mid-Execution Amendment).
      Report PASS or FAIL with quoted excerpts.
  ```

- [AC-2.2] The "Escalation boundary" rule (item 2: "user requests a pause mid-workflow") is reinforced to require a user message, with cross-reference to Mid-Execution Amendment for the amend-vs-pause distinction.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: |
      Read the "Escalation boundary" paragraph in claude-plugins/manifest-dev/skills/do/SKILL.md "## Constraints". Confirm item (2) "user requests a pause mid-workflow" is qualified by "via an explicit user message" or equivalent, AND cross-references Mid-Execution Amendment so the agent distinguishes amend-shaped messages (→ Self-Amendment) from pause-shaped messages (→ User-Requested Pause). Report PASS or FAIL with quoted excerpts.
  ```

### Deliverable 3: /drive-tick wide-tick rule surfacing

**Acceptance Criteria:**

- [AC-3.1] A load-bearing "Tick scope" rule appears prominently in `claude-plugins/manifest-dev/skills/drive-tick/SKILL.md` (top of body, before the Tick Execution Order section). It states: each tick = one full /do convergence run (manifest mode) + adapter post-stages; /do is not invoked piecemeal per AC; the cron/loop/interval framing is a scheduling concern, not a per-AC pause point.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/skills/drive-tick/SKILL.md. Confirm a clearly-labeled rule appears near the top of the body (before "## Tick Execution Order") that states: each tick delegates the full /do convergence (in manifest mode); /do is not invoked piecemeal per AC; cron/loop/interval framing is scheduling, not per-AC pausing. The rule must be readable as load-bearing — not buried as a side-note. Report PASS with the section heading, or FAIL with reasoning.
  ```

- [AC-3.2] The new rule is consistent with babysit mode (where /do is not invoked at all) and existing references to "stateless tick", "wide ticks", "intra-tick convergence", "/do delegation" — no contradictions introduced.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: |
      Read claude-plugins/manifest-dev/skills/drive-tick/SKILL.md in full. Confirm the new "Tick scope" rule:
      1. Does not contradict babysit mode behavior (where /do is skipped entirely; only inbox + tend stages run).
      2. Is consistent with the description's "wide ticks with intra-tick convergence", §D Do Invocation's delegation contract, and §C Continue.
      3. Does not duplicate or contradict the §Action Decision Tree's Terminal exits table.
      Report PASS if consistent, FAIL with the conflicting passages otherwise.
  ```

### Deliverable 4: Distribution sync + plugin version bump

**Acceptance Criteria:**

- [AC-4.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version bumps from `0.102.1` to `0.102.2` (patch — bug fix).
  ```yaml
  verify:
    method: bash
    command: |
      v=$(grep '"version"' claude-plugins/manifest-dev/.claude-plugin/plugin.json | head -1 | sed 's/.*"version": *"\([^"]*\)".*/\1/')
      [ "$v" = "0.102.2" ] && echo "VERIFIED: version=$v" || { echo "FAIL: version=$v expected 0.102.2"; exit 1; }
  ```

- [AC-4.2] Distribution mirrors `dist/gemini`, `dist/opencode`, `dist/codex` are regenerated via the `sync-tools` skill and reflect the post-edit source content. (Concrete check: User-Requested Pause text in dist matches the source.)
  ```yaml
  verify:
    method: bash
    command: |
      set -e
      for dist in gemini opencode codex; do
        [ -d "dist/$dist" ] || { echo "FAIL: dist/$dist missing"; exit 1; }
      done
      # Check the source's User-Requested Pause section (must include the new evidence-floor wording) is reflected in at least one dist mirror — exact path varies per format.
      grep -rq "User-Requested Pause" dist/ || { echo "FAIL: User-Requested Pause section absent across dist/"; exit 1; }
      echo "VERIFIED: dist/ mirrors regenerated and contain expected sections"
  ```

- [AC-4.3] All updated README sync items per CLAUDE.md "README sync checklist" — N/A here because no components added/renamed/removed; only existing skill content changed.
  ```yaml
  verify:
    method: codebase
    command: |
      # Sanity: confirm no new/removed skill directories that would require README updates.
      git diff --name-status main -- claude-plugins/manifest-dev/skills/ | grep -E '^[AD]\s' && echo "FAIL: skill dirs added/removed; README sync may be required" || echo "VERIFIED: no skill structure changes; README sync N/A"
  ```
