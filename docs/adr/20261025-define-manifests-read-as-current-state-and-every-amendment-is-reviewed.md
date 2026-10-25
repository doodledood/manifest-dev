# ADR: define writes every Manifest as current state, and reviews every amendment in a fresh context

## Status
Accepted

## Area
define

## Decided by
The user

## Context
Manifests for big tasks became hard to use as feedback arrived. Each amendment added without removing. New gates and assumption entries piled up beside the ones they replaced. One gate gained a clause for every reported instance. History text appeared ("previously…", "updated to…"), and Intent or the Approach kept describing the older task. The user named the worst offender: "user ruled X on date Y" notes spread through gates and Intent, so a newcomer had to piece the current picture together.

`/define`'s rules already forbade an amendments log, sibling gates and a stale frame, and the failures still happened. Two causes are visible in the prompt. First, the amendment rules only added. "An amendment that changes a decision produces a gate", each unattended decision added an assumption entry, and "preserving unaffected items verbatim" protected what was there. No rule said to delete what an amendment replaces, or what the whole file should look like afterwards. Second, nobody reread the whole result. `20261018-define-reviews-each-new-manifest-in-a-fresh-context` gave new Manifests a fresh-context review and deferred amendments "if they do" show the failure. They now have. The rule's own reason, "No amendments log — git is history", was also false: Manifests live in the user's home directory, outside any repository, while `/do`'s Execution Log already records what each amendment changed.

The provenance notes do one job worth keeping. They tell the user what was decided for them, and they tell `/do` which choices are the user's (not to be overturned) and which are its own (revisable). That is a fact about the current state. Dates and the story of how a choice was reached are history.

## Decision
Every Manifest `/define` writes or amends reads as current state. A reader who was not in the session reads it top to bottom and has the current task, with nothing to piece together. Gates, Intent, Initial Approach and Process Guidance state only what holds now: no date that records when something was decided or changed, no note of who decided what, and nothing about what an item used to say. A why may name the requirement a value comes from, never who decided it or when. Who decided what is stated once, in Known Assumptions, without those dates. The `(auto)` mark after an item's ID is the one pointer to it. What changed, when and why belongs in the figure-out log and `/do`'s Execution Log.

An amendment deletes what it replaces, and replaces a Known Assumption it supersedes rather than adding a second one. A deleted ID is retired, never reused. A gate the amendment touches is rewritten so its body states the whole class, not given one more clause for the reported instance. Removing a dated or "ruled" note changes no requirement, so an amendment removes such notes wherever they sit, untouched gates included. The author searches for references to each deleted ID and resolves them. A gate stating a value the user did not give states it plainly; its `(auto)` Known Assumption records the value and reason, and the gate no longer has to cite it.

Every amendment gets the one fresh-context review that new Manifests get. The reviewer receives the Manifest before the amendment, or a diff, never a description of the change. Its scope is shorter: a newcomer read of the whole file, the per-gate wrong-result question on the touched gates only, and a check that nothing the amendment replaced survives. A fix lands in a touched gate or in text that binds nothing. A fix that would change an untouched gate's requirement, or what the user agreed, is asked when attended; unattended, it is not applied and is named in the digest. It never becomes a new Known Assumption, since that section holds each decision or open hole once, not a record of how a finding was handled. One pass, no second review, no wait on an unattended amendment.

## Alternatives Considered
- **Provenance nowhere in the Manifest**: all of it in the logs — Not chosen by the user: `/do` would lose which choices are the user's and which it may revise.
- **Provenance inline, undated**: short notes beside each item — Not chosen by the user: the scatter that makes a newcomer piece the picture together stays.
- **Review only attended amendments**: — Not chosen by the user: unattended `/do` steering is where many amendments come from, and nobody reads those before execution resumes.
- **Review every Nth amendment, or only large ones**: — Not chosen by the user: bloat builds from small amendments, and letting the author decide which amendments are large enough is self-grading.
- **A shipped script that flags history words, dangling IDs and growth**: — Not chosen: overlap, clause growth and a stale frame are matters of meaning that a script cannot see. The one mechanical risk the deletion rule adds, a reference to a deleted ID, is covered by the author's own search. A script is the fix if such references keep appearing.
- **Stronger inline bans**: — Not chosen: three of the four failures already had a rule against them; the failure is a local reading, which more text in the same context does not reach.

## Consequences

### Positive
- A newcomer, `/do` and `manifest-to-goal` read one current picture, with who decided what in one place.
- Old notes leave on the next amendment, attended or not.

### Negative
- Each amendment costs one more fresh context.
- `/do` re-verifies a gate whose text changed only because a note was removed.
- The history of a Manifest is readable only where the logs are kept.

## Enforced by
partly — the define eval case `d09-amend-widen`'s `current-state` grader fails an amended Manifest that keeps a dated or "ruled" note or text about the replaced rule; whether the amendment review runs and settles its findings is judgment, checked by the `define` recipe's `current-state-amend` and `amend` scenarios.

## Source
- Session: figure-out read and define run on 2026-10-25, from the user's reports of bloated Manifests
- Related: amends 20261018-define-reviews-each-new-manifest-in-a-fresh-context (amendments are now reviewed); see also 20261019-define-searches-each-new-manifest-for-a-wrong-result-that-passes-every-gate
