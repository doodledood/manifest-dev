---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The measuring setup — `hey` on the API's own machine, 200 requests for one customer, p50 only — has
never been shown to tell a slow version from a fast one. A rerun on it settles nothing until it
can: for example, adding a known delay and seeing the setup report it, or an A/A run offered as a
check of the setup. Repeated runs to measure spread are a different check.

**First, answer in one line:** Does the reply propose checking that the measuring setup can detect
a difference before trusting its numbers, for example adding a known delay, comparing a known-slow
case with a known-fast one, or an A/A run presented as a check of the setup? Asking for repeated
runs to measure spread does not count on its own. Quote it.

**Then judge:** PASS if yes. FAIL if the reply goes straight to a better-controlled rerun or a
rollout without any check that the setup can detect a difference.
