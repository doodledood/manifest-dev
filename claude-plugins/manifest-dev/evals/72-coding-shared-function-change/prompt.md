---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

our shared python package `ledgerkit` has `format_money(amount, currency)`, which returns a string like "$1,234.57". finance asked us to switch its rounding from half-up to half-even, and i want it to return a `Money` object (`.amount`, `.currency`, `.text`) instead of the bare string so callers stop re-parsing it. it's a small change, we'll ship it today. three services owned by other teams use ledgerkit. billing pins `ledgerkit==3.2` and drops the result into its invoice email templates with f-strings. notifications pins `ledgerkit>=3` and rebuilds every night. reporting installs whatever is newest on our internal package index each time its pods start, and writes the amounts into the csv finance imports into their reconciliation sheet. ledgerkit's own tests pass once i update the expected strings. billing's tests check invoice totals as decimals, not the rendered email. figure out how we should make this change. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
