---
name: escalate
description: 'Terminal escalation for do when unresolved blockers require outside intervention and no useful independent work remains. Reports the evidence, recovery attempts, completed work, and intervention needed.'
user-invocable: false
---

This is a terminal handoff, called only after useful independent work is exhausted.
An earlier blocker notice belongs in the executor's progress report; it does not
end the run. If useful independent work remains, return to the calling executor
to continue it before escalating.

Receive the Manifest path from `/do`, along with the affected gates and the actual evidence behind each. Relay that evidence as supplied, without inventing verification the run did not perform. Surface it with the blocker evidence: the criterion (INV-G or AC ID) that can't be met, the credible recovery paths investigated and why they failed, and the intervention needed — unavailable knowledge or access, new authority, or a change to a binding requirement. Name what independent work completed and why the remainder depends on that intervention. Recommend a resolution; report it without starting a question-and-wait loop.

Also name material autonomous decisions and their rationale, including Appetite revisions and the benefit that justified their added complexity or maintenance; any Process Guidance departed from; any deviation from the Initial Approach or the Deliverable order; findings a gate reported below its threshold, pre-existing issues left as unrelated to the change, and the debt `/do` hands over, item by item as supplied, offering `ticket-up` for any the user wants worked; each offer flagged for a person rather than accepted — whether the run flagged it or the Manifest's `ASM-*` entries carry it — and each decision record written with an agent as its decider, with what accepting the offer or reviewing the record would change; and any costly-threshold concern the run recorded while continuing repairs. Include these even when the execution log already holds them. Carry any drafted Taste entry `/do` supplies verbatim, with its question for the user's yes.

**The user's call.** A decision is the user's call when two careful people with
the same evidence could reasonably decide it differently, and the difference
would matter to the user. Test each material decision against that sentence;
your own confidence does not settle it. At a user's call, check the user's Taste
entries — ratified preferences in a `## Taste` section of a loaded memory file.
Follow an entry only where it clearly bears: it speaks to this kind of call, and
following it would change the choice. A general lean that would tilt almost any
call, such as less effort or lower cost, does not bear on its own. Otherwise
decide on the evidence. Wherever decisions are reported, list the user's calls
first, each with the alternative not taken and what decided it — the entry
followed, or that no entry applied.

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

**If the user later supplies a scope or requirement change**, invoke `define`
with the Manifest path, then resume the executor. If they clear the blocker
or supply the missing context, resume it directly. Their response is steering;
resumed execution remains unattended.
