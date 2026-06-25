# Definition: Add "Leading word" pattern to prompt-engineering skill

## 1. Intent & Context
- **Goal:** Add the one genuinely-missing authoring lever — *leading words* — to our `prompt-engineering` skill as a single additive pattern. Reject the rest of the surveyed framework as bloat our skill already covers behaviorally or that belongs to `/define`/`/do`.
- **Mental Model:** Our skill is strong at *subtraction* (cut no-ops) but nearly silent on the *positive craft* of the lines that survive. The leading-word lever fills exactly that: collapse a multi-word directive onto a single compact word the model already holds from pretraining (`tight`, `relentless`, `red`), and the corollary — the fix for a weak directive is a *stronger word, not more words*. Verified this session (independent re-derivation) to be a real gap, not a no-op, since a model authoring a prompt *explains* by default instead of recruiting a prior.
- **Provenance:** `prompt-engineering` is vendored from upstream `claude-code-plugins` (tracked in `.claude/.claude-code-plugins-sync.json`) and symlinked into `.claude/`. The real file lives at `claude-plugins/manifest-dev-tools/skills/prompt-engineering/`. This change is a *deliberate accepted local divergence*; a future upstream re-sync would overwrite it unless pushed upstream too.

## 2. Approach
- **Architecture:** One terse `## Leading word` section appended to `references/patterns.md` in the existing Gap / What-it-does shape, then propagate to the three `dist/` distributions and bump versions.
- **Execution Order:**
  - D1 (source edit) → D2 (versioning + distribution sync)
  - Rationale: distributions are generated from source; version/Pi bumps depend on what actually changed under `dist/`.
- **Trade-offs:**
  - [T-1] Minimal divergence vs completeness → Prefer landing *only* leading-words (drop the two optional one-liners — invocation rule, co-location) because the skill is vendored and every added line widens the fork; leading-words is the only high-value import.

## 3. Global Invariants

- [INV-G1] Additive only — no existing high-signal content in `patterns.md` is removed or reworded for taste; the only source change to the prompt body is the new section.
  ```yaml
  verify:
    prompt: |
      Inspect the working-tree diff of claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md
      (git diff). PASS only if every change is an ADDITION forming the new "## Leading word" section (plus at most
      adjacent separators) — no pre-existing pattern is deleted, reordered, or reworded. FAIL if any existing line
      changed. BLOCKED if the diff cannot be obtained.
    phase: 1
  ```
- [INV-G2] Prompt quality — the changed prompt content meets our own bar (no no-ops, no anti-patterns, house voice).
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill against the new "## Leading word" section in
      claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md (the rest of the file is
      pre-existing context). Judge it as an authoring pattern: it must pass the skill's own gap test — a capable
      model writing a prompt would NOT, unprompted, collapse directives onto a single pretrained word or know that
      the fix for a weak directive is a stronger word rather than more words (it explains instead). PASS only if no
      MEDIUM-or-higher findings AND the pattern is not a no-op. Report findings with severity.
    phase: 1
  ```
- [INV-G3] Change intent — the change does what was asked and nothing more (no scope creep into the rejected items).
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full working-tree diff.
      Intended change: add ONE "## Leading word" authoring pattern to the prompt-engineering skill plus mechanical
      version/distribution propagation. PASS only if no LOW-or-higher findings — in particular FAIL if any
      out-of-scope content was added (model-vs-user invocation rule, co-location, predictability framing,
      failure-mode vocabulary, router skills, completion-criteria/premature-completion) or unrelated files changed.
    phase: 1
  ```
- [INV-G4] Portable/universal — the new pattern names portable capability, not harness-bound primitives.
  ```yaml
  verify:
    prompt: |
      Read the new "## Leading word" section in
      claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md. PASS only if it contains
      no harness-specific primitives (no named CLI tool, scheduler, MCP, or product-bound mechanic) — it should read
      as a portable prompt-authoring principle. FAIL otherwise.
    phase: 1
  ```

## 4. Process Guidance
- [PG-1] High-signal only: keep the section terse; match the exact Gap / What-it-does / concrete-shape voice of the surrounding patterns. Don't restructure the file.
- [PG-2] Provenance-aware: edit the real file under `claude-plugins/manifest-dev-tools/` (the `.claude/` path is a symlink to it). Accept the local divergence from upstream; do not attempt to reach the out-of-scope `claude-code-plugins` repo.
- [PG-3] Emotional tone: trusted-advisor register, no urgency/superlatives — consistent with the file.

