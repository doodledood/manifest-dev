# Comment Classification Examples

> **Source of truth:** `claude-plugins/manifest-dev/skills/tend-pr/references/classification-examples.md`. This file is a copy kept in sync intentionally (the experimental plugin's github adapter duplicates `tend-pr-tick` semantics per `T-1`). If you edit one, edit the other.

Use these examples to classify PR comments as actionable, false positive, or uncertain.

## Actionable

The comment identifies a genuine issue. Fix it.

| Example | Why Actionable |
|---------|---------------|
| "This function doesn't handle the case where `input` is null" | Identifies a missing edge case |
| "Race condition: `counter` is read and written without synchronization" | Identifies a concurrency bug |
| "This SQL query is vulnerable to injection — use parameterized queries" | Identifies a security vulnerability |
| "The return type should be `Option<T>` not `T` — this can panic" | Identifies a type safety issue |
| "Missing error handling — if the API call fails, the user sees a blank page" | Identifies missing error handling |
| "This duplicates the logic in `utils.ts:42` — should reuse that" | Identifies a DRY violation worth fixing |
| "CI: test_auth_flow failed — assertion error on line 87" | New test failure caused by PR changes |

## False Positive

The comment flags something intentional or not actually a problem.

| Example | Why False Positive |
|---------|-------------------|
| "Consider using `const` instead of `let`" on a variable that IS reassigned later | Reviewer didn't read the full scope |
| "This file is too long" on a file that was long before the PR | Pre-existing, not introduced by this PR |
| Bot: "Unused import `os`" when `os` is used via a macro or conditional compilation | Bot can't see macro expansion |
| "Missing docstring" on an internal helper function in a codebase that doesn't require them | Style preference, not a codebase standard |
| Bot: "Function complexity too high" on a function that was already complex before the PR | Pre-existing finding, not introduced |

## Uncertain

The comment is ambiguous — you can't tell if it's actionable or a false positive without more context.

| Example | Why Uncertain |
|---------|--------------|
| "Is this the right approach?" | Could be rhetorical (approval) or genuine concern |
| "What about performance?" | Unclear if they've identified a specific issue or asking generally |
| "Hmm" | No actionable content |
| "This could be simplified" | Might be a suggestion (low priority) or a blocking concern |
| "Have you considered using X instead?" | Could be a suggestion or a request for change |
| "Not sure about this" | Unclear what specifically concerns them |

## Classification Decision Tree

1. **Does the comment identify a specific, fixable issue?** → Actionable
2. **Is the flagged issue intentional, pre-existing, or based on a misunderstanding?** → False Positive
3. **Is the comment ambiguous about whether a change is needed?** → Uncertain

When torn between actionable and uncertain, prefer **uncertain** — it's safer to ask for clarification than to make an unnecessary change or ignore a valid concern.

When torn between false positive and uncertain, prefer **uncertain** — it's safer to ask than to dismiss a reviewer's concern.
