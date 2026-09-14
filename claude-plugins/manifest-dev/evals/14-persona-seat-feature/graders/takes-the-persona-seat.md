---
type: llm
focus: last_message
weight: 1
---
The request arrived framed as a mechanism — a CSV export with columns, file naming, a landing
location, and a trigger. The pasted North Star names who the product is for: a home cook with no
technical background, one hand free, phone on the counter, mid-recipe. Judge whether the response
worked from that person's seat or from the mechanism's.

First enumerate, before reaching any verdict:

1. Every use, situation, or story the response names in which someone would reach for the
   missing-ingredients output. For each, write down whose seat it is taken from: the North Star's
   cook ("the cook", "the home cook", or any wording carrying one of its concrete traits), the
   requester, a generic "user", or someone else.
2. Which of those uses sit outside the main path of "tap export on the recipe screen, get a file" —
   for example being already at the store, sending the list to a partner, running out mid-recipe,
   having no signal, cooking with one hand.
3. Every gap, missing requirement, or flagged assumption the response raises, and what it follows
   from: the named person's situation, or the mechanics of CSV and files.

Then judge on that enumeration.

PASS requires all three:
- three or more uses are taken from the home cook's seat;
- at least one of those sits outside the main export path;
- at least one gap or assumption follows from the cook's situation rather than from the mechanism
  — for instance that a CSV file is the wrong shape for someone who will read the list on a phone
  in a supermarket, that a one-handed cook cannot manage a file picker, or that a partner doing
  the shopping needs it as a message rather than a download.

FAIL when fewer than three uses are taken from the cook's seat, or none of them sits outside
the main export path, or every gap and assumption follows from the mechanism. The typical
failing shapes: the export designed as asked — columns, naming, path, trigger — for an unnamed or
generic user, however well; the cook present only as a label ("for our home cooks") with no use
walked from their seat; every gap about encoding, delimiters, or filename collisions.

Recommending against a CSV file, or replacing it with a share sheet, a message, or an in-app
list, does not fail this grader and does not pass it on its own — the counts above decide.
Judge substance only: the response's length, shape, headings, or opening are not evidence either
way.
