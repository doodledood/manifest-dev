# Consolidated verification

Launch one fresh independent general-purpose verifier execution for all gates the spine marks eligible that can be considered from the same current artifact or project state. It receives the Manifest's absolute path, the set of eligible gate IDs, and the run state the spine sends with them — each gate's scope, and the spine's framing line. For repository-backed subjects, record the relevant head SHA or SHAs; non-repository work uses its current artifact state without inventing a head.

One execution covers gates of both kinds and of differing scope, so the briefing says which scope applies to which gate ID. Otherwise one gate's narrowed scope silently narrows another's.

Have it evaluate every eligible gate separately and return a distinct PASS, FAIL, or BLOCKED record with concrete evidence per gate. Reject an overall verdict that lacks a record for every evaluated gate: one gate's evidence or threshold never stands in for another's. The consolidated verifier evaluates; it does not repair the artifact.

Record provenance as `consolidated independent verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified by a consolidated verifier` and include the explicit verifier model or inherited model choice.
