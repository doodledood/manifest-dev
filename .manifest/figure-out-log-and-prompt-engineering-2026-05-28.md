# Definition: Add figure-out investigation logging and prompt-engineering calibration

## 1. Intent & Context

- **Goal:** Add an optional `--log [path]` mode to `/figure-out` and `/figure-out-team` that keeps an append-only, evidence-based local narrative investigation log for long-running sessions. Also update `/figure-out` so prompt-shaped investigations invoke the prompt-engineering skill when available, giving prompt/skill/agent reasoning the same calibration principles `/define` uses for verifier prompts.
- **Mental Model:** `/figure-out` is the live thinking partner. A session transcript is raw conversation; a handoff is a curated rewrite for a next session; ADRs are durable decision records; a Manifest is an execution contract. The new log is none of those. It is a running investigation journal: append-only, chronological, portable across sessions/tools by path, and focused on what was learned, why the read shifted, what evidence supports it, and what remains open.

## 2. Approach

- **Architecture:** Keep the base `figure-out/SKILL.md` and `figure-out-team/SKILL.md` small. Add only trigger lines there: update argument hints and load each skill's local `references/LOG.md` when `--log` appears. For `figure-out`, also invoke prompt-engineering when the topic becomes prompt-shaped. Put logging mechanics in copied `LOG.md` reference files under both skills.
- **Execution Order:**
  - D1 (`figure-out/references/LOG.md`) -> D2 (`figure-out/SKILL.md` trigger updates) -> D3 (`figure-out-team/references/LOG.md` + `figure-out-team/SKILL.md` trigger updates) -> D4 (docs/version/sync)
  - Rationale: the base skill should point at a concrete reference file once edited. Documentation/version/distribution updates happen after source behavior is settled.
- **Risk Areas:**
  - [R-1] Logging could bloat normal figure-out context if mechanics are inlined in `SKILL.md` | Detect: `SKILL.md` only contains the short trigger and all detailed log mechanics live in `references/LOG.md`.
  - [R-2] `--log` could dirty the repo by default | Detect: default path is scratch (`/tmp` when writable, otherwise temp dir), and repo-local logs require an explicit path argument.
  - [R-3] The log could degrade into transcript duplication or conclusion-only summaries | Detect: `LOG.md` requires narrative entries with evidence refs, reasoning shifts, surprises, open threads, and next crux; it explicitly says not to copy the transcript.
  - [R-4] Prompt-engineering activation could hijack normal investigations | Detect: the trigger is bounded to prompt-shaped topics and says figure-out owns the investigation; prompt-engineering supplies calibration principles only.
  - [R-5] `figure-out-team` logging could leak into Slack | Detect: team LOG.md and SKILL.md state logs are local artifacts only and are never posted to Slack.
  - [R-6] Distribution mirrors may drift from plugin source | Detect: generated `dist/` copies are refreshed or verified in sync with both figure-out skill sources.
- **Trade-offs:**
  - [T-1] Inline log instructions vs reference file -> Prefer reference file. The mechanics are stateful and mode-specific; default figure-out should stay minimal.
  - [T-2] `--log` only vs `--log [path]` -> Prefer optional path. No-arg mode is convenient; explicit path gives durable cross-session continuation.
  - [T-3] Scratch default vs project-local default -> Prefer scratch. Logging is user-requested, but repo mutation should require an explicit project-local path.
  - [T-4] Broad prompt-engineering trigger vs narrow prompt-text-only trigger -> Prefer broad but bounded. Prompt-shaped includes prompts, system prompts, skills, agents, reviewer prompts, metaprompting, and prompt-driven failures; ordinary usage of the word "prompt" should not trigger it.
  - [T-5] Shared LOG.md via cross-reference vs copied local reference for `figure-out-team` -> Prefer copy. User asked for the same flag by copying; local references keep each skill self-contained in distributions.

## 3. Global Invariants

- [INV-G1] `figure-out/SKILL.md` remains compact; logging mechanics are progressively disclosed through `references/LOG.md`
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md and claude-plugins/manifest-dev/skills/figure-out/references/LOG.md. PASS only if SKILL.md contains a short --log trigger that loads references/LOG.md, while detailed mechanics such as path resolution, append timing, entry shape, and resume semantics live in LOG.md rather than SKILL.md. FAIL with the inline mechanics or missing reference details quoted."
    agent: prompt-reviewer
  ```

- [INV-G2] `--log` never creates a repo-local file by default
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/LOG.md. PASS only if the no-path form of --log creates the log under a writable scratch/temp location (prefer /tmp when writable, otherwise host temp dir), and repo-local paths are used only when the user passes an explicit path. FAIL with the conflicting text quoted."
  ```

