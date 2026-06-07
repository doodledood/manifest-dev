# Writing a system prompt

A system prompt runs in a deployment loop — it sits in front of every turn for an assistant or agent in production. The gap it closes is *the entire posture* of the assistant: who it is, what it's trying to do, how it stops, what it refuses, what shape its output takes.

For a single-purpose system prompt with one Role and one Goal, the section template below is a useful frame. For multi-phase workflows, skills with subdomains, or instructional documents, organize by theme or phase instead — but every applicable section below should be answerable on a read.

## Section template

| Section | What goes here |
|---------|----------------|
| **Role** | Identity and stance — who the model is, what context it operates in, what it's responsible for. One or two sentences. |
| **Personality** | Voice, tone, formality, warmth, directness. Skip when the prompt is a worker, pipeline, transformation, extraction, or any non-user-facing task. Personality is for user-facing surfaces only. |
| **Goal** | The user-visible outcome the run produces. State the destination, not the path. |
| **Success criteria** | What must be true before the final answer. Include the **degradation paths** — when to **retry** (transient failure), **fallback** (alternative method), **abstain** (refuse with reason), **ask** (for the smallest missing field). Naming the four prevents silent loops and silent guessing. |
| **Constraints** | Rules that must hold throughout the run — policy, safety, business, evidence, side-effect limits. Reserve absolutes (MUST / NEVER) for true invariants; for judgment calls, use decision rules (`see patterns.md`). When multiple non-invariant rules apply, mark priority (MUST > SHOULD > PREFER). |
| **Output** | Format, length, audience, structure. Be specific only where it changes behavior — don't over-prescribe shape the model already gets right from Goal. |
| **Stop rules** | Loop control: when to stop pursuing more information and answer with what you have. Distinct from Success (target state) and degradation (non-success behavior). |

## Success vs Constraints vs Stop rules

Three different jobs that authors frequently conflate. For a retrieval agent:

- **Success criteria**: *"answer addresses every part of the asked question"* — the target state.
- **Constraints**: *"ground every factual claim in retrieved content; never invent citations"* — rules that hold throughout.
- **Stop rules**: *"when one more search would not change the answer, write"* — the loop-exit rule.

Conflating Success and Stop → over-search or premature stop. Conflating Constraints and Success → target buried inside hard rules. Conflating Constraints and Stop → permanent rule turned into a one-shot exit.

Constraints bound the path, not the destination. *"Don't fail to answer"* just restates the goal negatively — adds no boundary. Test for a real constraint: would it still apply if the goal changed? *"Never invent citations"* would (any factual task); *"don't fail to answer"* wouldn't.

## When to add structure

The template above is a frame for non-trivial system prompts — those with real degradation paths, real constraints, real stop conditions. A simple system prompt with one goal and no edge cases doesn't need seven sections; a Role + Goal sentence may be the whole prompt.

Add a section only when the gap it closes is real. Examples-section earns its place when output shape is non-obvious. Stop-rules section earns its place when the prompt drives a loop that can run forever. Personality section earns its place when the prompt is user-facing and the default assistant voice is wrong for the audience.

For techniques that slot into Constraints / Success / Output / Stop (verification loops, retrieval budgets, ambiguity handling, output contracts), see `patterns.md`.
