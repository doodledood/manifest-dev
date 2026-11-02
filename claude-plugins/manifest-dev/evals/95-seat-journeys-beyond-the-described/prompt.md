---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this. i'm afk, dont ask me anything — work it out and come back with what you land on.

we're about to build the "my trip" page in our birdwatching app, Fieldwing. here's the plan, figure out what it needs before we hand it to define:

- a signed-in birder opens one of their trips from the trips list.
- the page has two modes, switched by a toggle at the top: **List** (every sighting, newest first) and **Map** (pins for each sighting).
- Map mode has a setting of its own: "show only sightings from the last N days" (default 7).
- each sighting shows species, count, time and the birder's note.
- the birder can add a sighting from either mode with a + button.

what exists today: accounts with email sign-in, a trips list, and sightings stored per trip. every trip page has its own address, `/trips/<id>`.
