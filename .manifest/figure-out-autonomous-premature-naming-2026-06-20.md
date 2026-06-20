# Definition: figure-out `--autonomous` premature-read-naming fix + `/goal` completion-condition backstop

## 1. Intent & Context
- **Goal:** (D1/D2) Edit figure-out's `--autonomous` overrides so the mode stops naming its read prematurely — by telling it the completeness bar *rises* when the user-as-second-presser is gone, detaching "stop" from the mere act of naming, and pointing it at the discipline that already self-activates in the no-auditor case (independent re-derivation). (D3) Add a second, cross-turn guard against the same premature-stopping: make the manifest-dev surfaces construct and print a *proper* `/goal` **completion condition** (measurable end state + check + optional turn bound) instead of the naive `/goal /do <manifest>` — so the host CLI's fresh-model `/goal` evaluator re-runs turns until the work is genuinely done.
- **Mental Model:** This is a prompt change governed by the prompt-engineering gap-calibration discipline (close the real gap with the minimum change; no mechanism-as-prescription; no split-rule). The defect/feature were figured out and agreed with the user — encode, do not re-derive. D1 is localized to `claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md` + a dedup touch in sibling `SKILL.md`. D3 spans the surfaces that emit or document `/goal`: figure-out `autonomous.md`, `define`/`auto`/`do` SKILL.md, the three READMEs, and `plugin.json` — plus the `sync-tools` reference rules. `/goal`'s argument *is* the completion condition (it starts a turn with the condition as directive); a fresh fast model judges it against the transcript after every turn. **Pi has no `/goal`**, so `sync-tools` drops the goal block from Pi dist while Codex/OpenCode keep the concrete `/goal`. All edited skills are sync-tools-governed shared assets (copies under `dist/{codex,opencode,pi}`); several ship under `dist/pi/`, so this is again a Pi-distributed shared-asset change.

## 2. Approach
- **Architecture:** Edit the canonical source file (`claude-plugins/manifest-dev/skills/figure-out/...`; `.claude/` resolves to it via symlink). Then propagate through the deterministic pipeline: bump versions, regenerate dist via sync-tools, run the lint/format/type gate, commit, push, open PR.
- **Execution Order:**
  - D1 (prompt edits) → D2 (versioning, dist sync, gates, PR)
  - Rationale: distribution and verification must reflect the final prompt text.
- **Risk Areas:**
  - [R-1] Edit "fixes" by adding bulk — a new section, an enumerated probe checklist. Detect: anti-bloat AC (AC-1.4) + review-prompt gate flag mechanism-as-prescription.
  - [R-2] Split-rule dedup leaves the no-execution stop stated in neither file, or still in both. Detect: AC-1.2 checks exactly one canonical statement survives and the no-execution semantics are preserved.
  - [R-3] dist copies drift from source if sync-tools isn't run. Detect: AC-2.3 / AC-3.5 byte-compare dist copies to regenerated output.
  - [R-4] (D3) The Pi drop is incomplete — a `/goal` block leaks into Pi dist (Pi has no `/goal`), or the drop also strips the surrounding non-goal prose. Detect: AC-3.5 checks Pi dist carries no `/goal` while Codex/OpenCode do, and the skill's other content survives.
  - [R-5] (D3) The `/goal` conditions become a fixed templated wall (mechanism-as-prescription) or a turn-bound hardcodes an arbitrary number. Detect: INV-G2 review-prompt; ASM-3 keeps the turn bound a user-filled placeholder.
