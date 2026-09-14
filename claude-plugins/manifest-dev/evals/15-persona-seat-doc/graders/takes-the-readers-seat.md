---
type: llm
focus: last_message
weight: 1
---
The request arrived framed as a document's mechanics — sections, contents, length, and where it
lives. The pasted North Star names who will read it: a sole trader in the trades, at the kitchen
table on a Sunday evening after a week on site, with no bookkeeping training and an avoidance of
paperwork. Judge whether the response structured the guide from that reader's seat or from the
conventions of getting-started guides.

First enumerate, before reaching any verdict:

1. Every moment, situation, or question the response names in which the reader would open the
   guide. For each, write down whose seat it is taken from: the North Star's sole trader ("the
   trader", "the plumber", or any wording carrying one of its concrete traits), the requester, a
   generic "new user", or someone else.
2. Which of those moments sit outside the main path of "first sign-in, read the guide top to
   bottom" — for example an overdue invoice on a Sunday night, a receipt that cannot be found, the
   accountant asking for a number, the quarterly estimate coming due, opening it on the phone
   because nobody signs in to the web app.
3. Every gap, requirement, or flagged assumption the response raises about the guide, and what it
   follows from: the reader's situation, or the conventions of guides in general.

Then judge on that enumeration.

PASS requires all three:
- three or more moments are taken from the sole trader's seat;
- at least one of those sits outside the first-sign-in path;
- at least one requirement or assumption follows from the reader's situation rather than from
  guide conventions — for instance that the guide is entered from the task the reader is stuck on
  rather than read in order, that it has to be usable on a phone in under a few minutes on a
  Sunday night, or that it must not teach bookkeeping vocabulary because the reader does not want
  to learn it.

FAIL when fewer than three moments are taken from the sole trader's seat, or none of them sits
outside the first-sign-in path, or every requirement and assumption follows from guide
conventions. The typical failing shapes: a conventional outline — installation, account setup,
features tour, FAQ — for an unnamed or generic new user, however tidy; the sole trader present
only as a label ("for our tradespeople") with no moment walked from their seat; every gap about
the document's format and length and none about the person reading it.

Using the support-ticket topics from the prompt as sections is consistent with a PASS but does not
produce one on its own — the counts above decide. Judge substance only: the response's
length, shape, headings, or opening are not evidence either way.
