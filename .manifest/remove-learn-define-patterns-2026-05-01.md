# Definition: Remove unused learn-define-patterns skill

## 1. Intent & Context

- **Goal:** Remove the `learn-define-patterns` skill (and its sole-consumer agent `define-session-analyzer`) from the manifest-dev plugin and all synced distributions, since the skill is unused. After removal, no references to either component remain anywhere in the active codebase, the test suite still passes, and the plugin remains installable on every supported CLI.
- **Mental Model:** This is a pure deletion. The skill is single-file, the agent serves only this skill, and references are concentrated in three places: (1) source plugin files, (2) `dist/{codex,gemini,opencode}/` mirrored copies, (3) READMEs / plugin metadata / a single test file. The historical `.manifest/learn-define-patterns-2026-03-01.md` is intentionally preserved as an audit trail.
- **Mode:** thorough
- **Interview:** autonomous

## 2. Approach

- **Architecture:** Subtractive cleanup, ordered to keep the tree consistent at every step:
    1. Delete the skill directory and its `.claude/` symlink (source of truth gone).
    2. Delete the orphaned `define-session-analyzer` agent.
    3. Update plugin metadata: bump `plugin.json` version (0.95.0 → 0.96.0), prune skill-specific keywords.
    4. Update READMEs (root, `claude-plugins/`, plugin) to remove rows / list mentions.
    5. Update `tests/test_dist_skill_references.py` — delete the two assertions naming `learn-define-patterns-manifest-dev`.
    6. Delete dist mirrors for all three CLIs (skill dir + agent file + opencode command + opencode/codex installer/config entries + GEMINI.md / AGENTS.md / README mentions).
    7. Delete sync-tools `references/{codex,gemini,opencode}-cli.md` paragraphs that document `learn-define-patterns`-specific substitution rules (dead documentation post-removal).
    8. Run lint/format/typecheck and `pytest tests/test_dist_skill_references.py` to confirm green.

- **Execution Order:**
    - D1 → D2 → D3 → D4 → D5 → D6 → D7 → D8
    - Rationale: source-of-truth files first, then metadata, then tests, then dist mirrors, then sync-tools docs, with the verification gate last so it observes the fully clean state.

- **Risk Areas:**
    - [R-1] A reference to `learn-define-patterns` or `define-session-analyzer` slips through (especially in dist/ which has many small mentions). | Detect: AC-G1 (full-tree grep returns zero hits in non-archival paths).
    - [R-2] `dist/codex/config.toml` retains an orphan `[agents.define-session-analyzer]` section pointing at a deleted TOML file. | Detect: AC-4.2 specifically targets config.toml.
    - [R-3] `.claude/skills/learn-define-patterns` symlink left dangling after source dir removed. | Detect: AC-1.2 verifies the symlink path is absent.
    - [R-4] Test suite assertions still reference removed skill name → CI red. | Detect: AC-G2 (`pytest tests/test_dist_skill_references.py` passes).

- **Trade-offs:**
    - [T-1] Manual dist deletion vs running /sync-tools → Prefer manual deletion because the operation is purely subtractive, well-bounded, and avoids coupling correctness to /sync-tools' delete-handling path. (PG-1 codifies this.)
    - [T-2] Major vs minor version bump → Prefer minor (0.96.0). Removing an unused user-invocable skill is technically breaking, but the user states it's unused, the repo treats new-skill addition as minor, and no precedent calls for major on removal.
    - [T-3] Keep `.manifest/learn-define-patterns-2026-03-01.md` vs delete → Prefer keep. Archival manifests document history and don't affect runtime; deleting them would erase audit trail.

## 3. Global Invariants

- [INV-G1] No active-code reference to `learn-define-patterns` or `define-session-analyzer` survives anywhere in the repo, except in `.manifest/` (historical archival) and in `git log` / commit messages. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      hits=$(grep -rEn "learn-define-patterns|define-session-analyzer|learn_define_patterns|define_session_analyzer" \
        --include="*.md" --include="*.json" --include="*.py" --include="*.toml" --include="*.ts" --include="*.yml" --include="*.yaml" \
        . 2>/dev/null \
        | grep -v "^./\.manifest/" \
        | grep -v "^./\.git/" || true)
      if [ -n "$hits" ]; then
        echo "FAIL: stale references found:"; echo "$hits"; exit 1
      fi
      echo "PASS: no active references"
  ```

- [INV-G2] Lint, format, and typecheck pass on `claude-plugins/`. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy"
  ```

