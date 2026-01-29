---
name: prompt-engineering
description: 'Craft or update LLM prompts from first principles. Use when creating new prompts, updating existing ones, or reviewing prompt structure. Ensures prompts define WHAT and WHY, not HOW.'
---

**User request**: $ARGUMENTS

Create or update an LLM prompt. Prompts act as manifests: clear goal, clear constraints, freedom in execution.

**If creating**: Discover goal, constraints, and structure through targeted questions.

**If updating**: Read existing prompt, identify issues against principles, make targeted fixes.

## Context Discovery

Before writing or improving a prompt, surface all required context through user engagement. Missing domain knowledge creates ambiguous prompts. You can't surface latent requirements you don't understand.

**What to discover**:

| Context Type | What to Surface |
|--------------|-----------------|
| **Domain knowledge** | Industry terms, conventions, patterns, constraints |
| **User types** | Who interacts, expertise level, expectations |
| **Success criteria** | What good output looks like, what makes it fail |
| **Edge cases** | Unusual inputs, error handling, boundary conditions |
| **Constraints** | Hard limits (length, format, tone), non-negotiables |
| **Integration context** | Where prompt fits, what comes before/after |

**Interview method**:

| Principle | How |
|-----------|-----|
| **Generate candidates, learn from reactions** | Don't ask open-ended "what do you want?" Propose concrete options: "Should this be formal or conversational? (Recommended: formal for enterprise context)" |
| **Mark recommended options** | Reduce cognitive load. For single-select, mark one "(Recommended)". For multi-select, mark sensible defaults or none if all equally valid. |
| **Outside view** | "What typically fails in prompts like this?" "What have you seen go wrong before?" |
| **Pre-mortem** | "If this prompt failed in production, what would likely cause it?" |
| **Discovered ≠ confirmed** | When you infer constraints from context, confirm before encoding: "I'm inferring X should be a constraint?" Includes ambiguous scope (list in/out assumptions). |
| **Encode explicit statements** | When user states a preference or requirement, it must appear in the final prompt. Don't let constraints get lost. |
| **Domain terms** | Ask for definitions, don't guess. Jargon you don't understand creates ambiguous prompts. |
| **Missing examples** | Ask for good/bad output examples when success criteria are unclear. |

**Stopping rule**: Continue probing until very confident further questions would yield nothing new, or user signals "enough". Err toward more probing—every requirement discovered now is one fewer failure later.

**Handling ambiguity**: Critical ambiguities (those that would cause prompt failure) require clarification even if user wants to move on. Minor ambiguities can be documented with chosen defaults and proceed. When in doubt, ask—a prompt built on assumptions will fail in ways the user didn't expect.

## Core Principles

| Principle | What It Means |
|-----------|---------------|
| **WHAT and WHY, not HOW** | State goals and constraints. Don't prescribe steps the model knows how to do. |
| **Trust capability, enforce discipline** | Model knows how to search, analyze, generate. Only specify guardrails. |
| **Maximize information density** | Every word earns its place. Fewer words = same meaning = better. |
| **Avoid arbitrary values** | "Max 4 rounds" becomes rigid. State the principle: "stop when converged". |
| **Output structure when needed** | Define format only if artifact requires it. Otherwise let agent decide. |

## Issue Types

**Clarity**:
- Ambiguous instructions (multiple interpretations)
- Vague language ("be helpful", "use good judgment", "when appropriate")
- Implicit expectations (unstated assumptions)

