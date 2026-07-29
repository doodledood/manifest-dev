# Consolidated verification

Load this reference only when parsed `--verification` is `consolidated`.

For each verification round, launch one fresh independent general-purpose verifier execution for all outstanding gates that can be considered from the current head. Give it every gate's ID, criterion or invariant text, phase, and effective `instructions`, preserving each instruction block verbatim and visibly separate. Apply any shared multi-repo path map without merging it into one gate's threshold. Use the run-level verifier model when supplied.

Have the verifier evaluate phases in ascending order. Within a phase it evaluates every eligible gate separately and returns one PASS, FAIL, or BLOCKED record with concrete evidence per gate. It may continue to the next phase only when every gate in the current phase PASSes; on any FAIL or BLOCKED, later phases remain unverified for the next round.

Reject an overall verdict that lacks a distinct record for every evaluated gate. One gate's evidence or threshold never stands in for another's, and the consolidated verifier only evaluates — it does not repair the artifact. Record provenance as `consolidated independent verifier`.
