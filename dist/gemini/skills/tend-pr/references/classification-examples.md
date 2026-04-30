# Comment Classification Examples

Use these examples to classify PR comments as actionable, false positive, or uncertain. Examples are drawn from all three comment surfaces — **inline** (file-level review threads), **review-body** (text submitted with Approve / Request Changes / Comment), and **top-level** (the conversation tab below the diff). The same classification rules apply across surfaces — a top-level "Could you also handle X?" is just as actionable as an inline "this is missing the null check."

## Actionable

The comment identifies a genuine issue. Fix it.

| Example | Surface | Why Actionable |
|---------|---------|---------------|
| "This function doesn't handle the case where `input` is null" | inline | Identifies a missing edge case |
| "Race condition: `counter` is read and written without synchronization" | inline | Identifies a concurrency bug |
| "This SQL query is vulnerable to injection — use parameterized queries" | inline | Identifies a security vulnerability |
| "The return type should be `Option<T>` not `T` — this can panic" | inline | Identifies a type safety issue |
| "Missing error handling — if the API call fails, the user sees a blank page" | inline | Identifies missing error handling |
| "This duplicates the logic in `utils.ts:42` — should reuse that" | inline | Identifies a DRY violation worth fixing |
| "CI: test_auth_flow failed — assertion error on line 87" | top-level | New test failure caused by PR changes |
| "Could you also handle the case where the user is logged out? It's not covered anywhere in this PR." | top-level | Scope-extension request for a missing case |
| "Requesting changes — the migration script needs a rollback path before this can land." | review-body | Reviewer blocking on a concrete missing capability |
| "Please also update the README — the new flag isn't documented anywhere." | top-level | Specific cross-cutting fix tied to this PR |

## False Positive

The comment flags something intentional or not actually a problem.

| Example | Surface | Why False Positive |
|---------|---------|-------------------|
| "Consider using `const` instead of `let`" on a variable that IS reassigned later | inline | Reviewer didn't read the full scope |
| "This file is too long" on a file that was long before the PR | inline | Pre-existing, not introduced by this PR |
| Bot: "Unused import `os`" when `os` is used via a macro or conditional compilation | inline | Bot can't see macro expansion |
| "Missing docstring" on an internal helper function in a codebase that doesn't require them | inline | Style preference, not a codebase standard |
| Bot: "Function complexity too high" on a function that was already complex before the PR | inline | Pre-existing finding, not introduced |
| "Looks great, ship it 🚀" | top-level | Approval acknowledgement, no change requested |
| "Approving — nice cleanup." | review-body | Approval, not actionable |
| "Why are we not just deleting this whole module?" — when the module is actively used by another consumer not visible in the PR diff | top-level | Misunderstanding of broader usage; not a real ask |

## Uncertain

The comment is ambiguous — you can't tell if it's actionable or a false positive without more context.

| Example | Surface | Why Uncertain |
|---------|---------|--------------|
| "Is this the right approach?" | inline | Could be rhetorical (approval) or genuine concern |
| "What about performance?" | inline | Unclear if they've identified a specific issue or asking generally |
| "Hmm" | inline | No actionable content |
| "This could be simplified" | inline | Might be a suggestion (low priority) or a blocking concern |
| "Have you considered using X instead?" | inline | Could be a suggestion or a request for change |
| "Not sure about this" | inline | Unclear what specifically concerns them |
| "Should we revisit the design here?" | top-level | Could mean "block this PR" or "let's chat after merge" |
| "Have you thought about how this interacts with the new auth system?" | top-level | Could be an informational question or a blocking concern; surface area unspecified |
| "I'm leaning toward not shipping this until we discuss." | review-body | Direction unclear: pause-pending-discussion vs request-changes — needs reviewer clarification |

## Classification Decision Tree

1. **Does the comment identify a specific, fixable issue?** → Actionable
2. **Is the flagged issue intentional, pre-existing, or based on a misunderstanding?** → False Positive
3. **Is the comment ambiguous about whether a change is needed?** → Uncertain

When torn between actionable and uncertain, prefer **uncertain** — it's safer to ask for clarification than to make an unnecessary change or ignore a valid concern.

When torn between false positive and uncertain, prefer **uncertain** — it's safer to ask than to dismiss a reviewer's concern.
