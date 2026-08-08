---
name: done
description: 'Completion marker for the /do workflow. Outputs a plain-prose summary of what was built. Called by /do after every Acceptance Criterion and Global Invariant has fresh PASS evidence, when the manifest is complete, all criteria pass, or the workflow needs to wrap up with a completion summary.'
user-invocable: false
metadata:
  internal: true
---

Receive the manifest path, selected verification mode, explicit or inherited verifier-model provenance, gate ledger, and the selected verification reference's evidence/provenance wording from `/do`.

Emit a completion summary in plain prose: what was built, the key changes (files, behavioral effect — not just paths), any Process Guidance departed from and any deviation from the Initial Approach or the Deliverable order with why, anything notable about how the work landed. State the verification mode, model provenance, and evaluator provenance exactly from the supplied ledger and selected-reference wording; do not translate the mode into a second inline policy here. Name any findings a gate reported below its threshold, too — they were handed over rather than repaired, and this summary is where the user meets them — and any gate whose bar the run read as suspect without a user to ask, with what the rounds beneath it turned up. Name all of these even when an execution log already records them; a reader of the summary should not have to open the log to learn which advisory guidance was set aside or how the plan moved. Adapt detail to the task's complexity — a small fix gets a couple of sentences; a multi-deliverable refactor gets a paragraph or two. Multi-repo manifests: a single summary covers the whole manifest, naming which repos' deliverables were verified.

Reachable only after every Acceptance Criterion and Global Invariant has fresh PASS evidence under the selected mode in `/do`'s gate ledger, with no unverified, FAIL, stale, BLOCKED/actionable, or escalation-pending criteria. End with the mandatory trailing line — directive, not observational, because the manifest stays the source of truth post-completion:

*If the next message describes a change or new requirement (not a pure question), invoke `/manifest-dev:define <this-manifest-path>` to amend. Pure questions are answered inline.*
