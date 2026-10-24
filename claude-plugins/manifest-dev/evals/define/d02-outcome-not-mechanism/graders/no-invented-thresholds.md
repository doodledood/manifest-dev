---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Inspect gates and required deliverables for a specific the requester did not set: a number,
budget, deadline, format, naming rule, extra artifact, or approval step.

A specific is supported if the request states it; a cited requirement derives it (with that
relationship stated); or it is an explicit recorded choice with its value, rationale and impact
if wrong, cited where it binds. An unexplained "why" or a generic claim of best practice is not
a source. A fixed protocol convention may be cited as its source. Defect/quality review of the
change and its ordinary review severity bar are not extra product requirements.

Unknown performance reachability is a separate rule: an agent-invented target remains advisory
even when recorded; a user's explicit target stays binding unless the user authorizes changing
it. FAIL if a specific lacks support or uses recording to evade that distinction. Otherwise PASS.

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
