---
type: llm
focus: trace
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

This is a backend diagnosis: a nightly job got slower, and nothing a customer sees or uses
changes. Judge from the trace and the final reply.

First answer, in one line each:
1. Does any tool call read a figure-out reference file about a person's seat, journeys or product
   stances (a file under the skill's `references/` whose name or content is about the seat pass)?
2. Does the trace show a separate pass that walks a customer's or person's journeys, or judges
   product choices against product stances, for this job?
3. Does the final read carry product findings — what a customer should see, where a control should
   live, what a person gains — rather than the diagnosis of the job?

PASS when all three are no. FAIL when any is yes. Mentioning that customers are unaffected, or
that the overlap with morning traffic matters, is part of the diagnosis and is not a product
finding.
