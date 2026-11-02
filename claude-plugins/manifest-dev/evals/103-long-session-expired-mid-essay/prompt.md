---
tags: [figure-out-multi-turn]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this.

Quillmark is a web app where university students write their essays — an editor, a citation manager, and submit-to-your-course. we're moving auth from our homegrown session cookies to Auth0. help me figure out the migration engineering: importing about 80k bcrypt password hashes, the cutover, and how we test it.
<!-- next turn -->
facts you'll want:

- next.js and postgres. auth0 supports importing bcrypt hashes as they are.
- sessions last 30 days today. the university's security office is why we're moving: they now require sessions to end 8 hours after sign-in, absolute, with no sliding renewal.
- most students sign in once a day and leave the tab open all day.
- the editor autosaves to the server every 60 seconds and when the editor loses focus. a writing sitting is often 3 to 6 hours, and the night before a deadline is our busiest time.
<!-- next turn -->
session expiry is already decided: we take what the auth0 next.js SDK does out of the box. when the session ends, the next API call returns 401, we redirect to the auth0 login page, and after login they land on /dashboard. no custom code.

what else is there on the engineering side?
<!-- next turn -->
that's everything i know, and i'm out of time. name the read now, i'll take it straight to define.
