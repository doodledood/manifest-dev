# ADR: define reviews each new Manifest in a fresh context before the digest

## Status
Accepted — amended by 20261019-define-searches-each-new-manifest-for-a-wrong-result-that-passes-every-gate: the review also searches the whole Manifest for wrong results that pass every gate at once, by judgment, and the digest names the holes found. Further amended by 20261025-define-manifests-read-as-current-state-and-every-amendment-is-reviewed: amendments now get the review too, with a shorter scope, and every Manifest reads as current state

## Area
define

## Decided by
The user

## Context
`/define`'s own rules already forbid the failures users kept meeting: a specific with no source ("not a number made up to look measurable"), gates that cannot hold together, and a reread of every gate body before handoff. They still slipped through. One user asked in figure-out for a renderer to be "fast"; `/define` bound a fixed FPS number nobody had checked, and `/do` chased it. The context that writes the gates also rereads them, and it reads them as it meant them: it knows the number was a guess, while `/do` reads it cold as a requirement. The digest the user approves shows no gate text, so nobody else read the bound value before execution. The user ran fresh-context reviews of their Manifests by hand — handing the Manifest, `/define`'s instructions, the figure-out log and the transcript to a new context — and those reviews caught invented or too-strict targets, conflicting gates, and points from the session the Manifest dropped. `20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass` had already found that a same-context self-critique shares the converged frame.

## Decision
Every new Manifest gets one review in a fresh context before the digest, attended or unattended. The fresh context is handed the Manifest, `/define`'s rules (its `SKILL.md`, the schema, the task files the session loaded, the project context file and any Taste entries) and the session record (the figure-out log, and the transcript where the host keeps one it can read, else the conversation verbatim). Its brief, `define/references/REVIEW.md`, points it at those rules as the standard and restates none of them: it adds only what the rules lack — read the Manifest cold, as `/do` will; compare it with the session for settled points dropped, weakened or changed; weigh most the rules an author's reread misses, named by where they live; and report each finding with the gate, the conflicting source and the fix. It reports findings and never edits; a fix never adds a number the session did not give. The author settles every finding in one pass and names each rejected one with its reason. A fix that changes what the user agreed is the user's call: asked when attended; unattended, not applied, and recorded. Where no isolated context is available, the author reviews against the brief and says the review was self-graded. The digest also lists every number a gate binds, so the user can veto one before execution. Amendments get no review.

## Alternatives Considered
- **Strengthen the inline rules again**: another sharpening of the sourcing and hold-together bullets — Not chosen: the rules are already stated and were hill-climbed; the failure is self-grading, which more text in the same context does not reach.
- **Review only attended sessions**: save the extra context when no one is present — Not chosen: unattended runs are where no person reads the Manifest before `/do` holds the work to it.
- **Review amendments too**: — Deferred: amendments have not shown the failure; the review can extend to them if they do.
- **A brief that lists the rules to check**: — Not chosen: a list restating `/define`'s rules drifts from them; a first draft lost two rules' exceptions and would have flagged correct gates. The user ruled that the reviewer reads the skill itself.
- **Let the reviewer edit the Manifest**: — Not chosen: the author holds the conversation and the user's calls, and a reviewer that edits can make gates stricter unseen.
- **A loop until the review is clean**: — Not chosen: a run that keeps verifying past the point it is satisfied is a defect, and one pass caught the failures in manual use.

## Consequences

### Positive
- Invented numbers, dropped points and conflicting gates are caught by a reader who meets the Manifest the way `/do` will.
- The user sees every bound number before execution.

### Negative
- Each new Manifest costs one more fresh context.
- A thin or unusual Manifest can draw many findings, which the author must triage.

## Enforced by
partly — `tests/test_skill_frontmatter.py` keeps the review's wording host-neutral; whether `/define` runs it and settles its findings is judgment, checked by the `define` recipe's `fresh-review` scenario and the define eval case `d25-vague-target`.

## Source
- Session: figure-out read and define run on 2026-10-18, with the user's manual reviews as evidence
- Related: 20260606-harden-figure-out-truth-seeking-inline-defer-independent-pass, 20261018-a-target-of-unknown-reach-binds-a-floor-and-advises-an-aim, 20261018-do-names-the-evidence-that-puts-a-gate-out-of-reach
