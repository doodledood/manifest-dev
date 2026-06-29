# Definition: Default-on docs and logs with opt-out flags

## 1. Intent & Context
- **Goal:** Reverse the figure-out and babysit logging defaults so durable docs/log behavior is on by default, with explicit opt-out flags, while preserving progressive disclosure and removing old positive-flag compatibility.
- **Mental Model:** `figure-out` is still a thin entry prompt. Default-on does not mean inlining mode mechanics: the trigger flips from positive flag presence to absence of a negative flag. `WITH_DOCS.md` and `LOG.md` remain the owners of docs/log mechanics. `figure-out-team` inherits defaults through `figure-out --team`, but team mode keeps docs read-only and logs local-only. `babysit-pr` gets the same opt-out shape for its PR journal while `/do` stays consumer-only.

## 2. Approach
- **Architecture:** Edit source plugin prompts under `claude-plugins/`; update reference files that name old flags; update user docs and plugin/package versions; run `sync-tools` so `dist/` mirrors source. Do not hand-edit generated dist except through sync output.
- **Execution Order:**
  - D1 source prompt/reference edits → D2 docs/version updates → D3 sync generated distributions → D4 verification/commit
  - Rationale: sync should run after source and metadata are final; verification should inspect both source and generated copies.
- **Risk Areas:**
  - [R-1] Default-on docs could accidentally inline docs mechanics into `SKILL.md` | Detect: prompt-quality/progressive-disclosure static review confirms only thin trigger lines live in the entry prompt.
  - [R-2] Team mode could inherit write-capable docs behavior | Detect: `team.md` explicitly keeps docs read-only unless `--no-docs` and forbids CONTEXT/ADR writes from Slack.
  - [R-3] Old positive flags could remain documented as supported | Detect: source README/skill grep for `--with-docs` and `--log [path]` is clean outside historical manifests/ADRs.
  - [R-4] Generated distributions could drift | Detect: sync output plus source-vs-dist grep/static checks.
- **Trade-offs:**
  - [T-1] Backward compatibility vs clean flag surface → Prefer clean surface because the user explicitly said no backward compatibility.
  - [T-2] Remove all `--log` forms vs keep path override → Keep `--log <path>` because explicit log path selection is still live functionality, not compatibility.
  - [T-3] Strict invalid-flag rejection vs simply dropping old flags from support → Prefer dropping from supported syntax without extra rejection prose; these are skill prompts, and rejection logic adds prompt surface for a path the user does not want to support.

## 3. Global Invariants
- [INV-G1] Progressive disclosure is preserved for touched mode/reference behavior.
  ```yaml
  verify:
    prompt: "Read touched SKILL.md files and companion references: figure-out/SKILL.md plus references/WITH_DOCS.md, LOG.md, autonomous.md, team.md; figure-out-team/SKILL.md; walk-pr/SKILL.md plus references/CANVAS_MODE.md. PASS only if entry skill files own the load conditions using parsed top-level options (not raw topic text), and references assume they were intentionally loaded, while detailed mechanics such as CONTEXT bootstrap, glossary/ADR capture, path resolution, append cadence, Slack/team behavior, autonomous backstop, and canvas behavior remain in the reference files rather than being inlined into entry prompts. FAIL with quoted trigger boilerplate inside references or missing/ambiguous entry-skill triggers."
    phase: 1
  ```
- [INV-G2] Old positive flag compatibility is removed from current source-facing surfaces.
  ```yaml
  verify:
    prompt: "Inspect current source docs/prompts under claude-plugins/manifest-dev and claude-plugins/manifest-dev-tools, excluding archived manifests and ADR history. PASS only if --with-docs and the old optional form --log [path] are no longer advertised or described as supported current flags. --log <path> may remain as an explicit path override. FAIL with file:line evidence for any current supported old positive flag wording."
    phase: 1
  ```
- [INV-G3] Prompt edits pass change-intent and prompt-quality review.
  ```yaml
  verify:
    prompt: "Activate the manifest-dev:review-code skill with dimension=change-intent and review the full diff against the stated intent: invert docs/log defaults with --no-docs/--no-log opt-outs, preserve progressive disclosure, remove old positive-flag compatibility, make babysit-pr journaling default-on, keep /do consumer-only, sync docs/dist/versions. Then activate the manifest-dev-tools:review-prompt skill on the touched skill/reference prompt files. PASS only if review-code reports no LOW-or-higher findings and review-prompt reports no MEDIUM-or-higher findings. FAIL with findings and evidence."
    phase: 2
  ```

## 4. Process Guidance
- [PG-1] Apply prompt-engineering calibration: replace existing flag lines rather than adding duplicate walls; every new line must close the default-inversion gap.
- [PG-2] Edit source plugin files first; generated distributions must come from sync output.
- [PG-3] Use conventional commit at the end and do not push.
- [PG-4] Treat `CONTEXT.md` glossary capture from this figure-out session as part of the docs side effect; keep it only if the entry remains high-value project language.

## 5. Known Assumptions
- [ASM-1] (auto) Version bumps should reflect breaking flag/default changes. Default: bump `manifest-dev` major, bump `manifest-dev-tools` major if its plugin semantics are considered breaking, and bump the Pi package for changed distributed assets. Impact if wrong: version can be adjusted before commit.
- [ASM-2] (auto) `--log <path>` syntax is sufficient for explicit path override; bare `--log` does not need current support text. Impact if wrong: users who pass bare `--log` get no extra behavior, matching default logging.
- [ASM-3] (auto) Static verification is adequate because this is prompt/skill metadata, not executable code. Impact if wrong: add targeted script/grep checks.

