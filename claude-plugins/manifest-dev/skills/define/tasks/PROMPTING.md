# PROMPTING Task Guidance

Creating or updating LLM prompts, skills, agents, system instructions.

## Core Principle

Prompts are manifests: **WHAT and WHY, not HOW**. State goals and constraints. Trust model capability—don't prescribe steps it knows how to do.

## Quality Gates

| Aspect | Agent | Threshold |
|--------|-------|-----------|
| Clarity | general-purpose | No ambiguous instructions or vague language |
| No conflicts | general-purpose | No contradictory rules or priority collisions |
| Information density | general-purpose | Every word earns its place |
| No anti-patterns | general-purpose | No prescriptive HOW, arbitrary limits, weak language |

## Risks

- **Prescribing HOW** - step-by-step instructions for things model knows; probe: can this be a goal instead of steps?
- **Arbitrary limits** - "max 3 iterations" instead of "until converged"; probe: is this a principle or a number?
- **Weak language** - "try to", "maybe", "if possible"; probe: can this be direct?
- **Over-engineering** - 10 phases for simple task; probe: does complexity match the task?
- **Buried critical info** - important rules hidden in middle of prompt
- **Missing context** - domain terms undefined, success criteria unclear; probe: what does good output look like?

## Trade-offs

- Brevity vs explicit guidance
- Flexibility vs specificity
- Principles vs examples
- Trust capability vs enforce discipline

## Scenario Prompts

- **Context rot** - critical instruction forgotten mid-execution; probe: long prompt? multi-step workflow?
- **Ambiguous interpretation** - instruction parsed differently than intended; probe: could this be read two ways?
- **Capability assumption** - assumes model can do something unreliably; probe: within model strengths?
- **Conflicting instructions** - two rules can't both be satisfied; probe: priority clear? edge cases?
- **Edge case unhandled** - prompt works for typical input, fails on unusual; probe: what weird inputs are possible?
- **Wrong model assumption** - prompt tuned for one model, used with another; probe: model-specific behaviors?
- **Overfitting to examples** - follows examples too literally; probe: are examples representative?
- **Error handling gap** - no guidance when things go wrong; probe: what should happen on failure?
- **State management missing** - multi-step loses track; probe: needs memento pattern? externalized state?
- **Tool use unclear** - model doesn't know when/how to use tools; probe: tool guidance explicit?
- **Guardrail too loose** - harmful output possible; probe: what outputs must never happen?
- **Guardrail too tight** - valid use cases blocked; probe: false positives acceptable?
- **Verbosity mismatch** - too long or too terse for use case; probe: output length expectations?

## Multi-Phase Prompts

If prompt accumulates findings across steps, needs memento pattern:
- Write to log after each step (combat context rot)
- Read full log before synthesis (restore context)
- Externalize state to todos (working memory limit ~5-10 items)
