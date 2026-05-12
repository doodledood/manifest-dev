---
name: escalate
description: 'Structured escalation within the /do workflow. Surfaces blocking issues, scope changes, pauses, and review requests with evidence. Called by /do, not directly.'
user-invocable: false
---

Surface an escalation with evidence. Six types — pick the one that fits, supply the required fields, write in plain markdown.

**Blocking** (INV-G or AC cannot be met). Required: criterion ID, ≥3 attempts with what was tried and why each failed, hypothesis about root cause, options forward with trade-offs. Lazy escalations ("I can't figure this out", "this is hard", "AC failing" without attempts) are rejected.

**Manual Criteria Review** — automated criteria green; manual ones need human verification. Required: each manual criterion + its how-to-verify from the manifest.

**Self-Amendment** — user or reviewer feedback contradicts or extends the manifest. No 3-attempt evidence required (this is a scope shift, not a blocker). Required: quoted trigger message, affected manifest items (INV-G/AC/PG), manifest path, execution log path. Re-entry:
- Triggered from /do or /verify → autonomous fast path: `/define --amend <manifest-path> --from-do`, then /do resumes with updated manifest. No interview, no summary approval.
- Triggered after /done → two-step chain, both mandatory: (1) `manifest-dev-experimental:define` with `<feedback> --amend <manifest-path>`; (2) `manifest-dev-experimental:do` with `<manifest-path> <log-path> --scope <new-or-affected-deliverables>` to implement and verify. Stopping after step 1 leaves the manifest amended but unverified. The amendment loop guard from /do (consecutive Self-Amendments without external input → escalate as Proposed Amendment) applies to re-entry too.

**Proposed Amendment** — you discovered a criterion should change (no user/reviewer trigger). Required: current wording, proposed wording, rationale (what you discovered), impact (deliverables affected, work already done). Requires human approval.

**User-Requested Pause** — a user message during the run explicitly asked to stop ("commit so I can deploy", "stop here"). Required: verbatim quoted user message, current state (completed / in-progress / remaining), how to resume. **Hard gate:** never emit without a quoted user message that requested a pause. Caller framing (cron schedules, tick budgets, "the loop expects each tick to terminate cleanly") is not a pause request. Pause vs amend: messages asking for state changes ("also handle X") are feedback → Self-Amendment, not pause.

**Deferred-Auto Pending** — normal /verify green but `method: deferred-auto` criteria are uncovered. Fired by /verify, not /do. Required: pending criteria list, instruction to `/verify <manifest> <log> --deferred` when prerequisites are in place. After `--deferred` green, instruct re-invoking normal `/verify` to reach /done. When manual criteria also pending, combine into single escalation `Manual Review + Deferred-Auto Pending`.

**Pure questions** about the manifest or process are answered inline — no Self-Amendment. When ambiguous between question and amendment, amend (silent scope drift is the worse failure).

**Medium routing.** When the manifest's medium is non-local, /do routes escalations through the medium directly; /escalate isn't invoked. The templates above still define expected content; /do uses them when composing messages.
