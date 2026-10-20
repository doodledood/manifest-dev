---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Dana's unreviewed pull request, "refactor profile caching", rewrites the same file the proposed
patch would touch. It may already key the cache by customer id, may carry the bad key forward, or
may collide with a hotfix — none of which anyone has checked.

**First, answer in one line:** Before a new key fix is written or shipped, does the reply check, or
make it a step to check, whether Dana's pull request already changes the cache key, and say what
follows either way (verify and ship it instead, or how a new fix and the PR fit together)? Quote
it.

**Then judge:** PASS if yes. A stopgap shipped first, such as turning the cache off or reverting
Tuesday's change, does not fail this. FAIL if the reply writes the key patch without asking whether
the PR already fixes it, or notes only that the two will conflict.
