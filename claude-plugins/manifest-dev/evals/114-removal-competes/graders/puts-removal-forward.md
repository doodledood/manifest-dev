---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Profiles are read through an in-process cache (`app/local_cache.py`, one per gunicorn worker,
eight workers, one-hour expiry) in front of Redis. A change of email clears Redis but not the
other workers' in-process caches, so the old email shows for up to an hour and flips between
workers. The changelog says the in-process cache was added for a dashboard widget that read one
profile about 40 times per page, and that the widget was removed; Redis reads take about 2 ms.
Two kinds of answer fix it: add to the system (tell every worker to clear its cache, shorten the
expiry, version the keys) or remove the in-process cache, whose job is gone.

**First, answer in one line:** does the read offer removing the in-process cache as an answer —
recommended, or compared beside an additive fix? Quote it.

**Then judge.** PASS if yes. FAIL if the read offers only additive fixes, or mentions removal only
to dismiss it without weighing it.
