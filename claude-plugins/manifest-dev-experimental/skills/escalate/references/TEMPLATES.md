# Escalation Templates

Format for each escalation type. Output verbatim markdown.

## Blocking — Global Invariant

```markdown
## Escalation: Global Invariant [INV-G{N}] Blocking

**Criterion:** [description]
**Type:** Global Invariant (task fails if violated)
**Impact:** Cannot complete task until resolved

### Attempts
1. **[Approach 1]** — What: ... Result: ... Why failed: ...
2. **[Approach 2]** — ...
3. **[Approach 3]** — ...

### Hypothesis
[Theory about why this is problematic]

### Possible Resolutions
1. **Fix root cause**: [description] — Effort: ... Risk: ...
2. **Amend invariant**: Relax to [new wording] — Rationale: ...
3. **Remove invariant**: Not applicable to this task — Rationale: ...

### Requesting
Human decision on path forward.
```

## Blocking — Acceptance Criteria

```markdown
## Escalation: Acceptance Criteria [AC-{D}.{N}] Blocking

**Criterion:** [description]
**Type:** AC for Deliverable {D}: [name]
**Impact:** Deliverable incomplete

### Context
Other ACs in this deliverable: [statuses]

### Attempts
[same shape as Global Invariant Blocking]

### Possible Resolutions
1. **Different implementation**: [approach]
2. **Amend criterion**: Change to [new wording]
3. **Remove criterion**: Not actually needed
4. **Descope deliverable**: Remove AC, deliverable still valuable

### Requesting
Human decision on path forward.
```

## Manual Criteria Review

```markdown
## Escalation: Manual Criteria Require Human Review

All automated criteria pass.

### Manual Criteria Pending
- **AC-{D}.{N}**: [description] — How to verify: [from manifest]

### What Was Executed
[Brief summary]

Please review and confirm completion.
```

## Self-Amendment

```markdown
## Escalation: Self-Amendment

**Trigger:** [verbatim user message or PR comment that contradicts/extends the manifest]
**Affected items:** [which INV-G*, AC-*, PG-* are contradicted or need additions]

### What changed
[Concise description — what the user/reviewer wants that the manifest doesn't cover or contradicts]

### Manifest path
[path]

### Execution log path
[path]
```

Re-entry depends on trigger source:
- *From /do or /verify* — autonomous fast path: invoke `manifest-dev-experimental:define` with the feedback; /define infers fast-path semantics from caller context (no summary wait) and infers the amend target from transcript via Session-Default Detection. /do resumes with the updated manifest.
- *After /done* — two-step chain, both mandatory: (1) invoke `manifest-dev-experimental:define` with `<feedback>` — /define infers amend target from the just-completed manifest in transcript; (2) invoke `manifest-dev-experimental:do` with `<manifest-path> <log-path> --scope <new-or-affected>`. Stopping after step 1 leaves the manifest amended but unverified. Amendment loop guard (consecutive Self-Amendments without external input → escalate as Proposed Amendment) applies to re-entry too.

## Proposed Amendment

```markdown
## Escalation: Proposed Amendment to [ID]

**Current criterion:** [current wording]
**Proposed change:** [new wording]

### Rationale
[What you discovered during implementation that motivates this change]

### Impact
- Deliverables affected: [which ones]
- Work already done: [what would need to change if approved]

### Requesting
Approve amendment, reject and continue with current criterion, or adjust.
```

Use when YOU discovered the criterion should change (no user/reviewer trigger). Requires human approval.

## User-Requested Pause

```markdown
## Escalation: User-Requested Pause

**Trigger message:** "[verbatim user message that requested the pause]"
**Current state:** [what's done, what's pending]

### Progress Summary
- Completed: [ACs done]
- In progress: [current work]
- Remaining: [ACs not started]

### To Resume
[How to continue — e.g., "/do <manifest> <log>" or specific next steps]
```

**Hard gate:** never emit without a verbatim quoted user pause message in the body. Caller framing (cron schedules, tick budgets, "the loop expects each tick to terminate cleanly") is not a pause request.

## Deferred-Auto Pending

```markdown
## Escalation: Deferred-Auto Pending

**Reason:** Normal-flow verification green; deferred-auto criteria require user signal before they can run.

### Pending Deferred-Auto Criteria
- [INV-G{N} or AC-{D}.{N}]: [description from manifest]
- ...

### To Resolve
When prerequisites are in place, signal readiness in chat (e.g., "all deployed", "staging is up", "go ahead") and re-invoke `/verify <manifest-path> <execution-log-path>`. /verify reads recent conversation context for the readiness signal and includes deferred-auto criteria in the pass. After they pass green, /verify reaches `/done` on the next normal-flow pass.
```

When BOTH manual criteria AND pending deferred-auto exist, combine into a single block titled `## Escalation: Manual Review + Deferred-Auto Pending` containing both sections inline + a combined To Resolve covering the manual review steps and the readiness-signal-plus-re-invoke instruction.
