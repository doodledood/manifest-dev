# Definition: walk-pr canvas — three-layer orientation + depth-on-demand + boundary-first depth

## 1. Intent & Context

- **Goal:** Encode three coordinated contracts in `walk-pr` so a reviewer with codebase fluency but zero PR context can land on the canvas, understand the feature at workflow level, skim each sub-changeset's behavior and verification at a glance, and drop into boundary-level depth only where they want it — with the diff one click further as evidence rather than the default exposition. Per ADR `docs/adr/20260518-walk-pr-boundary-first-canvas-depth.md`.

- **Mental Model:** Walk-pr's previous canvas mistook one mode of review (deep, topic-by-topic) for the only mode. The new model has **three layers**: (1) a **PR primer** above the SC walk that introduces the feature in workflow vocabulary and defines PR-introduced terms; (2) **per-SC card surfaces** that show only a one-sentence behavior summary and a one-sentence verification probe, collapsing everything else behind a single expand; (3) **inside the expand, a boundary view** describing the change at module-boundary altitude (types, signatures, dependencies, contracts) in ≤3 short freeform paragraphs, with diff hunks as per-file on-demand affordances. SKILL.md carries enough of these contracts at the surface for chat-only callers (who never load CANVAS_MODE.md); CANVAS_MODE.md owns canvas-specific mechanics. The reader-model gets an addendum: PR-introduced vocabulary is not shared ground; the primer is the only place it gets introduced.

- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

- **Architecture:**
  - Update `references/CANVAS_MODE.md` with: a new **PR primer** section (conditional slots, workflow-vocabulary level); an update to the **Cognitive-load contract / Interaction model** to make per-SC card surfaces carry only behavior + verify always-visible, with everything else collapsed behind a single per-SC expand; a new **boundary view** sub-section (goal-stated, ≤3 paragraphs, freeform, at module-boundary altitude); a **diff-as-evidence** rule (per-file `<details>` "show diff" affordance inside the expand, on-demand); a **reader-model addendum** about PR-introduced vocabulary; new **anti-patterns** covering line-level diff as default depth, problem+change+mechanism prose grounding, type-listing boundary view, type-signature glossary, and primer that introduces while asking the reviewer to evaluate.
  - Update `SKILL.md` so chat-only callers (who never load `CANVAS_MODE.md`) get the orientation + depth contracts self-sufficiently — surface the three-layer model in compressed form, name the PR-introduced-vocabulary clause, and reference CANVAS_MODE.md for canvas-specific mechanics.
  - Bump `claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json` version `0.6.2` → `0.7.0` (minor — behavior change to an existing skill).
  - Sync READMEs only if topic-rendering or canvas-rendering claims need updating; READMEs stay high-level per CLAUDE.md README Guidelines.

- **Execution Order:**
  - D1 → D2 → D3 → D4
  - Rationale: write the canvas contract first (D1: CANVAS_MODE.md is the source of truth for canvas mechanics), then surface its load-bearing pieces into SKILL.md for chat-only callers (D2), then bump the version (D3), then sync READMEs (D4, likely no-op).