- [INV-G3] `pytest tests/test_dist_skill_references.py` produces **no new failures** vs the pre-change baseline. (Amended: 8 tests in this file fail on the base branch unrelated to this change — `test_namespaced_skill_handoffs_are_installed_safely`, `test_codex_reference_guide_uses_namespaced_dollar_invocations`, `test_opencode_readme_distinguishes_commands_from_internal_skills`, `test_gemini_docs_describe_extension_skills_not_slash_commands`, `test_gemini_installer_outputs_skill_usage_guidance`, `test_verification_model_defaults_to_inherit_across_source_and_dist`, `test_opencode_installer_preserves_root_plugin_and_config`, `test_gemini_installer_merges_settings_additively`. Per PG-2, those are out of scope. The previously-passing test, `test_sync_tools_docs_require_complete_additive_installs`, must still pass; the failure set must be ⊆ the baseline set.) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      set -e
      passed_test='test_sync_tools_docs_require_complete_additive_installs'
      baseline_failures='test_namespaced_skill_handoffs_are_installed_safely test_codex_reference_guide_uses_namespaced_dollar_invocations test_opencode_readme_distinguishes_commands_from_internal_skills test_gemini_docs_describe_extension_skills_not_slash_commands test_gemini_installer_outputs_skill_usage_guidance test_verification_model_defaults_to_inherit_across_source_and_dist test_opencode_installer_preserves_root_plugin_and_config test_gemini_installer_merges_settings_additively'
      out=$(pytest tests/test_dist_skill_references.py --tb=no -q 2>&1 || true)
      echo "$out" | tail -20
      echo "$out" | grep -qE "PASSED.*${passed_test}|${passed_test}.*PASSED" || \
        pytest tests/test_dist_skill_references.py::${passed_test} -v
      current_failures=$(echo "$out" | grep -oE 'FAILED tests/test_dist_skill_references.py::[a-zA-Z_]+' | sed 's|.*::||' | sort -u)
      for f in $current_failures; do
        echo " $baseline_failures " | grep -q " $f " || { echo "NEW FAILURE: $f"; exit 1; }
      done
      echo "PASS: previously-passing test still passes; no new failures vs baseline"
  ```

- [INV-G4] No NEW test regressions introduced by this change. (Amended: tests/ has pre-existing failures unrelated to learn-define-patterns removal; the gate is "this change introduces no new failures", not "all tests pass".) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      git stash --include-untracked --quiet
      base_out=$(pytest tests/ --tb=no -q 2>&1 || true)
      git stash pop --quiet
      head_out=$(pytest tests/ --tb=no -q 2>&1 || true)
      base_fail=$(echo "$base_out" | grep -oE 'FAILED [^ ]+' | sort -u)
      head_fail=$(echo "$head_out" | grep -oE 'FAILED [^ ]+' | sort -u)
      new=$(comm -13 <(echo "$base_fail") <(echo "$head_fail") | grep -v '^$' || true)
      if [ -n "$new" ]; then
        echo "FAIL: new regressions:"; echo "$new"; exit 1
      fi
      echo "PASS: no new failures introduced by this change"
  ```

- [INV-G5] No stale or dangling symlinks under `.claude/skills/`. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      bad=$(find .claude/skills -maxdepth 2 -type l ! -exec test -e {} \; -print 2>/dev/null || true)
      if [ -n "$bad" ]; then echo "FAIL: dangling symlinks:"; echo "$bad"; exit 1; fi
      echo "PASS"
  ```

## 4. Process Guidance

- [PG-1] Do not run `/sync-tools` as part of this change. Apply dist edits directly — the operation is purely subtractive and the explicit edits are auditable in the diff.
- [PG-2] Only edit lines/files that name `learn-define-patterns` or `define-session-analyzer`. Don't tidy unrelated stale references discovered along the way (scope creep).
- [PG-3] Preserve `.manifest/learn-define-patterns-2026-03-01.md` unchanged — historical archive.
- [PG-4] Preserve every commit message / git history mention — never rewrite history for this change.

## 5. Known Assumptions

- [ASM-1] Version bump policy: minor (0.95.0 → 0.96.0). Default chosen because the user said the skill is unused (no real consumer), and the repo's convention for adding/removing skills is minor. Impact if wrong: a downstream user whose tooling actually depended on this skill upgrades silently and discovers it missing.
- [ASM-2] The historical `.manifest/learn-define-patterns-2026-03-01.md` is preserved. Impact if wrong: minor (file remains; if user wanted it removed they'll say so).
- [ASM-3] Removing dist mirrors directly (rather than re-running /sync-tools post-source-deletion) produces the same end state. Impact if wrong: dist `.sync-meta.json` records pre-deletion SHA, but next /sync-tools run will delta-sync the deletion forward — so no real divergence.

## 6. Deliverables

### Deliverable 1: Source skill directory and symlink removed

**Acceptance Criteria:**
- [AC-1.1] `claude-plugins/manifest-dev/skills/learn-define-patterns/` does not exist. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -e claude-plugins/manifest-dev/skills/learn-define-patterns && echo PASS"
  ```
- [AC-1.2] `.claude/skills/learn-define-patterns` (symlink path) does not exist. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -e .claude/skills/learn-define-patterns && test ! -L .claude/skills/learn-define-patterns && echo PASS"
  ```

### Deliverable 2: Orphaned define-session-analyzer agent removed

**Acceptance Criteria:**
- [AC-2.1] `claude-plugins/manifest-dev/agents/define-session-analyzer.md` does not exist. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -e claude-plugins/manifest-dev/agents/define-session-analyzer.md && echo PASS"
  ```

### Deliverable 3: READMEs updated

