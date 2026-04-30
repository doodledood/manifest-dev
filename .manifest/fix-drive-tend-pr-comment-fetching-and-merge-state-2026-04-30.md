# Definition: Fix /drive and /tend-pr — full comment fetching + merge-state health

## 1. Intent & Context

- **Goal:** Close two reported gaps in `/drive` (github adapter) and `/tend-pr-tick`: (a) top-level PR comments are routinely missed because the skills don't enumerate the three distinct `pull_request_read` methods (file-level review threads, formal review submissions, top-level issue-style comments); (b) branch-protection blockers — specifically "branch must be up-to-date with base" — aren't detected, so merge-readiness fires while GitHub still blocks the merge. While fixing (a) and (b), also close two adjacent gaps that compromise the same goal: pagination is unspecified (so paginated comment lists silently truncate), and PR title/description sync is gated on commit-producing ticks (so a manifest amendment that changes scope/intent doesn't propagate to the PR until /do produces a commit).
- **Mental Model:** The skill exists to drive a PR to merge-ready. Every fix here is framed by that higher-order goal: a missed top-level comment delays merge-ready; a missed `mergeable_state: "behind"` blocks merge silently; a stale PR description after a scope amendment confuses reviewers. "Merge State Health" is the unifying lens — replace the narrower "Merge Conflicts" framing with a section that enumerates the GitHub `mergeable_state` taxonomy and a fallback rule for unspecified values. Skills stay non-prescriptive about HOW (model knows MCP semantics) but explicit about WHAT must be fetched and WHICH conditions block merge-ready.
- **Mode:** thorough
- **Interview:** thorough

## 2. Approach

- **Architecture:** Parallel edits to `claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md` and `claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md`. Both skills get: (i) explicit three-method comment-fetch enumeration with pagination in their Read State sections, (ii) renamed `Merge State Health` section replacing `Merge Conflicts`, covering `behind | blocked | unstable | unknown | dirty (conflicts) | other` with explicit dispositions, (iii) `Merge Readiness` preconditions reference `Merge State Health` as authoritative, (iv) PR Description Sync expanded trigger: fires on Intent/Deliverable amendment OR commit-producing tick, with combined-single-sync when both apply. `classification-examples.md` (in `claude-plugins/manifest-dev/skills/tend-pr/references/`) gains top-level-comment rows. tend-pr-tick mirrors drive's `### Inbox — ` disposition log shape (per-event `kind: inline | top-level | review-body`). Wrappers (`tend-pr/SKILL.md`, `drive/SKILL.md`, `drive-tick/SKILL.md`) untouched — the issues live in tick + adapter.

- **Execution Order:**
  - D1 (drive github.md) → D2 (tend-pr-tick) → D3 (classification examples) → D4 (version bumps) → D5 (sync-tools dist regen)
  - Rationale: D1 is the more elaborate adapter — establish the structure there, then mirror to D2. D3 is independent. D4 (versions) before D5 (sync) so dist regenerates with new versions baked in.

- **Risk Areas:**
  - [R-1] drive github.md and tend-pr-tick diverge after the fix despite same root cause | Detect: cross-read both files post-edit; spec must be functionally equivalent on the four touched concerns (comment fetch, merge state, sync trigger, inbox tagging).
  - [R-2] `mergeable_state` enumeration has a gap — an unspecified value triggers undefined behavior | Detect: the new `Merge State Health` section explicitly states a fallback rule for unspecified values.
  - [R-3] Pagination instruction added to one method but not all | Detect: each of the three `pull_request_read` comment methods has explicit pagination guidance.
  - [R-4] Top-level classification examples are too narrow / overfit a few patterns | Detect: examples span actionable / FP / uncertain with diverse top-level patterns (scope-extension request, ship-it acknowledgement, design question, etc.).
  - [R-5] dist drift — source changes land but `dist/` not regenerated | Detect: post-D5, run `sync-tools` and verify all three CLI dists carry the new content.
  - [R-6] Behavior regression — over-instructing destabilizes existing classification or terminal-state logic | Detect: change-intent-reviewer flags no LOW+ regressions; cross-read existing logic (Thread Hygiene, CI Triage, Terminal States) post-edit to confirm untouched.
  - [R-7] Scope creep — "broad" framing tempts unrelated edits | Detect: every edit traces to one of the four user-confirmed gaps + dist sync + version bump.

- **Trade-offs:**
  - [T-1] Inline three-method enumeration vs shared reference file → Prefer inline because it keeps each skill self-contained and parallel; the ~5 lines of duplication is acceptable.
  - [T-2] Rename Merge Conflicts → Merge State Health vs inline edit → Prefer rename because the broader taxonomy doesn't fit under the old name; downstream cross-refs (Gotchas, Merge Readiness) must be updated to the new section name.
  - [T-3] Combined single sync vs two separate syncs per tick → Prefer combined to keep PR edit history low-noise.
  - [T-4] Explicit per-method pagination vs single global pagination rule → Per the user's pick: explicit per method (pagination is the kind of thing where general guidance gets skipped).

## 3. Global Invariants

- [INV-G1] change-intent-reviewer reports no LOW+ findings on the diff. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff against this manifest's intent (close two reported /drive and /tend-pr gaps: missed top-level PR comments and missed branch-protection 'behind' blocker, plus pagination and amendment-sync correctness). Flag any LOW+ behavioral divergence between intent and changes."
  ```

- [INV-G2] prompt-reviewer reports no MEDIUM+ findings on edited skill files. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review the prompt quality of the edited files: claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md, claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md, and claude-plugins/manifest-dev/skills/tend-pr/references/classification-examples.md. Flag MEDIUM+ issues against the prompt-engineering principles."
  ```

- [INV-G3] Skill-pair parity: every concept added to one skill (three-method comment fetch, Merge State Health section, amendment-driven sync trigger, per-event kind tagging) is present in the other. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Cross-read claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md and claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md. Verify both files cover: (1) explicit enumeration of pull_request_read methods get_review_comments + get_reviews + get_comments with pagination; (2) a 'Merge State Health' section handling mergeable_state values behind / blocked / unstable / unknown / dirty + a fallback rule; (3) PR description sync trigger fires on Intent/Deliverable amendment as well as commit-producing ticks, with combined-single-sync when both apply same tick; (4) per-classified-comment kind tagging in the disposition log/output. Report any concept present in one but missing in the other."
  ```

- [INV-G4] Wrapper skills (`tend-pr/SKILL.md`, `drive/SKILL.md`, `drive-tick/SKILL.md`) are unchanged in this PR — **with one explicit exception** (per Amendments §A1): `drive-tick/SKILL.md` §P (Tend PR) may add ONE new step "PR Description Sync — runs every tick, after Thread Hygiene completes; adapter owns the trigger logic; adapter may no-op." No other edits to drive-tick are permitted. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Inspect git diff for the three wrapper paths (claude-plugins/manifest-dev/skills/tend-pr/SKILL.md, claude-plugins/manifest-dev-experimental/skills/drive/SKILL.md, claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md). The first two MUST be unchanged. The third (drive-tick/SKILL.md) MAY contain exactly one additive change to §P (Tend PR): a new step 'PR Description Sync' added after Thread Hygiene, with adapter-owned trigger logic. Confirm: tend-pr/SKILL.md and drive/SKILL.md are byte-identical to origin/main. drive-tick/SKILL.md's only change is the §P additive step described above — no other section modified. Run: git diff -- <three paths> and inspect."
  ```

## 4. Process Guidance

- [PG-1] Frame all fixes around the higher-order goal: get the PR to merge-ready. When deciding placement or wording, ask "does this serve merge-readiness, and is it the right concern in the right section?" — don't add a check that doesn't trace back to a merge blocker.
- [PG-2] Maintain parity between `/drive` github adapter and `/tend-pr-tick`. When editing one, mirror the change in the other in the same /do iteration — don't defer the second skill to a later cycle.
- [PG-3] Don't restructure unrelated sections (Thread Hygiene, CI Triage, Terminal States). Scope is strictly: comment fetching, merge-state taxonomy, PR sync trigger, classification examples, dist sync, version bumps.
- [PG-4] Edit source in `claude-plugins/`, NOT the `.claude/` hardlinks (CLAUDE.md rule). Hardlinks propagate automatically.
- [PG-5] Trust LLM capability — the spec states WHAT must be fetched and WHICH conditions matter, not HOW to make MCP calls. No procedural step-by-step.
- [PG-6] Run `sync-tools` skill at the end (D5), AFTER source edits and version bumps land — so dist captures both.

## 5. Known Assumptions

- [ASM-1] `mcp__github__pull_request_read` continues to expose `get_review_comments`, `get_reviews`, `get_comments` methods as currently documented. | Default: trust the schema verified during /define. | Impact if wrong: spec lands referencing a method that no longer exists; user reports breakage and we patch.
- [ASM-2] GitHub's `mergeable_state` taxonomy stays stable around the named values (`clean | behind | blocked | dirty | unstable | unknown | has_hooks | draft`). | Default: assume stable; the fallback rule for unspecified values protects against new states. | Impact if wrong: low — fallback handles unknown values.
- [ASM-3] `sync-tools` skill is functional and produces correct dist output for `gemini | opencode | codex`. | Default: trust the existing skill. | Impact if wrong: dist drift; user re-runs sync.
- [ASM-4] Hardlinks between `claude-plugins/manifest-dev/skills/...` and `.claude/skills/...` are intact. | Default: per CLAUDE.md, hardlinks are committed; `git status` after editing source should not show `.claude/` separately. | Impact if wrong: edits land in source but session reads stale `.claude/` copy; surfaced by inspection.

## Amendments

### §A1 — 2026-04-30 (from /do, user-approved Option A)

**Trigger:** /verify pass 2 INV-G1 (change-intent-reviewer) found that drive's amendment-only PR Description Sync trigger is unreachable: §PR Description Sync was invoked only from §Write Outputs step 4, and drive-tick gates §Write Outputs on code changes. On amendment-only ticks, drive-tick skips §Write Outputs → trigger (b) was dead text on drive. INV-G4 (wrappers untouched) blocked the structural fix. /escalated as Proposed Amendment with three options; user picked Option A.

**Change:**
- **INV-G4 relaxed** with one explicit exception: `drive-tick/SKILL.md` §P may add ONE new step "PR Description Sync — runs every tick, after Thread Hygiene; adapter owns trigger logic; adapter may no-op." All other drive-tick edits remain forbidden.
- **AC-1.4 updated**: §PR Description Sync is hoisted out of §Write Outputs into its own contract slot in github.md; invoked unconditionally from drive-tick §P via the new step.
- **AC-1.7 added**: explicit verifiable criterion for the drive-tick §P new step.

**Nothing removed.** Prior content (D1–D5, INV-G1–G3, PG-1–G6, ASM-1–4, R-1–R-7, T-1–T-4, AC-1.1–1.6, AC-2.*, AC-3.*, AC-4.*, AC-5.*) is preserved unchanged.

## 6. Deliverables

### Deliverable 1: /drive github adapter — comment fetching + Merge State Health + amendment-driven sync

File: `claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md`

**Acceptance Criteria:**

- [AC-1.1] `Read State` → `Inputs` enumerates three pull_request_read methods explicitly: `get_review_comments` (inline file-level threads), `get_reviews` (formal review bodies), `get_comments` (top-level PR/issue comments). Each method's listing is paginated to exhaustion (perPage + page or cursor-based pagination per the method's contract). | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md and confirm the Read State Inputs section names all three pull_request_read methods (get_review_comments, get_reviews, get_comments) explicitly, and instructs to paginate each to exhaustion."
  ```

- [AC-1.2] `Merge Conflicts` section is renamed to `Merge State Health` and covers the full `mergeable_state` taxonomy: `dirty` (conflicts → existing auto-merge path), `behind` (auto-merge from base — branch protection requires up-to-date), `blocked` (block merge-ready precondition; do not auto-resolve), `unstable` (informational only — non-required check failing), `unknown` (wait for next tick), plus a fallback rule for unspecified values. The existing rebase-vs-merge rule is preserved. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md. Confirm: (1) section header is now 'Merge State Health' (not 'Merge Conflicts'); (2) all five named mergeable_state values are addressed with explicit dispositions; (3) a fallback rule exists for unspecified values; (4) the prefer-merge-over-rebase rule is preserved."
  ```

