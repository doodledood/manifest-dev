# Definition: AI-Slop Reviewer Coverage — test-quality-reviewer + prose-value-reviewer

## 1. Intent & Context

- **Goal:** Close two confirmed gaps in the marketplace's AI-slop reviewer coverage — tautological-test detection (folded into a renamed coverage-reviewer) and prose value/AI-tells (new agent for code comments + repo doc files). Slopsquatting was identified earlier but is out of scope here.
- **Mental Model:** The marketplace's reviewer suite is organized around orthogonal analytical axes (intent / design / simplicity / maintainability / type-safety / etc.) with strict Out-of-Scope sections enforcing boundaries. This work adds one new axis (`prose-value-reviewer`) and expands one existing axis (`code-coverage-reviewer` → `test-quality-reviewer`, now covering both test presence and test validity). The expanded agent's mission shifts from "are scenarios tested?" to "are scenarios tested AND validated?" — a tautological test no longer counts as coverage.
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

*Initial direction. Adjust during /do if reality diverges.*

- **Architecture:**
  - Mirror existing reviewer prompt structure (Scope Rules → Review Categories → Actionability Filter → Out of Scope → Report Format). Both agents follow the established pattern — keeps the suite coherent and the prompt-reviewer happy.
  - Tautology detection integrates as an extension of `code-coverage-reviewer`'s existing Step 3 ("Check existing tests"). Categories are additive; existing forward-derivation discipline preserved.
  - `prose-value-reviewer` is a fresh agent file. Targets: code comments + repo doc files (README.md, *.md in /docs and root). Excludes commits/PRs/external surfaces by design (narrow scope).
  - Comment-quality core for prose-value: comments must be load-bearing-WHY, not WHAT-restatement or past-iteration narration. This is the canonical framing in the prompt.
  - Orthogonality is enforced by updating the Out-of-Scope sections of all neighbor reviewers to (a) reference the renamed agent and (b) cite `prose-value-reviewer` where it owns the gap (especially `docs-reviewer` for accuracy-vs-value split, `code-maintainability-reviewer` for dead-code-vs-comment-value split, `context-file-adherence-reviewer` for project-rule-vs-prose-value split).
  - Naming: drops the `code-` prefix because both agents audit non-source artifacts (test code / prose), consistent with `docs-reviewer` / `contracts-reviewer` / `prompt-reviewer`.

- **Execution Order:**
  - D1 (rename + extend) → D2 (new prose-value) → D3 (orthogonality cascade) → D4 (READMEs + version) → D5 (dist/ regen)
  - Rationale: rename first establishes the new identity; extension adds the tautology axis; new agent comes second with its own clean scope; cascade catches all references in one sweep; mechanical sync last.

- **Risk Areas:**
  - [R-1] sync-tools may not delete stale `code-coverage-reviewer.*` files in dist/ after rename | Detect: `find dist -name 'code-coverage-reviewer.*'` should return empty after sync
  - [R-2] Regression on existing coverage findings — extension dilutes forward-derivation discipline | Detect: prompt-reviewer comparison against pre-change agent; manual sanity check that derived-scenario examples still appear with same prominence
  - [R-3] Prompt-length bloat — tautology section doubles agent length | Detect: line count vs peer reviewers (target: stay within ~20% of comparable agents)
  - [R-4] False-positive flood from prose-value-reviewer (judgmental axis) | Detect: dry-run on a clean PR — should produce empty report
  - [R-5] Tell-list creep during implementation — expansion beyond the four agreed tells per agent | Detect: tell-list audit before merge against the manifest's resolved categories
  - [R-6] Orthogonality cascade incomplete — neighbor reviewers reference old name or fail to mention prose-value-reviewer | Detect: `grep -r code-coverage-reviewer claude-plugins/` returns zero hits; each neighbor's Out-of-Scope reviewed against the new map
  - [R-7] Description discoverability lost on rename — auto-discovery fails to route old "check coverage" triggers | Detect: ensure new description's trigger list keeps coverage-related phrases alongside test-quality phrases

