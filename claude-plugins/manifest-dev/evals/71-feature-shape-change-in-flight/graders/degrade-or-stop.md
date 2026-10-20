---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The gift part of an order can fail on its own: a wrap kit can be unavailable, the warehouse API
drops out most weeks, or the tag PDF can fail to render. The design has to say whether the order
then goes through unwrapped (with the £3.50 refunded or the customer told) or stops until the gift
part succeeds. Either can be right; what matters is that it is decided with a reason.

**First, answer in one line:** Does the reply decide what happens to the order when only the
gift-wrap part fails — let it through without wrap, or hold or fail it — and give a reason tied to
the case, such as the fee already charged, a gift arriving unwrapped, or the warehouse outages?
Quote it.

**Then judge:** PASS if yes. FAIL if the reply never raises this, or says only to "handle failures
gracefully" or "add error handling" without deciding which way the order goes.
