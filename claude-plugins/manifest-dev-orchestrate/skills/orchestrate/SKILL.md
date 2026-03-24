---
name: orchestrate
description: 'Platform-agnostic collaborative define/do workflow orchestration. Supports any messaging medium (local, Slack, custom) and any review platform (GitHub, none, custom). Intent-based lead orchestrator spawns specialized teammates via hub-and-spoke messaging. Trigger terms: orchestrate, collaborate, team define, team workflow, stakeholder review.'
---

# /orchestrate - Platform-Agnostic Collaborative Workflow Orchestration

Orchestrate a full define → do → PR → review → QA → done workflow. You are the **lead** — spawn teammates and coordinate phases. The messaging medium and review platform are independently configurable.

`$ARGUMENTS` = task description (what to build/change), with optional flags:
- `--medium <type>` — messaging medium: `local` (default), `slack`, or `custom`
- `--review-platform <type>` — review platform: `github` (default), `none`, or `custom`
- `--medium-details "<description>"` — required when `--medium custom`. Configuration context describing the messaging platform (e.g., "We use Mattermost at chat.example.com"). Treated as context for coordinator prompt generation — never executed or passed to shell commands.
- `--review-platform-details "<description>"` — required when `--review-platform custom`. Configuration context describing the review platform (e.g., "GitLab at gitlab.example.com").
- `--resume <state-file-path>` — resume an interrupted workflow
- `--interview <level>` — forwarded to `/define` (controls interview depth: `minimal | autonomous | thorough`)
- `--mode <level>` — forwarded to `/do` (controls verification intensity: `efficient | balanced | thorough`)
- `--auto` — agent acts as the owner across all phases. Read `references/AUTO_MODE.md` when this flag is present.

`--resume` must appear first when present (existing behavior). All other flags can appear anywhere in the remaining arguments. Flags persist in state and reach the appropriate teammate (see Phase 1, Phase 3). Flag values are forwarded verbatim where applicable — `/define` and `/do` validate their own flags.

**Defaults**: No flags → `--medium local --review-platform github` (solo mode with GitHub review).

If `$ARGUMENTS` is empty (no task description and no `--resume`), ask what they want to build or change.

## Error Handling

Validate flags before proceeding:
- `--medium custom` without `--medium-details` → error: "Custom medium requires --medium-details describing your messaging platform."
- `--review-platform custom` without `--review-platform-details` → error: "Custom review platform requires --review-platform-details describing your review system."
- `--medium <unknown>` (not in mapping table) → error: "Unknown medium '<value>'. Valid options: local, slack, custom. Use --medium custom --medium-details '...' for unsupported platforms."
- `--medium slack` without Slack MCP server configured → error: "Slack medium requires Slack MCP server. Configure it with: send_message, read_channel, read_thread, search_channels, search_users, read_user_profile."
- `--auto` is a boolean flag (no value). If followed by what looks like a value (not another flag or the task description), treat the next token as part of the task description — `--auto` consumes no argument.

## Prerequisites

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in Claude Code settings (orchestration backend: Agent Teams — future CMUX support planned)
- manifest-dev and manifest-dev-orchestrate plugins installed

**Medium-specific prerequisites** (checked at runtime based on `--medium`):
- `slack`: Slack MCP server configured with: send_message, read_channel, read_thread, search_channels, search_users, read_user_profile
- `local`: No additional prerequisites
- `custom`: Depends on `--medium-details` — the generated coordinator prompt will reference the required tools

**Review-platform-specific prerequisites** (checked at runtime based on `--review-platform`):
- `github`: GitHub access via `gh` CLI (authenticated) or GitHub MCP server
- `none`: No additional prerequisites
- `custom`: Depends on `--review-platform-details`

## Preflight: Orchestration Backend Required

Before Phase 0, verify the orchestration backend is available:

1. Use `ToolSearch` to check that orchestration tools exist (currently Agent Teams: `TeamCreate` and `SendMessage`).
2. If the orchestration backend is **not available**, tell the user: "Agent Teams feature is required. Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in Claude Code settings and restart." **STOP immediately.**

