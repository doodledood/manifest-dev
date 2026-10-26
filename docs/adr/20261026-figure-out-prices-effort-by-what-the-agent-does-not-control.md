# ADR: figure-out prices effort by what the agent does not control, and defaults to the solution that would be right if effort were free

## Status
Accepted

## Area
figure-out

## Decided by
The user

## Context
Planning sessions tame their solutions. They price work as if people do it: "this needs two or
three engineers for a quarter", "phase it", "patch it here; the proper fix is a multi-sprint
migration". So they recommend the compromise, not the solution they would choose if effort were
not a problem. When an agent does the work, research, planning, design, building and testing cost
close to nothing. What still costs is what the agent does not control: a person's decisions and
attention; coordination between people; waits on reviews, approvals, partners and users; access,
accounts and money; acts that cannot be undone; and proof that the result works where it will be
used, beyond the tests the agent can run.

figure-out never says who does the work or how to price effort. Its *Reference class* probe in
`tasks/DECISION.md` asks how efforts like this usually turned out. That invites base rates from
efforts that people did. The probe asks where the case differs, but a model does not name "an
agent does the work" unprompted.

Drives on the skill before this decision bear this out. Where the request said that coding agents
build, or the project's context file did, figure-out priced the build as agent work and put the
time on reviews and waits. Where nobody said who builds, it priced the same work in developer
time: "5–12 weeks of developer work" for an i18n job, and "about 1–3 days with tests, not 3–4
weeks" for a fix an agent writes in one session. define read a two-sprint estimate as the request
rejecting the full fix.

`20261025-figure-out-records-what-the-lean-body-rebuild-retired` found that an outside-view line
added to the spine made a small choice heavier (case `64`, failing 2 of 2). A new spine line can
over-fire the same way.

## Decision
- **A spine line in figure-out's *What holds throughout*:** price options by the effort that
  binds. Research, design, building and testing are an agent's to do unless the person says
  people will do them, and that work costs close to nothing. What costs is what the agent does not
  control, as listed above. So the default is the solution that would be right if effort were
  free, for the same problem and not a bigger one. A session moves off that solution only for a
  cost the agent does not control, and names that cost. Estimates are given in those terms
  (agent sessions, the person's time, outside waits), never in team-weeks.
- **The *Reference class* probe** adds that, where an agent does the controlled work, base rates
  from efforts people did overstate time and effort, so only the parts the agent does not control
  carry over.
- **define's Appetite line** adds that Appetite never counts effort the agent controls. Appetite
  still bounds complexity and surface.

The rule makes the solution braver. It does not grow the scope: more features, modes or parts
still earn their place as before.

## Alternatives Considered
- **A general instruction to be brave or ambitious.** Rejected: it changes tone more than
  decisions, and it collides with the North Star principle *Claim only what holds*.
- **A *bigger version* probe for feature and product work** that shows a version of the outcome
  worth much more beside the one asked for. This was in the first draft. Rejected by the user:
  bigger means braver in the solution to the same problem, not more scope.
- **Fix the estimates only.** Rejected: a corrected estimate still leaves the compromise as the
  default recommendation.
- **Leave define unchanged**, because its Appetite already bounds complexity and surface rather
  than time. Rejected: a standalone `/define` would still be free to cut the ideal solution for
  effort.

## Consequences

### Positive
- Sessions recommend the solution they would choose with effort out of the picture, and name the
  real cost when they choose otherwise.
- Estimates name what really waits on the person and on the world.

### Negative
- A session can underprice controlled work that is in fact hard for an agent, for example a long
  build that needs many sessions to converge.
- One more spine line, with the over-firing risk that case `64` showed for the outside-view line.

## Enforced by
partly — eval cases driven through the recipes. Three fail on the skill before this decision:
`claude-plugins/manifest-dev/evals/92-estimate-what-waits-on-people` (an estimate prices the build
as agent work and puts the time on what waits on people),
`93-thorough-fix-not-tamed-for-effort` (the read keeps the full fix and sizes it without developer
time, adding no scope) and `define/d28-appetite-ignores-agent-effort` (Appetite keeps the whole fix
and bounds nothing by engineer time). Two guard against over-firing:
`64-decision-small-and-undoable` on a small choice, and `65-decision-plan-before-committing` on work
people do. Whether a named cost is outside the agent's control stays judgment

## Revisit when
A read prices controlled work as near zero and the work then overruns on controlled work alone,
read in that run's report or Execution Log.

## Source
- Session: a figure-out session on timid planning, 2026-10-26.
- Related: 20261025-figure-out-records-what-the-lean-body-rebuild-retired, 20261026-decision-records-give-grounds-not-a-veto
