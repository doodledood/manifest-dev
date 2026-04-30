# Definition: Shared Understanding Canvas — Live Visual Artifact for /define

## 1. Intent & Context

- **Goal:** Reframe /define around *building shared understanding* between user and agent, encoded formally as a Manifest (and optionally visualized as a live, browser-rendered Shared Understanding Canvas). Add an opt-in `--canvas` flag that produces a self-contained HTML file alongside the manifest, updates live as the interview unfolds, and auto-opens in the user's default browser on desktop environments.
- **Mental Model:** /define has two outputs serving two readers: the **manifest** (formal, dense, machine-readable — for /do) and the **canvas** (visual, layered, human-readable — for the user during the interview). The agent processes formal structure natively; humans don't. The canvas absorbs that cognitive asymmetry so feedback during /define becomes "look and react" instead of "read 800 lines and audit." The canvas exists only during the initial interview phase — it freezes when the user approves and is not maintained on `--amend`, autonomous interviews, /auto invocations, or non-desktop environments.
- **Mode:** thorough
- **Interview:** thorough
- **Medium:** local

## 2. Approach

- **Architecture:**
  - SKILL.md gets two changes: (a) Goal and section framing rewritten universally to elevate "build shared understanding, encoded formally as a Manifest" — the canvas is then introduced as the optional visual layer of that universal goal; (b) `--canvas` flag added to the Input parsing block alongside `--interview`/`--medium`/`--amend`, with a small dispatch section that gates loading `references/CANVAS_MODE.md` when the flag is active and the environment supports it.
  - All canvas-mode operational detail lives in **`references/CANVAS_MODE.md`** (progressive disclosure — keeps SKILL.md from bloating). That file owns: canvas principles, illustrative content menu, format requirements (single self-contained `.html` with Tailwind + mermaid via CDN, embedded JS for auto-reload), update cadence, auto-open mechanism, failure handling, file naming.
  - File output: `/tmp/canvas-{ts}.html` — same `{ts}` as the manifest and discovery log so the three are linkable.
  - Canvas is silently a no-op when ANY of the following: `--amend` is also passed, `--interview autonomous` (which transitively covers `/auto` invocations — `/auto` always passes `--interview autonomous` to /define), `--medium slack` (Slack user has no access to the host's browser), OR no graphical-browser launcher (`xdg-open` / `open` / `start`) is available. A single one-line warning is printed in the launcher-missing case; the others skip silently because the user already opted into a context where the canvas can't reach them.
  - Summary for Approval: when canvas active, the existing chat summary still runs and a one-line `Canvas: file:///tmp/canvas-{ts}.html` link is appended. The chat surface remains the approval channel; the canvas is the deeper-look surface.

- **Execution Order:**
  - D2 (CANVAS_MODE.md) → D1 (SKILL.md changes that reference D2) → D3 (plugin metadata + READMEs)
  - Rationale: the reference file is the substantive artifact; SKILL.md changes are integration; metadata/READMEs are last-mile.

- **Risk Areas:**
  - [R-1] Flag-absent regression — any change to /define risks subtly altering today's behavior when `--canvas` is not set | Detect: AC-1.2 (byte-equivalence of flag-absent flow encoded as criterion); change-intent-reviewer flags drift
  - [R-2] Content menu calcifies into a checklist — agent treats illustrative items as required and produces templated artifacts | Detect: prompt-reviewer flags prescriptive framing in CANVAS_MODE.md; AC-2.2 enforces "consider including" framing
  - [R-3] SKILL.md bloat — canvas detail leaking into SKILL.md instead of CANVAS_MODE.md | Detect: AC-1.4 caps SKILL.md additions; PG-2 enforces progressive disclosure
  - [R-4] Live-update token cost compounds in long interviews — every meaningful event triggers a full HTML rewrite | Detect: PG-4 scopes "meaningful event" tightly; ASM-5 logs the cost trade-off as accepted
  - [R-5] Browser auto-reload jank — page reloads lose scroll position, expand state, mid-read | Detect: CANVAS_MODE.md states the principle ("preserve scroll/expand state when feasible"); agent picks mechanism
  - [R-6] Desktop-detection false negatives — env has a graphical browser but launchers aren't on PATH; canvas is wrongly suppressed | Detect: ASM-1 logs the heuristic; warn message tells user what to check
  - [R-7] Composition surprise with existing flags — `--canvas --amend`, `--canvas` inside `/auto` etc. produce unexpected behavior | Detect: AC-1.2 enumerates suppression conditions explicitly
  - [R-8] Plain HTML / bullet-list output instead of compelling visuals — agent generates a tidy outline that defeats the comprehension principle | Detect: prompt-reviewer on CANVAS_MODE.md flags if its illustrative-content guidance leans toward header-and-bullet patterns over diagrams/layered-reveal patterns; CANVAS_MODE.md must include at least one illustrative visual fragment (e.g., mermaid flowchart, tabbed/collapsible component) framed as "what visual richness looks like, not a required structure"

- **Trade-offs:**
  - [T-1] Token cost vs feedback quality → Prefer feedback quality because the canvas's entire purpose is reducing the cognitive cost of reviewing /define output; token cost is the price of the value being delivered, and the flag is opt-in so users who don't want it don't pay
  - [T-2] Agent freedom vs predictable output → Prefer agent freedom (principles + illustrative menu, not template) because the user's explicit constraint was "no fixed structure" and templated output would defeat the comprehension-over-completeness principle
  - [T-3] Live updates vs end-only generation → Prefer live updates because user feedback during the interview is the value; end-only would replicate the chat summary and add nothing
  - [T-4] HTML-only vs markdown-also → Prefer HTML-only because "interactive site" + Tailwind + auto-reload requires real HTML; markdown adds maintenance burden without the layered-reveal capability
  - [T-5] Hard-error vs warn-and-skip on non-desktop → Prefer warn-and-skip because /define must remain usable in any env; failing the workflow because of an optional visual layer breaks the principle that the manifest is the load-bearing output

## 3. Global Invariants (The Constitution)

- [INV-G1] All changed files pass change-intent-reviewer with no LOW or above issues
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    prompt: "Review the diff for behavioral divergence from stated intent: adding an opt-in --canvas flag to /define that produces a live, browser-rendered Shared Understanding Canvas (HTML file with Tailwind + mermaid + auto-reload), updating live during the interview, freezing on approval, no-op on --amend / --interview autonomous / /auto / non-desktop env. Flag-absent path must be byte-equivalent to today's behavior."
  ```

- [INV-G2] All changed prompt files pass prompt-reviewer with no MEDIUM or above issues
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    prompt: "Review changed prompt files for quality: claude-plugins/manifest-dev/skills/define/SKILL.md and claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md. Apply standard prompt-reviewer gates including clarity, no anti-patterns (no prescriptive HOW, no rigid checklists in CANVAS_MODE.md content menu), structure, complexity fit, edge case coverage (--amend, autonomous, /auto, non-desktop, generation failure), description-as-trigger if SKILL.md frontmatter changed."
  ```

- [INV-G3] When `--canvas` is NOT passed, /define behavior is functionally equivalent to the pre-change behavior — no new files written, no browser open attempts, no warnings emitted, summary-for-approval format unchanged
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md. Verify that the --canvas flag handling is gated such that the absent-flag path is unchanged from before the change. FAIL if: (1) any unconditional canvas-related instructions exist outside the --canvas-gated block, (2) summary-for-approval section adds canvas references unconditionally rather than 'when canvas is active', (3) any unconditional reference to /tmp/canvas-*.html, (4) CANVAS_MODE.md is loaded unconditionally instead of only when the flag is active and env supports it. PASS if all canvas-related additions are gated on flag + env."
  ```

- [INV-G4] `--canvas` is silently a no-op (skipped without artifact generation, no browser open) when ANY of these hold: `--amend` is also passed, `--interview autonomous` (which already covers /auto invocations — /auto always passes `--interview autonomous` to /define), or `--medium slack` (Slack user has no access to host's browser). A single one-line warning is printed (and then skipped) when env lacks a graphical-browser launcher. SKILL.md documents all four suppression conditions explicitly.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md for explicit handling of --canvas suppression conditions. FAIL if any of these four conditions are NOT explicitly enumerated as suppression triggers: (1) --amend present, (2) --interview autonomous (with a note that /auto invocations are already covered because /auto passes --interview autonomous), (3) --medium slack, (4) non-desktop env (no xdg-open/open/start launcher). For (1)-(3), suppression must be silent (no warning); for (4) a single one-line warning must be specified. PASS if all four are explicitly enumerated with the correct suppression behavior."
  ```

- [INV-G5] Plugin version in `claude-plugins/manifest-dev/.claude-plugin/plugin.json` bumped per CLAUDE.md rules (minor for new feature — middle segment incremented, patch reset to 0)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Run: git diff origin/main -- claude-plugins/manifest-dev/.claude-plugin/plugin.json. Verify that the version field changed AND the change is a minor bump (middle segment incremented by 1, patch segment reset to 0, major unchanged). For example: 1.4.7 → 1.5.0 PASSES; 1.4.7 → 1.4.8 (patch bump only) FAILS for this 'minor for new feature' rule; 2.0.0 (major bump) FAILS as too large. FAIL if version unchanged, patch-only bump, or major bump. PASS only if minor segment incremented correctly."
  ```

- [INV-G6] README sync per CLAUDE.md checklist completed: root `README.md`, `claude-plugins/README.md`, and `claude-plugins/manifest-dev/README.md` reflect the new `--canvas` capability
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check that README.md (repo root), claude-plugins/README.md, and claude-plugins/manifest-dev/README.md have been updated to mention the --canvas flag for /define and the Shared Understanding Canvas concept. FAIL if any of the three READMEs is missing reference to the new capability. PASS if all three reflect it appropriately for their level of detail (root: brief mention; plugin README: high-level component description; define-specific section if present: usage/behavior summary)."
  ```

- [INV-G7] CANVAS_MODE.md lives at `claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md` and is substantive (covers principles, content menu, format, cadence, auto-open, failure handling, file naming). Line-count bound on SKILL.md additions handled by AC-2.7 (bash); CANVAS_MODE.md size bound handled by AC-1.9. This invariant focuses purely on the substantive-content check.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check that the file claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md exists and its content covers each of: canvas principles, illustrative content menu, format requirements (single self-contained HTML, Tailwind, mermaid, embedded auto-reload), update cadence, auto-open mechanism, failure handling, and file naming. FAIL if the file is missing or any of the seven topics is absent or only mentioned in passing without substantive content. PASS if all seven topics are substantively covered."
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] **Scope guard.** Hold the line on what's specified: `--canvas` flag + universal Goal reframe + single-HTML generation with Tailwind/mermaid/auto-reload + auto-open + desktop detection + augmented summary. Do NOT add: theming options, export-to-PDF, shareable URLs, deeper interactivity beyond layered reveal, persistent sessions across `/define` invocations, multi-file site output, retroactive canvas generation for existing manifests, runtime CDN-reachability checks, in-tool `/tmp` cleanup. Those are explicit follow-ups, not part of this change.
- [PG-2] **Progressive disclosure.** Canvas operational detail belongs in `references/CANVAS_MODE.md`, not in SKILL.md. SKILL.md gets only: Goal reframe, flag parsing, dispatch ("when --canvas active and env supports, load `references/CANVAS_MODE.md` in full"), Summary-for-Approval addition, optional Intent-section schema field for traceability. Operational specifics (HTML structure, content menu, auto-reload mechanism, auto-open command, failure handling) live in CANVAS_MODE.md. The dispatch is a single-load contract — the whole file, no section-targeted dispatch.
- [PG-3] **Content menu is illustrative, not prescriptive.** In CANVAS_MODE.md, frame the content-types list as "Consider including any of these when they serve the task — none are required" rather than "Include the following sections." If the framing reads as a checklist, rewrite it.
- [PG-4] **"Meaningful event" defined.** Live updates fire after: each interview cluster's checkpoint synthesis, each coverage-goal resolution, each AC/INV/PG/ASM addition or modification, each Approach-section update, each scope-guard or trade-off lock-in. Do NOT fire after every agent turn or every tool call — that's noise. The principle is "the user's mental picture should change in step with the manifest's substance," not "the canvas re-renders constantly."
- [PG-5] **Auto-reload mechanism is the agent's call** under the principle: page must auto-reload when the file changes, and SHOULD preserve scroll position and expand/collapse state when feasible. JS polling, fetch + DOM diff, meta-refresh — agent picks based on task-specific factors. The agent picks ONCE at canvas-generation time per /define session — the embedded mechanism doesn't change mid-interview. Different /define sessions may produce different mechanisms; that's acceptable.
- [PG-6] **Generation failure is non-blocking.** If the canvas file write fails, the browser-open command fails, or any canvas-related operation errors out, the agent prints a single warning and continues with the normal /define flow. The canvas is supplementary; never block the manifest workflow on a canvas failure.
- [PG-7] **Canvas absorbs the cognitive translation work.** When generating canvas content, the agent's job is to make formal manifest content grasp-able by a less-formally-literate reader. If the agent finds itself producing prose that mirrors the manifest line-by-line, it has failed the principle — the canvas should look and feel different from the manifest, not be a re-skinned copy.
- [PG-8] **Universal Goal reframe is genuine.** The SKILL.md Goal section reframe ("build shared understanding, encoded as a Manifest, optionally as a Canvas") must read as a coherent universal framing — not a chunk of canvas-mode bolted onto the existing wording. If a reader without canvas context reads the new Goal, it should still make sense and not feel like it's promoting a feature.
- [PG-9] **Suppression conditions are owned by SKILL.md dispatch, not CANVAS_MODE.md.** SKILL.md's Canvas Mode section evaluates the four suppression conditions (--amend, --interview autonomous, --medium slack, non-desktop env) and ONLY loads `references/CANVAS_MODE.md` when all pass. CANVAS_MODE.md does NOT restate the suppression conditions — it assumes it's loaded only when canvas is genuinely active. Single source of truth for suppression logic.
- [PG-10] **Manual smoke test before declaring complete.** After all automated checks pass, run `/define --canvas "trivial test task"` end-to-end on a desktop env once to confirm: canvas file is created, browser opens (or warning fires if non-desktop), at least one live update fires after a meaningful event, summary-for-approval includes the canvas link. Also run `/define "trivial test task"` (no `--canvas`) once to confirm flag-absent path is unchanged. This is the only practical way to catch integration issues that automated review can miss.