- **Trade-offs:**
  - [T-1] Tell-list comprehensiveness vs prompt brevity → Prefer brevity. PROMPTING anti-pattern is over-engineering; expansions are follow-up work.
  - [T-2] Strict orthogonality cascade vs faster shipping → Prefer cascade-completeness. The reviewer system depends on Out-of-Scope sections for routing; a stale reference fragments the suite.
  - [T-3] Naming clarity (rename) vs continuity (no rename) → User chose rename. Cost is cascade work; benefit is description-trigger-rename coherence.
  - [T-4] Prose-value scope — files only vs commits/PRs too → User chose narrow (files only). Defer broader coverage until adopter feedback shows the gap.
  - [T-5] False-positive discipline vs catching subtle slop → Prefer false-positive discipline. Match existing Actionability Filter — empty report > noisy report. Aligns with customer profile (quality-first developers allergic to noise).

## 3. Global Invariants

- [INV-G1] Description: Both new/renamed agent prompts pass `change-intent-reviewer` with no LOW+ findings. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review claude-plugins/manifest-dev/agents/test-quality-reviewer.md and claude-plugins/manifest-dev/agents/prose-value-reviewer.md for intent-behavior divergence. Stated intent: test-quality-reviewer extends coverage-reviewer with tautological-test detection (mirror-impl, mock-SUT, trivial-asserts, snapshot-without-intent) while preserving original forward-derivation of test scenarios from source logic. prose-value-reviewer audits code comments and repo doc files for narrating-the-obvious comments, generic puffery, AI rhetorical patterns, and sycophantic fragments — comments must be load-bearing-WHY not WHAT-restatement. Both narrow scope, match existing Actionability Filter."
  ```

- [INV-G2] Description: Both new/renamed agent prompts pass `prompt-reviewer` with no MEDIUM+ findings. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review claude-plugins/manifest-dev/agents/test-quality-reviewer.md and claude-plugins/manifest-dev/agents/prose-value-reviewer.md against prompt-engineering principles. Both are read-only auditor agents following the marketplace's reviewer pattern (Scope Rules → Review Categories → Actionability Filter → Out of Scope → Report Format). Description must follow What+When+Triggers. Trusted-advisor tone, no urgency. Categories presented as guidance not exhaustive enumeration."
  ```

- [INV-G3] Description: No file in `claude-plugins/`, root README, or non-archived sources references the old name `code-coverage-reviewer`. Archived manifests in `.manifest/` and generated `dist/` are exempt. | Verify:
  ```yaml
  verify:
    method: bash
    command: "! grep -rln --exclude-dir=.manifest --exclude-dir=dist --exclude-dir=.git 'code-coverage-reviewer' --include='*.md' --include='*.json' --include='*.yaml' --include='*.toml' --include='*.py' . 2>/dev/null | grep ."
  ```

- [INV-G4] Description: No stale `code-coverage-reviewer.*` files remain in `dist/` after sync-tools regen. | Verify:
  ```yaml
  verify:
    method: bash
    command: "! find dist -name 'code-coverage-reviewer.*' 2>/dev/null | grep ."
  ```

- [INV-G5] Description: `test-quality-reviewer.md` continues to detect every coverage category that `code-coverage-reviewer.md` did before the change (missing test files, untested functions, untested branches, missing error paths, missing edge cases) — the rename is additive, not replacement. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Verify that claude-plugins/manifest-dev/agents/test-quality-reviewer.md contains all five original coverage categories from the prior code-coverage-reviewer.md (missing test files, untested functions, untested branches, missing error path coverage, missing edge case coverage) AND adds a tautological-test detection section covering mirror-impl, mock-SUT, trivial-asserts, snapshot-without-intent. Both must be discoverable in the prompt — the rename must be additive, not replacement. PASS if both sets are present and clearly framed as part of the agent's mission."
  ```

- [INV-G6] Description: `prose-value-reviewer.md` exists, declares its scope (code comments + repo doc files only — explicitly excludes commits/PRs/external surfaces), and its tell categories cover all four agreed patterns plus the WHY-not-WHAT comment-quality framing. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Verify claude-plugins/manifest-dev/agents/prose-value-reviewer.md exists. Confirm: (1) Scope explicitly limits to code comments + repo doc files (READMEs, /docs); explicitly excludes commit messages and PR descriptions. (2) Tell categories cover narrating-the-obvious comments, generic puffery / empty buzzwords, AI rhetorical patterns (em-dash overuse, 'It's not just X — it's Y' patterns), sycophantic / assistant-voice fragments. (3) Comment-quality framing states comments must be load-bearing-WHY not WHAT-restatement or past-iteration narration. (4) Categories are framed as guidance, not exhaustive (preserves judgment for unseen patterns). PASS if all four conditions hold."
  ```

