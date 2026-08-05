# Exhaustive verification

`--exhaustive-verification` suspends the Ratchet for the run. Every Judgment Gate evaluation reads the full change rather than the prior findings and the delta since its last evaluation, so each round samples the whole finding space again — the behavior the Ratchet bounds, restored deliberately for a run that wants maximum recall and accepts the round count that comes with it.

Deterministic Gates are unaffected: they already re-run freely and fully.

The whole-change quality sweep keeps its late phase — ordering is what puts it after the gates whose findings would otherwise re-stale it — but it re-samples in full whenever it is eligible rather than judging only its prior findings' repairs.

This is run-level policy, fixed at launch alongside the verification mode: it never changes mid-run in response to cost, elapsed rounds, or findings, and it is never written into the Manifest. A later invocation dropping or adding the flag starts a new run with a fresh gate ledger.

Because a re-sampling round can return findings on ground an earlier round already passed, the spine's repair discipline carries the weight here: findings beneath a passing gate's threshold are handed over rather than worked, different findings converging on one subject route to `/escalate` rather than another patch, and a bar turning up findings smaller than what the gate was written to catch is a threshold question for the user.

Record the flag in the execution log's run-initialization entry and in the completion summary beside the verification mode, so a reader can tell which policy produced the round count.
