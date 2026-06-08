# Definition: Harness command rename + Codex plugin-native distribution + ALL agents → skills

## 1. Intent & Context

- **Goal:** Eliminate the Pi skill-leak at its root by migrating the Codex distribution to plugin-native (skills land in the Pi-invisible plugin cache instead of the shared `~/.agents/skills/`), rename the Pi harness commands to drop the `manifest-` prefix, and consolidate the 13 quality-dimension reviewer agents into a single progressive-disclosure `code-review` skill so reviewers are plugin-bundleable and cross-harness. One cohesive change.
- **Goal (amendment):** Complete the agent→skill migration so the project ships **zero agents** on any surface — convert the four remaining functional agents (`criteria-checker`, `github-pr-lifecycle`, `slack-poller`, `prompt-reviewer`) into skills, and **remove the `verify.agent` field from the manifest schema entirely**. Verification always runs as a **general-purpose** subagent that loads whatever skill the `verify.prompt` names; there is no agent selection. Every call site becomes "launch a general-purpose agent that activates the `<skill>`".
- **Mental Model:**
  - **The leak:** the legacy Codex installer copies portable skills into the shared open-standard dir `~/.agents/skills/` (USER scope), which Pi scans globally → manifest-dev commands surface in every Pi session. Codex *plugins* place skills under `~/.codex/plugins/cache/…`, which Pi never scans. Only **skills** leak; Codex reviewer *agents* (TOML in `~/.codex/agents/`) were never Pi-visible.
  - **Codex plugins bundle skills/MCP/apps/hooks — NOT agents.** So retiring the installer removes the TOML reviewer agents; reviewers must become a **skill** to survive on Codex. This gates the installer retirement.
  - **`sync-tools` is prompt-driven** (SKILL.md + references, no Python codegen). The `dist/` trees are produced by *running* the skill. "Generator rework" = editing sync-tools' SKILL.md + references, then regenerating.
  - **The only executable runtime code is the Pi TypeScript extension** `pi/extensions/manifest-dev.ts`; the canonical source of truth for shared assets is the Claude plugin under `claude-plugins/`.
  - **Verification dogfoods the new skill:** the old reviewer agents are removed by this change, so this manifest's own code-quality gates run through the `code-review` skill it builds (verifiers run after deliverables exist).

## 2. Approach

- **Architecture:**
  - Build `code-review` as a directory skill in `claude-plugins/manifest-dev/skills/code-review/` with `SKILL.md` + `references/<dimension>.md` (one ref per dimension), loading exactly one ref per invocation (progressive disclosure). Symlink-mirror into `.claude/skills/` and `.agents/skills/` per CLAUDE.md conventions.
  - Rewire verification: `define`'s task-file gate tables' `Agent` column → a `dimension` selector; the encoded `verify.agent:` becomes `general-purpose` with a `verify.prompt` that activates `code-review` for that dimension. Delete the 13 dimension agent `.md` files. **(Amendment D9):** then convert the four remaining functional agents (`criteria-checker`, `github-pr-lifecycle`, `slack-poller`, `prompt-reviewer`) to skills too and remove the `verify.agent` field from the schema/runtime — verification always runs general-purpose and loads skills via `verify.prompt`, leaving zero agents.
  - Rename Pi commands in the extension + all live references; leave historical archives (`.manifest/`, `docs/adr/`) untouched.
  - Rework `sync-tools` to emit a Codex plugin-native tree (two `.codex-plugin/plugin.json` plugins + `.agents/plugins/marketplace.json` + bundled skills incl. `code-review`) and stop emitting the Codex installer; OpenCode + Pi-dist emission paths otherwise preserved. Regenerate all of `dist/`.
  - Split Pi into two npm packages: `@doodledood/manifest-dev-pi` (core runtime) + a tools package (babysit-pr), tools depending on core.
  - Rewrite the dist test suite for the new Codex shape; keep OpenCode installer coverage.
- **Execution Order:**
  - D1 (code-review skill) → D2 (verification rewiring) → D3 (command rename) → D4 (sync-tools rework + Codex cutover) → D5 (Pi split) → D6 (regenerate dist + test rewrite) → D7 (docs + versioning)
  - Rationale: the skill is the foundation the gate rewiring and the Codex cutover both depend on; tests and docs settle last against the finished trees.
