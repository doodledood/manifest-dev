---
name: done
description: 'Completion marker for the /do workflow. Outputs a plain-prose summary of what was built. Called by /do after every Acceptance Criterion and Global Invariant has fresh PASS evidence, when the manifest is complete, all criteria pass, or the workflow needs to wrap up with a completion summary.'
user-invocable: false
metadata:
  internal: true
---

Emit a completion summary in plain prose: what was built, the key changes (files, behavioral effect — not just paths), trade-offs applied, anything notable about how the work landed. Adapt detail to the task's complexity — a small fix gets a couple of sentences; a multi-deliverable refactor gets a paragraph or two. Multi-repo manifests: a single summary covers the whole manifest, naming which repos' deliverables were verified.

Reachable only after every Acceptance Criterion and Global Invariant has fresh independent verifier PASS evidence in /do's gate ledger, with no unverified, FAIL, stale, BLOCKED/actionable, or escalation-pending criteria. End with the mandatory trailing line — directive, not observational, because the manifest stays the source of truth post-completion:

*If the next message describes a change or new requirement (not a pure question), invoke `/define <this-manifest-path>` to amend. Pure questions are answered inline.*
