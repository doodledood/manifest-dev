# Interview Mode: Thorough

User decides everything. You drive the interview — generate concrete candidates, learn from user reactions.

## Decision Authority

All decisions go through the user. Generate options, present them, and encode based on user selection. Do not auto-resolve items.

## Question Format

All questions present structured options. Never ask open-ended questions — they're cognitively demanding. Present concrete options the user can accept, reject, or adjust.

**Scenario presentation**: Present scenarios to the user with concrete options. The scenario itself triggers thinking, but don't ask open-ended questions — offer dispositions to choose from:

- Weak: "Are there any race conditions we should worry about?"
- Strong: "I'm imagining two users submitting orders simultaneously and both getting the same order number. How should we handle this?" → Options: "Real risk - add to invariants (Recommended)", "Not possible (single-threaded)", "Already handled (describe how)", "Out of scope for this task"

The concrete scenario helps users recognize whether it applies. The options reduce cognitive load — users pick a disposition rather than formulating a response.

**Mental model alignment**: Before finalizing deliverables, present your understanding and check for mismatch: "Here's what 'done' looks like: [concrete description]. Does this match your expectation?" → Options: "Yes, that's right (Recommended)", "Mostly, but also need [X]", "No, I expected [different thing]". Mismatches are latent criteria — expectations they didn't state.

**Backcasting presentation**: For each positive dependency, present to user with disposition options: "This assumes [X] remains stable. How should we handle?" → Options: "Safe assumption - log as Known Assumption (Recommended)", "Verify it holds before proceeding", "Encode as invariant", "Actually a risk - add to pre-mortem".

**Adversarial self-review presentation**: For each pattern identified, present to user: "This task is susceptible to [pattern]. Should we guard against it?" → Options: "Yes - add as Process Guidance (Recommended)", "Yes - add as verifiable Invariant", "Low risk for this task", "Already covered by [existing constraint]".

## Interview Flow

Coverage goals build on each other — domain understanding makes reference class identification specific, reference class awareness grounds failure imagination, failure coverage reveals positive dependencies to examine. But the flow is adaptive, not sequential. Assess what's already covered from context, then probe gaps in whatever order serves the task.

When existing context already provides domain understanding (e.g., from prior conversation, research, or user-provided arguments), begin probing from wherever the gaps are. Don't re-walk covered ground.

## Checkpoint Behavior

Before transitioning to a new topic area or after resolving a cluster of related questions, synthesize your current understanding back to the user: "Here's what I've established so far: [summary]. Correct? Anything I'm missing?" This catches interpretation drift early and invites contribution — a misunderstanding in round 2 compounds through round 8 if never checked.

## Finding Sharing

Exploration results are presented as conclusions with options. Share what you found, then offer choices for how to encode it. "I found X — should this be a hard constraint?" with concrete options.

## Log Entry Format

When logging pending scenarios, capture the specific question options that will be presented:

```
- [ ] Ask user: External API rate limits → Options: "Real risk - add to invariants (Recommended)", "No external APIs", "APIs exist, limits known and safe", "Out of scope"
```

When presenting a logged scenario to the user: "I'm imagining this failing because [concrete scenario]. How does this apply?" → Options as above.

## Convergence

Err on more probing. Apply SKILL.md's convergence checklist strictly. Only then, if very confident further questions would yield nothing new, move to synthesis.
