# Slack-Collab Full Specification

*Living spec for the manifest-dev-collab plugin. Run `/do .manifest/slack-collab-full-spec.md` to verify all criteria and fix regressions.*

## 1. Intent & Context

- **Goal:** Collaborative define/do workflow via Slack using Agent Teams. Lead orchestrator spawns specialized teammates (slack-coordinator, define-worker, executor) that coordinate via mailbox messaging for stakeholder Q&A, manifest review, PR review, and QA sign-off.

- **Mental Model:**
  - **Lead** = the `/slack-collab` skill session. Pure orchestrator. Asks preflight questions, creates team, manages phases, writes state file, acts as subagent bridge (spawns subagents on behalf of workers). **NEVER uses Slack MCP tools directly** — all Slack interaction routes through the slack-coordinator. Terminates all teammates via shutdown_request in Phase 6.
  - **slack-coordinator** (haiku model, spawned via `subagent_type: manifest-dev-collab:slack-coordinator`) = dedicated Slack I/O teammate. Posts messages, polls threads, routes stakeholder answers to lead. Continuous polling at 60-second intervals — starts after first thread, runs until shutdown_request. Each item (question, review, phase transition) gets its own parent message in the main channel (no mega-thread). Tags only relevant stakeholders per thread to minimize notifications (stakeholders have channel muted).
  - **define-worker** (spawned via `subagent_type: manifest-dev-collab:define-worker`, model omitted = inherits parent) = runs `/define` with TEAM_CONTEXT. Messages lead for all communication (stakeholder Q&A routed through lead → coordinator). Requests verification subagent launches from lead. Persists as manifest authority for QA evaluation.
  - **executor** (spawned via `subagent_type: manifest-dev-collab:executor`, model omitted = inherits parent) = runs `/do` with TEAM_CONTEXT. Messages lead for all communication (escalations routed through lead → coordinator). Requests verification subagent launches from lead. Creates PR. Fixes QA issues routed through lead. Does NOT run /verify or spawn verification agents locally.
  - **Hub-and-spoke** = all teammate communication flows through the lead. No direct teammate↔teammate messaging. The lead is the communication hub.
  - **Subagent bridge** = workers needing subagent capabilities (manifest-verifier, criteria-checkers) request launches from lead. Subagents send results directly to the requesting worker via SendMessage (if feasible) or write to `/tmp/subagent-result-{id}.md` and lead tells worker the file path (fallback).
  - **TEAM_CONTEXT** = behavior switch. Tells `/define` and `/do` to message the lead instead of using AskUserQuestion. Format includes `lead` name, `coordinator` name, and `role`.
  - **State file** = crash/resume recovery. JSON at `/tmp/collab-state-{run_id}.json`. Written by lead (single writer) after phase transitions and thread updates. Supports mid-phase resume.
  - **Active polling** = coordinator polls Slack threads every 60 seconds continuously from first thread until shutdown_request. 24-hour timeout before escalating unanswered questions to owner. No Slack notification API available.
  - **Channel** = user-provided. No channel creation or invite available in Slack MCP. User must create channel and ensure stakeholders are members before starting.

- **TEAM_CONTEXT Format:**
  ```
  TEAM_CONTEXT:
    lead: <lead-name>
    coordinator: slack-coordinator
    role: define|execute
  ```

## 2. Approach

