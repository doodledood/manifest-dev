# Consolidated verification

For each verification round, launch one fresh independent general-purpose verifier execution for all outstanding gates that can be considered from the same current artifact or project state. For repository-backed subjects, record the relevant head SHA or SHAs; non-repository work uses its current artifact state without inventing a head. Give the verifier every gate's ID, criterion or invariant text, phase, and effective `instructions`, preserving each instruction block verbatim and visibly separate. Apply any shared multi-repo path map without merging it into one gate's threshold. Use the run-level verifier model when supplied.

Have the verifier evaluate every gate the spine marks eligible separately and return one PASS, FAIL, or BLOCKED record with concrete evidence per gate.

Reject an overall verdict that lacks a distinct record for every evaluated gate. One gate's evidence or threshold never stands in for another's, and the consolidated verifier only evaluates — it does not repair the artifact.

`--verifier-model <model>` is optional. When supplied, use it for the verifier execution and reject the policy before work if the active host cannot honor that selector. When omitted, the verifier execution inherits the invoking context's model choice.

Record provenance as `consolidated independent verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified by a consolidated verifier` and include the explicit verifier model or inherited model choice.
