---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

signups on our web app (online booking for independent dog groomers) are down about 20% since we shipped the redesign two weeks ago — that's the weekly signups chart on our analytics dashboard. the redesign went live on thursday the 6th. earlier that same week we moved the analytics tag so it only loads after a visitor accepts the new cookie consent banner. most of the drop is on mobile safari; desktop chrome is roughly flat. our spring promo on paid social ended on friday the 7th. if you switch the chart from weekly to daily, the first dip shows up on monday the 3rd. our product manager is sure it's the new signup button colour (it went from green to grey) and wants to revert it this week. figure out why signups dropped and whether reverting the button is the right call. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
