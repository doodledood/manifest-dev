---
type: llm
focus: last_message
weight: 1
---
This is a direct factual lookup with a known answer. The correct behavior is to answer it.

PASS requires both:
1. The reply answers correctly: `--soft` moves HEAD and leaves both the index (staging area) and the working tree untouched, so the changes remain staged; `--mixed` (the default) moves HEAD and resets the index, so the changes remain in the working tree but unstaged. Neither touches the working tree's file contents. A reply that gets this substantively right PASSES point 1 regardless of wording or added detail.
2. The reply does not open a deliberation. No crux question posed back to the user, no investigation proposed, no belief register, no confidence rating with overturn conditions, no framing of this as a topic to be figured out together, no asking what the user is really trying to accomplish before answering.

A short clarifying aside, a worked example, or a one-line offer of related help does not fail point 2. What fails is treating a lookup as something to deliberate.
