# Consolidated verification

For each verification round, launch one fresh independent general-purpose verifier execution for all outstanding gates that can be considered from the same current artifact or project state. For repository-backed subjects, record the relevant head SHA or SHAs; non-repository work uses its current artifact state without inventing a head.

The execution is **pointed at the gates, never handed copies of them**: give it the Manifest's absolute path and the set of eligible gate IDs, and tell it to read each gate's text from the file. Carry the spine's framing line with it — evaluate each named gate as written, and treat nothing else in the Manifest as binding on any verdict. Apply any shared multi-repo path map without merging it into one gate's threshold. Use the run-level verifier model when supplied. A Manifest path the execution cannot read returns BLOCKED for every gate in the set.

Have the verifier evaluate every gate the spine marks eligible separately and return one PASS, FAIL, or BLOCKED record with concrete evidence per gate.

One execution evaluates gates of both kinds, so the briefing carries each gate's scope with it, taken from that gate's declared kind — scope is run state rather than Manifest content. A Deterministic Gate is given the current artifact state and re-run in full. A Judgment Gate on its first evaluation is given the full change; on any later evaluation — unless its own body suspends the Ratchet, which gives it the full change again — it is given the findings it reported last time and the delta since the artifact state it read then — for repository work, that state's head SHA against the current one — and told to judge only whether those findings are repaired and whether the delta introduces anything its criterion catches. Say which scope applies to which gate ID in the same briefing, so one gate's narrowed scope never silently narrows another's.

Reject an overall verdict that lacks a distinct record for every evaluated gate. One gate's evidence or threshold never stands in for another's, and the consolidated verifier only evaluates — it does not repair the artifact.

`--verifier-model <model>` is optional. When supplied, use it for the verifier execution and reject the policy before work if the active host cannot honor that selector. When omitted, the verifier execution inherits the invoking context's model choice.

Record provenance as `consolidated independent verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified by a consolidated verifier` and include the explicit verifier model or inherited model choice.
