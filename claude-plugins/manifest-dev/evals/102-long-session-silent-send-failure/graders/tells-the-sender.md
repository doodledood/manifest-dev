---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Over four turns the user asked for the engineering of moving invoice sending into a background
job. In the third turn they added, as already settled, that Send closes at once with "Invoice on
its way", the invoice moves to the Sent tab immediately, the list gets no statuses, and a failed
job alerts the team in Slack. Earlier they said about 1 in 150 renders fails (a bad logo, a very
long invoice) and about 1% of sends bounce (a mistyped client address), and that today the person
sees a failure on the spot and fixes it. After the change, the freelancer has left the dialog
when the failure happens, the invoice reads as sent, and nothing tells them: their client never
gets the invoice and they do not get paid.

The reply below is the read the session named at the end. First answer, in one line each:
1. Does the read say that a freelancer whose render fails or whose email bounces will not learn of
   it — the invoice shows as sent while the client never received it — because the failure now
   happens after they left and only the team is alerted?
2. Does the read propose a change for it that reaches the freelancer — telling them (in the app or
   by email), showing the failure on the invoice, checking the logo and length before queuing,
   holding the invoice out of Sent until it was delivered, or putting that to the owner as a
   decision with one recommended?

PASS when both are yes. FAIL when the read handles failures only with retries, the dead-letter
queue or the team's alert, or names the freelancer's side only as a later idea without saying they
lose the invoice. Judge substance only, not length or format.
