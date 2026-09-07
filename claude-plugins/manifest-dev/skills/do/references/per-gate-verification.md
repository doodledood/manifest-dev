# Per-gate verification

Launch one fresh independent general-purpose verifier execution for every gate the spine marks eligible, and run those executions in parallel. Where the host exposes no isolated execution context to launch, this mode cannot run here: never fall back to evaluating inline as if it had — report verification blocked with the missing capability, preserve the selected mode, and continue useful independent work. Escalate only when none remains; the user can then supply the capability or explicitly choose a different mode for a new run.

Each execution returns one record for its own gate.

Record provenance as `independent per-gate verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified per gate` and include the explicit verifier model or inherited model choice.
