# ADR: An orchestrating skill runs the queue in parallel and replaces the sweep and event triggers

## Status
Accepted — amended by 20261019-each-item-waiting-on-the-person-carries-its-recommendation-risk-and-evidence: each waiting item carries the recommended answer, its risk and its evidence; and by 20261019-one-cause-failing-several-runs-pauses-the-effort-once: one cause failing several runs pauses the effort once; amended by 20261023-projects-advance-toward-assigned-outcomes-within-delegated-authority: outcome-led progress and independent adoption choices

## Area
Strategy

## Decided by
The user

## Context
Unattended Ticket work started in two ways. A scheduled `sweep-tickets` run recovered or started
one Ticket and stopped. An event-triggered automation, which the user built from guidance in
`ticket-up`'s automated-execution reference, launched `run-ticket` when an issue changed. The sweep
advances at most one Ticket per invocation, which is too slow once many agents can run at once.
The event path is fast, but it leaves the user to build the adapter, its per-Ticket single-flight,
its retries and its failure handoff on their own host. Neither path gives a person control over
what runs: there is no plan to approve, no view of what is in flight, and no single place that
knows which runs are live. In the owner's own use, running many Tickets by hand meant asking each
session for its status, again and again.

20261015-projects-drive-themselves-as-far-as-each-user-climbs ruled that manifest-dev ships no
orchestrator, because one ties the project to one host and adds user-facing complexity, and
because `/sweep-tickets` was already the one step a scheduler calls. The owner reversed that
position: the sweep gives too little control and is too slow.

## Decision
- A new skill, `orchestrate`, takes an effort or, when none is named, the whole store. It runs
  ready Tickets in parallel, each through `run-ticket` in its own session, up to `--max-batch` at
  once (default 10; `none` removes the limit). It ranks candidates by the store's delay-loss rule.
  An optional type filter limits it to Tickets of the named Ticket Types, as the sweep's did, and
  an untyped Ticket never matches one.
- It has two modes, and each mode decides whether it chains, so no flag does. By default it
  proposes an execution plan and waits for the person's approval; when the plan ends, it proposes
  the next one, and no answer means stop. With `--autonomous` it acts on its own, keeps filling
  free slots while work remains in scope, then stops. Autonomous runs take Auto Tickets end to
  end, and Tickets without Auto up to a ready pull request, under
  20261018-a-ticket-without-auto-runs-until-it-needs-a-person-and-never-lands-on-its-own.
- An approved plan may include ungranted Tickets. They stop at a ready pull request with its
  evidence and land only after the person looks. Approving a plan is not an Auto grant.
- Orchestrators never coordinate with each other. Each knows only itself; the store and git are
  all they share. The first live run on a Ticket wins: its attempt record names the run and its
  session, and a run is live from its launch until it writes an outcome, while the host reports
  its session alive and its per-run timeout has not passed. Before each launch, merge, close or mark change, the orchestrator re-reads that one
  Ticket and stops when the run facts on it are not its own. Git rejects a stale run's push, and
  that run then stops.
- Collisions are handled at three points. At plan time, Tickets likely to touch the same code run
  one after another, including a cross-cutting pair, where one change alters how every instance of
  something must look and the other adds a new instance. When the base moves, in-flight runs merge
  it in early, which keeps conflicts small, and re-run their gates only at their landing turn. At
  landing, a run whose base moved reads what landed and checks the cross-cut both ways; it extends
  its work when the extension fits its Ticket, and otherwise writes a follow-up for a person.
- Planning splits by size. A quick ticket-up happens in the orchestrator's conversation. Deep
  planning runs in its own session: figure-out with the person, whose read `ticket-up` turns into
  Tickets in the effort. The orchestrator hands the person a ready start line naming the topic and
  the effort, and starts that session itself where the host lets it start one the person can
  open. In `--autonomous`, the start line waits on the person's list. The orchestrator learns of
  the new Tickets from the store at its next check-in, so the planning session sends it nothing.
- A person follows the run on a status page: a view rebuilt from the store at each check-in, never
  a record of its own, linked from the effort's front item so later plans update the same page.
  It is one fixed template shipped with `orchestrate` that reads a single data block, and each
  check-in rewrites only that block. It shows the Tickets as a graph of the order between them,
  with what waits on the person listed apart. The orchestrator publishes it on the page surface
  the host offers, such as an Artifact or a hosted page, and writes it as a local file where the
  host offers none. Where the host gives the page a live data store, the orchestrator writes each
  check-in's data there, and every open view updates in place, animating what changed; elsewhere
  the page shows the data as of its last rewrite.
  The orchestrator keeps one list of what waits on the person — held pull requests, escalations,
  follow-ups awaiting a person's grant, the next plan — ordered by what waiting costs.
- The person's answers count by where they come from. The orchestrator writes an answer given in
  its conversation back to the Ticket, and on the person's explicit answer it may record the
  continuation and clear an escalation mark. On the venue, only a pull-request approval by someone
  with write access counts. An Auto grant still goes through `ticket-up`; in `--autonomous`, `orchestrate` itself grants it
  where the criterion holds, under 20261018-orchestrate-tickets-up-debt-and-grants-auto-where-the-criterion-holds.