## 5. Known Assumptions
- [ASM-1] (auto) Version bump is a **patch** (0.27.2 → 0.27.3) | Default: patch | Impact if wrong: a single additive pattern is a refinement, not a new feature surface; if reviewer prefers minor, trivially re-bumped.
- [ASM-2] (auto) The two optional one-liners (invocation rule, co-location) are **dropped** | Default: land leading-words only | Impact if wrong: they can be added later; dropping minimizes the vendored-skill fork (T-1).
- [ASM-3] (auto) `dist/` propagation is done via the **sync-tools** skill (its generator), not hand-copied | Default: run sync-tools | Impact if wrong: hand-editing dist risks drift from the generator's format.
- [ASM-4] (auto) Pi package version is bumped **iff** `dist/pi/` assets actually change | Default: conditional bump per CLAUDE.md | Impact if wrong: an unnecessary or missing Pi bump; verifier checks the dist diff.

## 6. Deliverables

### Deliverable 1: "Leading word" pattern in source `patterns.md`

**Acceptance Criteria:**
- [AC-1.1] A new `## Leading word` section exists in `claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md`, in the same shape as the other patterns (a **Gap** line and a **What it does** explanation, terse), covering: collapse a multi-word directive onto a single compact pretrained word (e.g. `tight`, `relentless`, `red`); recruited as a token it anchors a region of behavior in the fewest words and sharpens activation when reused in a description; the fix for a weak directive is a stronger word, not more words; prefer an existing pretrained word because a coined one recruits no priors.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md. PASS only if it
      contains a new "## Leading word" section that (a) follows the same structural shape as the existing patterns
      (a Gap statement and a What-it-does explanation, terse), and (b) conveys all four ideas: collapse-to-a-
      pretrained-word, token-anchors-behavior/sharpens-activation, stronger-word-not-more-words, and prefer-an-
      existing-word-over-a-coined-one. FAIL if the section is missing, malformed, or omits any of the four ideas.
    phase: 1
  ```

### Deliverable 2: Versioning + distribution consistency

**Acceptance Criteria:**
- [AC-2.1] `claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json` version is bumped from `0.27.2` to `0.27.3`.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json. PASS only if "version" is exactly "0.27.3".
      FAIL otherwise.
    phase: 1
  ```
- [AC-2.2] The `dist/` copies of `patterns.md` (`dist/codex/plugins/manifest-dev-tools/...`, `dist/opencode/skills/...`, `dist/pi/skills/...`) all contain the new "## Leading word" section, matching the source.
  ```yaml
  verify:
    prompt: |
      Compare the "## Leading word" section across the source file
      claude-plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md and each dist copy:
      dist/codex/plugins/manifest-dev-tools/skills/prompt-engineering/references/patterns.md,
      dist/opencode/skills/prompt-engineering/references/patterns.md,
      dist/pi/skills/prompt-engineering/references/patterns.md.
      PASS only if every dist copy contains the same new section as the source (distributions in sync). FAIL if any
      dist copy is missing the section or diverges in content. BLOCKED if a dist path legitimately does not exist for
      this skill.
    phase: 2
  ```
- [AC-2.3] Pi package version in repo-root `package.json` is bumped if and only if `dist/pi/` assets changed; the `pi-cli.md` reference example stays consistent with `package.json`.
  ```yaml
  verify:
    prompt: |
      Determine from the working-tree diff whether any file under dist/pi/ changed. If yes: PASS only if the
      "version" in repo-root package.json (@doodledood/manifest-dev-pi) was bumped in this change AND the package
      version example in .claude/skills/sync-tools/references/pi-cli.md matches package.json. If no dist/pi/ file
      changed: PASS only if package.json version is unchanged. FAIL on mismatch.
    phase: 2
  ```
- [AC-2.4] Repo lint/format/typecheck pass (markdown-only change, expected no-op).
  ```yaml
  verify:
    prompt: |
      Run: ruff check claude-plugins/ && black --check claude-plugins/ && mypy . (from repo root). PASS only if all
      three exit cleanly. FAIL with the offending output otherwise. BLOCKED if a tool is not installed.
    phase: 2
  ```
