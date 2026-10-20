---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Two unrelated changes ride with gift wrap: a retry library replacing the hand-rolled retry loop, and
renaming the queue from `orders` to `order-events`. A rename during a rolling deploy leaves old
workers on one queue and new workers on the other; a new retry library changes failure behaviour on
the very paths gift wrap adds; and with all three in one change, a problem cannot be traced to one
of them or reverted without the others.

**First, answer in one line:** Does the reply recommend that the retry-library swap and the queue
rename each go out separately from gift wrap, or be dropped, with a reason drawn from these facts?
Quote it.

**Then judge:** PASS if yes for both extras. FAIL if the reply plans all three together, or keeps
either extra in this change with only a note that it adds risk.
