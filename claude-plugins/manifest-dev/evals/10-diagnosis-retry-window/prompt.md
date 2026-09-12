---
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 3
---
the nightly order export writes zero rows maybe once or twice a week and nobody can work out why. the rows are definitely in the db. finance has been reconciling by hand for a month.

use the figure-out skill for this. i'm afk for the next few hours - dont ask me anything, work it out on your own and come back with what you land on, how sure you are, what its based on, and what would change your mind.

everything i can give you is below.

the job runs on a cron at 20:45 UTC. container env: `TZ=UTC`, `EXPORT_WINDOW_HOURS=24`, `EXPORT_WINDOW_TZ=Asia/Jerusalem`, `MAX_ATTEMPTS=3`, `BACKOFF=4`.

```python
WINDOW_HOURS = int(os.environ["EXPORT_WINDOW_HOURS"])
WINDOW_TZ    = ZoneInfo(os.environ["EXPORT_WINDOW_TZ"])

def compute_window(now):
    local_mid = now.astimezone(WINDOW_TZ).replace(
        hour=0, minute=0, second=0, microsecond=0)
    end   = local_mid.astimezone(timezone.utc)
    start = end - timedelta(hours=WINDOW_HOURS)
    return start, end

def run():
    for attempt in range(1, MAX_ATTEMPTS + 1):
        start, end = compute_window(datetime.now(timezone.utc))
        try:
            rows = db.query(SETTLED_BETWEEN, start, end)
            log.info("window %s..%s, matched %d", start, end, len(rows))
            write_csv(rows)
            return
        except TransientError as e:
            log.warning("attempt %d failed: %s", attempt, e)
            time.sleep(BACKOFF ** attempt)
```

a normal night:

```
2026-09-09T20:45:02Z INFO  export start
2026-09-09T20:45:04Z INFO  window 2026-09-08T21:00:00+00:00..2026-09-09T21:00:00+00:00, matched 3184
2026-09-09T20:45:09Z INFO  wrote orders-20260909.csv
```

a zero night:

```
2026-09-11T20:45:02Z INFO  export start
2026-09-11T20:45:31Z WARN  attempt 1 failed: TransientError('connection reset by peer')
2026-09-11T20:49:35Z WARN  attempt 2 failed: TransientError('connection reset by peer')
2026-09-11T21:05:51Z INFO  window 2026-09-11T21:00:00+00:00..2026-09-12T21:00:00+00:00, matched 0
2026-09-11T21:05:51Z INFO  wrote orders-20260911.csv
```

the db team says there was a brief network blip on the 11th but the same blip happened on the 6th and that night exported fine. and someone pointed out the container is on UTC while the window config says Asia/Jerusalem, which looks wrong to them.

(write any notes or logs you keep into the current directory rather than your home directory)
