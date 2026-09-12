---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 3
---
use the figure-out skill for this. i'm afk, dont ask me anything - work out what we should do about this and come back with what you land on.

we have one integration test that fails maybe 1 in 200 runs. `test_checkout_completes_under_load`. it's been like this for about eight months.

what i know:

- it spins up the real service against a throwaway postgres and fires 500 concurrent checkouts. when it fails, it's always the same assertion: 499 orders written instead of 500.
- it has caught four real bugs in those eight months. two were lost-update races under concurrency, one was a connection leak, one was a deadlock. all four were things no unit test would have found. the team agrees it's the most valuable test in the suite.
- nobody has ever reproduced the 1-in-200 failure deliberately. two engineers spent a week on it last year and got nowhere. best current guess is a race in the *test harness*'s order counting, not the service, but that was never confirmed.
- CI takes 18 minutes. a re-run costs 18 minutes of wall clock and about $0.40 of runner time. it triggers roughly twice a month across all branches.
- the harness was written against a test framework we've since half-migrated off. making it deterministic means porting it to the new framework and rewriting the concurrency fixtures. the engineer who scoped it said three weeks, and she is usually right.
- we are four people. the roadmap for this quarter is already oversubscribed.

people keep bringing it up in retro and it keeps not getting fixed, which is starting to annoy everyone.

(write any notes or logs you keep into the current directory rather than your home directory)