```
/slack-collab "build auth system"
│
├─ PHASE 0: PREFLIGHT (Lead alone, no team yet)
│  ├─ Ask user via AskUserQuestion:
│  │   - Existing Slack channel ID (no creation)
│  │   - Stakeholders (names, Slack handles, roles)
│  │   - QA needs
│  ├─ Create team via subagent_type: slack-coord (haiku), define-worker, executor
│  ├─ Message slack-coord: "Post intro to channel, create
│  │   topic threads for initial Q&A"
│  ├─ Coord sends thread_ts values to lead
│  └─ Lead writes state file
│
├─ PHASE 1: DEFINE
│  ├─ Lead messages define-worker: "Run /define for [task]
│  │   TEAM_CONTEXT: lead: <name>, coordinator: slack-coordinator, role: define"
│  ├─ define-worker runs /define, messages lead for Q&A
│  ├─ Lead routes Q&A to coordinator → Slack → poll → relay back
│  ├─ define-worker requests manifest-verifier → lead spawns subagent
│  ├─ Subagent sends results directly to define-worker (or file fallback)
│  ├─ define-worker completes, messages lead: manifest_path
│  └─ Lead writes state file
│
├─ PHASE 2: MANIFEST REVIEW
│  ├─ Lead messages coord: "Post manifest for review, poll for approval"
│  ├─ If feedback: lead → define-worker revises → re-enter Phase 2
│  ├─ If approved: proceed
│  └─ Lead writes state file
│
├─ PHASE 3: EXECUTE
│  ├─ Lead messages executor: "Run /do for [manifest_path]
│  │   TEAM_CONTEXT: lead: <name>, coordinator: slack-coordinator, role: execute"
│  ├─ executor runs /do, messages lead for escalations
│  ├─ executor requests verification → lead spawns subagents
│  ├─ Subagents send results directly to executor (or file fallback)
│  ├─ executor completes, messages lead
│  └─ Lead writes state file
│
├─ PHASE 4: PR
│  ├─ Lead messages executor: "Create PR"
│  ├─ Executor creates PR, messages lead with URL
│  ├─ Lead messages coord: "Post PR for review, poll approval"
│  ├─ If review comments: lead → executor fixes (max 3), then escalate
│  └─ Lead writes state file
│
├─ PHASE 5: QA (optional, if QA stakeholders exist)
│  ├─ Lead messages coord: "Post QA request"
│  ├─ QA tester (human) posts issues in Slack thread
│  ├─ Coord picks up → lead → define-worker evaluates against manifest
│  ├─ Lead → executor fixes validated issues
│  ├─ Repeat until QA sign-off or max 3 fix rounds then escalate
│  └─ Lead writes state file
│
└─ PHASE 6: DONE
   ├─ Lead messages coord: "Post completion summary" (tag all)
   ├─ Lead sends shutdown_request to all 3 teammates
   ├─ Lead waits for shutdown confirmations
   └─ Lead writes final state, tells user workflow complete
```

- **Risk Areas:**
  - [R-1] Subagent SendMessage feasibility — subagents spawned with team_name may not have SendMessage access | Detect: test on first launch; fall back to file-based handoff
  - [R-2] Mid-phase resume after long pause — /tmp files may not survive system restarts | Detect: document as known limitation
  - [R-3] Hub-and-spoke bottleneck — QA feedback loop has many hops | Detect: if >5 messages per QA issue, consider relaxing for future iteration
  - [R-4] State file write contention — mitigated by single-writer (lead) pattern
  - [R-5] Context overflow in lead from subagent relay — mitigated by subagent-direct-messaging + memento log
  - [R-6] Agent Teams experimental instability — teammate creation or messaging may fail | Detect: visible stall; lead re-spawns once then stops
  - [R-7] Teammates don't persist across phases — define-worker may be cleaned up before QA | Detect: lead monitors; re-spawns with manifest context if needed

- **Trade-offs:**
  - [T-1] Hub-and-spoke vs mesh → Prefer hub-and-spoke: lead visibility, reduced teammate confusion
  - [T-2] Subagent-direct-messaging vs lead-relay → Prefer direct: saves lead context; file fallback if infeasible
  - [T-3] Topic-based vs per-stakeholder threads → Prefer topic-based: groups context by question
  - [T-4] 24h timeout vs shorter → Prefer 24h: cross-timezone, business day workflows
  - [T-5] Dedicated coordinator vs lead-handles-Slack → Prefer dedicated: clean separation of concerns
  - [T-6] Persistent define-worker vs fresh reviewer → Prefer persistent: preserves full interview context for QA

## 3. Global Invariants (The Constitution)