- [AC-1.3] `Merge Readiness` precondition list references `Merge State Health` as authoritative for merge-state checks (replacing the older "mergeable conflicts = none" wording). | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md and confirm the Merge Readiness preconditions reference the Merge State Health section as the authoritative check (not just 'no conflicts')."
  ```

- [AC-1.4] `PR Description Sync` triggers fire on (a) commit-producing ticks (status quo) AND (b) ticks where a manifest amendment changed Intent (Goal/Mental Model) or Deliverables (added/removed/renamed). When both fire in the same tick, the section specifies a single combined sync with the merged picture. **Invocation path on drive:** §PR Description Sync is hoisted out of §Write Outputs into its own contract slot, invoked unconditionally from drive-tick §P (Tend PR) per the new step (see AC-1.7). Trigger logic in github.md decides whether to fire or no-op. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md PR Description Sync section. Confirm: (1) both triggers (commit-producing tick AND Intent/Deliverable-amendment tick) and the combined-single-sync rule; (2) §PR Description Sync is its own contract (no longer invoked from inside §Write Outputs step 4 — that step is removed or rewritten as a cross-reference); (3) the §Write Outputs step 4 entry is removed or refers to §PR Description Sync as separately invoked."
  ```

- [AC-1.5] `Read State` `## Inbox` per-comment line tags `kind: inline | top-level | review-body` (today says `inline | top-level | review`; if the rename to `review-body` is adopted for clarity, both files use the same vocabulary). | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md and confirm the Read State Output Inbox section's per-comment template tags each event with its kind across the three sources."
  ```

- [AC-1.7] `drive-tick/SKILL.md` §P (Tend PR) gains exactly one new step "PR Description Sync — runs every tick, after Thread Hygiene completes; adapter owns the trigger logic; adapter may no-op." No other edits to drive-tick. This is the INV-G4 exception per Amendments §A1. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev-experimental/skills/drive-tick/SKILL.md §P (Tend PR). Confirm: (1) a new third numbered step 'PR Description Sync' exists, runs every tick, after Thread Hygiene; (2) adapter owns the trigger logic; (3) no other section of drive-tick was modified beyond this addition (run git diff to confirm)."
  ```

