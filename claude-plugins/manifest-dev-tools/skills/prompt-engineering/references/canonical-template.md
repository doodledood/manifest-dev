# Canonical Template

Reach for this when 1-3 paragraphs of essence don't fit — typically complex system prompts, agents with subdomains, multi-phase workflows. Each section has one job; keep each short; add detail only where it changes behavior.

```
Role
Personality          (optional — see below)
Goal
Success criteria
Constraints
Output
Stop rules
```

| Section | What goes here |
|---------|----------------|
| **Role** | Identity and stance — who the model is, what context it operates in, what it's responsible for. One or two sentences. |
| **Personality** | Voice, tone, formality, warmth, directness. Shapes how the assistant *sounds* to the user. **Skip** when the prompt is a worker, internal-pipeline, transformation, extraction, or any non-user-facing task — Personality is for user-facing surfaces only. |
| **Goal** | The user-visible outcome the run produces. State the destination, not the path. |
| **Success criteria** | What must be true before the final answer. Include the **degradation paths**: when to **retry** (transient failure), **fallback** (alternative method), **abstain** (refuse with reason), **ask** (for the smallest missing field). The four verbs prevent loops and silent guessing. |
| **Constraints** | Rules that must hold throughout the run — policy, safety, business, evidence, side-effect limits. Reserve absolutes (MUST/NEVER) for true invariants; for judgment calls, decision rules ("When X, do Y; otherwise Z"). When multiple non-invariant rules apply, mark priority (MUST > SHOULD > PREFER). |
| **Output** | Format, length, audience, structure. Be specific only where it changes behavior — don't over-prescribe shape the model already gets right from Goal. |
| **Stop rules** | Loop control: when to stop pursuing more information and answer with what you have. Distinct from Success (target state) and degradation (non-success behavior). |

## Success vs Constraints vs Stop rules

Three jobs frequently conflated. For a retrieval agent:

- **Success criteria:** *"answer addresses every part of the asked question"* — the target state.
- **Constraints:** *"ground every factual claim in retrieved content; never invent citations"* — rules that hold throughout.
- **Stop rules:** *"when one more search would not change the answer, write"* — the loop-exit rule.

Conflating Success and Stop → over-search or premature stop. Conflating Constraints and Success → target buried inside hard rules. Conflating Constraints and Stop → permanent rule turned into one-shot exit.

Constraints bound the path, not the destination. *"Don't fail to answer"* just restates the goal negatively — adds no boundary. Test for a real constraint: would it still apply if the goal changed? *"Never invent citations"* would (any factual task); *"don't fail to answer"* wouldn't.

## When canonical headers vs theme/phase organization

- **Canonical headers** when the prompt is a single-purpose system prompt for an assistant — one Role, one Goal, runtime in a deployment.
- **Theme or phase organization** when the prompt's structure is itself non-trivial — multi-phase workflows, skills with subdomains, instructional documents — so long as every applicable canonical section is answerable on read.

For non-trivial sections, pull techniques from `system-prompt-patterns.md`.
