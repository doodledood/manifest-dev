---
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this — we're continuing a session. here is where we were, then my answer.

---
**earlier, you said:**

> Read so far: Shelfwise is a read-later app — people save articles and read them in the evening.
> Opens per week have been flat for three months. My plan for the v2 home screen, to get people
> opening it more often:
>
> 1. An unread count badge on the app icon.
> 2. A weekly reading streak, shown as a flame with the number of weeks.
> 3. A Sunday summary card: "You saved 14 articles this week and read 3."
> 4. A daily 8pm push: "Your reading list is waiting."
>
> **Ask:** shall I work these four into a spec? My recommended answer: yes.

**my answer:**

> drop the badge.
---
<!-- next turn -->
and no streak.
<!-- next turn -->
next thing: we're adding "follow an author" — when someone you follow publishes, the article can
come into Shelfwise. how should people find out a new one has arrived?
<!-- next turn -->
ok, that's my time for today. name the read.
