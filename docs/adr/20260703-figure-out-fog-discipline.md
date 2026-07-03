# ADR: figure-out gains fog discipline; multi-session orchestration stays out of scope

## Status
Accepted

## Context

A comparison against an external, publicly available planning skill (fetched from its public source repository, 2026-07-03; self-labeled in-progress by its author) asked what figure-out should adopt. That skill plans work "more than one agent session can hold" as a shared map on an issue tracker — typed child tickets, blocking edges rendering a visible frontier, claim-by-assignee for concurrent sessions, one ticket per session — and keeps a "fog" section for questions not yet precisely statable. It delegates actual investigation to separate questioning/domain-modeling skills: it is an orchestration layer above a figure-out-class skill, not a rival investigation discipline.

figure-out already implements fog-clearing as behavior: crux-first parent-before-children ordering, emergent branches, a live rival set, one question per turn. What it lacked surfaced in two places. In the log, the entry shape's single `Open threads` field flattened sharp-but-unanswered questions together with dim not-yet-statable areas — and the log is the resume surface after compaction, where everything listed reads as pressable. In live sessions, an observed failure (2026-07-03): a dim area got prematurely decomposed into a sub-question tree — structure invented before the terrain was visible — which parent-before-children could not block because the manufactured decomposition created fake parents to walk.

Separately, ADR practice hit a friction: a decision that evolved while its PR was still open accumulated in-place amendments, and the Immutability rules ("Once Accepted, do not rewrite") read as if they applied from drafting, inviting supersede-chains for ADRs that had never merged.

## Decision

Import exactly one concept — the fog-vs-sharp test: *a question is sharp when you can state it precisely now, regardless of whether you can answer it* — in two placements:

- **`SKILL.md`** (behavior): some branches are fog — areas you sense matter but can't yet state as a question. Don't force a question shape onto them or slice them into subtrees; sharpen them first: resolve the parent, or gather the evidence that makes them statable.
- **`references/LOG.md`** (serialization): the entry shape splits `Open threads` (sharp — statable precisely now, even if blocked) from `Fog` (not yet statable — don't pre-slice; a patch may resolve into several questions or none).

Clarify **`references/ADR_FORMAT.md`** Immutability: append-only discipline begins at publication (merge, or visibility outside the authoring branch). An ADR still on its own open branch is a draft — edit, amend, or delete it in place; no supersede-chains or stacked amendment ADRs for unmerged decisions. Line 56's trigger is unified to "Accepted and published."

Reject the external skill's remainder — shared map, frontier, concurrency claiming, one-ticket-per-session, ticket types — as out of scope for figure-out.

## Alternatives Considered

- **Adopt an orchestration mode into figure-out**: Rejected — figure-out's operating shape is one serial session with subagent fan-out; tracker mechanics (claiming, session-sized tickets) are dead weight inside a single-thread discipline. A fog-clearing engine needs fog marked in its save file, not its engine.
- **Build a separate orchestration skill**: Deferred, not rejected on merits — no genuinely multi-session, parallel-worker effort exists to justify it; revisit if one appears.
- **LOG.md-only placement (no SKILL.md line)**: Initially preferred on the "no gap in live-conversation behavior" theory — overturned by the observed live-session premature-decomposition failure, exactly the evidence bar that placement had named as its own overturn condition.
- **Take nothing**: Rejected — the flattened `Open threads` field is a real resume-time gap, and the crux-selection rule silently assumes threads are already sharp.
- **Other elements of the external skill** (index-not-store, prototype tickets, refer-by-name, task tickets): already covered (`--scratch`, ADR conventions) or inapplicable (figure-out has no issue ids and does no execution work).

## Consequences

### Positive
- The log distinguishes what a resumed session can press now from what needs sharpening first; the don't-pre-slice corollary blocks premature decomposition both live and at resume.
- ADR drafting stops generating supersede-noise for decisions still evolving on their own branch.
- figure-out stays lean; no tracker machinery added.

### Negative
- Genuinely multi-session, parallel-worker investigations remain uncovered until a separate orchestration skill is justified.
- One more field in the log entry shape; sessions must judge sharp-vs-fog rather than dumping both in one list (the test sentence carries that judgment).

## Source
- Session: figure-out comparison session (2026-07-03), operator-confirmed observed failure; landed with the edits in this PR.
- Related: 20260611-figure-out-spine-owns-epistemics-mode-refs-thin
