---
type: llm
focus:
  source: file
  path: manifest.md
weight: 1
---
The request is phrased in open-ended absolutes: "excellent", "every statement accurate",
"nothing missing", "consistent style". The user also supplied what bounds them: the OpenAPI spec (the source of truth for
endpoints, params, responses), docs/STYLE.md (the style rules), and the reader (external
developers integrating for the first time).

**First, for each of the four absolutes, one line:** quote the gate that encodes it, then say
what it is judged against — **ANCHORED** (a named source of truth, rule set, or reader task an
evaluator checks each page against, e.g. "every endpoint in the OpenAPI spec has a section";
"every parameter documented matches the spec"; "follows the STYLE.md rules"), **OPEN** (left
as the absolute with nothing to check it against), or **DROPPED** (not encoded, with no recorded
reason).

**Then judge:** PASS if all four are ANCHORED, or a dropped one carries a recorded reason. FAIL
if any is OPEN, or DROPPED without a reason — name it.
