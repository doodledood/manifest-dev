---
name: review-prompt
description: 'Review LLM prompts against the prompt-engineering skill''s principles — leading with where each line came from — and report the findings without modifying files. Use when reviewing prompt quality, auditing a prompt, evaluating a system prompt, or checking whether prompt issues are high-confidence and fixable.'
user-invocable: true
---

Review LLM prompts. Report findings without modifying files — this skill diagnoses; it never edits the prompt.

**First**: invoke the prompt-engineering skill to load the principles. Evaluate the prompt against them.

The provenance question leads: for each line, where did it come from — a user ruling, knowledge outside what the run will read, or a default it counteracts? A line the author could have worked out from material the run also gets is the finding. Judge a prompt by what its lines do, never by sections it lacks: a short prompt with nothing spare is the target, not a deficient one.

**Input**: if no prompt is given (file path or inline text), ask before analyzing — don't assume.

Report format:

## Assessment: {Excellent | Good with Minor Issues | Needs Work}

**Strengths** — what's working, what the author should preserve.

**Issues**:

| Issue | Severity | Fix |
|-------|----------|-----|
| {description} | High / Medium / Low | {concrete recommendation} |

**Priority**: the highest-impact change first.

**Severity**:
- **High** — the prompt actively misbehaves or breaks a contract. Examples: contradiction between two rules that can't both hold; missing the goal entirely; absolute used on a judgment call that observably misfires; the agent declares a need for a tool it doesn't have, or omits a tool it actually uses.
- **Medium** — the prompt works but drifts toward known failure modes. Examples: vague directive that produces inconsistent behavior across runs; restated model default adding noise the model has to wade through; a line whose only provenance is the author's own reading; a real gap left unclosed; arbitrary numbers without a rubric; boundary failures — naming a harness-bound primitive, a rule-scope qualifier that silently excludes valid cases, mechanism stated as the only path, or one principle split across multiple places.
- **Low** — minor friction with no functional impact. Examples: duplication that doesn't change behavior; awkward phrasing where the meaning is still unambiguous; stylistic-only cleanup.

Only flag high-confidence issues. Low-confidence findings are noise — skip style preferences, minor wording, and unverified hunches.
