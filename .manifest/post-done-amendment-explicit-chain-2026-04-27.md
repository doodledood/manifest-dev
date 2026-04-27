# Definition: Post-/done Amendment Re-entry — Explicit Chain to /do

## 1. Intent & Context

- **Goal:** When user feedback arrives after `/done`, the agent must perform a deterministic two-step chain: (1) `/define --amend <manifest-path>` to amend the manifest (with or without questions, per the manifest's recorded `Interview:` style), then (2) `/do <manifest-path> <log-path> [--scope ...]` to implement and verify the change. Today step 2 is described as descriptive prose — agents read it as a suggestion and stop after step 1, leaving the manifest amended but unimplemented and unverified. Make the chain explicit, ordered, and mandatory in skill prompts so verification reliably runs after every amendment.

- **Mental Model:**
  - **Post-/done feedback is a re-entry, not a continuation** — `/do` already terminated; the agent must explicitly re-invoke `/do` to resume the verification cycle. This is structurally identical to `/auto`'s `/define → /do` chain, just triggered post-completion instead of fresh.
  - **The descriptive-vs-directive gap is the bug.** `done/SKILL.md` line 89 reads "invoke `/define --amend ...`, then `/do ...`" — a single sentence treating both calls as equally weighted advice. `/auto` succeeds where post-/done fails because `/auto` numbers its steps and uses imperative invocation language. Mirror that pattern.
  - **`/define` stays a leaf skill.** The chain belongs at the orchestrator (the agent reading `done/SKILL.md`'s Post-Completion Feedback section), not inside `/define`. `/define` continues to "output the manifest path and stop" — clean separation of concerns.
  - **Existing primitives carry the load.** `AMENDMENT_MODE.md` already inherits interview style from manifest's `Interview:` field (so questions appear when style is `thorough`, not when `autonomous`). `/do`'s "Must call /verify" rule transitively closes the verification gap once `/do` is reliably invoked. The amendment loop guard (R-7 in `do/SKILL.md`) already covers oscillation. Nothing new to build — strengthen the language so the existing chain actually runs.

- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach
*Initial direction. Skill-prompt-only fix; no hooks, no flags, no schema changes. Mirrors `/auto`'s explicit-chain pattern.*

- **Architecture:**
  - **`done/SKILL.md` Post-Completion Feedback rewrite.** Replace the single-sentence Re-entry flow with an explicit ordered list (Step 1: invoke `/define --amend ...`; Step 2: invoke `/do ...`) plus a mandatory-completion line ("Both steps are mandatory. Stopping after step 1 leaves the manifest amended but unimplemented and unverified — the same failure mode as silent scope drift."). Imperative invocation language ("Invoke the manifest-dev:define skill with: ...") matches `/auto`'s pattern. Pure-question carve-out, manifest-in-scope detection, and no-manifest case stay as-is.
  - **`escalate/SKILL.md` Self-Amendment "Triggered after /done" bullet rewrite.** Mirror the explicit chain in summary form, then cross-reference `done/SKILL.md` Post-Completion Feedback as canonical. Avoids text drift — one source of truth, one summary that points to it.
  - **No changes to `define/SKILL.md` Complete section.** `/define` stays a leaf skill that outputs and stops. Chain orchestration lives entirely in `done/SKILL.md`.
  - **No new hooks, no `stop_do_hook` changes.** Per prior user direction ("don't pollute the context after done unnecessarily"). If skill-prompt strengthening proves insufficient, hook-level enforcement is a follow-up.
  - **Plugin metadata + distribution sync.** Version bump (minor, 0.92.0 → 0.93.0) since this fixes a behavioral feature. Distributions under `dist/` regenerated via `sync-tools` skill as the **final** step, after all source changes pass verification.

- **Execution Order:**
  - D1 (`done/SKILL.md` rewrite — load-bearing change)
  - D2 (`escalate/SKILL.md` mirror — depends on D1's wording)
  - D3 (plugin version bump)
  - D4 (sync-tools regeneration — runs LAST, after D1–D3 pass verification, per user direction)
  - Rationale: D1 is the primary fix; D2 mirrors so escalate stays coherent; D3 is housekeeping; D4 must run after the source-truth verification gates pass, otherwise dist/ would lock in pre-amendment text.

- **Risk Areas:**
  - [R-1] **Agent reads new explicit chain but still stops after step 1** — the most likely residual failure mode. | Detect: change-intent-reviewer specifically asked to flag if the new wording could plausibly be read as "step 2 optional"; prompt-reviewer flags weak language.
  - [R-2] **`--scope` inferred too narrow** — fix touches a shared file that breaks an out-of-scope deliverable. | Detect: `/verify`'s mandatory full final gate (existing safety net per `do/SKILL.md` and `verify/SKILL.md`) catches cross-deliverable regressions before `/done` is reachable. No new check needed.
  - [R-3] **Pure-question carve-out misclassified** — agent treats "what does AC-1.1 mean?" as amendment-worthy. | Detect: existing carve-out wording preserved verbatim with concrete examples; ambiguous defaults to amend (asymmetric per existing rule).
  - [R-4] **Distribution drift** — source SKILL.md updated but `dist/` (Gemini, OpenCode, Codex) not regenerated. | Detect: D4 explicitly invokes sync-tools as the final step; INV-G5 asserts dist files match source post-sync.
  - [R-5] **Hardlink break** — editing `claude-plugins/manifest-dev/skills/done/SKILL.md` should propagate to `.claude/skills/done/SKILL.md` via hardlink. If a tool unexpectedly creates a copy instead of editing in place, the two files diverge. | Detect: INV-G3 asserts inode equality post-edit.
  - [R-6] **Composition conflict between `/done`'s mandatory trailing italic line and the new Re-entry flow** — both speak to the user about post-completion feedback; tone or content could clash. | Detect: prompt-reviewer specifically asked to check coherence between the trailing line and the Post-Completion Feedback section.

- **Trade-offs:**
  - [T-1] Skill-prompt-only vs hook enforcement → Prefer **skill-prompt-only**. Per prior user direction "don't pollute the context after done unnecessarily." Hook enforcement adds maintenance burden and context noise; skill prompt is reversible if the new wording proves weak. (Logged as ASM-1.)
  - [T-2] Modify `/define`'s Complete section vs keep it neutral → Prefer **keep `/define` neutral**. `/define` is a leaf skill — adding context-aware chaining ("if invoked from post-/done, chain to /do") couples `/define` to its callers. Cleaner to keep the chain in `done/SKILL.md` (the actual orchestrator). (Logged as ASM-3.)
  - [T-3] `--scope <new-or-affected-deliverables>` vs full `/do` → Prefer **`--scope`**. Preserves selective-verification economics from the prior `default-to-amend-and-selective-verify` change. Agent infers scope from amendment log; full final gate catches cross-deliverable bugs. (Logged as ASM-2.)
  - [T-4] Duplicate full chain text in `escalate/SKILL.md` vs cross-reference to `done/SKILL.md` → Prefer **brief mirror + cross-reference**. Avoids text drift. Both files stay coherent; canonical source is one. (Logged as ASM-4.)
  - [T-5] Patch vs minor version bump → Prefer **minor (0.93.0)**. Strengthens an existing behavioral feature; not pure typo (patch) and not breaking (major). Per CLAUDE.md versioning convention. (Logged as ASM-5.)

## 3. Global Invariants

- [INV-G1] **Intent analysis on the changeset.** change-intent-reviewer reports no LOW+ findings — the modified text in `done/SKILL.md` and `escalate/SKILL.md` achieves the stated intent (post-/done feedback deterministically chains `/define --amend` → `/do`) without behavioral divergence or wording that could plausibly be read as "step 2 optional."
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Adversarially analyze whether the changes to claude-plugins/manifest-dev/skills/done/SKILL.md (Post-Completion Feedback section) and claude-plugins/manifest-dev/skills/escalate/SKILL.md (Self-Amendment 'Triggered after /done' bullet) achieve this stated intent: when amendment-worthy feedback arrives after /done, the agent must perform a deterministic two-step chain — (1) invoke /define --amend <manifest-path>, then (2) invoke /do <manifest-path> <log-path> [--scope ...]. Flag wording that could plausibly be read as 'step 2 is optional', any hedge that weakens the chain, regressions in the pure-question carve-out, regressions in the no-manifest fail-open path, or composition conflicts with the existing trailing italic line in /done's output template. Report LOW/MEDIUM/HIGH findings."
  ```

- [INV-G2] **Prompt quality across all modified prompts.** prompt-reviewer reports no MEDIUM+ findings on every modified `SKILL.md` file (clarity, no conflicts, structure, density, anti-patterns, invocation fit, edge case coverage, emotional tone — per PROMPTING.md gates).
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review the modified text in claude-plugins/manifest-dev/skills/done/SKILL.md (Post-Completion Feedback section) and claude-plugins/manifest-dev/skills/escalate/SKILL.md (Self-Amendment 'Triggered after /done' bullet) against prompt-engineering principles. Check: clarity (no ambiguity in the ordered steps), no conflicts (the new ordered steps cohere with /done's mandatory trailing italic line and existing pure-question carve-out), structure (steps surface prominently), density (no padding), anti-patterns (no weak language like 'try to' or 'maybe', no arbitrary limits, no prescriptive HOW the model should reason), invocation fit (parent agent is the consumer), composition (cross-reference between escalate and done is non-redundant), edge case coverage (pure-question, no-manifest, multi-repo cases preserved), emotional tone (low arousal, trusted advisor). Report MEDIUM/HIGH findings."
  ```

- [INV-G3] **Hardlink integrity preserved.** `claude-plugins/manifest-dev/skills/done/SKILL.md` and `.claude/skills/done/SKILL.md` share an inode after the edit; same for `escalate/SKILL.md`. Confirms edits propagated correctly without breaking the hardlink.
  ```yaml
  verify:
    method: bash
    command: "for f in skills/done/SKILL.md skills/escalate/SKILL.md; do a=\"claude-plugins/manifest-dev/$f\"; b=\".claude/$f\"; ai=$(stat -c %i \"$a\"); bi=$(stat -c %i \"$b\"); if [ \"$ai\" != \"$bi\" ]; then echo \"FAIL hardlink: $f (source inode $ai != mirror inode $bi)\"; exit 1; fi; done; echo OK"
  ```

- [INV-G4] **Pre-PR commands pass clean.** `ruff check claude-plugins/`, `black --check claude-plugins/`, `mypy`, and `pytest tests/hooks/ -v` all pass. Hook tests must continue passing — this change is skill-prompt only, no hook code changes, so existing tests should not regress.
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy && pytest tests/hooks/ -v"
  ```

- [INV-G5] **Distributions under `dist/` match source.** After `sync-tools` runs (D4), the regenerated dist files reflect the updated SKILL.md text. No stale text in Gemini, OpenCode, or Codex distributions.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "After sync-tools has been invoked, verify that the post-/done re-entry chain wording in dist/ distributions reflects the source SKILL.md changes. Specifically: (1) check that the explicit Step 1/Step 2 chain language from claude-plugins/manifest-dev/skills/done/SKILL.md Post-Completion Feedback section is present in any dist/ files derived from done/SKILL.md (Gemini, OpenCode, Codex packaging — exact filenames depend on sync-tools output structure); (2) check that the escalate/SKILL.md mirror language is similarly reflected. PASS if dist files contain the new chain wording. FAIL if any dist file still has the old single-sentence Re-entry flow text or is missing the explicit ordered steps."
  ```

- [INV-G6] **No regression in /auto's existing chain.** `/auto`'s `/define → /do` flow is structurally similar but lives in a different file (`auto/SKILL.md`) — unaffected by this change. Verify that `auto/SKILL.md` was NOT modified and its existing chain text is unchanged.
  ```yaml
  verify:
    method: bash
    command: "git diff origin/main..HEAD -- claude-plugins/manifest-dev/skills/auto/SKILL.md .claude/skills/auto/SKILL.md | wc -l | { read n; if [ \"$n\" -ne 0 ]; then echo \"FAIL: auto/SKILL.md was modified ($n diff lines) — should be untouched\"; exit 1; fi; echo OK; }"
  ```

- [INV-G7] **No new hook firings or hook code changes.** Per ASM-1, this is a skill-prompt-only fix. Verify that `claude-plugins/manifest-dev/hooks/` is unchanged in this branch.
  ```yaml
  verify:
    method: bash
    command: "git diff origin/main..HEAD -- claude-plugins/manifest-dev/hooks/ | wc -l | { read n; if [ \"$n\" -ne 0 ]; then echo \"FAIL: hooks/ was modified ($n diff lines) — should be untouched per skill-prompt-only scope\"; exit 1; fi; echo OK; }"
  ```

## 4. Process Guidance

- [PG-1] **Surgical edits only.** Modify only the Post-Completion Feedback section in `done/SKILL.md` and the "Triggered after /done" bullet in `escalate/SKILL.md`'s Self-Amendment section. Do not reword adjacent sections, do not "improve" unrelated text, do not add new flags or hooks. High-signal changes only — every edit must address the failure mode (descriptive→directive chain language) or the verification gates this manifest declares.
- [PG-2] **Low arousal, trusted-advisor tone.** No urgency language ("CRITICAL", "MUST IMMEDIATELY"), no emotional pressure ("don't fail the user"), no excessive emphasis. Use direct imperative ("Invoke ...", "Both steps are mandatory.") in calm voice. Match the existing tone of `done/SKILL.md` and `escalate/SKILL.md`.
- [PG-3] **Write manifest and execution log incrementally and in chunks.** Per user direction during discovery — do not write entire files in single Write calls. Use Edit with append-style additions for the manifest, and append to the execution log after each AC attempt (matches `/do`'s Memento Pattern: "After EACH AC attempt, append what happened and the outcome").

## 5. Known Assumptions

- [ASM-1] **Skill-prompt-only fix.** Default: no new hooks, no `stop_do_hook` changes. Impact if wrong: post-/done chain still skipped despite clearer wording — follow-up adds a UserPromptSubmit hook that fires when `has_done=true` and a recent `/define --amend` invocation is not followed by `/do`. (Inherited from prior user direction "don't pollute context after done unnecessarily.")
- [ASM-2] **`--scope <new-or-affected-deliverables>` guidance preserved.** Default: agent infers scope from the amendment log entries. Impact if wrong: full `/do` runs instead of selective — slower but still correct (full final gate already catches cross-deliverable issues).
- [ASM-3] **`/define`'s Complete section unchanged.** Default: `/define` stays a leaf skill that outputs path and stops. Impact if wrong: chain logic could fragment between `done/SKILL.md` and `define/SKILL.md`; correctable by moving the chain orchestration if a future use case demands.
- [ASM-4] **`escalate/SKILL.md`'s "Triggered after /done" bullet uses brief mirror + cross-reference.** Default: avoid duplicating the full chain text. Impact if wrong: agents reading escalate without reading done miss part of the chain — cross-reference points them at the canonical source.
- [ASM-5] **Plugin version bump: minor (0.92.0 → 0.93.0).** Default: behavioral fix that strengthens an existing feature warrants minor per CLAUDE.md convention. Impact if wrong: easily corrected (version bump is a one-line change).
- [ASM-6] **README updates not required.** Default: this is a behavioral fix to existing post-/done flow; no new components, no description-level capability change. Impact if wrong: easily added; current READMEs already mention `/done` and amendment behavior at a high level.
- [ASM-7] **`auto/SKILL.md` unchanged.** Default: `/auto`'s explicit chain is the *pattern* this fix mirrors, but `/auto` itself doesn't need modification. Impact if wrong: easily added in follow-up if a regression appears.

## 6. Deliverables

### Deliverable D1: Rewrite `done/SKILL.md` Post-Completion Feedback section — explicit ordered chain

**Acceptance Criteria:**

- [AC-1.1] The Post-Completion Feedback section in `claude-plugins/manifest-dev/skills/done/SKILL.md` contains an explicit, numbered, ordered list of steps for amendment-worthy feedback (Step 1: invoke `/define --amend ...`; Step 2: invoke `/do ...`). The phrasing uses imperative invocation language ("Invoke the manifest-dev:define skill with: ...") matching `/auto`'s pattern.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/done/SKILL.md. In the 'Post-Completion Feedback' section, verify: (1) an explicit numbered/ordered list documents the re-entry steps; (2) Step 1 invokes /define --amend with the manifest path; (3) Step 2 invokes /do with manifest path, log path, and optional --scope; (4) imperative invocation language is used (e.g., 'Invoke the manifest-dev:define skill with: ...'), matching the pattern in claude-plugins/manifest-dev/skills/auto/SKILL.md. PASS if all four hold; FAIL otherwise."
  ```

- [AC-1.2] The section explicitly states that **both steps are mandatory** and names the failure mode of stopping after step 1 (e.g., "Stopping after step 1 leaves the manifest amended but unimplemented and unverified"). This anti-failure framing is the load-bearing language that closes the descriptive→directive gap.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md. Verify: (1) the section explicitly states that both re-entry steps are mandatory (using direct language like 'Both steps are mandatory' or equivalent); (2) the section names the failure mode of stopping after step 1 (the manifest is amended but unimplemented/unverified, or equivalent characterization). PASS if both hold; FAIL if either is missing or hedged with weak language ('try to', 'maybe', 'should')."
  ```

- [AC-1.3] The pure-question carve-out is preserved with concrete examples ("What does AC-1.1 require?" / "Why approach A?"). Existing wording continues to distinguish state-change feedback (amend) from inquiry (inline answer). When ambiguous, default-to-amend behavior is preserved.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md. Verify: (1) the pure-question carve-out is preserved with concrete examples distinguishing state-change feedback (amend) from inquiry (inline answer); (2) the asymmetric default-to-amend rule for ambiguous cases is preserved (silent scope drift treated as the worse failure). PASS if both preserved; FAIL if dropped or substantively weakened."
  ```

- [AC-1.4] The no-manifest fail-open case is preserved verbatim — when /do completed without a manifest in scope, post-completion feedback falls back to inline handling.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md. Verify the no-manifest case is documented: when /do somehow completed without a manifest in scope, post-completion feedback falls back to inline handling (fail-open). PASS if present; FAIL if removed or weakened."
  ```

- [AC-1.5] The manifest-in-scope detection paragraph is preserved — judgment-based, no session boundary, ask user once when ambiguous.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md. Verify the manifest-in-scope detection guidance is preserved: judgment-based, no session boundary, ask user once when ambiguous. PASS if preserved; FAIL if removed or substantively changed."
  ```

- [AC-1.6] Step 1 explicitly notes that `/define --amend` inherits the manifest's recorded `Interview:` style — "with or without questions as needed" per the user's framing maps to the manifest's interview field (autonomous = no questions, thorough = questions, minimal = light probing).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md. Verify Step 1 (the /define --amend invocation step) notes that the amendment's interview style is inherited from the manifest's recorded Interview field — autonomous manifests amend without questions, thorough manifests probe, minimal manifests do light probing. PASS if explicit; FAIL if missing or vague."
  ```

- [AC-1.7] Step 2 specifies how `--scope` is determined (new-or-affected-deliverables inferred from the amendment log) and notes that `/do`'s mandatory full final gate runs unconditionally before `/done` becomes reachable.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md. Verify Step 2 (the /do invocation step): (1) specifies how --scope is determined (new-or-affected-deliverables, inferred from the amendment); (2) notes that /do's mandatory full final gate runs unconditionally before /done can be reached (cross-references existing /verify selective→full machinery). PASS if both; FAIL if either missing."
  ```

- [AC-1.8] The amendment loop guard (R-7 in `do/SKILL.md`) is referenced or its constraint is preserved in the post-/done case — repeated Self-Amendment without external input escalates as Proposed Amendment.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the 'Post-Completion Feedback' section of claude-plugins/manifest-dev/skills/done/SKILL.md and claude-plugins/manifest-dev/skills/do/SKILL.md. Verify that the amendment loop guard (consecutive amendments without external input → escalate as Proposed Amendment) applies to the post-/done re-entry case — either via explicit reference in done/SKILL.md or via existing language in do/SKILL.md that already covers the post-/done case. PASS if covered; FAIL if the guard does not apply to post-/done re-entry."
  ```

- [AC-1.9] The mandatory trailing italic line in `/done`'s output template ("Post-completion feedback defaults to amending this manifest. Send a message describing the change; pure questions are answered inline.") is preserved unchanged. Composition with the rewritten Post-Completion Feedback section is coherent — the trailing line stays a one-line user-facing reminder; the section provides the agent-facing chain logic.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/done/SKILL.md. Verify: (1) the mandatory trailing italic line in the Output Format section ('Post-completion feedback defaults to amending this manifest. Send a message describing the change; pure questions are answered inline.') is preserved; (2) it is still labeled mandatory in /done's output. PASS if both; FAIL if the line was removed, modified beyond cosmetic fixes, or no longer marked mandatory."
  ```

### Deliverable D2: Mirror the chain in `escalate/SKILL.md` Self-Amendment "Triggered after /done" bullet

**Acceptance Criteria:**

- [AC-2.1] The "Triggered after /done" bullet in `escalate/SKILL.md`'s Self-Amendment section presents the same two-step chain (define-amend → do) in summary form and cross-references `done/SKILL.md` Post-Completion Feedback as the canonical source.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/escalate/SKILL.md. In the Self-Amendment section, find the 'Re-entry depends on the trigger source' bullet list. For the 'Triggered after /done' bullet, verify: (1) the two-step chain (define --amend, then /do) is presented in summary form using imperative language; (2) it explicitly cross-references done/SKILL.md Post-Completion Feedback as the canonical source. PASS if both; FAIL if either missing."
  ```

- [AC-2.2] The "Triggered from /do or /verify" bullet (the autonomous fast path with `--from-do`) is preserved — only the post-/done bullet is modified.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/escalate/SKILL.md Self-Amendment section's 'Re-entry depends on the trigger source' bullet list. Verify the 'Triggered from /do or /verify' bullet (autonomous fast path: /define --amend <path> --from-do, then /do resumes) is preserved unchanged. PASS if preserved; FAIL if modified."
  ```

- [AC-2.3] The Self-Amendment escalation template block (`## Escalation: Self-Amendment` markdown block) is preserved unchanged.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/escalate/SKILL.md. Verify the Self-Amendment escalation template block (the markdown fence containing '## Escalation: Self-Amendment', Trigger, Affected items, What changed, Manifest path, Execution log path) is preserved unchanged. PASS if preserved; FAIL if modified."
  ```

### Deliverable D3: Plugin version bump

**Acceptance Criteria:**

- [AC-3.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is bumped from `0.92.0` to `0.93.0`.
  ```yaml
  verify:
    method: bash
    command: "v=$(python3 -c 'import json; print(json.load(open(\"claude-plugins/manifest-dev/.claude-plugin/plugin.json\"))[\"version\"])'); test \"$v\" = '0.93.0' && echo OK || { echo \"FAIL: version is $v, expected 0.93.0\"; exit 1; }"
  ```

- [AC-3.2] Marketplace registry (`.claude-plugin/marketplace.json`) reflects the bumped version if it pins manifest-dev's version.
  ```yaml
  verify:
    method: bash
    command: "if grep -q '\"manifest-dev\"' .claude-plugin/marketplace.json && grep -A5 '\"manifest-dev\"' .claude-plugin/marketplace.json | grep -q 'version'; then v=$(python3 -c 'import json; m=json.load(open(\".claude-plugin/marketplace.json\")); plugins=m.get(\"plugins\", []); p=[x for x in plugins if x.get(\"name\")==\"manifest-dev\"]; print(p[0].get(\"version\",\"\") if p else \"\")'); if [ \"$v\" != '0.93.0' ] && [ -n \"$v\" ]; then echo \"FAIL: marketplace pins manifest-dev to $v, expected 0.93.0 or unpinned\"; exit 1; fi; fi; echo OK"
  ```

### Deliverable D4: sync-tools regeneration of distributions (runs LAST)

*Per user direction: invoke `sync-tools` after all other deliverables are done and verified. This is the final wrap-up step — its AC verifies that dist files reflect source post-sync (covered by INV-G5 above; this deliverable's AC asserts sync-tools was invoked and completed without errors).*

**Acceptance Criteria:**

- [AC-4.1] The `sync-tools` skill was invoked successfully (no errors, no failures) after D1–D3 verification passed.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read the execution log for this manifest. Verify that the sync-tools skill was invoked AFTER deliverables D1, D2, and D3 had passed verification, and that the sync-tools invocation completed without errors. PASS if sync-tools invocation is logged after the D1-D3 pass with successful outcome. FAIL if sync-tools was not invoked, was invoked before D1-D3 verification, or reported errors."
  ```

- [AC-4.2] After sync-tools runs, `git status` shows no uncommitted changes that suggest sync-tools generated unrelated/unexpected modifications. Only `dist/` regeneration plus the source edits in D1/D2/D3 should appear.
  ```yaml
  verify:
    method: bash
    command: "git status --porcelain | awk '{print $2}' | sort -u | { read -r line || true; while [ -n \"$line\" ]; do case \"$line\" in dist/*|claude-plugins/manifest-dev/skills/done/SKILL.md|claude-plugins/manifest-dev/skills/escalate/SKILL.md|claude-plugins/manifest-dev/.claude-plugin/plugin.json|.claude/skills/done/SKILL.md|.claude/skills/escalate/SKILL.md|.claude-plugin/marketplace.json) ;; *) echo \"FAIL: unexpected modified path $line\"; exit 1 ;; esac; read -r line || break; done; echo OK; }"
    phase: 2
  ```

---

*End of manifest. Execution order: D1 → D2 → D3 → (verify D1–D3 + INV-G1..G4, G6, G7) → D4 → (verify INV-G5 + AC-4.1, AC-4.2 in phase 2). The full final gate per `/verify`'s selective→full chain runs unconditionally before `/done` becomes reachable.*


