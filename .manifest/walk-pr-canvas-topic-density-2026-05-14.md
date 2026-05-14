# Definition: walk-pr canvas — reduce per-topic density via progressive disclosure

## 1. Intent & Context
- **Goal:** Eliminate walls-of-text within each focused topic in walk-pr canvas mode by encoding a per-topic prose-shape contract and a progressive-disclosure rendering rule. Topics must land in one glance; supporting detail (rationale, code excerpts, alternatives) is one click away, not inline.
- **Mental Model:** The canvas already rations *visibility* across sub-changesets and topics (one-of-each in focus). What it lacks is a *content-density* contract within a topic. The fix has two coupled pieces: (a) **prose shape** — each topic's *visible headline* is a one-line concrete framing of the concern (in codebase vocabulary) + a one-line recommended call, each line a single declarative sentence with no nested clauses or embedded justification; no narrated reasoning; no invented jargon; (b) **progressive disclosure** — anything beyond that headline (the "why", topic-level code excerpts, trade-off detail, alternatives considered) renders behind a single expand affordance per topic, closed by default, applied only to the *current* topic's body. Prior/future topics keep their existing rationing (preview / dimmed title). Sub-changeset diff hunks keep rendering inside the in-focus card per existing 'Rendering and layout adapt to the content' rule. Reader model the LLM targets: someone who **lives in the repo** (knows modules, idioms, naming) but has **zero context on this PR** — assume codebase fluency, never PR fluency.
- **Mode:** thorough
- **Interview:** autonomous
- **Medium:** local

## 2. Approach

- **Architecture:**
  - Update `references/CANVAS_MODE.md` with two new contracts: (1) **Reader model** named explicitly so the LLM targets the right level of explanation; (2) **Topic shape and progressive disclosure** — define the visible headline (one-line framing + recommended call, single declarative sentences, no embedded justification) and the collapsible detail body (rationale, topic-level code excerpts, alternatives). Add `<details>`/`<summary>`-based rendering rule (native HTML, no JS dependency) with localStorage-persisted open state. Constrain the new rule to the *current* topic's body so the existing focus rationing (current vs prior preview vs future dimmed title) is unaffected. Add a single good/bad headline contrast example so "narrated reasoning" has a concrete anchor.
  - Update `SKILL.md` "review topics" sentence to name the headline shape so chat-only callers (who never load CANVAS_MODE.md) get the contract self-sufficiently.
  - Add anti-patterns: "narrated reasoning inline" (the LLM-prose tell), "headline restates body", "detail dump in the headline", "invented abstraction instead of codebase vocabulary".
  - Bump plugin version 0.5.1 → 0.6.0 (minor: behavior change, not breaking).
  - Sync READMEs only if they describe topic rendering specifically; otherwise no-op.

- **Execution Order:**
  - D1 → D2 → D3 → D4
  - Rationale: edit the contract (D1: CANVAS_MODE.md) before the surface pointer (D2: SKILL.md); bump version (D3) after content stabilizes; sync READMEs (D4) only if needed.

- **Risk Areas:**
  - [R-1] Contract becomes prescriptive HOW (PROMPTING.md anti-pattern) | Detect: prompt-reviewer flags rigid step-by-step or capability instructions
  - [R-2] Progressive-disclosure rule adds JS complexity that breaks the self-contained `file://` constraint | Detect: review uses `<details>` (native HTML) only; no new JS deps introduced
  - [R-3] Regression: rendering rule conflicts with existing Cognitive-load contract / Interaction model / Rendering-adapts / Lifecycle sections | Detect: AC-1.5 subagent reviews internal consistency including localStorage persistence behavior across reloads
  - [R-4] Over-engineering: change doubles file length or adds rules for edge cases that don't matter | Detect: size delta justified by content, not padding; SKILL.md capped at +6 added lines
  - [R-5] Headline framing slips into "summary of body" pattern (LLM tendency to restate) | Detect: anti-pattern explicitly named; contrast example included
  - [R-6] Chat-only walk-pr regresses: contract reads naturally in canvas but supporting detail has no home in chat-only mode after the change | Detect: AC-2.3 verifies the chat-only mode still has a place for rationale / code / alternatives (subsequent message, on-demand probe, etc.) without forcing reviewer scroll
  - [R-7] Long-line headline: LLM stays inside one framing line + one recommended-call line but pads each line with nested clauses and embedded justification, still producing a wall | Detect: AC-1.2 requires single declarative sentence per line, no nested clauses, no embedded justification

