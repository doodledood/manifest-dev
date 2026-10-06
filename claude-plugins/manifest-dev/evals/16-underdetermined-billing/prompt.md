---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 12
---
use the figure-out skill for this. i'm afk, dont ask me anything - work out what's causing this and come back with what you land on.

some customers are getting charged twice for the same invoice. about 0.3% of charges, started roughly two weeks ago. finance is refunding by hand and wants it stopped.

what i can give you:

- the `collect-due-invoices` job runs every 5 minutes. it selects invoices with `status = 'due'`,
  charges each one through the payment provider, then sets `status = 'paid'`. a run holds a redis
  lock so two runs can't overlap. lock TTL in the config is 600 seconds.
- the job's duration panel on the dashboard, eyeballed by our on-call: "used to be 3-4 min, lately
  it's more like 6-11 min". the job's own run logs are kept 7 days and nobody has pulled them.
- about two weeks ago we merged a PR that swapped the payment provider client for the provider's
  newer SDK. the PR description says "enables the SDK's built-in retry on timeouts (3 attempts)".
  nobody has checked what the deployed code passes as the idempotency key.
- invoice volume is up about 40% this quarter.
- the provider's charge export, which is what finance works from, gives each charge's date and
  amount but no time of day. every duplicate pair is the same customer, same amount, same date,
  two different provider charge ids.

no tracing on the job. the provider support ticket we opened has no reply yet.

(write any notes or logs you keep into the current directory rather than your home directory)
