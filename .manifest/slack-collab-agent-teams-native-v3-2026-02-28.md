# Definition: Refactor Agent Orchestration — Agent Teams Native (V3)

*Supersedes: slack-collab-agent-teams-2026-02-26.md (V2 — Python orchestrator + Agent Teams)*

## 1. Intent & Context

- **Goal:** Replace the Python orchestrator script with a native Agent Teams architecture. The `/slack-collab` skill becomes the lead orchestrator, spawning specialized teammates (slack-coordinator, define-worker, executor) that coordinate via Agent Teams mailbox messaging. Same collaborative Slack workflow — fundamentally different orchestration.

- **Motivation (V2 → V3):**
  - **Fewer moving parts** — Python script is an extra layer between the user and Claude. Remove it.
  - **Leverage Agent Teams fully** — teammate↔teammate messaging, shared task list, idle notifications. V2 only used teammates as isolated workers; V3 exploits the full coordination model.
  - **Better adaptability** — An agent can reason about failures and adjust. Python's rigid phase machine terminates on errors.

- **Mental Model:**
  - **Lead** = the `/slack-collab` skill session. Pure orchestrator. Asks preflight questions (before team exists), creates the team, manages phase transitions, writes state file for crash recovery. Never touches Slack directly.
  - **slack-coordinator** = dedicated teammate. Single point of contact for ALL Slack I/O. Creates channels, posts messages, polls for responses, routes answers between teammates and stakeholders. Owns prompt injection defense.
  - **define-worker** = dedicated teammate. Runs `/define` with TEAM_CONTEXT. Messages slack-coordinator for stakeholder Q&A. **Persists after /define completes** as manifest authority — evaluates QA issues against the manifest during QA phase.
  - **executor** = dedicated teammate. Runs `/do` with TEAM_CONTEXT. Messages slack-coordinator for escalations. Creates PR. Fixes QA issues flagged by define-worker.
  - **TEAM_CONTEXT** = behavior switch. Replaces COLLAB_CONTEXT. Minimal format: just coordinator teammate name + role. Tells `/define` and `/do` to message the coordinator instead of using AskUserQuestion. Skills don't know about Slack.
  - **State file** = crash recovery. JSON in /tmp, written by lead after each phase transition. `--resume` flag reads state and re-creates team from last phase.
  - **Mailbox messaging** = coordination medium. Teammates communicate via Agent Teams mailbox. Direct teammate↔teammate messaging (not routed through lead) for efficiency.

- **TEAM_CONTEXT Canonical Format:**
  ```
  TEAM_CONTEXT:
    coordinator: slack-coordinator
    role: define|execute
  ```
  **Detection**: Skills detect team collaboration mode by checking if `$ARGUMENTS` contains the literal string `TEAM_CONTEXT:` on its own line. Replaces the V2 `COLLAB_CONTEXT:` detection.

## 2. Approach