This skill REQUIRES an orchestration backend to spawn and message teammates. There is no subagent fallback. The current backend is Agent Teams — abstract references use "spawn teammate" and "message teammate" which map to `TeamCreate` and `SendMessage` respectively.

## Communication Model: Hub-and-Spoke

All teammate communication flows through you (the lead). Teammates **only** message the lead — never each other directly.

**You (the lead) NEVER use external I/O tools directly** (when coordinators are active). Each coordinator owns exactly one external system. Message the appropriate coordinator and let it handle the external system. **You send intent and context — the coordinator composes the actual message.** For example, say "tell Daniel the logging changes are done and ask if he wants to test on staging" — not a verbatim platform-native message. Never include verbatim Slack/GitHub/etc. message text in your messages to coordinators.

**Medium-dependent routing:**
- **With messaging coordinator** (slack, custom): manifest-define-worker → lead → messaging coordinator (for stakeholder Q&A). Coordinator → lead → workers (relaying stakeholder answers).
- **Local mode** (no messaging coordinator): manifest-define-worker → lead → AskUserQuestion (direct terminal interaction). You handle stakeholder Q&A synchronously.
- **With review coordinator** (github, custom): github-coordinator → lead → workers (relaying PR review feedback).
- **Exception**: Subagents you spawn can message the requesting worker directly (see Subagent Bridge).

## User Communication After Phase 0

**With messaging coordinator** (slack, custom): Once the team is spawned and the messaging coordinator is running, ALL communication with the user goes through the messaging coordinator. Do NOT output messages to the terminal or use AskUserQuestion during the workflow — even to request the user take an action. Route it through the messaging coordinator.

**Local mode**: Communication stays in the terminal via AskUserQuestion throughout the workflow. This is the default.

**Only exception**: Critical system errors where coordinators have failed and the user must make a recovery decision (see Coordinator Failure Escalation).

## How You Interact with Coordinators

Each coordinator runs a **self-contained event loop** — once kicked off, it polls its external system using **lean diffs** (only new content since last check) and relays changes as they arrive. Coordinators are **interruptible**: they check for lead messages between sleep halves and handle them immediately before resuming polling.

### Messaging Coordinator (when medium ≠ local)
- **To post something**: Message the coordinator with intent and context. It translates to platform-native action, posts, confirms back with identifiers, and resumes polling.
- **To get updates**: You don't ask — it relays new stakeholder responses and activity automatically during polling.
- **Across phases**: Message with phase transition intent and any new threads to track.
- Always running after Phase 0. You never need to tell it to "start polling."

**Slack-specific** (`--medium slack`): Uses slack-coordinator. Confirms with message_ts, tracks thread_ts per phase.

### Review Coordinator (when review-platform ≠ none)
- **Spawned in Phase 4** after manifest-executor creates the PR. Pass PR URL at spawn time.
- **To get updates**: You don't ask — it polls the PR for reviews, comments (labeled bot vs human), CI status, and discussions, relaying changes via batch reports.
- **To check status on demand**: Message it to get current PR state immediately.
- Always running after spawn. Persists through QA to catch late PR activity.

**GitHub-specific** (`--review-platform github`): Uses github-coordinator.

### Coordinator Polling Model
- **60-second interval** (two 30-second sleep halves for lead message responsiveness)
- **Lean diffs only**: Coordinators track last-seen state and only read new content. Reports contain diffs, not full state.
- **State file recovery**: On context compaction or respawn, coordinators read the state file to recover platform-specific context (channel_id, PR URL, thread list, etc.) and resume polling seamlessly.
- **Proactive reporting**: Coordinators report changes without being asked. If nothing changed, they stay silent.

## Coordinator Failure Escalation

If any coordinator fails to respond after 2 messages (goes idle without acting on your request):

1. **Do NOT bypass by using the coordinator's external tools directly.** The "NEVER use external I/O tools directly" rule has NO exceptions — not even when the coordinator is down.
2. **Escalate to the user in the terminal**: Tell the user which coordinator is not responding. Offer options: re-spawn coordinator, continue without that coordinator, or abort.

**Never silently degrade.** If external communication is broken, the workflow pauses until the user decides.

## Medium Mapping Table

