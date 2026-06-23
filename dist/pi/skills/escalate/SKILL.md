---
name: escalate
description: 'Structured escalation when /do hits an unrecoverable blocker. Surfaces what was tried, why it failed, and what the user can decide. Called by /do when work is blocked, cannot proceed, hits an unrecoverable failure, needs a user decision, or gets stuck.'
user-invocable: false
---

Surface a blocker with evidence: the criterion (INV-G or AC ID) that can't be met, what was tried and why each attempt failed, the resolutions you see (fix path, amend the criterion, drop it, descope), and what you need from the user to unblock. Lazy escalations ("I can't", "this is hard") are rejected — show the attempts.

A BLOCKED verifier verdict (e.g., "deploy hasn't happened yet", "awaiting human approval") routes here too, with the BLOCKED note quoted from the verifier and the suggested user action carried through. Pure questions about the manifest or process are answered inline by /do, not escalated.

**If the user responds with a scope change rather than addressing the blocker** ("change AC-X", "drop that criterion", "add a check for Y", "actually we also need Z"), invoke `/define <manifest-path>` to amend the manifest, then resume /do. Otherwise (user clears the blocker or supplies missing context), resume /do directly.
