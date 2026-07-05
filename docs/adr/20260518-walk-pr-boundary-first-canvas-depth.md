# ADR: Walk-PR depth becomes boundary-first, diff as evidence

## Status
Accepted

## Context

Walk-PR's `--canvas` mode produces a sub-changeset-by-sub-changeset, topic-by-topic review surface. Its initial design centered on **verbatim quotes from both sides, never paraphrased** — diff hunks were the canonical depth, "survived/cut/moved" prose summarized the line-level mapping, and topics often framed concerns at the level of specific lines or hunks.

Field experience on a moderately complex but not large PR (37 files, +869 / −154, 5 sub-changesets, 9 topics) surfaced a consistent failure mode: even with the previous round of tightening (per-topic progressive disclosure and the topic-shape contract), a reviewer with codebase fluency but zero PR-specific context experienced the canvas as an immediate wall of low-level detail with nothing to orient them first.

Two layered causes:

1. **No orientation above the SCs.** The canvas dropped the reviewer straight from a categorized overview (a table of SC names + sizes + classes) into SC1's prose grounding + diff hunks + topics. New PR-specific vocabulary — freshly introduced type and function names, plus a subtle behavioral distinction the PR added — was used without being introduced. Codebase fluency ≠ PR fluency, and the existing reader-model didn't separate them.

2. **Depth forced at line level.** Once inside an SC, the diff was the canonical depth and the "survived/cut/moved" prose listed every type, file, and call site by name. A reviewer who wanted to verify "this PR makes sense and doesn't break things" had no path short of parsing every hunk and engaging every topic. The skill mistook *one mode of review* (deep, topic-by-topic) for the *only mode*.

## Decision

Walk-PR canvas adopts a **three-layer model** with explicit orientation, depth-on-demand, and boundary-first depth content.

**Layer 1 — PR primer (above the SCs, before the categorized overview).** Conditional slots, workflow-level vocabulary. Always present: a one-paragraph problem statement in user terms, not codebase identifiers. Conditional: a glossary of PR-introduced concepts (workflow-level definitions, never type signatures); a mermaid sketch when component flow is at stake; a one-sentence reading hint when SCs differ in importance. Empty slots are skipped. Goal: a reviewer leaves the primer knowing what to expect when they hit new terms downstream.

**Layer 2 — per-SC card surface (always visible).** A one-sentence behavior summary in user terms and a one-sentence verification probe (concrete, observable). Everything else — prose grounding, boundary view, diff hunks, topics — collapses behind a single per-SC expand. A reviewer skims top-to-bottom in minutes and clicks into only the SCs that warrant depth.

**Layer 3 — inside the expand: boundary view, diff as evidence.** The expanded body opens with a **boundary view** describing the change at module-boundary altitude — new/changed types and what they represent, signatures at module edges, dependency-edge shifts, contract changes — in ≤3 short paragraphs, freeform, load-bearing pieces only. Diff hunks become per-file "show diff" affordances — one more click, on-demand. Topics retain their existing two-declarative-sentence shape; most topics on the field-experience PR were already boundary-level, so the contract holds.

**Reader-model addendum.** Codebase-fluent still holds. New clause: vocabulary introduced by *this PR* is not shared ground. The primer is the only place that vocabulary gets introduced; downstream SC summaries, boundary views, and topics use it without re-explanation.

**Cross-mode parity.** SKILL.md (chat-only walk) and CANVAS_MODE.md (canvas walk) both carry the orientation and depth contracts. Canvas-specific mechanics (per-SC `<details>` expand, per-file diff affordance, copy-as-prompt bundle) stay in CANVAS_MODE.md.

## Alternatives Considered

- **Status quo: diff-centric depth with topic-shape tightening only.** Lean on prompt discipline to keep topics off line-level edge cases; leave diff and "survived/cut/moved" as the canonical depth. Rejected because the wall-of-detail failure survives even with disciplined topics — the prose grounding and the diff itself remain the things the reviewer hits first. A prior iteration tried a softer version of this (per-topic progressive disclosure) and the failure mode persisted in the field.

- **Boundary translation above diff (additive).** Add a boundary-mapping block at the top of each SC expand, but keep diff hunks and "survived/cut/moved" prose below as canonical depth. Rejected because the expand still holds everything — the wall of detail moves but doesn't shrink. The reviewer still scrolls past walls of low-level content after engaging the boundary view; the architecture stays diff-centric in practice.

- **Rigid facet-structured boundary view.** Four named subsections inside the expand — Types, Signatures, Dependencies, Contracts — each rendered conditionally. Rejected: rigid structure is scaffolding the LLM doesn't need if the goal is clear, and small PRs end up with empty named headers. Goal-statement-over-structure is honest to how the rest of CANVAS_MODE.md works.

- **Mode toggle (`--brief` / `--deep`).** Add a flag that switches between behavior-only and full-depth canvases. Rejected because the right answer is a single layered canvas where the reviewer chooses depth per-SC, not per-canvas. A mode toggle forces a commitment up front; per-SC expand makes the commitment local.

## Consequences

### Positive

- A reviewer with codebase fluency but zero PR context can do a behavior-level pass in minutes and dig into specific SCs as needed. The skim path that didn't exist before now exists by default.
- The primer creates a single place where PR-introduced vocabulary gets defined — downstream SC content can use those terms without re-explanation, eliminating the "new term used cold" failure mode.
- Boundary-first depth matches how senior reviewers actually engage with architectural change. Walk-PR stops asking the reviewer to recover the boundary view from the diff in their head.
- The diff doesn't disappear — it's one click per file. Reviewers who want verbatim ground truth still have it. The skill's previous "verbatim quotes" promise becomes "verbatim quotes, on demand" rather than "verbatim quotes, by default."

### Negative

- Boundary-first depth is **paraphrase by definition**. The LLM's boundary summary can gloss a subtle behavior shift the diff would have shown (e.g., a null-to-undefined call-site contract change that the boundary view might not foreground). Mitigation: subtle line-level concerns surface as topics with anchors; the per-file diff affordance is one click away when needed.
- The skill's stated value pitch shifts: "verbatim quotes from both sides, never paraphrased" gives ground to "boundary view, diff one click deep." Consumers who came to walk-pr for the verbatim-quote frame need to recalibrate.
- More structural layers means a more complex contract. Mitigation: each layer is goal-stated rather than rigidly templated, so the contract stays tight even as it adds layers.
- Activation logic ("when does the primer include a sketch? when does the boundary view collapse to direct diff?") is left to LLM judgment with goal-statement framing rather than rigid triggers. Some PRs may land with the wrong depth chosen; corrections will be by re-running, not by config.

## Source

- Prior iteration: per-topic progressive disclosure and the topic-shape contract; this ADR builds on that work.
- Related: first ADR for the manifest-dev repo.