- **Trade-offs:**
  - [T-1] Native `<details>` vs custom JS expand widget → Prefer `<details>` because zero-dep, accessible, persists naturally with localStorage, degrades cleanly. The canvas ships with a "no local server" / `file://` constraint, and `<details>` is the lowest-friction fit.
  - [T-2] Shape constraint vs word/line cap → Prefer shape-constraint with explicit "single declarative sentence; no nested clauses; no embedded justification" — arbitrary limits is a PROMPTING anti-pattern; sentence-shape bites without a magic number.
  - [T-3] Touch SKILL.md surface vs leave the contract only in references → Prefer surface touch (one updated sentence in SKILL.md naming the headline shape) because chat-only mode never loads CANVAS_MODE.md; chat-only callers need the contract self-sufficiently. CANVAS_MODE.md still owns the full progressive-disclosure rendering rule (canvas-specific).
  - [T-4] `<details>` applies to every topic uniformly vs only the current topic's body → Prefer current-topic-only. The existing focus rationing already collapses prior topics to one-line previews and dims future topics to titles; another collapse axis there is redundant. Apply `<details>` only to the in-focus topic's supporting detail.
  - [T-5] Topic-level code excerpts (illustrative snippets cited inside a probe / trade-off) vs sub-changeset diff hunks → Move only *topic-level* excerpts behind expand. The sub-changeset's actual diff hunks keep rendering in the in-focus card per existing 'Rendering and layout adapt to the content' rule. Moving sub-changeset diffs behind expand would be a much bigger UX change and isn't what overwhelms.

## 3. Global Invariants

- [INV-G1] Change intent matches goal (no LOW+ severity issues from change-intent-reviewer).
  ```yaml
  verify:
    method: subagent
    agent: change-intent-reviewer
    model: inherit
    prompt: "Review the diff on this branch against the manifest's stated goal: reduce per-topic density in walk-pr canvas via a prose-shape contract and progressive-disclosure rendering rule. Flag any divergence between stated intent and actual behavioral change. Files of interest: claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md and claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md."
  ```

