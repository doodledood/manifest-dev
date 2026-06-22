# Definition: Autonomous `/goal` posture + reliable emission + proactive fog-clearing

## 1. Intent & Context
- **Goal:** Make the manifest-dev `/goal` machinery encode the figure-out **autonomous operating posture** — "clear all fog that can be cleared without human intervention" — in three ways: (1) the posture rides inside every printed `/goal` string so the backstop is self-contained; (2) the print itself becomes a reliable first-action (figure-out `--autonomous` was observed continuing without emitting it, and `auto` never emits it at all); (3) `autonomous.md` itself states the proactive fog-clearing principle, not just reactive per-question self-answering. Builds incrementally on the prior PR (commit `7182baf`) that already turned these `/goal` strings into measurable completion conditions.
- **Mental Model:** A `/goal` is the host CLI's turn-continuation wrapper: a fresh-model evaluator judges the **transcript** (not files) against the goal after each turn and re-opens the turn until the condition holds. The goal string is the one artifact that survives compaction or a copy-paste into a fresh session (e.g. a `/do` run that never loaded `autonomous.md`), so it must carry the operating posture, not just the stop condition. The posture clause is kept **distinct** from the completion condition so the evaluator's done-test stays crisp. This is a prompt change governed by gap-calibration: close the real gap with the minimum edit — no mechanism-as-prescription, no enumerated checklist, no split-rule duplication. All edited skills are `sync-tools`-governed shared assets (copies live under `dist/{codex,opencode,pi}`); several ship under `dist/pi/`, so this is a Pi-distributed shared-asset change. **Pi has no `/goal`**, so `sync-tools` drops the goal block from Pi dist while Codex/OpenCode keep the concrete `/goal`.

## 2. Approach
- **Architecture:** Edit the canonical source under `claude-plugins/manifest-dev/skills/...` (the `.claude/` paths resolve to it via symlink). Then run the deterministic pipeline: bump versions, regenerate dist via `sync-tools`, run the lint/format/type gate, commit, push, open PR.
- **Execution Order:**
  - D1 (prompt edits) → D2 (versioning, dist sync, gates, PR)
  - Rationale: distribution and verification must reflect the final prompt text.
- **Risk Areas:**
  - [R-1] The "fix" adds bulk — a new heading/section in `autonomous.md` or an enumerated probe/posture checklist. Detect: AC-1.7 anti-bloat numstat + INV-G2 review-prompt flags mechanism-as-prescription.
  - [R-2] The proactive fog-clearing principle restates the master-frame "explore instead of asking" instead of intensifying it (split-rule duplication). Detect: AC-1.3 checks it reads as a mode-specific intensification, not a near-verbatim restatement; INV-G2 review-prompt split-rule check.
  - [R-3] The posture clause gets folded INTO the completion condition, muddying the evaluator's done-test. Detect: AC-1.1 checks the posture is a distinct clause, not part of the measurable end state.
  - [R-4] dist copies drift from source if `sync-tools` isn't re-run. Detect: AC-2.3 re-runs sync and asserts clean `git status`.
  - [R-5] The Pi drop is incomplete (a `/goal` block leaks into Pi dist) or over-broad (strips surrounding non-goal prose). Detect: AC-2.3 checks Pi dist carries no `/goal` token in the affected skills while Codex/OpenCode do, and surrounding content survives.
  - [R-6] A hardcoded turn bound replaces the user-filled placeholder. Detect: AC-1.1 + INV-G2; ASM-3 keeps it a placeholder.
- **Trade-offs:**
  - [T-1] Posture as a distinct appended clause vs. woven into the completion condition → Prefer the distinct clause (user decision) so the fresh-model evaluator's "is it done?" test stays a crisp measurable end state.
  - [T-2] Reliable emission via prompt-salience vs. an explicit signal `/auto` passes to suppress nested prints → Prefer prompt-salience (user decision): the `/auto` invocation is already visible in-transcript, so detection was never the failure — directive salience was; an explicit flag is a call-contract change that trips the same anti-bloat gates. Suppression fails TOWARD printing (when unsure, print) because a missing backstop is worse than a redundant one.

