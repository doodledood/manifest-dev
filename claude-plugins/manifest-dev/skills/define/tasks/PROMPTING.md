# PROMPTING Task Guidance

Creating or updating LLM prompts, skills, agents, system instructions.

## Quality Gates

| Aspect | Verifier | Quality owed |
|--------|----------|-----------|
| Intent analysis | `review-code` skill, dimension=`change-intent` | The prompt serves its accepted purpose and obligations |
| Prompt quality | `review-prompt` skill | The prompt supplies sufficient, consistent and usable direction for its actual inputs, capabilities and output consumer |

Claims state these qualities for the prompt's intended use. Evidence activates `review-code`
with dimension `change-intent` and `review-prompt` for prompt quality, passing the claims and any
deliberately required policy, as `SKILL.md` → *Specialized gates activate a skill* says. Reviewer
grades inform those judgments. Both are Judgment Gates, assessed from findings and evidence
rather than a command outcome.

When review-prompt is unavailable, use these concerns to assess the quality claim:

| Gate | Threshold |
|------|-----------|
| Clarity | Goal, binding requirements, and consequential choices are unambiguous; implementation choices may remain with the run |
| No conflicts | No contradictory rules, no priority collisions, edge cases covered |
| Structure | Critical rules surfaced prominently, clear hierarchy, no unintentional redundancy |
| Information density | Every word earns its place |
| No anti-patterns | Required mechanisms and limits carry a user ruling, external constraint, or observed failure; incidental HOW stays with the run |
| Invocation fit | Prompt's trigger, caller identity, and output consumer match deployment context |
| Domain context | Domain terms, conventions, and constraints captured—not guessed |
| Complexity fit | Prompt complexity matches the task—not over-engineered, not under-specified |
| Memento (if multi-phase) | Multi-step prompts externalize state correctly |
| Description (if skill/agent) | Description is natural-language activation prose: what it does, when to use it, and phrases users actually say |
| Edge case coverage | Required boundary behavior is reachable and consistent with the goal and caller; no speculative procedure is added merely for completeness |
| Model-prompt fit | Stays within model capabilities—doesn't assume unreliable behaviors |
| Guardrail calibration | Safety boundaries neither too loose nor too tight |
| Output calibration | Output format, length, and detail level match the use case and consumer |
| Emotional tone | Low arousal—no urgency language, excessive praise, or pressure framing; "trusted advisor" tone; failure normalized in iterative prompts |

When the task involves creating or updating a skill, also apply:

| Gate | Threshold |
|------|-----------|
| Folder architecture | Skill is a directory with SKILL.md + appropriate companions (references, assets, scripts) — not a standalone file |
| Progressive disclosure | Domain knowledge and reference data in companion files, not front-loaded into SKILL.md |
| Description as activation prose | Description field naturally explains what the skill does and when it should activate; no appended keyword lists |
| Provenance | Every line traces to a user ruling, to knowledge outside what the run will read, or to an observed model default it counteracts — not to the author's own reading of material the run also gets |

## Defaults

*Domain best practices for this task type.*

- **Assess config needs** — If a skill requires configuration (IDs, names, preferences), persist it at a fixed path in the project rather than inside the skill directory, and read it instead of re-asking each session
- **High-signal changes only** (updates) — Every change must address a real failure mode or materially improve clarity. Don't change for the sake of change. Don't overcorrect — one edge case doesn't warrant restructuring
- **Externalize state in multi-phase prompts** — Where the prompt spans several steps and accumulates findings, have it write that state out as it goes rather than carry it in context
- **Define empty input behavior** — State in the prompt what it does when it receives no arguments: ask, error, or use a default
- **Calibrate emotional tone** — Keep arousal low (avoid urgency language, excessive praise, pressure framing). Target "trusted advisor" tone. Normalize failure in iterative prompts. Opening framing propagates into response planning
- **Blind behavior checks** — Behavior cases keep their own wording and rubric out of what the prompt under test sees, and grade what the run actually did — the files it opened and wrote — rather than its account of what it did
- **Model a shared protocol before shipping it** — Where the prompt sets rules that several runs, agents or people follow on the same state (claims, handoffs, retries, who writes what), weigh a throwaway model of those rules, checked in scratch with whatever tool fits (such as TLA+ or Alloy) and only as deep as the risk warrants; turn what it finds into design decisions and gates, and keep the model as a check only where the protocol will keep changing
- **One rule, one place** — A rule another file already states is not restated or contradicted; where a check could hold a rule, prefer the check to another line every run must read, above all for what models do unreliably (exact counts, long-range recall, a format held over long output)