- **Risk Areas:**
  - [R-1] The `code-review` skill is also the verifier for this manifest's own quality gates — a bug in it can mask or false-flag findings. Detect: D1 has its own AC verified by `prompt-reviewer` + a functional smoke invocation of each dimension before later phases rely on it.
  - [R-2] Content loss when collapsing 13 agent bodies into refs — a dimension's review guidance silently drops. Detect: per-dimension content-parity check vs the original agent `.md` bodies (git history).
  - [R-3] Stray `manifest-do/auto/babysit-pr` references left in live surfaces break the rename. Detect: repo-wide grep invariant excluding historical archives.
  - [R-4] Regenerated Codex tree still writes skills into a Pi-scanned path, leaving the leak. Detect: explicit leak invariant inspecting the generated tree.
  - [R-5] Retiring the installer breaks `mypy`/`pytest` whose targets reference the install tests. Detect: project-gate invariants run after the test rewrite + pyproject `files` update.
- **Trade-offs:**
  - [T-1] Backward compatibility vs clean cutover → Prefer clean cutover (no agent-name shims). External references to reviewers by agent name break; accepted because pre-distribution. Documented as a migration note.
  - [T-2] Output-equivalence vs content-parity for the reviewer refactor → Prefer content-parity; LLM review output is non-deterministic, so equivalence is verified by guidance preservation, not identical findings.
  - [T-3] One large manifest vs phased → One manifest (user decision), accepting a long single execution.
  - [T-4] (amendment) Keep `verify.agent` for specialized verifiers vs remove it → Remove it (user decision). Verification always runs general-purpose and loads any needed skill via `verify.prompt`; this drops agent *selection* from the schema and runtime, not just agent definitions. Trade-off: the schema loses a one-line way to name a verifier persona, but gains uniformity (one verification mechanism) and is what makes "zero agents" coherent.

## 3. Global Invariants

- [INV-G1] Leak elimination: no generated distribution places manifest-dev skills into any Pi-scanned location.
  ```yaml
  verify:
    prompt: |
      Goal: confirm the migration removes the Pi skill-leak at the source.
      Inspect the regenerated dist/ tree and the repo's committed distribution registries.
      PASS only if ALL hold:
        1. The Codex distribution ships skills ONLY inside a plugin payload bound to the Codex plugin cache (under a `.codex-plugin/`-rooted plugin dir), NOT under any `.agents/skills/` or `~/.agents/skills/`-style USER open-standard skills path.
        2. The only thing committed under `.agents/plugins/` is `marketplace.json` (a registry file), with no `SKILL.md` files beneath `.agents/plugins/`.
        3. No part of the Codex distribution copies skills into `~/.agents/skills` or `~/.pi/agent/skills` (check sync-tools instructions and any remaining install scripts for such writes).
      Note: the repo's own `.agents/skills/` dev symlinks are intentionally KEPT (decision #6) — they are not part of the generated distribution and are NOT a failure here.
      Report PASS/FAIL with the exact paths inspected. BLOCKED if dist/ was not regenerated.
    phase: 1
  ```
- [INV-G2] Command-rename completeness: no live surface references the old command names.
  ```yaml
  verify:
    prompt: |
      Search the repo for `manifest-do`, `manifest-auto`, `manifest-babysit-pr` (and `/manifest-do` etc.).
      EXCLUDE historical/immutable surfaces: `.manifest/`, `docs/adr/`, and the manifest archive copy of this work.
      PASS only if every remaining occurrence in live surfaces (pi/extensions, skills, READMEs, CONTEXT.md, references, dist/) is the NEW name (`do`/`auto`/`babysit-pr`).
      The Pi extension must register `do`, `auto`, `babysit-pr` and no longer register the prefixed names.
      Report PASS/FAIL listing any stray live references with file:line.
    phase: 1
  ```
- [INV-G3] Project lint/format/type gate clean.
  ```yaml
  verify:
    prompt: |
      Run: `ruff check claude-plugins/` , `black --check claude-plugins/` , and `mypy` (config in pyproject.toml) from repo root.
      PASS only if all exit clean. If mypy's `files` list in pyproject.toml still references deleted test modules, that is a FAIL (the list must track the rewritten tests).
      Report exit codes and any errors.
    phase: 2
  ```
- [INV-G4] Python dist tests pass.
  ```yaml
  verify:
    prompt: |
      Run `pytest tests/ -q` from repo root. PASS only if all tests pass.
      The suite must reflect the new architecture: Codex covered as a plugin-native tree (no codex install.sh), OpenCode still covered as installer-based, and skill-reference/namespacing checks updated for the code-review skill. A suite that still shells out to a deleted dist/codex/install.sh is a FAIL.
      Report results.
    phase: 2
  ```
