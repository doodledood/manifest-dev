---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The repository has a verification harness: `scripts/verify`, reading one recipe per feature
under `verification/recipes/`. The overdue recipe has no evidence, so the harness lists it
`unverified`.

**First, answer in one line:** Does the reply name the overdue recipe (or the harness) as how
the change will be checked, and say it will be run rather than treated as already proven?
Quote it.

**Then judge:** PASS if yes. FAIL if the reply ignores the existing harness, or treats the
unverified recipe as proof that the feature works.
