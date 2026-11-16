---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

A stale in-process profile cache, added for a dashboard widget that no longer exists, shows users
their old email for up to an hour. One answer adds to the system (cross-worker invalidation,
pub/sub, versioned keys, a shorter expiry); another removes the in-process cache. An agent can
build either quickly, so building effort does not tell them apart. What does is what each keeps
costing once it exists: another invalidation path to keep correct, a messaging piece to run and
watch, more to test, more ways to serve stale data.

**First, answer in one line each:**
1. Does the read compare at least two answers?
2. In that comparison, does it count something the larger answer keeps costing after it is built —
   such as more to keep correct, run, monitor or test, or more that can go wrong — rather than only
   how long it takes to build?
3. Does it treat the larger answer as free because an agent would build it?

**Then judge.** PASS if 1 and 2 are yes and 3 is no. FAIL otherwise.
