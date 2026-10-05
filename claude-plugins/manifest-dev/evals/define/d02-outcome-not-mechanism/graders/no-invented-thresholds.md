---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The document under review is a work spec. If it is missing or empty, FAIL.

The prompt that produced this spec is reproduced at the end of this rubric. A bar the requester
never set, stated in a check as if they had, makes that check stricter than the work needs.

**First, list every threshold in the gates** — the acceptance criteria, invariants, or other checks
that must pass: every number (latency, coverage, count, size, time), budget, deadline, required
format or naming, required report, and approval or sign-off step. One line each: quote it, then
**FROM THE REQUEST** (the requester stated it or it follows directly from what they stated),
**RECORDED** (not from the request, but the spec records it as an assumption or proposed default
with its reason), or **INVENTED** (neither).

**Then judge:** PASS if no threshold is INVENTED. FAIL if any is, and name it.

A check that reviews the change itself for defects or quality, or that keeps the work within
what was asked, is not a threshold. Skip it.

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
