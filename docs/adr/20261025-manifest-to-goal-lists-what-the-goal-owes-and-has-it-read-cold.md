# ADR: manifest-to-goal lists what the goal owes before drafting, and has the goal read cold

## Status
Accepted

## Area
Goal setting

## Decided by
The user, for adding a review, its shape (one fresh context, goal first) and the output (the bare fence, with a note only when needed). An agent under the user's delegation for this change ("take it from here and merge when done"), with no review, for the listing step and for dropping the prompt-engineering call.

## Context
manifest-to-goal turns a Manifest into a goal of at most 4,000 characters, and the goal replaces the Manifest: the agent that works from it never sees the Manifest, so a dropped obligation is gone and an invented one binds. The user saw both: goals that dropped or weakened conditions, and goals that invented or blurred requirements, most often on complex Manifests. The skill drafted straight from a full reading with no inventory of what it owed, so under the length cap conditions fell out unnoticed. It invoked prompt-engineering before drafting, whose pruning discipline is about writing prompts and pulls a compression toward cutting. Its bars were vague ("consequential thresholds", "quality bar", "derivable detail"). And the context that wrote the goal was the only one that checked it, so it read the goal as it meant it — the failure `20261018-define-reviews-each-new-manifest-in-a-fresh-context` found for Manifests.

## Decision
Before drafting, the skill writes down every Acceptance Criterion and Global Invariant with its pass condition, wherever in the gate it is stated, plus every scope limit, exclusion, stopping limit and approval boundary; that list is what the goal owes. Process Guidance and the Initial Approach advise and are carried only where a gate binds a method. When the list cannot fit, the skill asks which item to cut before drafting. After drafting and counting, one fresh context reads the goal alone first — what it would build, what limits it sets, how it would decide it is done — and then the Manifest and the user's amendments, deriving what the goal owes for itself and checking the author's list as a claim. It reports dropped or weakened obligations, inventions, revived scope, references to the Manifest, conditions it could not settle as done or not done where the Manifest settles them, and a plausible wrong result per gate that the gate itself would catch. The author settles every finding in one pass and counts the goal again; a fix that breaks the cap is a cut the user decides; no second review follows. The skill returns the bare fence, with one short note under it only when a finding was rejected or the review was self-graded.

## Alternatives Considered
- **Two fresh contexts, one per reading**: a cold reader that never sees the Manifest, and a separate comparer — Not chosen: the user chose one context to keep the cost of each conversion down; the goal-first order keeps the cold reading uncoloured by the Manifest.
- **A reviewer handed both texts at once**: — Not chosen: it cannot test whether the goal stands on its own, which is the property the goal exists for.
- **Stronger drafting rules alone**: — Not chosen: the old skill already said to check for lost obligations; the failure is self-grading, which more text in the same context does not reach.
- **A script that checks literal specifics survive**: — Not chosen: it catches dropped numbers but not weakened conditions, inventions or revived scope, and adds machinery to a one-file skill.
- **A fixed report beside the goal**: — Not chosen: the user pastes the fence into a goal field, so anything beyond the goal is noise unless it needs their attention.
- **A loop until the review is clean**: — Not chosen: one pass settles the findings, and a run that keeps verifying past that point is a defect.

## Consequences

### Positive
- Every pass condition, including one buried in a gate's why, has a line in the list the goal is checked against.
- A reader who meets the goal the way the working agent will checks it before the user pastes it.

### Negative
- Each conversion costs one more fresh context.
- Where no isolated context is available, the review is self-graded, and the note says so.

## Enforced by
partly — the `manifest-to-goal` recipe's `fresh-review` scenario drives the skill on a 28-gate Manifest whose pass conditions come close to the cap, with a buried threshold, an amendment and advisory steps; whether a run lists, reviews and settles findings stays judgment.

## Source
- Session: figure-out read and `/auto` run on 2026-10-25
- Related: 20261018-define-reviews-each-new-manifest-in-a-fresh-context
