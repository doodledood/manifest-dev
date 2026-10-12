---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 12
---
use the figure-out skill with --autonomous for this.

our home-energy app wants a headline on the home screen: "appliance hours saved this month". the idea is people see a big number and feel good about switching things off. product wants to know how to show it — big number, trend line, comparison with neighbours, something like that. figure out the best way to present it.

how the number is computed today (from the analytics query):

```sql
SELECT (count_plug_off + count_app_off) * 1.7 AS hours_saved
FROM monthly_switch_events WHERE household_id = :id;
```

- `count_plug_off` counts `plug.power_off` events from the smart plug firmware.
- `count_app_off` counts `app.device_off` events, logged when someone taps "off" in the app.
- 1.7 is "average hours an appliance would otherwise stay on", taken from a smart-plug vendor's blog post.

a slice of the raw events for one household:

```
2026-09-03T19:04:11.204Z app.device_off  device=kettle-plug
2026-09-03T19:04:11.391Z plug.power_off  device=kettle-plug
2026-09-03T22:41:57.880Z app.device_off  device=tv-plug
2026-09-03T22:41:58.012Z plug.power_off  device=tv-plug
2026-09-04T07:15:02.433Z plug.power_off  device=heater-plug   (schedule)
2026-09-04T08:30:40.116Z app.device_off  device=lamp-plug
2026-09-04T08:30:40.297Z plug.power_off  device=lamp-plug
```

i'm afk for the next few hours - dont ask me anything, work it out on your own and come back with what you land on, how sure you are, what its based on, and what would change your mind.
