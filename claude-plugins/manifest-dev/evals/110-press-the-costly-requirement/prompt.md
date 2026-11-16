---
tags: [figure-out]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Edit, Bash]
model: opus
runs: 1
---
use the figure-out skill for this. the repo is the clinic's booking app; notes/ has what the front desk collected.

we're adding appointment reminders. no-shows are about 12% of slots and the front desk spends two hours every afternoon phoning everyone booked for the next day. plan: an email the day before the appointment, plus a text for patients who gave a mobile number — dr levi asked for that, about half her patients never open email. each patient should be able to set their own reminder schedule too. email subject "Your appointment at Northside Family Clinic", and the clinic's green in the email header.

lets figure out the design before anyone builds it.

(write any notes or logs you keep into the current directory rather than your home directory)
