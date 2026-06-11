# PROMPTING Task Guidance

Creating or updating LLM prompts, skills, agents, system instructions.

## Quality Gates

| Aspect | Verifier | Threshold |
|--------|----------|-----------|
| Intent analysis | `review-code` skill, dimension=`change-intent` | no LOW+ |
| Prompt quality | `review-prompt` skill | no MEDIUM+ |

Both gates encode as a general-purpose verifier (no `verify.agent`) whose `verify.prompt` activates a skill: the intent gate activates the `review-code` skill (dimension=change-intent); the prompt-quality gate activates the `review-prompt` skill.

When the review-prompt skill is not available, encode these as individual criteria verified via general-purpose subagent:

| Gate | Threshold |
|------|-----------|
| Clarity | No ambiguous instructions, no vague language, no implicit expectations |
| No conflicts | No contradictory rules, no priority collisions, edge cases covered |
| Structure | Critical rules surfaced prominently, clear hierarchy, no unintentional redundancy |
| Information density | Every word earns its place |
| No anti-patterns | No prescriptive HOW, arbitrary limits, capability instructions, weak hedging, unjustified absolutes |
| Invocation fit | Prompt's trigger, caller identity, and output consumer match deployment context |
| Domain context | Domain terms, conventions, and constraints captured—not guessed |
| Complexity fit | Prompt complexity matches the task—not over-engineered, not under-specified |
| Memento (if multi-phase) | Multi-step prompts externalize state correctly |
| Description (if skill/agent) | Description is natural-language activation prose: what it does, when to use it, and phrases users actually say |
| Edge case coverage | Handles boundary inputs and unusual conditions, not just the happy path |
| Model-prompt fit | Stays within model capabilities—doesn't assume unreliable behaviors |
| Guardrail calibration | Safety boundaries neither too loose nor too tight |
| Output calibration | Output format, length, and detail level match the use case and consumer |
| Emotional tone | Low arousal—no urgency language, excessive praise, or pressure framing; "trusted advisor" tone; failure normalized in iterative prompts |

When the task involves creating or updating a skill, also apply:

| Gate | Threshold |
|------|-----------|
| Folder architecture | Skill is a directory with SKILL.md + appropriate companions (references, assets, scripts) — not a standalone file |
| Progressive disclosure | Domain knowledge and reference data in companion files, not front-loaded into SKILL.md |
| Gotchas section | Contains observed failure modes — specific, actionable, grounded in real behavior (not theoretical) |
| Description as activation prose | Description field naturally explains what the skill does and when it should activate; no appended keyword lists |

## Defaults

*Domain best practices for this task type.*

- **Identify skill type** — Determine which category the skill falls into (Library/API, Verification, Data, Business Process, Scaffolding, Code Quality, CI/CD, Runbook, Infra Ops) and match architecture to its core pattern
- **Assess config needs** — If skill requires user-specific configuration (IDs, names, preferences), persist in a config file within the skill directory rather than re-asking each session
- **High-signal changes only** (updates) — Every change must address a real failure mode or materially improve clarity. Don't change for the sake of change. Don't overcorrect — one edge case doesn't warrant restructuring
- **Probe for memento needs** — Multi-phase prompts that accumulate findings need externalized state; probe: does this prompt span multiple steps?
- **Define empty input behavior** — What happens when the prompt receives no arguments; probe: should it ask, error, or use defaults?
- **Calibrate emotional tone** — Keep arousal low (avoid urgency language, excessive praise, pressure framing). Target "trusted advisor" tone. Normalize failure in iterative prompts. Opening framing propagates into response planning