## 5. Known Assumptions

- [ASM-1] Desktop detection via `command -v xdg-open || command -v open || command -v start` is sufficient — these cover Linux/macOS/Windows-WSL respectively. | Default: this heuristic; first matching launcher used to open the file. | Impact if wrong: rare false negative (env has graphical browser but no standard launcher) → user sees the warning, can open the file manually using the printed path. False positive (launcher exists but no display, e.g., headless Linux with X tools installed) → command fails silently, agent continues; user sees no canvas open and the warning didn't fire — they'll notice the missing canvas and can re-run without `--canvas`. Acceptable.
- [ASM-2] Tailwind + mermaid via CDN is acceptable; users on offline desktops or in CDN-blocked corporate environments see degraded styling. | Default: CDN, no runtime reachability check. | Impact if wrong: offline / blocked degradation → page still readable as semantic HTML (Tailwind degrades gracefully); diagrams won't render. Mitigation deferred — fix only if reported. Out-of-scope (PG-1) explicitly because runtime CDN checks add complexity disproportionate to the affected user fraction.
- [ASM-3] A single `.html` file with embedded JS polling (or whatever auto-reload mechanism the agent picks) is sufficient — no local HTTP server is needed. | Default: file:// URL with embedded auto-reload logic. | Impact if wrong: some browsers restrict `fetch()` against `file://` — the agent's chosen mechanism may need to fall back to meta-refresh. Acceptable; agent has discretion.
- [ASM-4] `/tmp/canvas-{ts}.html` naming convention parallels existing `/tmp/manifest-{ts}.md` and `/tmp/define-discovery-{ts}.md`, sharing the same `{ts}` for linkability. | Default: this naming. | Impact if wrong: trivial to rename.
- [ASM-5] Token cost of live updates after every meaningful event is the price of the canvas's value, accepted by anyone opting into the flag. | Default: no token-budget cap; live updates fire as specified in PG-4. | Impact if wrong: extreme-length interviews become slow/expensive — fix by adding a per-interview update budget in a follow-up; not in scope here.
- [ASM-6] Canvas is fresh-/define-only — on `--amend`, the flag is silently ignored even if passed. The earlier canvas (if any) from the original /define stays untouched on disk; no attempt is made to extend or refresh it during amendment. | Default: amendment ignores `--canvas` entirely. | Impact if wrong: user expected amendments to reflect in the canvas → fix in a follow-up; out of scope here per user decision.
- [ASM-7] Live-update wall-clock latency (separate from token cost) — each meaningful event triggers a full HTML rewrite, which adds latency to the agent's interview turns. | Default: accepted as the price of value, mirroring T-1 / ASM-5 reasoning. The flag is opt-in; users who don't want the latency don't pay it. | Impact if wrong: extreme-length interviews feel sluggish → fix by adding async/background writes or debounce in a follow-up.
- [ASM-8] Multiple concurrent /define sessions on the same host — each session writes its own `/tmp/canvas-{ts}.html` (unique timestamp per session) and each auto-open command opens a new browser tab. | Default: no coordination needed; default browser handles multi-tab naturally. | Impact if wrong: rare race or browser quirk → user closes extra tabs manually; not a blocker.
- [ASM-9] Plugin-version verification baseline is `origin/main`. The branch for this change starts at `origin/main` with no prior version bumps, so the diff cleanly shows the bump. | Default: `origin/main` baseline in INV-G5 / AC-3.1. | Impact if wrong: a future use of the same baseline on a long-lived branch with prior version bumps could pass spuriously — fix in a follow-up by switching to merge-base; not a concern for this change.
- [ASM-10] `/tmp/canvas-*.html` cleanup is the operating system's responsibility (standard `/tmp` lifecycle: clear on reboot or via system-managed `tmpfiles.d`). No in-tool cleanup of stale canvas files. | Default: no cleanup logic. | Impact if wrong: long-running systems accumulate canvas files until reboot — trivial disk impact; not a blocker.
- [ASM-11] SSH-into-headless-host scenario (user runs `/define --canvas` over SSH on a desktop-launcher-equipped host but the user's actual display is remote) is accepted as user-must-know-what-they're-doing. Launcher heuristic may produce false positives here — canvas opens on the host's nonexistent display. | Default: no SSH detection (no `SSH_CONNECTION` check). | Impact if wrong: user sees no canvas open and re-runs without `--canvas`; not a blocker. Out-of-scope per PG-1.

## 6. Deliverables (The Work)

### Deliverable 1: Create `references/CANVAS_MODE.md`

The substantive specification of canvas behavior, isolated in a reference file so SKILL.md stays lean. Owns: principles, illustrative content menu, format requirements, update cadence, auto-open mechanism, failure handling, file naming.

**Acceptance Criteria:**

- [AC-1.1] File exists at `claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md` and contains a top-level intro framing the canvas as a comprehension instrument that absorbs the cognitive translation work between formal manifest content and human-readable visual understanding (without using literal phrases like "less literate user")
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md exists. Verify the intro section frames the canvas as serving comprehension/grasp by the human reader and acknowledges the asymmetry between the agent's native ability to process formal structure and the human's. FAIL if intro is missing, generic, or uses phrasing like 'less literate user' / 'illiterate user'. PASS if intro conveys the asymmetric-comprehension framing in respectful, professional language."
  ```

- [AC-1.2] Three principles encoded explicitly: (1) Comprehension over completeness, (2) Layered reveal, (3) Visual where flow exists, prose where it doesn't. Each principle has at least one sentence of explanation. Verification is NOT listed as a principle.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for three explicitly numbered or labeled principles: (1) comprehension over completeness, (2) layered reveal, (3) visual where flow exists, prose where it doesn't. Each must have explanatory text. FAIL if any principle is missing, if more or fewer than three principles are listed at the principle level, or if 'verification' / 'verification by recognition' is presented as a principle. PASS if exactly the three principles are present with explanations."
  ```

- [AC-1.3] Illustrative content menu present, framed explicitly as suggestions ("consider including any of these when they serve the task — none are required" or equivalent), covering at minimum: high-level process flows (before/after for changes), mental model diagrams, component/dependency relationships, deliverable + AC visualization, decision trees / trade-off comparisons, "what changes" callouts for amendments
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for an illustrative content menu. FAIL if: (1) the menu is missing, (2) the framing reads as prescriptive ('include the following', 'must include', 'required sections'), (3) any of these items are missing from the menu: process flows / before-after, mental model diagrams, component/dependency relationships, deliverable + AC visualization, decision trees or trade-off comparisons, 'what changes' callouts for amendments. PASS if the menu is present, framed as suggestions, and covers all six item types."
  ```

- [AC-1.4] Format requirements documented: single self-contained `.html` file at `/tmp/canvas-{ts}.html`, Tailwind via CDN, mermaid via CDN, embedded JS for auto-reload (mechanism agent's choice under principle "must auto-reload when file changes; preserve scroll/expand state when feasible")
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for format requirements. FAIL if any of these are missing: (1) single self-contained .html file specified, (2) file path /tmp/canvas-{ts}.html (with {ts} matching the manifest timestamp), (3) Tailwind via CDN specified, (4) mermaid via CDN specified, (5) auto-reload mechanism is left to the agent under the stated principle (must auto-reload when file changes; should preserve scroll/expand state when feasible). FAIL if mechanism is over-specified (e.g., mandates JS polling vs meta-refresh). PASS if all five format elements are present with the auto-reload principle stated and mechanism left to agent discretion."
  ```

- [AC-1.5] Update cadence documented: live updates fire after each meaningful event (interview-cluster checkpoint, coverage-goal resolution, AC/INV/PG/ASM addition or modification, Approach update, scope-guard or trade-off lock-in). Does NOT fire after every agent turn or tool call.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for the update-cadence section. FAIL if: (1) cadence is missing, (2) it does not enumerate meaningful events (interview cluster checkpoint, coverage-goal resolution, AC/INV/PG/ASM add/modify, Approach update, trade-off/scope-guard lock-in — these or close equivalents), (3) it does not exclude per-turn or per-tool-call updates as too noisy. PASS if cadence enumerates meaningful events and explicitly excludes noise."
  ```

- [AC-1.6] Auto-open mechanism documented: best-effort using first available of `xdg-open` / `open` / `start`; on first canvas creation only (not on every update). Failure to open is non-blocking — print path and continue.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for auto-open behavior. FAIL if: (1) launcher detection (xdg-open/open/start) is missing or not first-available-wins, (2) does not specify open happens only on first creation (not on every update), (3) does not specify failure is non-blocking with path printed. PASS if all three are present."
  ```

- [AC-1.7] Failure handling documented: any canvas-related operation failure (file write, browser open, anything) results in a single warning and continues with normal /define flow. Never blocks the manifest workflow.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for failure-handling section. FAIL if: (1) section missing, (2) does not specify warn-and-continue posture, (3) does not explicitly state canvas failure must never block /define / manifest workflow. PASS if all three are present."
  ```

- [AC-1.8] CANVAS_MODE.md includes at least one illustrative visual fragment (e.g., a mermaid flowchart snippet, a tabbed/collapsible component sketch, or an HTML structure example) framed as "what visual richness looks like, not a required structure." Prevents the agent from defaulting to bullet-list output. (Detection of generic-vs-rich framing covered by R-8 and INV-G2's prompt-reviewer pass.)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md for at least one illustrative visual fragment showing what visual richness looks like in practice (e.g., a mermaid diagram example, a tabbed component sketch, or an HTML/CSS pattern example). FAIL if: (1) no concrete visual fragment is shown anywhere, OR (2) examples are framed prescriptively ('your canvas must include sections like this' instead of 'this is what visual richness looks like; pick what fits'). PASS if at least one visual fragment exists with non-prescriptive framing."
  ```

- [AC-1.9] CANVAS_MODE.md size is bounded — soft cap of 300 lines. Beyond that, prefer pruning or splitting before adding more content (the file is loaded in full on every `--canvas` invocation; bloat costs tokens for every user).
  ```yaml
  verify:
    method: bash
    command: "lines=$(wc -l < claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md); echo \"CANVAS_MODE.md lines: $lines\"; [ \"$lines\" -le 300 ]"
  ```

- [AC-1.10] CANVAS_MODE.md does NOT restate the four suppression conditions (--amend, --interview autonomous, --medium slack, non-desktop). It assumes it's loaded only when canvas is genuinely active — SKILL.md owns suppression logic per PG-9.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/references/CANVAS_MODE.md. Verify it does NOT contain its own gating logic for the four suppression conditions (--amend, --interview autonomous, --medium slack, non-desktop env). The file may MENTION these in passing as context (e.g., 'this file is loaded only when canvas is active'), but must NOT re-evaluate or duplicate the suppression checks. FAIL if CANVAS_MODE.md re-states 'if --amend then skip', 'if autonomous then skip', etc. PASS if suppression logic is single-sourced in SKILL.md per PG-9."
  ```

### Deliverable 2: Update `define/SKILL.md`

Three integration changes to /define's main skill file: universal Goal reframe, `--canvas` flag parsing and dispatch, augmented Summary for Approval. Additions bounded to keep SKILL.md from bloating.

**Acceptance Criteria:**

- [AC-2.1] `--canvas` flag is parsed from arguments alongside existing `--interview`, `--medium`, `--amend`. SKILL.md's Input section documents the flag (one line: "Parse `--canvas` from arguments (can appear anywhere). When present, see Canvas Mode section.")
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Input section. Verify --canvas is documented as a parseable flag in the same paragraph or list as --interview, --medium, --amend. FAIL if --canvas is missing from Input section or documented elsewhere only. PASS if Input section explicitly mentions --canvas with a pointer to the Canvas Mode dispatch section."
  ```

- [AC-2.2] When `--canvas` is NOT passed, /define behavior is functionally equivalent to today — no canvas-related instructions execute, no warnings emit, no files written. (Behavioral check; structural enforcement at INV-G3.)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md. Verify all canvas-related additions (file writes, browser-open commands, summary-link append, CANVAS_MODE.md load instructions) are explicitly gated on --canvas being present (and env supporting it). FAIL if any canvas-related addition is unconditional, runs in the absent-flag path, or affects the existing summary-for-approval format when --canvas is not set. PASS if all additions are gated."
  ```

- [AC-2.3] `--canvas` is silently no-op when --amend is also passed, --interview autonomous (which transitively covers /auto since /auto always passes --interview autonomous to /define), or --medium slack. A single one-line warning ("--canvas requires a desktop environment with a graphical browser; skipping artifact generation" or equivalent) is printed when env lacks any of `xdg-open` / `open` / `start`. SKILL.md's Canvas Mode dispatch section enumerates all four conditions, with a note that /auto is covered by the autonomous case.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Canvas Mode dispatch section. Verify it explicitly enumerates four suppression conditions: (1) --amend present, (2) --interview autonomous (with a brief note that /auto invocations are covered because /auto always passes --interview autonomous), (3) --medium slack, (4) non-desktop env (no xdg-open/open/start). For (1)-(3) suppression must be silent (no warning). For (4) a single one-line warning must be specified. FAIL if any condition is missing, /auto is enumerated as a separate fifth condition rather than noted as covered by autonomous, or wrong suppression behavior. PASS if exactly the four enumerated correctly."
  ```

- [AC-2.4] Goal section in SKILL.md reframed to "build shared understanding, encoded formally as a Manifest" framing. Reframe is universal — applies whether or not --canvas is set. Reads as coherent framing, not feature-promotion bolted onto existing wording.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Goal section. Verify: (1) Goal explicitly frames /define as building shared understanding between user and agent, encoded formally as a Manifest; (2) the framing is universal — does not condition on --canvas being set; (3) reads as coherent universal framing, not feature-promotion. The Canvas may be mentioned as the optional visual layer of this universal goal, but the universal framing must stand on its own. FAIL if the Goal still reads as 'build a Manifest' without the shared-understanding framing, or if the new framing only makes sense in canvas context. PASS if Goal genuinely reframes /define around shared understanding."
  ```

- [AC-2.5] Canvas Mode dispatch section in SKILL.md is bounded — gates loading of `references/CANVAS_MODE.md` only when --canvas is active and env supports it; defers all operational detail (HTML structure, content menu, auto-reload, auto-open, failure handling, file naming) to CANVAS_MODE.md
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Canvas Mode dispatch section. Verify it: (1) gates loading CANVAS_MODE.md on --canvas being active AND env supporting it, (2) does NOT include operational detail (no HTML structure, no content menu, no auto-reload mechanism, no auto-open commands, no failure-handling logic, no file naming spec). All such detail must be in CANVAS_MODE.md. FAIL if dispatch section duplicates CANVAS_MODE.md content or includes operational specifics. PASS if dispatch is purely gating + load-instruction."
  ```

- [AC-2.6] Summary for Approval, when canvas is active, includes a one-line link to the canvas file path (e.g., "Canvas: file:///tmp/canvas-{ts}.html"). When canvas is not active, summary-for-approval format is unchanged.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Summary for Approval section. Verify: (1) when canvas is active, a one-line link to the canvas file path (file:///tmp/canvas-{ts}.html or equivalent) is appended to the existing summary; (2) when canvas is not active, summary format is unchanged from before this change. The canvas-link addition must be explicitly conditional on canvas being active. FAIL if link is unconditional or summary format is altered when canvas is inactive. PASS if both conditions met."
  ```

- [AC-2.7] SKILL.md additions are bounded — no more than 40 net added lines related to the canvas feature (Goal reframe + flag parsing + dispatch + summary tweak combined; target ~25, hard cap 40). Larger additions indicate operational detail leaking out of CANVAS_MODE.md.
  ```yaml
  verify:
    method: bash
    command: "added=$(git diff origin/main -- claude-plugins/manifest-dev/skills/define/SKILL.md | grep -E '^\\+[^+]' | wc -l); echo \"Added lines: $added\"; [ \"$added\" -le 40 ]"
  ```

- [AC-2.8] SKILL.md's Canvas Mode dispatch section instructs loading `references/CANVAS_MODE.md` in full (single-load contract — no section-targeted dispatch). Keeps the SKILL.md/CANVAS_MODE.md interface simple.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Canvas Mode dispatch section. Verify the load instruction reads as 'read references/CANVAS_MODE.md in full' or equivalent (the entire file is loaded, no section-targeted instructions). FAIL if dispatch tries to load only specific sections, or if the load contract is ambiguous. PASS if it's a single-load-the-whole-file contract."
  ```

- [AC-2.9] /do never touches the canvas — the manifest's flow contract (and SKILL.md's Canvas Mode section) explicitly states the canvas freezes at /define approval; /do does not regenerate, extend, or annotate it. Implementer signal in case it's later tempting to extend.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/skills/define/SKILL.md Canvas Mode section. Verify it explicitly states the canvas is fresh-/define-only and /do never touches it (no regeneration, extension, or annotation by /do). FAIL if this is missing or ambiguous. PASS if explicitly stated."
  ```

### Deliverable 3: Plugin metadata + READMEs

Bump plugin version (minor for new feature) and sync READMEs per CLAUDE.md checklist.

**Acceptance Criteria:**

- [AC-3.1] Plugin version in `claude-plugins/manifest-dev/.claude-plugin/plugin.json` bumped (minor version increment per CLAUDE.md rules). (Mechanical pass/fail; semantic correctness — minor not patch — covered by INV-G5.)
  ```yaml
  verify:
    method: bash
    command: "diff_out=$(git diff origin/main -- claude-plugins/manifest-dev/.claude-plugin/plugin.json); echo \"$diff_out\"; echo \"$diff_out\" | grep -qE '^[+-]\\s*\"version\"'"
  ```

- [AC-3.2] Root `README.md`, `claude-plugins/README.md`, and `claude-plugins/manifest-dev/README.md` reflect the new `--canvas` flag and the Shared Understanding Canvas concept. Each at the appropriate level of detail per existing READMEs (root: brief mention; plugin index: high-level; plugin README: usage summary).
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check that README.md (repo root), claude-plugins/README.md, and claude-plugins/manifest-dev/README.md mention the --canvas flag and the Shared Understanding Canvas concept. Each at appropriate detail level — root may mention briefly, plugin index high-level, plugin README usage-level. FAIL if any of the three READMEs entirely lacks reference to the new capability. PASS if all three reflect it appropriately."
  ```

- [AC-3.3] If `claude-plugins/manifest-dev/.claude-plugin/plugin.json` description or keywords would benefit from updates reflecting canvas capability, those are made (per CLAUDE.md guidance on plugin.json updates for significant capability additions). Judgment call — manifest-dev's existing description may already be broad enough; only update if clearly warranted.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    prompt: "Check claude-plugins/manifest-dev/.claude-plugin/plugin.json description and keywords. Verify whether the addition of the --canvas / Shared Understanding Canvas capability warrants an update. PASS if either: (a) description/keywords were updated to reflect the new capability, OR (b) the existing description/keywords are already broad enough (e.g., 'verification-first manifest workflows' covers it) and no update was needed. FAIL only if the addition clearly merits a description/keywords update and none was made."
  ```