- [INV-G2] Prompt-quality gates pass on changed prompt content (no MEDIUM+ from prompt-reviewer, except for intentional contract duplication explicitly required by another AC — duplication for surface self-sufficiency is a design choice, not a quality defect, provided both copies stay in sync).
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review the changed sections of claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md and claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. Focus on the new reader-model statement, topic shape contract, progressive-disclosure rendering rule, and added anti-patterns. Apply standard prompt-quality dimensions (clarity, no conflicts, structure, density, no anti-patterns, invocation fit, complexity fit, edge case coverage, emotional tone). Report any MEDIUM+ issues. When evaluating contract duplication between SKILL.md and references/CANVAS_MODE.md, treat duplication explicitly required by AC-2.3 (SKILL.md must be self-sufficient for chat-only mode, since chat-only never loads CANVAS_MODE.md) as a design choice rather than a MEDIUM issue. Verify the duplicated copies are in sync; do not flag the duplication itself."
  ```

- [INV-G3] No new external JS dependencies introduced. Progressive disclosure uses native `<details>` (or other zero-dep HTML), preserving the self-contained `file://` and CDN-only constraint already in CANVAS_MODE.md "Format" section.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. Confirm: (a) the progressive-disclosure mechanism for per-topic detail uses native HTML (e.g. <details>/<summary>) or otherwise zero-dependency, not a new JS library; (b) the existing 'Format' / 'Self-contained' constraint (Tailwind + mermaid + diff renderer + syntax-highlighter via CDN, opens via file://) still holds; (c) no new CDN script tags added beyond the existing four. PASS if all three hold; FAIL listing the specific violation otherwise."
  ```

- [INV-G4] No prescriptive HOW or capability instructions introduced.
  ```yaml
  verify:
    method: codebase
    prompt: "Read the diff on claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md and claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. Identify any added content that prescribes HOW (rigid step-by-step procedures, 'first do X then Y then Z') or instructs the model on capabilities it already has ('use grep', 'read the file'). FAIL with the offending lines if found; PASS if all additions are goal/constraint/shape statements."
  ```

- [INV-G5] Project-wide lint / format / typecheck gate runs clean per CLAUDE.md before-PR checklist.
  ```yaml
  verify:
    method: bash
    command: "cd /home/user/manifest-dev && ruff check claude-plugins/ && black --check claude-plugins/ && mypy 2>&1 | tail -5"
  ```

- [INV-G6] Edits respect the symlink convention — only the `claude-plugins/manifest-dev-tools/` plugin path is modified; the `.claude/skills/walk-pr` symlink target was not edited directly (per CLAUDE.md symlink convention and PG-1).
  ```yaml
  verify:
    method: bash
    command: "test $(git diff --name-only origin/main -- .claude/skills/walk-pr/ 2>/dev/null | wc -l) -eq 0"
  ```

## 4. Process Guidance

- [PG-1] Edit `claude-plugins/manifest-dev-tools/` paths only — the `.claude/skills/walk-pr` path is a symlink to the plugin (per CLAUDE.md).
- [PG-2] High-signal changes only. Don't restructure CANVAS_MODE.md beyond what's needed for the two new contracts. Size delta must be justified by content, not padding.
- [PG-3] When updating SKILL.md's "review topics" sentence, keep SKILL.md ≤ ~5 paragraphs (current shape). Contract details belong in CANVAS_MODE.md; SKILL.md gets the pointer + the headline shape (so chat-only callers get the contract self-sufficiently).
- [PG-4] Calibrate emotional tone — low arousal, no urgency framing, no "MUST always". Use "When X, do Y" decision-rule shape for non-invariant guidance.

## 5. Known Assumptions

- [ASM-1] (auto) The chosen progressive-disclosure primitive is native `<details>`/`<summary>`. Default: chosen. Impact if wrong: if a different primitive is preferred (e.g. button-toggled div with JS), the rendering rule needs swap. Low risk — `<details>` is zero-dep, accessible, persists naturally; it's the obvious fit.
- [ASM-2] (auto) Headline shape is "one concrete framing line + one recommended-call line, each a single declarative sentence with no nested clauses and no embedded justification". Default: chosen (sentence-shape, no word cap). Impact if wrong: if user wants a strict word cap, add it post-hoc. Low risk — arbitrary limits is a PROMPTING anti-pattern; sentence-shape bites without a magic number.
- [ASM-3] (auto) Plugin version bump is minor (0.5.1 → 0.6.0). Default: minor. Impact if wrong: trivial re-bump. Reasoning: behavior change to an existing skill that meaningfully alters output.
- [ASM-4] (auto) READMEs likely do not need updating because they describe walk-pr at a high level, not topic rendering. Default: read each, edit only if a topic-rendering claim contradicts the new contract. Impact if wrong: a README stays accurate by accident or needs a one-line tweak.
- [ASM-5] (auto) Reader model phrasing: "the reviewer lives in the repo (knows modules, idioms, naming) but has zero context on this PR." Default: this exact phrasing. Impact if wrong: trivial reword.
- [ASM-6] (auto) Tests not applicable — markdown skill files have no automated unit test scaffold in this repo. Hook tests don't apply. Default: skip test addition. Impact if wrong: nothing automated could meaningfully verify prose-shape contracts beyond the prompt-reviewer gate.
- [ASM-7] (auto) Memento pattern not applicable — this is a single-pass markdown edit, not a multi-step state-accumulating workflow. PROMPTING.md memento default is silently dropped.
- [ASM-8] (auto) PROMPTING.md "Gotchas section" gate satisfied by CANVAS_MODE.md's existing "Anti-patterns" section (functionally equivalent — named failure modes grounded in real behavior). AC-1.4 adds the new entries there.
- [ASM-9] (auto) `<details>` accessibility is treated as a trade-off justification (T-1), not as a separately encoded AC. Default: rely on the native primitive's built-in accessibility (keyboard-operable, screen-reader-readable summary). Impact if wrong: if the user wants explicit accessibility ACs, add a verification.
- [ASM-10] (auto) The current-topic-only application of `<details>` (T-4) is the chosen composition. Prior topics keep their one-line preview (textarea content); future topics keep their dimmed title.
- [ASM-11] (auto) Only topic-level code excerpts (illustrative snippets inside probes / trade-offs) move behind expand. Sub-changeset diff hunks render in the in-focus card per existing rendering rule (T-5).
- [ASM-12] (auto) Visual composition between a `<details>`-collapsed topic body and adjacent sub-changeset diff hunks rendered in the in-focus card is left to the implementer's layout judgment. Default: prior CANVAS_MODE.md 'Rendering and layout adapt to the content' guidance governs. Impact if wrong: if a layout conflict appears in practice, surface a follow-up; not gated here.
- [ASM-13] (auto) Detail-body persistence reuses the existing 'expand/collapse state' Lifecycle bucket — no new localStorage keys introduced. Reasoning: native `<details>` open/close *is* expand/collapse state by natural reading; reusing the existing bucket avoids key-collision risk and keeps the Lifecycle wording untouched. Impact if wrong: if a separate persistence channel is needed, introduce a scoped prefix as a follow-up.
- [ASM-14] Amendment from /do (pass 4) — INV-G2 carve-out for intentional contract duplication. The original "no MEDIUM+" threshold conflicted with AC-2.3's mandatory chat-only self-sufficiency: T-3 chose surface-touch (SKILL.md carries the full headline-shape contract so chat-only callers, who never load CANVAS_MODE.md, get it self-sufficiently). The prompt-reviewer kept flagging the resulting duplication as MEDIUM with its own NEEDS_USER_INPUT conditional ("if SKILL.md must stand alone, duplication is justified"). The carve-out documents that AC-2.3 supplies the "yes" and instructs the reviewer to check sync rather than re-flag the duplication. Impact if wrong: if a future amendment removes AC-2.3, the carve-out becomes overly permissive and should be revisited.

## 6. Deliverables

### Deliverable 1: CANVAS_MODE.md — reader model + topic shape + progressive disclosure

**Acceptance Criteria:**
- [AC-1.1] CANVAS_MODE.md contains a named **Reader model** that establishes the reviewer as codebase-fluent (knows modules, idioms, naming) but PR-context-zero.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS if a section or named statement establishes the reviewer reader model — codebase-fluent (modules/idioms/naming known) but zero PR context. FAIL if no such reader model is named, or if it's a generic 'expert reviewer' framing without the codebase-fluent / PR-context-zero distinction."
  ```

