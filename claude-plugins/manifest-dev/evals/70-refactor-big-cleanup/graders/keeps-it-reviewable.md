---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

One pull request would rename and move 6,000 lines, touch the 40 files that import from them, and
change error handling from return codes to exceptions — mechanical edits mixed with behaviour
changes. Its only capable reviewer is on call the same sprint. Nobody can review a diff like that
with confidence that the nightly sync still behaves the same.

**First, answer in one line:** Does the reply say that the single pull request is too large or too
mixed to review with confidence — naming its size, the mix of mechanical and behavioural changes,
or the one on-call reviewer — and propose splitting it, for example keeping the renames and moves
apart from the error-handling change? Quote it.

**Then judge:** PASS if yes. FAIL if the reply keeps the work in one pull request, or offers only
ways to make the one large review easier, such as a walkthrough or a checklist.
