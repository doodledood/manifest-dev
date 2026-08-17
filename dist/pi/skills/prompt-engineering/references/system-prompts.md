# System prompts

For a prompt that ships in a deployment loop — sitting in front of every turn of a production assistant or agent. The gap it closes is the whole posture: who the model is, what it is trying to do, how it stops, what it refuses, what its output looks like.

The blocks at the bottom are written for that artifact. They are prose to adapt into a deployment prompt, and dropping them into a skill is how a skill becomes long.

## Sections

For a single-purpose prompt with one role and one goal, this frame is useful. Multi-phase work organizes by phase instead — but each applicable section should still be answerable on a read.

| Section | What goes here |
|---------|----------------|
| **Role** | Identity and stance — who the model is, what it is responsible for. A sentence or two. |
| **Personality** | Voice, tone, formality, directness. User-facing surfaces only; skip it for workers, pipelines, and extraction. |
| **Goal** | The user-visible outcome. The destination, not the path. |
| **Success criteria** | What must be true before the final answer — including the degradation paths: when to **retry** (transient failure), **fall back** (another method), **abstain** (refuse, with the reason), **ask** (for the smallest missing field). Naming all four is what prevents silent loops and silent guessing. |
| **Constraints** | What holds throughout — policy, safety, evidence, side-effect limits. Mark priority when several non-invariant rules apply. |
| **Output** | Format, length, audience, structure — specified only where it changes behaviour. |
| **Stop rules** | When to stop gathering and answer with what you have. |

Three of those are routinely conflated. For a retrieval agent: success is *the answer addresses every part of the question*; a constraint is *ground every factual claim in retrieved content*; a stop rule is *when one more search would not change the answer, write*. Conflating success with stop gives over-search or premature answers; conflating constraints with success buries the target inside hard rules.

Constraints bound the path, not the destination — *don't fail to answer* restates the goal negatively and bounds nothing. The test: would it still apply if the goal changed?

Add a section only where its gap is real. A simple prompt with one goal and no edge cases may be a role and a goal sentence and nothing else.

## Blocks

Adapt these; do not paste them. Each closes a gap that appears in deployment loops.

**A verification pass before an irreversible step** — for a prompt driving commits, deletes, deploys, or evidence-grounded output where a requirement miss would do real damage:

```
Before any final answer or irreversible step, check: does the output cover what
was asked? Are factual claims grounded in tool output or supplied context rather
than memory? Does the format match what was requested? If the next action has
external consequences, state the action and its parameters and wait for confirmation.

If a check fails, revise before continuing.
```

**Narrate, execute, confirm** — for an agent mutating external state with each call, where un-narrated actions cannot be recovered:

```
Treat every state-changing call as narrate → execute → confirm. Narrate what you
are about to do and with what inputs; confirm the outcome and what you checked.
```

**A tool-call budget** — for search and retrieval loops that over-tool or under-tool depending on phrasing:

```
Default to the smallest number of searches that answers the question. Search again
when the results do not answer it, a required fact is missing, the user asked for
comparison or exhaustive coverage, or a named artifact must be opened. Otherwise
answer.
```

**An output contract** — where the consumer has real needs and *produce a good answer* yields walls of text. Name the audience and what they already know, the length envelope, and the ordering (conclusion first, caveats last). For editing tasks, state the preservation posture: keep the original's length, structure and voice; improve clarity and correctness; add no new claims or sections.

**Ambiguity handling** — where free-form input may be underspecified and silently picking one reading is the worst outcome:

```
When the request is ambiguous: ask the one or two precise questions that resolve it,
when the missing information would change the answer or the action. Otherwise state
the most likely reading with its assumptions labelled, and answer that.

When facts may have changed and no tool can check, answer in general terms and say
so. Invent no figures, dates, or sources.
```

**A high-risk self-check** — for legal, financial, medical, compliance or safety contexts, where an overstated claim causes real harm. Scan the draft for numbers not grounded in the provided context, assumptions the reader may not share, and absolute language; qualify them, state the assumptions, and replace an ungrounded claim with what would need to be checked.
