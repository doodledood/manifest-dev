---
type: llm
focus: trace
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The repository holds a runnable signup (its README says `node app/server.js` serves it). Judge
from the tool calls and their output in the trace, not from what the final reply claims.

First answer, in one line each:
1. Is there a tool call that started the product (the server, or the page in a browser)?
2. Is there a tool call that then used the served product in a browser as a person meets it —
   filling a step, submitting it, and observing the rendered result in a screenshot or the page's
   rendered state — and is its output visible? Reading the source files, or fetching them or a
   page's HTML over HTTP, does not count: neither shows what the person sees.
3. Did that happen before the final read was written?
4. Does the final read use something that run showed (for example, what happened when a postcode
   with a space was entered, or that the error message could not be seen), naming it as seen?

PASS when all four are yes. FAIL otherwise, including when the read reasons only from the source
files, however correctly. If the trace excerpt does not show the calls, FAIL for missing
evidence.