- [INV-G3] Prompt-engineering calibration is bounded to prompt-shaped investigations and does not replace figure-out's interview ownership
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md. PASS only if it instructs the agent to invoke prompt-engineering when the topic becomes prompt-shaped (prompts, system prompts, skills, agents, reviewer prompts, metaprompting, or prompt-driven failures) if available, and also says not to start a separate prompt-engineering interview because figure-out owns the investigation. FAIL with missing or over-broad/under-broad trigger language quoted."
    agent: prompt-reviewer
  ```

- [INV-G4] Prompt quality review finds no MEDIUM+ issues in the prompt/skill changes
  ```yaml
  verify:
    prompt: "Invoke the prompt-reviewer subagent on the changes to claude-plugins/manifest-dev/skills/figure-out/SKILL.md and claude-plugins/manifest-dev/skills/figure-out/references/LOG.md. Assess against prompt-engineering principles: every line earns its place, mode-specific mechanics are progressively disclosed, trigger language is bounded, no contradictory rules, no weak hedging, and no unnecessary HOW where the model already knows the behavior. PASS only if there are no MEDIUM+ findings. FAIL with findings quoted otherwise."
    agent: prompt-reviewer
  ```

- [INV-G5] Intent-behavior review finds no LOW+ divergence from the agreed design
  ```yaml
  verify:
    prompt: "Invoke the change-intent-reviewer subagent on the changes to figure-out logging and prompt-engineering activation. Stated intent: add --log [path] append-only evidence-based narrative logging with scratch default and explicit-path resume, and add bounded prompt-engineering invocation for prompt-shaped figure-out topics without hijacking normal investigations. PASS only if the reviewer reports no LOW+ findings. FAIL with findings quoted otherwise."
    agent: change-intent-reviewer
  ```

- [INV-G6] Plugin admin updates are complete for new figure-out and figure-out-team flags
  ```yaml
  verify:
    prompt: "Inspect plugin metadata and docs after implementation. PASS only if claude-plugins/manifest-dev/.claude-plugin/plugin.json has an appropriate patch version bump, user-facing docs that describe /figure-out or /figure-out-team flags mention --log where those flags are listed, and generated distribution copies under dist/ include the updated figure-out and figure-out-team source files. FAIL listing missing admin updates."
  ```

- [INV-G7] `figure-out-team --log` writes only to a local file, never to Slack
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md and claude-plugins/manifest-dev/skills/figure-out-team/references/LOG.md. PASS only if both make clear that --log is a local append-only file artifact and the log must not be posted to Slack or sent as a Slack message. FAIL with missing or conflicting text quoted."
  ```

## 4. Process Guidance

- [PG-1] High-signal changes only. Do not refactor adjacent skills, rename unrelated references, or rewrite working figure-out prose beyond the exact flag/trigger additions.
- [PG-2] Apply prompt-engineering calibration while editing: every new line must close a real gap, and mode-specific mechanics belong in the reference file rather than the always-loaded skill body.
- [PG-3] Keep log prose low-arousal and factual. The journal should capture evidence and reasoning shifts, not motivational narration or transcript theater.
- [PG-4] Preserve existing `--with-docs` and `--autonomous` behavior. The new `--log` mode composes with them; it does not change their semantics.
- [PG-5] For `figure-out-team`, Slack remains the deliberation surface only. The log is a local continuity artifact and must not be mirrored into Slack.

## 5. Known Assumptions

- [ASM-1] (auto) This is a prompting/skill task, not a general coding task. Default: use PROMPTING gates only; do not compose CODING gates because the task updates markdown skill instructions, not executable code. Impact if wrong: low; implementation still has file-level verification and prompt/intent review.
- [ASM-2] (auto) Plugin version bump is patch. Default: existing skill gains an optional flag and a companion reference file; no breaking behavior. Impact if wrong: low; semver can be amended before release.
- [ASM-3] (auto) `--log` can compose with `--with-docs` and `--autonomous` for `/figure-out`, and with Slack polling for `/figure-out-team`. Default: logging records what the active mode learns; it does not alter docs capture, autonomous self-answering, Slack posting, or Slack polling. Impact if wrong: medium; LOG.md would need explicit incompatibility rules.
- [ASM-4] (auto) The output log format is Markdown. Default: human-readable, append-friendly, path-portable. Impact if wrong: low; alternate formats can be introduced later with another flag if needed.

## 6. Deliverables

### Deliverable 1: Add `--log [path]` reference file

Create `claude-plugins/manifest-dev/skills/figure-out/references/LOG.md` describing the append-only investigation log mode.

**Acceptance Criteria:**

