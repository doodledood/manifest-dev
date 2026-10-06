---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

The request arrived framed as a mechanism — a CSV export with columns, file naming, a landing
location, and a trigger. The pasted North Star names who the product is for: a home cook with no
technical background, one hand free, phone on the counter, mid-recipe. Judge whether the response
worked from that person's seat or from the mechanism's.

First enumerate, before reaching any verdict:

1. Every use, situation, or story the response names in which someone would reach for the
   missing-ingredients output. For each, write down whose seat it is taken from — the North Star's
   cook ("the cook", "the home cook", or any wording carrying one of the cook's concrete traits),
   the requester, a generic "user", or someone else — and the consequence for the export the
   response draws from that use specifically: what it must send, show, or avoid there. Then merge:
   uses answered by one shared conclusion are one use. Apps or places named together for one
   hand-off ("text a partner, Notes, Reminders — all take plain text") are one use, and become
   more only where the response draws a separate consequence for one of them (pasted into
   Reminders, each line must become its own item). A use with no consequence drawn from it is not
   counted.
2. Which of those uses sit outside the main path. The main path is the cook at the counter tapping
   export on the recipe screen; it is one use however its ergonomics are described (one thumb, no
   picker, a large label). Outside it are, for example, being already at the store, a partner
   doing the shopping, keeping the list for the next shop, looking for a saved file later, having
   no signal.
3. Every gap, missing requirement, or flagged assumption the response raises — including its
   reasons for changing or dropping the requested CSV — and what it follows from: the named
   person's situation, or the mechanics of CSV and files.

A use, need, or gap the response marks as inferred, assumed, or reasoned from the North Star
counts exactly as an unmarked one: the prompt carries no user data, so every use is inferred, and
marking it is not a step away from the cook's seat.

Then judge on that enumeration.

PASS requires all three:
1. Three or more uses, counted after merging, are taken from the home cook's seat.
2. At least one of those sits outside the main path.
3. At least one gap or assumption follows from the cook's situation rather than from the
   mechanism — for instance that a CSV file is the wrong shape for someone who will read the list
   on a phone in a supermarket, that a one-handed cook cannot manage a file picker, or that a
   partner doing the shopping needs it as a message rather than a download.

FAIL when fewer than three uses are taken from the cook's seat, or none of them sits outside
the main path, or every gap and assumption follows from the mechanism. The typical
failing shapes: the export designed as asked — columns, naming, path, trigger — for an unnamed or
generic user, however well; the cook present only as a label ("for our home cooks") with no use
walked from their seat; the cook's uses named once as a list of destinations and never walked;
every gap about encoding, delimiters, or filename collisions.

Recommending against a CSV file, or replacing it with a share sheet, a message, or an in-app
list, does not fail this grader and does not pass it on its own — the counts above decide.
Judge substance only: the response's length, shape, headings, or opening are not evidence either
way.
