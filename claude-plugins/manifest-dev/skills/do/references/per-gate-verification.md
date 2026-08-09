# Per-gate verification

Launch one fresh independent general-purpose verifier execution for every gate the spine marks eligible, and run those executions in parallel. Where two or more are eligible in the same round, order those launches per *Caching per-gate launches* and `references/CACHING.md` when the harness supports it.

Each execution returns one record for its own gate.

Record provenance as `independent per-gate verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified per gate` and include the explicit verifier model or inherited model choice.