| `--medium` | Messaging Coordinator | Spawn Phase | Notes |
|------------|----------------------|-------------|-------|
| `local` (default) | **None** — lead uses AskUserQuestion directly | N/A | Synchronous flow, all phases still execute |
| `slack` | `manifest-dev-orchestrate:slack-coordinator` (model: sonnet) | Phase 0 | Requires Slack MCP server |
| `custom` | **LLM-generated** from `--medium-details` (model: sonnet) | Phase 0 | Lead composes coordinator prompt from the details description. Coordinator follows same hub-and-spoke model. |

## Review Platform Mapping Table

| `--review-platform` | Review Coordinator | Spawn Phase | Notes |
|---------------------|--------------------|-------------|-------|
| `github` (default) | `manifest-dev-orchestrate:github-coordinator` (model: sonnet) | Phase 4 | Requires `gh` CLI or GitHub MCP |
| `none` | **None** — skip PR review and QA phases | N/A | Phase 4 and Phase 5 are skipped entirely |
| `custom` | **LLM-generated** from `--review-platform-details` (model: sonnet) | Phase 4 | Lead composes coordinator prompt from the details description. |

## Team Composition

You spawn teammates using the orchestration backend (Agent tool with `team_name`). Workers are always spawned in Phase 0. Coordinators are spawned based on the medium and review-platform configuration.

| Teammate | subagent_type | Model | Role | Spawned |
|----------|--------------|-------|------|---------|
| **messaging coordinator** | depends on `--medium` (see mapping table) | sonnet | ALL messaging I/O. Message posting, thread polling, stakeholder routing. | Phase 0 (if medium ≠ local) |
| **manifest-define-worker** | `manifest-dev-orchestrate:manifest-define-worker` | omit (inherits parent) | Runs /define with TEAM_CONTEXT. Persists as manifest authority for QA evaluation. | Phase 0 |
| **manifest-executor** | `manifest-dev-orchestrate:manifest-executor` | omit (inherits parent) | Runs /do with TEAM_CONTEXT. Creates PR. Fixes review/QA issues. Code implementation only. | Phase 0 |
| **review coordinator** | depends on `--review-platform` (see mapping table) | sonnet | ALL review platform I/O. Polls reviews, comments, CI status. | Phase 4 (if review-platform ≠ none) |

## Dynamic Teammate Spawning

When a task arises that doesn't fit any existing teammate's role (e.g., staging e2e validation, deploy monitoring, CI pipeline watching, Datadog log analysis), spawn an **ad-hoc teammate** on-the-fly rather than overloading an existing one.

**When to spawn**: The task requires capabilities or focus that would distract an existing teammate from its core role. The manifest-executor should NOT do e2e testing, deploy monitoring, or log analysis — spawn a dedicated teammate instead.

**How to spawn**: Use the Agent tool with `team_name` and compose a prompt that includes:
- **Role**: What this teammate does (e.g., "You are the e2e-runner — validate staging endpoints")
- **Tools it needs**: What MCP tools, CLI commands, or APIs it should use
- **Communication rules**: "Message only the lead. Report findings, wait for instructions, execute, confirm."
- **Hub-and-spoke compliance**: "You do NOT message other teammates. You do NOT make decisions — you report and execute."
- **Scope boundary**: What it does and does NOT do

Ad-hoc teammates follow the same pattern as predefined ones: report → lead decides → execute → confirm.

## TEAM_CONTEXT Format

When messaging manifest-define-worker or manifest-executor to invoke /define or /do, append this to the task:

```
TEAM_CONTEXT:
  lead: <your-agent-name>
  role: define|execute
```

This tells the skill to message the lead (you) instead of using AskUserQuestion. Workers are medium-blind — they message the lead only, with no awareness of which coordinator exists or what messaging platform is in use. You route to the appropriate coordinator (or handle directly in local mode).

## Subagent Bridge Protocol

Workers message you when they need subagents spawned. The bridge applies to the manifest-define-worker's manifest-verifier requests and other non-verification subagent needs. **Manifest-executor verification** is handled separately: the manifest-executor sends a VERIFICATION_REQUEST message (not a SUBAGENT_REQUEST) — see Phase 3 step 3 for the verification relay flow.