- A line on the effort's front item pauses the effort: an orchestrator starting on it starts
  nothing new, and running sessions finish.
- A failed launch is retried. After three failed launches, the Ticket goes to a person with the
  run references. Each run has a timeout.
- A file store gets no parallel runs: separate checkouts share no live surface on which claims
  can separate runs.
- On a host that cannot start other sessions, a batch of one runs the Ticket inside the
  orchestrator's own session.
- `sweep-tickets` and the event-trigger guidance are removed. A scheduler the user already runs
  may start `orchestrate --autonomous`.
- `orchestrate` is an optional extra under
  20261013-new-capabilities-live-inside-the-four-workflow-entry-points: figure-out, define, do and
  auto never depend on it, and every skill it drives still works on its own.
- The North Star's *How they arrive* now reads: "manifest-dev ships an orchestrating skill, not a
  scheduler: the user starts it by hand or from a scheduler they already run, and every skill it
  drives still works on its own."

## Alternatives Considered
- **Keep the sweep and the event path**: one Ticket per sweep is too slow, and the event path
  leaves the user to build adapter machinery with no plan, no view and no control.
- **Batch the sweep**: rejected in 20260812-scheduled-ticket-sweep-is-recovery-first-and-one-ticket
  because "the sweep becomes an orchestrator". That is now the decision, made openly, with the
  plan, view and control a batch needs, rather than inside a scheduled step.
- **Keep run state in the status page**: cheaper to read, but the page and the Tickets can then
  disagree, and a crashed or second orchestrator acts on the wrong one. An independent
  re-derivation of the design found this; per-run facts live on the Ticket, under
  20261018-the-tickets-attempt-record-carries-its-manifest-progress-and-run-facts.
- **A lock per scope that every orchestrator checks**: the owner wants each orchestrator aware
  only of itself, and the first live run per Ticket separates them without a shared lock.
- **Re-run gates in every in-flight run each time anything lands**: catches breakage sooner, but
  the cost grows with the square of the batch.
- **Ship a scheduler or hosting**: ties the project to one host, which is the part of the
  2026-10-15 grounds that still holds.

## Consequences

### Positive
- Many Tickets run at once under one plan the person approved, with one page that shows where
  each stands.
- Users no longer build trigger adapters: single-flight, retries and the failure handoff live in
  one skill.
- Several orchestrators can run on different efforts without knowing about each other.

### Negative
- One more skill a person invokes, and a larger one than the sweep.
- Without required up-to-date branches or a merge queue, two orchestrators landing on one branch
  leave a race of seconds between a run's last check and its merge. The plan names it once.
- With no event path, new Tickets wait for the next orchestrator pass.
- A cross-cutting pair that the Ticket text does not reveal lands incomplete until the landing
  check sees it.
- How well an agent judges overlap at plan time has not been tested.

## Enforced by
`tests/test_ticket_automation_prompts.py` — `test_orchestrate_proposes_and_waits_by_default`, `test_orchestrate_selects_recovers_first_and_leaves_paused_work_alone`,
`test_orchestrate_rereads_one_ticket_before_each_launch_merge_close_or_mark_change`,
`test_orchestrate_orders_cross_cutting_pairs_and_checks_them_at_landing`,
`test_orchestrate_counts_answers_by_where_they_come_from`, `test_orchestrate_names_its_failure_and_host_paths`,
`test_orchestrate_stays_an_optional_extra` and `test_the_sweep_and_the_event_trigger_guidance_are_gone`
fail if `orchestrate` loses propose-and-wait as its default, the autonomous fill-and-stop, recovery
first, the re-read of one Ticket before each launch, merge, close or mark change, the ordering of
cross-cutting pairs, the rules for where the person's answers count, its failure and host paths,
or its place as an optional extra, or if the sweep or the event-trigger guidance returns. Also
`tests/test_entry_points.py` — `test_user_invocable_skills_are_the_declared_set` declares
`orchestrate` in place of `sweep-tickets`, and `tests/test_dist_skill_references.py` —
`test_codex_does_not_ship_reviewer_agents_or_removed_skills` fails if `sweep-tickets` ships again.

## Source
- Session: figure-out on running unattended Ticket work with many agents at once (2026-10-18).
- Supersedes 20260812-scheduled-ticket-sweep-is-recovery-first-and-one-ticket,
  20260812-trigger-adapters-enforce-per-ticket-single-flight,
  20260812-trigger-adapters-hand-off-exhausted-runner-failures
- Related: amends 20261015-projects-drive-themselves-as-far-as-each-user-climbs,
  20260825-escalation-clears-the-claim-and-carries-its-own-mark,
  20260812-human-assignment-pauses-auto-ticket-execution; see also
  20261018-orchestrate-lands-and-run-ticket-stops-at-a-ready-pull-request,
  20261018-a-ticket-without-auto-runs-until-it-needs-a-person-and-never-lands-on-its-own,
  20260814-ticket-selection-minimizes-delay-loss-across-available-executors,
  20261013-new-capabilities-live-inside-the-four-workflow-entry-points,
  20260703-figure-out-fog-discipline,
  20260811-ticket-type-is-a-rollout-selector-not-a-classification,
  20261018-orchestrate-tickets-up-debt-and-grants-auto-where-the-criterion-holds
