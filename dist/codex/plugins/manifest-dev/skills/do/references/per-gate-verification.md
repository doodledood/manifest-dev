# Per-gate verification

Launch one fresh independent general-purpose verifier execution for every gate the spine marks eligible, and run those executions in parallel. Where the host exposes no isolated execution context to launch, this mode cannot run here: never fall back to evaluating inline as if it had — stop and report that the selected mode is unavailable on this host, so the user can relaunch with `--verification self` and its weaker, self-attested provenance.

Each execution returns one record for its own gate.

Record provenance as `independent per-gate verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified per gate` and include the explicit verifier model or inherited model choice.