## 6. Deliverables

### Deliverable 1: Figure-out default-on docs/log opt-outs

**Acceptance Criteria:**
- [AC-1.1] `figure-out/SKILL.md` advertises and implements default-on docs/log via opt-outs.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if argument-hint advertises --no-docs, --no-log, and --log <path>; does not advertise --with-docs or --log [path]; the body says to interpret only top-level skill options as flags so quoted/code/topic mentions of --no-docs, --no-log, or --log <path> remain topic text; and the body loads references/WITH_DOCS.md unless parsed options include --no-docs and references/LOG.md unless parsed options include --no-log. PASS only if --log <path> is described only as explicit path override. FAIL with actual lines quoted."
    phase: 1
  ```
- [AC-1.2] Figure-out references contain mechanics, not load-trigger policy.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/WITH_DOCS.md, LOG.md, ADR_FORMAT.md, autonomous.md, and team.md. PASS only if the references do not contain trigger boilerplate such as 'Loaded when', 'Loaded by default', or instructions about whether args contain their loading flags; WITH_DOCS.md still describes bootstrap/glossary/ADR mechanics, LOG.md still describes default path and --log <path> path override mechanics, ADR_FORMAT.md refers to docs mode rather than figure-out --with-docs and contains no --no-docs policy, autonomous.md still describes autonomous behavior, and team.md still describes team behavior. FAIL with missing mechanics or trigger boilerplate quoted."
    phase: 1
  ```

### Deliverable 2: Figure-out-team inherits defaults safely

**Acceptance Criteria:**
- [AC-2.1] `figure-out-team` forwards the new opt-out/path flags and no old positive docs flag.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md. PASS only if argument-hint advertises --no-docs, --no-log, and --log <path>, does not advertise --with-docs or --log [path], and the body forwards topic and flags including --no-docs, --no-log, and --log <path> to figure-out --team. FAIL with actual lines quoted."
    phase: 1
  ```
- [AC-2.2] Team mode preserves read-only docs and local-only logging without owning load triggers.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/team.md and figure-out/SKILL.md. PASS only if figure-out/SKILL.md owns the --team/--no-docs/--no-log load conditions, while team.md contains no load-trigger boilerplate and still says docs mode is read-only in team mode, with no CONTEXT captures/init and no ADR offers/writes from Slack; and logging is local-only, with explicit log path only choosing the local path and never posted to Slack. FAIL with missing or conflicting text quoted."
    phase: 1
  ```

### Deliverable 3: Babysit-pr journal defaults on

**Acceptance Criteria:**
- [AC-3.1] `babysit-pr` journaling is default-on with opt-out and path override.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/babysit-pr/SKILL.md. PASS only if argument-hint advertises --no-log and --log <path> but not --log [path], Inputs no longer calls logging optional, Logging says the PR journal is created/used by default unless --no-log, and --log <path> overrides the default PR-keyed path. PASS only if Execution passes the resolved journal path to /do by default unless --no-log, while /do remains the sole consumer. FAIL with actual conflicting lines quoted."
    phase: 1
  ```
- [AC-3.2] `/do` remains consumer-only.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md. PASS only if /do still has no user-facing --log or --no-log argument surface and only reacts when a caller supplies a journal/log path. FAIL with any added /do user flag or removed consumer behavior quoted."
    phase: 1
  ```

### Deliverable 4: Docs, versions, and generated distributions are synced

**Acceptance Criteria:**
- [AC-4.1] User-facing READMEs describe the new opt-out defaults.
  ```yaml
  verify:
    prompt: "Inspect README.md, claude-plugins/README.md, claude-plugins/manifest-dev/README.md, and claude-plugins/manifest-dev-tools/README.md. PASS only if current figure-out/team/babysit-pr descriptions match default docs/log or default journal behavior with --no-docs/--no-log opt-outs and --log <path> path override where relevant, and do not advertise --with-docs or --log [path]. FAIL with stale lines quoted."
    phase: 1
  ```
- [AC-4.2] Plugin/package versions are bumped consistently with changed source and Pi-distributed assets.
  ```yaml
  verify:
    prompt: "Inspect claude-plugins/manifest-dev/.claude-plugin/plugin.json, claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json, package.json, and .claude/skills/sync-tools/references/pi-cli.md if it contains the Pi package version example. PASS only if changed plugin/package surfaces have appropriate version bumps and the Pi docs example matches package.json. FAIL with stale versions or mismatches quoted."
    phase: 1
  ```
- [AC-4.3] Generated distribution copies match the source semantics.
  ```yaml
  verify:
    prompt: "Inspect dist/opencode, dist/codex, and dist/pi copies for figure-out, figure-out-team, babysit-pr, their touched references, and README/package metadata. PASS only if generated copies mirror the new --no-docs/--no-log/default-on semantics from source and no generated current docs advertise --with-docs or --log [path]. FAIL with file:line evidence for drift."
    phase: 2
  ```
- [AC-4.4] Repository verification commands pass.
  ```yaml
  verify:
    prompt: "Run the repository's available verification for prompt/markdown changes: at minimum `ruff check claude-plugins/`, `black --check claude-plugins/`, and `mypy` when configured/available, plus targeted grep checks for stale flag docs in current source/dist. PASS only if commands/checks pass or non-applicable commands are explicitly justified. FAIL with command output."
    phase: 2
  ```
