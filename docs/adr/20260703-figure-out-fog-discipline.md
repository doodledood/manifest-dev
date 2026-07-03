# ADR: figure-out gains fog discipline; multi-session orchestration stays out of scope

## Status
Accepted

## Context

figure-out implements fog-clearing as behavior: crux-first parent-before-children ordering, emergent branches, a live rival set, one question per turn. But it had no vocabulary for the distinction between a question that is *sharp* — statable precisely now, even if unanswerable yet — and an area that is still *fog*: sensed to matter but not yet statable as a question. The gap surfaced in two places.

In the log, the entry shape's single `Open threads` field flattened sharp-but-unanswered questions together with dim not-yet-statable areas — and the log is the resume surface after compaction, where everything listed reads as pressable. In live sessions, an observed failure (2026-07-03): a dim area got prematurely decomposed into a sub-question tree — structure invented before the terrain was visible — which parent-before-children could not block because the manufactured decomposition created fake parents to walk.

Separately, ADR practice hit a friction: a decision that evolved while its PR was still open accumulated in-place amendments, and the Immutability rules ("Once Accepted, do not rewrite") read as if they applied from drafting, inviting supersede-chains for ADRs that had never merged.

## Decision

Adopt the fog-vs-sharp test — *a question is sharp when you can state it precisely now, regardless of whether you can answer it* — in two placements:

- **`SKILL.md`** (behavior): some branches are fog — areas you sense matter but can't yet state as a question. Don't force a question shape onto them or slice them into subtrees; sharpen them first: resolve the parent, or gather the evidence that makes them statable.
- **`references/LOG.md`** (serialization): the entry shape splits `Open threads` (sharp — statable precisely now, even if blocked) from `Fog` (not yet statable — don't pre-slice; a patch may resolve into several questions or none).

Clarify **`references/ADR_FORMAT.md`** Immutability: append-only discipline begins at publication (merge, or visibility outside the authoring branch). An ADR still on its own open branch is a draft — edit, amend, or delete it in place; no supersede-chains or stacked amendment ADRs for unmerged decisions. Line 56's trigger is unified to "Accepted and published."

`references/autonomous.md`'s loose uses of "fog" (any unclearable unknown, including calls that need the user) are reworded to "unknown"/"question", reserving the term for this taxonomy — under it, a user-preference call is a sharp question, not fog.

## Alternatives Considered

- **Multi-session orchestration machinery** (a persistent shared map of typed investigation tickets with blocking edges, per-session claiming, and a visible frontier, worked one ticket per session): Rejected — figure-out's operating shape is one serial session with subagent fan-out; tracker mechanics are dead weight inside a single-thread discipline. A fog-clearing engine needs fog marked in its save file, not its engine.
- **A separate orchestration skill above figure-out**: Deferred, not rejected on merits — no genuinely multi-session, parallel-worker effort exists to justify it; revisit if one appears.
- **LOG.md-only placement (no SKILL.md line)**: Initially preferred on the "no gap in live-conversation behavior" theory — overturned by the observed live-session premature-decomposition failure, exactly the evidence bar that placement had named as its own overturn condition.
- **Take nothing**: Rejected — the flattened `Open threads` field is a real resume-time gap, and the crux-selection rule silently assumes threads are already sharp.

## Consequences

### Positive
- The log distinguishes what a resumed session can press now from what needs sharpening first; the don't-pre-slice corollary blocks premature decomposition both live and at resume.
- ADR drafting stops generating supersede-noise for decisions still evolving on their own branch.
- figure-out stays lean; no tracker machinery added.

### Negative
- Genuinely multi-session, parallel-worker investigations remain uncovered until a separate orchestration skill is justified.
- One more field in the log entry shape; sessions must judge sharp-vs-fog rather than dumping both in one list (the test sentence carries that judgment).

## Source
- Session: figure-out session (2026-07-03), operator-confirmed observed failure; landed with the edits in this PR.
- Related: 20260611-figure-out-spine-owns-epistemics-mode-refs-thin