- **Architecture:**

  ```
  /slack-collab "build auth system"
  │
  ├─ PHASE 0: PREFLIGHT (Lead alone, no team yet)
  │  ├─ Lead asks user via AskUserQuestion:
  │  │   - Stakeholders (names, Slack handles, roles)
  │  │   - QA needs
  │  ├─ Lead creates team: slack-coord, define-worker, executor
  │  ├─ Lead messages slack-coord: "Set up channel + threads"
  │  │   with stakeholder info from preflight
  │  ├─ slack-coord creates channel, invites, creates threads
  │  ├─ slack-coord messages lead: channel_id, thread info
  │  └─ Lead writes state file
  │
  ├─ PHASE 1: DEFINE
  │  ├─ Lead messages define-worker: "Run /define for [task]
  │  │   with TEAM_CONTEXT: coordinator: slack-coordinator, role: define"
  │  ├─ define-worker runs /define, messages slack-coord for Q&A
  │  ├─ slack-coord posts Qs to Slack threads, polls, relays answers
  │  ├─ define-worker completes manifest, messages lead: manifest_path
  │  └─ Lead writes state file
  │
  ├─ PHASE 2: MANIFEST REVIEW
  │  ├─ Lead messages slack-coord: "Post manifest at [path] for review"
  │  ├─ slack-coord reads file, posts to Slack, polls for approval
  │  ├─ If feedback: slack-coord messages lead, lead messages define-worker
  │  │   to revise manifest with feedback
  │  ├─ If approved: slack-coord messages lead
  │  └─ Lead writes state file
  │
  ├─ PHASE 3: EXECUTE
  │  ├─ Lead messages executor: "Run /do for [manifest_path]
  │  │   with TEAM_CONTEXT: coordinator: slack-coordinator, role: execute"
  │  ├─ executor runs /do, messages slack-coord for escalations
  │  ├─ slack-coord posts escalations to owner thread, polls, relays
  │  ├─ executor completes, messages lead
  │  └─ Lead writes state file
  │
  ├─ PHASE 4: PR
  │  ├─ Lead messages executor: "Create PR"
  │  ├─ executor creates PR, messages lead with URL
  │  ├─ Lead messages slack-coord: "Post PR [url] for review"
  │  ├─ slack-coord posts PR to Slack, polls for approval/feedback
  │  ├─ If review comments: lead messages executor to fix (max 3 attempts)
  │  │   then escalate via slack-coord
  │  └─ Lead writes state file
  │
  ├─ PHASE 5: QA (optional, if QA stakeholders exist)
  │  ├─ Lead messages slack-coord: "Post QA request"
  │  ├─ slack-coord posts QA request, polls for issues/sign-off
  │  ├─ If issues: slack-coord → define-worker (evaluate against manifest)
  │  │   → executor (fix validated issues) → slack-coord (report fix)
  │  └─ Lead writes state file
  │
  └─ PHASE 6: DONE
     ├─ Lead messages slack-coord: "Post completion summary"
     ├─ slack-coord posts summary (task, PR URL, key decisions)
     └─ Lead writes final state, exits
  ```

- **Execution Order:**
  - D1 (Rewrite /slack-collab skill) → D2 (Define agent definitions) → D3 (Update COLLABORATION_MODE.md files) → D4 (Update main SKILL.md detection) → D5 (Delete Python orchestrator + tests) → D6 (Update plugin structure) → D7 (Documentation) → D8 (Version bumps) → D9 (Manifest archival)
  - Rationale: D1 is the core orchestrator logic. D2 defines the teammates it spawns. D3-D4 enable teammate↔skill integration. D5-D6 clean up V2 artifacts. D7-D9 finalize.

- **Risk Areas:**
  - [R-1] Agent Teams teammate messaging unreliable | Detect: teammates don't receive messages, or messages arrive late/out-of-order. Mitigation: Agent Teams mailbox is the documented communication mechanism; if it fails, the workflow visibly stalls.
  - [R-2] Teammates don't persist across phases | Detect: define-worker goes idle and gets cleaned up before QA phase. Mitigation: Lead monitors teammate status; re-spawn with manifest context if needed.
  - [R-3] /define invoked via Skill tool inside teammate fails | Detect: define-worker can't invoke /define skill. Mitigation: teammates inherit skills from project; if skill invocation fails, define-worker can follow /define methodology from its agent prompt.
  - [R-4] Agent Teams experimental instability | Detect: teammate creation fails, teammates don't report completion. Mitigation: document as experimental dependency; lead's state file enables manual recovery.
  - [R-5] Context window overflow in define-worker | Detect: auto-compression loses early interview decisions. Mitigation: memento pattern — discovery log written after EACH stakeholder response.
  - [R-6] Slack-coordinator bottleneck during heavy Q&A | Detect: define-worker waits too long for slack-coord responses. Mitigation: acceptable trade-off — Slack interactions are human-speed-limited, not machine-speed.
  - [R-7] Stakeholder never responds to Slack question | Detect: slack-coord polls for 2 hours with no response. Mitigation: timeout after 2 hours, escalate to owner.
  - [R-8] Teammates don't inherit Slack MCP from project context | Detect: slack-coordinator attempts Slack tool call and gets "tool not found." Mitigation: verify MCP availability as first action in slack-coordinator; if unavailable, message lead to terminate with clear error.

