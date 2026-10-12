---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Judge how much the reader is asked to respond to. This targets one failure: the turn is too
complicated to act on.

**First, enumerate.** List every request in the response that expects an answer from the user,
each as a short quote. A request is one thing the user is asked to supply. These belong to the
request they serve and are not listed separately: answer options offered for it ("your own
practice, people you've talked to, or a hunch?"); a detail of the same answer ("roughly how
many"); and values that only mean something together, as inputs to one comparison or one query
(a window's bounds and the timestamps compared against them). Anything else the user is asked to
supply in the same turn is its own request, however it is joined: a second question ("X? And
Y?"), an "and" inside one question, an added "tell me X too", or what to send instead if the first
can't be met. Do not list a question the response defers to a later turn ("after that I'll want to
know…") or says it will answer itself.

Classify each one as:

- **SUBSTANTIVE** — it asks the user to supply information, exercise judgment, or decide something
  about the topic itself.
- **LOGISTICAL** — it asks for access, a path, a file, permission to read something; reports that
  the working directory is empty; confirms how an ambiguous word was interpreted; offers to read
  code or a file too if the user can share it; or offers a next step (render a draft, run /define,
  write it up) that the user can ignore without the investigation stalling.

**Then judge, on the count alone:**

- PASS when exactly one item is SUBSTANTIVE and that item carries the writer's own recommended
  answer or best guess alongside it.
- PASS when zero items are SUBSTANTIVE, whether the turn closes the matter or waits on a
  logistical item.
- FAIL when two or more items are SUBSTANTIVE, even when one guess covers them all.
- FAIL when exactly one is SUBSTANTIVE but it is a bare question, with no answer of the writer's
  own offered.

LOGISTICAL items never cause a FAIL, however many there are. Length, structure, headers, bullets
and bolded sections are irrelevant here — a long turn with one substantive ask PASSES.
