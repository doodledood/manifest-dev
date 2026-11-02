# ADR: setup-project audits the whole setup when run, and figure-out fixes what is on its path

## Status
Accepted — amended by 20261018-the-harness-commits-no-evidence-and-time-lines-live-in-recipes: statuses are no longer a part setup offers an existing harness. Also amended by 20261102-setup-offers-taste-entries-mined-from-stated-reasons: the one-time Taste offer is not made again to a project recording surfaces v13 or later, whatever the answer; the recorded version marks it as made.

## Area
Project context

## Decided by
The user

## Context
After 20261013-set-up-projects-receive-updates-through-a-version-marker, a project that recorded the newest surfaces version was reported current and offered nothing, by setup-project as well as by figure-out. The version line records what was offered, not whether the setup is sound: a surface installed badly, a verification surface that was never driven, or a decision record whose check was never found all pass for current. Someone who runs setup-project is asking whether their setup is sound, and a version check answers a narrower question. The same record rejected a checklist of features because it would offer declined items again and grow with every release.

## Decision
- A setup-project run audits the project against the setup its own references describe, whatever version the project records, and offers each gap on its own. What changed since the recorded version is marked as new. The references are the checklist, so no separate list grows with each release.
- The best setup is the one the project needs now. Each offer names the need it serves today; a piece the project has no current use for is not a gap, so an audit never adds parts a project carries without using them.
- Nothing records a decline. An item declined on an earlier run is offered again on the next run someone starts; the run is rare and deliberate, so a repeated offer costs little, and a decline list would be one more piece of state to drift.
- Differences in a project-owned copy keep the attribution the version line gives: content the shipped text gained since that version is offered, anything else is the project's own choice and stays.
- For a verification surface, setup seeds a missing one and offers an existing one only its missing parts — statuses, README, repository check, the feature-map shape. It offers no harness, drive or proof improvement: a surface grows with the work that needs it, raised by figure-out when work touches a surface it cannot trust and built by that work's Manifest. Offering harness work at setup would grow every adopter's scope ahead of any need.
- figure-out does not audit the whole setup. Its offer of setup-project stays gated by the version line, plus one offer per session when docs mode meets a plainly broken surface — a surfaces section naming a missing path, an index listing a missing record. A surface on the path of the work that is missing, drifting or not fit to trust is repaired as part of that work, by define and do.

## Alternatives Considered
- **Everything the references describe, needed or not**: adds surfaces and parts a project carries without using, which is the cost a setup exists to avoid.
- **Defects only on an explicit run**: answers whether something is broken, not whether the setup is sound, which is what someone running setup asks.
- **A decline record beside the version line**: avoids repeated offers but adds state that drifts; worth revisiting if setup-project runs often or for a team.
- **Fix surface gaps inside setup**: makes setup long, open-ended and hard to verify; harness work needs its own gates and proof run.
- **Offer harness and proof gaps at setup and hand them off as Tickets or `/define`s**: turns every setup into a backlog of verification work no change has asked for yet.
- **figure-out audits on every session**: takes over investigations that are about something else.

## Consequences

### Positive
- A project gets what the current setup offers by running setup-project, whatever version it records.
- figure-out sessions stay on their topic while still catching broken surfaces they meet.

### Negative
- An explicit run repeats offers the project declined before.
- An explicit run costs more than a version check: it reads the references and the project's surfaces in full.

## Enforced by
partly — `tests/test_setup_project_versions.py` (`test_eval_cases_track_the_newest_version`) keeps an eval case for a project one version behind; eval cases `30`, `45` and `47` measure figure-out's gated offer once run. Whether an explicit run audits and offers each gap stays judgment.

## Source
- Session: investigation of setup-project's update behavior.
- Narrows: 20261013-set-up-projects-receive-updates-through-a-version-marker
- Related: 20261014-the-feature-map-is-a-navigation-contract-over-what-users-invoke
- Related: 20261014-only-records-in-effect-carry-enforcement
