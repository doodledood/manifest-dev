---
name: escalate
description: 'Structured escalation when /do hits an unrecoverable blocker. Surfaces what was tried, why it failed, and what the user can decide. Called by /do when work is blocked, cannot proceed, hits an unrecoverable failure, needs a user decision, or gets stuck.'
user-invocable: false
---

Receive the manifest path, selected verification mode, explicit or inherited verifier-model provenance, and affected gate ledger entries including evaluator provenance from `/do`. Surface that policy/provenance with the blocker evidence: the criterion (INV-G or AC ID) that can't be met, what was tried and why each attempt failed, the resolutions you see (fix path, amend the criterion, drop it, descope), and what you need from the user to unblock. Show the attempts — that is what separates this payload from "I can't" or "this is hard".

Also name any Process Guidance departed from, any deviation from the Initial Approach or the Deliverable order, any findings a gate reported below its threshold, and any gate whose bar the run read as suspect without a user to ask, with why — nothing gates on these, so this payload is where they surface when the run exits here.

A gate whose criterion misdescribes what it judges routes here too — reported by its verifier, or surfaced by execution — passing or failing, wherever `/do`'s advance delegation does not reach the repair: the deliberately-chosen set, unclear provenance, or anything that is not a raise-only altitude repair. A gate whose criterion is right but whose bar costs more than it returns arrives the same way, carrying what recent rounds found and what another round would re-verify. Quote the report or name what execution showed, in place of attempts a passing gate does not have, and name the decision being asked for: whether the gate's text changes. That is the user's call, never the run's, which is why it arrives here rather than as an amendment.

A BLOCKED verifier verdict routes here too when a person can act on it — "awaiting human approval" names someone who can act, while "the scheduled build has not run yet" names only elapsed time — with the BLOCKED note quoted from the verifier and the suggested user action carried through. Under a caller's no-wait overlay a BLOCKED that leaves only waiting reports as pending rather than arriving here; without that overlay it waits and re-verifies instead. Pure questions about the manifest or process are answered inline by /do, not escalated.

**If the user responds with a scope change rather than addressing the blocker** ("change AC-X", "drop that criterion", "add a check for Y", "actually we also need Z"), invoke `/define <manifest-path>` to amend the manifest, then resume /do. Otherwise (user clears the blocker or supplies missing context), resume /do directly.
