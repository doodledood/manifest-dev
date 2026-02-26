# PROMPTING Task Guidance

Creating or updating LLM prompts, skills, agents, system instructions.

## Core Principle

Prompts are manifests: **WHAT and WHY, not HOW**. State goals and constraints. Trust model capability—don't prescribe steps it knows how to do.

## Quality Gates

| Gate | Threshold | Verify |
|------|-----------|--------|
| Clarity | No ambiguous instructions, no vague language, no implicit expectations | Read each instruction aloud—flag any with multiple valid interpretations |
| No conflicts | No contradictory rules, no priority collisions, edge cases covered | Identify all MUST/SHOULD rules, check for pairs that can't both be satisfied |
| Structure | Critical rules surfaced prominently, clear hierarchy, no unintentional redundancy | Skim first and last paragraphs only—are critical rules visible? |
| Information density | Every word earns its place | Remove each sentence—if nothing is lost, it didn't earn its place |
| No anti-patterns | No prescriptive HOW, arbitrary limits, capability instructions, weak language | Scan for HOW language, arbitrary numbers, tool names, "try to"/"maybe" |
| Invocation fit | Prompt's expected trigger, caller identity, and output consumer match actual deployment context | Compare prompt's assumptions against where it runs (auto-invoked vs user-facing, output to human vs agent) |
| Domain context | Domain terms, conventions, and constraints captured—not guessed | Check domain-specific language against source material or user confirmation |
| Complexity fit | Prompt complexity matches the task—not over-engineered, not under-specified | Compare prompt structure depth to task difficulty |
| Memento (if multi-phase) | Multi-step prompts externalize state correctly | Verify log-after-each-step and read-before-synthesis disciplines present |
| Description (if skill/agent) | Description follows What + When + Triggers pattern | Check description drives correct auto-invocation |
| Edge case coverage | Prompt handles boundary inputs and unusual conditions, not just the happy path | Identify edge cases from domain; verify prompt addresses each |
| Model-prompt fit | Prompt stays within model capabilities—doesn't assume unreliable behaviors | Flag instructions requiring capabilities the model doesn't reliably have |
| Guardrail calibration | Safety boundaries neither too loose (harmful output possible) nor too tight (valid use cases blocked) | Test boundary cases—does the guardrail correctly allow/block? |
| Output calibration | Output format, length, and detail level match the use case and consumer | Compare expected output characteristics against actual consumer needs |

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

## Issue Types

### Clarity
- **Ambiguous instructions** - multiple valid interpretations; probe: could this be read two ways?
- **Vague language** - "be helpful", "use good judgment", "when appropriate"; probe: what specifically?
- **Implicit expectations** - unstated assumptions; probe: what does "good" mean here?

### Conflict
- **Contradictory rules** - "Be concise" vs "Explain thoroughly"; probe: which wins?
- **Priority collisions** - two MUST rules that can't both be satisfied; probe: priority clear?
- **Edge case gaps** - rules don't cover a situation; probe: what happens when X?

### Structure
- **Buried critical info** - important rules hidden in middle; probe: would skimming miss this?
- **No hierarchy** - all instructions treated as equal priority; probe: what's most important?
- **Unintentional redundancy** - same thing said multiple ways (note: repetition can be intentional emphasis)

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

## Trade-offs

Prompt decisions often involve trade-offs—surface these during discovery:

| Tension | Probe |
|---------|-------|
| Brevity vs explicit guidance | How much does user need spelled out vs trust capability? |
| Flexibility vs specificity | Should output vary or follow strict format? |
| Principles vs examples | Learn from rules or from demonstrations? |
| Trust capability vs enforce discipline | What guardrails are actually needed? |

## When Updating Prompts

If the task is updating an existing prompt (not creating new):

**High-signal changes only**: Every change must address a real failure mode or materially improve clarity. Don't change for the sake of change.

**Right-sized changes**: Don't overcorrect. One edge case doesn't warrant restructuring.

**Questions to probe**:
- Does this change address a real failure mode?
- Am I adding complexity to solve a rare case?
- Can this be said in fewer words?
- Am I turning a principle into a rigid rule?

**Over-engineering warning signs** (probe if present):
- Prompt length doubled or tripled
- Adding edge cases that won't happen
- "Improving" clear language into verbose language
- Adding examples for obvious behaviors

## Prompt Structure Guidance

### Skills/Agents

If creating a skill or agent, probe for:
- **Name**: kebab-case, max 64 chars
- **Description**: What it does + When to use + Trigger terms (under 1024 chars)
- **Mission**: One-line WHAT, not HOW
- **Empty input handling**: What happens with no arguments?
- **Multi-phase**: Does it need memento pattern (log file)?

### System Instructions

If creating system instructions, probe for:
- **Role**: Identity and purpose
- **Approach**: Principles for thinking, not procedures
- **Constraints**: MUST > SHOULD > PREFER hierarchy
- **Output**: Format requirements if any

### Skill Description Pattern

Descriptions drive auto-invocation. Pattern: **What + When + Triggers**

Weak: "Helps with prompts"
Strong: "Craft or update LLM prompts from first principles. Use when creating new prompts, updating existing ones, or reviewing prompt structure."

## Multi-Phase Prompts

If prompt accumulates findings across steps, needs memento pattern:

| LLM Limitation | Pattern Response |
|----------------|------------------|
| Context rot (middle content lost) | Write findings to log after EACH step |
| Working memory is limited | Todo lists externalize tracked areas |
| Synthesis failure at scale | Read full log BEFORE final output |
| Recency bias | Refresh moves findings to context end |

Structure when memento applies:
```
- [ ] Create log /tmp/{workflow}-*.md
- [ ] {Area 1}→log; done when {criteria}
- [ ] {Area 2}→log; done when {criteria}
- [ ] (expand: areas as discovered)
- [ ] Refresh: read full log    ← Never skip
- [ ] Synthesize→artifact; done when complete
```

Key disciplines:
- `→log` after each collection step (discipline, not capability)
- `Refresh: read full log` before synthesis (restores context)
- Acceptance criteria on each todo ("; done when X")

