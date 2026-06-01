# Definition: Babysit PR, Goal Handoff, Review PR One-Shot, Hook Removal

## 1. Intent & Context

- **Goal:** Add an author-side `/babysit-pr` tool, make `/goal /do <manifest-path>` the documented unattended execution recommendation, make `/review-pr` non-loop mode perform a meaningful one-shot PR review/advance pass, and remove manifest-dev's hook payload.
- **Mental Model:** `/do` remains the semantic contract carrier. `/goal` is only the host's turn-continuation wrapper. `/review-pr --loop` schedules repeated one-shot review passes; it does not own separate review intelligence.

## 2. Approach

- **Architecture:** Keep core manifest execution in `manifest-dev`; add the PR wrapper to `manifest-dev-tools`; remove hook code/tests/registrations; sync generated CLI distributions after source plugin edits.
- **Execution Order:**
  - D1 -> D2 -> D3 -> D4 -> D5 -> D6
  - Rationale: Source prompts and metadata define the behavior; docs and generated distributions must follow; verification runs after all affected files settle.
- **Risk Areas:**
  - [R-1] Prompt changes overfit the conversation and duplicate `/do` semantics | Detect: prompt-engineering review finds redundant or brittle lines
  - [R-2] Hook references remain in docs, plugin metadata, tests, or generated distributions | Detect: repository grep for removed hook names and hook-enforcement claims
  - [R-3] `/review-pr --loop` diverges from non-loop behavior | Detect: review-pr prompt audit confirms LOOP.md delegates to the one-shot pass
  - [R-4] New `/babysit-pr` skill is not discoverable in local skill mirrors or generated distributions | Detect: source, symlink, and dist metadata checks include `babysit-pr`
- **Trade-offs:**
  - [T-1] Long explicit `/goal` condition vs simple `/goal /do <manifest>` -> Prefer simple `/goal /do <manifest>` because `/do` owns the contract; upgrade later only if empirical runs show premature completion.
  - [T-2] Keep hooks as a safety backstop vs remove hooks -> Prefer removal for cross-CLI simplicity now that `/goal` covers turn continuation as a host-level workflow.

## 3. Global Invariants

- [INV-G1] Prompt-engineering discipline applies to all skill/prompt changes.
  ```yaml
  verify:
    prompt: "Review all changed SKILL.md and prompt-like reference files against claude-plugins/manifest-dev-tools/skills/prompt-engineering/SKILL.md and its relevant references (skills.md, review.md, agents.md if applicable). PASS only if each changed line closes a real gap, avoids duplicating natural model behavior, and holds at the edge cases in this manifest. Report FAIL with specific file/line concerns."
  ```

- [INV-G2] Generated distributions reflect source plugin state.
  ```yaml
  verify:
    prompt: "Inspect dist/codex and dist/opencode against source plugin changes. PASS only if babysit-pr, review-pr, /goal handoff text, and hook removal are reflected consistently in generated skills/commands/metadata/docs, with no stale hook plugin payloads."
  ```

- [INV-G3] Pre-PR verification is clean.
  ```yaml
  verify:
    prompt: "Run the repo's non-hook verification: ruff check claude-plugins/ && black --check claude-plugins/ && mypy && pytest tests/ -v. PASS only if all commands exit 0."
  ```

## 4. Process Guidance

- [PG-1] Use prompt-engineering calibration before and after prompt edits; prefer replacements over additive walls.
- [PG-2] Treat hook deletion as a product behavior change, not a mechanical cleanup; remove the claims that hooks enforce completion.
- [PG-3] Do not push or open a PR; create one local conventional commit on the new branch.

## 5. Known Assumptions

- [ASM-1] The simple `/goal /do <manifest-path>` recommendation is acceptable until empirical use shows premature goal completion | Default: keep simple | Impact if wrong: docs and handoff text later grow an explicit `until /done or /escalate` suffix.
- [ASM-2] Removing hooks warrants a major version bump for `manifest-dev` | Default: bump to 2.0.0 | Impact if wrong: release consumers may see a larger-than-expected version change.
- [ASM-3] Adding `/babysit-pr` is a minor feature for `manifest-dev-tools` | Default: bump to 0.16.0 | Impact if wrong: version semantics can be adjusted before release.