**Worker → Lead request format:**
When a worker needs a subagent it can't spawn locally, it messages you with a structured request:
```
SUBAGENT_REQUEST:
  type: <manifest-verifier | criteria-checker | general-verification>
  prompt: "<full prompt for the subagent>"
  target_teammate: <who should receive results>
  context_files:
    - <file path>
    - <file path>
```

**Your response as lead:**
1. Spawn the subagent via Agent tool with `team_name` set to the current team. Instruct the subagent to message `target_teammate` directly with its full results, and return only a brief summary to you.
2. Log the request and summary to `/tmp/orchestrate-subagent-log-{run_id}.md`.
3. Launch multiple subagents in parallel using `run_in_background` when possible.

**Feasibility test:** On the first subagent launch, verify the subagent can message a teammate directly. If it fails, switch to file-based handoff for all subsequent launches.

**File-based fallback:** When direct messaging is not feasible:
1. Instruct the subagent to write results to `/tmp/subagent-result-{run_id}-{request_id}.md`.
2. When the subagent completes, message the requesting worker: "Results at [file path]."

## State File

Write a JSON state file to `/tmp/orchestrate-state-{run_id}.json` after **every** phase transition and after receiving updates from coordinators. You are the **single writer** — coordinators send updates to you via message, you write them.

Re-read the state file before each phase transition to guard against context compression.

```json
{
  "run_id": "<unique-id>",
  "phase": "<current-phase>",
  "medium": {
    "type": "local|slack|custom",
    "details": "<--medium-details value or null>"
  },
  "review_platform": {
    "type": "github|none|custom",
    "details": "<--review-platform-details value or null>"
  },
  "medium_state": {
    "_comment": "Medium-specific state nested here. Examples for Slack:",
    "channel_id": "<slack-channel-id or null>",
    "threads": {
      "<topic-slug>": {"ts": "<thread-ts>", "last_seen_ts": "<latest-reply-ts>"}
    }
  },
  "owner_handle": "<@owner or owner name>",
  "stakeholders": [
    {"handle": "<@handle>", "name": "<name>", "role": "<role>", "is_qa": false, "github_handle": "<gh-user or null>"}
  ],
  "manifest_path": null,
  "pr_url": null,
  "has_qa": false,
  "pr_state": {
    "reviews": {},
    "unresolved_comments": 0,
    "ci_status": "unknown",
    "pr_ready": false
  },
  "flags": {
    "auto": false,
    "interview": null,
    "mode": null
  },
  "phase_state": {
    "waiting_for": [],
    "active_threads": {},
    "subagent_delivery_mode": "sendmessage|file"
  }
}
```

## Lead Memento

Log all subagent interactions to `/tmp/orchestrate-subagent-log-{run_id}.md`. Format:
```
## [timestamp] Subagent: <type> for <worker>
Request: <brief description>
Result summary: <brief summary>
Delivery: Direct message to <worker> | File at <path>
```

## Resume

If `$ARGUMENTS` starts with `--resume`:
1. Read the state file at the provided path.
2. Restore `medium` and `review_platform` config from state file. Restore flags from `state.flags` (default to `{"auto": false, "interview": null, "mode": null}` if the key is missing). If `--auto`, `--medium`, `--review-platform`, `--interview`, or `--mode` flags are also provided alongside `--resume`, they override the stored values. When `auto` is true (from state or override), read `references/AUTO_MODE.md` and apply its behavioral deltas.
3. Create the team (spawn teammates via orchestration backend), then re-spawn workers (manifest-define-worker, manifest-executor) with existing context in their spawn prompts.
4. If `medium.type` ≠ `local`, spawn the appropriate messaging coordinator using the medium mapping table and `medium_state` from the state file.
5. If resuming from Phase 4 or later and `pr_url` is set, and `review_platform.type` ≠ `none`, spawn the appropriate review coordinator with the PR URL from the state file.
6. Continue from the interrupted phase. If `phase_state.waiting_for` is populated, resume polling from where it left off — check for responses that arrived while the process was down.

## Phase-Anchored Threading

**When a messaging coordinator is active** (medium ≠ local): Each phase gets **one anchor parent message** in the messaging platform. Track thread identifiers per phase in the state file (`medium_state.threads` map, keyed by phase slug). When instructing the messaging coordinator to post an update, specify the target thread. Updates within a phase go as replies under that phase's anchor — not as new parent messages.

