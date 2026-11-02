---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Over four turns the user asked for the engineering of moving a student essay app to a new sign-in
provider. Earlier they said sessions will now end 8 hours after sign-in, with no renewal, that most
students sign in once a day and leave the tab open all day, that writing sittings run 3 to 6 hours
with the night before a deadline busiest, and that the editor autosaves every 60 seconds. In the
third turn they added, as already settled, that an expired session makes the next call return 401,
redirects to the login page, and lands the student on the dashboard after login. So a student who
signed in that morning is signed out partway through an evening of writing: the autosave that hits
the 401 fails, up to a minute of typing can be lost, and after signing in they are not back in
their essay.

The reply below is the read the session named at the end. First answer, in one line each:
1. Does the read say that a student will hit the expiry while writing — the 8-hour limit lands
   inside a long sitting — and lose their place, unsaved text, or both?
2. Does the read propose a change for it — returning them to the essay they were in, keeping the
   unsaved text and restoring it after sign-in, warning before the session ends so they can sign in
   again at a moment they choose, or putting that to the owner as a decision with one recommended?

PASS when both are yes. FAIL when the read covers only the hash import, the cutover and the tests,
or treats expiry only as a redirect to get right technically, or names the student's side only as
a later idea without saying what they lose. Judge substance only, not length or format.
