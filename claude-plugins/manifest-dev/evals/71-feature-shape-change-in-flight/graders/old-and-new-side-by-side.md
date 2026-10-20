---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Checkout deploys on its own and the 12 workers roll one at a time over about 20 minutes, so for that
window old and new workers consume the same queue: checkout may publish messages with the gift
fields while old workers are still running, and old-shape messages reach new workers. An old worker
handed a gift order rejects the message or drops the gift fields. Reverting the deploy brings the
same mix back, with gift messages already queued.

**First, answer in two lines:** Does the reply address old and new versions handling the same
messages during the rollout — a versioned or tolerant message shape, consumers deployed before the
producer, or a flag that turns gift wrap on only once every worker is new? Quote it. Does it say how
the change is reversed with gift messages in flight? Quote it.

**Then judge:** PASS if both are yes. FAIL if the reply treats the deploy as a single switch-over,
or names a revert with no word on messages and workers of both versions during the window.