- [INV-G7] Description: Out-of-Scope sections in neighbor reviewers (code-bugs, code-design, code-maintainability, code-simplicity, code-testability, type-safety, change-intent, contracts, docs, context-file-adherence) reference the renamed `test-quality-reviewer` (not `code-coverage-reviewer`) and, where appropriate, cite `prose-value-reviewer` for prose value/AI-tells. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "For each agent in claude-plugins/manifest-dev/agents/ except test-quality-reviewer.md and prose-value-reviewer.md, check the Out-of-Scope or 'handled by other agents' section. PASS conditions: (1) zero references to 'code-coverage-reviewer' remain; (2) where the agent's scope abuts test quality (testability-reviewer, simplicity-reviewer, etc.), the reference is updated to 'test-quality-reviewer'; (3) docs-reviewer, code-maintainability-reviewer, and context-file-adherence-reviewer cite 'prose-value-reviewer' for the prose-value/AI-tells boundary. FAIL if any reference is stale or any obvious cross-reference is missing."
  ```

- [INV-G8] Description: Plugin version bumped (minor — new feature). | Verify:
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json,sys; v=json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; maj,minor,patch=map(int,v.split('.')); ref='0.93.2'; rmaj,rminor,rpatch=map(int,ref.split('.')); ok=(maj>rmaj) or (maj==rmaj and minor>rminor); sys.exit(0 if ok else 1)\""
  ```

- [INV-G9] Description: Three READMEs (root, claude-plugins, claude-plugins/manifest-dev) list both new agents (`test-quality-reviewer` and `prose-value-reviewer`) and remove references to the old `code-coverage-reviewer`. | Verify:
  ```yaml
  verify:
    method: bash
    command: "for f in README.md claude-plugins/README.md claude-plugins/manifest-dev/README.md; do grep -q test-quality-reviewer \"$f\" || { echo \"missing test-quality-reviewer in $f\"; exit 1; }; grep -q prose-value-reviewer \"$f\" || { echo \"missing prose-value-reviewer in $f\"; exit 1; }; ! grep -q code-coverage-reviewer \"$f\" || { echo \"stale code-coverage-reviewer in $f\"; exit 1; }; done"
  ```

