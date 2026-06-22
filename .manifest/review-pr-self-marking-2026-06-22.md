# Definition: Hidden marker to identify review-pr's own comments on a shared account

## 1. Intent & Context
- **Goal:** Stamp a hidden HTML-comment marker on every comment `review-pr` posts and make marker presence — not account authorship — the definition of "an automated review-pr comment," so the skill stops re-processing a human reviewer's manual comments on a shared account. Decision recorded in `docs/adr/20260622-mark-review-pr-comments-with-hidden-marker.md`.
- **Mental Model:** GitHub strips `<!-- … -->` from rendered markdown but returns it in raw API bodies — the same mechanism dependabot/CodeRabbit use to recognize their own comments. The marker is the identity boundary; the existing manifest-mode *content* fingerprint (criterion id + finding substance) stays — the marker only makes its criterion-identification half exact, it does not replace finding-substance comparison.
- **Type:** PROMPTING (skill/prompt edits only; no executable code → no CODING gates).

## 2. Approach
- **Architecture:** Edit canonical skill sources under `claude-plugins/manifest-dev/skills/` (`.claude/` paths are symlinks). Define the marker token canonically once in `review-pr/SKILL.md`; every other mention (MANIFEST_MODE.md, check-pr) references that one spelling rather than restating it.
- **Execution Order:**
  - D1 (review-pr core) → D2 (check-pr awareness) → D3 (ship: version, docs, dist, lint, ADR, PR)
  - Rationale: the token's canonical spelling is established in D1; D2 references it; D3 packages and lands.
- **Risk Areas:**
  - [R-1] Token spelled differently across files (drift). | Detect: grep the token string across edited files — exactly one canonical definition, the rest reference it.
  - [R-2] Distributed copies under `dist/` go stale for the edited skills. | Detect: check whether review-pr/check-pr ship in `dist/`; if so, regenerate via sync-tools.
  - [R-3] Over-editing — restating the rule per surface instead of one uniform instruction. | Detect: review-prompt gate (no MEDIUM+).
- **Trade-offs:**
  - [T-1] Coverage vs minimalism in prompt edits → Prefer minimal, gap-closing lines (prompt-engineering calibration) over exhaustive per-surface restatement.

## 3. Global Invariants
- [INV-G1] Change intent is coherent and the diff matches the stated scope (no scope creep beyond review-pr + check-pr + ship mechanics; babysit-pr unchanged).
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the diff on
      branch claude/review-pr-silent-comments-h93h9i.
      Context: the change adds a hidden HTML-comment marker to review-pr's posted comments and gates its
      "advance our threads" detection on the marker; adds one awareness line to check-pr; bumps version;
      stages an ADR. babysit-pr must be unchanged.
      PASS only if no LOW-or-higher change-intent findings. Report findings with severity.
  ```
- [INV-G2] Prompt quality of the edited skills holds.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill and review the edited prompt files
      (claude-plugins/manifest-dev-tools/skills/review-pr/SKILL.md, claude-plugins/manifest-dev-tools/skills/review-pr/references/MANIFEST_MODE.md,
      .../check-pr/SKILL.md) against the prompt-engineering gap-calibration principles.
      Focus: the new marker lines close a real gap, the token has ONE canonical spelling referenced
      elsewhere (no split restatement), no over-specification, rules hold at the edges.
      PASS only if no MEDIUM-or-higher findings. Report findings with severity.
  ```
- [INV-G3] Repo tooling is clean.
  ```yaml
  verify:
    prompt: |
      Run `ruff check claude-plugins/ && black --check claude-plugins/ && mypy` from the repo root.
      PASS only if all three exit clean. BLOCKED if a tool is missing/unrunnable; report the command output.
  ```

## 4. Process Guidance
- [PG-1] Apply prompt-engineering calibration: add only lines that close the real gap; unify the token's single spelling; do not restate the rule per surface.
- [PG-2] Edit only the canonical sources under `claude-plugins/manifest-dev/skills/`; never edit through `.claude/` symlink copies as if separate.
- [PG-3] High-signal changes only — do not restructure the skills; touch what the four decisions require and nothing more.

