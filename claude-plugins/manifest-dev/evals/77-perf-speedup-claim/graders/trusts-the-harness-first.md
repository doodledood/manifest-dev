---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The measuring setup — `hey` on the API's own machine, 200 requests for one customer, p50 only — has
never been shown to tell a slow version from a fast one. A rerun on it settles nothing until it can:
for example, adding a known delay and seeing the setup report it, or running the same version twice
and seeing it report no difference.

**First, answer in one line:** Does the reply propose checking the measuring setup itself before
trusting its numbers — a known-slow against a known-fast case, the same version run twice, or an
equivalent calibration — rather than only rerunning the comparison? Quote it.

**Then judge:** PASS if yes. FAIL if the reply goes straight to a better-controlled rerun or a
rollout without any check that the setup can detect a difference.