- [INV-G10] Description: Both agents follow the established read-only reviewer contract — explicit "READ-ONLY" critical block, Actionability Filter with high-confidence bar, Out-of-Scope section delineating boundaries from neighbor agents. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "For both claude-plugins/manifest-dev/agents/test-quality-reviewer.md and claude-plugins/manifest-dev/agents/prose-value-reviewer.md, verify presence of: (1) explicit 'READ-ONLY Agent' or equivalent CRITICAL block forbidding file modifications; (2) Actionability Filter section with high-confidence bar matching existing reviewers (CERTAIN, not 'might be'); (3) Out-of-Scope or 'handled by other agents' section listing at least three boundary delegations to other reviewers. PASS if all three present in both."
  ```

## 4. Process Guidance

- [PG-1] Tell-lists for both agents must match this manifest exactly. The four tautology tells (mirror-impl, mock-SUT, trivial-asserts, snapshot-without-intent) and four prose tells (narrating-obvious, generic puffery, AI rhetorical patterns, sycophantic fragments) are the agreed set. Frame them as guidance not exhaustive (mirroring existing reviewers) but do not enumerate additional categories during implementation. Expansions are follow-up work.

- [PG-2] Prompt-length budget: stay within ±20% of comparable existing reviewers (~150–250 lines). Both agents should feel like peers of code-bugs-reviewer / code-design-reviewer in density, not bloated successors.

- [PG-3] Trusted-advisor tone. No urgency framing, no excessive praise, no pressure language. Failure-of-detection is normalized — empty report is a valid outcome.

- [PG-4] High-signal additions only. Every category in the new tautology section and the prose-value categories must address a real failure mode the team has seen or that the AI-slop literature documents. No speculative tells.

- [PG-5] Description-as-trigger discipline. Both new agents' `description:` field follows the What + When + Triggers pattern from PROMPTING.md. The renamed agent's description must keep coverage-related trigger phrases (e.g., "check coverage", "test coverage", "coverage gaps") so old-trigger discoverability survives the rename.

- [PG-6] Orthogonality cascade is part of the work, not a follow-up. When updating neighbor reviewers' Out-of-Scope sections, audit the entire boundary against both new agents — don't just rename the old reference; also add prose-value-reviewer where appropriate (especially docs-reviewer accuracy-vs-value split, maintainability-reviewer dead-code-vs-comment-value split, context-file-adherence-reviewer project-rule-vs-prose-value split).

- [PG-7] After file rename and content edits, run sync-tools skill to regenerate dist/. Verify stale `code-coverage-reviewer.*` files are removed (R-1) — if sync-tools doesn't delete them, do it manually before completion.

## 5. Known Assumptions

- [ASM-1] sync-tools skill correctly handles a renamed agent file (deletes old dist/ outputs, creates new ones). | Default: assume yes; verify per INV-G4. | Impact if wrong: manual cleanup of dist/ during D5.
- [ASM-2] Plugin marketplace consumers reference agents by their `name:` frontmatter, so file rename + frontmatter rename suffices. | Default: yes. | Impact if wrong: backward-compat shim needed (unlikely; the marketplace pattern routes by name).
- [ASM-3] No external skill, hook, or workflow file in this repo hardcodes `code-coverage-reviewer` as a string (e.g., as an agent invocation argument). | Default: assume no; INV-G3 catches violations. | Impact if wrong: caught by INV-G3, fixed during D3.
- [ASM-4] The `.manifest/learn-define-patterns-2026-03-01.md` reference to `code-coverage-reviewer` is an archived historical record, not active config. Leaving it untouched is correct. | Default: leave alone. | Impact if wrong: a forgotten active reference, caught by users running learn-define-patterns. Low risk.

## 6. Deliverables

### Deliverable 1: test-quality-reviewer (renamed + extended)

Rename `claude-plugins/manifest-dev/agents/code-coverage-reviewer.md` to `test-quality-reviewer.md`. Update `name:` frontmatter to `test-quality-reviewer`. Update `description:` to reflect expanded scope while preserving coverage-related trigger phrases. Extend the Review Categories section with a new tautological-test detection subsection covering the four agreed patterns plus a "guidance not exhaustive" caveat. Update Step 3 of Edge Case Enumeration to also judge existing tests for tautology, not just check existence. Update Out-of-Scope section to reflect the renamed identity.

**Acceptance Criteria:**

- [AC-1.1] File renamed; `name:` frontmatter matches new filename. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/agents/test-quality-reviewer.md && ! test -f claude-plugins/manifest-dev/agents/code-coverage-reviewer.md && head -5 claude-plugins/manifest-dev/agents/test-quality-reviewer.md | grep -q '^name: test-quality-reviewer$'"
  ```

- [AC-1.2] Description follows What + When + Triggers pattern; trigger phrases include both coverage-era ("check coverage", "test coverage", "coverage gaps") and quality-era ("tautological tests", "test quality", "are tests adequate"). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read frontmatter of claude-plugins/manifest-dev/agents/test-quality-reviewer.md. PASS if description (a) follows What+When+Triggers pattern (describes what the agent audits, when to invoke it, and lists trigger phrases), (b) trigger list includes at least three coverage-era phrases like 'check coverage', 'test coverage', 'coverage gaps', and (c) trigger list includes at least two quality-era phrases like 'tautological tests', 'test quality', 'are tests adequate'."
  ```

- [AC-1.3] Tautological-test detection subsection added with four named categories (mirror-impl, mock-SUT, trivial-asserts, snapshot-without-intent) framed as guidance not exhaustive. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/agents/test-quality-reviewer.md. PASS if it contains a tautological-test detection subsection that names all four categories: (1) tests that mirror implementation (mocks return X, code returns mock, asserts X), (2) mocks of the system under test, (3) trivial or missing assertions, (4) snapshot tests without intent. AND if the section frames categories as guidance / not exhaustive (preserving judgment for unseen patterns), matching the existing 'These categories are guidance, not exhaustive' phrasing."
  ```

