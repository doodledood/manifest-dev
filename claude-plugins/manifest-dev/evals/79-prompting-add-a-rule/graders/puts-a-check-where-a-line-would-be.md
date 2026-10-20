---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The proposed fix is one more instruction, and it asks for an exact count — five bullets — which
models hold unreliably from a line alone. Length can instead be held by a check: a word or bullet
count on each draft before an agent sees it, with a retry or trim when it fails, or a test that
runs the prompt over the 200 saved tickets and measures the drafts' length against what agents
actually sent.

**First, answer in one line:** Does the reply propose holding the length rule with a check rather
than relying on the instruction alone — a length check on each draft, or a test over the saved
tickets that measures the drafts — and say why an instruction is not enough here? Quote it.

**Then judge:** PASS if yes. FAIL if every change the reply proposes is prompt wording, whether
the new line, a reworded one, or examples added to the prompt.