- [AC-1.6] No unrelated sections changed: Thread Hygiene, CI Failure Triage classification rules, Terminal States detection (other than wording around merge-state references), Bootstrap. | Verify:
  ```yaml
  verify:
    method: bash
    command: "git diff origin/main...HEAD -- claude-plugins/manifest-dev-experimental/skills/drive/references/platforms/github.md | grep -E '^[-+]' | grep -vE '(^[+-]{3}|^[-+]\\s*$)' | head -200"
    prompt: "Manually inspect — every changed hunk should map to AC-1.1 through AC-1.5. Flag any change to Thread Hygiene rules, CI Triage classification, Terminal State detection (beyond merge-state reference rewording), or Bootstrap."
  ```

### Deliverable 2: /tend-pr-tick — parity with drive

File: `claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md`

**Acceptance Criteria:**

- [AC-2.1] `Read State` section enumerates the three `pull_request_read` methods (`get_review_comments`, `get_reviews`, `get_comments`) with pagination-to-exhaustion guidance, parallel to drive's spec. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md Read State section. Confirm explicit enumeration of all three pull_request_read methods with pagination guidance."
  ```

- [AC-2.2] `Merge Conflicts` section is renamed to `Merge State Health`, covering the same `mergeable_state` taxonomy as drive (dirty / behind / blocked / unstable / unknown + fallback). Behavior parallels drive's adapter on each value. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md. Confirm the Merge Conflicts section is renamed to Merge State Health and covers the same five mergeable_state values plus a fallback as drive's github.md adapter."
  ```

