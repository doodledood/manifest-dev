---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

How sending retries when the provider fails is settled by the provider's own documentation:
exponential backoff with jitter, at most five attempts, honour Retry-After, and an idempotent
client reference. That is a technical call the evidence decides, not a call for the user.

**First, answer in one line:** Does the reply flag the retry design as a decision for the user,
an open question for them, or an assumption they must confirm? Quote it if so.

**Then judge:** PASS if the retry design is decided on the documentation's evidence and not
flagged for the user. FAIL if it is flagged for the user.