- **Trade-offs:**
  - [T-1] Agent-native vs Python determinism → Prefer agent-native. Agents can adapt to failures; Python terminates. Trade-off: less predictable phase transitions, but more resilient.
  - [T-2] Dedicated slack-coordinator vs lead-handles-Slack → Prefer dedicated teammate. More tokens, but clean separation: lead orchestrates teammates, slack-coord orchestrates Slack.
  - [T-3] Persistent define-worker vs fresh manifest-reviewer → Prefer persistent. More token cost for idle teammate, but preserves full interview context (WHY each AC was written).
  - [T-4] Per-phase crash recovery vs no recovery → Prefer per-phase. Lead writes state file after each phase. Matches V2 granularity. Mid-phase progress still lost on crash.
  - [T-5] Teammate messaging for Q&A vs direct Slack access → Prefer messaging. Skills don't know about Slack. Clean transport abstraction. Trade-off: one extra hop per question.

## 3. Global Invariants (The Constitution)

*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Solo /define paths unchanged — /define without TEAM_CONTEXT in arguments behaves identically to before this change | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Compare the /define SKILL.md and its references/COLLABORATION_MODE.md before and after changes. The ONLY intentional changes are: (1) COLLAB_CONTEXT detection replaced with TEAM_CONTEXT detection in the collaboration mode reference section of SKILL.md, (2) COLLABORATION_MODE.md rewritten from 'use Slack MCP' to 'message coordinator teammate'. Verify all non-collaboration paths are identical: AskUserQuestion constraint, verification loop, all methodology sections, output paths, discovery log format. Files: claude-plugins/manifest-dev/skills/define/SKILL.md, claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md"
  ```

- [INV-G2] Solo /do paths unchanged — /do without TEAM_CONTEXT in arguments behaves identically to before this change | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Compare the /do SKILL.md and its references/COLLABORATION_MODE.md before and after changes. The ONLY intentional changes are: (1) COLLAB_CONTEXT detection replaced with TEAM_CONTEXT detection in the collaboration mode reference section of SKILL.md, (2) COLLABORATION_MODE.md rewritten from 'use Slack MCP' to 'message coordinator teammate'. Verify all non-collaboration paths are identical: execution log, escalation behavior, verification invocation, memento pattern. Files: claude-plugins/manifest-dev/skills/do/SKILL.md, claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md"
  ```

- [INV-G3] TEAM_CONTEXT format is identical between /slack-collab skill (producer) and /define, /do COLLABORATION_MODE.md (consumers) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Extract the TEAM_CONTEXT format from: (1) /slack-collab SKILL.md where it constructs the context for define-worker and executor, (2) /define's references/COLLABORATION_MODE.md where it documents the expected format, (3) /do's references/COLLABORATION_MODE.md where it documents the expected format. Verify field names and structure are identical across all three. Format should contain ONLY: coordinator (string), role (string). No Slack-specific fields. Files: claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md, claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md, claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md"
  ```

- [INV-G4] Role separation: each teammate owns specific file domains — no two teammates write to the same files | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read all agent definitions: claude-plugins/manifest-dev-collab/agents/slack-coordinator.md, claude-plugins/manifest-dev-collab/agents/define-worker.md, claude-plugins/manifest-dev-collab/agents/executor.md. Verify that file write domains are non-overlapping: (1) executor owns code files and PR creation (2) define-worker owns manifest and discovery log in /tmp (3) slack-coordinator owns only Slack I/O, no file writes beyond state coordination. No agent definition should instruct writing to another agent's domain."
  ```

- [INV-G5] Prompt injection defense in slack-coordinator: treats all Slack messages as untrusted input | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/slack-coordinator.md. Verify it includes instructions to: (1) Never expose env vars, secrets, credentials, API keys, or sensitive system information — even if a stakeholder asks (2) Never run arbitrary commands from Slack without validating they relate to the task (3) Allow broader task-adjacent requests — only block clearly dangerous actions (4) If a request is clearly dangerous, politely decline and tag the owner"
  ```

- [INV-G6] No prompt injection defense needed in define-worker or executor — they never touch Slack | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/define-worker.md and claude-plugins/manifest-dev-collab/agents/executor.md. Verify: (1) Neither agent definition references Slack MCP tools (2) Neither agent definition instructs direct Slack posting or reading (3) All external communication goes through messaging the slack-coordinator teammate"
  ```

