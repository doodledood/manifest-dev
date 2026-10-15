# ADR: The verification harness is optional — a project may verify its own way

## Status
Accepted

## Area
define / do

## Decided by
The user

## Context
20261013-runs-build-and-maintain-a-project-verification-surface had runs build a missing
verification surface, unattended too, and 20261014-one-verification-harness-per-project made that
surface one harness setup seeds without asking. So every skill treated the harness as owed: define
cut building it as the first Deliverable wherever the context file named none, do built it from
the project's assets or from nothing, and setup installed it. A project that already verifies its
own way on purpose — its own test runner, scripts and release checklist — got a second system it
never chose, and the North Star's Never says nothing a user adds may require anyone else to adopt
manifest-dev.

Separately, the same steering asked whether a scenario a CI service already runs needs evidence of
its own. The owner ruled that the workflow must not depend on CI, and should carry fewer concepts
rather than more.

## Decision
- The harness is the project's choice, never a run's. The verification bullet of the context
  file's project-surfaces section is the one place the choice lives, in one of two forms: the
  harness form names its command; the own-way form names the project's commands and steps and says
  the project verifies its own way by choice.
- Where the bullet names the harness, nothing changes: runs build the parts a change needs, keep
  recipes current and repair what is unfit, as before.
- Where it names the project's own way, runs verify through that way and add any check a change
  needs in that same form. No run builds, gates on or offers a harness.
- Where there is no bullet, a harness already on disk counts as chosen: runs treat it as the
  harness form and suggest recording its bullet. Otherwise the project never chose: runs verify
  through the checks the project already has, add only the check the change needs in the project's
  own form, build no harness, and recommend the harness in their report.
- The line is build versus maintain, not harness versus none. No run builds a verification system
  the project did not choose, and every run keeps sound the checks the project has, in whatever
  form — a test, a script, a checklist step, a recipe — where its work touches them. The *Fit to
  trust* jobs judge any check, and a touched check that fails one is repaired within scope in its
  own form or reported as debt. An opt-out means only that no workflow run builds or offers a
  harness.
- Verification still comes before the work: when nothing the project has can check what a change
  touches, the first step adds such a check, in the project's own form.
- The harness is recommended, so setup-project installs it by default; the user opts out to keep
  the project's own way, which writes the own-way bullet, so no figure-out, define or do run offers
  it again. A setup-project run is an audit against the recommended setup, so it still offers the
  upgrade to the harness, even to a project with its own way or a harness of its own making: the
  upgrade adopts the project's checks by delegation, and a decline leaves them as they are. Every
  skill still does its whole job without a harness. The upgrade guides offer the same choice to installed projects.
- Evidence stays uniform for every scenario a harness runs. A scenario a CI service also runs gets
  no exception, so the workflow does not depend on CI and carries no second evidence rule.

## Alternatives Considered
- **Keep building a harness scoped to the change wherever none is named**: rejected. It adds a
  surface to projects that verify their own way on purpose, and nothing records that they declined,
  so every run would build or offer it again.
- **A separate setting or file recording the choice**: rejected. The verification bullet already
  names how the project verifies; a second record could disagree with it.
- **Repair only checks inside a chosen harness**: rejected. A project's own test suite is as much
  its verification as a harness is; leaving it broken because it has another form would let the
  checks the work relies on rot.
- **Make evidence optional for deterministic scenarios a CI service covers**: rejected. It ties the
  workflow to CI, and adds a rule about which scenarios need evidence.

## Consequences

### Positive
- A project that verifies its own way uses every skill without gaining a system it did not choose.
- The choice is made once and read from one line every session already loads.

### Negative
- A project that never ran setup gets an offer rather than a harness, so it gains one only when a
  person accepts it.
- Without a harness there are no recipes or evidence statuses; the project's own checks carry what
  the harness would have recorded.

## Enforced by
partly — `tests/test_harness_optional.py` fails when define's, do's, figure-out's or
setup-project's shipped text loses the condition that harness work applies only where the project
chose it, stops naming the project's own way as the other path, or drops the duty to repair a
touched check in the project's own form; whether each sentence behaves
right on each kind of project stays judgment.

## Source
- Session: the owner's steering during the surfaces v5 change, 2026-10-15
- Related: Amends 20261013-runs-build-and-maintain-a-project-verification-surface and
  20261014-one-verification-harness-per-project; see also
  20261015-the-shipped-harness-is-a-default-shape-a-project-adapts