- [AC-1.4] All five original coverage categories preserved (regression check). | Verify: covered by INV-G5.

- [AC-1.5] Step 3 of Edge Case Enumeration extended to also judge existing tests for tautology, not only check existence. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/agents/test-quality-reviewer.md, focusing on the Edge Case Enumeration section's Step 3 (Check existing tests). PASS if Step 3 now instructs the agent to BOTH compare derived scenarios against existing tests for absence AND judge whether existing tests for present scenarios actually validate the behavior (vs being tautological). FAIL if Step 3 only checks for absence."
  ```

- [AC-1.6] Test-only diff handling: when only test files changed, agent audits those tests directly for tautology. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/agents/test-quality-reviewer.md. PASS if Scope Rules or Special Cases section explicitly handles the test-only diff case: when the diff modifies only test files with no source changes, the agent audits those tests directly for tautology rather than skipping. FAIL if test-only diffs aren't addressed or the agent is instructed to skip them."
  ```

- [AC-1.7] Actionability Filter retains the high-confidence bar; tautology findings are subject to the same "CERTAIN, not might-be" discipline. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/agents/test-quality-reviewer.md Actionability Filter. PASS if it (a) preserves the existing high-confidence bar ('CERTAIN', empty report > false positives), (b) explicitly applies this bar to tautology findings, and (c) for tautology specifically, requires the reviewer to name the missing assertion or specific behavior the test fails to verify before flagging."
  ```

### Deliverable 2: prose-value-reviewer (new)

Create `claude-plugins/manifest-dev/agents/prose-value-reviewer.md`. Audits code comments and repo doc files (READMEs, /docs/*.md) for prose value. Scope explicitly excludes commit messages and PR descriptions. Tells: narrating-the-obvious comments, generic puffery / empty buzzwords, AI rhetorical patterns (em-dash overuse, "It's not just X — it's Y", tricolon padding), sycophantic / assistant-voice fragments. Comment-quality framing: comments must be load-bearing-WHY, not WHAT-restatement or past-iteration narration. Match existing reviewer structure and Actionability Filter.

**Acceptance Criteria:**

- [AC-2.1] File exists at correct path with frontmatter (`name:`, `description:`, `tools:`). | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev/agents/prose-value-reviewer.md && head -5 claude-plugins/manifest-dev/agents/prose-value-reviewer.md | grep -q '^name: prose-value-reviewer$'"
  ```

- [AC-2.2] Scope Rules explicitly target code comments + repo doc files (READMEs, *.md in /docs and root); explicitly exclude commit messages and PR descriptions. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/agents/prose-value-reviewer.md Scope Rules section. PASS if (a) it lists code comments and repo documentation files (README.md, *.md in /docs and root) as the audit targets, AND (b) explicitly excludes commit messages, PR descriptions, and external surfaces. FAIL if scope is ambiguous or implicitly broader."
  ```

- [AC-2.3] Tell categories cover all four agreed patterns — narrating-the-obvious comments, generic puffery / empty buzzwords, AI rhetorical patterns, sycophantic / assistant-voice fragments. Framed as guidance not exhaustive. | Verify: covered by INV-G6.

- [AC-2.4] Comment-quality framing states comments must be load-bearing-WHY, not WHAT-restatement or past-iteration narration. The framing is the canonical anchor for the comment audit. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/agents/prose-value-reviewer.md. PASS if the comment-audit framing explicitly states all three: (1) comments must be load-bearing for understanding, (2) comments documenting WHY (non-obvious reasoning, hidden constraints, workarounds, surprising behavior) earn their place, (3) comments narrating WHAT the code does or referencing past iterations / change history are flagged as bloat. The framing should be prominent, not buried."
  ```

