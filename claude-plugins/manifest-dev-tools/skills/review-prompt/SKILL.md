---
name: review-prompt
description: 'Review LLM prompts against the prompt-engineering skill''s principles — leading with where each line came from — and report the findings without modifying files. Use when reviewing prompt quality, auditing a prompt, evaluating a system prompt, or checking whether prompt issues are high-confidence and fixable.'
user-invocable: true
---

Review LLM prompts. Report findings; modify no file.

**First**: invoke the prompt-engineering skill to load the principles. Evaluate the prompt against them. They are opinionated defaults: where a rule the user stated, in the session or a context file, or a convention the project states or documents differs, that rule governs, a prompt following it raises no finding, and the report names the rule applied — except a High issue on the scale below that makes the prompt miss its goal, which is still reported, naming the rule that produced it.

The provenance question leads: for each line, where did it come from — a user ruling, knowledge outside what the run will read, or a default it counteracts? Identify material the author merely derived from what the run also receives, and show the consequence of retaining it. Judge a prompt by what its lines do for its actual goal, inputs and consumer, never by sections it lacks: a short prompt with nothing spare is the target, not a deficient one.

The caller owns acceptance. When asked for a gate verdict, assess its substantive claims and any
deliberately required policy. A grade or removable sentence alone does not establish a material
failure; state the conflicting instruction, missing context or concrete behavioral or reading
cost. Required evidence that is missing leaves the assessment unresolved. Otherwise report the
findings and assessment without inventing a severity threshold.

**Input**: if no prompt is given (file path or inline text), ask before analyzing — don't assume.

Report format:

**Strengths** — what's working, what the author should preserve.

**Issues**:

| Issue and evidence of its consequence | Severity | Fix |
|---------------------------------------|----------|-----|
| {description and affected claim or concrete cost} | High / Medium / Low | {concrete recommendation} |

**Priority**: the highest-impact change first.

**Severity**:
- **High** — the prompt actively misbehaves or breaks a contract. Examples: contradiction between two rules that can't both hold; missing the goal entirely; absolute used on a judgment call that observably misfires; the agent declares a need for a tool it doesn't have, or omits a tool it actually uses.
- **Medium** — a concrete quality gap materially impairs the prompt's use. Examples: an ambiguous directive produces inconsistent behavior; duplicated or historical instructions obscure which rule applies; an arbitrary number forces the wrong decision; a host-specific primitive excludes a supported context. Name that cost rather than grading a category of wording automatically.
- **Low** — polish or a nit of any kind: style, naming, structure, or otherwise. Example: duplication that adds reading load without changing behavior or the underlying promise.

Only flag high-confidence issues. Low-confidence findings are noise — skip style preferences, minor wording, and unverified hunches.
