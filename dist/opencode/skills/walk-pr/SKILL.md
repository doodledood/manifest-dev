---
name: walk-pr
description: 'Walk through a PR or large diff together — your own or someone else''s — one sub-changeset at a time and one review topic at a time within it. Use when reviewing a substantive PR collaboratively, walking a large refactor, or when the user asks to walk a PR, walk a diff, explain a PR, review collaboratively, or review a change together. Optional --canvas runs the walk in a live HTML artifact.'
argument-hint: '[pr-url-or-range] [--canvas]'
user-invocable: true
---

Walk the user through a PR or large diff **one sub-changeset (SC) at a time** — a group of files that makes sense together — and **one review topic at a time within it**.

**Reader model.** The reviewer lives in the repo but has zero context on *this PR*. Codebase vocabulary is shared ground; **vocabulary the PR introduces is not** — new types, modes, modules, domain terms need explicit introduction before downstream content uses them.

**Attention contract.** Every mode of this skill serves the same contract: high-level orientation first, one idea active at a time, and depth — rationale, code, diffs, long text — only when the reviewer asks for it. In chat that is the one-SC/one-topic discipline below; in canvas it is a visual map with everything textual behind taps. Whenever a presentation choice arises, the failure to avoid is the text wall: never put more in front of the reviewer than the current idea needs.

**Open with orientation.** Present a **PR primer** before the change overview: a one-paragraph problem statement in workflow vocabulary, plus — only when load-bearing — a concept glossary (workflow-level definitions, not type signatures), a component sketch, or a reading hint. Then a categorized overview (load-bearing vs scaffolding/data, biggest-signal-first); skip both on trivial diffs.

**Per sub-changeset, depth on demand.** The always-visible surface per SC is a one-sentence **behavior summary** (what changes for the user) and a one-sentence **verification probe** (how to observe it works). Everything else — boundary view, topics, diff — is depth the reviewer expands only on SCs that need it.

**Inside the depth — boundary-first.** Open with a **boundary view**: ≤3 short paragraphs at module-boundary altitude — new/changed types, signatures at module edges, dependency-edge shifts, contract changes — load-bearing pieces only, no inventory. Diff hunks are **per-file, on-demand** evidence, not the default exposition. Then topics.

**Topic shape.** Surface review topics (probes, trade-offs, recommendations) **one at a time**. Each topic = two declarative sentences: a concrete framing of the concern in codebase vocabulary, then the recommended call. No nested clauses, no embedded justification, no narrated reasoning. Put rationale, code excerpts, and alternatives in supporting material (a follow-up message or on-demand probe), not the headline. Wait for the user's response before advancing. Don't batch — "thoughts on all of these?" is the failure mode this skill prevents. Hold positions under pushback when evidence still supports them.

**Triage, then post.** Capture the user's response per topic. When the walk completes, triage every captured item — topic responses and free notes alike — into three kinds: **settled calls** that become draft comments; **questions** the reviewer raised that you must answer first — from the code, the repo's ADRs, and any design doc the PR implements (fetch it; design-vs-implementation deviations are prime review material) — because investigation routinely flips or reshapes the would-be comment; and **drops** that generate nothing. Then confirm the proposed comments with the reviewer **one at a time** — a batched approval table recreates the overload the walk exists to prevent — each line-anchored where it ties to a specific code location, file-level or PR-level otherwise. Once all items lock, post them as a single PR review using the available GitHub review mechanism. Whether and how the PR's author addresses the comments is the manifest workflow's job downstream, not /walk-pr's.

**`--canvas`.** Load `references/CANVAS_MODE.md`. The HTML artifact **replaces** chat as the walkthrough surface — and it is a picture, not a document: one persistent system map of the PR with a stepped story, pinned review topics, comment-anywhere, and diffs in an on-demand drawer, generated once upfront and opened immediately. The user navigates self-paced and hands the consolidated review bundle back to chat, where the triage above takes over. **Input** = PR number, PR URL, diff range, or nothing (infer the current branch's PR; fall back to `origin/main..HEAD`).
