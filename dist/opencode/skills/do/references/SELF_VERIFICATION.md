# Self-verification

Load this reference only when parsed `--verification` is `self`.

Do not launch verifier executions. In the executor context, follow every eligible gate's effective `instructions`, activate any skill they name, inspect the required evidence, and record a separate PASS, FAIL, or BLOCKED result for each gate. Respect phase ordering and stop before a later phase when the current phase contains a non-PASS verdict.

Implementation familiarity, a summary claim, or a host continuation check is not gate evidence. Record what was inspected or run and why it meets the gate's own threshold. The host continuation capability remains an outer completion backstop and does not make this evidence independent. Record provenance as `executor self-verification`.
