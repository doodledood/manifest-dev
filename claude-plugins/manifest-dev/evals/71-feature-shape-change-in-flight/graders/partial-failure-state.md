---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

For a gift order the worker charges the card first, then reserves the item and a wrap kit through a
warehouse API that drops out for a few minutes most weeks. If the reservation fails after the charge
succeeded, the customer has paid and nothing is reserved, and a retry of the message charges the
card again unless the charge is safe to repeat.

**First, answer in one line:** Does the reply name the state left when the charge succeeds and the
reservation fails — a paid order with nothing reserved — and say how the design deals with it:
reserving before charging, a refund or other compensating step, or a retry that cannot charge twice?
Quote it.

**Then judge:** PASS if yes. FAIL if the reply treats the charge and the reservation as if they
succeed or fail together, or proposes retrying the message without saying what happens to the card
already charged.
