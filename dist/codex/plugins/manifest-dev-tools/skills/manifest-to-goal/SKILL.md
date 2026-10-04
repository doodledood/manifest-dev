---
name: manifest-to-goal
description: 'Turn a Manifest into a standalone goal prompt of at most 4,000 characters. Use when the user wants to paste the work into a goal field without a Manifest file reference.'
argument-hint: '<manifest path or inline text>'
user-invocable: true
---

Turn the supplied Manifest — the specification of what to deliver, what counts as done, and the constraints that hold throughout — into one standalone goal paragraph of at most 4,000 characters. Invoke the prompt-engineering skill.

Read the whole Manifest, following references where they carry requirements needed to understand the work. Use the Manifest identified in the request or conversation; ask which one if the target is missing or ambiguous. Explicit user amendments in the conversation supersede the corresponding text. An unresolved contradiction that changes the goal needs a focused question, not an invented decision.

Write an actionable goal for an agent that will have neither the Manifest nor this conversation. Lead with the intended outcome and experience. Preserve the deliverables, scope boundaries, consequential thresholds, quality bar, completion conditions and delivery or authorization limits. Carry the user's priorities through the whole paragraph: a retained detail must not quietly pull the work back toward a superseded goal. Keep requirements distinct from suggested implementation choices; compress repetition, examples, rationale and process before sacrificing what changes the result. Use plain language in place of gate IDs and workflow jargon. Include necessary context directly, with no file references or instructions to consult the original Manifest or conversation. Do not invent requirements or silently relax them to fit.

Check the draft against the complete source for lost obligations and conflicting scope. Count the final paragraph programmatically, including spaces and punctuation, and revise until it is within 4,000 characters; the limit is a ceiling, not a target. If a material choice is needed to fit faithfully, ask rather than conceal the omission.

Print only the goal paragraph, without a heading, preamble, code fence, character-count note or follow-up. This invocation drafts text: it does not edit the Manifest, set a running goal or begin the work it describes.
