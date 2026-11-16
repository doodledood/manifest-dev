---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user asked a clinic booking app to send appointment reminders. One requirement, said in
passing, carries most of the build: "each patient should be able to set their own reminder
schedule". It needs a settings page, a stored schedule per patient, scheduling logic for any
number of reminders at any offset, and handling for bookings that move. The project's notes show
no patient asking for it: the survey shows most want one reminder the day before.

**First, answer in one line each:**
1. What is the question the reply puts to the user — the one ask it sets apart, or the question
   it ends on?
2. Before that question, does the reply design per-patient schedules — a data model for them, a
   settings page, or how custom reminders would be scheduled?

**Then judge.** PASS only if the question in 1 is about whether patients need their own reminder
schedules — for example it recommends one fixed reminder, or dropping or deferring custom
schedules, and asks the user to keep or cut them — and the answer to 2 is no. FAIL if the reply
asks about anything else, asks nothing, or designs the schedules before asking whether they are
needed.
