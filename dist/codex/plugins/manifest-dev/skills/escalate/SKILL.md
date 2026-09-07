---
name: escalate
description: 'Terminal escalation for do or just-do when unresolved blockers require outside intervention and no useful independent work remains. Reports the evidence, recovery attempts, completed work, and intervention needed.'
user-invocable: false
---

This is a terminal handoff, called only after useful independent work is exhausted.
An earlier blocker notice belongs in the executor's progress report; it does not
end the run. If useful independent work remains, return to the calling executor
to continue it before escalating.

Receive the manifest path, selected verification mode, explicit or inherited verifier-model provenance, and affected gate ledger entries including evaluator provenance from `/do`. From `just-do`, receive the Manifest path and its actual gate evidence and evaluator provenance; relay any supplied policy without inventing a mode or independent verification it did not use. Surface that policy/provenance with the blocker evidence: the criterion (INV-G or AC ID) that can't be met, the credible recovery paths investigated and why they failed, and the intervention needed — unavailable knowledge or access, new authority, or a change to a binding requirement. Name what independent work completed and why the remainder depends on that intervention. Recommend a resolution; report it without starting a question-and-wait loop.

Also name material autonomous decisions and their rationale, including Appetite revisions and the benefit that justified their added complexity or maintenance; any Process Guidance departed from; any deviation from the Initial Approach or the Deliverable order; findings a gate reported below its threshold; and any costly-threshold concern the run recorded while continuing repairs. Include these even when the execution log already holds them.

A false binding premise outside the caller's amendment authority can arrive here
even when its gate passed. Quote the report or name what execution showed in place
of attempts a passing gate does not have. A costly bar alone is not a blocker
while repairs remain viable; it is reported as a concern, never lowered by this
skill.

A BLOCKED verifier verdict is not sufficient on its own: the executor first
investigates what it can recover and completes useful independent work. Quote the
remaining BLOCKED note and name the required outside action. A pure external wait
reports as pending under a no-wait policy; otherwise the executor waits and
re-verifies. A stalled wait with no viable recovery path names the intervention
needed here. Pure user questions about the manifest or process are answered inline
by the executor.

**If the user later supplies a scope or requirement change**, invoke the calling
executor's authoring skill with the Manifest path (`define` for `/do`,
`just-define` for `just-do`), then resume that executor. If they clear the blocker
or supply the missing context, resume it directly. Their response is steering;
resumed execution remains unattended.
