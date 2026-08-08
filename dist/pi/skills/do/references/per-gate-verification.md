# Per-gate verification

Launch one fresh independent general-purpose verifier execution for every gate the spine marks eligible, and run those executions in parallel. Each receives the Manifest's absolute path, the ID of the one gate it evaluates, and the run state the spine sends with it — that gate's scope, and the spine's framing line.

Each execution returns one PASS, FAIL, or BLOCKED record for its gate, with concrete evidence. An execution evaluates; it does not repair the artifact.

Record provenance as `independent per-gate verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified per gate` and include the explicit verifier model or inherited model choice.
