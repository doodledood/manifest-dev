---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The repository has the skill and an eval suite under evals/ with recorded results.

**First, answer in one line:** Does the reply say the change is checked by behavior cases
run against the skill (new or existing cases in evals/, judged on what the run produced),
and note that the recorded results go stale once the skill changes? Quote it.

**Then judge:** PASS if the reply plans behavior cases for the five-line rule and its
exception. FAIL if it plans no way to check the skill's behavior, or only rereads the
prompt text.
