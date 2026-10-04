---
name: manifest-to-goal
description: 'Turn a Manifest into a standalone goal prompt of at most 4,000 characters. Use when the user wants to paste the work into a goal field without a Manifest file reference.'
argument-hint: '<manifest path or inline text>'
user-invocable: true
---

Distill the supplied Manifest — the specification of what to deliver, what counts as done, and the constraints that hold throughout — into a faithful standalone goal. Before drafting, invoke the prompt-engineering skill and apply its principles.

Read the whole Manifest and references needed to understand its intent and requirements. Use the Manifest identified in the request or conversation; ask which one if the target is missing or ambiguous. Apply explicit user amendments, distinguishing settled decisions from suggestions still under discussion. Ask a focused question only when an unresolved choice or contradiction would materially change the goal.

Write for an agent that will have neither the Manifest nor this conversation. Build upward from the intended outcome, adding the decisions and constraints that define success: deliverables, scope, consequential thresholds, quality bar, and delivery or authorization limits. Preserve source-grounded purpose and rationale that guide interpretation or trade-offs, and examples that define a meaningful boundary. Keep assumptions qualified. A retained detail must not revive a superseded goal.

Preserve required methods; leave advisory implementation choices open. Omit derivable implementation detail and repeated explanations that add no decision-relevant information. Synthesize related requirements without weakening their conditions. Use plain language in place of gate IDs and workflow jargon; inline essential requirements rather than sending the reader to the Manifest or another requirements document.

Make the successful end state and its proof explicit: carry the specified checks and pass conditions, including qualitative criteria, and require observed results to support completion. Concrete check commands and target artifact names may define success. Preserve supplied stopping limits and approval boundaries without inventing metrics, budgets, reporting formats or extra review gates.

Check the draft against the complete source for lost obligations, invented requirements and conflicting scope. If fitting the goal would require a material scope decision, ask rather than conceal an omission.

Return one paragraph inside a single plain-text code fence, with no surrounding commentary. Count the goal text inside the fence programmatically, including spaces and punctuation, and revise until it is at most 4,000 characters; the ceiling is not a target. This invocation drafts text only: it does not edit the Manifest, set a running goal or begin the work it describes.
