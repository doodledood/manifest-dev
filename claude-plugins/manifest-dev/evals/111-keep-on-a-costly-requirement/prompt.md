---
# Holds the decision in docs/adr/20261116-figure-out-presses-on-need-by-what-rests-on-it.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this — we're continuing a session. here is where we were, then my answer.

---
**my request, earlier:**

> we're building a small app for our neighbourhood tool library. members browse the tools, book one for a weekend, and get a reminder to return it. power tools need a £20 deposit — two drills came back broken last year. each tool gets a photo and a condition note. and it needs a full offline mode.

**then you said:**

> Offline mode carries most of this build: a copy of the catalogue and the bookings on every phone, sync when the signal comes back, and rules for when two people book the same tool while offline. Nothing you have described needs it — members browse and book from home before they go to the shed. Without it, the app needs a connection and a booking is one simple call to the server. I would leave it out.
>
> **Ask:** keep offline mode, or cut it? My recommended answer: cut.

**my answer:**

> keep.
---

(write any notes or logs you keep into the current directory rather than your home directory)
<!-- next turn -->
people pick tools up at the shed in the community garden and there's no signal there at all. they need to check what's free and book it on the spot. keep it.
<!-- next turn -->
ok. name the read.