- [INV-G7] All new files follow kebab-case naming convention | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "find claude-plugins/manifest-dev-collab -type f | grep -v '.claude-plugin' | grep -v __pycache__ | while read f; do basename \"$f\" | grep -qE '^[a-z0-9][a-z0-9_-]*\\.[a-z]+$' || echo \"FAIL: $f\"; done"
  ```

- [INV-G8] Plugin JSON files are valid JSON with required fields | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json')); assert all(k in d for k in ['name','version','description']), f'Missing fields: {d.keys()}'; print('PASS')\""
  ```

- [INV-G9] Skill frontmatter contains required fields and follows conventions | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify YAML frontmatter has: name (kebab-case, max 64 chars), description (max 1024 chars, action-oriented). Verify user-invocable is true (or defaulted)."
  ```

- [INV-G10] Agent definitions inherit tools from invoking context (no tools frontmatter) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read each agent definition: claude-plugins/manifest-dev-collab/agents/slack-coordinator.md, define-worker.md, executor.md. Verify that NONE of them declare a 'tools' field in their YAML frontmatter — they inherit all tools from the invoking context."
  ```

- [INV-G11] Prompt clarity: No contradictory instructions within or across modified files | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: opus
    prompt: "Review these prompt files for contradictions, unclear instructions, and anti-patterns: claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md, claude-plugins/manifest-dev-collab/agents/slack-coordinator.md, claude-plugins/manifest-dev-collab/agents/define-worker.md, claude-plugins/manifest-dev-collab/agents/executor.md, claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md, claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Focus on: (1) Does TEAM_CONTEXT collaboration mode contradict any existing constraint in the main SKILL.md? (2) Are teammate messaging instructions unambiguous? (3) Is the message→slack-coord→Slack→poll→relay pattern clear? (4) Do agent definitions clearly delineate responsibilities?"
  ```

- [INV-G12] Prompt information density: No redundant sections, no filler in prompts | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: code-simplicity-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md and all agent definitions in claude-plugins/manifest-dev-collab/agents/ for unnecessary complexity. Every section must earn its place. The SKILL.md should be focused on orchestration flow; agent .md files should be focused on their specific role. No duplication across files."
  ```

- [INV-G13] Documentation updated: READMEs reflect V3 architecture accurately | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Verify documentation consistency: (1) Root README.md mentions manifest-dev-collab plugin (2) claude-plugins/README.md includes manifest-dev-collab in plugin table (3) claude-plugins/manifest-dev-collab/README.md describes the V3 Agent Teams native architecture: team composition (lead, slack-coordinator, define-worker, executor), prerequisites (Slack MCP, Agent Teams env var, plugins installed), workflow phases, TEAM_CONTEXT, usage, resume instructions (4) claude-plugins/manifest-dev/README.md mentions team collaboration mode in /define and /do (5) No stale references to Python orchestrator, session-resume, COLLAB_CONTEXT, or V2 patterns in any docs"
  ```

- [INV-G14] CLAUDE.md adherence: All changes comply with project instructions | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review all changed and new files against CLAUDE.md instructions. Check: kebab-case naming, plugin structure conventions, version bump requirements, README sync checklist, skill frontmatter format, agent definitions (tools inherited, not declared)."
  ```

