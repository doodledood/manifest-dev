---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
use the define skill for this.

we're building the Saved places page for a shared trip in Waymark, our trip planner. people use it mostly on their phones while planning a trip with friends. what it does:

- a trip has an owner and a few days (for example Lisbon, 12–14 May). each trip page has its own address, `/trips/<id>`, and people share that link in their group chats.
- the page lists the places people saved for the trip, and anyone signed in can add a place.
- two modes, switched at the top: List (every saved place) and Day plan, which lays the saved places out as a day-by-day plan for the trip with a suggested time for each.
- Day plan has its own setting: the time each day starts (8:00, 9:00 or 10:00), kept per person.
- sign-in is by email and already exists elsewhere in the app.

the app is a small node server with no framework. the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything. write the spec to ./manifest.md in the current directory, not your home directory.
