# Definition: Fix figure-out `--autonomous` premature-read-naming gap

## 1. Intent & Context
- **Goal:** Edit figure-out's `--autonomous` overrides so the mode stops naming its read prematurely — by telling it the completeness bar *rises* when the user-as-second-presser is gone, detaching "stop" from the mere act of naming, and pointing it at the discipline that already self-activates in the no-auditor case (independent re-derivation).
- **Mental Model:** This is a prompt bug fix governed by the prompt-engineering gap-calibration discipline (close the real gap with the minimum change; no mechanism-as-prescription; no split-rule). The defect was figured out and agreed in the preceding figure-out session — encode it, do not re-derive. The fix is localized to `claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md`, with one targeted dedup touch in the sibling `SKILL.md`. `autonomous.md` is a sync-tools-governed shared asset (copies under `dist/{codex,opencode,pi}`), and because it ships under `dist/pi/`, changing it is a Pi-distributed shared-asset change.

## 2. Approach
- **Architecture:** Edit the canonical source file (`claude-plugins/manifest-dev/skills/figure-out/...`; `.claude/` resolves to it via symlink). Then propagate through the deterministic pipeline: bump versions, regenerate dist via sync-tools, run the lint/format/type gate, commit, push, open PR.
- **Execution Order:**
  - D1 (prompt edits) → D2 (versioning, dist sync, gates, PR)
  - Rationale: distribution and verification must reflect the final prompt text.
- **Risk Areas:**
  - [R-1] Edit "fixes" by adding bulk — a new section, an enumerated probe checklist. Detect: anti-bloat AC (AC-1.4) + review-prompt gate flag mechanism-as-prescription.
  - [R-2] Split-rule dedup leaves the no-execution stop stated in neither file, or still in both. Detect: AC-1.2 checks exactly one canonical statement survives and the no-execution semantics are preserved.
  - [R-3] dist copies drift from source if sync-tools isn't run. Detect: AC-2.3 byte-compares dist copies to regenerated output.
