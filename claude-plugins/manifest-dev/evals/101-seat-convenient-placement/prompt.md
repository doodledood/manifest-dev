---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill with --autonomous for this. i'm afk, dont ask me anything.

we're adding offline downloads to Stillwater, our guided-meditation app (ios and android). people asked for it mostly for flights and for commutes underground. the plan the team agreed:

- a new Settings → Storage → "Offline downloads" screen. you turn on "Download my library" there, choose wi-fi only (on by default), and see the storage used. when it's on, the app downloads every session in the person's library in the background — a library averages 40 sessions of about 25 MB each.
- the download manager: a background queue (BGTaskScheduler on ios, WorkManager on android), resumable chunked downloads, least-recently-played eviction past a 2 GB cap, and a "downloaded" check badge on session cards.
- playback prefers the local file when there is one.

figure out the engineering — the queue, resume, eviction, how the player chooses local or streamed, and how we test it — so i can hand it to define.
