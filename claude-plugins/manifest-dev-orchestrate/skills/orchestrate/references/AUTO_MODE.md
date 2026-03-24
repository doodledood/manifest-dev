# Auto Mode

`--auto` makes the agent act as the owner. All phases still run. External stakeholders (Slack channels, PR reviewers, QA testers) are still messaged and waited on. Only decisions that would route to the owner are automated.

In solo/local mode, this means effectively full autonomy. In Slack+GitHub mode, the agent posts to channels, waits for reviewers, waits for QA — but handles owner decisions itself.

## Implied Defaults

`--auto` applies these defaults. Each is overridable by an explicit flag:

| Implied default | Override with | Effect |
|----------------|---------------|--------|
| `--interview autonomous` | `--interview <other>` | Define builds manifest with agent-driven interview |
| `--medium local` | `--medium <other>` | No messaging coordinator (unless overridden) |
| `--review-platform github` | `--review-platform <other>` | Full PR review cycle (default) |

**Flag resolution order**: Parse `--auto` first, apply implied defaults, then apply any explicit flags as overrides. Example: `--auto --interview thorough` → thorough interactive interview (override), auto applies to all other phases.

## Per-Phase Behavioral Deltas

Each section describes what changes when auto mode is active. External stakeholder interactions are unaffected — only owner-routed decisions change.

### Phase 0: Preflight

- **With messaging coordinator** (medium ≠ local): Skip AskUserQuestion for stakeholder gathering. Instead, use available context (task description, channel info from flags) to fill stakeholder details autonomously. If critical info is missing (e.g., no channel specified for Slack), halt and ask the user.
- **Local mode** (medium = local): Skip stakeholder gathering entirely — no external stakeholders in solo mode.
- Log decision: what context was used, what was inferred.

### Phase 1: Define

- Implied `--interview autonomous` (unless overridden). The manifest-define-worker drives /define with agent-decided answers.
- No change to how TEAM_CONTEXT or the define-worker operates — the `--interview` flag controls behavior within /define itself.

### Phase 2: Manifest Review

- **Owner approval is automatic**: The agent approves the manifest without waiting for the owner. Log: "Auto mode: manifest approved at [path]."
- **Stakeholder review via medium is unaffected**: If a messaging coordinator is active, the manifest is still posted to stakeholders for review. Wait for stakeholder responses as normal. Only the owner's approval gate is removed.
- **Local mode**: No approval gate (no external stakeholders to wait for). Proceed directly to Phase 3.

### Phase 3: Execute

- **Escalations**: The agent resolves owner-routed escalations autonomously using best judgment. Each resolution is logged with context, decision, and reasoning.
- **Halt condition**: If an escalation is truly unresolvable — missing credentials, ambiguous requirements with no reasonable default, conflicting constraints with no clear priority — halt and ask the user. Auto mode is not silent-failure mode.
- **Stakeholder-routed escalations** (via messaging coordinator): Still routed to stakeholders normally. Only escalations that would go to the owner are auto-resolved.
- **Verification hard gate**: Unchanged. Verification is automated and mandatory regardless of auto mode.

### Phase 4: PR Review

- **Owner-routed questions**: When a review comment or thread needs the owner's input (e.g., "needs-clarification" from manifest-define-worker, disputes, or reviewer resistance), the agent answers as the owner using best judgment.
- **Reviewer interactions**: Unchanged. PR reviews are still requested, waited on, and processed normally. Bot and human comment handling follows the same triage flow.
- **Fix loop**: Unchanged. manifest-define-worker evaluates, manifest-executor fixes.
- **Escalation on repeated failure**: When the existing escalation threshold is reached (per SKILL.md), the agent resolves as the owner instead of routing to the user. Logged.

### Phase 5: QA

- **Owner-routed QA questions**: The agent answers as the owner.
- **QA testing**: If external QA stakeholders exist (via medium), QA is still routed to them and waited on normally. Only owner decisions during QA are automated.
- **Local mode**: The agent performs QA itself — evaluating deliverables against the manifest's acceptance criteria and logging pass/fail dispositions.
- **Escalation on repeated failure**: Same as Phase 4 — agent resolves as the owner. Logged.

### Phase 6: Done

- No change. Completion summary and teammate shutdown proceed as normal.

## Decision Log

All decisions the agent makes as the owner are logged to `/tmp/orchestrate-auto-decisions-{run_id}.md`.

**Entry format:**
```
## [Phase N] <Decision Type>
**Context:** <what triggered this decision>
**Decision:** <what the agent decided>
**Reasoning:** <why this choice was made>
```

**What gets logged:**
- Phase 0: Inferred stakeholder context
- Phase 1: Interview decisions (logged by /define's autonomous mode, not duplicated here)
- Phase 2: Manifest approval
- Phase 3: Each auto-resolved escalation
- Phase 4: Each owner-routed PR review response
- Phase 5: Each owner-routed QA response, local-mode QA dispositions

## Resume Behavior

The `auto` flag persists in `state.flags`. On resume with `auto: true`, re-read this document and re-apply all behavioral deltas. If `--auto` is provided alongside `--resume`, it overrides the stored value (in either direction).

## Halt Conditions

Auto mode halts and asks the user when:
- **Missing credentials**: A phase requires authentication or secrets not available to the agent.
- **Ambiguous requirements**: No reasonable default exists and multiple valid interpretations would lead to substantially different outcomes.
- **Conflicting constraints**: Two requirements contradict and there's no clear priority from the manifest's trade-offs.
- **Coordinator failure**: A coordinator goes unresponsive (existing escalation path — auto mode doesn't change this).
- **Repeated failure**: A problem persists after auto-resolution attempts and the agent's judgment is exhausted.

When halting, the agent logs what it tried, why it's stuck, and what options it sees for the user.