- [INV-G15] Python orchestrator and tests fully removed — no orphan files | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -f claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py && test ! -d tests/collab && echo PASS || echo FAIL"
  ```

## 4. Process Guidance (Non-Verifiable)

*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Keep the /slack-collab SKILL.md focused on orchestration flow — phase logic, team creation, state management, teammate coordination. Don't duplicate agent-specific instructions.
- [PG-2] Agent definitions should be self-contained — each agent .md file has everything the teammate needs to do its job. Don't assume the teammate reads the skill.
- [PG-3] TEAM_CONTEXT format must stay minimal. If new fields are needed, that's a manifest amendment.
- [PG-4] When modifying /define and /do COLLABORATION_MODE.md, verify the result by reading it in isolation — if it contradicts any existing constraint when active, it's wrong.
- [PG-5] Guard against scope creep — no Slack notifications beyond what's defined (Q&A, manifest review, escalations, PR review, QA, completion). No progress posts, no status updates.
- [PG-6] State file schema should be flat and simple — phase, channel info, stakeholders, manifest_path, pr_url. No nested schemas.
- [PG-7] Use `cp` and `mv` for file operations when moving/deleting the Python orchestrator and tests. Faster than Write tool for bulk operations.
- [PG-8] Lead memento pattern: re-read the state file after each phase transition to guard against context compression. The lead accumulates messages from 3 teammates across 7 phases — if context compresses, re-reading the state file restores phase awareness.

## 5. Known Assumptions

*Items where a reasonable default was chosen. High-impact assumptions have corresponding R-* risk areas with detection criteria. If any assumption is wrong, amend the manifest.*

- [ASM-1] `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` env var is set in user's Claude Code settings. | Default: User has configured it. | Impact if wrong: Teammate creation fails; skill should check and warn. | Severity: HIGH — blocks entire workflow.
- [ASM-2] Teammate↔teammate mailbox messaging works reliably. | Default: Documented Agent Teams feature. | Impact if wrong: Workflow stalls; messages lost. Fallback: route all messages through lead. | Severity: HIGH — see R-1.
- [ASM-3] Teammates persist across phases (define-worker stays alive through QA). | Default: Teammates stay until lead dismisses or session ends. | Impact if wrong: Define-worker gone by QA; lead re-spawns with manifest context. | Severity: HIGH — see R-2.
- [ASM-4] Lead detects teammate completion via idle notifications. | Default: Documented Agent Teams behavior. | Impact if wrong: Lead polls shared task list as fallback. | Severity: MEDIUM.
- [ASM-5] Teammates inherit Slack MCP from project context. | Default: Agent Teams docs confirm. | Impact if wrong: slack-coordinator can't use Slack tools; workflow fails at channel creation. | Severity: HIGH — see R-8.
- [ASM-6] /define invoked via Skill tool inside a teammate session works normally. | Default: Teammates inherit skills. | Impact if wrong: define-worker follows /define methodology from agent prompt instead. | Severity: HIGH — see R-3.
- [ASM-7] One lead can manage 3 teammates simultaneously. | Default: Recommended team size is 3-5. | Impact if wrong: Reduce to 2 teammates (merge roles).
- [ASM-8] Agent Teams works in interactive mode (not just `-p` mode). | Default: Confirmed — Agent Teams docs describe interactive usage with Shift+Down to cycle teammates. | Impact if wrong: Need `-p` mode with Agent Teams env var like V2.
- [ASM-9] Slack MCP is pre-configured in user's Claude Code settings. | Default: User has Slack MCP set up. | Impact if wrong: Slack-coordinator fails at first Slack call.
- [ASM-10] Slack MCP provides: create_channel, invite_to_channel, post_message, read_messages/read_thread_replies. | Default: Standard Slack MCP tools. | Impact if wrong: Slack-coordinator must adapt tool names.
- [ASM-11] No automated E2E/integration tests — requires full Agent Teams + Slack environment. Verification via subagent review of prompts and flow. | Default: Manual integration testing. | Impact if wrong: Integration bugs caught later.

## 6. Deliverables (The Work)

### Deliverable 1: Rewrite /slack-collab Skill (Orchestrator)

*Complete rewrite of `claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md` from thin Python launcher to full Agent Teams orchestrator.*

**Acceptance Criteria:**

- [AC-1.1] Skill acts as team lead: preflight phase asks user for stakeholders via AskUserQuestion, then creates team. Passes full stakeholder roster (names, handles, roles) to slack-coordinator in its spawn prompt | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify: (1) Preflight phase uses AskUserQuestion to gather stakeholder names, Slack handles, roles, and QA needs (2) After preflight, creates Agent Teams team with 3 teammates: slack-coordinator, define-worker, executor (3) Each teammate spawned with reference to their agent definition file (4) Slack-coordinator spawn prompt includes the full stakeholder roster (names, handles, roles, QA flag) from preflight — this is how the coordinator gets its routing table (5) No Python script invocation"
  ```

