---
name: manifest-to-goal
description: 'Turn a Manifest into a standalone goal prompt of at most 4,000 characters. Use when the user wants to paste the work into a goal field without a Manifest file reference.'
argument-hint: '<manifest path or inline text>'
user-invocable: true
---

Turn the supplied Manifest — the specification of what to deliver, what counts as done, and the constraints that hold throughout — into one standalone goal paragraph of at most 4,000 characters. Before drafting, invoke the prompt-engineering skill and apply its principles to the goal.

Read the whole Manifest, following references where they carry requirements needed to understand the work. Use the Manifest identified in the request or conversation; ask which one if the target is missing or ambiguous. Explicit user amendments in the conversation supersede the corresponding text. An unresolved contradiction that changes the goal needs a focused question, not an invented decision.

Write for an agent that will have neither the Manifest nor this conversation. Start with the intended outcome and add the requirements that define its successful end state: deliverables, scope, consequential thresholds, quality bar and delivery or authorization limits. Carry the user's priorities throughout; a retained detail must not revive a superseded goal. State what must be true when the work is complete, rather than merely listing activities. Keep suggested implementation choices optional and omit process the executing agent can derive. Use plain language in place of gate IDs and workflow jargon; inline essential requirements rather than referring the reader to the Manifest or another requirements document.

Make completion checkable. Carry the specified checks and pass conditions into the goal, including qualitative review criteria where numbers would misrepresent the intended result. Require the executor to surface evidence of those results in its completion report, so a reader can distinguish verified completion from a plan, attempt or partial result. Concrete check commands and target artifact names may be included when they define success. Preserve supplied stopping limits and approval boundaries; do not invent metrics, budgets or extra review gates.

Check the draft against the complete source for lost obligations, invented requirements and conflicting scope. Cut repetition, examples and rationale before sacrificing what changes the result. Count the final paragraph programmatically, including spaces and punctuation, and revise until it is within 4,000 characters; the limit is a ceiling, not a target. If a material choice is needed to fit faithfully, ask rather than conceal the omission.

Print only the goal paragraph, without a heading, preamble, code fence, character-count note or follow-up. This invocation drafts text: it does not edit the Manifest, set a running goal or begin the work it describes.
