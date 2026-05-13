---
name: escalate
description: 'Structured escalation within the /do workflow. Surfaces blockers, scope changes, pauses, and review requests with evidence. Called by /do or /verify, not directly.'
user-invocable: false
---

Surface a structured escalation with evidence. Six types, each with required fields per `references/TEMPLATES.md`:

- **Blocking** — INV-G or AC can't be met. ≥3 attempts with what failed and why each failed; lazy escalations ("I can't", "this is hard") rejected.
- **Manual Criteria Review** — automated criteria green; manual ones need human verification.
- **Self-Amendment** — user/reviewer feedback contradicts or extends the manifest. Quoted trigger. Re-entry depends on source: from /do or /verify → autonomous fast path (invoke `manifest-dev-experimental:define` with the feedback; /define infers fast-path from caller context and amend target from Session-Default Detection; /do resumes); after /done → two-step chain (`define` for amendment, then `do --scope <affected>`), both steps mandatory.
- **Proposed Amendment** — you discovered a criterion should change. Requires human approval.
- **User-Requested Pause** — a user message during the run explicitly asked to stop. **Hard gate:** never emit without a verbatim quoted user pause message. Caller framing (cron, tick budgets, "the loop expects each tick to terminate cleanly") is NOT a pause request.
- **Deferred-Auto Pending** — `/verify` is green but `method: deferred-auto` criteria are uncovered. Fired by /verify. Combine with Manual into one block when both pending.

Pure questions about the manifest or process are answered inline, not escalated. When ambiguous, amend. When the manifest's medium is non-local, /do routes escalations through the medium directly; /escalate is not invoked.