- [AC-2.5] Description follows What + When + Triggers pattern. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read frontmatter description of claude-plugins/manifest-dev/agents/prose-value-reviewer.md. PASS if description follows What+When+Triggers pattern: clearly states what is audited (comments + doc prose), when to invoke (after implementing features, before PRs, when comments/docs feel padded), and lists trigger phrases (e.g., 'prose review', 'comment value', 'AI tells', 'doc puffery', 'narrating obvious')."
  ```

- [AC-2.6] Read-only contract present (CRITICAL block, Actionability Filter, Out-of-Scope section). | Verify: covered by INV-G10.

- [AC-2.7] Out-of-Scope delineates boundaries: docs accuracy → docs-reviewer; project-specific anti-comment rules → context-file-adherence-reviewer; commit/PR prose → "deferred / not in scope". | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read Out-of-Scope section of claude-plugins/manifest-dev/agents/prose-value-reviewer.md. PASS if it delegates: (1) documentation accuracy and drift to docs-reviewer, (2) project-specific anti-comment policies to context-file-adherence-reviewer, (3) explicitly notes commit messages and PR descriptions are out of scope (not delegated to another agent — simply not audited)."
  ```

### Deliverable 3: Orthogonality Cascade and Task-File Integration

Update Out-of-Scope sections of all neighbor reviewers to (a) reference the renamed `test-quality-reviewer` and (b) cite `prose-value-reviewer` where it owns the gap. Affected agents: change-intent-reviewer, code-bugs-reviewer, code-design-reviewer, code-maintainability-reviewer, code-simplicity-reviewer, code-testability-reviewer, type-safety-reviewer, contracts-reviewer, docs-reviewer, context-file-adherence-reviewer.

Update `claude-plugins/manifest-dev/skills/define/tasks/CODING.md` Quality Gates table: rename existing `code-coverage-reviewer` row to `test-quality-reviewer` (and rename label from "Test coverage" to "Test quality"); add a new row for `prose-value-reviewer` so /define auto-includes the gate for code-change tasks. WRITING.md / BLOG.md / DOCUMENT.md left untouched — their scope is standalone-authored prose, not repo-resident comments or doc files.

**Acceptance Criteria:**

- [AC-3.1] Zero stale `code-coverage-reviewer` references in `claude-plugins/`. | Verify: covered by INV-G3.

- [AC-3.2] Out-of-Scope updates cite `test-quality-reviewer` where the boundary previously cited `code-coverage-reviewer`. | Verify: covered by INV-G7.

- [AC-3.3] `prose-value-reviewer` cited in at least three neighbors where boundaries are tight: docs-reviewer (accuracy-vs-value split), code-maintainability-reviewer (dead-code-vs-comment-value split), context-file-adherence-reviewer (project-rule-vs-prose-value split). | Verify:
  ```yaml
  verify:
    method: bash
    command: "for f in claude-plugins/manifest-dev/agents/docs-reviewer.md claude-plugins/manifest-dev/agents/code-maintainability-reviewer.md claude-plugins/manifest-dev/agents/context-file-adherence-reviewer.md; do grep -q prose-value-reviewer \"$f\" || { echo \"missing prose-value-reviewer in $f\"; exit 1; }; done"
  ```

- [AC-3.4] CODING.md task file updated: rename `code-coverage-reviewer` row to `test-quality-reviewer`; rename row label from "Test coverage" to "Test quality" to reflect expanded scope; threshold preserved as "no MEDIUM+". | Verify:
  ```yaml
  verify:
    method: bash
    command: "! grep -q code-coverage-reviewer claude-plugins/manifest-dev/skills/define/tasks/CODING.md && grep -q test-quality-reviewer claude-plugins/manifest-dev/skills/define/tasks/CODING.md && grep -q '| Test quality |' claude-plugins/manifest-dev/skills/define/tasks/CODING.md"
  ```

