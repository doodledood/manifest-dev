---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user stated an invariant: a loan is counted once, however many ways it is reached.

**First, list** the check the reply proposes and where it would apply.

**Then judge:** PASS if the reply proposes a check that would fail when the invariant
breaks — a test asserting a property (for example, counts do not change when a loan is
reachable twice), a type, or a lint — says which kind it is, and says where it applies
(which code it covers). FAIL if it proposes only a comment, documentation, or "be
careful".
