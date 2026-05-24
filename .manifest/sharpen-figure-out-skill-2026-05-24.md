# Definition: Sharpen figure-out skill (convergence, verbosity, scope) + broaden prompt-engineering triggers

## 1. Intent & Context

- **Goal:** Land three behavioral fixes to the `figure-out` skill body (exit-too-early, per-turn verbosity, /define-gravity from widened scope), and broaden the `prompt-engineering` skill's frontmatter description so it auto-activates on discussion-mode (not only on write/update/review/diagnose). Then sync multi-CLI distributions, bump plugin version, archive the manifest, and ship via PR.
- **Mental Model:**
  - `figure-out`'s description already declares broad scope ("any topic, problem, or idea… or when figuring it out IS the goal"). The body trips over its own description by closing on `/define`, which only fits engineering/artifact contexts. Removing that closing line eliminates the contradiction.
  - The convergence wording in `figure-out/references/autonomous.md` line 26 ("Stop when the high-leverage unknowns are resolved — remaining ones wouldn't shift the read") is already in clean natural English and is the model for the new SKILL.md convergence rule. Pull that up; don't reinvent.
  - All new prose in SKILL.md uses natural English only. No jargon (no VOI, no BO, no acquisition, no posterior, no "fixed-point"). "Load-bearing" is metaphorical-English already in the skill — keep it as is.
  - `prompt-engineering` description change is purely additive — add discussion-mode triggers; preserve current shape and principle line.

## 2. Approach

- **Architecture:** Surgical edits to two `SKILL.md` files. No new files, no structural changes. Plugin version bump, distribution sync via existing `sync-tools` skill, archival per CLAUDE.md convention, PR creation on the existing dev branch.
- **Execution Order:**
  - D1 (figure-out SKILL.md) → D2 (prompt-engineering description) → D3 (distributions sync) → D4 (PR shipped)
  - Rationale: D3 must run after D1+D2 because it propagates plugin component changes to `dist/`. D4 happens last because it shepherds everything through CI.
- **Risk Areas:**
  - [R-1] Jargon from this session ("VOI", "BO", "fixed-point") leaks into the new SKILL.md prose. | Detect: prompt-reviewer + INV-G3 grep for forbidden terms.
  - [R-2] `WITH_DOCS.md` line 7 quotes SKILL.md's "Clarifying answers feed exploration, not action" line; if that exact line is accidentally modified, the quote breaks. | Detect: AC-1.4 verifies the line is preserved verbatim.
  - [R-3] `prompt-engineering` description exceeds the 1024-char frontmatter limit after additions. | Detect: AC-2.2 measures length.
  - [R-4] `sync-tools` output drift causes spurious diffs in `dist/` unrelated to our changes. | Detect: AC-3.1 verifies diff is limited to skills we touched.
- **Trade-offs:**
  - [T-1] Body brevity vs. explicit discipline → Prefer brevity. The new convergence rule and per-turn governor are each one or two sentences; over-specifying would prescribe HOW, which the prompt-engineering principles forbid for behaviors the model already has.
  - [T-2] /define discoverability vs. scope-pure body → Prefer scope-pure. `/define` discoverability lives elsewhere (marketplace, `--with-docs` reference, CLAUDE.md). The body must not push toward an artifact when the user's topic produces none.

## 3. Global Invariants

- [INV-G1] Intent analysis: change-intent-reviewer finds no LOW+ severity intent mismatches between the user's stated goals (in this manifest) and the diff.
  ```yaml
  verify:
    prompt: "Run change-intent-reviewer against the diff on branch claude/figure-out-skill-rbBCF vs main. Stated intent: (1) remove the /define closing line from figure-out SKILL.md, (2) add a per-turn verbosity governor preserving the recommended-answer pairing, (3) replace soft convergence with a stop-when-nothing-shifts rule using natural-English vocabulary consistent with autonomous.md line 26, (4) broaden prompt-engineering description to auto-fire on discussion-mode. PASS only if no findings at LOW or above. FAIL otherwise; list each finding with severity and quote."
    agent: "change-intent-reviewer"
  ```

