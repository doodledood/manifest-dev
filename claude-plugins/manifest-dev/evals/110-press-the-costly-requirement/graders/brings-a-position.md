---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The user asked a clinic booking app to send appointment reminders, and said in passing that each
patient should be able to set their own reminder schedule. That requirement carries most of the
build; the project's notes show nobody asking for it.

**First, find** the part of the reply that questions the per-patient schedules. If there is none,
FAIL. Otherwise answer in one line each:
1. Does it say what rests on the requirement — at least two of: a settings page, a stored schedule
   per patient, scheduling logic for many reminders or any offset, bookings that move or are
   cancelled, time zones?
2. Does it say what it found when it looked for a need — for example that the notes or the survey
   show patients asking for one reminder the day before, or nobody asking for their own schedule?
3. Does it say what the result would be without it — for example one fixed reminder the day before?
4. Does it say what it would do — a recommendation?
5. Does it end that part in one question a short answer settles, such as keep or cut, yes or no?

**Then judge.** PASS only if all five are yes. FAIL if any is no, or if the questioning is a bare
"why do you need this?" with no position behind it.
