---
name: slack-collab
description: 'Orchestrate team collaboration on define/do workflows through Slack using Agent Teams. The skill acts as the team lead, spawning specialized teammates (slack-coordinator, define-worker, executor) that coordinate via mailbox messaging. Trigger terms: slack, collaborate, team define, team workflow, stakeholder review.'
---

# /slack-collab - Collaborative Define/Do via Slack (Agent Teams)

Orchestrate a full define → do → PR → review → QA → done workflow with your team through Slack. You are the **lead** — spawn teammates and coordinate phases.

`$ARGUMENTS` = task description (what to build/change), or `--resume <state-file-path>` to resume.

If `$ARGUMENTS` is empty, ask what they want to build or change.

## Prerequisites

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in Claude Code settings
- Slack MCP server configured with: send_message, read_channel, read_thread, search_channels, search_users, read_user_profile
- manifest-dev and manifest-dev-collab plugins installed

## Communication Model: Hub-and-Spoke

All teammate communication flows through you (the lead). Teammates **only** message the lead — never each other directly.

- **define-worker → lead → slack-coordinator** (for stakeholder Q&A)
- **executor → lead → slack-coordinator** (for escalations)
- **slack-coordinator → lead → workers** (relaying stakeholder answers)
- **Exception**: Subagents you spawn can SendMessage directly to the requesting worker (see Subagent Bridge).

## Team Composition

You create **three teammates**, each defined by an agent file in `agents/` relative to this plugin:

| Teammate | Agent File | Model | Role |
|----------|-----------|-------|------|
| **slack-coordinator** | `agents/slack-coordinator.md` | haiku | ALL Slack I/O. Message posting, thread polling, stakeholder routing. Prompt injection defense. |
| **define-worker** | `agents/define-worker.md` | default | Runs /define with TEAM_CONTEXT. Persists as manifest authority for QA evaluation. |
| **executor** | `agents/executor.md` | default | Runs /do with TEAM_CONTEXT. Creates PR. Fixes QA issues. |

## TEAM_CONTEXT Format

When messaging define-worker or executor to invoke /define or /do, append this to the task:

```
TEAM_CONTEXT:
  lead: <your-agent-name>
  coordinator: slack-coordinator
  role: define|execute
```

This tells the skill to message the lead (you) instead of using AskUserQuestion. You then route to the coordinator for stakeholder interaction.

## Subagent Bridge Protocol

Workers cannot spawn subagents (no Agent tool access). When they need verification (manifest-verifier, criteria-checkers), they message you with a structured request:

**Worker → Lead request format:**
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
1. Spawn the subagent via Agent tool with `team_name` set to the current team. Instruct the subagent to send its full results directly to `target_teammate` via SendMessage, and return only a brief summary to you.
2. Log the request and summary to `/tmp/collab-subagent-log-{run_id}.md`.
3. Launch multiple subagents in parallel using `run_in_background` when possible.

**Feasibility test:** On the first subagent launch, verify the subagent can SendMessage to a teammate. If it fails, switch to file-based handoff for all subsequent launches.

**File-based fallback:** When SendMessage is not feasible:
1. Instruct the subagent to write results to `/tmp/subagent-result-{run_id}-{request_id}.md`.
2. When the subagent completes, message the requesting worker: "Results at [file path]."

## State File

Write a JSON state file to `/tmp/collab-state-{run_id}.json` after **every** phase transition and after receiving thread updates from the coordinator. You are the **single writer** — coordinator sends thread updates to you via message, you write them.

Re-read the state file before each phase transition to guard against context compression.

```json
{
  "run_id": "<unique-id>",
  "phase": "<current-phase>",
  "channel_id": "<slack-channel-id>",
  "owner_handle": "<@owner>",
  "stakeholders": [
    {"handle": "<@handle>", "name": "<name>", "role": "<role>", "is_qa": false}
  ],
  "threads": {"<topic-slug>": "<thread-ts>"},
  "manifest_path": null,
  "pr_url": null,
  "has_qa": false,
  "phase_state": {
    "waiting_for": [],
    "active_threads": {},
    "subagent_delivery_mode": "sendmessage|file"
  }
}
```

## Lead Memento

