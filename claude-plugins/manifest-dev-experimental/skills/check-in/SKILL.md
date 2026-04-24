---
name: check-in
description: 'Blocking, same-session fallback scheduler for /drive when /loop is not installed. Takes <interval> <log-path> <command>, sleeps the interval (chunked ≤9m to stay under the Bash tool cap), invokes the command via the Skill tool, reads the log file to find the most recent drive-tick outcome header, and either exits (Terminal / Error / BUDGET EXHAUSTED) or re-loops (Continuing / Skipped). Trades /loop''s background cron for blocking-session determinism. Use when /drive pre-flight selects it because /loop is unavailable. Triggers: check-in, fallback scheduler, sleep and invoke, loop without loop, drive without cron.'
user-invocable: true
---

# /check-in — Blocking Fallback Scheduler

Substitute for `/loop` when it is not installed. Drives `/drive-tick` from a single blocking Skill invocation.

## Args

`<interval> <log-path> <command>` — three positional args, required.

- `<interval>`: `15m`–`24h` inclusive.
- `<log-path>`: absolute path to drive's execution log.
- `<command>`: invoked verbatim via the Skill tool — no shell expansion, no re-parsing.

### Errors

- Missing/empty args → `Usage: /check-in <interval> <log-path> <command>`.
- `<interval>` unparseable or out of range → `Interval '<value>' out of range. Must be between 15m and 24h.`

## Flow

1. Parse `<interval>` to seconds. Compute `chunks = ceil(interval_seconds / 540)` upfront.
2. Record `last_seen_header` = the last `## Tick N — …` line already in `<log-path>` at entry (null if none).
3. Set `empty_count = 0`.
4. Loop:
   - Sleep: issue `chunks - 1` sequential `sleep 540` Bash calls, then one `sleep <remainder>` for the final chunk. Cumulative — drift is acceptable.
   - Invoke `<command>` via the Skill tool. If the Skill tool itself errors, times out, or crashes (NOT the normal case of drive-tick completing and writing a log entry), exit fail-loud. No retry.
   - Read `<log-path>`. Find the last line matching `^## Tick N — ` or `^## BUDGET EXHAUSTED`.
   - If no match, OR the match is not strictly newer than `last_seen_header`: `empty_count += 1`. If `empty_count >= 2`, exit fail-loud (drive-tick produced no new outcome for two consecutive iterations). Otherwise re-loop — ONE grace iteration for first-tick init races.
   - Otherwise update `last_seen_header`, set `empty_count = 0`, classify:
     - `## Tick N — Terminal:` / `## Tick N — Error:` / `## BUDGET EXHAUSTED` → exit.
     - `## Tick N — Continuing` / `## Tick N — Skipped (lock held)` → re-loop.
     - Any other header (none of the five anchors) → exit fail-loud. Never silently continue.

## Terminal markers (verbatim — em-dash U+2014, not hyphen)

- `## Tick N — Terminal:` (terminal)
- `## Tick N — Error:` (terminal)
- `## BUDGET EXHAUSTED` (terminal)
- `## Tick N — Continuing` (continuing)
- `## Tick N — Skipped (lock held)` (continuing)

Authored by drive-tick's Output Protocol; `/check-in` must match them byte-for-byte.

## Gotchas

- **Blocking session.** Closing the Claude Code session stops the loop immediately — no background cron. Install `/loop` for fire-and-forget.
- **Log file is the contract.** drive-tick writes outcomes to `<log-path>`, not to its Skill-tool response. `/check-in` ignores the response text.
- **Chunked-sleep drift.** Per-chunk tool overhead adds <1% over the minimum interval. Interval is a floor, not a precise cadence.