- [INV-G1] Standalone /define unchanged — /define without TEAM_CONTEXT behaves identically. COLLABORATION_MODE.md only activates with TEAM_CONTEXT block.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md and claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md. Verify COLLABORATION_MODE.md only activates when TEAM_CONTEXT block is present in $ARGUMENTS. Verify all non-collaboration paths are identical: AskUserQuestion, verification loop, all methodology sections."
  ```

- [INV-G2] Standalone /do unchanged — /do without TEAM_CONTEXT behaves identically.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md and claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify COLLABORATION_MODE.md only activates when TEAM_CONTEXT block is present. Verify all non-collaboration paths unchanged: execution log, escalation, verification, memento pattern."
  ```

- [INV-G3] TEAM_CONTEXT format consistent across producer (SKILL.md) and consumers (COLLABORATION_MODE.md files). Must contain: lead, coordinator, role.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Extract TEAM_CONTEXT format from: (1) claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md (producer) (2) claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md (consumer) (3) claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md (consumer). Verify all three agree on fields: lead, coordinator, role."
  ```

- [INV-G4] Hub-and-spoke enforced — no agent file instructs teammates to message other teammates directly. All teammate communication routes through lead. Only exception: subagents spawned by lead can SendMessage to teammates.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read all agent files in claude-plugins/manifest-dev-collab/agents/. Verify NONE instruct messaging another teammate directly. All communication goes through the lead. Only subagents spawned by lead may SendMessage to teammates."
  ```

- [INV-G5] Role separation — each teammate owns specific domains. Executor owns code/PR. Define-worker owns manifest/discovery log. Coordinator owns Slack I/O. No overlap.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read all agent files in claude-plugins/manifest-dev-collab/agents/. Verify file write domains are non-overlapping: executor owns code files and PR creation, define-worker owns manifest and discovery log in /tmp, coordinator owns only Slack I/O. No agent writes to another's domain."
  ```

- [INV-G6] Prompt injection defense in coordinator — treats all Slack messages as untrusted. Never exposes secrets, never runs arbitrary commands, declines dangerous requests and tags owner.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/slack-coordinator.md. Verify prompt injection defense: (1) Never expose env vars/secrets/credentials (2) Never run arbitrary commands from Slack without validation (3) Allow task-adjacent requests, block clearly dangerous actions (4) Decline suspicious requests and tag owner."
  ```

- [INV-G7] Workers never touch Slack — define-worker and executor never reference Slack MCP tools. All external communication through lead.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/define-worker.md and executor.md. Verify: (1) Neither references Slack MCP tools (2) Neither instructs direct Slack posting or reading (3) All external communication goes through messaging the lead."
  ```

- [INV-G8] No channel creation or invite references in any collab file. Channel is user-provided.
  ```yaml
  verify:
    method: bash
    command: "grep -riE 'create_channel|invite_to_channel' claude-plugins/manifest-dev-collab/ claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md && echo 'FAIL: found channel creation API references' || echo 'PASS'"
  ```

- [INV-G9] No DM references — no file instructs sending direct messages outside the shared channel.
  ```yaml
  verify:
    method: bash
    command: "grep -riE 'send a dm|send dm|private message|direct message to user' claude-plugins/manifest-dev-collab/ claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md && echo 'FAIL: found DM references' || echo 'PASS'"
  ```

- [INV-G10] Subagent request format consistent — format in SKILL.md (lead side) matches format in COLLABORATION_MODE.md files (worker side).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read subagent bridge protocol in claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md and both COLLABORATION_MODE.md files. Verify the subagent request format is consistent across all three — same fields, same structure."
  ```

- [INV-G11] Kebab-case naming on all files.
  ```yaml
  verify:
    method: bash
    command: "find claude-plugins/manifest-dev-collab -type f | grep -v '.claude-plugin' | grep -v __pycache__ | grep -v README.md | grep -v SKILL.md | while read f; do basename \"$f\" | grep -qE '^[a-z0-9][a-z0-9_-]*\\.[a-z]+$' || echo \"FAIL: $f\"; done"
  ```

