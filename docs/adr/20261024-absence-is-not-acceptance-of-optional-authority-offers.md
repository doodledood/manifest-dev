# ADR: Absence is not acceptance of optional authority-surface offers

## Status
Accepted

## Area
Ticketing

## Decided by
An agent in an unattended run, with no review — assignment to investigate the reported gap and build what holds up

## Context
v10 added optional authority-surface offers: scoped instructions and coordination preparation. Earlier upgrades already said a run with no person present flags owner-judgment items and writes nothing. The v10 offers and setup's update pass did not carry that sentence. Autonomous figure-out self-accepts an authorized `setup-project` handoff, and that exception was readable as permission to answer the inner "when wanted" items. A project that recorded v10 then looked current, so figure-out would not offer the update again.

A downstream report described an unattended coordination upgrade answering those offers on the owner's behalf. The owner's later distrust of high-level UI and product calls is the class `20261012-unattended-runs-flag-the-users-calls-by-disagreement-not-confidence` already chose to flag and continue during work, not a reason to invent a new sign-off policy file.

This decision sits inside the North Star's *Purpose*: people keep the choices they retain.

## Decision
"Wanted" and "accepts" on optional authority-surface offers mean a present person or a choice the project already records. Absence is not acceptance. Inference from existing instructions does not make those items wanted when no person is present.

An authorized setup or ticket-up assignment covers running that workflow and its mechanical items. It does not answer inner owner-judgment offers — optional adoption, scoped instructions, coordination preparation, a retained-decision ask, and any similar item that is only wanted when a person says so. Those are flagged in the report and not written. The surfaces version waits for a person's answer or an already-recorded choice.

When a person accepts coordination, or asks for scoped adjustments, ask which decisions they retain. Capture each as a principle with an example they give, in the existing scoped-instructions slot. The owner names the set. Do not add a policy file, a default principle list, or a new project surface.

Unattended work calls stay under `20261012-unattended-runs-flag-the-users-calls-by-disagreement-not-confidence`: flag them and continue. This record does not stop a run at each user's call, write placeholders into project surfaces, or audit past offers for who answered them.

## Alternatives Considered
- **A sign-off-principles interview with a shipped default set:** would become the permission file `20261023-assignment-bounds-delegated-decisions-and-retained-acceptance` rejected, or harden one project's examples as every project's rule.
- **Stop the unattended run and ask, or write a flagged placeholder into the context file:** `20261012-unattended-runs-flag-the-users-calls-by-disagreement-not-confidence` rejected stopping the run; a pending line in a resident surface reads as accepted policy. The existing flagged-candidate branch already names the unanswered item.
- **A standing upgrade audit of offers earlier unattended runs answered:** setup records no who-answered, so the audit cannot tell owner-accepted from agent-accepted and would nag legitimate accepts. A later attended setup can still offer the retained-decision ask when coordination is in use and none are named.
- **Leave v10 as written:** the missing absent-owner sentence is what lets an authorized upgrade seal optional authority surfaces.

## Consequences

### Positive
- Optional authority surfaces stay owner-answered, including on an authorized unattended upgrade.
- Attended coordination adoption fills the slot the project already has, without a new document.

### Negative
- A v10 project that already recorded agent-accepted coordination stays as it is until someone runs setup attended or names retained decisions themselves.
- Instruction consistency still cannot guarantee every model follows the boundary.

## Enforced by
partly — `tests/test_owner_judgment_offers.py` pins the absent-owner and inner-offer sentences in `setup-project/SKILL.md` and `figure-out/references/autonomous.md`; whether a run obeys them stays judgment.

## Revisit when
Attended setup runs that accept coordination still leave scoped instructions empty of retained decisions, read on those projects' context files after a setup report that claimed the ask ran.

## Source
- Session: figure-out `--autonomous` then `/auto` on the reported setup/upgrade gap
- Amends 20261023-assignment-bounds-delegated-decisions-and-retained-acceptance
- Related: 20261012-unattended-runs-flag-the-users-calls-by-disagreement-not-confidence
- Related: 20260907-executors-own-unattended-decisions-within-explicit-bounds
