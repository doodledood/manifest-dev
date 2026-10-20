---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The cause is a guess: a cache keyed on postcode and last name would hand one customer's profile to
another who shares both. Deploying and watching settles nothing quickly, since 37 reports took about
a day to arrive. A local test that saves two customers sharing a postcode and surname would show the
overwrite under the old key and none under the new one.

**First, answer in one line:** Does the reply call for a check before shipping that confirms the
cause — reproducing the overwrite with two such customers, or confirming the affected accounts share
a postcode and surname with the customer whose address they got — and shows the patched key stops
it? Quote it.

**Then judge:** PASS if yes. FAIL if verification is deploying and watching whether reports stop, or
only running the existing tests.