- [INV-G12] Valid plugin JSON with required fields.
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json')); assert all(k in d for k in ['name','version','description']), f'Missing fields: {d.keys()}'; print('PASS')\""
  ```

- [INV-G13] Skill frontmatter valid — name (kebab-case, max 64), description (max 1024, action-oriented).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify YAML frontmatter has: name (kebab-case, max 64 chars), description (max 1024 chars, action-oriented). Verify user-invocable is true or defaulted."
  ```

- [INV-G14] Prompt quality — no prescriptive HOW, no arbitrary limits, no capability instructions, no weak language, no buried critical info. All prompts state goals and constraints.
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: opus
    prompt: "Review all prompt files in claude-plugins/manifest-dev-collab/ (SKILL.md and all agents) and both COLLABORATION_MODE.md files for anti-patterns: prescriptive HOW, arbitrary limits, capability instructions, weak language, buried critical info, over-engineering, contradictions, ambiguity. Also check: domain context accuracy, complexity fit, description quality, guardrail calibration."
  ```

- [INV-G15] Documentation accurate — READMEs reflect current architecture.
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: opus
    prompt: "Compare README.md files (root, claude-plugins/, manifest-dev-collab/, manifest-dev/) with actual agent and skill files. Verify READMEs accurately describe: user provides channel, hub-and-spoke communication, subagent bridge, 60s polling, 24h timeout, topic-based threads, haiku coordinator. No stale references to Python orchestrator, COLLAB_CONTEXT, session-resume, channel creation, or DMs."
  ```

- [INV-G16] CLAUDE.md adherence — kebab-case, version bumps, README sync, frontmatter conventions.
  ```yaml
  verify:
    method: subagent
    agent: claude-md-adherence-reviewer
    model: opus
    prompt: "Review all files in claude-plugins/manifest-dev-collab/ and the two COLLABORATION_MODE.md files against project CLAUDE.md. Check: kebab-case naming, plugin versions consistent, README sync checklist, skill/agent frontmatter format."
  ```

- [INV-G17] Python orchestrator fully removed — no orphan files.
  ```yaml
  verify:
    method: bash
    command: "test ! -f claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py && test ! -d tests/collab && echo PASS || echo FAIL"
  ```

- [INV-G18] No stale V1/V2 references in any file.
  ```yaml
  verify:
    method: bash
    command: "if grep -rli 'COLLAB_CONTEXT\\|slack-collab-orchestrator\\.py\\|session-resume\\|session_resume' claude-plugins/manifest-dev-collab/ claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md 2>/dev/null; then echo FAIL; else echo PASS; fi"
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Use `/prompt-engineering` skill for all prompt changes — skill/agent files are LLM prompts.
- [PG-2] Right-sized changes — each update addresses only what's specified. No scope creep.
- [PG-3] Agent definitions should be self-contained — each has everything the teammate needs. Don't assume it reads the skill.
- [PG-4] TEAM_CONTEXT must stay minimal. New fields require manifest amendment.
- [PG-5] State file schema should be flat and simple — no nested schemas beyond stakeholder list and phase_state.
- [PG-6] State file single-writer — lead owns all writes. Coordinator sends thread updates via message; lead writes them.
- [PG-7] Launch verification subagents in parallel — use `run_in_background`.
- [PG-8] Test subagent SendMessage feasibility on first launch. If fails, switch to file-based handoff for all subsequent.
- [PG-9] Guard against scope creep — no Slack notifications beyond Q&A, reviews, escalations, completion. No progress posts.
- [PG-10] Lead memento pattern: re-read state file after each phase transition. Log subagent interactions to `/tmp/collab-subagent-log-{run_id}.md`.
- [PG-11] Document load-bearing assumptions in each changed file.

## 5. Known Assumptions

- [ASM-1] `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set | Impact if wrong: team creation fails
- [ASM-2] /tmp files persist within session | Impact if wrong: resume fails
- [ASM-3] Teammates inherit Slack MCP from project context | Impact if wrong: coordinator can't use Slack
- [ASM-4] /define and /do invoked via Skill tool inside teammates work normally | Impact if wrong: workers follow methodology from agent prompt instead
- [ASM-5] One lead can manage 3 teammates simultaneously | Impact if wrong: reduce to 2 (merge roles)
- [ASM-6] Agent frontmatter tool declarations not present (pre-existing gap, out of scope) | Impact if wrong: follow-up task

