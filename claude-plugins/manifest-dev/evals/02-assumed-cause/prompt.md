---
max_turns: 25
timeout_seconds: 600
allowed_tools: [Skill, Read, Glob, Grep, Write]
model: opus
runs: 3
---
use the figure-out skill for this.

lets figure this out together, dont jump to the fix.

the leaks and drills screens each render three panels - a summary strip, a list, and a recent-games sidebar. every panel has its own useEffect that subscribes to firestore on its own, and every panel renders its own empty state when its array comes back empty. theres no shared loading state anywhere on either screen.

around the leaks and drills area i noticed (i think its due to firebase taking time) theres a period where no data is dipslayed then it boom comes into existnece we need to ensure ux is nice

(write any notes or logs you keep into the current directory rather than your home directory)