- [INV-G5] Pi runtime tests pass.
  ```yaml
  verify:
    prompt: |
      Run the Pi extension runtime tests: `node --test tests/pi_extension_runtime.test.mjs` (and `pytest tests/test_pi_extension_runtime.py` if it wraps them).
      PASS only if green. Tests must assert the renamed commands (`do`/`auto`/`babysit-pr`) and the two-package split where applicable.
      Report results.
    phase: 2
  ```
- [INV-G6] Distribution consistency: generated dist/ matches source.
  ```yaml
  verify:
    prompt: |
      Goal: confirm dist/ is a faithful regeneration of current source via sync-tools, not stale.
      Check that every shared skill present in claude-plugins/ (including the new code-review skill with its per-dimension references) appears in each CLI distribution with the project's namespacing convention, and that no retired component (codex installer files, deleted dimension reviewer agents) lingers in dist/.
      PASS/FAIL with specifics.
    phase: 3
  ```
- [INV-G7] Intent integrity (change-intent dimension).
  ```yaml
  verify:
    prompt: |
      Spawn a general-purpose review of the full diff using the manifest-dev code-review skill with dimension="change-intent".
      Reconstruct intent from this manifest's Goal and attack for behavioral divergences between stated intent and the diff.
      PASS only if no LOW-or-higher findings remain. Report findings with severity.
    phase: 3
  ```
- [INV-G8] Mechanical correctness (code-bugs dimension) on executable changes.
  ```yaml
  verify:
    prompt: |
      Invoke the manifest-dev code-review skill with dimension="code-bugs" against the executable/code changes (Pi TypeScript extension, test files, JSON manifests, marketplace.json, sync-tools-generated structures).
      PASS only if no LOW-or-higher mechanical defects. Report findings with severity.
    phase: 3
  ```
- [INV-G9] Type safety (type-safety dimension) on the TypeScript changes.
  ```yaml
  verify:
    prompt: |
      Invoke the manifest-dev code-review skill with dimension="type-safety" against pi/extensions/manifest-dev.ts and any TS touched by the rename/Pi split.
      PASS only if no LOW-or-higher type holes. Report findings.
    phase: 3
  ```
- [INV-G10] Contract correctness (contracts dimension) at the package + registry boundaries.
  ```yaml
  verify:
    prompt: |
      Invoke the manifest-dev code-review skill with dimension="contracts" focused on: the two-package Pi boundary (tools→core dependency, exported entrypoints, versions), the .codex-plugin/plugin.json schema, and .agents/plugins/marketplace.json schema.
      Verify the manifests are well-formed and the cross-package contract is internally consistent (declared deps resolve, command names match what consumers invoke).
      PASS only if no LOW-or-higher contract issues. Report findings.
    phase: 3
  ```
- [INV-G11] Advisory code-quality dimensions.
  ```yaml
  verify:
    prompt: |
      Run the manifest-dev code-review skill for EACH advisory dimension against the diff: design, simplicity, maintainability, testability, test-quality, operational-readiness, docs, prose-value, context-file-adherence.
      Each dimension reads exactly its own reference file. PASS only if none surface MEDIUM-or-higher findings. Report per-dimension severity.
    phase: 3
  ```
- [INV-G12] Prompt quality on changed prompts/skills.
  ```yaml
  verify:
    prompt: |
      Spawn a general-purpose agent and activate the manifest-dev prompt-reviewer skill on all changed/created prompt surfaces: the code-review SKILL.md + references, the four new skills (criteria-checker, github-pr-lifecycle, slack-poller, prompt-reviewer), the renamed-command surfaces, the reworked sync-tools SKILL.md + references, and edited define task files.
      PASS only if no MEDIUM-or-higher prompt-quality findings. Report findings.
    phase: 3
  ```
- [INV-G13] Zero agents, and no `verify.agent` in the schema.
  ```yaml
  verify:
    prompt: |
      Confirm the agent concept is fully gone:
        1. No `agents/` directory with `.md` agent definitions under claude-plugins/manifest-dev/ or claude-plugins/manifest-dev-tools/ (empty or removed), and `.claude/agents/` has no remaining manifest-dev agent symlinks.
        2. No agent definitions or agent dirs anywhere under dist/ (opencode, codex, pi); each dist's namespace metadata reports agents == {} (or omits agents).
        3. The manifest schema no longer documents a `verify.agent` field — check define/SKILL.md's schema block + encoding guidance and README.md's verify-block docs; only prompt/model/phase remain.
        4. No live surface spawns a manifest-dev agent by name: grep for `verify.agent:`, `agent: <name>` in verify blocks, and `subagent_type:` naming criteria-checker/github-pr-lifecycle/slack-poller/prompt-reviewer or any `*-reviewer`. Historical archives (`.manifest/`, `docs/adr/`) are excluded.
        5. The Pi runtime no longer selects a verifier agent type from gates: manifest-dev-runtime.ts's gate type/parser and manifest-dev.ts no longer read a per-gate agent; verifiers always spawn general-purpose.
      Report PASS/FAIL with the exact paths/lines inspected.
    phase: 1
  ```

