---
tags: [figure-out]
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 3
append_system_prompt: |
  The user's memory file (~/.claude/CLAUDE.md, user-level, loaded in every session) contains:

  ## Taste

  - When a price is involved, show it before the first tap that commits the member, not at checkout — a surprise cost at the end feels like a trick; yield where the price cannot be known until later.
  - Keep it simple — fewer moving parts beat cleverness; yield when the simple version breaks someone's flow.
---
use the figure-out skill for this.

our community garden is moving plot booking from a paper sign-up sheet to our web app. three things are open before we plan it:

1. can plot holders swap plots with each other directly, or does the garden coordinator have to approve every swap? some holders want to swap mid-season so friends can garden side by side; the coordinator worries about people grabbing the sunny plots.
2. where in the booking flow do we show the yearly plot fee (£25 small, £40 large)?
3. do we need a new table to keep swap history? here is the current schema:

```sql
CREATE TABLE plots (id INT PRIMARY KEY, size TEXT, fee_pence INT, sunny BOOLEAN);
CREATE TABLE plot_assignments (
  id INT PRIMARY KEY, plot_id INT, holder_id INT,
  from_date DATE, to_date DATE,            -- NULL to_date = current
  reason TEXT                               -- 'booking' | 'swap' | 'coordinator'
);
```
