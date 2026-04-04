# PROMPTING Task Guidance

Creating or updating LLM prompts, skills, agents, system instructions.

## Core Principle

Prompts are manifests: **WHAT and WHY, not HOW**. State goals and constraints. Trust model capability—don't prescribe steps it knows how to do.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Intent analysis | change-intent-reviewer | no LOW+ |
| Prompt quality | prompt-reviewer | no MEDIUM+ |

When prompt-reviewer is not available, encode these as individual criteria verified via general-purpose subagent:

| Gate | Threshold |
|------|-----------|
| Clarity | No ambiguous instructions, no vague language, no implicit expectations |
| No conflicts | No contradictory rules, no priority collisions, edge cases covered |
| Structure | Critical rules surfaced prominently, clear hierarchy, no unintentional redundancy |
| Information density | Every word earns its place |
| No anti-patterns | No prescriptive HOW, arbitrary limits, capability instructions, weak language |
| Invocation fit | Prompt's trigger, caller identity, and output consumer match deployment context |
| Domain context | Domain terms, conventions, and constraints captured—not guessed |
| Complexity fit | Prompt complexity matches the task—not over-engineered, not under-specified |
| Memento (if multi-phase) | Multi-step prompts externalize state correctly |
| Description (if skill/agent) | Description follows What + When + Triggers pattern |
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
| Description as trigger | Description field is a trigger specification (what + when + trigger terms), not a human-readable summary |

## Context to Discover

Before defining a prompt, probe for these—missing context creates ambiguous prompts:

| Context Type | What to Surface | Probe |
|--------------|-----------------|-------|
| **Domain knowledge** | Industry terms, conventions, patterns | What jargon should the prompt understand? |
| **User types** | Who interacts, expertise level, expectations | Who will use this? What do they expect? |
| **Success criteria** | What good output looks like, what makes it fail | Show me a good/bad example output? |
| **Edge cases** | Unusual inputs, error handling, boundary conditions | What weird inputs are possible? |
| **Constraints** | Hard limits (length, format, tone), non-negotiables | What MUST never happen? What limits exist? |
| **Integration context** | Where prompt fits, what comes before/after | What triggers this? What consumes the output? |

## Anti-Patterns

| Anti-pattern | Example | Fix |
|--------------|---------|-----|
| Prescribing HOW | "First search, then read, then analyze..." | State goal: "Understand the pattern" |
| Arbitrary limits | "Max 3 iterations", "2-4 examples" | Principle: "until converged", "as needed" |
| Capability instructions | "Use grep to search", "Read the file" | Remove—model knows how |
| Rigid checklists in authored prompts | "Step 1: search. Step 2: read. Step 3: analyze." baked into the prompt | Convert to goal + constraints (discipline patterns like memento are exempt) |
| Weak language | "Try to", "maybe", "if possible" | Direct: "Do X", "Never Y" |
| Buried critical info | Important rules in middle | Surface prominently |
| Over-engineering | 10 phases for a simple task | Match complexity to need |

## Risks & Scenario Prompts

Pre-mortem fuel—imagine the prompt failing:

- **Context rot** - critical instruction forgotten mid-execution; probe: long prompt? multi-step workflow?
- **Edge case unhandled** - prompt works for typical input, fails on unusual; probe: what weird inputs are possible?
- **Wrong model assumption** - prompt tuned for one model, used with another; probe: model-specific behaviors?
- **Overfitting to examples** - follows examples too literally; probe: are examples representative?
- **Error handling gap** - no guidance when things go wrong; probe: what should happen on failure?
- **State management missing** - multi-step loses track; probe: needs memento pattern? externalized state?
- **Tool use unclear** - model doesn't know when/how to use tools; probe: tool guidance explicit?
- **Guardrail too loose** - harmful output possible; probe: what outputs must never happen?
- **Guardrail too tight** - valid use cases blocked; probe: false positives acceptable?
- **Verbosity mismatch** - output too long or too terse for use case; probe: output length expectations?
- **Regression on update** - change fixes one issue but silently breaks existing behavior that was correct; probe: what currently works that this change could affect?
- **Composition conflict** - prompt works in isolation but contradicts system instructions, tool definitions, or other prompts it's embedded with; probe: what else will be in context when this runs?
- **Emotional tone miscalibrated** - urgency language, excessive praise, or pressure framing triggers sycophancy or corner-cutting; probe: does the opening set a calm, direct tone? any high-stakes framing that could be read as pressure?
- **Over-engineering on update** - change addresses one issue but doubles prompt length or adds edge cases that won't happen; probe: is this change proportional to the problem?

## Trade-offs

Prompt decisions often involve trade-offs—surface these during discovery:

| Tension | Probe |
|---------|-------|
| Brevity vs explicit guidance | How much does user need spelled out vs trust capability? |
| Flexibility vs specificity | Should output vary or follow strict format? |
| Principles vs examples | Learn from rules or from demonstrations? |
| Trust capability vs enforce discipline | What guardrails are actually needed? |

## Defaults

*Domain best practices for this task type.*

- **Identify skill type** — Determine which category the skill falls into (Library/API, Verification, Data, Business Process, Scaffolding, Code Quality, CI/CD, Runbook, Infra Ops) and match architecture to its core pattern
- **Assess config needs** — If skill requires user-specific configuration (IDs, names, preferences), persist in a config file within the skill directory rather than re-asking each session
- **High-signal changes only** (updates) — Every change must address a real failure mode or materially improve clarity. Don't change for the sake of change. Don't overcorrect — one edge case doesn't warrant restructuring
- **Probe for memento needs** — Multi-phase prompts that accumulate findings need externalized state; probe: does this prompt span multiple steps?
- **Define empty input behavior** — What happens when the prompt receives no arguments; probe: should it ask, error, or use defaults?
- **Calibrate emotional tone** — Keep arousal low (avoid urgency language, excessive praise, pressure framing). Target "trusted advisor" tone. Normalize failure in iterative prompts. Opening framing propagates into response planning

## Multi-Phase Prompts

If prompt accumulates findings across steps, probe for memento pattern needs:

| LLM Limitation | What memento must achieve |
|----------------|--------------------------|
| Context rot (middle content lost) | Findings externalized after each step |
| Working memory is limited | Tracked areas externalized |
| Synthesis failure at scale | Full log read before final output |
| Recency bias | Refresh mechanism moves findings to context end |

Key disciplines: log after each collection step, read full log before synthesis, acceptance criteria on each tracked item.

