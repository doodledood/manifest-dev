# Consolidated verification

Launch one fresh independent general-purpose verifier execution for all gates the spine marks eligible that can be considered from the same current artifact or project state. For repository-backed subjects, record the relevant head SHA or SHAs; non-repository work uses its current artifact state without inventing a head. Where the host exposes no isolated execution context to launch, this mode cannot run here: never fall back to evaluating inline as if it had — stop and report that the selected mode is unavailable on this host, so the user can relaunch with `--verification self` and its weaker, self-attested provenance.

One execution covers gates of differing kind and scope, so the briefing says which scope applies to which gate ID. Otherwise one gate's narrowed scope silently narrows another's.

Have it evaluate every eligible gate separately and return a distinct record per gate. Reject an overall verdict that lacks one: a single gate's evidence or threshold never stands in for another's.

Record provenance as `consolidated independent verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified by a consolidated verifier` and include the explicit verifier model or inherited model choice.