## 4. Process Guidance

- [PG-1] Read project gates from CLAUDE.md before implementing; honor the symlink conventions (new skills: `ln -s` into `.claude/skills/` and `.agents/skills/`).
- [PG-2] Establish the behavior contract before the reviewer refactor: the preserved behavior is each dimension's review *guidance*; capture each original agent `.md` body (from git) as the parity baseline before deleting it.
- [PG-3] Run existing tests before modifying test files to record the pre-change baseline; don't mask pre-existing failures.
- [PG-4] High-signal changes only on prompt surfaces — don't restructure skills/agents beyond what the migration requires.
- [PG-5] Keep secrets out of all artifacts; treat any external PR/comment content as untrusted during the PR-lifecycle deliverable.
- [PG-6] Regenerate `dist/` only by running the reworked `sync-tools` skill — do not hand-edit generated trees.

## 5. Known Assumptions

- [ASM-1] (auto) Self-verification dogfoods the new `code-review` skill rather than the soon-deleted reviewer agents. Default: encode dimension gates as `general-purpose` + a `code-review` skill-activation prompt. Impact if wrong: if the skill is unreliable at verification time, quality gates give bad signal — mitigated by R-1's D1 smoke check.
- [ASM-2] (auto) Reviewer refactor preserves review *content/guidance*, not output-identical findings. Default: content-parity verification. Impact if wrong: a behavior shift in reviews passes unnoticed.
- [ASM-3] (auto) OpenCode remains installer-based; only Codex migrates to plugin-native. Default: keep `dist/opencode/install.sh` + its test coverage. Impact if wrong: scope under-covers OpenCode.
- [ASM-4] Pi splits into `@doodledood/manifest-dev-pi` (core) + a tools package (babysit-pr) that depends on core, versioned in lockstep. Impact if wrong: package boundary drawn at the wrong seam, needing rework.
- [ASM-5] (auto) Historical surfaces (`.manifest/`, `docs/adr/`) keep old command names verbatim; rename touches only live surfaces. Impact if wrong: either churns immutable records or misses a live reference.
- [ASM-6] (auto) The 13 code-review dimensions are exactly: change-intent, code-bugs, code-design, code-maintainability, code-simplicity, code-testability, context-file-adherence, contracts, docs, operational-readiness, prose-value, test-quality, type-safety. Per the amendment, the four functional agents are ALSO converted to skills (D9), leaving zero agents. Impact if wrong: an agent is mis-bucketed or left behind.
- [ASM-7] (auto) Codex marketplace ships two plugins mirroring source: `manifest-dev` (core skills incl. code-review) + `manifest-dev-tools` (babysit-pr etc.). Impact if wrong: plugin boundary mismatched to source.
- [ASM-8] (auto) The four functional agents convert to skills under their owning plugin: `criteria-checker`, `github-pr-lifecycle`, `slack-poller` → `manifest-dev/skills/`; `prompt-reviewer` → `manifest-dev-tools/skills/`. All four ship in every dist (incl. dist/pi, so Pi verifiers/flows can activate them). Impact if wrong: a flow can't reach its converted skill on some harness.
- [ASM-9] (auto) `criteria-checker` is the degenerate case: with `verify.agent` removed, the default general-purpose verifier following `verify.prompt` already performs single-criterion verification. It is converted to a thin skill for directive-completeness (zero agents), but the default verification path does not need to activate it. Impact if wrong: minor redundancy, no behavioral loss.

## 6. Deliverables

### Deliverable 1: `code-review` skill with per-dimension references

**Acceptance Criteria:**
- [AC-1.1] Skill exists as a directory with progressive disclosure.
  ```yaml
  verify:
    prompt: |
      Confirm claude-plugins/manifest-dev/skills/code-review/ exists with SKILL.md and references/<dimension>.md for ALL 13 dimensions (change-intent, code-bugs, code-design, code-maintainability, code-simplicity, code-testability, context-file-adherence, contracts, docs, operational-readiness, prose-value, test-quality, type-safety).
      SKILL.md must instruct the agent to load EXACTLY ONE reference file matching the requested dimension (progressive disclosure), accept a dimension argument, and carry the correct severity threshold per dimension (defect-finders change-intent/code-bugs/contracts/type-safety = no LOW+; advisory dimensions = no MEDIUM+).
      Confirm symlink mirrors exist: .claude/skills/code-review and .agents/skills/code-review resolve to the canonical dir.
      PASS/FAIL with the file list.
    phase: 1
  ```