Log all subagent interactions to `/tmp/collab-subagent-log-{run_id}.md`. Format:
```
## [timestamp] Subagent: <type> for <worker>
Request: <brief description>
Result summary: <brief summary>
Delivery: SendMessage to <worker> | File at <path>
```

## Resume

If `$ARGUMENTS` starts with `--resume`:
1. Read the state file at the provided path.
2. Re-create the team (slack-coordinator, define-worker, executor) with existing channel/stakeholder context in their spawn prompts.
3. Continue from the interrupted phase. If `phase_state.waiting_for` is populated, resume polling from where it left off — check for responses that arrived while the process was down.

## Phase Flow

### Phase 0: Preflight (Lead alone — no team yet)

1. Ask the user via AskUserQuestion:
   - What is the existing Slack channel ID? (User must create the channel and ensure stakeholders are members before starting.)
   - Who are the stakeholders? (names, Slack @handles, roles/expertise)
   - Which stakeholders handle QA (if any)?
2. Generate a unique `run_id`.
3. Create the team — spawn all three teammates:
   - **slack-coordinator** (model: haiku): pass the full stakeholder roster (names, handles, roles, QA flags) and the state file path in the spawn prompt.
   - **define-worker**: pass the task description.
   - **executor**: pass initial context (will receive manifest path later).
4. Message slack-coordinator: "Post an intro message to channel [channel_id]. Create topic threads for initial stakeholder introductions. Report back with thread_ts values."
5. When slack-coordinator reports thread info, write state file.

### Phase 1: Define

1. Message define-worker: "Run /define for: [task description]\n\nTEAM_CONTEXT:\n  lead: <your-name>\n  coordinator: slack-coordinator\n  role: define"
2. When define-worker messages you with Q&A questions, route them to slack-coordinator for Slack posting. Relay coordinator's responses back to define-worker.
3. When define-worker requests a subagent (manifest-verifier), follow the Subagent Bridge Protocol.
4. When define-worker messages you with the manifest_path, update state file.

### Phase 2: Manifest Review

1. Message slack-coordinator: "Post the manifest at [manifest_path] to Slack for stakeholder review. Tag all stakeholders. Poll for owner approval."
2. Wait for slack-coordinator's report:
   - **Approved**: Update state, move to Phase 3.
   - **Feedback**: Message define-worker: "Revise manifest at [path] with this feedback: [feedback]". Then re-enter Phase 2.

### Phase 3: Execute

1. Message executor: "Run /do for manifest at [manifest_path]\n\nTEAM_CONTEXT:\n  lead: <your-name>\n  coordinator: slack-coordinator\n  role: execute"
2. When executor messages you with escalations, route them to slack-coordinator. Relay responses back.
3. When executor requests verification subagents, follow the Subagent Bridge Protocol.
4. When executor completes, update state file.

### Phase 4: PR

1. Message executor: "Create a PR for the changes. Report back with the PR URL."
2. When executor reports PR URL, update state.
3. Message slack-coordinator: "Post PR [url] to Slack for review. Tag reviewers. Poll for approval."
4. Wait for slack-coordinator's report:
   - **Approved**: Move to Phase 5.
   - **Review comments**: Message executor: "Fix these review comments: [comments]". Max 3 fix attempts, then message slack-coordinator to escalate to owner.

### Phase 5: QA (optional — skip if no QA stakeholders)

QA is performed by human testers through Slack. All communication routes through you (lead).

1. Message slack-coordinator: "Post QA request. Ask QA stakeholders to test and report issues."
2. When slack-coordinator reports QA issues:
   - Message define-worker: "Evaluate these QA issues against the manifest: [issues]. Which ACs are violated? What needs fixing?"
   - When define-worker responds with evaluation, message executor: "Fix these validated issues: [fix instructions with AC refs]"
   - When executor reports fix complete, message slack-coordinator to update Slack.
   - Repeat until QA sign-off or max 3 fix rounds then escalate.
3. Update state file.

### Phase 6: Done

1. Message slack-coordinator: "Post completion summary to Slack: task description, PR URL, key decisions."
2. Write final state file with `phase: "done"`.
3. Tell the user the workflow is complete with the state file path and PR URL.

## Teammate Crash Handling

Monitor teammate status. If a teammate fails or crashes:
1. Re-spawn it once with the same task and context.
2. If it fails again, write state file and inform the user. They can resume later with `--resume`.

Do not retry infinitely.