- [AC-1.2] Phase flow matches the confirmed architecture: preflight → define → manifest review → execute → PR → QA (optional) → done | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify the orchestration flow includes all 7 phases in order: (0) Preflight (1) Define (2) Manifest Review (3) Execute (4) PR (5) QA optional (6) Done. For each phase, verify the lead's specific actions match: preflight=AskUserQuestion+create team, define=message define-worker, review=message slack-coord, execute=message executor, PR=message executor+slack-coord, QA=slack-coord→define-worker→executor flow, done=slack-coord posts summary."
  ```

- [AC-1.3] State file management: writes JSON state file to `/tmp/collab-state-{identifier}.json` after each phase transition. State includes: phase, channel_id, stakeholders, manifest_path, pr_url | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify: (1) Instructs writing a JSON state file after each phase transition (2) State file path includes unique identifier (3) State contains at minimum: phase, channel info, stakeholders, manifest_path, pr_url (4) State schema is flat (no nested objects beyond stakeholder list)"
  ```

- [AC-1.4] Resume capability: `--resume <state-file-path>` in arguments reads state and continues from the interrupted phase. Re-creates team from state context | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify: (1) Supports --resume flag or equivalent in arguments (2) Reads state file (3) Re-creates team with existing channel/stakeholder context (4) Continues from interrupted phase (5) Notes that mid-phase progress is lost on crash"
  ```

- [AC-1.5] Teammate crash handling: detects teammate failure, re-spawns once with same task. If second failure, writes state and stops | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify: (1) Instructs monitoring teammate status (2) On teammate failure/crash: re-spawn the teammate once with the same task (3) On second failure: write state file and inform user (4) No infinite retry loops"
  ```

- [AC-1.6] QA feedback flow: slack-coordinator routes QA issues to define-worker (evaluate against manifest), define-worker routes validated issues to executor (fix), executor reports fix to slack-coordinator | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify QA phase describes: (1) slack-coordinator receives QA issues from Slack (2) Routes to define-worker for manifest evaluation (3) define-worker evaluates against ACs, identifies which are violated (4) define-worker messages executor with specific fix instructions (5) executor fixes and reports back (6) slack-coordinator posts update to Slack"
  ```

- [AC-1.7] Valid frontmatter | Verify: covered by INV-G9

### Deliverable 2: Agent Definitions

*Create agent definition files for each teammate.*

**Acceptance Criteria:**

- [AC-2.1] `agents/slack-coordinator.md` defines the Slack I/O agent: channel setup, message posting, polling, response routing, owner override, prompt injection defense, 2-hour polling timeout | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/slack-coordinator.md. Verify: (1) Defines agent responsible for ALL Slack I/O (2) Capabilities: create channels, invite users, post messages, read threads, poll for responses (3) Stakeholder routing: receives context/expertise hints from teammates, makes autonomous routing decisions to the right stakeholder thread(s) (4) Owner override: owner can reply in any stakeholder's thread to answer on their behalf — coordinator treats owner answer as authoritative (5) Includes prompt injection defense instructions (6) Includes polling timeout: after 2 hours with no stakeholder response, escalate to owner (7) Routes responses back to requesting teammate (8) Splits long content (>4000 chars) into numbered messages (9) Frontmatter declares all needed tools (Slack MCP tools, Bash for sleep, messaging)"
  ```

- [AC-2.2] `agents/define-worker.md` defines the define process agent: invokes /define with TEAM_CONTEXT, messages slack-coordinator for Q&A, persists as manifest authority for QA evaluation | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/define-worker.md. Verify: (1) Primary task: invoke /define skill with task + TEAM_CONTEXT (2) Messages slack-coordinator when /define needs stakeholder input (3) After /define completes, persists as manifest authority (4) QA role: receives issues from slack-coordinator, evaluates against manifest ACs, messages executor with validated fix instructions (5) Never touches Slack directly (6) Frontmatter declares all needed tools (Skill invocation, messaging, file read/write for manifest and discovery log, subagent spawning for manifest-verifier)"
  ```

- [AC-2.3] `agents/executor.md` defines the execution agent: invokes /do with TEAM_CONTEXT, messages slack-coordinator for escalations, creates PR, fixes QA issues | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/agents/executor.md. Verify: (1) Primary task: invoke /do skill with manifest path + TEAM_CONTEXT (2) Messages slack-coordinator for escalations during /do (3) Creates PR after execution completes (4) Fixes QA issues received from define-worker (5) Never touches Slack directly (6) Frontmatter declares all needed tools (Skill invocation, messaging, bash for git/gh, file read/write, subagent spawning for verification)"
  ```