## 3. Global Invariants
- [INV-G1] The change matches its stated intent — the three-part `/goal` posture/emission/mode-prose change plus the required version bumps and regenerated dist — and nothing more (no scope creep).
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff on branch
      claude/goal-manual-messaging-0tgd43 (compare against origin/main). Stated intent has three parts:
      (A) a tight autonomous-posture clause ("resolve every question you can yourself; record low-confidence calls
      as assumptions; only halt for a blocker that genuinely needs the user") added to the printed /goal strings in
      figure-out references/autonomous.md, define/SKILL.md, and auto/SKILL.md, plus the three READMEs' goal examples
      — kept distinct from the measurable completion condition;
      (B) reliable emission — figure-out autonomous.md's print directive strengthened to a salient first action with
      suppression that fails toward printing; auto/SKILL.md gaining an ACTIVE print instruction (it previously only
      documented the goal);
      (C) autonomous.md gaining a proactive "clear all fog clearable without human intervention" principle folded
      into existing prose.
      Plus version bumps (manifest-dev plugin minor; Pi packages + pi-cli.md example; opencode mirror) and
      regenerated dist copies. PASS only if the diff does ONLY (A)+(B)+(C)+versioning+dist — no unrelated changes,
      no touched files outside the named set (and the merge of origin/main is not counted as a change). PASS only if
      no LOW-or-higher findings. Report findings with severity.
    phase: 2
  ```
- [INV-G2] The edited prompt text passes gap-calibration review.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review the edited prompt files —
      claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md,
      claude-plugins/manifest-dev/skills/define/SKILL.md, and
      claude-plugins/manifest-dev/skills/auto/SKILL.md — against gap-calibration discipline. Check especially:
      (1) every added/retained line closes a real gap a capable model wouldn't reach on its own;
      (2) no mechanism-as-prescription — the posture clause and the proactive fog-clearing principle are tuned
      guidance, NOT an enumerated/hardcoded checklist; the /goal turn bound stays a user-filled placeholder, never a
      hardcoded number;
      (3) no split-rule duplication — the proactive fog-clearing principle in autonomous.md intensifies the
      master-frame "explore instead of asking" rather than restating it near-verbatim; the no-chain-into-execution
      stop is not duplicated across files;
      (4) the autonomous-posture clause reads as operating guidance distinct from the measurable completion
      condition, so it does not muddy the /goal evaluator's done-test.
      PASS only if no MEDIUM-or-higher findings. Report findings with severity.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Edit the canonical source under `claude-plugins/manifest-dev/skills/...`, never a `dist/` copy or the `.claude/` symlink target directly. dist copies are regenerated, not hand-edited.
- [PG-2] Treat this as an *update* audit, not a rewrite: preserve effective existing language; change only the lines that carry the gap (high-signal changes only).

## 5. Known Assumptions
- [ASM-1] (auto) The plugin to version-bump is `manifest-dev`, bumped MINOR (2.14.0 → 2.15.0) because the goal-posture/emission work adds a capability. Impact if wrong: wrong level; trivially corrected.
- [ASM-2] (auto) Because edited skills ship under `dist/pi/`, the repo-root `package.json` and `packages/manifest-dev-pi-tools/package.json` are Pi-distributed shared assets and are bumped 0.11.3 → 0.11.4 in lockstep, with `sync-tools/references/pi-cli.md`'s version example kept matching and `dist/opencode/plugin/package.json` set to the new plugin version (2.15.0) by sync-tools. Impact if wrong: a harmless extra bump, or a desynced Pi package if omitted.
- [ASM-3] (auto) The optional turn/time bound in every printed `/goal` stays a **user-filled placeholder** ("Stop after N turns…"), never a hardcoded number. Impact if wrong: an arbitrary cap could cut off or fail to bound a legitimate run.
- [ASM-4] (auto) `plugin.json`'s description, which describes `/goal` only at a high level ("completion condition", no literal printed-goal string), needs NO posture clause — only the version bump. Impact if wrong: a missed prose touch-up; cosmetic.
- [ASM-5] (auto) `manifest-dev-tools` plugin (0.26.0) is NOT bumped — no tools-plugin skill changes (figure-out/define/auto all live in the `manifest-dev` plugin). Impact if wrong: a missed bump on an unaffected package; cosmetic.
- [ASM-6] (auto) The three READMEs' `/goal` examples receive the same posture clause for consistency with the printed strings; the explanatory prose around them is preserved. Impact if wrong: minor doc inconsistency.

## 6. Deliverables

### Deliverable 1: Prompt content, emission, and mode-prose edits

**Acceptance Criteria:**
- [AC-1.1] Each of the three printed `/goal` strings (figure-out `references/autonomous.md`, `define/SKILL.md` Complete handoff, `auto/SKILL.md`) carries the autonomous-posture clause as a clause **distinct** from the measurable completion condition, and the turn bound remains a user-filled placeholder.
  ```yaml
  verify:
    prompt: |
      Read the printed /goal strings in:
      claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md,
      claude-plugins/manifest-dev/skills/define/SKILL.md (Complete handoff block), and
      claude-plugins/manifest-dev/skills/auto/SKILL.md.
      PASS only if ALL hold for each of the three:
      (a) the /goal still contains its measurable completion condition (Read named with full anatomy / every AC and
      GI PASS and /done reported / full-chain complete — as appropriate to that surface);
      (b) it ALSO contains an autonomous-operating-posture clause meaning: resolve every question you can yourself
      with best judgment, record low-confidence calls as assumptions to revisit, and only halt for a blocker that
      genuinely needs the user;
      (c) the posture clause is grammatically/visually distinct from the completion condition (a separate clause or
      sentence), not fused into the measurable end state;
      (d) any turn bound remains a user-filled placeholder (e.g. "Stop after N turns…"), with no hardcoded number.
      FAIL if any of the three lacks the posture, fuses it into the completion condition, or hardcodes a turn bound.
      Report the exact /goal text from each file.
    phase: 1
  ```
- [AC-1.2] figure-out `autonomous.md` makes emitting the `/goal` a salient first action, and the nested-suppression rule fails toward printing.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if ALL hold:
      (a) emitting the copy-pasteable /goal backstop is framed as an explicit FIRST action on autonomous
      activation (before pressing the topic) — strengthened from a single passing mention into an unambiguous
      directive;
      (b) the "don't print a nested /goal when chained under /auto" suppression is conditioned so that it only
      applies when the run can CLEARLY see it is under /auto, and otherwise it PRINTS (fails toward printing /
      "when unsure, print");
      (c) no new Markdown heading/section was introduced to carry this (the change is tightened directive prose).
      FAIL if the print is still a weak single passing sentence, if suppression defaults to NOT printing when
      context is ambiguous, or if a new heading/section was added. Report exact quotes.
    phase: 1
  ```
- [AC-1.3] `autonomous.md` states the proactive "clear all fog clearable without human intervention" principle as an intensification of the master frame, folded into existing prose.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md and, for comparison, the
      "explore instead of asking" line in the figure-out master SKILL.md
      (claude-plugins/manifest-dev/skills/figure-out/SKILL.md). PASS only if:
      (a) autonomous.md now conveys a PROACTIVE principle — the mode's standing job is to uncover and resolve ALL
      fog that investigation or a defensible default can clear without a human, leaving only a genuine
      preference / unknowable-without-asking call (recorded as a low-confidence assumption) — i.e. not merely
      reactive per-posed-question self-answering;
      (b) it is phrased as a mode-specific INTENSIFICATION ("no user present → the bar to self-clear is maximal"),
      NOT a near-verbatim restatement of the master frame's "explore instead of asking";
      (c) it is folded into existing prose / the activation framing, with NO new heading/section;
      (d) the no-chain-into-execution boundary ("chaining into execution belongs to the caller", or equivalent)
      is preserved.
      FAIL if the principle is absent, is only reactive, duplicates the master line verbatim, adds a new section,
      or drops the no-execution boundary. Report exact quotes from both files.
    phase: 1
  ```
- [AC-1.4] `auto/SKILL.md` actively PRINTS the chain-completion `/goal` (with posture) at standalone run start, rather than only documenting it as user-facing prose.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/auto/SKILL.md. Before this change it only DOCUMENTED the recommended
      /goal as user-facing prose ("the recommended form is to launch /auto under a goal…") and never emitted it.
      PASS only if: (a) the skill now instructs /auto, at the start of a standalone run, to PRINT the chain-complete
      /goal backstop (figure-out Read named → manifest written → /do reports /done with all ACs/GIs PASS), carrying
      the autonomous-posture clause; (b) it remains clear that /auto is the chain-owner, so figure-out/define
      suppress their own nested /goal prints when clearly under /auto. FAIL if the goal is still only documentation
      with no active print instruction. Report exact quotes.
    phase: 1
  ```
- [AC-1.5] The three READMEs' `/goal` examples carry the posture clause, with surrounding explanatory prose preserved.
  ```yaml
  verify:
    prompt: |
      Inspect the /goal examples in README.md (root), claude-plugins/README.md, and
      claude-plugins/manifest-dev/README.md. PASS only if: (a) each recommended /goal example now includes the
      autonomous-posture clause (resolve what you can yourself / record low-confidence as assumptions / only halt
      for a genuine blocker), in addition to its measurable completion condition; (b) the explanatory prose that
      /goal is the host CLI's turn-continuation wrapper is retained; (c) no example regressed to a bare
      "/goal /do <path>" or "/goal /auto <task>" without a completion condition. FAIL if any recommended example
      lacks the posture clause or the explanation was removed. Report exact quotes with file:line.
    phase: 1
  ```
- [AC-1.6] Anti-bloat: the `autonomous.md` change stays targeted — no new heading/section and no enumerated probe/posture checklist; existing effective prose is preserved, not rewritten wholesale.
  ```yaml
  verify:
    prompt: |
      Run: git diff origin/main -- claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md
      (fall back to the branch merge-base if origin/main is unavailable). PASS only if: no new Markdown
      heading/section was added; AND no enumerated/hardcoded checklist was introduced; AND the change is targeted
      edits (strengthened print directive + suppression tweak + folded-in proactive principle + posture clause in
      the /goal) rather than a wholesale rewrite of the file's existing prose. FAIL if a new heading appeared, an
      enumerated checklist was baked in, or the existing prose was rewritten wholesale. Report the numstat and any
      added headings.
    phase: 1
  ```

### Deliverable 2: Versioning, distribution sync, gates, and PR

**Acceptance Criteria:**
- [AC-2.1] The `manifest-dev` plugin version is bumped one MINOR increment (2.14.0 → 2.15.0); `manifest-dev-tools` is unchanged.
  ```yaml
  verify:
    prompt: |
      Compare claude-plugins/manifest-dev/.claude-plugin/plugin.json version against origin/main (base 2.14.0).
      PASS only if it incremented by exactly one MINOR (minor digit +1, patch reset → 2.15.0) AND
      claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json is UNCHANGED from origin/main (still 0.26.0).
      FAIL if manifest-dev is unchanged / patch-only / major-bumped, or if manifest-dev-tools changed. Report both
      old and new versions.
    phase: 1
  ```
- [AC-2.2] The Pi package versions and the documented example are bumped/synced because `dist/pi/` shared assets changed.
  ```yaml
  verify:
    prompt: |
      Edited skills (figure-out, define, auto) ship under dist/pi/, so the repo-root package.json
      (@doodledood/manifest-dev-pi) and packages/manifest-dev-pi-tools/package.json are Pi-distributed shared
      assets. PASS only if: both package versions increased relative to origin/main (base 0.11.3) to 0.11.4 and are
      in lockstep with each other; AND the package-version example in .claude/skills/sync-tools/references/pi-cli.md
      matches the new package.json version (0.11.4); AND dist/opencode/plugin/package.json matches the new
      manifest-dev plugin version (2.15.0). FAIL on any mismatch or unbumped file. Report the versions found in each
      file.
    phase: 1
  ```
- [AC-2.3] The `dist/` copies match freshly regenerated `sync-tools` output: Codex/OpenCode keep the concrete `/goal` (now with posture), Pi drops the `/goal` block while keeping surrounding content.
  ```yaml
  verify:
    prompt: |
      Two parts. PART 1 (regeneration): Re-run the sync (invoke the manifest-dev:sync-tools skill, or its generation
      command) and confirm `git status` shows NO further changes to dist/ files — i.e. the committed dist matches
      regenerated output. PART 2 (Pi drop vs Codex/OpenCode keep): For each affected skill (figure-out
      references/autonomous.md, define/SKILL.md, auto/SKILL.md), confirm the dist/pi copy contains NO `/goal` token
      while the dist/codex and dist/opencode copies DO contain the concrete `/goal` WITH the new posture clause; and
      confirm the surrounding non-goal content (including the new proactive fog-clearing prose in autonomous.md)
      survives in the Pi copies. PASS only if BOTH parts hold. FAIL with specifics (file:line / grep results)
      otherwise.
    phase: 1
  ```
- [AC-2.4] The repo's pre-PR gate passes.
  ```yaml
  verify:
    prompt: |
      Run: ruff check claude-plugins/ && black --check claude-plugins/ && mypy. PASS only if all three exit clean
      (no lint errors, no formatting diffs, no type errors). No Python source changed, so this should pass
      untouched; FAIL and report output if any gate errors.
    phase: 1
  ```
- [AC-2.5] The work is committed and pushed to the designated branch with a non-draft PR open.
  ```yaml
  verify:
    prompt: |
      PASS only if: branch claude/goal-manual-messaging-0tgd43 exists on origin and contains the commit(s) with
      these changes; AND an open, non-draft pull request exists for that branch in the doodledood/manifest-dev
      repository. Use the available GitHub tooling to confirm PR state. FAIL if no PR exists, the PR is a draft, or
      the branch wasn't pushed. Report the PR number/URL and draft state.
    phase: 2
  ```
