---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 3
---
use the figure-out skill for this. i'm afk, dont ask me anything - work out what's causing this and come back with what you land on.

checkout api returns 502 for a few minutes, two or three times a day, no pattern anyone can see. started about three weeks ago. we shipped a lot in that window.

what i can give you:

gateway log during an episode:
```
14:22:07 502 upstream_reset      /api/checkout  upstream=orders-svc  dur=30001ms
14:22:07 502 upstream_reset      /api/checkout  upstream=orders-svc  dur=30003ms
14:22:11 502 upstream_reset      /api/checkout  upstream=orders-svc  dur=30000ms
14:25:40 200 -                   /api/checkout  upstream=orders-svc  dur=143ms
```
gateway `proxy_read_timeout` is 30s.

orders-svc during the same window — nothing at ERROR, and this at INFO:
```
14:21:58 INFO  pool: acquired conn (in_use=48 idle=2 max=50 waiters=0)
14:22:03 INFO  pool: acquired conn (in_use=50 idle=0 max=50 waiters=6)
14:22:09 INFO  pool: acquired conn (in_use=50 idle=0 max=50 waiters=19)
14:25:31 INFO  pool: acquired conn (in_use=31 idle=19 max=50 waiters=0)
```

orders-svc calls payments-svc synchronously inside the checkout handler. payments-svc has no
request logging at all — the team turned it off in July because of volume. its dashboard shows p99
latency for the period as a flat line at exactly 30000ms, which the SRE says is "probably just the
graph clipping".

no traces. the tracing agent was removed from orders-svc in the same three-week window.
deploy log for those three weeks shows 31 deploys across 6 services.

(write any notes or logs you keep into the current directory rather than your home directory)