## 6. Deliverables (The Work)

### Deliverable 1: Lead Orchestrator — SKILL.md
*File: `claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md`*

- [AC-1.1] Phase 0 asks user for existing Slack channel ID via AskUserQuestion (no channel creation). Documents that stakeholders must already be in the channel.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify Phase 0 asks user for existing channel ID (not creating a channel). Verify it documents stakeholders must already be in channel."
  ```

- [AC-1.2] Phase 0 gathers stakeholders (names, handles, roles, QA flags) via AskUserQuestion. Passes full roster to coordinator at spawn time.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify preflight gathers stakeholder info and passes the full roster to slack-coordinator in its spawn prompt as a routing table."
  ```

- [AC-1.3] Creates team with 3 teammates via `subagent_type` identifiers (manifest-dev-collab:slack-coordinator, manifest-dev-collab:define-worker, manifest-dev-collab:executor). Coordinator spawned with model: haiku. Define-worker and executor omit model (inherits parent).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify team creation spawns 3 teammates via subagent_type identifiers (manifest-dev-collab:*). Verify slack-coordinator specifies model: haiku. Verify define-worker and executor omit model (inherits parent). No 'agents/*.md' file path references."
  ```

- [AC-1.4] Hub-and-spoke communication model explicitly stated. Teammates only message lead.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify it explicitly states hub-and-spoke: teammates only communicate with lead. No direct teammate-to-teammate messaging."
  ```

- [AC-1.5] Subagent bridge protocol documented with concrete request format including: what subagent to run, prompt, who receives results, context files.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify subagent bridge protocol: worker request format, lead spawn mechanism, result delivery (SendMessage primary, file-based fallback with naming convention /tmp/subagent-result-{run_id}-{request_id}.md), how lead logs interactions."
  ```

- [AC-1.6] Subagent SendMessage feasibility test: lead tests on first subagent launch, falls back to file-based if fails.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify it instructs testing subagent SendMessage feasibility on first launch and falling back to file-based handoff if it fails."
  ```

- [AC-1.7] Phase flow: preflight → define → manifest review → execute → PR → QA (optional) → done. Each phase described with lead's specific actions.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify 7 phases in order: (0) Preflight (1) Define (2) Manifest Review (3) Execute (4) PR (5) QA optional (6) Done. Verify lead's actions per phase match the architecture."
  ```

- [AC-1.8] Phase 5 (QA) routes through lead: coordinator → lead → define-worker evaluates → lead → executor fixes. No direct define-worker↔executor messaging.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md Phase 5. Verify QA flow: coordinator → lead → define-worker → lead → executor. No direct define-worker-to-executor messaging."
  ```

- [AC-1.9] State file written after every phase transition. Schema includes: run_id, phase, channel_id, stakeholders, threads, manifest_path, pr_url, phase_state (active threads, polling status for mid-phase resume).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify state file written after each phase transition with schema including phase_state for mid-phase resume. Lead is single writer."
  ```

- [AC-1.10] Resume capability: `--resume <state-file-path>` reads state, re-creates team, continues from interrupted phase. Supports mid-phase resume for polling states.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify resume reads state file, re-creates team with existing context, continues from interrupted phase including mid-phase polling states."
  ```

- [AC-1.11] Teammate crash handling: re-spawn once with same task. Second failure: write state, stop.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify: on teammate failure, re-spawn once. On second failure, write state and inform user. No infinite retry."
  ```

- [AC-1.12] Lead memento: subagent interaction log at `/tmp/collab-subagent-log-{run_id}.md`. Re-read state file before phase transitions.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify lead memento pattern: subagent interaction log file, re-read state file before phase transitions."
  ```

