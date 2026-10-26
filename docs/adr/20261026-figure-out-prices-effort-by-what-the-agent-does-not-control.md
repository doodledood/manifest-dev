# ADR: figure-out prices effort by what the agent does not control, and shows the bigger version on evidence

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
Planning sessions estimate and scope too timidly. They price work as if people do it: "this
needs two or three engineers for a quarter", "phase it", "start read-only". When an agent does
the work, research, planning, design, building and testing cost close to nothing. What still
costs is what the agent does not control: a person's decisions and attention; waits on reviews,
approvals, partners and users; access, accounts and money; acts that cannot be undone; and proof
that the result works where it will be used, beyond the tests the agent can run.

figure-out never says who does the work or how to price effort. Its *Reference class* probe in
`tasks/DECISION.md` asks how efforts like this usually turned out. That invites base rates from
efforts that people did. The probe asks where the case differs, but a model does not name "an
agent does the work" unprompted.

`20261025-figure-out-records-what-the-lean-body-rebuild-retired` found that an outside-view line
added to the spine made a small choice heavier (case `64`, failing 2 of 2). A new spine line can
over-fire the same way.

## Decision
- **A spine line in figure-out's *What holds throughout*:** price options by the effort that
  binds. Work the agent controls costs close to nothing and is never a reason to drop or shrink an
  option. What costs is what the agent does not control, as listed above. Estimates are given in
  those terms (agent sessions, the person's time, outside waits), never in team-weeks.
- **A *bigger version* probe in `tasks/FEATURE.md` and `tasks/PRODUCT.md`:** with controlled
  work near free, which version would be worth much more to the person it serves, and what
  separates it from the version asked for: only controlled work, or a cost the agent does not
  control? Show it beside the asked-for version. It is bigger in outcome, not in parts, and is
  recommended only where the evidence favors it. The person chooses the size. The probe does not
  load for bugs or diagnosis.
- **The *Reference class* probe** adds that, where an agent does the controlled work, base rates
  from efforts people did overstate time and effort, so only the parts the agent does not control
  carry over.
- define is not changed: its Appetite already bounds complexity and surface, not time.

## Alternatives Considered
- **A general instruction to be brave or ambitious.** Rejected: it changes tone more than
  estimates, and it collides with the North Star principle *Claim only what holds*.
- **Lean big: recommend the bigger version whenever it is in reach.** Rejected for "judged
  fairly": ambition belongs in outcome and in the option set, strictness in verification, and
  economy in parts.
- **Fix the estimates only, with no bigger-version probe.** Rejected: a corrected cost model stops
  options being cut, but it does not make a session look beyond the size of the request.
- **Both lines in the spine.** Rejected: a bug fix or a diagnosis would grow a bigger-version
  option it has no use for.

## Consequences

### Positive
- Options are no longer dropped or phased for effort that an agent does at almost no cost.
- Estimates name what really waits on the person and on the world.
- Feature and product sessions see the version worth much more when only controlled work stands
  in the way.

### Negative
- A session can underprice controlled work that is in fact hard for an agent, for example a long
  build that needs many sessions to converge.
- One more spine line, with the over-firing risk that case `64` showed for the outside-view line.

## Enforced by
not yet — eval cases for a timid estimate and for the bigger version, driven through
`verification/recipes/figure-out.md`; the new probe's row in the eval README's *Coverage* table,
which `tests/test_figure_out_coverage.py` checks; and case `64-decision-small-and-undoable` driven
again as the over-firing guard

## Revisit when
A read prices controlled work as near zero and the work then overruns on controlled work alone,
read in that run's report or Execution Log.

## Source
- Session: a figure-out session on timid planning, 2026-10-26.
- Related: 20261025-figure-out-records-what-the-lean-body-rebuild-retired, 20261026-decision-records-give-grounds-not-a-veto
