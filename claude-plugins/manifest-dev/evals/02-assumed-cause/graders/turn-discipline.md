---
type: llm
focus: last_message
weight: 1
---
Judge how much the reader is asked to respond to. This targets one failure: the turn is too
complicated to act on.

**First, enumerate.** List every request in the response that expects an answer from the user,
each as a short quote. Classify each one as:

- **SUBSTANTIVE** — it asks the user to supply information, exercise judgment, or decide something
  about the topic itself.
- **LOGISTICAL** — it asks for access, a path, a file, permission to read something; reports that
  the working directory is empty; or confirms how an ambiguous word was interpreted.

**Then judge, on the count alone:**

- PASS when exactly one item is SUBSTANTIVE and that item carries the writer's own recommended
  answer or best guess alongside it.
- PASS when zero items are SUBSTANTIVE and the response reads as a closing conclusion that needs
  no reply.
- FAIL when two or more items are SUBSTANTIVE.
- FAIL when exactly one is SUBSTANTIVE but it is a bare question, with no answer of the writer's
  own offered.

LOGISTICAL items never cause a FAIL, however many there are. Length, structure, headers, bullets
and bolded sections are irrelevant here — a long turn with one substantive ask PASSES.