## 5. Known Assumptions
- [ASM-1] Task type is PROMPTING with no CODING composition. | Default: no code-bug/test gates encoded. | Impact if wrong: a code path went unverified (none expected — markdown only).
- [ASM-2] "Land it" = implement + commit + push + open PR ready for review. | Default: do not drive CI-green/merge (babysit's job). | Impact if wrong: PR opened but not babysat to mergeable; user can `/babysit-pr` next.
- [ASM-3] No README/marketplace component change needed (no skill/agent added or renamed — behavior change only). | Default: skip README sync; bump version only. | Impact if wrong: a README references the changed behavior and goes slightly stale.
- [ASM-4] Marker token spelling `<!-- manifest-dev:review-pr -->` (with `ac=<id>` appended in manifest mode). | Default: this spelling. | Impact if wrong: cosmetic; any stable namespaced token works as long as it is canonical and referenced.

## 6. Deliverables

### Deliverable 1: review-pr writes and gates on the marker
**Acceptance Criteria:**
- [AC-1.1] `review-pr/SKILL.md` defines the marker token canonically once, instructs stamping it on **every** posted body (new findings, thread replies, summary header, approval body), and gates "threads we authored or replied to" detection on marker presence so unmarked same-account comments read as human and are left alone. The known limitation (legacy unmarked comments read as human; safe-fail) is noted.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/skills/review-pr/SKILL.md.
      PASS only if ALL hold: (1) a hidden HTML-comment marker token is defined once as the canonical
      identity of an automated review-pr comment; (2) the skill instructs stamping it on every posted
      surface — new finding comments, thread replies, summary header, and the approve body; (3) the
      "advance our existing threads"/"threads we authored or replied to" detection is gated on marker
      presence (account authorship alone is no longer sufficient), so unmarked same-account comments are
      treated as human and excluded; (4) the legacy-unmarked-comments limitation is acknowledged.
      Report any missing element as FAIL with the specifics.
  ```
- [AC-1.2] `review-pr/references/MANIFEST_MODE.md` carries the criterion id in the marker for manifest-mode PASS/FAIL comments, references the canonical token (does not re-define it), and preserves that the content fingerprint still compares finding substance (marker makes only criterion identification exact).
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/skills/review-pr/references/MANIFEST_MODE.md and review-pr/SKILL.md.
      PASS only if ALL hold: (1) manifest-mode PASS/FAIL comments carry the criterion id inside the marker;
      (2) the marker token is referenced, not independently re-spelled differently from SKILL.md's canonical
      definition; (3) the text still states the content fingerprint compares finding substance / re-posts on
      finding change — the marker does NOT replace it, only makes criterion identification exact.
      Report any missing element as FAIL.
  ```

### Deliverable 2: check-pr awareness of the marker
**Acceptance Criteria:**
- [AC-2.1] `check-pr/SKILL.md` gains exactly one awareness line at its existing recurring-bot-comment tracking guidance, noting that review-pr's own comments carry the canonical marker as an exact signal — referencing the token, not restating its rule. `babysit-pr/SKILL.md` is unchanged.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/check-pr/SKILL.md and inspect the git diff for
      claude-plugins/manifest-dev/skills/babysit-pr/SKILL.md on branch claude/review-pr-silent-comments-h93h9i.
      PASS only if ALL hold: (1) check-pr has a single added awareness line, co-located with its existing
      "track recurring bot comments by content fingerprint" guidance, stating review-pr's own comments carry
      the marker token as an exact signal; (2) it references the canonical token rather than re-defining the
      marker mechanism; (3) babysit-pr/SKILL.md has no changes in the diff.
      Report violations as FAIL.
  ```

### Deliverable 3: Version, distribution, ADR, and PR
**Acceptance Criteria:**
- [AC-3.1] Both touched plugins' versions are bumped (minor — new behavior): `claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json` (owns review-pr) and `claude-plugins/manifest-dev/.claude-plugin/plugin.json` (owns check-pr). The `dist/` copies of review-pr (SKILL.md + MANIFEST_MODE.md) and check-pr (SKILL.md) under codex/pi/opencode are regenerated via sync-tools to reflect the marker changes.
  ```yaml
  verify:
    prompt: |
      Inspect the git diff on branch claude/review-pr-silent-comments-h93h9i.
      PASS only if ALL hold: (1) claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json version
      increased by a minor bump vs base; (2) claude-plugins/manifest-dev/.claude-plugin/plugin.json version
      increased by a minor bump vs base; (3) the dist/ copies of review-pr (SKILL.md, references/MANIFEST_MODE.md)
      and check-pr (SKILL.md) — under dist/codex, dist/pi, dist/opencode — were regenerated and reflect the
      marker changes (not left stale). Report any unmet condition as FAIL.
  ```
- [AC-3.2] The ADR `docs/adr/20260622-mark-review-pr-comments-with-hidden-marker.md` is committed, and a PR (ready for review, not draft) is open for branch `claude/review-pr-silent-comments-h93h9i` against the default branch.
  ```yaml
  verify:
    prompt: |
      Confirm via git and the GitHub API: (1) docs/adr/20260622-mark-review-pr-comments-with-hidden-marker.md
      is committed on branch claude/review-pr-silent-comments-h93h9i; (2) the branch is pushed to origin;
      (3) an open, non-draft pull request exists for that branch on doodledood/manifest-dev.
      PASS only if all three hold. BLOCKED (not FAIL) if push/PR creation is impossible due to permissions or
      network — report the specific obstacle.
  ```