- [AC-2.4] Agent definitions omit tools frontmatter (inherit from invoking context) | Verify: covered by INV-G10

### Deliverable 3: Update COLLABORATION_MODE.md Files

*Rewrite both /define and /do COLLABORATION_MODE.md from COLLAB_CONTEXT (Slack MCP) to TEAM_CONTEXT (teammate messaging).*

**Acceptance Criteria:**

- [AC-3.1] /define COLLABORATION_MODE.md: when TEAM_CONTEXT present, /define messages the coordinator teammate for stakeholder input instead of using AskUserQuestion. Messages include relevant expertise context so coordinator can route to the right stakeholder. Waits for coordinator reply. Continues interview | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md. Verify: (1) Activated by TEAM_CONTEXT in arguments (not COLLAB_CONTEXT) (2) Instead of AskUserQuestion, messages the coordinator teammate (3) Question format: include options as numbered list plus relevant expertise context (e.g., 'Relevant expertise: backend/security') so coordinator can route to the right stakeholder (4) Routing delegation: /define does NOT decide which specific stakeholder to ask — it provides context and the coordinator makes the routing decision (5) Waits for coordinator's reply with stakeholder answer (6) Continues interview from where it left off (7) Discovery log and manifest write to /tmp only (8) Verification loop runs locally (9) No Slack-specific instructions — transport is teammate messaging (10) Security note: explicitly states that prompt injection defense is handled by the coordinator agent (11) Everything else in /define unchanged"
  ```

- [AC-3.2] /do COLLABORATION_MODE.md: when TEAM_CONTEXT present, /do messages the coordinator teammate for escalations instead of direct Slack interaction. Posts escalation with context. Waits for reply | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify: (1) Activated by TEAM_CONTEXT in arguments (not COLLAB_CONTEXT) (2) For escalations, messages the coordinator teammate (3) Escalation format: what's blocked, what was tried, options for resolution (4) Waits for coordinator's reply with owner response (5) Continues execution (6) Execution log and verification results write to /tmp only (7) /verify and todos work locally as normal (8) No Slack-specific instructions (9) Security note: explicitly states that prompt injection defense is handled by the coordinator agent (10) Everything else in /do unchanged"
  ```

- [AC-3.3] Both files include memento discipline reminder: log to discovery/execution file after EACH stakeholder/owner response received via coordinator | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read both COLLABORATION_MODE.md files: claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md and claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify each includes explicit instruction to log findings/decisions to the appropriate log file after receiving each response from the coordinator. This is the memento pattern to guard against context compression in long teammate sessions."
  ```

### Deliverable 4: Update SKILL.md Detection Strings

*Update /define and /do main SKILL.md files to detect TEAM_CONTEXT instead of COLLAB_CONTEXT.*

**Acceptance Criteria:**

- [AC-4.1] /define SKILL.md: collaboration mode section references TEAM_CONTEXT detection instead of COLLAB_CONTEXT | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md. Verify: (1) The collaboration mode section references 'TEAM_CONTEXT:' as the detection string (2) No references to 'COLLAB_CONTEXT' remain (3) All other content is unchanged"
  ```

- [AC-4.2] /do SKILL.md: collaboration mode section references TEAM_CONTEXT detection instead of COLLAB_CONTEXT | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md. Verify: (1) The collaboration mode section references 'TEAM_CONTEXT:' as the detection string (2) No references to 'COLLAB_CONTEXT' remain (3) All other content is unchanged"
  ```

### Deliverable 5: Delete Python Orchestrator and Tests

*Remove V2 artifacts: Python script and unit tests.*

**Acceptance Criteria:**

- [AC-5.1] `scripts/slack-collab-orchestrator.py` deleted | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -f claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py && echo PASS || echo FAIL"
  ```

