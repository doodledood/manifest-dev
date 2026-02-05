---
name: harden-task-file
description: 'Harden /define task guidance files for one-shot quality. Iterates: orthogonality gap analysis, user-approved additions, prompt review, fix, converge. Use when a task file needs comprehensive coverage or "harden task file".'
user-invocable: true
---

**User request**: $ARGUMENTS

Systematically harden a /define task guidance file until manifests built from it produce deliverables that don't need iteration.

If no arguments, ask which task file to harden.

## Context

Task files live in `claude-plugins/manifest-dev/skills/define/tasks/` and supplement the /define interview with domain-specific guidance:

- **Quality Gates** — Verifiable output properties. Can split into baselines (always enforced) and selectable (meaningful rigor choices)
- **Risks** — Process failure modes with probe questions
- **Scenario Prompts** — Pre-mortem fuel: "imagine this deliverable was rejected — what went wrong?"
- **Trade-offs** — Competing tensions the user resolves during the interview

New items must match the depth and structural conventions of the parent skill (`skills/define/SKILL.md`) and existing sibling task files.

## Goal

The task file should be comprehensive enough that a /define interview using it surfaces all criteria needed for one-shot quality. "One-shot" = the deliverable passes review without iteration.

## Log

Write findings to `/tmp/harden-{timestamp}.md` after each round. Read full log before each new round — prevents re-proposing rejected items and losing dimension context.

Per-round log structure:
```
## Round N
### Dimension Map
[dimension → items mapping]
### Gaps Found
[uncovered dimensions]
### Proposals
[item: accepted/rejected by user]
### Reviewer Findings
[finding: agree/disagree, applied/skipped]
```

## Orthogonality Analysis

The core discipline. Map every item in the file to a dimension — an independent axis of concern. A dimension is a top-level concern like "evidence quality" or "audience fit"; items are specific checks within a dimension like "source credibility" or "cross-referencing". Two items share a dimension if improving one naturally helps the other.

User validates the dimension map before gap-filling begins. Gaps = dimensions with no coverage.

Examples of dimension sources: deliverable lifecycle (creation → review → use → maintenance), rejection triggers, wrongness vs incompleteness, base-rate failures for this task class, user interaction points.

If the first analysis finds no gaps, invoke the reviewer once and exit if clean — not every task file needs hardening.

## Iteration Loop

Each iteration achieves:
- **Gaps identified** via orthogonality analysis
- **Additions designed** — invoke the `prompt-engineering:prompt-engineering` skill before proposing changes
- **User-approved additions** applied (all additions via AskUserQuestion)
- **Quality validated** — invoke the `prompt-engineering:review-prompt` skill on the task file after applying changes
- **Reviewer findings evaluated critically** — not all are valid. Present assessment with rationale; user decides
- **Log updated** after each round

Converged when criteria in Convergence section met.

## Section Placement

Each item belongs in exactly one section:

| Section | What it checks | Test |
|---------|---------------|------|
| Quality Gate (baseline) | Output property that should always be true | Would omitting this ever be acceptable? No → baseline |
| Quality Gate (selectable) | Output property representing a meaningful rigor choice | Reasonable to skip for some tasks? Yes → selectable |
| Risk | Process failure mode during execution | About how the work was done, not the output? → risk |
| Scenario Prompt | Specific way the deliverable fails or gets rejected | "Imagine the reader rejected this because..." → scenario |
| Trade-off | Competing tension with no universal right answer | Both sides have legitimate merit? → trade-off |

A concern appears once, in its most natural section. When the same concern appears in multiple sections, keep the stronger version.

## Principles

| Principle | Enforcement |
|-----------|-------------|
| Orthogonality over volume | Cover all dimensions, not all possible items within a dimension |
| User approves all changes | Propose via AskUserQuestion, never auto-add |
| Critical reviewer evaluation | Evaluate each finding independently — push back with rationale when wrong. When reviewer suggests items in already-covered dimensions, orthogonality wins |
| No redundancy across sections | Same concern in both risks and scenarios = pick one |
| Principles over thresholds | "Corroborated across independent sources" not "verified across 2+ sources" |
| No capability instructions | Don't prescribe verification methods — parent skill handles that |
| Match complexity to domain | Not every task file needs 17 quality gates — match depth to the diversity of ways the deliverable can fail |

## Never

- Auto-add items without user approval
- Blindly apply all reviewer suggestions
- Add arbitrary numerical thresholds
- Prescribe verification methods (parent skill handles this)
- Re-propose items the user already rejected (check log)

## Convergence

Done when:
- Orthogonality analysis finds no new uncovered dimensions
- Prompt reviewer finds no high-severity issues
- User confirms satisfaction
