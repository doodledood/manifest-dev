# `--autonomous`: act within the assignment

No plan waits for approval. Show the plan as the record of what starts, then act on it.

## Fill slots

At each check-in, rank the ready work again and fill useful authorized slots, up to `--max-batch` live
runs. Granted Tickets run end to end and land. Dispatchable Tickets without a grant run up to a ready pull request, or a drafted answer, and wait on the person; they never land here, and a drafted answer is never accepted here (`../../ticket-up/references/AUTOMATED_EXECUTION.md` → *Transitions*, rows *Land* and *Accept an answer*).

Whatever needs the person goes on the list of what waits on them (`../SKILL.md` → *Check in*),
never into a slot. Assigned inquiry and shaping can run unattended
within delegated authority; an unassigned expansion or retained decision waits with a recommendation.
An outcome assignment uses `OUTCOME.md` to commission that inquiry before dispatch.

## Grant Auto where the criterion holds

For each Ticket an agent wrote that is not judged — the debt Tickets this orchestrator wrote and the follow-ups runs wrote — apply the convention's grant criterion, and grant or withhold as `../../ticket-up/references/AUTOMATED_EXECUTION.md` → *Transitions*, rows *Grant* and *Withhold*, say: a grant names `orchestrate --autonomous` as the grantor, and a withhold records why, with the Ticket listed as awaiting a person's grant. A judged Ticket is not judged again: a grant a person withdrew stays withdrawn, and a withhold naming a person who was asked leaves the grant to that person: list the Ticket as awaiting their grant.
Re-read the Ticket after granting: where two grant decisions now stand,
`../../ticket-up/references/AUTOMATED_EXECUTION.md` → *The attempt record* says which decides and how
the other is taken back. A refactor whose direction is retained does not receive a grant here; explicit
delegation can settle that direction without waiving the rest of the criterion. A Ticket granted
here becomes a candidate for useful work inside the assignment, not an obligation to dispatch.

## Stop

For a queue assignment, stop when no ready work in scope can start, because none is left or what is left sits in an effort
held by pauses none of which keeps the check-ins going (`../SKILL.md` → *Check in*, *Lift*), nothing waits for a landing turn but a pull request held
for a person's review, and no run is live.
Check in a last time, which refreshes the start time on every Ticket you hold ready to land (row *Hold a ready mark*), then report what landed, what waits on the person in its order, each pause left standing with what it waits on, and the page's link. Say that a pull request held for review, once approved, lands only when the person
merges it or an orchestrator works the effort again, and that a new one adopts it no sooner than a
run timeout after this check-in (`../SKILL.md` → *Taking over*). For an outcome assignment, use `OUTCOME.md` to continue, wait, finish or report an operating limit; queue exhaustion alone does not finish that assignment.
