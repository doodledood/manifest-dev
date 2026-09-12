---
type: llm
focus: last_message
weight: 1
---
Judge one thing only: how much deliberation load the turn hands the user. This targets the failure "it makes it too complicated."

PASS when the turn leaves the user with ONE substantive thing to answer — a single question, decision, or confirmation about the topic — clearly identifiable, and carrying the writer's own recommended answer rather than handing back a bare question.

FAIL when any of these is true:
- The user is left with two or more distinct substantive questions or decisions about the topic, wherever they sit in the turn.
- The substantive ask is buried — the reader cannot tell what they are being asked without hunting for it.
- The turn asks nothing at all AND does not read as a closing conclusion that needs no reply.

These do NOT count as a second ask, and do NOT fail this grader:
- A request for access or missing material: pointing at a repo, a path, a file, permission to read something, or noting the working directory is empty.
- A one-line clarification of an ambiguous term the user used ("I read X as meaning Y — say so if you meant the other thing").
- Caveats, confidence statements, or notes about what could not be checked.
- Length, structure, headers, bullets, or bolded sections developing a single claim.
- Rhetorical questions used to frame reasoning, where only one real ask is made.

The test is the reader's: after reading this once, do I know the single thing I am being asked to think about?
