# Definition: Replace tend-pr/tend-pr-tick with graduated drive

## 1. Intent & Context

- **Goal:** Promote `/drive` and `/drive-tick` from `manifest-dev-experimental` to `manifest-dev` (graduation), and entirely remove `/tend-pr` and `/tend-pr-tick`. After this change, `manifest-dev` is the canonical home for PR-lifecycle automation, and `manifest-dev-experimental` is preserved as an empty placeholder for future experiments.
- **Mental Model:** Drive replaces tend-pr — it does everything tend-pr did and more (manifest-driven loops, none-mode local runs, intra-tick `/do` convergence, pluggable platform/sink adapters). The change is a re-home + removal: nothing else about how drive works changes, but every cross-reference shifts because drive now lives in the core plugin and tend-pr is gone.
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

- **Architecture:** Filesystem moves (`mv`) for skill directories; targeted text edits for every file that names tend-pr; metadata bumps for both plugin.json files; symlink updates under `.claude/skills/`; `/sync-tools` regenerates `dist/` from the new source. The Claude-plugin source tree is the single source of truth — all dist/* changes flow from sync-tools, not direct edits.

- **Execution Order:**
  - D1 → D2 → D3 → D4 → D5 → D6 → D7 → D8
  - Rationale: move skills first so cross-references resolve to real files; remove tend-pr next; update the consumer skill (`/auto`); update internal cross-references; bump plugin metadata; update repo-level prose; regenerate dist/; verify gates last.

- **Risk Areas:**
  - [R-1] Cross-reference rot — file paths inside drive's SKILL.md or drive-tick's SKILL.md still point to `manifest-dev:tend-pr/...` after move | Detect: grep for `tend-pr` and `tend_pr` after each step.
  - [R-2] Stale symlinks — `.claude/skills/{tend-pr,tend-pr-tick}` left dangling, `.claude/skills/drive` not created | Detect: `ls -la .claude/skills/` plus broken-link check.
  - [R-3] Dist drift — `dist/{cli}/` keeps tend-pr while source removes it | Detect: post-sync `ls dist/{cli}/skills/` matches manifest-dev/skills.
  - [R-4] `/auto` flag scheme regresses — users invoking `--tend-pr` after the change get an unhelpful error rather than guidance | Detect: read /auto SKILL.md final text — must mention `--drive` and explain the rename.
  - [R-5] manifest-dev-experimental left in a broken state — directory empty but plugin.json claims drive | Detect: read plugin.json + README and verify they describe a placeholder.

- **Trade-offs:**
  - [T-1] Mirror tend-pr's defaults in `/auto --drive` vs match drive's own defaults → Prefer mirroring tend-pr's intent: `/auto --drive` defaults `--platform github` (drive's standalone default is `none`). Reasoning: `/auto` is end-to-end shipping; the natural continuation after `/do` is the GitHub PR lifecycle. Local-only drive loops from `/auto` are unusual and remain available with explicit `--drive --platform none`.
  - [T-2] Drop or keep `--reviewers` / `--log` flags from `/auto` → Drop. Drive does not consume them, and silently ignoring user flags is worse than rejecting them. Document the removal in /auto's SKILL.md.
  - [T-3] Preserve historical `.manifest/` archives mentioning tend-pr vs scrub them → Preserve. Per CLAUDE.md "Manifest Archival", archived manifests are point-in-time records, not living docs. Editing them rewrites history.

## 3. Global Invariants (The Constitution)

- [INV-G1] No active references to `tend-pr` or `tend_pr` remain in `claude-plugins/`, `dist/`, repo-level READMEs, or `CLAUDE.md`. Historical archives in `.manifest/` are exempt.
  ```yaml
  verify:
    method: bash
    command: "! grep -RIn --include='*.md' --include='*.py' --include='*.json' --include='*.toml' --include='*.yaml' --include='*.yml' -E 'tend-pr|tend_pr' claude-plugins/ dist/ README.md CLAUDE.md"
  ```

- [INV-G2] `/drive` and `/drive-tick` skills exist in the canonical manifest-dev plugin location.
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/skills/drive/SKILL.md && test -f claude-plugins/manifest-dev/skills/drive-tick/SKILL.md && test -d claude-plugins/manifest-dev/skills/drive/references && test -f claude-plugins/manifest-dev/skills/drive/references/ADAPTER_CONTRACT.md && test -f claude-plugins/manifest-dev/skills/drive/references/fallback-inline.md && test -d claude-plugins/manifest-dev/skills/drive/references/platforms && test -d claude-plugins/manifest-dev/skills/drive/references/sinks"
  ```

- [INV-G3] `manifest-dev-experimental/skills/` exists but contains no skill (placeholder for future experiments). Plugin directory and plugin.json remain.
  ```yaml
  verify:
    method: bash
    command: "test -d claude-plugins/manifest-dev-experimental && test -f claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json && [ \"$(ls -A claude-plugins/manifest-dev-experimental/skills 2>/dev/null)\" = \"\" ] || ! test -d claude-plugins/manifest-dev-experimental/skills"
  ```

- [INV-G4] `marketplace.json` still lists `manifest-dev-experimental` (and other plugins are unchanged).
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; d=json.load(open(\".claude-plugin/marketplace.json\")); names={p[\"name\"] for p in d[\"plugins\"]}; assert names == {\"manifest-dev\",\"manifest-dev-tools\",\"manifest-dev-experimental\"}, names'"
  ```

- [INV-G5] Drive's relative cross-references inside its SKILL.md and references still resolve to existing files after the move.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/drive/SKILL.md and claude-plugins/manifest-dev/skills/drive-tick/SKILL.md and every file under claude-plugins/manifest-dev/skills/drive/references/. For every relative path mentioned (../X/...., references/Y/..., etc.), verify the path resolves to a file or directory that actually exists in the repo. Report PASS only if every relative path resolves; otherwise FAIL with the unresolved paths."
  ```

- [INV-G6] Project gates pass: ruff (lint), black (format check), mypy (typecheck).
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy"
  ```

- [INV-G7] Hook tests still pass (no regressions from this change).
  ```yaml
  verify:
    method: bash
    command: "pytest tests/hooks/ -v"
  ```

- [INV-G8] No NEW failures in `tests/test_dist_skill_references.py` introduced by this change. (Discovered during /do: 8 pre-existing failures exist on the pre-change baseline — confirmed via `git stash` test. The original wording of this invariant — "still passes" — assumed a green baseline that was not the case. Amended to the actual intent: no regressions vs baseline. The 8 pre-existing failures are about skill-handoff content patterns and installer-merge behavior unrelated to tend-pr / drive — outside this task's scope.)
  ```yaml
  verify:
    method: bash
    command: "test \"$(pytest tests/test_dist_skill_references.py 2>&1 | grep -oE '[0-9]+ failed' | head -1)\" = '8 failed'"
  ```

  ## Amendment Block (added during /do)

  - **Trigger**: AC discovery during D8 verification preparation.
  - **Reason**: INV-G8 as originally written assumed `tests/test_dist_skill_references.py` was green on the branch's pre-change state. Running the test on the stashed pre-change tree shows 8 pre-existing failures, all about (a) skill-handoff content strings not present in dist files (e.g. `\`do-manifest-dev\` skill`), (b) installer settings-merge behavior, (c) verification-model defaults — none of which intersect with the tend-pr → drive replacement.
  - **Resolution**: amended invariant requires the failure count to match the pre-change baseline (8) — i.e., this change introduces zero new failures and resolves zero existing ones. Fixing the pre-existing failures is out of scope. A follow-up task should triage and either fix or delete the broken assertions.

- [INV-G9] `manifest-dev` plugin.json version bumped (minor) and lists `drive` keywords; no longer lists `tend-pr` keyword.
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; d=json.load(open(\"claude-plugins/manifest-dev/.claude-plugin/plugin.json\")); kws=set(d[\"keywords\"]); assert \"tend-pr\" not in kws and \"drive\" in kws, (d[\"version\"], kws); v=tuple(int(x) for x in d[\"version\"].split(\".\")); assert v >= (0,98,0), v'"
  ```

- [INV-G10] `manifest-dev-experimental` plugin.json description no longer claims to ship `/drive` (since drive moved out).
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; d=json.load(open(\"claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json\")); desc=d[\"description\"].lower(); assert \"drive\" not in desc or \"graduated\" in desc or \"placeholder\" in desc, desc'"
  ```

- [INV-G11] `/auto` SKILL.md uses `--drive` (not `--tend-pr`), and its description / flag table / Tend PR step refer to drive.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md fully. Verify: (1) the description frontmatter mentions --drive (not --tend-pr); (2) the flag explanation lists --drive and drive's pass-through flags (--platform, --interval, --max-ticks, --sink, --base); (3) the post-/do step invokes /drive (manifest-dev:drive), not manifest-dev:tend-pr; (4) error messages and usage strings reference --drive. PASS only if all four hold."
  ```

- [INV-G12] Drive's SKILL.md no longer claims `Coexists with /tend-pr`.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr' claude-plugins/manifest-dev/skills/drive/SKILL.md claude-plugins/manifest-dev/skills/drive-tick/SKILL.md"
  ```

- [INV-G13] Documentation accuracy gate (docs-reviewer) on the changed prose surface — no MEDIUM+ findings.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: inherit
    prompt: "Audit prose accuracy in: README.md, CLAUDE.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, claude-plugins/manifest-dev-experimental/README.md, claude-plugins/manifest-dev/skills/auto/SKILL.md, claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md, claude-plugins/manifest-dev/skills/do/references/SCOPED_EXECUTION.md, claude-plugins/manifest-dev/skills/drive/SKILL.md, claude-plugins/manifest-dev/skills/drive-tick/SKILL.md, dist/codex/README.md, dist/codex/AGENTS.md, dist/gemini/README.md, dist/gemini/GEMINI.md, dist/opencode/README.md, dist/opencode/AGENTS.md. Verify against actual code/skill behavior post-change: tend-pr / tend-pr-tick must be entirely absent; drive / drive-tick must be present and correctly described; /auto's --drive flag must be documented to mirror the description in the manifest. Threshold: no MEDIUM or higher findings."
  ```

- [INV-G14] Context-file adherence gate (context-file-adherence-reviewer) — no MEDIUM+ findings.
  ```yaml
  verify:
    method: subagent
    agent: context-file-adherence-reviewer
    model: inherit
    prompt: "Audit changes against CLAUDE.md project rules. Pay attention to: README sync checklist (root README, claude-plugins/README, plugin READMEs), plugin version bump rules, naming convention (kebab-case), skills frontmatter, file ops preference for cp/mv. Threshold: no MEDIUM or higher findings."
  ```

- [INV-G15] Prose-value gate (prose-value-reviewer) — no MEDIUM+ findings on edited prose.
  ```yaml
  verify:
    method: subagent
    agent: prose-value-reviewer
    model: inherit
    prompt: "Audit prose value in changed READMEs and SKILL.md files (root README, CLAUDE.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, claude-plugins/manifest-dev-experimental/README.md, claude-plugins/manifest-dev/skills/auto/SKILL.md, claude-plugins/manifest-dev/skills/drive/SKILL.md). Flag narrating-the-obvious comments, generic puffery, AI rhetorical patterns, sycophantic / assistant-voice fragments. Threshold: no MEDIUM or higher findings."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Use `mv` (not `cp` followed by `rm`) for moving skill directories — preserves git rename detection.
- [PG-2] Use `Edit` for targeted text changes; reserve `Write` for the rare full-rewrite case (manifest-dev-experimental README, where the new content is shorter than the old).
- [PG-3] After the source-tree changes settle, run `/sync-tools` to regenerate `dist/`. Do not edit dist/ files directly.
- [PG-4] Bump `manifest-dev` to a minor version (0.97.0 → 0.98.0): a skill graduated in, two skills removed. No breaking change to manifest schema or `/define` flow, but skill surface changes warrant a minor bump.
- [PG-5] Bump `manifest-dev-experimental` patch version (0.6.1 → 0.6.2 or minor 0.6.1 → 0.7.0): the plugin loses its skills entirely. Treat as minor (0.7.0) since the user-visible footprint changes.
- [PG-6] Do not edit files in `.manifest/` (historical archives, point-in-time records).
- [PG-7] Verify drive's relative paths still resolve after the move — `../drive/references/...` from drive-tick remains correct because both skills move together as siblings.
- [PG-8] Drive's `Coexists with /do, /tend-pr, /auto` line in SKILL.md becomes `Coexists with /do, /auto`. Drop tend-pr from sibling-skill enumerations everywhere.

## 5. Known Assumptions

- [ASM-1] `/sync-tools` correctly handles a brand-new skill (drive) appearing in `claude-plugins/manifest-dev/` and brand-new skill removals (tend-pr). Default behavior: full sync since SKILL list changes. Impact if wrong: dist/ stays stale; caught by INV-G1 grep over `dist/` and INV-G8 dist-references test.
- [ASM-2] No external consumer depends on `manifest-dev-experimental` shipping a skill called `drive`. Default: assumption holds (the plugin was experimental). Impact if wrong: an external consumer breaks; documented as a graduation, not a silent removal.
- [ASM-3] `/auto`'s old `--reviewers` and `--log` flags were rarely used; dropping them is acceptable. Default: hold. Impact if wrong: minor user friction, surfaced via the explicit usage error.

## 6. Deliverables

### Deliverable 1: Move drive + drive-tick into manifest-dev plugin

**Acceptance Criteria:**
- [AC-1.1] `claude-plugins/manifest-dev/skills/drive/SKILL.md` exists with the same content as the old experimental file (modulo cross-reference fixes from D5).
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/skills/drive/SKILL.md && head -5 claude-plugins/manifest-dev/skills/drive/SKILL.md | grep -q 'name: drive'"
  ```
- [AC-1.2] `claude-plugins/manifest-dev/skills/drive-tick/SKILL.md` exists with frontmatter `name: drive-tick`.
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/skills/drive-tick/SKILL.md && head -5 claude-plugins/manifest-dev/skills/drive-tick/SKILL.md | grep -q 'name: drive-tick'"
  ```
- [AC-1.3] `claude-plugins/manifest-dev/skills/drive/references/` exists and contains ADAPTER_CONTRACT.md, fallback-inline.md, `platforms/{none.md,github.md}`, `sinks/local.md`.
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/skills/drive/references/ADAPTER_CONTRACT.md && test -f claude-plugins/manifest-dev/skills/drive/references/fallback-inline.md && test -f claude-plugins/manifest-dev/skills/drive/references/platforms/none.md && test -f claude-plugins/manifest-dev/skills/drive/references/platforms/github.md && test -f claude-plugins/manifest-dev/skills/drive/references/sinks/local.md"
  ```
- [AC-1.4] `.claude/skills/drive` and `.claude/skills/drive-tick` symlinks exist and resolve into `claude-plugins/manifest-dev/skills/`.
  ```yaml
  verify:
    method: bash
    command: "test -L .claude/skills/drive && test -L .claude/skills/drive-tick && readlink .claude/skills/drive | grep -q 'claude-plugins/manifest-dev/skills/drive$' && readlink .claude/skills/drive-tick | grep -q 'claude-plugins/manifest-dev/skills/drive-tick$'"
  ```

### Deliverable 2: Remove tend-pr + tend-pr-tick + experimental drive copies

**Acceptance Criteria:**
- [AC-2.1] `claude-plugins/manifest-dev/skills/tend-pr/` and `claude-plugins/manifest-dev/skills/tend-pr-tick/` are gone.
  ```yaml
  verify:
    method: bash
    command: "! test -e claude-plugins/manifest-dev/skills/tend-pr && ! test -e claude-plugins/manifest-dev/skills/tend-pr-tick"
  ```
- [AC-2.2] `claude-plugins/manifest-dev-experimental/skills/drive/` and `drive-tick/` are gone (drive moved out).
  ```yaml
  verify:
    method: bash
    command: "! test -e claude-plugins/manifest-dev-experimental/skills/drive && ! test -e claude-plugins/manifest-dev-experimental/skills/drive-tick"
  ```
- [AC-2.3] `.claude/skills/tend-pr` and `.claude/skills/tend-pr-tick` symlinks no longer exist.
  ```yaml
  verify:
    method: bash
    command: "! test -e .claude/skills/tend-pr && ! test -e .claude/skills/tend-pr-tick && ! test -L .claude/skills/tend-pr && ! test -L .claude/skills/tend-pr-tick"
  ```

### Deliverable 3: Update `/auto` to use `/drive`

**Acceptance Criteria:**
- [AC-3.1] `/auto` SKILL.md frontmatter description references `--drive` (not `--tend-pr`) and matches the user-facing flag rename.
  ```yaml
  verify:
    method: bash
    command: "head -10 claude-plugins/manifest-dev/skills/auto/SKILL.md | grep -q -- '--drive' && ! head -10 claude-plugins/manifest-dev/skills/auto/SKILL.md | grep -q -- '--tend-pr'"
  ```
- [AC-3.2] `/auto` documents `--drive` defaults (default `--platform github` when `/auto` invokes drive) and explains the rename in inline prose. The skill invokes `manifest-dev:drive` (not `manifest-dev:tend-pr`) after `/do` completes.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev/skills/auto/SKILL.md fully. Verify: (a) when --drive is present and --platform is absent, /auto passes --platform github to /drive (mirrors the old tend-pr default); (b) when --drive --platform none is given, /auto passes that through; (c) the skill invokes manifest-dev:drive (Skill name 'drive') after /do; (d) drive's flag set is correctly named in the pass-through list (--platform, --interval, --max-ticks, --sink, --base); (e) error messages are updated and use --drive in usage strings; (f) the flag table notes the --tend-pr rename for users migrating. PASS only if all six hold."
  ```
- [AC-3.3] `/auto` Multi-Repo Behavior section refers to `/drive` instead of `/tend-pr` (per-cwd limitation now applies to drive).
  ```yaml
  verify:
    method: bash
    command: "grep -q '/drive' claude-plugins/manifest-dev/skills/auto/SKILL.md && ! grep -q '/tend-pr' claude-plugins/manifest-dev/skills/auto/SKILL.md"
  ```

### Deliverable 4: Update internal cross-references in core skills

**Acceptance Criteria:**
- [AC-4.1] `claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md` no longer mentions tend-pr; references drive (and only drive) for the optional PR-tending consumer.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md && grep -q 'drive' claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md"
  ```
- [AC-4.2] `claude-plugins/manifest-dev/skills/do/references/SCOPED_EXECUTION.md` updates the "When `/tend-pr` Invokes Scoped `/do`" heading and body to refer to drive.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' claude-plugins/manifest-dev/skills/do/references/SCOPED_EXECUTION.md && grep -q -i 'drive' claude-plugins/manifest-dev/skills/do/references/SCOPED_EXECUTION.md"
  ```
- [AC-4.3] Drive's SKILL.md and drive-tick's SKILL.md drop tend-pr mentions and update the "coexists with" enumeration accordingly.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' claude-plugins/manifest-dev/skills/drive/SKILL.md claude-plugins/manifest-dev/skills/drive-tick/SKILL.md"
  ```

### Deliverable 5: Update plugin metadata

**Acceptance Criteria:**
- [AC-5.1] `manifest-dev/.claude-plugin/plugin.json` version bumped to ≥ 0.98.0; keywords include `drive` and `drive-tick`; keywords do not include `tend-pr`.
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; d=json.load(open(\"claude-plugins/manifest-dev/.claude-plugin/plugin.json\")); v=tuple(int(x) for x in d[\"version\"].split(\".\")); kws=set(d[\"keywords\"]); assert v >= (0,98,0), v; assert \"drive\" in kws, kws; assert \"tend-pr\" not in kws, kws'"
  ```
- [AC-5.2] `manifest-dev-experimental/.claude-plugin/plugin.json` version bumped (any bump is fine — must change); description no longer claims drive ships there.
  ```yaml
  verify:
    method: bash
    command: "python3 -c 'import json; d=json.load(open(\"claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json\")); v=tuple(int(x) for x in d[\"version\"].split(\".\")); assert v > (0,6,1), v; desc=d[\"description\"].lower(); assert (\"placeholder\" in desc or \"graduated\" in desc or \"reserved\" in desc) or \"drive\" not in desc, desc'"
  ```
- [AC-5.3] `manifest-dev-experimental/README.md` describes the plugin as currently empty, drive having graduated, and is concise.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-experimental/README.md. Verify: (1) it explicitly states drive (and drive-tick) graduated to manifest-dev; (2) the plugin currently ships no skills; (3) it positions itself as a placeholder for future experiments. Word count ≤ 200. PASS only if all four hold."
  ```

### Deliverable 6: Update repo-level documentation

**Acceptance Criteria:**
- [AC-6.1] Root `README.md` no longer references `/tend-pr` in user-facing examples; promotes `/drive`. Keeps the same Quick Start surface (define + do + auto), with `/drive` as the PR/loop replacement for tend-pr in the examples.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' README.md && grep -q '/drive' README.md"
  ```
- [AC-6.2] `claude-plugins/README.md` updated: `manifest-dev` skill list shows `/drive` (not `/tend-pr`); `manifest-dev-experimental` description reflects the empty/placeholder state.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' claude-plugins/README.md && grep -q '/drive' claude-plugins/README.md"
  ```
- [AC-6.3] `claude-plugins/manifest-dev/README.md` updated: skill table lists `/drive` and `/drive-tick`; "See also" section updated to reflect manifest-dev-experimental's new state.
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' claude-plugins/manifest-dev/README.md && grep -q '/drive' claude-plugins/manifest-dev/README.md && grep -q '/drive-tick' claude-plugins/manifest-dev/README.md"
  ```
- [AC-6.4] `CLAUDE.md` (project context file) free of stale tend-pr references (it currently has none, but verify post-change).
  ```yaml
  verify:
    method: bash
    command: "! grep -n 'tend-pr\\|tend_pr' CLAUDE.md"
  ```

### Deliverable 7: Regenerate dist/ via /sync-tools

**Acceptance Criteria:**
- [AC-7.1] `dist/{codex,gemini,opencode}/skills/` contain `drive` and `drive-tick` directories; do not contain `tend-pr` or `tend-pr-tick`.
  ```yaml
  verify:
    method: bash
    command: "for cli in codex gemini opencode; do test -d dist/$cli/skills/drive && test -d dist/$cli/skills/drive-tick && ! test -e dist/$cli/skills/tend-pr && ! test -e dist/$cli/skills/tend-pr-tick || { echo FAIL: $cli; exit 1; }; done"
  ```
- [AC-7.2] `dist/{cli}/install_helpers.py` SKILLS lists include `drive`, `drive-tick`; do not include `tend-pr`, `tend-pr-tick`.
  ```yaml
  verify:
    method: bash
    command: "for cli in codex gemini opencode; do grep -q '\"drive\"' dist/$cli/install_helpers.py && grep -q '\"drive-tick\"' dist/$cli/install_helpers.py && ! grep -E '\"tend-pr\"|\"tend-pr-tick\"' dist/$cli/install_helpers.py || { echo FAIL: $cli; exit 1; }; done"
  ```
- [AC-7.3] `dist/{cli}/README.md`, `dist/codex/AGENTS.md`, `dist/gemini/GEMINI.md`, `dist/opencode/AGENTS.md` reference drive (not tend-pr) in their skill summaries.
  ```yaml
  verify:
    method: bash
    command: "! grep -RIn 'tend-pr\\|tend_pr' dist/codex/README.md dist/codex/AGENTS.md dist/gemini/README.md dist/gemini/GEMINI.md dist/opencode/README.md dist/opencode/AGENTS.md"
  ```
- [AC-7.4] `dist/opencode/commands/` contains `drive.md` and `drive-tick.md`; does not contain `tend-pr.md` or `tend-pr-tick.md`.
  ```yaml
  verify:
    method: bash
    command: "test -f dist/opencode/commands/drive.md && test -f dist/opencode/commands/drive-tick.md && ! test -e dist/opencode/commands/tend-pr.md && ! test -e dist/opencode/commands/tend-pr-tick.md"
  ```

### Deliverable 8: Verification gate (everything green)

**Acceptance Criteria:**
- [AC-8.1] All previous deliverables' ACs pass plus full grep sweep finds no `tend-pr` outside `.manifest/` archives.
  ```yaml
  verify:
    method: bash
    command: "! grep -RIn --include='*.md' --include='*.py' --include='*.json' --include='*.toml' --include='*.yaml' --include='*.yml' --exclude-dir='.manifest' --exclude-dir='.git' -E 'tend-pr|tend_pr' ."
  ```
