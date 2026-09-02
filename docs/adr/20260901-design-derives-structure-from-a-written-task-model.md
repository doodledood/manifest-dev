# ADR: The design skill derives structure from a written task model, and asks when the brief lacks one

## Status
Accepted — extended by 20260902-design-chooses-an-encoding-per-claim-figures-are-information-not-decoration: the task-model block gains a fifth line, *Encoding*, choosing per claim whether prose, a table, or a figure carries it; the four lines this record named, the trace rule, and the ask-once rule all stand.

## Area
Design skills

## Context

The `design` skill shipped with three named failure modes and a counter for each: styling effort landing on the wrong layer while the functional layer collapses, countered by the floors; stated principles not surviving into output, countered by external verification; and unforced style choices converging on the same few looks, countered by deriving distinctiveness from the subject.

Use surfaced a fourth. The skill produced artifacts that were well made and structurally wrong for the work they supported — a labeling tool that placed its questions below the task description, so the labeler had to scroll the thing being judged out of view to answer a question about it. The loop that tool exists to serve is *read the item → judge it → answer → next*, and it demands that the item and the question be visible at once. Nothing in the skill derived that.

None of the three counters reaches it. The skill's first decision named a purpose from four abstract metrics — Comprehension, Retention, Persuasion, Action — which selects what to optimize but says nothing about what the person does. Every decision after it governed presentation: register, tokens, floors. Task-loop reasoning appeared once, in the final verification decision's genre behavior probe, which is both too late and the wrong instrument: verification can reject a structure but cannot derive one, and that decision is skipped entirely at prototype weight. The skill also asked nothing, ever, so a brief that named an artifact and no work ("a page for labeling tasks") was filled in silently from habit.

Nor did the surrounding workflow compensate. `review-design`'s judged dimensions were register fit, floors, composition, craft, copy, and viewport, so the same defect passed the gate that exists to catch it, and the rendering flows invoke the skill at prototype weight where the only structural signal was skipped.

## Decision

The skill gains a task-model decision, placed between the purpose decision and the register decision, making six decisions where there were five. Four coupled choices:

1. **The model is a written artifact, not an intention.** The step's output is a declared block — who is at the artifact, the one loop they repeat, what must be co-visible at each step of that loop, and the rate the loop runs at — written before any layout and kept beside the token block. The skill's own second failure mode is that stated principles do not survive into output; a model held in mind is exactly such a principle, while a written block can be checked. The layout traces to the block region by region, and a region tracing to nothing is decoration or a missing model line, decided on the spot — the same call the skill already makes for a value outside the token system.

2. **Co-visibility is the line that decides structure, and it outranks familiarity.** Two things a loop step needs together cannot be a scroll apart, and this binds before register, aesthetics, or any conventional arrangement. When new evidence about the work arrives, the model line is what gets revised, never the layout that traced to it.

3. **An underspecified brief gets one bounded question; an unattended run writes the model down as an assumption.** Both branches are stated, because the skill runs in contexts with a user and in contexts without one — a gate evaluator, an unattended `/do`, a render made mid-deliberation. The rule that holds across both is that the model is never left unstated: an unstated model is the habit layout wearing the work's name.

4. **The step runs in full at prototype weight.** Structure is most of what a prototype is reacted to, and one in the wrong arrangement pulls the reaction onto the arrangement instead of onto the question the render was made to ask.

The sweep that follows: `review-design` names the loop as its own procedure step and judges task fit first among its dimensions — first because it is the one dimension whose repair restructures the artifact, so findings graded below it may be graded against an arrangement that will not survive — with a broken co-visibility pair grading HIGH and an uncompletable loop CRITICAL. `/define`'s UI task file names task fit in the gate's coverage and tells the manifest author to name the loop in the gate body where the manifest knows it. The by-hand fallbacks in `figure-out` and `just-figure-out`, for installs without the skill, carry the loop and co-visibility alongside the register and legibility they already carried.

## Alternatives Considered

- **Strengthen the verification decision instead**: add task fit to the critique criteria and sharpen the genre behavior probes, leaving the decision sequence untouched — not chosen because verification can only reject a structure, never derive one. A run that reaches verification with the wrong arrangement has already spent its effort styling it, and the repair is a restructure rather than a fix. The prototype path makes it worse: verification is skipped there entirely, so the defect would have no counter at all in exactly the mode the rendering flows use.
- **Supply the model from upstream — `figure-out` or `/define` — rather than inside the skill**: the understanding-first workflow already interviews the user, so the task model could ride in on the manifest — not chosen because `design` is a standalone skill invoked directly and from a prototype render mid-deliberation, and a shipped skill cannot defer a step it needs to a caller that may not exist. It would also reproduce the defect it fixes for every direct invocation, which is how the failure was found. The manifest still carries the loop where it knows it, as gate-body input to the evaluator, but that is an enrichment rather than the source.
- **Fold the model into the existing purpose decision**: keeps the decision count stable and touches less text — not chosen because the purpose decision's output is a single word chosen from a table, and burying a four-line model inside it hides the step whose absence caused the defect. A separately numbered decision is what makes skipping it visible.
- **Ship a task-model reference file loaded on trigger**: keeps `SKILL.md` short — not chosen because every invocation needs the model, so deferring it would put the always-needed step behind a load, which is the opposite of what progressive disclosure is for.

## Consequences

### Positive
- Structure is derived from the work before any presentation decision constrains it, and the derivation is written down where a later edit, a reviewer, and the evaluator can all check it.
- The skill now asks when it does not know, in the one place where an answer changes the artifact's shape, rather than never asking at all.
- The evaluator can catch structural misfit, so the defect has a counter at build time and at gate time rather than only in the author's reaction.
- Prototypes get the structural decision they are most judged on, at the weight where verification is deliberately absent.

### Negative
- Every invocation now pays for a step whose value is lowest on artifacts with no repeated loop — a poster, a one-screen marketing page — where the model collapses to a line or two and is written anyway.
- The trace rule is judgment, not mechanism: a run can write a model and then lay out from habit regardless, and only the evaluator would catch it.
- Deriving the loop from the artifact alone gives `review-design` a weaker basis than the author had, so a task-fit finding can be wrong in a way a contrast finding cannot; the skill is told to say so rather than convict on an invented loop.
- The effectiveness of the change rests on the same unmeasured ground as the skill itself — the blind pairwise eval named in `20260901-design-skill-pair-distills-research-eval-deferred` stays deferred, and a single behavioral probe on the brief that exposed the defect is evidence the instruction can work, not that it reliably does.

## Source
- Session: figure-out → define → do run, 2026-09-01, from the owner's report of repeated well-made-but-wrong artifacts across several standalone invocations.
- Related: 20260901-design-skill-pair-distills-research-eval-deferred (this adds a fourth failure mode and counter to the three that record's skill shipped with), 20260901-deliberation-renders-run-the-design-skill-at-prototype-weight (extended: a third decision now runs in full at prototype weight), 20260703-progressive-disclosure-triggers-live-in-loading-layer (why the step stays inline rather than becoming a reference).
