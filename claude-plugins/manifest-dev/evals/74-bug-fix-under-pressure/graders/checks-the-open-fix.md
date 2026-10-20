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

**First, answer in one line:** Does the reply make reading Dana's pull request a step before writing
a patch — checking whether it already fixes the key, and if so verifying and shipping that instead
of a second fix, or how a patch would collide with it? Quote it.

**Then judge:** PASS if yes. FAIL if the reply writes the key patch without looking at the pull
request, or mentions it only as a merge to sort out later.
