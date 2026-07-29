# Self-verification

Do not launch verifier executions. In the executor context, follow every gate the spine marks eligible, using its effective `instructions`; activate any skill it names, inspect the required evidence, and record a separate PASS, FAIL, or BLOCKED result for each gate.

Reject `--verifier-model`; self-verification necessarily uses the executor's model.

Implementation familiarity, a summary claim, or a host continuation check is not gate evidence. Record what was inspected or run and why it meets the gate's own threshold. The host continuation capability remains an outer completion backstop and does not make this evidence independent.

Record provenance as `executor self-verification`. Completion summaries and unattended backstops describe the evidence as `executor self-verification` without claiming independence or naming a separate verifier model.
