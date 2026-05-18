---
name: walk-pr
description: 'Walk through a PR or large diff together — your own or someone else''s — one sub-changeset at a time and one review topic at a time within it. PR primer orients first; per-SC behavior summary + verification probe surface what changes and how to verify; boundary view explains the structural shift, with diff as per-file on-demand evidence. At the end, present a plan of the comments captured during the walk; on approval, post them as a PR review. Optional --canvas runs the walk in a live HTML artifact that replaces chat as the review surface. Use when reviewing a substantive PR collaboratively or walking a large refactor. Triggers: walk pr, walk diff, walk me through, pr walkthrough, review collaboratively, review this change with me.'
argument-hint: '[pr-url-or-range] [--canvas]'
user-invocable: true
---

Walk the user through a PR or large diff **one sub-changeset at a time** — a group of files that makes sense together — and **one review topic at a time within it**.

**Reader model.** The reviewer lives in the repo but has zero context on *this PR*. Codebase vocabulary is shared ground; **vocabulary the PR introduces is not** — new types, modes, modules, domain terms need explicit introduction before downstream content uses them.

**Open with orientation.** Present a **PR primer** before the change overview: a one-paragraph problem statement in workflow vocabulary, plus — only when load-bearing — a concept glossary (workflow-level definitions, not type signatures), a component sketch, or a reading hint. Then a categorized overview (load-bearing vs scaffolding/data, biggest-signal-first); skip both on trivial diffs.

**Per sub-changeset, depth on demand.** The always-visible surface per SC is a one-sentence **behavior summary** (what changes for the user) and a one-sentence **verification probe** (how to observe it works). Everything else — boundary view, topics, diff — is depth the reviewer expands only on SCs that need it.

**Inside the depth — boundary-first.** Open with a **boundary view**: ≤3 short paragraphs at module-boundary altitude — new/changed types, signatures at module edges, dependency-edge shifts, contract changes — load-bearing pieces only, no inventory. Diff hunks are **per-file, on-demand** evidence, not the default exposition. Then topics.

**Topic shape.** Surface review topics (probes, trade-offs, recommendations) **one at a time**. Each topic = two declarative sentences: a concrete framing of the concern in codebase vocabulary, then the recommended call. No nested clauses, no embedded justification, no narrated reasoning. Put rationale, code excerpts, and alternatives in supporting material (a follow-up message or on-demand probe), not the headline. Wait for the user's response before advancing. Don't batch — "thoughts on all of these?" is the failure mode this skill prevents. Hold positions under pushback when evidence still supports them.

**Post at end.** Capture the user's response per topic. When the walk completes, present a plan of the captured comments — line-anchored where the topic ties to a specific code location, file-level or PR-level otherwise — via `ExitPlanMode`. On approval, post them as a single PR review using available GitHub tools (`gh pr review` / `mcp__github__pull_request_review_write` / API). Whether and how the PR's author addresses the comments is the manifest workflow's job downstream, not /walk-pr's.

**`--canvas`.** Load `references/CANVAS_MODE.md`. The HTML artifact **replaces** chat as the walkthrough surface — primer, per-SC behavior + verify summaries, boundary views, topics, diff affordances, and per-topic comment textareas all live in the canvas, generated once upfront. The user navigates self-paced and hands the consolidated review result back to chat via a single end-of-walk handoff. **Input** = PR number, PR URL, diff range, or nothing (infer the current branch's PR; fall back to `origin/main..HEAD`).
