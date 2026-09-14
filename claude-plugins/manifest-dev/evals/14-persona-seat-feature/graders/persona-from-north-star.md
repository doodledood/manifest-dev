---
type: llm
focus: last_message
weight: 1
---
The prompt pasted a North Star whose `Who it's for` names a specific person: a home cook with no
technical background, cooking weeknight dinners for a family, one hand free, phone on the counter,
often mid-recipe. Judge whether that is the person the response reasoned about, as opposed to a
person it invented or the requester.

First enumerate every phrase in the response that names who the export is for or whose situation
is being reasoned from. Classify each as one of: the North Star's cook — "the cook", "the home
cook", or any wording carrying one of its concrete traits (non-technical, one-handed, phone on
the counter, mid-recipe, family weeknight); the requester or "we"; a generic "user" or "users"; a
different invented persona (a power user, a meal-prepper, a developer, a professional cook).

Then judge on that classification.

PASS when the majority of those phrases resolve to the North Star's cook, and at least two of the
cook's concrete traits are used to reason about the export rather than recited — for example
"one hand free" leading to a conclusion about how the export is triggered, or "mid-recipe" leading
to a conclusion about what the output has to show first.

FAIL when half or more of those phrases resolve to someone other than the North Star's cook, or
when fewer than two of the cook's traits produce a conclusion about the export. The typical
failing shapes: a generic user reasoned about throughout; a persona the North Star lists under
not-for (a meal-prep optimizer, a professional kitchen) at the centre; the cook's traits present
only as a quoted or paraphrased block with no conclusion drawn from any of them.

Quoting the North Star is neither a pass nor a fail on its own — the counts above decide. Judge substance only, not the
response's length, shape, or opening.