- [AC-1.2] CANVAS_MODE.md contains a **topic shape** contract: each topic's *visible headline* is (a) a one-line concrete framing of the concern in codebase vocabulary, (b) a one-line recommended call, (c) each line is a single declarative sentence — no nested clauses, no embedded justification, no narrated reasoning, no invented abstractions in place of codebase vocabulary.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if the topic-shape contract names all of: (1) one-line concrete framing in codebase vocabulary, (2) one-line recommended call, (3) single declarative sentence per line — no nested clauses, no embedded justification, (4) explicit prohibition on narrated reasoning / preamble / restated context in the headline. FAIL if any of those four is missing or if the shape is left to LLM discretion as 'short statement' / 'concise'."
  ```

- [AC-1.3] CANVAS_MODE.md contains a **progressive-disclosure rendering rule**: the in-focus topic's headline (per AC-1.2) is visible by default; supporting detail (rationale, topic-level code excerpts, alternatives, trade-off depth) lives in a collapsible body that is **closed by default**. Open/closed state persists across reloads via the existing 'expand/collapse state' Lifecycle bucket (no new localStorage keys introduced — native `<details>` open/close *is* expand/collapse state). The rule applies only to the *current* topic's body — prior topics keep their existing one-line preview, future topics keep their dimmed title. Sub-changeset diff hunks render in the in-focus card per the existing 'Rendering and layout adapt to the content' rule (not behind expand).
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if the rendering rule names all of: (1) headline visible by default, (2) supporting detail (rationale, code excerpts, alternatives, trade-off depth) lives in a collapsible body, (3) body closed by default, (4) open/closed state persists across reloads (reusing the existing 'expand/collapse state' Lifecycle bucket — no new localStorage keys), (5) the rule applies only to the *current* topic's body (prior/future topics keep existing rationing), (6) sub-changeset diff hunks are NOT moved behind expand — they continue rendering in the in-focus card per existing rendering-adapts rule. FAIL with the missing point if any are absent."
  ```

- [AC-1.4] CANVAS_MODE.md Anti-patterns section gains entries explicitly naming the per-topic density failures: (a) narrated reasoning in the visible headline; (b) headline that restates the body; (c) detail dumped in the headline instead of the collapsible body; (d) invented abstraction in place of codebase vocabulary. The section also includes **one good/bad headline contrast example** so "narrated reasoning" has a concrete anchor.
  ```yaml
  verify:
    method: codebase
    prompt: "Read the Anti-patterns section of claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md. PASS only if (1) all four anti-patterns appear (named or paraphrased recognizably): narrated reasoning in headline, headline restates body, detail in headline instead of collapsible body, invented abstraction vs codebase vocabulary; AND (2) at least one good/bad headline contrast example is embedded. FAIL listing any missing element."
  ```