- [AC-1.13] TEAM_CONTEXT format includes `lead` field.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify TEAM_CONTEXT format includes lead field with lead's name, coordinator field, and role field."
  ```

- [AC-1.14] State file write ownership documented: lead is single writer. Coordinator sends thread updates via message.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md. Verify state file is lead-owned for writes. Coordinator sends thread tracking updates via message to lead."
  ```

- [AC-1.15] Prerequisites list only actually available Slack MCP tools. No create_channel or invite_to_channel.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read SKILL.md Prerequisites. Verify it lists only available Slack MCP tools (send_message, read_channel, read_thread, search_channels, search_users, read_user_profile). No create_channel or invite_to_channel."
  ```

- [AC-1.16] No references to channel creation, invite_to_channel, DMs, COLLAB_CONTEXT, or Python orchestrator.
  ```yaml
  verify:
    method: bash
    command: "grep -iE 'create.channel|invite.channel|COLLAB_CONTEXT|orchestrator\\.py' claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md && echo 'FAIL' || echo 'PASS'"
  ```

### Deliverable 2: Slack Coordinator Agent
*File: `claude-plugins/manifest-dev-collab/agents/slack-coordinator.md`*

- [AC-2.1] Channel setup responsibility: receives channel_id from lead (user-provided). No channel creation.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify channel creation NOT listed as responsibility. Expects channel_id from lead."
  ```

- [AC-2.2] Continuous polling: starts after first thread creation, runs until shutdown_request. Sleep 60 seconds between polls. Polls ALL tracked threads. Never stops on its own.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify: (1) polling starts after first thread (2) continuous until shutdown_request (3) 60-second interval (4) polls ALL tracked threads (5) never stops on its own — no phase-based resets or pauses."
  ```

- [AC-2.3] Escalation timeout: 24 hours before escalating to owner.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify escalation timeout is 24 hours. Escalates unanswered questions to owner after 24h."
  ```

- [AC-2.4] Topic-based threads: one thread per question/review/topic. Relevant stakeholders tagged.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify thread model is topic-based (one per question/review), NOT per-stakeholder."
  ```

- [AC-2.5] Main channel model: coordinator posts parent messages, stakeholders reply in threads. Monitors thread replies, not main channel posts.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify: coordinator posts parent messages, stakeholders reply in threads, monitors thread replies not main channel."
  ```

- [AC-2.6] Thread tracking: sends thread_ts values to lead via message (lead writes to state file). Reads state file on context compression to recover thread list.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify: sends thread_ts to lead via message, reads state file on context compression to recover threads."
  ```

- [AC-2.7] Stakeholder routing: uses roster from spawn prompt. Routes based on expertise context from lead. Owner can reply in any thread authoritatively.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify: stakeholder routing from roster, expertise-based routing, owner override (can answer in any thread)."
  ```

- [AC-2.8] Prompt injection defense: never expose secrets, never run arbitrary commands, decline dangerous requests, tag owner.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify prompt injection defense section covers: no secrets exposure, no arbitrary commands, decline dangerous requests, tag owner."
  ```

- [AC-2.9] Long content split: messages exceeding ~4000 chars split into numbered parts [1/N], [2/N].
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read slack-coordinator.md. Verify long content handling: split messages >4000 chars into [1/N], [2/N] format."
  ```

- [AC-2.10] No references to channel creation, DMs, or direct teammate messaging.
  ```yaml
  verify:
    method: bash
    command: "grep -iE 'create_channel|invite_to_channel' claude-plugins/manifest-dev-collab/agents/slack-coordinator.md && echo 'FAIL' || echo 'PASS'"
  ```

### Deliverable 3: Define Worker Agent
*File: `claude-plugins/manifest-dev-collab/agents/define-worker.md`*