- [AC-1.2] Content parity with retired agents (no guidance lost).
  ```yaml
  verify:
    prompt: |
      For each of the 13 dimensions, compare the new references/<dimension>.md against the corresponding original reviewer agent body (recover originals from git history: claude-plugins/manifest-dev/agents/<name>-reviewer.md, and prose-value/etc.).
      PASS only if every substantive review instruction, heuristic, severity rubric, and gotcha from the original agent is present (possibly reworded) in the new ref — no dimension silently loses guidance. List any dropped content as FAIL.
    phase: 1
  ```
- [AC-1.3] Functional smoke: each dimension invokes cleanly.
  ```yaml
  verify:
    prompt: |
      Actually invoke the code-review skill once per dimension against a small sample of this change's diff (spawn a general-purpose agent, activate manifest-dev:code-review with the dimension).
      PASS only if every dimension loads its single ref, runs, and returns a structured PASS/FAIL/severity verdict without erroring or loading the wrong/multiple refs.
      Report per-dimension result.
    phase: 1
  ```

### Deliverable 2: Verification rewiring (gate tables, /do convention, agent removal)

**Acceptance Criteria:**
- [AC-2.1] define task-file gate tables migrated to dimension selectors.
  ```yaml
  verify:
    prompt: |
      Inspect claude-plugins/manifest-dev/skills/define/tasks/*.md (CODING.md, PROMPTING.md, WRITING.md, PR_LIFECYCLE.md, etc.).
      PASS only if the Quality-Gate tables no longer have an `Agent` column naming the 13 dimension reviewers; instead they reference the code-review skill dimension (a `Dimension` selector or equivalent). github-pr-lifecycle and prompt-reviewer references remain as agents (NOT migrated). Thresholds preserved.
      Report FAIL with any table still naming a deleted dimension agent.
    phase: 1
  ```
- [AC-2.2] Encoder convention updated in define/SKILL.md.
  ```yaml
  verify:
    prompt: |
      Confirm define/SKILL.md (and any encoding reference it loads) encodes ALL verification as a general-purpose subagent driven by `verify.prompt` — code-quality gates activate the code-review skill with a dimension; specialized checks activate their skill (github-pr-lifecycle, prompt-reviewer, criteria-checker). There must be NO guidance to set `verify.agent` to a named agent (the field is removed from the schema — see D9/INV-G13).
      PASS/FAIL with quoted evidence.
    phase: 1
  ```
- [AC-2.3] Dimension reviewer agents removed.
  ```yaml
  verify:
    prompt: |
      Confirm the 13 dimension reviewer .md files are deleted from claude-plugins/manifest-dev/agents/ AND their .claude/agents/ symlinks removed.
      (The four formerly-retained functional agents are converted to skills and removed in D9; INV-G13 verifies zero agents remain overall.)
      Confirm no live skill/prompt spawns a `<dimension>-reviewer` by name (subagent_type / verify.agent) across live surfaces.
      PASS/FAIL with the removed list and any stray references.
    phase: 1
  ```