## 6. Deliverables

### Deliverable 1: Babysit PR Skill

**Acceptance Criteria:**
- [AC-1.1] `manifest-dev-tools` contains a user-invocable `babysit-pr` skill that accepts a PR URL or `--manifest <path>`, delegates synthesis to `manifest-dev:define --babysit <pr-url> --autonomous` when needed, and hands off to `/goal /do <manifest-path>`.
  ```yaml
  verify:
    prompt: "Inspect claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md. PASS only if it is thin, does not duplicate github-pr-lifecycle logic, handles PR URL vs --manifest conflicts, and names /goal /do <manifest-path> as the unattended command."
  ```

- [AC-1.2] Local skill mirrors and distribution metadata include `babysit-pr`.
  ```yaml
  verify:
    prompt: "Confirm .claude/skills/babysit-pr and .agents/skills/babysit-pr exist as intended, and generated dist metadata includes babysit-pr for both Codex and OpenCode after sync. PASS only if all are present or a documented environment limitation explains any missing local symlink."
  ```

### Deliverable 2: Goal Handoff Copy

**Acceptance Criteria:**
- [AC-2.1] `/define` Complete output and babysit docs recommend the simple `/goal /do <manifest-path>` form without duplicating manifest semantics.
  ```yaml
  verify:
    prompt: "Inspect define/SKILL.md, define/references/BABYSIT_MODE.md, README files, and generated dist copies. PASS only if the recommended unattended form is /goal /do <manifest-path> and the text does not expand into a long duplicated goal condition."
  ```

### Deliverable 3: Review PR One-Shot Behavior

**Acceptance Criteria:**
- [AC-3.1] `/review-pr` non-loop mode advances existing review threads before reviewing code, using GitHub state rather than session memory.
  ```yaml
  verify:
    prompt: "Inspect claude-plugins/manifest-dev-tools/skills/review-pr/SKILL.md. PASS only if every invocation resolves PR/current-head/prior-review/thread state from GitHub, verifies our unresolved threads, posts needed replies/resolutions, and only then reviews the relevant diff range."
  ```

- [AC-3.2] `/review-pr --loop` delegates to repeated one-shot passes.
  ```yaml
  verify:
    prompt: "Inspect review-pr/references/LOOP.md. PASS only if --loop is scheduling/backoff around the SKILL.md one-shot pass and does not carry a separate per-comment verifier or incremental-review brain."
  ```

### Deliverable 4: Hook Removal

**Acceptance Criteria:**
- [AC-4.1] Claude hook source files, hook tests, and plugin hook registrations are removed.
  ```yaml
  verify:
    prompt: "Run: test ! -e claude-plugins/manifest-dev/hooks && test ! -e tests/hooks && ! grep -q '\"hooks\"' claude-plugins/manifest-dev/.claude-plugin/plugin.json. PASS only if the command exits 0."
  ```

- [AC-4.2] User-facing docs no longer claim hook-based workflow enforcement.
  ```yaml
  verify:
    prompt: "Search README.md, CLAUDE.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, claude-plugins/manifest-dev-tools/README.md, and dist docs for stop_do_hook, post_compact_hook, workflow enforcement hooks, and claims that hooks prevent premature /do stopping. PASS only if no stale claim remains."
  ```

### Deliverable 5: Distribution Sync

**Acceptance Criteria:**
- [AC-5.1] Codex and OpenCode generated packages include new/changed skills and remove hook plugin artifacts.
  ```yaml
  verify:
    prompt: "Inspect dist/codex and dist/opencode after sync. PASS only if babysit-pr exists where skills/commands are generated, review-pr changes are copied, component-namespaces include babysit-pr, hook plugin files are removed, and READMEs/AGENTS files no longer describe hook enforcement."
  ```

### Deliverable 6: Local Commit

**Acceptance Criteria:**
- [AC-6.1] Work is committed locally on a new branch with a conventional commit, and no push or PR creation happened.
  ```yaml
  verify:
    prompt: "Run git branch --show-current, git log -1 --pretty=%s, and git status --short. PASS only if the branch is not main, the last commit uses a conventional prefix, intended changes are committed, unrelated pre-existing untracked files are not included, and there is no evidence of push/PR creation."
  ```
