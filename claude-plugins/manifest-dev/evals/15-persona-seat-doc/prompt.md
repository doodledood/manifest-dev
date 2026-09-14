---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 12
---
use the figure-out skill for this. i'm afk, dont ask me anything - work it out and come back with what you land on.

we need a getting-started guide for Tally. figure out its structure - the sections, what goes in
each, roughly how long, and where it lives (in-app, web page, PDF). i want to hand the structure
to define and have the guide written from it.

what Tally is:

- a bookkeeping app for one-person trade businesses. it does invoices, expense capture by
  photographing receipts, quarterly tax estimates, and a "what do i owe / who owes me" screen.
- it is phone-first. the web app exists but almost nobody signs in there.
- there is no onboarding in the app today. new users land on an empty invoices list.
- support tickets in the first month are mostly "how do i send an invoice", "where did my receipt
  go", and "is this the number i give my accountant".

the project's north star, so you have it:

```
## Who it's for
Sole traders in the trades — plumbers, electricians, decorators — who do their books at the
kitchen table on a Sunday evening after a full week on site, with no bookkeeping training and a
dislike of paperwork that borders on avoidance. Not for: accountants, businesses with a
bookkeeper, or anyone who wants to learn bookkeeping.
— hypothesis 2026-09

## Promise
Your books done on Sunday night in twenty minutes, and nothing waiting for you at tax time.
— hypothesis 2026-09

## Never
- Use a bookkeeping term where a plain one exists.
— ruled 2026-09
```

(write any notes or logs you keep into the current directory rather than your home directory)