- [AC-5.2] `scripts/` directory removed (or empty) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -d claude-plugins/manifest-dev-collab/scripts && echo PASS || (find claude-plugins/manifest-dev-collab/scripts -type f | wc -l | xargs test 0 -eq && echo PASS || echo FAIL)"
  ```

- [AC-5.3] `tests/collab/` directory and all test files removed | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test ! -d tests/collab && echo PASS || echo FAIL"
  ```

### Deliverable 6: Update Plugin Structure

*Ensure manifest-dev-collab plugin has correct structure for V3.*

**Acceptance Criteria:**

- [AC-6.1] `agents/` directory exists with 3 agent definitions | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-collab/agents/slack-coordinator.md && test -f claude-plugins/manifest-dev-collab/agents/define-worker.md && test -f claude-plugins/manifest-dev-collab/agents/executor.md && echo PASS || echo FAIL"
  ```

- [AC-6.2] Plugin JSON valid with correct metadata | Verify: covered by INV-G8

### Deliverable 7: Update Documentation

*Update all affected READMEs per sync checklist.*

**Acceptance Criteria:**

- [AC-7.1] Root README.md lists manifest-dev-collab plugin | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-collab' README.md && echo PASS || echo FAIL"
  ```

- [AC-7.2] claude-plugins/README.md includes manifest-dev-collab in plugin table | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-collab' claude-plugins/README.md && echo PASS || echo FAIL"
  ```

- [AC-7.3] manifest-dev-collab/README.md describes V3 Agent Teams native architecture | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/README.md. Verify it includes: (1) Overview of V3 Agent Teams native architecture (lead orchestrator + 3 teammates) (2) Team composition: slack-coordinator, define-worker, executor — roles described (3) Prerequisites: Slack MCP, CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS env var, plugins installed (4) Usage: /slack-collab 'task description' (5) Resume: how to resume from crash (6) Workflow phases listed (7) TEAM_CONTEXT explained (8) Known limitations: Agent Teams experimental, mid-phase crash recovery not supported (9) No references to Python orchestrator, COLLAB_CONTEXT, or V2 patterns"
  ```

- [AC-7.4] manifest-dev/README.md mentions team collaboration mode in /define and /do | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -qi 'team.*collaborat\\|collaborat.*team\\|TEAM_CONTEXT' claude-plugins/manifest-dev/README.md && echo PASS || echo FAIL"
  ```

- [AC-7.5] No stale references to Python orchestrator, COLLAB_CONTEXT, or session-resume in any README | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "if grep -rli 'COLLAB_CONTEXT\\|slack-collab-orchestrator\\.py\\|session-resume\\|session_resume' README.md claude-plugins/*/README.md 2>/dev/null; then echo FAIL; else echo PASS; fi"
  ```

### Deliverable 8: Version Bumps

*Bump versions for affected plugins.*

**Acceptance Criteria:**

- [AC-8.1] manifest-dev plugin version bumped (minor — COLLABORATION_MODE.md changes) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json,subprocess; current=subprocess.run(['git','show','HEAD:claude-plugins/manifest-dev/.claude-plugin/plugin.json'],capture_output=True,text=True); old=json.loads(current.stdout)['version'] if current.returncode==0 else '0.0.0'; new=json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; old_parts=list(map(int,old.split('.'))); new_parts=list(map(int,new.split('.'))); assert new_parts>old_parts, f'Version not bumped: {old} -> {new}'; print(f'PASS: {old} -> {new}')\""
  ```

- [AC-8.2] manifest-dev-collab plugin version bumped (major — breaking architecture change) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json,subprocess; current=subprocess.run(['git','show','HEAD:claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json'],capture_output=True,text=True); old=json.loads(current.stdout)['version'] if current.returncode==0 else '0.0.0'; new=json.load(open('claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json'))['version']; old_parts=list(map(int,old.split('.'))); new_parts=list(map(int,new.split('.'))); assert new_parts>old_parts, f'Version not bumped: {old} -> {new}'; print(f'PASS: {old} -> {new}')\""
  ```

### Deliverable 9: Manifest Archival

*Save this V3 manifest to .manifest/ directory.*

**Acceptance Criteria:**

- [AC-9.1] `.manifest/` directory contains V1, V2, and V3 manifests | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ls .manifest/slack-collab-*2026*.md | wc -l | xargs test 3 -le && echo PASS || echo FAIL"
  ```