- [AC-3.5] CODING.md task file adds a new quality gate row for `prose-value-reviewer` covering comments and repo doc files touched by the change. Threshold "no MEDIUM+" — matches the judgmental-axis bar of peer reviewers (docs-reviewer, code-simplicity-reviewer). | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Read claude-plugins/manifest-dev/skills/define/tasks/CODING.md Quality Gates table. PASS if it contains a new row referencing prose-value-reviewer with threshold 'no MEDIUM+'. The row should describe the aspect being audited (e.g., 'Comment/doc value', 'Prose value', or similar) and pair it with the prose-value-reviewer agent. FAIL if the row is missing or the threshold differs from 'no MEDIUM+'."
  ```

- [AC-3.6] WRITING.md, BLOG.md, and DOCUMENT.md task files left untouched — their scope is standalone-authored prose (articles, marketing, formal specs), not repo-resident comments or doc files. Adding prose-value-reviewer there would create scope overlap with the existing writing-reviewer / anti-slop gates. | Verify:
  ```yaml
  verify:
    method: bash
    command: "! grep -q prose-value-reviewer claude-plugins/manifest-dev/skills/define/tasks/WRITING.md 2>/dev/null && ! grep -q prose-value-reviewer claude-plugins/manifest-dev/skills/define/tasks/BLOG.md 2>/dev/null && ! grep -q prose-value-reviewer claude-plugins/manifest-dev/skills/define/tasks/DOCUMENT.md 2>/dev/null"
  ```

### Deliverable 4: README + plugin metadata sync

Update root `README.md`, `claude-plugins/README.md`, and `claude-plugins/manifest-dev/README.md` to list both new agents and remove old `code-coverage-reviewer` references. Bump `claude-plugins/manifest-dev/.claude-plugin/plugin.json` version (minor: 0.93.2 → 0.94.0). Update keywords if a new keyword like "test-quality" or "prose-value" earns its place; otherwise leave keywords unchanged (PG-4: high-signal only).

**Acceptance Criteria:**

- [AC-4.1] All three READMEs list both `test-quality-reviewer` and `prose-value-reviewer`; none mention old `code-coverage-reviewer`. | Verify: covered by INV-G9.

- [AC-4.2] Plugin version bumped (minor). | Verify: covered by INV-G8.

- [AC-4.3] README updates are descriptive (not just name-swaps) — both new agents have at least a one-line summary of what they audit. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check README.md, claude-plugins/README.md, and claude-plugins/manifest-dev/README.md for entries on test-quality-reviewer and prose-value-reviewer. PASS if each README has at least a one-line description of what each agent audits — not just a bullet with the agent name. The descriptions should be aligned with the agents' actual scope (test-quality covers presence + tautology; prose-value covers code comments + repo doc files)."
  ```

### Deliverable 5: Distribution sync

Run the sync-tools skill to regenerate `dist/gemini/`, `dist/opencode/`, `dist/codex/` for the renamed and new agents. Verify stale `code-coverage-reviewer.*` files are deleted from `dist/`. If sync-tools doesn't auto-delete, remove them manually.

**Acceptance Criteria:**

- [AC-5.1] sync-tools regen run successfully against current repo state. | Verify:
  ```yaml
  verify:
    method: bash
    command: "test -f dist/gemini/agents/test-quality-reviewer.md && test -f dist/opencode/agents/test-quality-reviewer.md && test -f dist/codex/agents/test-quality-reviewer.toml && test -f dist/gemini/agents/prose-value-reviewer.md && test -f dist/opencode/agents/prose-value-reviewer.md && test -f dist/codex/agents/prose-value-reviewer.toml"
  ```

- [AC-5.2] No stale `code-coverage-reviewer.*` files in `dist/`. | Verify: covered by INV-G4.

- [AC-5.3] Out-of-Scope updates and other content edits propagated to all three dist/ directories. | Verify:
  ```yaml
  verify:
    method: bash
    command: "for variant in gemini opencode; do for f in dist/$variant/agents/*.md; do ! grep -q code-coverage-reviewer \"$f\" || { echo \"stale ref in $f\"; exit 1; }; done; done; for f in dist/codex/agents/*.toml; do ! grep -q code-coverage-reviewer \"$f\" || { echo \"stale ref in $f\"; exit 1; }; done"
  ```