- [AC-1.1] LOG.md defines purpose and artifact boundaries
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/references/LOG.md. PASS only if it defines the log as an append-only narrative investigation journal and distinguishes it from raw transcripts, handoffs, ADRs, and Manifests. FAIL with missing distinctions listed."
  ```

- [AC-1.2] LOG.md specifies path behavior for `--log` and `--log <path>`
  ```yaml
  verify:
    prompt: "Read LOG.md. PASS only if it specifies: (1) --log with no path creates a timestamped markdown file under scratch/temp, preferring /tmp when writable; (2) --log <path> appends to the explicit path, creating parent directories only when safe/needed; (3) the agent prints or surfaces the active log path immediately so future sessions/tools can resume it. FAIL listing missing behavior."
  ```

- [AC-1.3] LOG.md defines append timing and entry content
  ```yaml
  verify:
    prompt: "Read LOG.md. PASS only if it requires appending after each meaningful turn or evidence-gathering pass before the next question, and entry content includes evidence refs, findings/surprises, reasoning shifts, open threads, and next crux when applicable. FAIL with missing required fields or cadence issues quoted."
  ```

- [AC-1.4] LOG.md prevents transcript duplication and unsupported claims
  ```yaml
  verify:
    prompt: "Read LOG.md. PASS only if it explicitly says not to copy the transcript and requires evidence-based entries with clear provenance for factual claims. FAIL with the relevant missing/contradictory text quoted."
  ```

### Deliverable 2: Update figure-out SKILL.md triggers

Update `claude-plugins/manifest-dev/skills/figure-out/SKILL.md` to expose the new flag and bounded prompt-engineering activation.

**Acceptance Criteria:**

- [AC-2.1] Argument hint includes `--log [path]`
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out/SKILL.md frontmatter. PASS only if argument-hint includes `[--log [path]]` alongside the existing topic and --with-docs hint. FAIL with the actual argument-hint quoted."
  ```

- [AC-2.2] SKILL.md loads LOG.md when args contain `--log`
  ```yaml
  verify:
    prompt: "Read figure-out/SKILL.md. PASS only if there is a short trigger line saying that when args contain `--log`, the agent loads `references/LOG.md` and keeps an append-only investigation log. FAIL with missing or incorrect trigger text quoted."
  ```

- [AC-2.3] SKILL.md invokes prompt-engineering for prompt-shaped topics only
  ```yaml
  verify:
    prompt: "Read figure-out/SKILL.md. PASS only if it instructs the agent to invoke the prompt-engineering skill when the investigation discusses or inspects prompts, system prompts, skills, agents, reviewer prompts, metaprompting, or prompt-driven failures, while making clear ordinary non-prompt investigations should not load it. FAIL with missing or over-broad trigger language quoted."
  ```

- [AC-2.4] Existing `--with-docs` and `--autonomous` trigger lines remain present
  ```yaml
  verify:
    prompt: "Read figure-out/SKILL.md. PASS only if the existing trigger lines for `--with-docs` loading `references/WITH_DOCS.md` and `--autonomous` loading `references/autonomous.md` remain present and semantically unchanged except for surrounding formatting. FAIL with the changed or missing lines quoted."
  ```

### Deliverable 3: Add `--log [path]` to figure-out-team

Copy the logging mode to `figure-out-team` with a local-only log contract. The team Slack thread remains the communication surface; the log is never posted to Slack.

**Acceptance Criteria:**

- [AC-3.1] figure-out-team has a copied LOG.md reference
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/references/LOG.md. PASS only if it defines --log as an append-only narrative investigation journal with the same path behavior as figure-out LOG.md, and explicitly states the log is local-only and must not be posted to Slack. FAIL listing missing behavior."
  ```

- [AC-3.2] figure-out-team argument hint includes `--log [path]`
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/skills/figure-out-team/SKILL.md frontmatter. PASS only if argument-hint includes `[--log [path]]` alongside the existing topic and --with-docs hint. FAIL with the actual argument-hint quoted."
  ```

- [AC-3.3] figure-out-team SKILL.md loads LOG.md locally and forbids Slack posting of the log
  ```yaml
  verify:
    prompt: "Read figure-out-team/SKILL.md. PASS only if there is a short trigger line saying that when args contain `--log`, the agent loads `references/LOG.md` and keeps a local append-only investigation log, and the line or nearby text states the log is not posted to Slack. FAIL with missing or incorrect trigger text quoted."
  ```

### Deliverable 4: Update plugin docs, version, and generated distributions

Make the new flag visible to users and keep published/generated artifacts aligned.

**Acceptance Criteria:**

- [AC-4.1] User-facing figure-out and figure-out-team docs mention `--log`
  ```yaml
  verify:
    prompt: "Inspect README.md and claude-plugins/manifest-dev/README.md. PASS only if the /figure-out and /figure-out-team descriptions mention `--log [path]` or equivalent local narrative logging behavior where flags are described. FAIL listing missing docs."
  ```

- [AC-4.2] Plugin version is bumped appropriately
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev/.claude-plugin/plugin.json and compare its version to main. PASS only if the version is incremented by at least a patch version for the new optional figure-out behavior. FAIL with current and main versions quoted otherwise."
  ```

- [AC-4.3] Distribution copies are synced
  ```yaml
  verify:
    prompt: "Compare the figure-out and figure-out-team skill files under claude-plugins/manifest-dev/skills/ with generated copies under dist/opencode/skills/ and dist/codex/skills/ if those distribution directories exist. PASS only if SKILL.md and LOG.md changes are represented in each generated distribution copy. FAIL listing stale or missing files."
  ```
