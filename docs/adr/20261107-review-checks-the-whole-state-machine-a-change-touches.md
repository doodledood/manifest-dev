# ADR: Review rebuilds and checks the whole state machine a change touches

## Status
Accepted

## Area
Code review

## Decided by
The user decided that the check runs in review without anyone asking. Placing it in `code-bugs` first is the agent's recommendation, which the user accepted with the read that proposed it; the drive under *Revisit when* can overturn it.

## Context
A state-machine defect often lives between distant sites: a change edits one writer of a status, while the transition that reaches a bad state sits in another file. `code-bugs` already traces, for every value a diff writes or reads, who else writes and reads it (`review-code/references/code-bugs.md`, *Mechanism tracing* and *State Inconsistencies*). It does not rebuild the whole machine — every state, every event — or check it exhaustively. Today the state-machine checks are split across three dimensions: `code-bugs` (inconsistent state), `change-intent` (transition gaps against the intent) and `type-safety` (missing discriminants).

20261107-a-figure-out-wrapper-sweeps-existing-code-for-state-machines gives existing code an on-demand sweep. The owner wants what proves useful to run without anyone remembering it, so the same check also runs in review, which every coding Manifest's gates and every review-pr pass already reach.

The North Star asks that anything adding cost or wait to every run — another agent, a review pass — earn its place by a gain shown on evidence. 20261013-design-judgment-moves-to-design-time-as-task-file-probes keeps review dimensions as post-code gates for defects; a reachable bad state in written code is such a defect.

## Decision
- When a change writes or reads state that has a lifecycle, the defect-finding review rebuilds the whole machine across the repository — every state, every event and every writer, including code the change did not touch — and checks it, sized to the risk as the sweep is. A confirmed counterexample is the finding's stated trigger. It reports only what the change introduced or exposed, as review-code's scope rules say.
- The check lives in `code-bugs`, which owns reachable states and already reads the other writers, so no new reviewer runs on every change.
- The check text is the one the sweep uses. Transition gaps against the author's intent stay with `change-intent`; missing discriminants stay with `type-safety`.

## Alternatives Considered
- **A new conditional dimension for state machines**: not taken first — another reviewer on every change that touches lifecycle state, a per-run cost the North Star asks evidence for, while `code-bugs` already reads the other writers. It replaces the `code-bugs` placement if the drive shows `code-bugs` cannot carry the check.
- **No change to review, with the sweep on demand only**: rejected — new defects would enter between sweeps, and a person must remember to run one.
- **Model-check every change that touches state**: rejected — models written to satisfy a rule rather than to find a defect (20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks); the risk sets the depth.

## Consequences

### Positive
- Every coding Manifest's review and every review-pr pass meet state-machine defects a change introduces or exposes, with no new reviewer.
- One check text serves the sweep and the review.

### Negative
- `code-bugs` grows, and a broad reviewer may give the check less attention than a dedicated one would; the drive measures this.
- Reviews of changes that touch lifecycle state take longer where a model is built.

## Enforced by
not yet — a before-and-after drive of review-code's `code-bugs` on a diff that changes one writer of a status while another file makes a bad transition reachable.

## Revisit when
The before-and-after drive shows `code-bugs` misses the planted defect with the check in place (then a conditional dimension), or catches it without the check (then review needs no new text), read in that drive's evidence.

## Source
- Session: a figure-out session on whether six prompts for coding agents that the owner came across belong in manifest-dev's core (2026-11-07).
- Related: see also 20261107-a-figure-out-wrapper-sweeps-existing-code-for-state-machines, 20261013-design-judgment-moves-to-design-time-as-task-file-probes, 20261019-verification-asks-whether-a-check-can-reach-the-case-that-breaks
