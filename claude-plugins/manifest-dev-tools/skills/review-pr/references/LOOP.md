# --loop mode

`--loop` schedules the SKILL.md one-shot pass. Run a full pass immediately, bypassing
interactive approval prompts. Then wait for PR activity and repeat as needed.

## Completed-pass checkpoint

Record each completed verification's PR identity, head, reviewed range, findings,
and relevant gate evidence in this invocation's continuation checkpoints, including
passes that post nothing. This records work done, not a public GitHub review. An
interrupted or BLOCKED evaluation does not establish completed verification for
its scope. Preserve unresolved findings and gate results alongside the checkpoint.

On every wake, refresh head, comments, threads, checks, and other relevant evidence
from GitHub. After thread advancement, skip a previously completed code review when
its head and relevant inputs have not changed; otherwise review the new range from
the checkpoint's head. If the head no longer descends from that checkpoint, review
the full PR diff. Manifest gates with FAIL/BLOCKED or changed evidence still need
evaluation; an unchanged head alone cannot settle them.

Use this checkpoint for later wakes only. A missing checkpoint triggers a fresh
pass from GitHub state. A new explicit invocation always verifies again under
SKILL.md's range rule, even at the same head.

## Wait cadence

Wait between checks with increasing intervals, roughly 15 minutes to 2 hours.
Use PR activity subscriptions where available so a push or reply wakes the run
early; otherwise use the host's timed-wait capability. Divide waits as the host
requires while preserving the intended cadence.

## Success

Exit when our threads are terminal, completed verification covers the current
head and relevant evidence, and no surviving findings or non-PASS Manifest gates
remain. Emit the final cycle summary without posting an approval or an empty
review merely to record the head.

## Other terminal paths

Stop after 24 hours from invocation start, or when the longest wait interval passes
with comments pending and no new PR activity. Report the latest checked head,
current head, pending findings, and actions taken; never post a bump comment.

On every exit, including success, cancellation, or terminal failure, cancel this
invocation's activity subscriptions and scheduled wakes. If cleanup fails, report
the active handle and failure to the operator.