**Conflict**:
- Contradictory rules ("Be concise" vs "Explain thoroughly")
- Priority collisions (two MUST rules that can't both be satisfied)
- Edge case gaps (what happens when rules don't cover a situation?)

**Structure**:
- Buried critical info (important rules hidden in middle)
- No hierarchy (all instructions treated as equal priority)
- Unintentional redundancy (but: repetition can be intentional emphasis—don't remove if it reinforces critical rules)

## Anti-Patterns to Eliminate

| Anti-pattern | Example | Fix |
|--------------|---------|-----|
| Prescribing HOW | "First search, then read, then analyze..." | State goal: "Understand the pattern" |
| Arbitrary limits | "Max 3 iterations", "2-4 examples" | Principle: "until converged", "as needed" |
| Capability instructions | "Use grep to search", "Read the file" | Remove - model knows how |
| Rigid checklists | Step-by-step heuristics tables | Convert to principles |
| Weak language | "Try to", "maybe", "if possible" | Direct: "Do X", "Never Y" |
| Buried critical info | Important rules in middle | Surface prominently |
| Over-engineering | 10 phases for a simple task | Match complexity to need |

## When Updating Prompts

**High-signal changes only**: Every change must address a real failure mode or materially improve clarity. Don't change for the sake of change.

**Right-sized changes**: Don't overcorrect. One edge case doesn't warrant restructuring.

**Questions before changing**:
- Does this change address a real failure mode?
- Am I adding complexity to solve a rare case?
- Can this be said in fewer words?
- Am I turning a principle into a rigid rule?

**Over-engineering warning signs**:
- Prompt length doubled or tripled
- Adding edge cases that won't happen
- "Improving" clear language into verbose language
- Adding examples for obvious behaviors

## Memento Pattern (Multi-Phase Workflows Only)

For prompts involving accumulated findings across steps:

| LLM Limitation | Pattern Response |
|----------------|------------------|
| Context rot (middle content lost) | Write findings to log after EACH step |
| Working memory (5-10 items max) | Todo lists externalize tracked areas |
| Synthesis failure at scale | Read full log BEFORE final output |
| Recency bias | Refresh moves findings to context end |

**Structure when memento applies**:
```
- [ ] Create log /tmp/{workflow}-*.md
- [ ] {Area 1}→log; done when {criteria}
- [ ] {Area 2}→log; done when {criteria}
- [ ] (expand: areas as discovered)
- [ ] Refresh: read full log    ← Never skip
- [ ] Synthesize→artifact; done when complete
```

**Key disciplines**:
- `→log` after each collection step (discipline, not capability)
- `Refresh: read full log` before synthesis (restores context)
- Acceptance criteria on each todo ("; done when X")

## Prompt Structure Reference

### Skills/Agents

```markdown
---
name: kebab-case-name
description: 'What it does. When to use. Trigger terms.'
---

**User request**: $ARGUMENTS

{One-line mission - WHAT, not HOW}

{Empty input handling}

{Log file path if multi-phase}

## {Sections based on actual workflow needs}

{Goals and constraints per section}

## Key Principles

| Principle | Rule |
|-----------|------|
| {Discipline} | {Enforcement} |

## Never Do

- {Anti-pattern}
```

### System Instructions

```markdown
## Role
{Identity and purpose - one paragraph}

## Approach
{Principles for thinking, not procedures}

## Constraints
{MUST > SHOULD > PREFER priority}

## Output
{Format requirements if needed}
```

## Skill Description Pattern

Descriptions drive auto-invocation. Pattern: **What + When + Triggers**

```yaml
# Weak
description: 'Helps with prompts'

# Strong
description: 'Craft or update LLM prompts from first principles. Use when creating new prompts, updating existing ones, or reviewing prompt structure.'
```

- Include trigger terms users say
- Specify when to use
- Under 1024 chars

## Validation Checklist

Before finalizing any prompt:

- [ ] All ambiguities resolved through user questions
- [ ] Domain context gathered (terms, conventions, constraints)
- [ ] Goals stated, not steps prescribed
- [ ] No arbitrary numbers (or justified if present)
- [ ] Weak language replaced with direct imperatives
- [ ] Critical rules surfaced prominently
- [ ] Complexity matches the task
- [ ] Each word earns its place
- [ ] If multi-phase: memento pattern applied correctly
