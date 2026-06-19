# Definition: babysit-pr `--log` journal + check-pr stateless simplification

## 1. Intent & Context

- **Goal:** Give `babysit-pr` an optional `--log` journal (figure-out's persisted append-only model) so a warm/persisted babysit lifecycle keeps coherence and scope across in-session compaction; couple it with removing `check-pr`'s dead retrigger/wait counting machinery (relocating runaway protection to `/do`, fed by the new log); keep all `dist/` tool distributions synced.
- **Mental Model:**
  - `babysit-pr` is a thin orchestrator (resolve manifest → `/do` → `/do` spawns a general-purpose verifier that activates `check-pr`). The lifecycle judgment ("what to address") lives in `/do`, not babysit-pr or check-pr.
  - The journal is the **single state store**. Warm/persisted is the primary case; the file survives compaction there. Fresh GitHub-Actions reinvocation is **niche** — degrade gracefully (no log → today's behavior), do not build native-state reconstruction or a PR-comment store now.
  - `check-pr`'s `Prior-retrigger context` input + cycle counters + cap tables are **verified dead** (no caller feeds the input; nothing writes the `### CI Retrigger`/`### Wait` lines; the one other consumer `drive` no longer exists). Remove them; check-pr becomes a pure stateless inspector. Runaway protection moves to `/do` using the log.

## 2. Approach

- **Architecture:** Edit `claude-plugins/` source skill prompts (the `.claude/` copies are symlinks). Add the `--log` surface to `babysit-pr`; teach `/do` to read/append the journal and own runaway protection; strip the dead counting machinery from `check-pr`; drop the stale reference in `PR_LIFECYCLE.md`; regenerate `dist/` via `sync-tools`; bump versions and sync READMEs.
- **Execution Order:**
  - D3 (check-pr removal) → D4 (PR_LIFECYCLE) → D1 (babysit-pr `--log`) → D2 (`/do` journal + runaway) → D5 (sync + housekeeping)
  - Rationale: removals and source prompt edits first; distribution regeneration and version/README housekeeping last so they capture the final source state.
- **Risk Areas:**
  - [R-1] Removing check-pr's cap machinery leaves a dangling reference or orphaned mention. | Detect: grep check-pr + callers for `Cycle`, `prior-retrigger`, `retrigger budget`, `### Wait`.
  - [R-2] Runaway protection silently lost rather than relocated — babysit could loop forever. | Detect: `/do` must explicitly own a stop condition fed by the log.
  - [R-3] `dist/` copies drift from source after edits. | Detect: re-run sync; compare touched files.
- **Trade-offs:**
  - [T-1] Coherence/continuity vs build cost → Prefer the minimal warm-case journal; the niche fresh/Actions durability (native-state / PR-comment) is explicitly deferred, not built.
  - [T-2] Stateless check-pr vs built-in cadence governor for standalone use → Prefer stateless inspector; keep only the stateless per-cycle wait *durations* as guidance, drop the counted caps.

## 3. Global Invariants

- [INV-G1] Every created/modified prompt file (SKILL.md, task file, references) is high-quality prompt content.
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev-tools:review-prompt skill. Review every prompt file changed by this work
      (git diff against the branch base) — `babysit-pr/SKILL.md`, `do/SKILL.md`, `check-pr/SKILL.md`,
      `define/tasks/PR_LIFECYCLE.md`, and any others touched. Apply the gap-calibration discipline:
      changes must close a real gap, trust the model, stay minimal and high-altitude.
      PASS only if no MEDIUM-or-higher findings across the changed prompt content. Report findings with severity.
    phase: 2
  ```
- [INV-G2] Changes match this manifest's intent — no scope creep (no native-state reconstruction, no PR-comment store, no unrelated rewrites).
  ```yaml
  verify:
    prompt: |
      Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff
      against the branch base. The intended change is exactly: add `--log` to babysit-pr; teach `/do` to
      read/append the journal and own runaway protection; remove check-pr's dead retrigger/wait counting
      machinery (keeping stateless wait durations); update PR_LIFECYCLE.md; sync dist/ + versions + READMEs.
      Flag anything outside that intent — especially any built (not merely noted-as-deferred) native-state
      reconstruction or PR-comment journal store. PASS only if no LOW-or-higher findings.
    phase: 2
  ```
- [INV-G3] Lint, format, and typecheck are clean.
  ```yaml
  verify:
    prompt: |
      Run `ruff check claude-plugins/ && black --check claude-plugins/ && mypy` from the repo root.
      PASS only if all three succeed with no errors. On failure, report the exact tool output.
    phase: 2
  ```
- [INV-G4] Source-of-truth discipline: edits land in `claude-plugins/` source files; `.claude/` symlinks remain intact and resolve to the edited source.
  ```yaml
  verify:
    prompt: |
      Confirm the edited skill files under `claude-plugins/` are the real source, and that the corresponding
      `.claude/skills|agents` entries are still symlinks resolving to them (e.g. `readlink` / `ls -l` on
      `.claude/skills/...` for any touched skill that has a `.claude/` mirror). PASS if no edits broke a symlink
      into a divergent real file. FAIL listing any symlink replaced by a divergent copy.
  ```

## 4. Process Guidance

- [PG-1] Edit the `claude-plugins/` source versions only; `.claude/` resolves through symlinks to the same file.
- [PG-2] Apply prompt-engineering calibration: add only lines that close a real gap, trust the model, keep edits minimal and high-altitude. Don't restructure files beyond what the change needs.
- [PG-3] Develop on branch `claude/babysit-pr-skill-logging-y2l5es`; do not push to another branch.
- [PG-4] Model the `--log` semantics on `.claude/skills/figure-out/references/LOG.md` (default `~/.manifest-dev/logs/`, explicit-path override, resume-or-create, append-only) without copying figure-out-specific framing wholesale.

## 5. Known Assumptions

- [ASM-1] (auto) Deliverables are split by component (babysit-pr / do / check-pr / PR_LIFECYCLE / sync). | Default: component split. | Impact if wrong: cosmetic — same edits, different grouping.
- [ASM-2] (auto) `manifest-dev-tools` gets a **minor** bump (new `--log` capability); `manifest-dev` gets a **minor** bump (check-pr behavior + /do journal). | Default: tools minor, dev minor. | Impact if wrong: wrong semver class; trivially adjusted.
- [ASM-3] (auto) Pi package (`@doodledood/manifest-dev-pi`) version bumps because Pi-distributed shared assets under `dist/pi/` change (check-pr, babysit-pr, PR_LIFECYCLE). | Default: bump Pi patch/minor and sync the `pi-cli.md` example. | Impact if wrong: stale Pi package version vs distributed assets.
- [ASM-4] (auto) The `--log` journal records dead-end memory + operational notes (retrigger/wait counts); scope rulings stay where they already are (PR thread replies), not duplicated into the journal. | Default: dead-end + operational notes only. | Impact if wrong: journal slightly under- or over-scoped; easily extended later.
- [ASM-5] (auto) "All tools synced" = the three `dist/` targets (opencode, pi, codex) regenerated via `sync-tools` so touched files match source. | Default: regenerate all three. | Impact if wrong: a distribution drifts from source.

## 6. Deliverables

### Deliverable 1: babysit-pr `--log` surface

**Acceptance Criteria:**
- [AC-1.1] `babysit-pr/SKILL.md` documents an optional `--log [path]` flag: persisted append-only journal; default path under `~/.manifest-dev/logs/` keyed to the PR so a warm reinvocation re-finds it; explicit `--log <path>` overrides; resume existing / create new. The `argument-hint` frontmatter includes `--log`.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md. PASS only if it documents an optional
      `--log [path]` flag with: (1) append-only persisted journal semantics; (2) default location under
      `~/.manifest-dev/logs/` keyed to the PR; (3) explicit-path override; (4) resume-or-create behavior; and
      (5) `--log` present in the `argument-hint`. FAIL naming any missing element.
  ```
- [AC-1.2] The log path is threaded into the `/do` invocation babysit-pr makes. `/do` is the sole journal consumer; the stateless `check-pr` verifier (per Deliverable 3) neither reads nor needs it, so the journal is deliberately NOT threaded through `define`/verifier steering.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md. PASS only if the `--log` path is
      explicitly threaded into the downstream `/do` execution rather than being a parsed-but-unused flag.
      The journal is `/do`'s alone — it is correct that it is NOT threaded into define/verifier steering,
      since check-pr is stateless. FAIL only if `--log` is accepted but never propagated to `/do`.
  ```

### Deliverable 2: `/do` journal consumption + runaway protection relocation

**Acceptance Criteria:**
- [AC-2.1] `do/SKILL.md` states that, when a log/journal path is supplied, `/do` reads it before deciding retries/comment-judgments and appends after acting — recording dead-end memory (attempted-and-abandoned fixes / rejected approaches with no commit) plus operational notes (retrigger/wait activity).
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/do/SKILL.md. PASS only if it specifies that, given a supplied
      journal/log path, /do (1) reads prior journal context before retry/judgment decisions and (2) appends
      after acting, capturing dead-end memory and operational notes. FAIL if journal read/append is absent or
      only one side (read or append) is specified.
  ```
- [AC-2.2] `/do` owns runaway protection: a stop condition (too many retriggers/waits) driven by the journal + session memory, routing to `/escalate` or a pending-summary when exhausted — explicitly replacing check-pr's removed counter. No reliance on a check-pr cycle/cap counter remains.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/do/SKILL.md. PASS only if /do owns a runaway/stop condition for
      repeated retrigger/wait cycles, fed by the journal (and warm-session memory), and does NOT depend on a
      check-pr-provided cycle/cap counter. FAIL if runaway protection is absent (silently dropped) or still
      delegated to check-pr's removed counting input.
  ```
- [AC-2.3] Graceful degradation: with no journal (fresh/GitHub-Actions reinvocation), behavior is unchanged from today (no regression); native-state reconstruction and a PR-comment store are mentioned only as deferred, not implemented.
  ```yaml
  verify:
    prompt: |
      Inspect do/SKILL.md and babysit-pr/SKILL.md. PASS only if: (1) absence of a journal degrades to current
      behavior with no new failure path; and (2) native-state reconstruction / PR-comment journal stores are
      either absent or explicitly framed as deferred/not-built. FAIL if either durable-store mechanism was
      actually implemented, or if a missing log breaks the flow.
  ```

### Deliverable 3: check-pr stateless simplification

**Acceptance Criteria:**
- [AC-3.1] `check-pr/SKILL.md` no longer contains the dead counting machinery: the `Prior-retrigger context` input, the `Cycle: <current>/<cap>` FAIL field, the cycle counter, the per-gate cycle-cap tables, and the retrigger-budget counter are all removed.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/check-pr/SKILL.md and grep it for: `Prior-retrigger`,
      `prior-retrigger`, `Cycle:`, `cycle cap`, `Cycle counter`, `Retrigger budget`, `### CI Retrigger`,
      `### Wait`. PASS only if the counting/cap machinery (input, Cycle field, cycle counter, cap tables,
      retrigger-budget counter) is gone. FAIL listing any surviving reference.
  ```
- [AC-3.2] The stateless per-cycle wait *durations* (CI ~300s, reviewer ~600s, bot scanner ~120s) remain as guidance for choosing the `bash sleep <N>` directive — durations kept, counted caps removed.
  ```yaml
  verify:
    prompt: |
      Read check-pr/SKILL.md. PASS only if stateless per-cycle wait DURATION guidance (approx values for CI,
      reviewer, bot scanner) is still present to size the sleep/wait directive, WITHOUT reintroducing any
      counted cap or cycle counter. FAIL if the durations were removed too, or if a counted cap remains.
  ```
- [AC-3.3] check-pr reads coherently as a pure stateless inspector — no dangling references to the removed mechanism anywhere in the file (FAIL examples, wait-cadence section, output schema).
  ```yaml
  verify:
    prompt: |
      Read check-pr/SKILL.md end to end. PASS only if it is internally coherent as a stateless inspector: no
      output-schema field, example, or prose still references a Cycle count, cap, budget counter, or prior-
      retrigger input that was removed. FAIL quoting any orphaned reference.
  ```

### Deliverable 4: PR_LIFECYCLE task-file update

**Acceptance Criteria:**
- [AC-4.1] `define/tasks/PR_LIFECYCLE.md` no longer references the prior-retrigger-context input or a check-pr retrigger-cap counter; any retained retrigger guidance is reworded to match the stateless check-pr (or removed). No dangling reference to the removed mechanism.
  ```yaml
  verify:
    prompt: |
      Read claude-plugins/manifest-dev/skills/define/tasks/PR_LIFECYCLE.md and grep for `prior-retrigger`,
      `retrigger context`, `scopes the counter`. PASS only if the prior-retrigger-context / cap-counter
      reference is gone and any remaining retrigger mention is consistent with a stateless check-pr.
      FAIL quoting any surviving stale reference.
  ```

### Deliverable 5: Distribution sync + housekeeping

**Acceptance Criteria:**
- [AC-5.1] The `dist/` targets (opencode, pi, codex) are regenerated so the touched files match source: the removed check-pr counting machinery is absent from all `dist/**/check-pr/SKILL.md` and `dist/**/PR_LIFECYCLE.md` copies, and the new `--log` content is present in every `dist/**/babysit-pr/SKILL.md` copy that ships it.
  ```yaml
  verify:
    prompt: |
      Grep dist/ for stale content: `Prior-retrigger`, `Cycle counter`, `Retrigger budget` must NOT appear in
      any dist/**/check-pr/SKILL.md, and the prior-retrigger reference must be gone from dist/**/PR_LIFECYCLE.md.
      Then confirm every dist copy of babysit-pr/SKILL.md that ships it contains the `--log` documentation
      matching source. PASS only if dist copies match the updated source (no stale removed content, new content
      present). FAIL listing any drifted file. (If a target legitimately excludes a skill, that exclusion is OK.)
    phase: 2
  ```
- [AC-5.2] Versions bumped: `manifest-dev-tools` plugin.json and `manifest-dev` plugin.json bumped per change class; the Pi package version in repo-root `package.json` bumped because `dist/pi/` assets changed, and the package-manifest example in `.claude/skills/sync-tools/references/pi-cli.md` matches the new `package.json` version.
  ```yaml
  verify:
    prompt: |
      Compare against the branch base (git): claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json and
      claude-plugins/manifest-dev/.claude-plugin/plugin.json must have higher versions; repo-root package.json
      (@doodledood/manifest-dev-pi) must be bumped; and the package version example in
      .claude/skills/sync-tools/references/pi-cli.md must equal the new package.json version. PASS only if all
      hold. FAIL naming any unbumped or mismatched version.
  ```
- [AC-5.3] READMEs synced for the new `--log` capability and the check-pr change: root `README.md`, `claude-plugins/README.md`, and the affected plugin READMEs reflect current behavior per the CLAUDE.md README sync checklist.
  ```yaml
  verify:
    prompt: |
      Read README.md (root), claude-plugins/README.md, claude-plugins/manifest-dev-tools/README.md, and
      claude-plugins/manifest-dev/README.md. PASS only if babysit-pr's new `--log` capability is reflected
      where babysit-pr is described and nothing still advertises check-pr's removed retrigger/cap counting.
      Keep it high-level per the README guidelines. FAIL if a README contradicts the shipped behavior.
  ```
