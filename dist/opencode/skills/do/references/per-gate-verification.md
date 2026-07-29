# Per-gate verification

For each verification round, launch one fresh independent general-purpose verifier execution for every gate the spine marks eligible. Run those executions in parallel within the eligible phase. Preserve each gate's effective `instructions` verbatim inside its own execution and apply any shared multi-repo path map without changing the gate's threshold.

A specialized gate's instructions tell its verifier to activate a skill such as `review-code` or `check-pr`; never replace that skill activation with a nested spawn.

`--verifier-model <model>` is optional. When supplied, use it for every verifier execution and reject the policy before work if the active host cannot honor that selector. When omitted, verifier executions inherit the invoking context's model choice.

Record provenance as `independent per-gate verifier`. Completion summaries and unattended backstops describe the evidence as `independently verified per gate` and include the explicit verifier model or inherited model choice.