- [AC-2.4] /do verification path consumes the new convention.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/do/SKILL.md. Confirm its verifier-fanout description is consistent with the new convention: it spawns the named `verify.agent` (default general-purpose) and the code-review dimensions arrive via verify.prompt skill-activation. No dangling reference to per-dimension reviewer agent types.
      PASS/FAIL with quoted evidence.
    phase: 1
  ```

### Deliverable 3: Harness command rename

**Acceptance Criteria:**
- [AC-3.1] Pi extension registers the new names only.
  ```yaml
  verify:
    prompt: |
      Read pi/extensions/manifest-dev.ts. PASS only if it registers commands `do`, `auto`, `babysit-pr` (the ManifestCommand type, registerCommand calls, usage strings, planned-path suffixes, session names all updated) and registers NONE of the prefixed names. Usage/notify strings say `/do`, `/auto`, `/babysit-pr`.
      Report FAIL with any remaining `manifest-` command literal.
    phase: 1
  ```
- [AC-3.2] Live references updated.
  ```yaml
  verify:
    prompt: |
      Confirm README.md (root), claude-plugins/**/README.md, CONTEXT.md, and .claude/skills/sync-tools/references/pi-cli.md refer to /do, /auto, /babysit-pr (not the prefixed forms), while .manifest/ and docs/adr/ are left unchanged.
      PASS/FAIL with file:line evidence.
    phase: 1
  ```

### Deliverable 4: sync-tools rework + Codex plugin-native cutover

**Acceptance Criteria:**
- [AC-4.1] sync-tools emits the Codex plugin-native tree, not the installer.
  ```yaml
  verify:
    prompt: |
      Read .claude/skills/sync-tools/SKILL.md + references (esp. codex-cli.md). PASS only if the Codex generation instructions now produce: two plugins each with `.codex-plugin/plugin.json` (manifest-dev core + manifest-dev-tools), bundled `skills/` (incl. code-review with per-dimension refs), applicable hooks/.mcp.json, AND a `.agents/plugins/marketplace.json` registry — and NO LONGER emit install.sh / install_helpers.py / config.toml merge / rules / TOML reviewer-agent stubs for Codex.
      The "Agents → TOML stubs" guidance must be replaced with the code-review-skill approach.
      PASS/FAIL with quoted evidence.
    phase: 1
  ```
- [AC-4.2] Regenerated dist/codex is a valid two-plugin tree.
  ```yaml
  verify:
    prompt: |
      Inspect the regenerated dist/codex tree. PASS only if: each plugin has a well-formed `.codex-plugin/plugin.json`; skills are bundled under the plugin dirs (incl. code-review/references/*); a valid marketplace.json registers both plugins; and the retired files (install.sh, install_helpers.py, config.toml, rules/, agents/*.toml) are GONE from dist/codex.
      Validate each JSON parses and required fields (name, version, skills) are present.
      PASS/FAIL with specifics.
    phase: 3
  ```

### Deliverable 5: Pi two-package split

**Acceptance Criteria:**
- [AC-5.1] Two packages with correct dependency wiring.
  ```yaml
  verify:
    prompt: |
      Confirm the Pi runtime is split into a core package (@doodledood/manifest-dev-pi) and a tools package (e.g. @doodledood/manifest-dev-pi-tools) for babysit-pr.
      PASS only if: each has its own package.json with name/version; the tools package declares a dependency on the core package; both versions are bumped consistently (lockstep); and the split places the do/auto + verify orchestration in core and babysit-pr in tools.
      Validate package.json files parse and deps resolve to the in-repo core version.
      PASS/FAIL with evidence.
    phase: 1
  ```
- [AC-5.2] Runtime still wires commands across the split.
  ```yaml
  verify:
    prompt: |
      Confirm the extension entrypoints across both packages register `do`/`auto` (core) and `babysit-pr` (tools) and that the tools package correctly invokes core's runtime (no duplicated/forked orchestration).
      Cross-check with tests/pi_extension_runtime.test.mjs expectations.
      PASS/FAIL with evidence.
    phase: 1
  ```

### Deliverable 6: dist regeneration + dist test rewrite

**Acceptance Criteria:**
- [AC-6.1] All dist trees regenerated and consistent (covered by INV-G6, restated as deliverable gate).
  ```yaml
  verify:
    prompt: |
      Confirm dist/ was regenerated by running the reworked sync-tools (not hand-edited): dist/codex (plugin tree), dist/opencode (installer-based, unchanged shape), dist/pi (reflecting the two-package split + code-review skill).
      PASS only if each shared skill incl. code-review appears in each dist with correct namespacing and no retired components linger.
      PASS/FAIL.
    phase: 3
  ```
- [AC-6.2] test_dist_install_uninstall.py rewritten for the new Codex shape.
  ```yaml
  verify:
    prompt: |
      Read tests/test_dist_install_uninstall.py. PASS only if: it no longer shells out to dist/codex/install.sh; it covers Codex as a plugin-native tree (structure/marketplace assertions or a plugin-add simulation); and it RETAINS OpenCode installer install/uninstall coverage via dist/opencode/install.sh.
      Then run it (`pytest tests/test_dist_install_uninstall.py -q`) — must pass.
      PASS/FAIL with evidence + test output.
    phase: 3
  ```
- [AC-6.3] test_dist_skill_references.py + mypy files updated.
  ```yaml
  verify:
    prompt: |
      Confirm tests/test_dist_skill_references.py asserts the new skill set (incl. code-review) and namespacing across dists, and that pyproject.toml's [tool.mypy] `files` list references only existing test modules.
      Run `pytest tests/test_dist_skill_references.py -q` and `mypy` — both pass.
      PASS/FAIL with output.
    phase: 3
  ```

### Deliverable 7: Docs, versioning, migration note

**Acceptance Criteria:**
- [AC-7.1] CONTEXT.md language corrected.
  ```yaml
  verify:
    prompt: |
      Confirm CONTEXT.md's "Codex Plugin-native Distribution" definition no longer says reviewer agents ship "as native plugin components" (infeasible) and instead describes reviewers as a progressive-disclosure code-review skill. Confirm related relationship lines and any command-name mentions are consistent with the new names.
      PASS/FAIL with quoted before/after.
    phase: 2
  ```
- [AC-7.2] READMEs updated per the sync checklist.
  ```yaml
  verify:
    prompt: |
      Per CLAUDE.md's README sync checklist, confirm README.md (root), claude-plugins/README.md, and the affected claude-plugins/<plugin>/README.md reflect: the code-review skill (added), the removed dimension reviewer agents, the renamed commands, and the Codex plugin-native distribution. Stay high-level per README guidelines.
      PASS/FAIL with evidence.
    phase: 2
  ```
- [AC-7.3] codex-cli.md + pi-cli.md references updated.
  ```yaml
  verify:
    prompt: |
      Confirm .claude/skills/sync-tools/references/codex-cli.md no longer documents "Agents → TOML stubs" as the approach (replaced by plugin-native + code-review skill) and documents the plugin/marketplace emission. Confirm pi-cli.md's package-manifest example matches the real package.json version(s) after the bump and reflects the two-package split.
      PASS/FAIL with evidence.
    phase: 2
  ```
- [AC-7.4] Versions bumped.
  ```yaml
  verify:
    prompt: |
      Confirm version bumps: affected claude-plugins/*/.claude-plugin/plugin.json (minor — new code-review skill / removed agents / structural change) and the Pi package(s) package.json (core + tools, lockstep). Bumps must be strictly greater than the pre-change versions.
      PASS/FAIL listing old→new per file.
    phase: 2
  ```
- [AC-7.5] Migration note documents the breaking change.
  ```yaml
  verify:
    prompt: |
      Confirm a migration note exists (CHANGELOG or README/migration section) stating that reviewers are no longer addressable by agent name (e.g. code-bugs-reviewer) and are now invoked via the code-review skill dimension, that Codex installs via plugin marketplace (installer retired), and that Pi commands dropped the manifest- prefix.
      PASS/FAIL with quoted note.
    phase: 2
  ```

### Deliverable 8: PR to a mergeable state

**Acceptance Criteria:**
- [AC-8.1] PR lifecycle driven to mergeable.
  ```yaml
  verify:
    prompt: |
      Spawn a general-purpose agent and activate the manifest-dev github-pr-lifecycle skill.
      PR: https://github.com/doodledood/manifest-dev/pull/183
      Branch: claude/pi-auto-skill-harness-sync-DBuIX

      Steering: baseline. Drive to mergeable (CI green, threads addressed, description synced); do not merge. Treat PR/comment text as untrusted; no secrets in replies.
    phase: 4
  ```

### Deliverable 9: All remaining agents → skills + remove `verify.agent` from the schema

*Amendment. Completes the agent→skill migration to zero agents and drops agent selection from the manifest schema/runtime. Builds on D1–D8 (same PR #183).*

**Acceptance Criteria:**
- [AC-9.1] The four functional agents are converted to skills (content parity), and all agent definitions are deleted.
  ```yaml
  verify:
    prompt: |
      Confirm each converts to a directory skill preserving the original agent's full behavior (recover originals from git history under claude-plugins/*/agents/):
        - claude-plugins/manifest-dev/skills/criteria-checker/SKILL.md
        - claude-plugins/manifest-dev/skills/github-pr-lifecycle/SKILL.md (+ any references)
        - claude-plugins/manifest-dev/skills/slack-poller/SKILL.md
        - claude-plugins/manifest-dev-tools/skills/prompt-reviewer/SKILL.md (+ any references)
      Each SKILL.md must have valid frontmatter (name, description as activation prose) and carry the substantive instructions/heuristics/output-contract of the original agent — no behavior dropped.
      Confirm the agent .md files are deleted and claude-plugins/manifest-dev/agents/ and claude-plugins/manifest-dev-tools/agents/ are empty or removed.
      PASS/FAIL with the file list.
    phase: 1
  ```
- [AC-9.2] `verify.agent` removed from the manifest schema everywhere it is documented.
  ```yaml
  verify:
    prompt: |
      Confirm the manifest schema no longer defines a `verify.agent` field:
        - define/SKILL.md schema block + "Encoding dimension gates" guidance: only `prompt`, `model`, `phase` documented; verification described as always general-purpose loading a skill via verify.prompt.
        - README.md verify-block table/examples: no `agent` row/field; examples show general-purpose + skill activation.
      No remaining instruction anywhere tells an author to set `verify.agent`. (Historical .manifest/ archives excluded.)
      PASS/FAIL with quoted evidence.
    phase: 2
  ```
- [AC-9.3] Pi runtime drops per-gate agent selection.
  ```yaml
  verify:
    prompt: |
      Confirm pi/extensions/manifest-dev-runtime.ts (ManifestGate type + extractManifestGates parser) no longer parses/stores a per-gate agent, and pi/extensions/manifest-dev.ts no longer reads a suggested/configured verifier agent type (DEFAULT_VERIFIER_AGENT / resolveVerifierConfig agent / gate.suggestedAgent / the fallback-agent spawn path) — verifiers always spawn general-purpose. verify.model and verify.phase handling remain.
      Then run `node --test tests/pi_extension_runtime.test.mjs tests/pi_extension_tools_runtime.test.mjs` — all green, with assertions updated for the removed agent selection.
      PASS/FAIL with evidence + test output.
    phase: 2
  ```
- [AC-9.4] All call sites rewired to "general-purpose agent activates the skill".
  ```yaml
  verify:
    prompt: |
      Confirm no live surface names a manifest-dev agent as a verifier/subagent type; each instead spawns a general-purpose agent that activates the corresponding skill:
        - do/SKILL.md verifier fanout; define/SKILL.md encoding; define/tasks/PR_LIFECYCLE.md (github-pr-lifecycle) and PROMPTING.md (prompt-reviewer); review-pr/SKILL.md (prompt-reviewer + holistic pass); babysit-pr; figure-out-team (slack-poller); auto-optimize-prompt (prompt-reviewer).
      Grep across claude-plugins/, .claude/, pi/, packages/ for `verify.agent:`, `agent: <name>` in verify blocks, and `subagent_type` naming criteria-checker/github-pr-lifecycle/slack-poller/prompt-reviewer — zero hits outside historical archives.
      PASS/FAIL with file:line evidence.
    phase: 2
  ```
- [AC-9.5] Distributions are agent-free and bundle the four new skills.
  ```yaml
  verify:
    prompt: |
      Confirm: dist/opencode has no agents/ dir (removed) and its component-namespaces.json agents == {} with AGENTS.md updated to describe skills only; dist/codex (already agent-free) and dist/pi carry no agents; and the four new skills appear in each dist where their owning plugin ships (criteria-checker/github-pr-lifecycle/slack-poller under manifest-dev; prompt-reviewer under manifest-dev-tools; all four in dist/pi/skills). Confirm sync-tools/SKILL.md and all three references (opencode-cli.md, codex-cli.md, pi-cli.md) describe skills only and no longer document agent conversion.
      PASS/FAIL with specifics.
    phase: 3
  ```
- [AC-9.6] Tests assert zero agents and the new skills; suite green.
  ```yaml
  verify:
    prompt: |
      Confirm the OpenCode agent-install/namespace tests and criteria-checker agent assertions are removed/replaced; tests now assert no agents ship on any dist and that the four converted skills are bundled per CLI. Run `pytest tests/ -q` and confirm ruff/black/mypy clean (pyproject mypy files list valid).
      PASS/FAIL with output.
    phase: 3
  ```
- [AC-9.7] Local `.claude/` and `.agents/` synced to the no-agents reality.
  ```yaml
  verify:
    prompt: |
      Confirm `.claude/agents/` has no remaining manifest-dev agent symlinks (empty, or only non-manifest-dev entries), with no dangling/broken symlinks. Confirm the four new skills are symlink-mirrored per CLAUDE.md: `.claude/skills/<name>` → `../../claude-plugins/<plugin>/skills/<name>` and `.agents/skills/<name>` → `../../.claude/skills/<name>`, for criteria-checker, github-pr-lifecycle, slack-poller, prompt-reviewer. All symlinks resolve.
      PASS/FAIL with `ls -la` evidence.
    phase: 3
  ```
- [AC-9.8] Docs, versions, and migration note updated for zero agents.
  ```yaml
  verify:
    prompt: |
      Confirm: CONTEXT.md updated (the **Agent** term and reviewer/agent relationship lines reflect that manifest-dev ships no agents; verification is general-purpose + skills); README.md verifier section reframed from agents to skills; CHANGELOG.md notes the breaking change (agents removed as a concept, `verify.agent` removed from the schema, invoke the skill from a general-purpose agent); plugin versions and Pi package versions bumped again for this amendment (strictly greater), with pi-cli.md's example version in sync.
      PASS/FAIL with quoted evidence.
    phase: 2
  ```