**Acceptance Criteria:**
- [AC-3.1] Root `README.md` contains no reference to the removed skill or agent. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -E 'learn-define-patterns|define-session-analyzer' README.md && echo PASS"
  ```
- [AC-3.2] `claude-plugins/README.md` contains no reference. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -E 'learn-define-patterns|define-session-analyzer' claude-plugins/README.md && echo PASS"
  ```
- [AC-3.3] `claude-plugins/manifest-dev/README.md` contains no reference. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -E 'learn-define-patterns|define-session-analyzer' claude-plugins/manifest-dev/README.md && echo PASS"
  ```

### Deliverable 4: Dist mirrors purged across all three CLIs

**Acceptance Criteria:**
- [AC-4.1] No file under `dist/codex/`, `dist/gemini/`, or `dist/opencode/` references either name (skill dirs, agent files, command file, install_helpers entries, AGENTS.md / GEMINI.md / README.md mentions, codex config.toml block all gone). | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      hits=$(grep -rEn "learn-define-patterns|define-session-analyzer|learn_define_patterns|define_session_analyzer" dist/ 2>/dev/null || true)
      if [ -n "$hits" ]; then echo "FAIL:"; echo "$hits"; exit 1; fi
      echo "PASS"
  ```
- [AC-4.2] No directory or file named `learn-define-patterns` or `define-session-analyzer*` remains under `dist/`. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      found=$(find dist -name 'learn-define-patterns*' -o -name 'define-session-analyzer*' 2>/dev/null || true)
      if [ -n "$found" ]; then echo "FAIL:"; echo "$found"; exit 1; fi
      echo "PASS"
  ```

### Deliverable 5: Test suite updated

**Acceptance Criteria:**
- [AC-5.1] `tests/test_dist_skill_references.py` no longer asserts on `$learn-define-patterns-manifest-dev` (line 107) or `/learn-define-patterns-manifest-dev` (line 119). | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -E 'learn-define-patterns|define-session-analyzer' tests/test_dist_skill_references.py && echo PASS"
  ```

### Deliverable 6: plugin.json metadata updated

**Acceptance Criteria:**
- [AC-6.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version is bumped to `0.96.0`. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json,sys; v=json.load(open(\"claude-plugins/manifest-dev/.claude-plugin/plugin.json\"))[\"version\"]; print(v); sys.exit(0 if v==\"0.96.0\" else 1)'"
  ```
- [AC-6.2] `plugin.json` keywords no longer contain `"learn"`, `"patterns"`, or `"preferences"`. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      python3 -c '
      import json, sys
      kw = json.load(open("claude-plugins/manifest-dev/.claude-plugin/plugin.json"))["keywords"]
      bad = [k for k in kw if k in ("learn", "patterns", "preferences")]
      print("bad:", bad)
      sys.exit(1 if bad else 0)
      '
  ```

### Deliverable 7: sync-tools reference docs cleaned

**Acceptance Criteria:**
- [AC-7.1] `.claude/skills/sync-tools/references/codex-cli.md`, `gemini-cli.md`, and `opencode-cli.md` no longer mention `learn-define-patterns` (the skill-specific paragraphs documenting per-CLI sync rules for it are removed). Surrounding context (e.g., generic notes about session-file paths in `define/SKILL.md`) may be retained — only the `learn-define-patterns`-specific text is excised. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "! grep -E 'learn-define-patterns|define-session-analyzer' .claude/skills/sync-tools/references/codex-cli.md .claude/skills/sync-tools/references/gemini-cli.md .claude/skills/sync-tools/references/opencode-cli.md && echo PASS"
  ```

### Deliverable 8: Verification gates green

**Acceptance Criteria:**
- [AC-8.1] (Same as INV-G2) Lint, format, typecheck pass. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy"
  ```
- [AC-8.2] (Same as INV-G3, amended) The previously-passing test in `tests/test_dist_skill_references.py` still passes; the failure set is ⊆ the pre-change baseline. | Verify: bash
  ```yaml
  verify:
    method: bash
    command: |
      set -e
      passed_test='test_sync_tools_docs_require_complete_additive_installs'
      baseline_failures='test_namespaced_skill_handoffs_are_installed_safely test_codex_reference_guide_uses_namespaced_dollar_invocations test_opencode_readme_distinguishes_commands_from_internal_skills test_gemini_docs_describe_extension_skills_not_slash_commands test_gemini_installer_outputs_skill_usage_guidance test_verification_model_defaults_to_inherit_across_source_and_dist test_opencode_installer_preserves_root_plugin_and_config test_gemini_installer_merges_settings_additively'
      out=$(pytest tests/test_dist_skill_references.py --tb=no -q 2>&1 || true)
      echo "$out" | tail -20
      pytest tests/test_dist_skill_references.py::${passed_test} -v
      current_failures=$(echo "$out" | grep -oE 'FAILED tests/test_dist_skill_references.py::[a-zA-Z_]+' | sed 's|.*::||' | sort -u)
      for f in $current_failures; do
        echo " $baseline_failures " | grep -q " $f " || { echo "NEW FAILURE: $f"; exit 1; }
      done
      echo "PASS"
  ```
