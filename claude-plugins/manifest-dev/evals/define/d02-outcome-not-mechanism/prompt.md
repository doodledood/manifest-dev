---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
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