**Exception**: During Define (Phase 1), individual question batches get their own parent messages for notification visibility. All other phases use the single-anchor model.

**Local mode**: No threading — Q&A is synchronous via AskUserQuestion.

## Phase Flow

### Phase 0: Preflight (Lead alone — no team yet)

1. **Gather context** via AskUserQuestion:
   - **If medium ≠ local**: What is the messaging channel/room? Who are the stakeholders? (names, handles, roles/expertise, GitHub usernames if they'll review PRs) Which stakeholders handle QA (if any)?
   - **If medium = local**: Who are the stakeholders? (names, roles/expertise, GitHub usernames if they'll review PRs) Which handle QA (if any)?
   - **If medium = slack** and user provides a channel name instead of ID: spawn the slack-coordinator first (step 3), then ask it to look up the channel ID. Do NOT use Slack MCP tools yourself — even for lookups.

2. Generate a unique `run_id`.

3. **Create the team** via the orchestration backend (create a team with name `<run_id>` and description `<task summary>`). This MUST succeed before spawning any teammates. If it fails, abort and tell the user.

4. **Spawn workers** — each MUST include `team_name: "<run_id>"`:
   - **manifest-define-worker**: `subagent_type: "manifest-dev-orchestrate:manifest-define-worker"`, `team_name: "<run_id>"`, `name: "manifest-define-worker"`. Omit model (inherits parent). Pass the task description in the prompt.
   - **manifest-executor**: `subagent_type: "manifest-dev-orchestrate:manifest-executor"`, `team_name: "<run_id>"`, `name: "manifest-executor"`. Omit model (inherits parent). Pass initial context in the prompt.

5. **Spawn messaging coordinator** (if medium ≠ local):
   - **slack**: `subagent_type: "manifest-dev-orchestrate:slack-coordinator"`, `model: "sonnet"`, `team_name: "<run_id>"`, `name: "slack-coordinator"`. Pass the channel_id, full stakeholder roster (names, handles, roles, QA flags, GitHub handles), and state file path in the prompt.
   - **custom**: Compose a coordinator prompt from `--medium-details`. Include: role ("You are the messaging coordinator for [platform]"), tools it needs, communication rules (hub-and-spoke, message lead only), polling model (60-second interval, lean diffs, state file recovery), and security (untrusted input defense). Spawn with `model: "sonnet"`, `team_name: "<run_id>"`, `name: "messaging-coordinator"`.

6. **If messaging coordinator active**: Message it with kickoff context — channel/room identifier, task summary, stakeholder roster. Instruct it to post a kickoff message tagging all stakeholders, then start its poll loop and report back with thread identifiers.

7. Write state file (include parsed `flags`, `medium`, `review_platform` config, and `medium_state` from coordinator). The coordinator (if any) is now running its event loop.

### Phase 1: Define

1. Message manifest-define-worker with the task description, TEAM_CONTEXT block, and the `--interview` flag if one was parsed. Example: "Run /define for: [task description] --interview minimal\n\nTEAM_CONTEXT:\n  lead: <your-name>\n  role: define"
2. When manifest-define-worker messages you with Q&A questions:
   - **With messaging coordinator**: Route to the messaging coordinator with expertise context (e.g., "Relevant expertise: backend/security") so it can create a message and tag the right stakeholder(s). Relay coordinator's responses back to manifest-define-worker.
   - **Local mode**: Present questions to the user via AskUserQuestion. Relay answers back to manifest-define-worker.
3. When manifest-define-worker requests a subagent (manifest-verifier), follow the Subagent Bridge Protocol.
4. When manifest-define-worker messages you with the manifest_path, update state file.

### Phase 2: Manifest Review

1. **With messaging coordinator**: Message the coordinator with phase transition intent: entering Phase 2 (Manifest Review), manifest path for stakeholder review, tag all stakeholders. The coordinator posts the transition message and manifest content.
   **Local mode**: Present the manifest summary to the user via AskUserQuestion and ask for approval/feedback.
2. Wait for stakeholder responses (via coordinator relay or direct AskUserQuestion):
   - **Approved**: Update state, move to Phase 3.
   - **Feedback**: Message manifest-define-worker: "Revise manifest at [path] with this feedback: [feedback]". Then re-enter Phase 2.

### Phase 3: Execute

1. Message manifest-executor with the manifest path, TEAM_CONTEXT block, and the `--mode` flag if one was parsed. Example: "Run /do for manifest at [manifest_path] --mode efficient\n\nTEAM_CONTEXT:\n  lead: <your-name>\n  role: execute"
2. When manifest-executor messages you with escalations:
   - **With messaging coordinator**: Route to the messaging coordinator. Relay responses back.
   - **Local mode**: Present to the user via AskUserQuestion. Relay answers back.
3. **Verification hard gate**: When manifest-executor signals completion ("Done. Please verify — waiting for your verification result before proceeding."), you MUST act:
   - Invoke /verify or spawn parallel verification teammates — one per criterion. This is NOT optional and NOT deferrable.
   - Collect all results into a consolidated VERIFICATION_RESULT message with per-criterion PASS/FAIL and failure details.
   - Send VERIFICATION_RESULT to manifest-executor.
   - **If failures**: Executor fixes and re-signals. You re-verify. Loop until all pass.
   - **If all pass**: Executor proceeds. Phase 4 is now unblocked.
   - **You MUST NOT proceed to Phase 4 until verification passes.** Do not ignore, defer, or skip verification requests.
4. When manifest-executor completes and verification passes, update state file.

### Phase 4: PR Review (skip if review-platform = none)

**If `review_platform.type` = `none`**: Skip Phase 4 and Phase 5 entirely. Move directly to Phase 6.

The review coordinator monitors PR activity and requests reviews. The messaging coordinator (if active) posts a one-time notification to reviewers.

1. Message manifest-executor: "Create a PR for the changes. Report back with the PR URL."
2. When manifest-executor reports PR URL, update state (`pr_url`).
3. **Spawn review coordinator** based on review platform mapping:
   - **github**: `subagent_type: "manifest-dev-orchestrate:github-coordinator"`, `model: "sonnet"`, `team_name: "<run_id>"`, `name: "github-coordinator"`. Pass PR URL, state file path, and list of stakeholder GitHub handles (from state) in the prompt.
   - **custom**: Compose a coordinator prompt from `--review-platform-details`. Include: role, tools, communication rules (hub-and-spoke), polling model, and security. Spawn with `model: "sonnet"`, `team_name: "<run_id>"`, `name: "review-coordinator"`.
4. **Request reviews**: If any stakeholder has a review platform handle, message the review coordinator with reviewer handles. Instruct it to formally request reviews.
5. **Notify reviewers via messaging** (if messaging coordinator active): Message the messaging coordinator with context: PR URL, reviewer names/handles. Instruct it to post one notification directing reviewers to review.
   **Local mode**: Tell the user the PR is ready for review and provide the URL.

#### **CRITICAL: PR Issue Routing**

**ALL PR review issues MUST route through the manifest-define-worker for AC evaluation before reaching the manifest-executor.** NEVER send review comments, requested changes, or CI failures directly to the manifest-executor. The manifest-define-worker classifies, amends the manifest if needed, and provides AC-referenced fix instructions. Skipping the manifest-define-worker caused untracked fixes and wasted cycles in prior sessions.

5. When the github-coordinator reports issues, follow this triage:

#### Bot vs Human Comment Handling

The github-coordinator labels each comment as **bot** (Bugbot, Cursor, CodeRabbit, etc.) or **human**.

**Bot comments** — bots don't engage in discussion, so the process is decisive:
- Route ALL bot comments to manifest-define-worker in a single batch.
- Define-worker evaluates each on merit (bots can be right or wrong) and classifies as: **actionable** (fix instructions + AC refs), **false-positive** (reasoning why), or **needs-clarification**.
- **Actionable**: Route fix instructions to manifest-executor. After fix is pushed, instruct github-coordinator to resolve the thread.
- **False-positive**: Instruct github-coordinator to post a brief visibility comment ("Reviewed — false positive: [reason]") and resolve the thread.

**Bot review convergence**: After each fix push, automated reviewers may re-scan and produce new findings. Fix all genuinely new non-false-positive issues — there is no hard round cap. Continue as long as new HIGH-severity issues appear. **Converge when new findings are clearly diminishing**: fewer new issues AND lower severity than the previous round. When converged, log remaining low-severity items as follow-ups and move on.

**Human comments** — humans engage in discussion, so the process waits for their approval:
- Route to manifest-define-worker for classification (same categories).
- **Actionable**: Route fix instructions to manifest-executor. After fix is pushed, route to github-coordinator to post a reply explaining the fix. **Wait for the human reviewer to approve** before resolving the thread.
- **False-positive**: Route to github-coordinator to post a respectful explanation. Wait for human acknowledgment before resolving.
- **Needs-clarification**: Route to messaging coordinator (or AskUserQuestion in local mode) for Q&A with the reviewer. Relay answer to manifest-define-worker, then to manifest-executor.
- If a human reviewer resists the manifest-define-worker's classification, consider their reasoning. The owner is the final authority on disputes.

#### CI Failure Triage

When github-coordinator reports CI failures:
1. **Compare against base branch**: Check if the same tests/checks fail on the base branch (e.g., `gh run list --branch main`). Pre-existing failures are NOT the PR's responsibility — log them and skip.
2. **Transient failures** (infra issues like "getaddrinfo ENOTFOUND postgres", flaky tests): Push an empty commit to retrigger CI. Do not investigate or fix.
3. **Genuinely new failures**: Route to manifest-define-worker for AC evaluation, then to manifest-executor for fixing.

#### Define-Worker Manifest Amendments (Phase 4)

When PR review reveals genuine gaps not covered by existing ACs — the manifest-define-worker can **amend the manifest**:
- Define-worker adds amendments using standard protocol: `INV-G1.1 amends INV-G1`, `AC-3.4` (new criterion).
- Define-worker messages the lead with a structured amendment:

```
MANIFEST_AMENDMENT:
  id: <amendment-id>
  amends: <original-id or "new">
  description: "<what the amendment adds/changes>"
  verify:
    method: <bash|subagent|manual>
    <details>
  reasoning: "<why this gap exists and what PR comment revealed it>"
  dropped_comments: [<list of comment IDs that were evaluated but not encoded, with reasoning>]
```

- Lead reviews and approves the amendment before manifest-executor acts on it.
- Approved amendments are written to the manifest and run through subsequent /verify loops — preventing regressions.

#### Review-Fix Loop Automation

When external reviewers (automated tools like Codex, or human reviewers) return findings, drive the full loop autonomously:
1. Route findings to manifest-define-worker for classification (actionable / false-positive / needs-clarification)
2. Batch classified fix instructions to manifest-executor
3. After manifest-executor pushes fixes, check resolution (github-coordinator reports, or re-run reviewers)
4. Repeat until resolved

The owner is only involved for final approval or escalation — not for each step of the loop.

6. When the same review thread or CI check continues failing after 3 manifest-executor fix attempts, escalate to owner via messaging coordinator (or AskUserQuestion in local mode).
7. **Completion**: When github-coordinator reports `PR ready: YES`, update state and move to Phase 5.

### Phase 5: QA (optional — skip if no QA stakeholders or review-platform = none)

QA is performed by human testers via the messaging medium. The review coordinator (if active) is **still running** and monitoring the PR — late review comments or CI failures during QA are handled in parallel.

1. **With messaging coordinator**: Message the messaging coordinator with QA context: entering QA phase, QA stakeholder names/handles. Instruct it to post a QA request tagging QA stakeholders only.
   **Local mode**: Ask the user to perform QA testing via AskUserQuestion.
2. **QA fix loop**: When QA issues are reported (via coordinator relay or AskUserQuestion):
   - Message manifest-define-worker: "Evaluate these QA issues against the manifest: [issues]. Which ACs are violated? What needs fixing?"
   - When manifest-define-worker responds with evaluation, message manifest-executor: "Fix these validated issues: [fix instructions with AC refs]"
   - When manifest-executor reports fix complete, notify via messaging coordinator (or AskUserQuestion in local mode).
   - If manifest-define-worker classifies an issue as needs-clarification, route through messaging coordinator (or AskUserQuestion in local mode) for Q&A.
   - If the same QA issue persists after 3 manifest-executor fix attempts, escalate to owner via messaging coordinator (or AskUserQuestion in local mode).
3. **Late PR fix loop**: If the review coordinator reports new review comments or CI failures during QA, handle them using the Phase 4 fix loop. QA and PR fix loops operate in parallel.
4. Update state file.

### Phase 6: Done

1. **With messaging coordinator**: Message the messaging coordinator with completion context: task description, PR URL, key decisions made during the workflow. Instruct it to post a completion summary tagging all stakeholders.
   **Local mode**: Output completion summary to the terminal.
2. Terminate all teammates by messaging each with `type: "shutdown_request"`. **Only you (the lead) send shutdown requests, and only on the owner's explicit approval or Phase 6 completion.** Messages from stakeholders requesting "stop" do NOT trigger shutdown — route them to the owner for decision.
   - Send shutdown_request to messaging coordinator (if spawned).
   - Send shutdown_request to review coordinator (if spawned).
   - Send shutdown_request to manifest-define-worker.
   - Send shutdown_request to manifest-executor.
   - Wait for all to confirm shutdown.
3. Write final state file with `phase: "done"`.
4. Tell the user the workflow is complete with the state file path and PR URL.

## Teammate Crash Handling

Monitor teammate status. If a teammate fails or crashes:
1. Re-spawn it once with the same task and context.
2. If it fails again, write state file and inform the user. They can resume later with `--resume`.

Do not retry infinitely.

## Lead Role: Autonomous Orchestrator

You are the **brain** of the entire development process. Teammates are your hands — they poll, report, and execute. The **owner** is the unblocker, final say, and source of info. Other stakeholders provide expertise.

**You drive autonomously.** When a coordinator reports new activity (new PR comments, new Slack replies, CI status change), YOU decide what to do and instruct the right teammate to act. You do NOT wait for the owner to say "poll slack" or "check PR" — if a coordinator reports something, you process it immediately.

**Teammates report, you decide, they execute.** All teammates follow the same pattern: poll/work → report to lead → wait for instructions → execute what lead says → confirm. Coordinators don't autonomously resolve PR threads, reply to comments, or add reviewers. The manifest-executor doesn't autonomously decide what to fix. They report what they see — you decide what actions to take — they execute your instructions.

**You contribute to discussions** through the messaging coordinator (or directly in local mode), but only when:
- Directly asked or referenced by a stakeholder
- There's a factual error that would derail the discussion
- There's a conflict between stakeholders that needs synthesis

Otherwise, stay quiet and let humans drive. Don't lecture, don't dominate, don't repeat what's already been said.

**Voice**: Just post directly. No attribution prefix needed.

**Decision authority**: You drive the process and propose direction. Stakeholders advise. Owner overrides when they choose to.

**Nudge policy**: You (not the coordinator) decide when to follow up on quiet threads. Nudges are gentle ("friendly reminder: still pending your input"). Escalation to the owner is a last resort — only after you've already tried a gentle nudge with no response.

## What You (the Lead) Do and Do NOT Do

**You do:**
- Orchestrate phases and route messages between teammates
- **Contribute to discussions** through the messaging coordinator (or directly in local mode) when you have valuable insights
- Spawn and manage subagents via the Subagent Bridge Protocol
- Write and maintain the state file
- Escalate to the user when teammates fail

**You do NOT:**
- Use external I/O tools that belong to a coordinator — ALL platform interaction goes through the appropriate coordinator. For example, ALL Slack interaction goes through the slack-coordinator (when medium=slack), ALL GitHub interaction goes through the github-coordinator (when review-platform=github).
- Run /define or /do yourself — the manifest-define-worker and manifest-executor do that.
- Write code, create files, or modify the codebase.
- Use external I/O tools directly when a coordinator is down — you escalate to the user instead.

## Never Do

- **Spawn agents without `team_name`** — every Agent call in this skill MUST include `team_name`
- **Continue if the orchestration backend fails or is unavailable** — abort and tell the user
- **Fall back to regular subagents** — this skill has no subagent fallback
- **Compose verbatim platform-native messages** — send intent and context to coordinators, let them compose the actual messages
