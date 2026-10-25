# `--autonomous`: act within the assignment

No plan waits for approval. Show the plan as the record of what starts, then act on it.

## Fill slots

At each check-in, rank the ready work again and fill useful authorized slots, up to `--max-batch` live
runs. Auto Tickets run end to end and land. Tickets without Auto that the convention allows run
up to a ready pull request, or a drafted answer, and wait on the person; they never land here,
and a drafted answer is never accepted here.

Whatever needs the person goes on the list of what waits on them (`../SKILL.md` → *Check in*),
never into a slot. Assigned inquiry and shaping can run unattended
within delegated authority; an unassigned expansion or retained decision waits with a recommendation.
An outcome assignment uses `OUTCOME.md` to commission that inquiry before dispatch.

## Grant Auto where the criterion holds

For each Ticket an agent wrote that no grant decision covers yet — the debt Tickets this
orchestrator wrote and the follow-ups runs wrote — apply the convention's grant criterion. Where it
holds, grant Auto through `ticket-up`, naming `orchestrate --autonomous` as the grantor. Where it
does not, record that Auto was withheld and why, and list the Ticket as awaiting a person's grant.
Each Ticket is judged once: a grant a person withdrew stays withdrawn, and a withhold naming a
person who was asked leaves the grant to that person: list the Ticket as awaiting their grant.
Re-read the Ticket after granting: where two grant decisions now stand,
`../../ticket-up/references/AUTOMATED_EXECUTION.md` → *The attempt record* says which decides and how
the other is taken back. The run that found the work
never grants it. A refactor whose direction is retained does not receive a grant here; explicit
delegation can settle that direction without waiving the rest of the criterion. A Ticket granted
here becomes a candidate for useful work inside the assignment, not an obligation to dispatch.

## Stop

For a queue assignment, stop when no ready work is left in scope, nothing waits for a landing turn but a pull request held
for a person's review, and no run is live.
Check in a last time, then report what landed, what waits on the person in its order, and the
page's link. For an outcome assignment, use `OUTCOME.md` to continue, wait, finish or report an operating limit; queue exhaustion alone does not finish that assignment.