- [AC-1.5] The new content composes with existing CANVAS_MODE.md sections — Cognitive-load contract, Interaction model, Rendering and layout adapt to the content, Lifecycle (auto-reload preserves state across reloads), and Failure handling — without contradiction. The detail-body open/closed state must persist across auto-reload — either because the existing "expand/collapse state" bucket naturally subsumes `<details>` open/closed (acceptable; explicit re-listing not required) or by explicitly extending Lifecycle's preserved-state list.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/references/CANVAS_MODE.md end-to-end. The new reader model, topic shape, and progressive-disclosure rule should compose with — not contradict — these existing sections: 'Cognitive-load contract' (one sub-changeset / one topic in focus), 'Interaction model' (one-shot generation, persisted textareas), 'Rendering and layout adapt to the content' (layout matches change shape, diff hunks render in in-focus card with syntax highlighting), 'Lifecycle' (auto-reload preserves scroll / expand-collapse / textareas), and 'Failure handling' (non-blocking). Specifically check: (a) detail-body open/closed state survives auto-reload — either via the existing 'expand/collapse state' preservation OR via an explicit Lifecycle addition (either is acceptable, but it must be unambiguous which path the document takes); (b) the new rendering rule does NOT say sub-changeset diff hunks go behind expand; (c) the rule applies only to the in-focus topic, not prior or future. Report any contradiction, ambiguity, or place where two rules tell the LLM to do conflicting things. PASS if internally consistent; FAIL with the conflict cited."
  ```

### Deliverable 2: SKILL.md — surface pointer to the topic shape

**Acceptance Criteria:**
- [AC-2.1] The "state the topic, recommend a call" sentence in SKILL.md is updated to name the topic shape — one-line concrete framing in codebase vocabulary + one-line recommended call, single declarative sentences, no narrated reasoning — so the contract is visible at the SKILL.md surface for both chat-only and canvas modes.
  ```yaml
  verify:
    method: codebase
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md. PASS if the topic-presentation guidance (currently 'state the topic, recommend a call, wait for the user's response') now names the headline shape — one-line concrete framing in codebase vocabulary + one-line recommended call, single declarative sentences, no narrated reasoning. FAIL if the SKILL.md surface text is unchanged or only references the canvas-mode contract by pointer."
  ```

- [AC-2.2] SKILL.md remains tight — no more than ~12 added non-blank lines vs origin/main. Cap accommodates the self-sufficient headline-shape statement required by AC-2.1 / AC-2.3 (chat-only callers need the full contract here, since they never load CANVAS_MODE.md) while still preventing SKILL.md from absorbing the full rendering rule (which belongs in CANVAS_MODE.md).
  ```yaml
  verify:
    method: bash
    command: "test $(git diff origin/main -- claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md | awk '/^\\+/ && !/^\\+\\+\\+/ && !/^\\+[[:space:]]*$/' | wc -l) -le 12"
  ```

- [AC-2.3] The SKILL.md headline-shape statement is self-sufficient — a reader who only loads SKILL.md (chat-only walk-pr never loads CANVAS_MODE.md) gets the full headline contract without needing the references file. In chat-only mode, supporting detail still has a place to land (subsequent message / on-demand probe / textarea body) — the change must not erase rationale / code excerpts / alternatives from chat mode.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-tools/skills/walk-pr/SKILL.md as if it were the only file you had. PASS if (a) the topic headline shape (one framing line + one recommended-call line, single declarative sentences, codebase vocabulary, no narrated reasoning) is fully conveyed without needing to load references/CANVAS_MODE.md, AND (b) in chat-only mode (no canvas), it remains clear where supporting detail (rationale, code excerpts, alternatives) lives — whether in subsequent messages, on-demand probes, or otherwise — so the change doesn't silently delete that material from chat. FAIL citing which condition isn't met."
  ```

### Deliverable 3: Plugin version bump

**Acceptance Criteria:**
- [AC-3.1] `claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json` version bumped from 0.5.1 to 0.6.0.
  ```yaml
  verify:
    method: bash
    command: "grep -q '\"version\": \"0.6.0\"' claude-plugins/manifest-dev-tools/.claude-plugin/plugin.json"
  ```

### Deliverable 4: README sync

**Acceptance Criteria:**
- [AC-4.1] Topic-rendering claims in the three READMEs (`README.md` root, `claude-plugins/README.md`, `claude-plugins/manifest-dev-tools/README.md`) don't contradict the new contract. Cheap deterministic check: no surviving phrase describing the *old* density behavior (wall-of-text topics, inline rationale, no progressive disclosure). Default expected outcome: no edits needed — READMEs stay high-level per CLAUDE.md README Guidelines.
  ```yaml
  verify:
    method: bash
    command: "! grep -E -i 'wall[- ]of[- ]text|inline rationale|monolithic topic' README.md claude-plugins/README.md claude-plugins/manifest-dev-tools/README.md 2>/dev/null"
  ```
