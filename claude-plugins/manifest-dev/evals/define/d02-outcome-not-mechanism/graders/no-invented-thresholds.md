---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Scan the gates — the acceptance criteria, invariants, or other checks that must pass — and the
deliverables the spec requires, for a specific threshold the requester never set: a number
(latency, coverage, count, size, time), budget, deadline, required format or naming, required
report or write-up (a runbook, change notes, a release or support note), or approval step. It is
fine when the request states it or it follows directly from what the request states, or when the
spec records it as an assumption or proposed default with its reason, or when the gate itself
states why. Also fine: a convention the stated stack or protocol already fixes, such as standard
HTTP status codes or a framework's defaults. Checks that review the change itself for defects or
quality, including the severity bar they apply, or keep the work within what was asked, are not
thresholds.

FAIL only if you can name a specific threshold that is neither from the request nor recorded.
Otherwise PASS.

The request:

use the define skill for this.

bug: after pricing updates a product's price, the storefront keeps showing the old price for up to
an hour. customers get charged the new price at checkout and file complaints. the storefront
reads prices through a redis cache with a 1h ttl.

fix i have in mind: add a cron job that flushes the price keys in redis every minute. what
actually matters is that no customer sees a price more than a minute older than the current one.

one hard rule: price changes must keep flowing through the existing PriceEvents bus. compliance
audits every price change from that bus, so no side channel that updates prices or the cache
around it.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
