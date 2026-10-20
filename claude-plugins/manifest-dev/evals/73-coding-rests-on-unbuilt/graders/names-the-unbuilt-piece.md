---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The plan rests on the carrier sending push events, but nobody has asked the carrier, and its API
docs describe only `GET /shipments/{id}`. Without push events, live status needs a poller — with the
carrier's rate limits, an interval that sets how live "live" is, and a job to run — which changes
both the scope and the design.

**First, answer in one line:** Does the reply flag that push events are unconfirmed (the docs show
only polling), say what changes if they do not exist, and make confirming them, or designing for
polling, a step before building? Quote it.

**Then judge:** PASS if yes. FAIL if the reply designs a receiver for carrier push events as though
they exist, or mentions the question in passing without saying what changes.