- [INV-G2] Prompt quality: prompt-reviewer finds no MEDIUM+ severity issues in either modified SKILL.md file.
  ```yaml
  verify:
    prompt: "Run prompt-reviewer against claude-plugins/manifest-dev/skills/figure-out/SKILL.md and claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md (post-change). Apply the gap-calibration audit from .claude/skills/prompt-engineering/references/review.md. PASS only if no findings at MEDIUM or above. FAIL otherwise; list each finding with severity."
    agent: "prompt-reviewer"
  ```

- [INV-G3] No jargon in figure-out SKILL.md body: the new additions and surrounding prose must not contain the terms "VOI", "Bayesian optimization", "BO", "acquisition function", "posterior", or "fixed-point". (Existing terms like "load-bearing" are permitted.)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. Search (case-insensitive) for these forbidden terms: 'VOI', 'Bayesian optimization', 'Bayesian opt', 'BO acquisition', 'acquisition function', 'posterior', 'fixed-point', 'fixed point'. PASS only if none present. FAIL otherwise; quote the offending lines."
  ```

- [INV-G4] Symlink integrity: `.claude/skills/figure-out/SKILL.md` and `.claude/skills/prompt-engineering/SKILL.md` remain symlinks that resolve to their `claude-plugins/manifest-dev/skills/*/SKILL.md` counterparts.
  ```yaml
  verify:
    prompt: "Check that .claude/skills/figure-out/SKILL.md and .claude/skills/prompt-engineering/SKILL.md are symlinks (using ls -la or readlink) and resolve to the matching files under claude-plugins/manifest-dev/skills/. PASS if both are symlinks pointing to the correct targets. FAIL otherwise."
  ```

## 4. Process Guidance

- [PG-1] Edit the `claude-plugins/manifest-dev/skills/...` files directly. The `.claude/skills/...` paths are symlinks per CLAUDE.md — modifying the symlink would not be wrong but the convention is to edit the canonical path. Do not break or replace the symlinks.
- [PG-2] Bump plugin version in `claude-plugins/manifest-dev/.claude-plugin/plugin.json`. Minor bump (new behavior — sharpened figure-out + broader prompt-engineering trigger).
- [PG-3] Run `sync-tools` skill **after** all SKILL.md edits land and **before** committing the final state. This regenerates `dist/` packages (OpenCode, Codex).
- [PG-4] Pre-PR gates: `ruff check --fix claude-plugins/ && black claude-plugins/ && mypy`. Skip `pytest tests/hooks/ -v` — hooks are not touched.
- [PG-5] Archive the final manifest to `.manifest/sharpen-figure-out-skill-2026-05-24.md` per CLAUDE.md convention.
- [PG-6] README sync per CLAUDE.md: no new components added, no renames, no removals — only behavior tweaks to existing skills. READMEs likely don't need updates. Verify (AC-5.1).
- [PG-7] Branch is `claude/figure-out-skill-rbBCF` (already checked out). Commit + push with -u origin; create PR ready for review (not draft).
- [PG-8] Keep edits minimal and high-signal. Don't restructure either skill body; don't rewrite working language for style. Only add what closes the named gap; only remove what no longer earns its place after the change.

## 5. Known Assumptions

- [ASM-1] The convergence wording in `autonomous.md` line 26 is correct as written and should be the lexical model for the SKILL.md convergence sentence. Default: pull up "Stop when … wouldn't shift the read" vocabulary. Impact if wrong: SKILL.md and autonomous.md drift in convergence language, future readers see inconsistency.
- [ASM-2] `prompt-engineering` SKILL.md description is the right surface to broaden — the auto-discovery scans this field at session start. Default: edit the description; do not add a duplicate or `references/` trigger. Impact if wrong: trigger broadening lands but doesn't actually fire.
- [ASM-3] "load-bearing" stays in the body; it is acceptable metaphorical English, not jargon. Default: do not rewrite it. Impact if wrong: minor — body would be slightly wordier without it but no semantic loss.
- [ASM-4] No README updates are required because no skill/agent/hook was added, renamed, or removed. Default: skip README edits. Impact if wrong: READMEs go slightly stale; not blocking.

## 6. Deliverables

### Deliverable 1: figure-out SKILL.md updated

**Acceptance Criteria:**

- [AC-1.1] The closing `/define`-pointer line is removed entirely. The body ends at the sentence containing "name the read" (no follow-on sentence about `/define` or Manifest).
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if: (a) the file contains 'name the read' somewhere in the body, (b) the file does NOT contain any reference to '/define' or 'Manifest' (capitalized) anywhere in the SKILL.md body (frontmatter excluded), and (c) the last non-empty sentence of the main body (before any '--with-docs' / '--autonomous' reference lines) is the 'name the read' sentence. FAIL otherwise; quote the current closing prose."
  ```

- [AC-1.2] A per-turn governor sentence is present that (a) instructs leading with one question and the recommended answer, (b) prohibits preamble, context-restate, and packed sub-questions, and (c) gives the override for tempting alternatives ("hold the rest").
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if the body contains a single coherent sentence or short paragraph that (a) tells the model to lead with one question and its recommended answer per turn, (b) names at least two of {preamble, context-restate, packed sub-questions} as things to avoid, and (c) handles alternative-question temptation by saying to pick the most-shifting one and hold the rest. FAIL otherwise; quote what's there."
  ```

- [AC-1.3] The soft convergence phrase ("when the space is exhausted") is replaced with a concrete stop-when-nothing-shifts rule that uses vocabulary consistent with `autonomous.md` line 26 ("shift the read").
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if: (a) the literal phrase 'space is exhausted' does NOT appear, AND (b) the body contains a convergence rule that uses the language 'shift the read' (or close variant like 'shift the picture' / 'change the read') AND tells the model to press remaining branches before naming the read. FAIL otherwise; quote the current convergence wording."
  ```

- [AC-1.4] The "Clarifying answers feed exploration, not action. Don't leap to the implied move — not the edit, not even the proposal." sentence is preserved verbatim. (WITH_DOCS.md line 7 quotes this; breaking it would break the reference.)
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if the file contains this exact substring (verbatim, punctuation included): 'Clarifying answers feed exploration, not action. Don'\\''t leap to the implied move — not the edit, not even the proposal.' FAIL otherwise."
  ```

- [AC-1.5] Existing core directives are preserved: "Press the topic relentlessly", "Walk every branch of the decision tree", "Tackle the next load-bearing question first", "Don't drop threads", "If something is discoverable", "Verify before asserting", "Hold positions under pushback", and the `--with-docs` / `--autonomous` reference lines.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if all of these phrases are present (verbatim): 'Press the topic relentlessly', 'Walk every branch of the decision tree', 'load-bearing', 'Don'\\''t drop threads', 'If something is discoverable', 'Verify before asserting', 'Hold positions under pushback', '--with-docs', '--autonomous'. FAIL otherwise; list which are missing."
  ```

### Deliverable 2: prompt-engineering SKILL.md description updated

**Acceptance Criteria:**

- [AC-2.1] The frontmatter `description` field includes the words "discuss" and "discussing" (in addition to existing write/update/review/diagnose verbs) and includes at least three new trigger phrases from: "discuss a skill", "think through a skill", "improve a skill", "this skill should", "this prompt needs".
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md. Inspect the frontmatter 'description' field. PASS only if: (a) both 'discuss' and 'discussing' appear in the description, AND (b) at least three of these trigger phrases appear in the description: 'discuss a skill', 'think through a skill', 'improve a skill', 'this skill should', 'this prompt needs'. FAIL otherwise; quote the current description."
  ```

- [AC-2.2] The frontmatter `description` field stays under 1024 characters (the enforced limit).
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md. Extract the value of the frontmatter 'description' field (the string after 'description: '). PASS only if the string length is < 1024 characters. FAIL otherwise; report actual length."
  ```

- [AC-2.3] The existing description shape (what + when + triggers + leads with the principle "State the goal, trust the model, add only what closes a real gap in natural behavior") is preserved.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md. PASS only if the frontmatter 'description' field still contains all of these substrings: 'system prompt, skill, or agent', 'State the goal, trust the model', 'closes a real gap', 'Triggers:'. FAIL otherwise; list which are missing."
  ```

- [AC-2.4] The body of `prompt-engineering` SKILL.md (everything after the frontmatter) is unchanged — only the frontmatter description was edited.
  ```yaml
  verify:
    prompt: "Use git diff to compare the body of claude-plugins/manifest-dev/skills/prompt-engineering/SKILL.md (everything below the closing '---' of the frontmatter) between branch claude/figure-out-skill-rbBCF and main. PASS only if the body has zero diff (only the frontmatter description changed). FAIL otherwise; show the body diff."
  ```

### Deliverable 3: Distributions synced

**Acceptance Criteria:**

- [AC-3.1] After running the `sync-tools` skill, the `dist/` directory contains updated versions of figure-out SKILL.md and prompt-engineering SKILL.md that match the source. Diff against pre-sync `dist/` is limited to files derived from the two skills we changed (plus any expected metadata bumps).
  ```yaml
  verify:
    prompt: "Run 'git diff main -- dist/' on branch claude/figure-out-skill-rbBCF. PASS only if: (a) the diff includes updates to dist/ files that mirror figure-out's SKILL.md and prompt-engineering's SKILL.md changes, AND (b) the diff is limited to files derived from these two skills (plus any expected version/metadata fields). FAIL if dist/ wasn't updated, or if dist/ shows unrelated drift. List unrelated changes if present."
  ```

### Deliverable 4: Plugin version bumped and manifest archived

**Acceptance Criteria:**

- [AC-4.1] `claude-plugins/manifest-dev/.claude-plugin/plugin.json` has its `version` field bumped by minor (e.g., 0.x.0 → 0.(x+1).0) relative to main.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/.claude-plugin/plugin.json on branch claude/figure-out-skill-rbBCF and on main. PASS only if the 'version' field on the branch is exactly one minor version higher than main (patch reset to 0). FAIL otherwise; report both values."
  ```

- [AC-4.2] Manifest archived: `.manifest/sharpen-figure-out-skill-2026-05-24.md` exists and matches the content of the source manifest at `/tmp/manifest-20260524-064938.md`.
  ```yaml
  verify:
    prompt: "Check that .manifest/sharpen-figure-out-skill-2026-05-24.md exists at the repo root. PASS only if (a) the file exists, AND (b) its content begins with '# Definition: Sharpen figure-out skill'. FAIL otherwise."
  ```

### Deliverable 5: Pre-PR gates pass

**Acceptance Criteria:**

- [AC-5.1] `ruff check --fix claude-plugins/` exits 0 (no remaining lint issues after auto-fix).
  ```yaml
  verify:
    prompt: "Run 'ruff check claude-plugins/' (without --fix, to check current state) from the repo root. PASS only if exit code is 0. FAIL otherwise; show output."
  ```

- [AC-5.2] `black claude-plugins/` reports no formatting changes needed.
  ```yaml
  verify:
    prompt: "Run 'black --check claude-plugins/' from the repo root. PASS only if exit code is 0. FAIL otherwise; show output."
  ```

- [AC-5.3] `mypy` exits 0.
  ```yaml
  verify:
    prompt: "Run 'mypy' from the repo root. PASS only if exit code is 0. FAIL otherwise; show output."
  ```

### Deliverable 6: PR open and lifecycle clean

**Acceptance Criteria:**

- [AC-6.1] Branch `claude/figure-out-skill-rbBCF` is pushed to origin with all commits, and a non-draft pull request exists targeting the default branch.
  ```yaml
  verify:
    prompt: "Use the GitHub MCP tools (mcp__github__list_pull_requests with head=claude/figure-out-skill-rbBCF) to verify a PR exists for branch claude/figure-out-skill-rbBCF on doodledood/manifest-dev. PASS only if: (a) one open PR exists for that head branch, AND (b) the PR is not a draft, AND (c) the PR's head SHA matches the local HEAD commit on the branch. FAIL otherwise."
    agent: "general-purpose"
  ```

- [AC-6.2] PR lifecycle: CI checks have completed and are all passing (or none configured); no unresolved review threads.
  ```yaml
  verify:
    prompt: "Invoke the github-pr-lifecycle agent on the PR for branch claude/figure-out-skill-rbBCF in doodledood/manifest-dev. PASS only if the agent reports PASS for CI status and review-thread status. BLOCKED if CI is still running. FAIL with the per-gate findings otherwise."
    agent: "github-pr-lifecycle"
    phase: 2
  ```