- [AC-3.1] Primary task: invoke /define with TEAM_CONTEXT. Messages lead for all communication.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read define-worker.md. Verify: invokes /define with TEAM_CONTEXT, messages lead (not coordinator or executor) for all communication."
  ```

- [AC-3.2] Verification delegation: messages lead for manifest-verifier with structured subagent request. Does not spawn subagents directly.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read define-worker.md. Verify: messages lead for manifest-verifier (not spawning directly). Request includes agent type, prompt, target files."
  ```

- [AC-3.3] Receives verification results from subagents (SendMessage) or from lead (file path fallback).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read define-worker.md. Verify it handles receiving results via SendMessage from subagent OR via lead message with file path."
  ```

- [AC-3.4] Persists after /define as manifest authority. Evaluates QA issues against ACs.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read define-worker.md. Verify: stays alive after /define, evaluates QA issues against manifest ACs, identifies which ACs violated, provides fix guidance."
  ```

- [AC-3.5] Never touches Slack. No references to Slack MCP tools or direct teammate messaging.
  ```yaml
  verify:
    method: bash
    command: "grep -i 'message.*executor\\|message.*coordinator\\|send.*executor\\|send.*coordinator\\|slack_' claude-plugins/manifest-dev-collab/agents/define-worker.md | grep -vi 'NOT\\|never\\|Do not' && echo 'FAIL' || echo 'PASS'"
  ```

### Deliverable 4: Executor Agent
*File: `claude-plugins/manifest-dev-collab/agents/executor.md`*

- [AC-4.1] Primary task: invoke /do with TEAM_CONTEXT. Messages lead for all communication.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read executor.md. Verify: invokes /do with TEAM_CONTEXT, messages lead (not coordinator or define-worker) for all communication."
  ```

- [AC-4.2] Verification delegation: messages lead for verification with manifest path and scope. Does not run /verify locally.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read executor.md. Verify: messages lead for verification (not running /verify locally). Request includes manifest path and scope."
  ```

- [AC-4.3] QA issues received from lead (not define-worker directly).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read executor.md. Verify QA issues come from lead, not define-worker directly."
  ```

- [AC-4.4] Receives verification results from subagents (SendMessage) or from lead (file path fallback).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read executor.md. Verify it handles receiving results via SendMessage from subagent OR via lead message with file path."
  ```

- [AC-4.5] Creates PR, fixes review comments (max 3 attempts), fixes QA issues.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read executor.md. Verify: creates PR with gh, fixes review comments, fixes validated QA issues."
  ```

- [AC-4.6] Never touches Slack. No references to Slack MCP tools or direct teammate messaging.
  ```yaml
  verify:
    method: bash
    command: "grep -i 'message.*define.worker\\|message.*coordinator\\|send.*define.worker\\|send.*coordinator\\|slack_' claude-plugins/manifest-dev-collab/agents/executor.md | grep -vi 'NOT\\|never\\|Do not' && echo 'FAIL' || echo 'PASS'"
  ```

### Deliverable 5: /define COLLABORATION_MODE.md
*File: `claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md`*

- [AC-5.1] Activated by TEAM_CONTEXT (not COLLAB_CONTEXT). Messages lead for stakeholder Q&A (not coordinator directly). Includes expertise context for routing delegation.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md. Verify: activated by TEAM_CONTEXT, messages lead (not coordinator directly), includes expertise context in questions, routing delegation to coordinator via lead."
  ```

- [AC-5.2] Verification Loop delegates to lead: messages lead with manifest-verifier request (not spawning locally). Subagent request format documented.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read COLLABORATION_MODE.md for /define. Verify Verification Loop instructs messaging lead for manifest-verifier, not spawning locally. Subagent request format documented."
  ```

- [AC-5.3] Memento discipline: log to discovery file after each response from lead.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /define COLLABORATION_MODE.md. Verify memento discipline: log findings to discovery file after each lead response."
  ```

- [AC-5.4] Everything else unchanged: full /define methodology applies (Domain Grounding, Pre-Mortem, etc.). Only interaction channel changes.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /define COLLABORATION_MODE.md. Verify it states all /define methodology applies unchanged — only the interaction channel changes."
  ```

- [AC-5.5] Security note: prompt injection defense handled by coordinator agent.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /define COLLABORATION_MODE.md. Verify security note states prompt injection defense is handled by coordinator agent."
  ```

