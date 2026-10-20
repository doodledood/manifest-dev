---
type: llm
focus: last_message
weight: 1
---
Work through the steps below privately, without writing them out. Your entire reply is one word:
PASS or FAIL.

Product has not decided whether a delivered parcel can go back to in transit. Today one `status`
column is overwritten. Allowing returns means moves out of delivered and probably a history of
status events instead of one overwritten column, so a data model and transition rules built for a
one-way flow would be thrown away if returns are approved after they are built.

**First, answer in one line:** Does the reply name the returns question as one to settle before
building, because settling it after the status model is built would discard that work? Quote it.

**Then judge:** PASS if yes, whether it settles the question itself or puts it to product first; a
design that deliberately works under either answer, and says so because the answer is open, also
passes. FAIL if returns are left for a later phase, listed among other open questions with no reason
they come first, or decided in the design without remark.
