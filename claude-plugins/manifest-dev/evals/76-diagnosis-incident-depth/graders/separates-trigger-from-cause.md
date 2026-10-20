---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The config push set the outage off. What made it possible is a different answer: a pool size of 5
could reach production unchecked, staging did not exercise it, and the error rate was already
rising unwatched. What made it worse is a third: the app's retries tripled load and the lagging
replica could not take over. The report's "what caused it" section has to say which of these
it names.

**First, answer in one line:** Does the reply separate what set the outage off (the config push)
from what made it possible and from what made it worse, naming at least one item in each of the
last two, and say which of them the "what caused it" section should name? Quote it.

**Then judge:** PASS if yes. FAIL if the reply gives the misconfigured pool size, or the push,
as the cause and treats the retries and the replica as background, or lists all the factors
without saying which role each played.
