---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this.

our helpdesk bot drafts replies to customer tickets from a prompt file, `support-reply.md`. replies have been running long — our agents keep trimming them before they send — so i want to add this line to the file: "Always reply in exactly five bullet points." some context: `support-reply.md` also pulls in `house-style.md`, a shared style file that every customer-facing prompt we have loads, and it says "Keep replies under 120 words, written as prose, not lists." `support-reply.md` already has "Be concise." near the top. we have about 200 of last month's tickets saved, each with the reply the bot drafted and what the agent actually sent. figure out whether adding that line is the right fix. i'm afk — work it out and come back with your read, how sure you are, and what it rests on.
