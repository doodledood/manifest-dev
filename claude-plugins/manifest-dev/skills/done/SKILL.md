---
name: done
description: 'Completion marker for the /do workflow. Outputs a plain-prose summary of what was built. Called by /do after every Acceptance Criterion and Global Invariant has fresh PASS evidence, when the manifest is complete, all criteria pass, or the workflow needs to wrap up with a completion summary.'
user-invocable: false
---

Receive the manifest path from `/do`, along with the basis on which each Acceptance Criterion and Global Invariant was judged to hold.

Include material autonomous decisions and their rationale, including any Appetite
revision and why its benefit justified the added complexity and maintenance, even
when already recorded in the execution log.

Emit a completion summary in plain prose: what was built, the key changes (files, behavioral effect — not just paths), any Process Guidance departed from and any deviation from the Initial Approach or the Deliverable order with why, anything notable about how the work landed. State the basis for each gate exactly as `/do` supplied it. Name any findings a gate reported below its threshold, and any pre-existing issue the run met but left as unrelated to the change, too — they were handed over rather than repaired, this summary is where the user meets them, and `ticket-up` is on offer for any the user wants worked — and any gate whose bar the run read as suspect without a user to ask, with what the rounds beneath it turned up. Name all of these even when an execution log already records them; a reader of the summary should not have to open the log to learn which advisory guidance was set aside or how the plan moved. Adapt detail to the task's complexity — a small fix gets a couple of sentences; a multi-deliverable refactor gets a paragraph or two. Multi-repo manifests: a single summary covers the whole manifest, naming which repos' deliverables were verified.

Reachable only after every Acceptance Criterion and Global Invariant holds on fresh evidence, with none left unverified, failing, stale, actionably blocked, or pending escalation. End with the mandatory trailing line — directive, not observational, because the manifest stays the source of truth post-completion:

*If the next message describes a change or new requirement (not a pure question), invoke `/define <this-manifest-path>` to amend. Pure questions are answered inline.*
