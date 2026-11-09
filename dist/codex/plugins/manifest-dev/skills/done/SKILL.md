---
name: done
description: 'Completion marker for the /do workflow. Outputs a plain-prose summary of what was built. Called by /do after the Outcome and every current Acceptance Criterion and Global Invariant has fresh PASS evidence, when the manifest is complete, all criteria pass, or the workflow needs to wrap up with a completion summary.'
user-invocable: false
---

Receive the manifest path from `/do`, along with the basis on which the Outcome and each Acceptance Criterion and Global Invariant was judged to hold, and the disposition of its bounded mandatory build work.

**The user's call.** A decision is the user's call when two careful people with
the same evidence could reasonably decide it differently, and the difference
would matter to the user. Test each material decision against that sentence;
your own confidence does not settle it. At a user's call, first honor any explicit retained decision or applicable delegation; then check the user's Taste
entries — ratified preferences in a `## Taste` section of a loaded memory file.
Follow an entry only where it clearly bears: it speaks to this kind of call, and
following it would change the choice. A general lean that would tilt almost any
call, such as less effort or lower cost, does not bear on its own. Otherwise
decide on the evidence. Wherever decisions are reported, list first each decision record the run
reopened, with the reason set aside and what reversing would cost, then the
user's calls, each with the alternative not taken and what decided it — the entry
followed, or that no entry applied.

Emit a completion summary in plain prose, in this order.

Open with one line: what was built, and that the Outcome and every gate holds.

Then what is the person's to decide or accept. List each decision record the run reopened and each user's call with its alternative, as *The user's call* above says. Where the Manifest's `ASM-*` entries record a request set aside for a project principle, name what was asked, the principle, what was built instead and the one change that restores what was asked. Name each offer flagged for a person rather than accepted, such as a setup-project update or a ticket-up handoff, whether the run flagged it or the Manifest's `ASM-*` entries carry it. Name each decision record written with an agent as its decider. For each offer and record, say what accepting or reviewing it would change. Carry any drafted Taste entry `/do` supplies verbatim, with its question for the user's yes.

Then the rest. Give the key changes (files, behavioral effect — not just paths), any Process Guidance departed from and any deviation from the Initial Approach or the Deliverable order with why, anything notable about how the work landed. Include material autonomous decisions and their rationale, including any material working-claim or evidence revision and its basis, and any Appetite revision and why its benefit justified the added complexity and maintenance. State the basis for the Outcome and each gate exactly as `/do` supplied it. Name the debt `/do` hands over, which is only what the run could not fix, item by item as supplied, offering `ticket-up` for any the user wants worked, and link the exercise evidence the surface kept. Never list a finding below a gate's bar or a pre-existing issue the run fixed on the way as handed over. Name the issues fixed on the way, and any test removed as useless or tautological with why. Name the execution log's path when `/do` kept one.

Name all of these even when an execution log already records them; a reader of the summary should not have to open the log to learn which advisory guidance was set aside or how the plan moved. Adapt detail to the task's complexity — a small fix gets a couple of sentences; a multi-deliverable refactor gets a paragraph or two. Multi-repo manifests: a single summary covers the whole manifest, naming which repos' deliverables were verified.

Reachable only after the Outcome and every current Acceptance Criterion and Global Invariant holds on fresh evidence, with none left unverified, failing, stale, actionably blocked, or pending escalation, and the bounded mandatory build work is finished or validly routed under `/do`'s rules. An unresolved amendment or necessary missing evidence prevents completion. Report the executor's supported finding dispositions without adding a reviewer-consensus condition. End with the mandatory trailing line — directive, not observational, because the manifest stays the source of truth post-completion:

*If the next message describes a change or new requirement (not a pure question), invoke `/define <this-manifest-path>` to amend. Pure questions are answered inline.*
