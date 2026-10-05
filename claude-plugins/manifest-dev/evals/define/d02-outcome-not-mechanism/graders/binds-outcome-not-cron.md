---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The user proposed a mechanism (a cron that flushes redis every minute) and then stated what
actually matters: no customer sees a price more than a minute older than the current one.

**First, quote** the gate or gates that check price freshness. For each, answer one line: if the
executor met the one-minute bound *without* a cron (say, event-driven invalidation), would this
gate still pass? Answer YES or NO.

**Then judge:** PASS if at least one gate checks the freshness outcome (a bound on how stale a
shown price can be) AND no gate would answer NO, meaning no gate requires the cron itself. FAIL
if freshness is only checked through the cron's existence or schedule, or if no gate checks
freshness at all.

The cron may appear in the approach or as a suggestion — that is fine. Only binding checks count.
