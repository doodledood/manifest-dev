---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

`on_profile_saved` is also called by loyalty points, newsletter preferences and the fraud score
check. Changing the cache key inside it changes what they get: they may look profiles up by the old
key, rely on the cache being filled or fresh when they run, or depend on the order the hook runs in,
and the fraud check may itself have been reading the wrong customer's profile.

**First, answer in one line:** Does the reply check what the three other callers assume about the
hook and its cache — the key they read by, freshness, call order — and whether the patch changes or
breaks that? Quote it.

**Then judge:** PASS if yes. FAIL if the reply patches the key with the other callers unmentioned,
or names them only as "test the other features" with no assumption checked.