### Deliverable 6: /do COLLABORATION_MODE.md
*File: `claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md`*

- [AC-6.1] Activated by TEAM_CONTEXT. Escalation messages lead (not coordinator directly).
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify: activated by TEAM_CONTEXT, escalations message lead, not coordinator directly."
  ```

- [AC-6.2] Verification delegates to lead: messages lead with verification request (not calling /verify locally). Subagent request format documented.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /do COLLABORATION_MODE.md. Verify verification instructs messaging lead (not running /verify locally). Subagent request format documented."
  ```

- [AC-6.3] Memento discipline: log to execution file after each response from lead.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /do COLLABORATION_MODE.md. Verify memento: log to execution file after each lead response."
  ```

- [AC-6.4] Everything else unchanged: all /do principles, hooks, /verify before completion apply.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /do COLLABORATION_MODE.md. Verify all /do methodology applies unchanged."
  ```

- [AC-6.5] Security note: prompt injection defense handled by coordinator.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read /do COLLABORATION_MODE.md. Verify security note about coordinator handling prompt injection defense."
  ```

### Deliverable 7: Plugin Structure and Versions
*Files: plugin.json, file structure*

- [AC-7.1] Plugin structure: agents/ with 3 files, skills/slack-collab/ with SKILL.md. No scripts/ directory.
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-collab/agents/slack-coordinator.md && test -f claude-plugins/manifest-dev-collab/agents/define-worker.md && test -f claude-plugins/manifest-dev-collab/agents/executor.md && test -f claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md && test ! -d claude-plugins/manifest-dev-collab/scripts && echo PASS || echo FAIL"
  ```

- [AC-7.2] manifest-dev-collab plugin.json version > 1.0.0.
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v=json.load(open('claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json'))['version']; print('PASS' if v > '1.0.0' else 'FAIL: version should be > 1.0.0, got ' + v)\""
  ```

- [AC-7.3] manifest-dev plugin.json version > 0.62.0 (COLLABORATION_MODE.md changes).
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; v=json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; print('PASS' if v > '0.62.0' else 'FAIL: version should be > 0.62.0, got ' + v)\""
  ```

### Deliverable 8: Documentation
*Files: READMEs*

- [AC-8.1] Root README.md lists manifest-dev-collab plugin.
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-collab' README.md && echo PASS || echo FAIL"
  ```

- [AC-8.2] claude-plugins/README.md includes manifest-dev-collab in plugin table.
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-collab' claude-plugins/README.md && echo PASS || echo FAIL"
  ```

- [AC-8.3] manifest-dev-collab/README.md describes current architecture: team composition, hub-and-spoke, subagent bridge, user provides channel, 60s polling, 24h timeout, topic threads, haiku coordinator, resume, prerequisites.
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/README.md. Verify it covers: Agent Teams architecture, team composition (lead + 3 teammates), hub-and-spoke communication, subagent bridge protocol, user provides channel (no creation), 60s polling, 24h timeout, topic-based threads, haiku model for coordinator, resume capability, prerequisites. No Python orchestrator, COLLAB_CONTEXT, or channel creation references."
  ```

- [AC-8.4] manifest-dev/README.md mentions team collaboration mode.
  ```yaml
  verify:
    method: bash
    command: "grep -qi 'team.*collaborat\\|collaborat.*team\\|TEAM_CONTEXT' claude-plugins/manifest-dev/README.md && echo PASS || echo FAIL"
  ```

- [AC-8.5] No stale references in any README.
  ```yaml
  verify:
    method: bash
    command: "if grep -rli 'COLLAB_CONTEXT\\|slack-collab-orchestrator\\.py\\|session-resume\\|session_resume\\|create_channel\\|invite_to_channel' README.md claude-plugins/*/README.md 2>/dev/null; then echo FAIL; else echo PASS; fi"
  ```
