---
name: slack-collab
description: 'Orchestrate team collaboration on define/do workflows through Slack using Agent Teams. The skill acts as the team lead, spawning specialized teammates (slack-coordinator, define-worker, executor) that coordinate via mailbox messaging. Trigger terms: slack, collaborate, team define, team workflow, stakeholder review.'
---

# /slack-collab - Collaborative Define/Do via Slack (Agent Teams)

Orchestrate a full define → do → PR → review → QA → done workflow with your team through Slack. You are the **lead** — spawn teammates and coordinate phases.

`$ARGUMENTS` = task description (what to build/change), or `--resume <state-file-path>` to resume a crashed session.

If `$ARGUMENTS` is empty, ask what they want to build or change.

## Prerequisites

- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in Claude Code settings
- Slack MCP server configured with: create_channel, invite_to_channel, post_message, read_messages/read_thread_replies
- manifest-dev and manifest-dev-collab plugins installed

## Team Composition

You create **three teammates**, each defined by an agent file in `agents/` relative to this plugin:

| Teammate | Agent File | Role |
|----------|-----------|------|
| **slack-coordinator** | `agents/slack-coordinator.md` | ALL Slack I/O. Channel setup, message posting, polling, stakeholder routing. Prompt injection defense. |
| **define-worker** | `agents/define-worker.md` | Runs /define with TEAM_CONTEXT. Persists as manifest authority for QA evaluation. |
| **executor** | `agents/executor.md` | Runs /do with TEAM_CONTEXT. Creates PR. Fixes QA issues. |

## TEAM_CONTEXT Format

When messaging define-worker or executor to invoke /define or /do, append this to the task:

```
TEAM_CONTEXT:
  coordinator: slack-coordinator
  role: define|execute
```

This tells the skill to message the slack-coordinator teammate instead of using AskUserQuestion.

## State File

Write a JSON state file to `/tmp/collab-state-{run_id}.json` after **every** phase transition. This is crash recovery — re-read it after each phase to guard against context compression.

```json
{
  "run_id": "<unique-id>",
  "phase": "<current-phase>",
  "channel_id": "<slack-channel-id>",
  "channel_name": "<channel-name>",
  "owner_handle": "<@owner>",
  "stakeholders": [
    {"handle": "<@handle>", "name": "<name>", "role": "<role>", "is_qa": false}
  ],
  "threads": {"<@handle>": "<thread-ts>"},
  "manifest_path": null,
  "pr_url": null,
  "has_qa": false
}
```

## Resume

If `$ARGUMENTS` starts with `--resume`:
1. Read the state file at the provided path.
2. Re-create the team (slack-coordinator, define-worker, executor) with existing channel/stakeholder context in their spawn prompts.
3. Continue from the interrupted phase. Mid-phase progress from the crashed session is lost.

## Phase Flow

### Phase 0: Preflight (Lead alone — no team yet)

1. Ask the user via AskUserQuestion:
   - Who are the stakeholders? (names, Slack @handles, roles/expertise)
   - Which stakeholders handle QA (if any)?
2. Generate a unique `run_id`.
3. Create the team — spawn all three teammates:
   - **slack-coordinator**: pass the full stakeholder roster (names, handles, roles, QA flags) in the spawn prompt so it has its routing table.
   - **define-worker**: pass the task description.
   - **executor**: pass initial context (will receive manifest path later).
4. Message slack-coordinator: "Set up Slack channel `collab-{task-slug}-{YYYYMMDD}` with these stakeholders: [roster]. Create per-stakeholder Q&A threads. Report back with channel_id and thread info."
5. When slack-coordinator reports back, write state file with channel info.

### Phase 1: Define

1. Message define-worker: "Run /define for: [task description]\n\nTEAM_CONTEXT:\n  coordinator: slack-coordinator\n  role: define"
2. Wait for define-worker to complete. It will message you with the manifest_path.
3. Update state file: `phase: "manifest_review"`, `manifest_path: <path>`.

### Phase 2: Manifest Review

1. Message slack-coordinator: "Post the manifest at [manifest_path] to Slack for stakeholder review. Tag all stakeholders. Poll for owner approval."
2. Wait for slack-coordinator's report:
   - **Approved**: Update state, move to Phase 3.
   - **Feedback**: Message define-worker: "Revise manifest at [path] with this feedback: [feedback]". Then re-enter Phase 2.

### Phase 3: Execute

1. Message executor: "Run /do for manifest at [manifest_path]\n\nTEAM_CONTEXT:\n  coordinator: slack-coordinator\n  role: execute"
2. Wait for executor to complete.
3. Update state file: `phase: "pr"`.

### Phase 4: PR

1. Message executor: "Create a PR for the changes. Report back with the PR URL."
2. When executor reports back with PR URL, update state.
3. Message slack-coordinator: "Post PR [url] to Slack for review. Tag reviewers. Poll for approval."
4. Wait for slack-coordinator's report:
   - **Approved**: Move to Phase 5.
   - **Review comments**: Message executor: "Fix these review comments: [comments]". Max 3 fix attempts, then message slack-coordinator to escalate to owner.

### Phase 5: QA (optional — skip if no QA stakeholders)

**Note**: This phase uses direct teammate↔teammate messaging for the QA feedback loop (not lead-as-hub). This is intentional — the define-worker evaluates issues and routes validated fixes directly to the executor for efficiency.

1. Message slack-coordinator: "Post QA request. Ask QA stakeholders to test and report issues."
2. When slack-coordinator reports QA issues:
   - Message define-worker: "Evaluate these QA issues against the manifest: [issues]. Which ACs are violated? What needs fixing?"
   - define-worker evaluates and messages executor directly: "Fix these validated issues: [issues with AC refs]"
   - executor fixes, reports back to slack-coordinator
   - Repeat until QA sign-off or max 3 fix rounds then escalate
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