- [AC-2.3] `Merge Readiness` preconditions reference `Merge State Health` as authoritative (consistent with AC-1.3). | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md Merge Readiness section. Confirm preconditions reference Merge State Health (not just conflicts) as the authoritative merge-state gate."
  ```

- [AC-2.4] `PR Description Sync` trigger expanded: fires on Intent/Deliverable amendment in addition to commit-producing tick; combined-single-sync rule for same-tick collisions, parallel to AC-1.4. Babysit-mode behavior (no manifest, no amendment trigger) unchanged. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md PR Description Sync section. Confirm both triggers (commit-producing + Intent/Deliverable amendment) and the combined-single-sync rule. Confirm babysit-mode (no manifest) is explicitly noted as N/A for amendment trigger."
  ```

- [AC-2.5] `Comment Classification` (or its log) tags each classified comment with its `kind: inline | top-level | review-body`, mirroring drive's `### Inbox — ` disposition log. The classification rules themselves (actionable / FP / uncertain) are not modified. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md. Confirm classified comments are logged with a kind tag (inline | top-level | review-body) consistent with drive's adapter. Confirm classification rules (actionable / FP / uncertain) are unchanged."
  ```

- [AC-2.6] No unrelated sections changed (Setup, Concurrency Guard, CI Failure Triage rules, Routing, Status Report, Output Protocol, Security). | Verify:
  ```yaml
  verify:
    method: bash
    command: "git diff origin/main...HEAD -- claude-plugins/manifest-dev/skills/tend-pr-tick/SKILL.md"
    prompt: "Manually inspect — every changed hunk should map to AC-2.1 through AC-2.5."
  ```

### Deliverable 3: classification-examples.md — top-level patterns

File: `claude-plugins/manifest-dev/skills/tend-pr/references/classification-examples.md`

**Acceptance Criteria:**

- [AC-3.1] Each of the three classification tables (Actionable, False Positive, Uncertain) contains at least one top-level-comment example. Examples are diverse (e.g., scope-extension request, ship-it acknowledgement, design question) and not narrowly templated on a single phrasing. | Verify:
  ```yaml
  verify:
    method: codebase
    prompt: "Open claude-plugins/manifest-dev/skills/tend-pr/references/classification-examples.md. Confirm each classification table (Actionable, False Positive, Uncertain) has at least one example labelled or recognizably representing a top-level PR/issue-style comment, and the new examples are diverse rather than templated."
  ```

- [AC-3.2] Existing examples and the Classification Decision Tree are preserved unchanged. | Verify:
  ```yaml
  verify:
    method: bash
    command: "git diff origin/main...HEAD -- claude-plugins/manifest-dev/skills/tend-pr/references/classification-examples.md | grep -E '^-[^-]' | head -50"
    prompt: "Inspect removed lines — should be empty or strictly formatting. No existing example or rule deleted."
  ```

### Deliverable 4: Plugin version bumps

Files: `claude-plugins/manifest-dev/.claude-plugin/plugin.json`, `claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json`

**Acceptance Criteria:**

- [AC-4.1] `manifest-dev` plugin.json version is patch-bumped (Z+1 in X.Y.Z). | Verify:
  ```yaml
  verify:
    method: bash
    command: "diff <(git show origin/main:claude-plugins/manifest-dev/.claude-plugin/plugin.json | grep version) <(grep version claude-plugins/manifest-dev/.claude-plugin/plugin.json) || echo 'changed'"
    prompt: "Confirm the version field changed by exactly the patch component (e.g., 0.4.5 -> 0.4.6); no minor or major bump."
  ```

- [AC-4.2] `manifest-dev-experimental` plugin.json version is patch-bumped. | Verify:
  ```yaml
  verify:
    method: bash
    command: "diff <(git show origin/main:claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json | grep version) <(grep version claude-plugins/manifest-dev-experimental/.claude-plugin/plugin.json) || echo 'changed'"
    prompt: "Confirm the version field changed by exactly the patch component; no minor or major bump."
  ```

### Deliverable 5: Dist regeneration via sync-tools

**Note (amendment, not scope change):** `sync-tools` is scoped to `claude-plugins/manifest-dev/` only — `manifest-dev-experimental` (where `/drive` and `/drive-tick` live) is NOT synced to dist by design (the sync-tools SKILL.md states this explicitly, and no `dist/*/skills/drive*` directories exist). So the only D5 changes are for tend-pr, tend-pr-tick, and classification-examples.

**Acceptance Criteria:**

- [AC-5.1] `sync-tools` skill is invoked AFTER D1–D4 land, regenerating `dist/{gemini,opencode,codex}/` packages from source for the manifest-dev plugin. | Verify:
  ```yaml
  verify:
    method: bash
    command: "git diff --stat origin/main...HEAD -- dist/ | tail -30"
    prompt: "Confirm dist/ has changes for tend-pr, tend-pr-tick, and classification-examples across the three CLI distributions (gemini, opencode, codex). manifest-dev-experimental skills (drive, drive-tick) are NOT synced to dist by design — their absence is expected. If no dist/ changes for tend-pr family, sync-tools wasn't run or didn't pick up the source changes."
  ```

- [AC-5.2] Dist content reflects the source changes (three-method comment fetch + Merge State Health + amendment sync trigger + per-comment kind tagging) for at least one CLI distribution's tend-pr-tick. Spot-check rather than exhaustive. | Verify:
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    prompt: "Open dist/gemini/skills/tend-pr-tick/SKILL.md and dist/gemini/skills/tend-pr/references/classification-examples.md. Confirm the new content appears: (1) three pull_request_read methods enumerated in Read State, (2) Merge State Health section replacing Merge Conflicts, (3) PR Description Sync covers both commit-producing and Intent/Deliverable amendment triggers with combined-single-sync rule, (4) Comment Classification disposition log includes a kind tag. (5) classification-examples.md has top-level-comment patterns. Report whether content is present and properly translated for the gemini distribution format."
  ```

- [AC-5.3] No source files outside this manifest's scope changed during the sync. | Verify:
  ```yaml
  verify:
    method: bash
    command: "git diff --name-only origin/main...HEAD | grep -vE '^(claude-plugins/manifest-dev/skills/tend-pr|claude-plugins/manifest-dev-experimental/skills/drive|claude-plugins/manifest-dev/\\.claude-plugin/plugin\\.json|claude-plugins/manifest-dev-experimental/\\.claude-plugin/plugin\\.json|dist/|\\.claude/skills/(tend-pr|drive))' || echo 'OK: no out-of-scope files'"
    prompt: "Output should be empty or 'OK' or contain only files explicitly in scope. Any out-of-scope source change indicates scope creep."
  ```