- **Risk Areas:**
  - [R-1] Contract becomes prescriptive HOW (PROMPTING anti-pattern — rigid step-by-step instead of goal/constraint) | Detect: prompt-reviewer flags rigid step-by-step or capability instructions; INV-G4 catches.
  - [R-2] Goal-stated boundary view regresses to walls of text (LLM packs four facets into freeform prose) | Detect: AC-1.3 verifies the boundary view section names the altitude (module boundary), names load-bearing-only inclusion, and explicitly forbids exhaustive type/file enumeration; anti-pattern entry from AC-1.6 reinforces.
  - [R-3] New rules contradict existing CANVAS_MODE.md sections (Cognitive-load contract, Interaction model, Rendering and layout adapt, Lifecycle, Failure handling) — especially the prior 2026-05-14 progressive-disclosure rule on per-topic detail | Detect: AC-1.7 reviews internal consistency end-to-end including the prior progressive-disclosure rule (which still holds — topics still have collapsible detail bodies; the new model layers on top, not replacing).
  - [R-4] SKILL.md becomes too long trying to carry the full contract for chat-only — should carry the load-bearing surface only, not the full canvas mechanics | Detect: AC-2.2 caps the added-line count; AC-2.3 verifies self-sufficiency without canvas mechanics duplicated.
  - [R-5] Anti-patterns are added vaguely or skip one of the five named failure modes | Detect: AC-1.6 names all five and requires each to be recognizable in the section.
  - [R-6] Cross-mode contract drift — SKILL.md says one thing about the headline / orientation / depth and CANVAS_MODE.md says something subtly different | Detect: AC-2.3 + AC-1.7 require the duplicated pieces to stay in sync; INV-G2's carve-out applies (intentional duplication is justified, but copies must align).
  - [R-7] Topic shape contract from prior iteration (2026-05-14) gets accidentally weakened or duplicated | Detect: AC-1.7 confirms the existing topic-shape / progressive-disclosure contract survives intact alongside the new layers.
  - [R-8] Diff-as-evidence affordance is specified ambiguously — could be interpreted as a single per-SC diff blob or per-file affordances; per-file is what's intended | Detect: AC-1.4 names "per-file" explicitly and forbids monolithic SC-level diff exposure inside the expand.

- **Trade-offs:**
  - [T-1] Goal-stated boundary view vs rigid four-facet structure → Prefer goal-stated. Decision in ADR per figure-out pushback: rigid structure is scaffolding the LLM doesn't need if the goal is clear, and small PRs end up with empty named headers. Goal-statement-over-structure is honest to how the rest of CANVAS_MODE.md works.
  - [T-2] Diff hunks gone entirely vs per-file on-demand affordance → Prefer per-file on-demand. The skill's "verbatim quotes" value gives ground to "verbatim quotes, on demand" — not "verbatim quotes, gone." Diff is one click per file; reviewers who want it have it.
  - [T-3] Cross-mode parity (SKILL.md + CANVAS_MODE.md both carry the new contracts) vs canvas-only contracts (chat-only walk gets nothing new) → Prefer parity. Orientation absence and detail-forcing affect both modes. Canvas-specific mechanics (`<details>` expand, per-file diff affordance, copy-as-prompt bundle) stay in CANVAS_MODE.md; the contract layer (primer, depth-on-demand, boundary-first depth, reader-model addendum) appears in both.
  - [T-4] PR primer always rendered vs conditionally rendered → Prefer conditional. Problem statement always present; glossary, mermaid sketch, reading hint each rendered only when load-bearing. Empty slots skipped — no placeholders.
  - [T-5] Behavior summary + verification probe both required vs only one of them → Prefer both. Behavior names the change in user terms; verify names how a reviewer would observe it concretely. Either alone leaves the reviewer guessing at the other.
  - [T-6] Boundary view replaces the current "ground the user" prose + "survived/cut/moved" paragraph entirely vs additive | → Prefer replaces. The prior dense-prose paragraphs are exactly the BOOM source the ADR rejects. The boundary view inherits their role at a different altitude — load-bearing structural change is summarized; line-level inventory moves to the per-file diff affordance.

## 3. Global Invariants

- [INV-G1] Change intent matches goal (no LOW+ severity issues from change-intent-reviewer).
  ```yaml
  verify:
    agent: change-intent-reviewer
    prompt: "Review the diff on this branch against the manifest's stated goal: encode three layered contracts in walk-pr — PR primer above the SC walk, per-SC card surfaces with behavior+verify always-visible (depth collapsed), and boundary-first depth content with diff as on-demand per-file affordance — per docs/adr/20260518-walk-pr-boundary-first-canvas-depth.md. Flag any divergence between stated intent and actual behavioral change. Files of interest: claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md and claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md."
  ```

