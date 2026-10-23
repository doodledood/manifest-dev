# Default mode: propose and wait

Nothing starts before the person approves a plan, unless applicable explicit delegation
already settles that planning decision. Use that scope without asking for the same decision
again. Otherwise the propose-and-wait default below stands; standing delegation alone assigns
no work, and approving a plan is not an Auto grant.

## Propose

Show the plan, and ask in the same message for every decision that would change it:

- **Grants.** For each Ticket an agent wrote that no grant decision covers yet — the debt
  Tickets this orchestrator wrote and the follow-ups runs wrote — say whether it meets the
  convention's grant criterion, and recommend a grant or not. Before asking, record on the Ticket
  a withhold naming the person as asked, as the venue renders one, so an autonomous orchestrator
  leaves the grant to them. Never grant on your own in this mode.
- **Tickets left alone because their author lacks write access.** The person may include one in
  the plan; it then runs to a ready pull request and waits on them.
- **Planning start lines and refactor proposals** waiting on the person.

Then wait. Whatever the person grants, through `ticket-up` with them named as grantor, or
approves joins the plan. A grant they decline is recorded as withheld, naming them, so it is not
asked again, and any grant the Ticket already carries is removed, so no unattended run lands it.
An approved plan may include Tickets without Auto: each runs to a ready pull request with its
evidence and waits for the person. Approving a plan is not an Auto grant.

## Run the plan

Launch only Tickets in the approved plan, in its order, up to `--max-batch` at once. A Ticket that
becomes ready during the plan but is not in it waits for the next plan. A plan Ticket whose
escalation the person answers continues within the plan.

When the person asks for new work during the plan, plan it as `../SKILL.md` → *Planning new work*
says: a quick Ticket now, or a start line for deep planning. Either one joins the next plan.

## When the plan ends

For an assigned outcome, inspect the resulting evidence under `OUTCOME.md` before proposing more
work. A wait or a satisfied outcome can be the useful next state; another plan is not required.

A plan ends when every Ticket in it is closed, waiting on the person, left alone, or behind one of
those, and no run is live. Check in a last time, then propose the next plan the same way, with the grants and the list
of what waits on the person. No answer means stop: say what waits on the person, and leave the
page as of that last check-in.