- **Trade-offs:**
  - [T-1] Pointer-to-existing-discipline vs enumerated presses → Prefer the pointer (invoke SKILL.md's re-derivation pass + reference the topic probe file) because an enumerated list is mechanism-as-prescription and leaks (the originating session's "skin in the game" press wasn't in the four).
  - [T-2] (D3) Concrete `/goal` in source (sync adapts per CLI) vs portable capability phrasing → Prefer concrete `/goal` (user decision): it matches the existing repo pattern and gives Claude users a copy-pasteable command; `sync-tools` owns the Pi drop and per-CLI adaptation, so the harness-bound reference is intentional, not a portability defect.

## 3. Global Invariants
- [INV-G1] The change matches its stated intent — the premature-naming fix and the `/goal` completion-condition backstop, nothing more.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff on branch
      claude/figure-out-autonomous-naming-xwqsty. Stated intent has two parts.
      PART A (figure-out premature-naming fix): (1) replacing autonomous.md's claim that the discipline/bar is
      "unchanged" with wording that the completeness bar RISES because the user-as-second-presser and per-turn
      cadence are gone (agent plays both roles); (2) removing the standalone "stop when the read is named" and
      tying the stop to the pre-naming gate being exhausted, while KEEPING the no-chain-into-execution stop;
      (3) a pointer bullet that self-supplies presses by reference (master pre-naming gate + topic probe file)
      and invokes SKILL.md's independent re-derivation pass for the no-auditor case, with NO enumerated probe
      checklist; (4) unifying the no-execution-stop duplication between SKILL.md and autonomous.md.
      PART B (/goal completion-condition backstop): the surfaces that emit or document /goal — figure-out
      autonomous.md, define/auto/do SKILL.md, the three READMEs, plugin.json — now construct/print a CONCRETE
      /goal whose argument is a measurable COMPLETION CONDITION (end state + check + optional turn bound), not
      the naive bare "/goal /do <manifest>" or "/goal /auto <task>"; sync-tools references updated so Pi dist
      drops the /goal block while Codex/OpenCode keep it. Verify the diff does only Parts A+B plus the required
      version bumps and regenerated dist copies — no unrelated scope creep. PASS only if no LOW-or-higher
      findings. Report findings with severity.
    phase: 2
  ```
- [INV-G2] The edited prompt text passes gap-calibration review.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review the edited prompt files —
      claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md,
      claude-plugins/manifest-dev/skills/figure-out/SKILL.md,
      claude-plugins/manifest-dev/skills/define/SKILL.md,
      claude-plugins/manifest-dev/skills/auto/SKILL.md, and
      claude-plugins/manifest-dev/skills/do/SKILL.md — against gap-calibration discipline. Check especially:
      every retained/added line closes a real gap a capable model wouldn't reach on its own; no
      mechanism-as-prescription (no enumerated/hardcoded probe checklist in figure-out; the /goal conditions are
      tuned guidance, not a rigid fixed template; no hardcoded arbitrary turn-bound number — it stays a
      user-filled placeholder); no split-rule duplication (the no-execution stop across figure-out's two files;
      the /goal construction guidance is tailored per surface, not contradictory restatements); each line holds
      at the edges (concrete /goal is an intentional, sync-adapted harness reference). PASS only if no
      MEDIUM-or-higher findings. Report findings with severity.
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Edit the canonical source under `claude-plugins/manifest-dev/skills/figure-out/`, never a `dist/` copy or the `.claude/` symlink target directly. dist copies are regenerated, not hand-edited.
- [PG-2] Treat this as an *update* audit, not a rewrite: preserve effective existing language; change only the lines that carry the defect.

## 5. Known Assumptions
- [ASM-1] (auto) The affected plugin to version-bump is `manifest-dev`. With D3 adding a new capability (goal-backstop guidance), the bump is a **minor** (base 2.11.0 → 2.12.0), not the patch that D1 alone would warrant. Impact if wrong: wrong level; trivially corrected.
- [ASM-2] (auto) Because edited skills ship under `dist/pi/`, the repo-root `package.json` (`@doodledood/manifest-dev-pi`) and the tools package are Pi-distributed shared assets and are bumped (base 0.11.0 → 0.11.2 across this branch's two shared-asset changes), with `sync-tools/references/pi-cli.md`'s package-version example and the opencode plugin mirror kept in lockstep. Impact if wrong: a harmless extra Pi bump, or a desynced Pi package if omitted.
- [ASM-3] (auto) The optional turn/time bound in every printed `/goal` condition is a **user-filled placeholder** (e.g. "stop after N turns"), never a hardcoded number — per prompt-engineering's no-arbitrary-numbers discipline. Impact if wrong: an arbitrary cap could cut off or fail to bound a legitimate run.
- [ASM-4] (auto) figure-out under `/auto` should NOT emit its own nested `/goal` (the wrapping entrypoint owns the goal); autonomous.md frames its `/goal` as the standalone-run backstop. Impact if wrong: a redundant nested goal — confusing but harmless.

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
- [AC-1.4] Anti-bloat: the `autonomous.md` change stays targeted — no new heading/section, no enumerated probe checklist. (Two legitimate additions are expected: D1's premature-naming reframe, and D3's contiguous `/goal` backstop block.)
  ```yaml
  verify:
    prompt: |
      Run: git diff origin/main -- claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md
      (fall back to the branch's merge-base if origin/main is unavailable). PASS only if: no new Markdown
      heading/section was added; AND no enumerated/hardcoded probe checklist was introduced; AND the change is
      targeted edits plus the single contiguous `/goal` backstop block (D3) — NOT a wholesale rewrite of the
      file's existing prose. The file may grow by the `/goal` block; that is expected. FAIL only if a new heading
      appeared, an enumerated probe checklist was baked in, or the existing prose was rewritten wholesale. Report
      the numstat and any added headings.
    phase: 1
  ```

### Deliverable 2: Versioning, distribution sync, gates, and PR

**Acceptance Criteria:**
- [AC-2.1] The `manifest-dev` plugin version is bumped to a new MINOR (feature: the goal-backstop adds a capability).
  ```yaml
  verify:
    prompt: |
      Compare claude-plugins/manifest-dev/.claude-plugin/plugin.json version against origin/main (or merge-base,
      which is 2.11.0). PASS only if the version increased by a MINOR increment relative to the base — i.e. the
      minor digit incremented and patch reset (2.11.0 -> 2.12.0). FAIL if unchanged, only patch-bumped, or
      major-bumped. Report old and new versions.
    phase: 1
  ```
- [AC-2.2] The Pi package versions and documented example are bumped/synced because `dist/pi/` shared assets changed.
  ```yaml
  verify:
    prompt: |
      Edited skills (figure-out, define, auto, do) ship under dist/pi/, so the repo-root package.json
      (@doodledood/manifest-dev-pi) and packages/manifest-dev-pi-tools/package.json are Pi-distributed shared
      assets. PASS only if: both package versions increased relative to origin/main (base 0.11.0) and are in
      lockstep with each other; AND the package-version example in .claude/skills/sync-tools/references/pi-cli.md
      matches the new package.json version; AND the opencode plugin mirror dist/opencode/plugin/package.json
      version was bumped to match the manifest-dev plugin version. FAIL on any mismatch or unbumped file. Report
      the versions found in each file.
    phase: 1
  ```
- [AC-2.3] The `dist/` copies of the figure-out files (`references/autonomous.md` and `SKILL.md`) match freshly regenerated output.
  ```yaml
  verify:
    prompt: |
      Verify the distribution copies of figure-out's references/autonomous.md AND SKILL.md under
      dist/codex/plugins/manifest-dev, dist/opencode, and dist/pi reflect the edited source (content-equivalent
      after any per-target transform — the load-bearing D1 changes are present and the old "unchanged" / "stop
      when the read is named" / "Under `--autonomous`, surface the read and stop — chaining onward belongs to the
      caller" wording is absent in each). The reliable check: re-run the sync (invoke the manifest-dev:sync-tools
      skill, or its generation command) and confirm `git status` shows no further changes to those dist files.
      PASS only if all dist copies are in sync. FAIL if any dist copy still carries pre-fix wording or differs
      from regenerated output. Report per-target status. (D3 dist/goal-block behavior is checked by AC-3.5.)
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

### Deliverable 3: `/goal` completion-condition backstop across surfaces

**Acceptance Criteria:**
- [AC-3.1] figure-out `autonomous.md` emits, on autonomous activation, a copy-pasteable concrete `/goal` whose argument is the Read's completion condition — not a bare command wrapper.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/figure-out/references/autonomous.md. PASS only if ALL hold:
      (a) it instructs the agent, when --autonomous activates, to surface a copy-pasteable `/goal <condition>`;
      (b) the condition is a measurable Read-completion bar (the Read named with full anatomy: load-bearing
      branches pressed, the independent re-derivation run, the rival set no longer moving; not a first-pass read)
      — i.e. a real completion condition, NOT the naive bare "/goal /do ..." form;
      (c) it notes this is the standalone-run backstop and that under /auto the goal belongs to the wrapping
      entrypoint (no redundant nested goal), and mentions the /goal evaluator is a fresh model that re-runs turns
      on an early stop;
      (d) it stays tight (a few lines) with NO new Markdown heading/section added to the file.
      FAIL if the emission is missing, the condition is just a wrapped command with no measurable end state, or a
      new section was added. Report exact quotes.
    phase: 1
  ```
- [AC-3.2] define's handoff prints a manifest-completion `/goal` condition; the naive `/goal /do <path>` is gone.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/define/SKILL.md (the "Complete" handoff block). PASS only if:
      (a) it still offers the foreground form "To execute: /do <manifest-path>"; AND (b) the unattended form is a
      concrete `/goal` whose condition is a measurable manifest-completion bar (every Acceptance Criterion and
      Global Invariant verifies PASS and /done is reported; don't stop while any gate is unverified, FAIL, or
      escalation-pending; optional user-filled turn bound); AND (c) the old naive bare "/goal /do <manifest-path>"
      line (a wrapped command with no completion condition) no longer appears. FAIL if the naive line survives or
      no measurable condition is printed. Report exact quotes.
    phase: 1
  ```
- [AC-3.3] `auto` and `do` SKILL.md each carry concrete `/goal` completion-condition guidance.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/auto/SKILL.md and claude-plugins/manifest-dev/skills/do/SKILL.md.
      PASS only if: auto/SKILL.md gives a recommended unattended-launch `/goal` whose condition spans the full
      chain (figure-out Read named -> define manifest written -> /do reports /done with all ACs/GIs PASS; don't
      stop while any phase is incomplete; optional turn bound); AND do/SKILL.md notes that an unattended /do run
      is launched under the manifest-completion `/goal` condition (the form define prints) as the cross-turn
      backstop. Both must be concrete completion conditions, not bare "/goal /do"/"/goal /auto" wrappers. FAIL if
      either is missing or naive. Report exact quotes.
    phase: 1
  ```
- [AC-3.4] The three READMEs and plugin.json are upgraded — no naive bare `/goal` example without a completion condition remains in source.
  ```yaml
  verify:
    prompt: |
      Inspect README.md (root), claude-plugins/README.md, claude-plugins/manifest-dev/README.md, and
      claude-plugins/manifest-dev/.claude-plugin/plugin.json. PASS only if: (a) at least one concrete
      good-condition `/goal` example (a measurable completion condition) is shown; (b) NO bare
      "/goal /do <manifest-path>" or "/goal /auto <task>" example without a following completion condition
      remains as the *recommended* form in these source docs; (c) the explanation that `/goal` is the host CLI's
      turn-continuation wrapper is retained; (d) plugin.json's description no longer presents the bare
      "/goal /do <manifest>" as the recommended wrapper. FAIL if a naive recommended example survives. Report
      exact quotes and file:line.
    phase: 1
  ```
- [AC-3.5] sync-tools references are updated and the dist reflects the Pi `/goal`-drop while Codex/OpenCode keep the concrete `/goal`.
  ```yaml
  verify:
    prompt: |
      Two parts. PART 1 (rules): Read .claude/skills/sync-tools/references/pi-cli.md and opencode-cli.md. PASS
      part 1 only if the pi-cli.md rule to drop the `/goal` unattended-execution content is generalized to the
      new (multi-line) goal block across the affected skills (define/figure-out/auto/do), and opencode-cli.md's
      note references the new condition-based form. PART 2 (dist): For each affected skill (figure-out
      autonomous.md, define/auto/do SKILL.md), confirm the dist/pi copy contains NO `/goal` token while the
      dist/codex and dist/opencode copies DO contain the concrete `/goal` condition; and confirm the surrounding
      non-goal content still survives in the Pi copies (the drop removed only the goal block). The reliable
      check: re-run sync-tools and confirm `git status` shows no further changes. PASS only if BOTH parts hold.
      FAIL with specifics (file:line / grep results) otherwise.
    phase: 1
  ```