- [INV-G2] Prompt-quality gates pass on changed prompt content (no MEDIUM+ from prompt-reviewer, except for intentional contract duplication between SKILL.md and CANVAS_MODE.md — duplication for chat-only self-sufficiency is a design choice per T-3, AC-2.3, provided both copies stay in sync).
  ```yaml
  verify:
    agent: prompt-reviewer
    prompt: "Review the changed sections of claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md and claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. Focus on the new PR primer section, per-SC card visibility model, boundary view sub-section, diff-as-evidence rule, reader-model addendum, and added anti-patterns. Apply standard prompt-quality dimensions (clarity, no conflicts, structure, density, no anti-patterns, invocation fit, complexity fit, edge case coverage, emotional tone). Report any MEDIUM+ issues. When evaluating contract duplication between SKILL.md and CANVAS_MODE.md, treat duplication required by AC-2.3 (SKILL.md must be self-sufficient for chat-only mode, since chat-only never loads CANVAS_MODE.md) as a design choice rather than a MEDIUM issue. Verify the duplicated copies are in sync; do not flag the duplication itself."
  ```

- [INV-G3] No new external JS dependencies introduced. The diff-as-evidence affordance uses native `<details>` (or other zero-dependency HTML) per the existing CANVAS_MODE.md "Format" / "Self-contained" constraint.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. Confirm: (a) the diff-as-evidence per-file affordance uses native HTML (e.g. <details>/<summary>) or otherwise zero-dependency, not a new JS library; (b) the existing 'Format' / 'Self-contained' constraint (Tailwind + mermaid + diff renderer + syntax-highlighter via CDN, opens via file://) still holds; (c) no new CDN script tags added beyond the existing four. PASS if all three hold; FAIL listing the specific violation otherwise."
  ```

- [INV-G4] No prescriptive HOW or capability instructions introduced. The new contracts state goals and constraints, not rigid step-by-step procedures.
  ```yaml
  verify:
    prompt: "Read the diff on claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md and claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. Identify any added content that prescribes HOW (rigid step-by-step procedures, 'first do X then Y then Z'), instructs the model on capabilities it already has ('use grep', 'read the file'), or arbitrary limits without justification. FAIL with the offending lines if found; PASS if all additions are goal/constraint/shape statements."
  ```

- [INV-G5] Project-wide lint / format / typecheck gate runs clean per CLAUDE.md "Before PR" checklist.
  ```yaml
  verify:
    method: bash
    command: "ruff check claude-plugins/ && black --check claude-plugins/ && mypy 2>&1 | tail -5"
  ```

- [INV-G6] Edits respect the symlink convention — only `claude-plugins/manifest-dev-tools/` plugin paths are modified; `.claude/skills/walk-pr` (a symlink to the plugin) was not edited directly.
  ```yaml
  verify:
    method: bash
    command: "test $(git diff --name-only origin/main -- .claude/skills/walk-pr/ 2>/dev/null | wc -l) -eq 0"
  ```

## 4. Process Guidance

- [PG-1] Edit `claude-plugins/manifest-dev-tools/` paths only — the `.claude/skills/walk-pr` path is a symlink to the plugin (per CLAUDE.md).
- [PG-2] High-signal changes only. Don't restructure CANVAS_MODE.md beyond what the three new contracts and the anti-patterns need. Size delta must be justified by content, not padding.
- [PG-3] Keep SKILL.md tight. Carry the surface-level contract for chat-only callers (PR primer goal, per-SC behavior+verify surface, boundary-first depth, PR-vocabulary clause); do not duplicate canvas mechanics (`<details>`, per-file affordance, copy-as-prompt). CANVAS_MODE.md is referenced for canvas surface details.
- [PG-4] Calibrate emotional tone — low arousal, no urgency framing, no "MUST always". Use "When X, do Y" decision-rule shape for non-invariant guidance. Match the existing CANVAS_MODE.md voice.
- [PG-5] The prior iteration's progressive-disclosure rule on per-topic detail (from `.manifest/walk-pr-canvas-topic-density-2026-05-14.md`) still holds. The new model layers on top — adding per-SC depth-on-demand and boundary-first depth — without replacing per-topic detail collapse.

## 5. Known Assumptions

- [ASM-1] (auto) PR primer rendered as a section in the canvas above the categorized overview table (not behind a per-SC expand). Default: above-overview placement. Impact if wrong: trivial relocation. Reasoning: the primer is orientation; orientation belongs at the top.
- [ASM-2] (auto) Behavior summary + verification probe render as always-visible content inside each SC card, above (or replacing the current default contents of) the SC's `sc-body`. Everything else inside the SC body is hidden until the reviewer expands. Default: as above. Impact if wrong: minor visual rework.
- [ASM-3] (auto) The per-SC expand affordance is a single click — could be the `sc-card.collapsed` toggle that exists today (clicking the SC header), or a dedicated "expand details" button. Default: reuse the existing collapse toggle on the SC header so no new UI primitive is introduced. Impact if wrong: swap toggle target. Reasoning: existing canvas already supports per-SC collapse/expand for the focus rationing.
- [ASM-4] (auto) Diff-as-evidence per-file affordance renders as native `<details>` per file inside the expanded SC body, keyed by file path. Default: native `<details>`. Impact if wrong: if a different primitive is preferred, swap rendering rule.
- [ASM-5] (auto) Plugin version bump is minor (0.6.2 → 0.7.0). Default: minor. Impact if wrong: trivial re-bump. Reasoning: behavior change to an existing skill that meaningfully alters output (orientation + depth-on-demand + boundary-first), not breaking.
- [ASM-6] (auto) READMEs likely do not need updates because they describe walk-pr at a high level, not topic / SC / canvas rendering. Default: read each, edit only if a topic-rendering or canvas-rendering claim contradicts the new contract. Impact if wrong: a README stays accurate by accident or needs a one-line tweak.
- [ASM-7] (auto) Tests not applicable — markdown skill files have no automated unit test scaffold in this repo. Default: skip test addition. Impact if wrong: nothing automated could meaningfully verify prose-shape and rendering-rule contracts beyond the prompt-reviewer gate.
- [ASM-8] (auto) PROMPTING.md gates apply; CODING.md does not compose (no executable code changes — only markdown skill/contract files and a JSON version bump).
- [ASM-9] (auto) The prior iteration's progressive-disclosure rule on per-topic detail bodies survives intact (PG-5). The new model adds two outer layers (PR primer above SCs, behavior+verify per SC surface) and one inner layer (boundary view replacing prose grounding + survived/cut/moved); the existing per-topic `<details>` for topic-level rationale stays untouched.
- [ASM-10] (auto) The categorized overview table at the canvas top survives. The PR primer goes above it. The category table remains the navigation surface.
- [ASM-11] (auto) "Survived / cut / moved" paragraph as a named pattern is retired in favor of the boundary view. Existing CANVAS_MODE.md mentions of the pattern get updated to reference the boundary view. Default: replace.
- [ASM-12] (auto) Verification probe shape is "concrete observable" — a check the reviewer could run, paired with an expected observation. Format left to LLM judgment with the goal-statement framing.

## 6. Deliverables

### Deliverable 1: CANVAS_MODE.md — PR primer + per-SC depth-on-demand + boundary view + diff-as-evidence + reader-model addendum + anti-patterns

**Acceptance Criteria:**

- [AC-1.1] CANVAS_MODE.md contains a named **PR primer** section that establishes: (a) the primer renders above the categorized overview, (b) a one-paragraph problem statement in workflow vocabulary (not codebase identifiers) is always present, (c) conditional slots — a glossary of PR-introduced concepts (workflow-level, not type-signature-level), a mermaid sketch when component flow is at stake, and a one-sentence reading hint when SCs differ in importance — render only when load-bearing; empty slots are skipped without placeholders, (d) the goal is named (a reviewer leaves the primer knowing what to expect when they hit new terms downstream).
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if the PR primer contract names ALL of: (1) placement above the categorized overview; (2) one-paragraph problem statement in workflow vocabulary as always present; (3) conditional slots for glossary, mermaid sketch, and reading hint; (4) workflow-level vocabulary, not type-signature-level (e.g. 'Live fallback: when replay can't find a frozen fact, it calls the live business service and notes which fact was missing' — NOT 'LiveFallbackHandle is a record with access: ExternalServiceAccess and recordLiveFallback: (key) => void'); (5) empty slots skipped, no placeholders; (6) the goal stated (reviewer leaves primer knowing what to expect downstream). FAIL with the missing point if any are absent."
  ```

- [AC-1.2] CANVAS_MODE.md updates the per-SC card visibility model so each SC's always-visible content is **only** a one-sentence behavior summary in user terms + a one-sentence verification probe (concrete observable). All other content — prose grounding, boundary view, diff hunks, topics — collapses behind a single per-SC expand affordance. The prior 2026-05-14 progressive-disclosure rule on per-topic detail bodies still applies inside the expanded SC.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md (Cognitive-load contract / Interaction model / Topic shape and progressive disclosure). PASS only if: (1) per-SC always-visible content is named as exactly behavior summary + verification probe; (2) behavior summary is in user terms (workflow vocabulary), one sentence; (3) verification probe is concrete and observable, one sentence; (4) all other content collapses behind a single per-SC expand; (5) the prior progressive-disclosure rule for per-topic detail bodies is preserved (topics retain their collapsible `<details>` body inside the expanded SC). FAIL with the missing point if any are absent."
  ```

- [AC-1.3] CANVAS_MODE.md contains a named **boundary view** sub-section inside the expand. Its contract: goal stated (give the reviewer the shape of the change at module-boundary altitude — types, signatures, dependencies, contracts — without forcing them to parse diff); rendered as ≤3 short paragraphs, freeform, load-bearing pieces only (no exhaustive type/file enumeration); replaces the prior "ground the user" prose and "survived/cut/moved" paragraph as the SC's structural exposition.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if the boundary view contract names ALL of: (1) the goal — give a reviewer the shape of the change at module-boundary altitude without parsing diff; (2) the altitude — module-boundary level, covering types / signatures / dependencies / contracts; (3) shape constraints — ≤3 short paragraphs, freeform, load-bearing pieces only; (4) explicit forbiddance of exhaustive enumeration (no listing every type or every file); (5) replacement of the prior dense prose grounding + 'survived/cut/moved' paragraph (their content moves to the boundary view; line-level inventory moves to the per-file diff affordance per AC-1.4). FAIL listing the missing point if any are absent."
  ```

- [AC-1.4] CANVAS_MODE.md specifies that diff hunks render as **per-file on-demand affordances** inside the expanded SC (one collapsible per file in the changeset, opened by the reviewer when needed), not as a monolithic SC-level diff block visible by default. Native HTML (`<details>` or equivalent zero-dependency primitive) per INV-G3.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if: (1) diff hunks are explicitly per-file (one affordance per touched file in the SC), not a monolithic SC-level diff block; (2) the affordance is on-demand — closed by default, opened by the reviewer; (3) the primitive is native HTML (e.g. `<details>` or equivalent), no new JS dependency; (4) the diff is NOT in the always-visible SC card surface — it's inside the expanded body, behind its own per-file affordance. FAIL with the missing point if any are absent."
  ```

- [AC-1.5] CANVAS_MODE.md Reader model section gains an **addendum** stating: codebase-fluent is still the assumption for pre-PR vocabulary; vocabulary introduced by *this PR* is not shared ground; the primer is the only place that vocabulary gets introduced; downstream SC summaries, boundary views, and topics use it without re-explanation.
  ```yaml
  verify:
    prompt: "Read the Reader model section of claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if the addendum names ALL of: (1) codebase fluency still holds for pre-PR vocabulary; (2) PR-introduced vocabulary is NOT shared ground; (3) the primer is the only place new vocabulary gets introduced; (4) downstream SC summaries, boundary views, and topics use the introduced vocabulary without re-explanation. FAIL listing the missing point if any are absent."
  ```

- [AC-1.6] CANVAS_MODE.md Anti-patterns section gains entries explicitly naming the new failure modes: (a) line-level diff as default depth (diff visible by default in the SC card surface); (b) prose grounding that mixes problem + change + mechanism into one block; (c) boundary view that regresses to listing every type / file / call site by name (vs load-bearing pieces only); (d) primer glossary at type-signature level instead of workflow level; (e) primer introducing a new concept while in the same paragraph asking the reviewer to evaluate it (introduction and evaluation must be separated).
  ```yaml
  verify:
    prompt: "Read the Anti-patterns section of claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if ALL five new anti-patterns appear (named or paraphrased recognizably): (a) line-level diff as default depth; (b) prose grounding mixing problem+change+mechanism; (c) boundary view listing every type/file/call site; (d) type-signature-level glossary in the primer; (e) primer introducing a concept while asking the reviewer to evaluate it. FAIL listing the missing anti-pattern if any are absent."
  ```

- [AC-1.7] The new content composes with existing CANVAS_MODE.md sections — Cognitive-load contract (one SC / one topic in focus), Interaction model (one-shot generation, persisted textareas), Rendering and layout adapt to the content, Topic shape and progressive disclosure (the 2026-05-14 per-topic detail-body collapse rule, which still holds for topics inside the expanded SC), Lifecycle (auto-reload preserves state), and Failure handling (non-blocking) — without contradiction. The prior topic-shape contract (two declarative sentences, codebase vocabulary, no narrated reasoning) survives intact and is referenced where load-bearing.
  ```yaml
  verify:
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md end-to-end. The new PR primer, per-SC card visibility model, boundary view, diff-as-evidence affordance, reader-model addendum, and anti-patterns should compose with — not contradict — these existing sections: 'Cognitive-load contract' (one sub-changeset / one topic in focus), 'Interaction model' (one-shot generation, persisted textareas), 'Rendering and layout adapt to the content', 'Topic shape and progressive disclosure' (per-topic detail bodies in `<details>`, closed by default, applied only to the in-focus topic), 'Lifecycle' (auto-reload preserves scroll / expand-collapse / textareas), and 'Failure handling' (non-blocking). Specifically check: (a) the per-SC depth collapse interacts coherently with the existing focus-rationing rule (which collapses non-focused SCs already); (b) the per-file diff affordance state survives auto-reload via the existing expand/collapse state bucket; (c) the boundary view replaces the prior 'ground the user' prose and 'survived/cut/moved' paragraph without leaving dangling references; (d) the prior topic-shape contract (two declarative sentences, codebase vocabulary, no narrated reasoning) is intact; (e) the prior per-topic detail-body progressive-disclosure rule is intact. Report any contradiction, ambiguity, or place where two rules tell the LLM to do conflicting things. PASS if internally consistent; FAIL with the conflict cited."
  ```

### Deliverable 2: SKILL.md — surface contracts for chat-only callers

**Acceptance Criteria:**

- [AC-2.1] SKILL.md surface text carries the three-layer model in compressed form so chat-only callers (who never load CANVAS_MODE.md) get the contracts self-sufficiently: (a) PR primer above the SC walk introducing the feature in workflow vocabulary and PR-introduced terms; (b) per-SC behavior summary + verification probe as the always-visible surface, with depth (boundary view, diff, topics) on demand; (c) boundary-first depth — boundary view first, diff one click further as evidence; (d) the reader-model clause about PR-introduced vocabulary.
  ```yaml
  verify:
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md. PASS only if the SKILL.md surface text names ALL of: (1) PR primer above the SC walk with workflow-vocabulary problem statement and PR-introduced concept introduction; (2) per-SC behavior summary + verification probe as the always-visible surface with depth-on-demand; (3) boundary-first depth — boundary view first, diff as per-file on-demand evidence; (4) reader-model clause stating PR-introduced vocabulary is not shared ground and gets introduced only in the primer. FAIL listing the missing point if any are absent."
  ```

- [AC-2.2] SKILL.md stays tight — no more than ~20 added non-blank lines vs origin/main. The added content carries only the surface-level contracts (per AC-2.1) for chat-only self-sufficiency; canvas-specific mechanics (`<details>` rendering, per-file affordance, copy-as-prompt bundle, localStorage persistence) stay in CANVAS_MODE.md and are not duplicated into SKILL.md.
  ```yaml
  verify:
    method: bash
    command: "test $(git diff origin/main -- claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md | awk '/^\\+/ && !/^\\+\\+\\+/ && !/^\\+[[:space:]]*$/' | wc -l) -le 20"
  ```

- [AC-2.3] The SKILL.md additions are self-sufficient for chat-only mode — a reader who only loads SKILL.md gets the full three-layer contract without needing to load CANVAS_MODE.md, AND in chat-only mode (no canvas) supporting detail still has a place to land (subsequent message / on-demand probe / textarea body), so the change doesn't silently delete rationale / code excerpts / alternatives from chat mode.
  ```yaml
  verify:
    agent: general-purpose
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md as if it were the only file you had. PASS only if: (a) the three-layer contract (PR primer above SCs, per-SC behavior+verify as always-visible surface with depth on demand, boundary-first depth with diff as evidence) and the PR-vocabulary reader-model clause are fully conveyed without needing references/CANVAS_MODE.md; (b) in chat-only mode (no canvas), it remains clear where supporting detail (rationale, code excerpts, alternatives) lives — whether in subsequent messages, on-demand probes, or textarea bodies — so the change doesn't silently delete that material from chat. FAIL citing which condition isn't met."
  ```

- [AC-2.4] No canvas-specific mechanics leak into SKILL.md — `<details>`, per-file affordance, copy-as-prompt bundle, localStorage, Tailwind/mermaid CDN, `/tmp/walk-pr-canvas-*.html` — none of these surface words should appear in SKILL.md added content (they belong in CANVAS_MODE.md). Cross-mode parity = same *contracts*, not same *mechanics*.
  ```yaml
  verify:
    method: bash
    command: "! git diff origin/main -- claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md | awk '/^\\+/ && !/^\\+\\+\\+/' | grep -E -i '<details>|<summary>|localStorage|copy[- ]as[- ]prompt|tailwind|mermaid\\.run|/tmp/walk-pr-canvas|cdn\\.tailwindcss|file:///'"
  ```

### Deliverable 3: Plugin version bump

**Acceptance Criteria:**

- [AC-3.1] `claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json` version bumped from `0.6.2` to `0.7.0`.
  ```yaml
  verify:
    method: bash
    command: "grep -q '\"version\": \"0.7.0\"' claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json"
  ```

### Deliverable 4: README sync

**Acceptance Criteria:**

- [AC-4.1] Topic-rendering and canvas-rendering claims in the three READMEs (`README.md` root, `claude-plugins/README.md`, `claude-plugins/manifest-dev-tools/README.md`) don't contradict the new contract. Cheap deterministic check: no surviving phrase describing the *old* density behavior or diff-first canvas (wall-of-text per SC, inline rationale, diff-first depth, no per-SC depth-on-demand). Default expected outcome: no edits needed — READMEs stay high-level per CLAUDE.md README Guidelines.
  ```yaml
  verify:
    method: bash
    command: "! grep -E -i 'wall[- ]of[- ]text|diff[- ]first|monolithic per-sc|inline rationale' README.md claude-plugins/README.md claude-plugins/manifest-dev-tools/README.md 2>/dev/null"
  ```