- **Trade-offs:**
  - [T-1] Pointer-to-existing-discipline vs enumerated presses → Prefer the pointer (invoke SKILL.md's re-derivation pass + reference the topic probe file) because an enumerated list is mechanism-as-prescription and leaks (the originating session's "skin in the game" press wasn't in the four).

## 3. Global Invariants
- [INV-G1] The change matches its stated intent — the premature-naming fix, nothing more, nothing less.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the diff on branch
      claude/figure-out-autonomous-naming-xwqsty. Stated intent: fix figure-out's --autonomous mode premature
      read-naming by (1) replacing autonomous.md's claim that the discipline/bar is "unchanged" with wording
      that the completeness bar RISES because the user-as-second-presser and per-turn cadence are gone (agent
      plays both roles); (2) removing the standalone "stop when the read is named" and tying the stop to the
      pre-naming gate being exhausted, while KEEPING the no-chain-into-execution stop; (3) adding a pointer
      bullet that self-supplies presses by reference (master pre-naming gate + topic probe file) and invokes
      SKILL.md's independent re-derivation pass for the no-auditor case, with NO enumerated probe checklist;
      (4) unifying the no-execution-stop duplication shared between SKILL.md and autonomous.md. Verify the diff
      does only this — no scope creep, no unrelated edits beyond the required version bumps and regenerated
      dist copies. PASS only if no LOW-or-higher findings. Report findings with severity.
    phase: 2
  ```
- [INV-G2] The edited prompt text passes gap-calibration review.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review the two edited prompt files —
      claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md and
      claude-plugins/manifest-dev/skills/figure-out/SKILL.md — against gap-calibration discipline. Check
      especially: every retained/added line closes a real gap a capable model wouldn't reach on its own;
      no mechanism-as-prescription (no enumerated/hardcoded probe checklist — presses must stay illustrative
      and by-reference); no split-rule duplication of the no-execution stop across the two files; each line
      holds at the edges of where the prompt runs. PASS only if no MEDIUM-or-higher findings. Report findings
      with severity.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Edit the canonical source under `claude-plugins/manifest-dev/skills/figure-out/`, never a `dist/` copy or the `.claude/` symlink target directly. dist copies are regenerated, not hand-edited.
- [PG-2] Treat this as an *update* audit, not a rewrite: preserve effective existing language; change only the lines that carry the defect.

## 5. Known Assumptions
- [ASM-1] (auto) The affected plugin to version-bump is `manifest-dev` (figure-out lives in `claude-plugins/manifest-dev/`). Default: patch bump. Impact if wrong: wrong plugin's version moves; trivially corrected.
- [ASM-2] (auto) Because `autonomous.md` ships under `dist/pi/`, the repo-root `package.json` (`@doodledood/manifest-dev-pi`) is a Pi-distributed shared asset and is bumped, with `sync-tools/references/pi-cli.md`'s package-version example kept in sync (per CLAUDE.md). Default: patch bump. Impact if wrong: an unnecessary Pi version bump — harmless; omitting it if required would desync the Pi package.

## 6. Deliverables

### Deliverable 1: figure-out `--autonomous` prompt fix

**Acceptance Criteria:**
- [AC-1.1] `autonomous.md` line-3 reframe: it no longer states the discipline/bar is "unchanged"; instead it states the completeness bar rises because there is no user to press back (no second presser, no per-turn cadence) and the agent plays both roles.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if: the text no
      longer contains a claim that the investigation/discipline/bar is "unchanged"; AND it explicitly conveys
      that losing the user removes a second presser (and the one-question-per-turn cadence) so the completeness
      bar RISES rather than relaxes, with the agent now playing both roles. FAIL if the "unchanged" framing
      survives anywhere, or the bar-rises reframe is absent. Report exact quotes.
    phase: 1
  ```
- [AC-1.2] Stop is detached from the act of naming, the no-chain-into-execution stop is preserved, and the cross-file split-rule duplication is unified.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md and the sibling SKILL.md.
      PASS only if ALL hold: (a) autonomous.md no longer contains a standalone instruction to "stop when the
      read is named" that licenses name-then-stop; (b) the stop is instead conditioned on the pre-naming gate
      being exhausted (rivals stopped moving / presses run); (c) the no-chain-into-execution stop ("chaining
      into execution belongs to the caller", or equivalent) is still present exactly once as the canonical
      statement — not duplicated near-verbatim across BOTH SKILL.md and autonomous.md. FAIL if the standalone
      name-then-stop survives, if the no-execution stop was dropped entirely, or if the duplication remains in
      both files. Report exact quotes from each file.
    phase: 1
  ```
- [AC-1.3] A pointer bullet self-supplies the presses by reference and invokes the independent re-derivation pass for the no-auditor case — with no enumerated probe checklist.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if: it instructs
      the agent, as sole auditor, to run the presses that a user would otherwise force — BY REFERENCE to the
      master pre-naming gate and the topic's probe file (tasks/*.md), NOT as a hardcoded enumerated list of
      specific probes; AND it invokes SKILL.md's independent re-derivation pass before naming, noting that pass
      already applies when "no one will audit before relied on" — which autonomous mode is. FAIL if a fixed
      enumerated probe checklist is baked in (e.g. a hardcoded list "informed-dissent, base rate, decision-
      relevance, recency" presented as THE set), or if the re-derivation pass is not invoked. Report exact quotes.
    phase: 1
  ```
- [AC-1.4] Anti-bloat: the net change to `autonomous.md` is a handful of lines and introduces no new heading/section.
  ```yaml
  verify:
    prompt: |
      Run: git diff origin/main -- claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md
      (fall back to diffing against the branch's merge-base if origin/main is unavailable). PASS only if the
      net line delta is small (on the order of a handful of lines, not a wholesale rewrite) AND no new Markdown
      heading/section was added to the file. FAIL if a new section appeared or the file roughly doubled. Report
      the numstat and any added headings.
    phase: 1
  ```

### Deliverable 2: Versioning, distribution sync, gates, and PR

**Acceptance Criteria:**
- [AC-2.1] The `manifest-dev` plugin version is bumped (patch) for the prompt fix.
  ```yaml
  verify:
    prompt: |
      Compare claude-plugins/manifest-dev/.claude-plugin/plugin.json version against origin/main (or merge-base).
      PASS only if the version increased by a patch increment (x.y.Z -> x.y.Z+1) relative to the base. FAIL if
      unchanged or bumped at the wrong level. Report old and new versions.
    phase: 1
  ```
- [AC-2.2] The Pi package version and its documented example are bumped/synced because a `dist/pi/` shared asset changed.
  ```yaml
  verify:
    prompt: |
      Because claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md ships under dist/pi/, the
      repo-root package.json (@doodledood/manifest-dev-pi) is a Pi-distributed shared asset. PASS only if:
      package.json version increased relative to origin/main (or merge-base); AND the package-version example in
      claude-plugins/.../sync-tools/references/pi-cli.md (path: skills/sync-tools/references/pi-cli.md) matches
      the new package.json version. FAIL if package.json is unchanged or the pi-cli.md example is out of sync.
      Report the versions found in both files.
    phase: 1
  ```
- [AC-2.3] The `dist/` copies of `figure-out/references/autonomous.md` match freshly regenerated output (sync-tools was run).
  ```yaml
  verify:
    prompt: |
      Verify the distribution copies of figure-out/references/autonomous.md under dist/codex/plugins/manifest-dev,
      dist/opencode, and dist/pi reflect the edited source (content-equivalent after any per-target transform —
      at minimum the load-bearing changed sentences from the source are present and the old "unchanged"/"stop when
      the read is named" wording is absent in each). The reliable check: re-run the sync (invoke the manifest-dev:
      sync-tools skill, or its generation command) and confirm `git status` shows no further changes to those dist
      files afterward. PASS only if all three dist copies are in sync with source. FAIL if any dist copy still
      carries the pre-fix wording or differs from regenerated output. Report per-target status.
    phase: 1
  ```
- [AC-2.4] The repo's pre-PR gate passes.
  ```yaml
  verify:
    prompt: |
      Run: ruff check claude-plugins/ && black --check claude-plugins/ && mypy. PASS only if all three exit
      clean (no lint errors, no formatting diffs, no type errors). No Python source changed, so this should pass
      untouched; FAIL and report output if any gate errors.
    phase: 1
  ```
- [AC-2.5] The work is committed and pushed to the designated branch with a PR open and ready for review.
  ```yaml
  verify:
    prompt: |
      PASS only if: branch claude/figure-out-autonomous-naming-xwqsty exists on origin and contains the commit(s)
      with these changes; AND an open, non-draft pull request exists for that branch in the doodledood/manifest-dev
      repository. Use the available GitHub tooling to confirm the PR state. FAIL if no PR exists, the PR is a draft,
      or the branch wasn't pushed. Report the PR number/URL and draft state.
    phase: 2
  ```
