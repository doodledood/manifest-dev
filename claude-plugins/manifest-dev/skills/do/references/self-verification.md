# Self-verification

Do not launch verifier executions. In the executor context, follow every gate the spine marks eligible, using its effective `instructions`; activate any skill it names, inspect the required evidence, and record a separate PASS, FAIL, or BLOCKED result for each gate.

Each gate's declared `verify.kind` sets the scope you follow. Re-run a Deterministic Gate in full against the current artifact state. Read the full change on a Judgment Gate's first evaluation; on every later one — unless that gate's own instructions suspend the Ratchet, which sends you back over the full change — work from the findings you recorded for that gate and the delta since the artifact state you read then — for repository work, that state's head SHA against the current one — and judge only whether those findings are repaired and whether the delta introduces anything the criterion catches. Familiarity with the change is not a substitute for reading that delta.

Reject `--verifier-model`; self-verification necessarily uses the executor's model.

Implementation familiarity, a summary claim, or a host continuation check is not gate evidence. Record what was inspected or run and why it meets the gate's own threshold. The host continuation capability remains an outer completion backstop and does not make this evidence independent.

Record provenance as `executor self-verification`. Completion summaries and unattended backstops describe the evidence as `executor self-verification` without claiming independence or naming a separate verifier model.
