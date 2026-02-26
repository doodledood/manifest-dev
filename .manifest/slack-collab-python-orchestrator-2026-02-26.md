# Definition: Slack-Based Collaborative Define/Do Workflow (Python Orchestrator)

## 1. Intent & Context

- **Goal:** Replace the pure-skill /slack-collab orchestrator with a **Python script** that controls workflow phases deterministically, invoking Claude Code CLI for intelligent work (define, do, Slack interaction). Python handles phase transitions, polling, crash recovery via state file. Slack scoped to collaboration only (Q&A, approvals, escalations) — all logs and artifacts stay in local files. **Claude Code never polls** — when /define or /do needs a Slack response, it posts the question/escalation and returns JSON; Python polls Slack and resumes the Claude session with `--resume <session-id>`.

- **Mental Model:**
  - **Python orchestrator** = deterministic shell. Controls phase transitions, launches Claude CLI for each phase, persists state to JSON, polls for approvals by invoking Claude CLI to read Slack threads.
  - **COLLAB_CONTEXT** = behavior switch. Passed to /define and /do via CLI arguments. Tells them to use Slack MCP tools for stakeholder Q&A instead of AskUserQuestion. Simplified: only stakeholder threads, no log/artifact threads. No poll_interval — Python owns all polling.
  - **Claude CLI** = the brain. Each phase is a `claude -p "..." --dangerously-skip-permissions --session-id <uuid>` call. Claude does the intelligent work; Python does the deterministic work.
  - **Session resume** = conversation continuity. For /define and /do, the orchestrator generates a session UUID, passes it via `--session-id`. When Claude returns "waiting_for_response" / "escalation_pending", Python polls Slack, then uses `claude -p "<response>" --resume <session-id>` to continue the same session with full context.
  - **Slack** = collaboration medium only. Stakeholder Q&A, manifest review, escalations, PR review. NOT for logs, progress, or state.
  - **State file** = crash recovery. JSON file in /tmp, written after each phase transition. Manual relaunch with `--resume` to continue.
  - **Thin skill** = launcher. /slack-collab SKILL.md tells Claude to run the Python script via Bash (run_in_background). Fire-and-forget.

- **COLLAB_CONTEXT Canonical Format** (simplified; identical for /define and /do):
  ```
  COLLAB_CONTEXT:
    channel_id: <slack-channel-id>
    owner_handle: <@owner>
    threads:
      stakeholders:
        <@handle>: <thread-ts>
        <@handle1+@handle2>: <thread-ts>
    stakeholders:
      - handle: <@handle>
        name: <display-name>
        role: <role/expertise>
  ```
  **No poll_interval**: Polling is Python's job. Skills never poll — they post and return JSON.
  **Detection**: Skills detect collaboration mode by checking if `$ARGUMENTS` contains the literal string `COLLAB_CONTEXT:` on its own line. The Python orchestrator places the COLLAB_CONTEXT block after a double newline following the task description. The block must be the last content in the arguments string.

## 2. Approach

*Initial direction, not rigid plan. Provides enough to start confidently; expect adjustment when reality diverges.*

- **Architecture:**

  ```
  /slack-collab skill (thin launcher)
       │
       └─→ Bash(run_in_background): python3 scripts/slack-collab-orchestrator.py "task"
              │
              ├─ Phase 0: Pre-flight
              │   └─ claude -p "gather stakeholders, create channel, create threads"
              │       → writes /tmp/collab-{id}-state.json (channel_id, thread_ids, stakeholders)
              │
              ├─ Phase 1: Define (session-resume loop)
              │   └─ claude -p "/define {task}\n\nCOLLAB_CONTEXT:..." --session-id <uuid>
              │       → /define posts question to Slack, returns {"status":"waiting_for_response",...}
              │       → Python polls Slack for response
              │       → claude -p "<stakeholder response>" --resume <session-id>
              │       → (repeat until {"status":"complete","manifest_path":"..."})
              │       → writes manifest path to state JSON
              │
              ├─ Phase 2: Manifest Review
              │   └─ claude -p "post manifest to Slack, ask for approval"
              │   └─ Python poll loop: sleep(interval) → claude -p "check for approval in thread"
              │       → approval or feedback (loop back to Define if feedback)
              │
              ├─ Phase 3: Execute (session-resume loop)
              │   └─ claude -p "/do {manifest}\n\nCOLLAB_CONTEXT:..." --session-id <uuid>
              │       → /do hits blocker, posts escalation, returns {"status":"escalation_pending",...}
              │       → Python polls Slack for owner response
              │       → claude -p "<owner response>" --resume <session-id>
              │       → (repeat until {"status":"complete"})
              │       → or runs to completion without escalation
              │
              ├─ Phase 4: PR
              │   └─ claude -p "create PR from manifest"
              │   └─ claude -p "post PR to Slack for review"
              │   └─ Python poll loop: sleep(interval) → claude -p "check PR status"
              │       → auto-fix review comments (max 3 attempts, then escalate)
              │
              ├─ Phase 5: QA (optional)
              │   └─ claude -p "post QA request to Slack"
              │   └─ Python poll loop: sleep(interval) → claude -p "check QA sign-off"
              │
              └─ Phase 6: Done
                  └─ claude -p "post completion summary to Slack"
                  └─ Python writes final state, exits
  ```

  Key design: Python is procedural — each phase is a function. State JSON written after each phase. Claude CLI calls use `-p --dangerously-skip-permissions --output-format json --json-schema '{...}'` for validated structured output. Python reads JSON from stdout — no file-based handoff needed.

  **JSON Output Schemas** (contract between Python and Claude CLI — passed via `--json-schema`):

  Pre-flight schema:
  ```json
  {
    "type": "object",
    "properties": {
      "channel_id": {"type": "string"},
      "channel_name": {"type": "string"},
      "owner_handle": {"type": "string"},
      "stakeholders": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "handle": {"type": "string"},
            "name": {"type": "string"},
            "role": {"type": "string"},
            "is_qa": {"type": "boolean"}
          },
          "required": ["handle", "name", "role"]
        }
      },
      "threads": {
        "type": "object",
        "properties": {
          "stakeholders": {"type": "object"}
        }
      },
      "slack_mcp_available": {"type": "boolean"}
    },
    "required": ["channel_id", "stakeholders", "threads", "slack_mcp_available"]
  }
  ```

  Define output schema (union — Claude returns one of two states):
  ```json
  {
    "type": "object",
    "properties": {
      "status": {"type": "string", "enum": ["waiting_for_response", "complete"]},
      "thread_ts": {"type": "string"},
      "target_handle": {"type": "string"},
      "question_summary": {"type": "string"},
      "manifest_path": {"type": "string"},
      "discovery_log_path": {"type": "string"}
    },
    "required": ["status"]
  }
  ```
  When `status: "waiting_for_response"`: thread_ts, target_handle, question_summary are populated.
  When `status: "complete"`: manifest_path (required), discovery_log_path (optional) are populated.

  Do/Execute output schema (union — Claude returns one of two states):
  ```json
  {
    "type": "object",
    "properties": {
      "status": {"type": "string", "enum": ["escalation_pending", "complete"]},
      "thread_ts": {"type": "string"},
      "escalation_summary": {"type": "string"},
      "do_log_path": {"type": "string"}
    },
    "required": ["status"]
  }
  ```
  When `status: "escalation_pending"`: thread_ts, escalation_summary are populated.
  When `status: "complete"`: do_log_path (optional) is populated.

  Polling check schema:
  ```json
  {
    "type": "object",
    "properties": {
      "approved": {"type": "boolean"},
      "feedback": {"type": ["string", "null"]}
    },
    "required": ["approved"]
  }
  ```

- **Execution Order:**
  - D1 (Update /define collab) + D2 (Update /do collab) → D3 (Plugin structure) → D4 (Python orchestrator) → D8 (Unit tests) → D5 (Thin skill rewrite) → D6 (Documentation) → D7 (Version bumps)
  - Rationale: D1/D2 simplify COLLAB_CONTEXT (can be parallel). D3 creates scripts/ dir. D4 is the main work, depends on D1/D2 format. D8 tests D4's logic. D5 depends on D4 (launches it). D6/D7 last.

- **Risk Areas:**
  - [R-1] Skills don't work in `-p` mode | Detect: `claude -p "/define test"` fails to invoke skill. Mitigation: fall back to passing full prompt via --system-prompt.
  - [R-2] `--json-schema` output doesn't match expected structure | Detect: JSON parsing fails or required fields missing. Mitigation: `--json-schema` enforces schema validation at CLI level; Python validates required fields as secondary check.
  - [R-3] Claude CLI subprocess hangs indefinitely | Detect: Python waits forever on subprocess.run(). Mitigation: set subprocess timeout per phase.
  - [R-4] Slack MCP tools not available | Detect: first CLI call fails. Mitigation: pre-flight check, fail fast with clear error.
  - [R-5] COLLAB_CONTEXT format change breaks existing /define or /do collaboration mode | Detect: /define doesn't detect COLLAB_CONTEXT or misparses it. Mitigation: D1/D2 update and INV-G3 verification.

- **Trade-offs:**
  - [T-1] Python complexity vs Claude autonomy → Prefer Python handles all deterministic logic (phase transitions, polling, state), Claude handles all intelligent logic (Q&A, code generation, reviews). Clear boundary.
  - [T-2] Subprocess timeout vs infinite wait → Prefer generous timeouts per phase (pre-flight: 5min, define: 4hr, do: 2hr, polling calls: 2min). Prevents hangs while allowing long workflows.
  - [T-3] State file completeness vs simplicity → Prefer flat JSON with just enough to resume (phase, channel_id, thread_ids, manifest_path, pr_url). No nested schemas.
  - [T-4] Error recovery vs simplicity → Prefer terminate + manual resume over auto-retry. One retry path, no cascading complexity.
  - [T-5] Slack-native richness vs portability → Prefer Slack-native features (threads, mentions). Not building for portability.

## 3. Global Invariants (The Constitution)

*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] /define non-collaboration paths unchanged (no regression) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Compare the /define SKILL.md before and after changes. IMPORTANT: Two intentional changes: (1) The '## Collaboration Mode' section has been replaced with a 2-line reference to references/COLLABORATION_MODE.md. (2) Output paths changed from /tmp/ to .manifest/ (manifest output, discovery log). Both are expected. Verify that all other instruction paths are identical to the original: AskUserQuestion constraint unchanged, verification loop unchanged, all methodology sections unchanged. The main SKILL.md should contain only a brief reference for collaboration mode, NOT the full content."
  ```

- [INV-G2] /do non-collaboration paths unchanged (no regression) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Compare the /do SKILL.md before and after changes. IMPORTANT: The '## Collaboration Mode' section has been replaced with a 2-line reference to references/COLLABORATION_MODE.md — this is the only intentional change. Verify that all other instruction paths are identical to the original: execution log path still /tmp/, escalation behavior unchanged, verification invocation unchanged, memento pattern unchanged. The main SKILL.md should contain only a brief reference for collaboration mode, NOT the full content."
  ```

- [INV-G3] COLLAB_CONTEXT format is identical between Python orchestrator (producer) and /define, /do (consumers) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Extract the COLLAB_CONTEXT format from: (1) the Python orchestrator script where it constructs the context string, (2) /define's references/COLLABORATION_MODE.md where it documents the expected format, (3) /do's references/COLLABORATION_MODE.md where it documents the expected format. Verify field names, types, and structure are identical across all three. The format should contain: channel_id, owner_handle, threads.stakeholders map, stakeholders list (handle, name, role). No poll_interval — Python owns polling. No extra fields in any file. Files: claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md, claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md, claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py"
  ```

- [INV-G4] All new files follow kebab-case naming convention | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "find claude-plugins/manifest-dev-collab -type f | grep -v '.claude-plugin' | grep -v __pycache__ | while read f; do basename \"$f\" | grep -qE '^[a-z0-9][a-z0-9_-]*\\.[a-z]+$' || echo \"FAIL: $f\"; done"
  ```

- [INV-G5] No Python linting/formatting/type errors in any modified or new Python files | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ruff check --fix claude-plugins/ && black --check claude-plugins/ && mypy"
  ```

- [INV-G6] Plugin JSON files are valid JSON with required fields | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json')); assert all(k in d for k in ['name','version','description']), f'Missing fields: {d.keys()}'; print('PASS')\""
  ```

- [INV-G7] Skill frontmatter contains required fields and follows conventions | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify YAML frontmatter has: name (kebab-case, max 64 chars), description (max 1024 chars, action-oriented). Verify user-invocable is true (or defaulted)."
  ```

- [INV-G8] Prompt clarity: No contradictory instructions within or across modified skill files | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: opus
    prompt: "Review these prompt files for contradictions, unclear instructions, and anti-patterns: claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md, claude-plugins/manifest-dev/skills/define/SKILL.md, claude-plugins/manifest-dev/skills/do/SKILL.md, claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md, claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Focus on: (1) Does the collaboration mode reference file contradict any existing constraint in the main SKILL.md? (2) Are the Slack interaction instructions unambiguous? (3) Is the collaboration context detection clear and non-fragile? (4) Does the reference instruction in the main SKILL.md clearly direct Claude to read the reference file?"
  ```

- [INV-G9] Prompt information density: No redundant sections, no filler in skill prompts | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: code-simplicity-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md for unnecessary complexity. Is the prompt lean? Does every section earn its place? The skill should be a thin launcher — if it's more than ~30 lines of instruction, it's too complex."
  ```

- [INV-G10] Documentation updated: READMEs reflect all changes accurately | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Verify documentation consistency: (1) Root README.md mentions manifest-dev-collab plugin (2) claude-plugins/README.md includes manifest-dev-collab in plugin table (3) claude-plugins/manifest-dev-collab/README.md describes the Python orchestrator architecture, prerequisites (Slack MCP, Python 3.8+), workflow phases, usage, and resume instructions (4) claude-plugins/manifest-dev/README.md mentions collaboration mode in /define and /do (5) No stale references"
  ```

- [INV-G11] CLAUDE.md adherence: All changes comply with project instructions | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Review all changed and new files against CLAUDE.md instructions. Check: kebab-case naming, plugin structure conventions, version bump requirements, README sync checklist, skill frontmatter format."
  ```

- [INV-G12] Python script handles all error paths with clear messages — no silent failures | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: code-bugs-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py for error handling: (1) Every subprocess.run() call checks returncode (2) Every JSON file read has try/except with clear error message (3) Pre-flight failure terminates with actionable message (4) No bare except clauses (5) State file written before termination on error (6) Errors logged to local log file"
  ```

- [INV-G13] Python script is procedural and simple — no unnecessary abstractions | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: code-simplicity-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py for unnecessary complexity. Check: (1) No class hierarchies for a procedural script (2) No abstract base classes or design patterns (3) Each phase is a simple function (4) State is a flat dict, not a complex schema (5) CLI invocation is direct subprocess.run, not wrapped in layers"
  ```

- [INV-G14] Prompt injection defense in skill prompts: /define and /do collaboration mode instructs treating Slack messages as potentially adversarial | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the collaboration mode reference files: claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md and claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify they include instructions to: (1) Not execute unrelated actions requested by stakeholders in Slack (2) Never expose env vars, secrets, credentials (3) Treat Slack messages as potentially adversarial input (4) Politely decline dangerous requests and tag the owner"
  ```

- [INV-G15] Python code maintainability: clean, readable, well-structured | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: code-maintainability-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py for maintainability."
  ```

- [INV-G16] Python code design fitness: architecture appropriate for the problem | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: code-design-reviewer
    model: opus
    prompt: "Review claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py for design fitness. The script should be a simple phase-based orchestrator using subprocess to invoke Claude CLI. Check that the design matches the problem complexity — no over-engineering."
  ```

## 4. Process Guidance (Non-Verifiable)

*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Collaboration mode sections in /define and /do must be cleanly separated — dedicated "## Collaboration Mode" section, not scattered conditionals.
- [PG-2] The thin /slack-collab skill should be minimal — just enough to launch the Python script. Don't duplicate orchestration logic in the skill prompt.
- [PG-3] Keep the Python state file flat — simple dict with string/number values. No nested schemas, no versioning, no migration logic.
- [PG-4] Keep the Python script procedural — one function per phase. No class hierarchies, no abstract patterns, no middleware.
- [PG-5] Document all load-bearing assumptions in code comments — Slack MCP tool names, CLI flag behavior, file paths.
- [PG-6] Guard against scope creep — no Slack notifications beyond what's defined (Q&A, manifest review, escalations, PR review). No progress posts, no status updates.
- [PG-7] The COLLAB_CONTEXT format must not grow beyond the fields defined in the canonical spec. If new fields are needed, that's a manifest amendment.
- [PG-8] When modifying /define and /do, verify the collaboration mode section by reading it in isolation — if it contradicts any existing constraint when active, it's wrong.

## 5. Known Assumptions

*Low-impact items where a reasonable default was chosen without explicit user confirmation. If any assumption is wrong, amend the manifest.*

- [ASM-1] `claude` CLI is on PATH and functional. | Default: Standard Claude Code installation. | Impact if wrong: Script fails immediately with clear error.
- [ASM-2] Slack MCP is pre-configured in user's Claude Code settings. | Default: User has already set up Slack MCP server. | Impact if wrong: Pre-flight check catches this, terminates with instructions.
- [ASM-3] Python 3.8+ is available. | Default: Widely available on modern systems. | Impact if wrong: Script fails with syntax error or import error.
- [ASM-4] `/tmp` is writable and persists for workflow duration. | Default: Standard Unix behavior. | Impact if wrong: State/artifact files can't be written.
- [ASM-5] `--json-schema` with `--output-format json` produces validated JSON on stdout. | Default: CLI help confirms these flags exist. | Impact if wrong: Fall back to --append-system-prompt file-based approach.
- [ASM-6] manifest-dev and manifest-dev-collab plugins are installed globally. | Default: User has installed plugins. | Impact if wrong: /define and /do skills not available; pre-flight can check.
- [ASM-7] Slack MCP provides: create_channel, invite_to_channel, post_message, read_messages/read_thread_replies. | Default: Available in major Slack MCP implementations. | Impact if wrong: Pre-flight check catches.
- [ASM-8] Slack message character limit ~4000 chars. | Default: Standard Slack limit. | Impact if wrong: Messages may be truncated; Python can split.
- [ASM-9] No automated E2E/integration tests — integration testing requires full Slack + Claude environment. Unit tests (D8) cover deterministic logic only. | Default: Manual integration testing during development. | Impact if wrong: Integration bugs caught later. Acceptable for MVP.
- [ASM-10] Claude CLI `--session-id <uuid>` sets the session UUID and `--resume <session-id>` resumes that session with full conversation context. | Default: Confirmed from CLI help and SDK docs. | Impact if wrong: Would need to use `--continue` (resumes last session) or fresh `-p` calls with serialized state.
- [ASM-11] Claude CLI `--resume` works with `-p` and `--output-format json` — the resumed session produces JSON output matching the `--json-schema` from the original session. | Default: Reasonable based on CLI docs showing resume + print mode. | Impact if wrong: May need `--json-schema` on each resume call too.

## 6. Deliverables (The Work)

### Deliverable 1: Update Collaboration Mode in /define SKILL.md

*Simplify the existing collaboration mode section: remove dual-write, simplify COLLAB_CONTEXT to stakeholder threads only.*

**Acceptance Criteria:**

- [AC-1.1] COLLAB_CONTEXT format in /define matches the simplified canonical spec (channel_id, owner_handle, threads.stakeholders, stakeholders list — no poll_interval, no process_log, manifest, execution, or verification threads) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md. Extract the COLLAB_CONTEXT format. Verify it contains ONLY: channel_id, owner_handle, threads.stakeholders (map of handle to thread-ts), stakeholders (list of handle/name/role). Verify it does NOT contain: poll_interval, process_log, manifest, execution, verification thread IDs. Also verify the main SKILL.md (claude-plugins/manifest-dev/skills/define/SKILL.md) has only a brief reference to the collaboration mode file, not the full content."
  ```

- [AC-1.2] No dual-write: discovery log writes to /tmp only, manifest writes to /tmp only. No Slack thread posting of logs or artifacts from /define itself | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md. Verify: (1) Discovery log is written to /tmp only — no instruction to post to Slack threads (2) Manifest is written to /tmp only — no instruction to post to Slack threads (3) The ONLY Slack interaction is posting questions to stakeholder threads."
  ```

- [AC-1.3] Stakeholder Q&A uses post-and-exit pattern: questions posted to stakeholder threads, then Claude exits with "waiting_for_response" JSON. No polling by Claude — orchestrator handles that. Owner can answer on behalf | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md. Verify it specifies: (1) Questions posted to stakeholder threads as thread replies with @-tag (2) Claude immediately exits with JSON {status:'waiting_for_response', thread_ts, target_handle, question_summary} — does NOT poll or wait (3) Owner can reply in any thread to answer on behalf (4) Multi-stakeholder question routing to shared threads (5) When session is resumed with the response, Claude continues the interview"
  ```

- [AC-1.4] Prompt injection defense present in collaboration mode | Verify: covered by INV-G14

### Deliverable 2: Update Collaboration Mode in /do SKILL.md

*Simplify the existing collaboration mode section: remove dual-write, simplify COLLAB_CONTEXT to stakeholder threads only.*

**Acceptance Criteria:**

- [AC-2.1] COLLAB_CONTEXT format in /do matches the simplified canonical spec (identical to /define's format — no poll_interval) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Extract the COLLAB_CONTEXT format. Verify it contains ONLY: channel_id, owner_handle, threads.stakeholders map, stakeholders list. No poll_interval. Verify format is identical to /define's. Also verify the main SKILL.md (claude-plugins/manifest-dev/skills/do/SKILL.md) has only a brief reference to the collaboration mode file, not the full content."
  ```

- [AC-2.2] No dual-write: execution log and verification results write to /tmp only. No Slack thread posting of logs or artifacts from /do itself | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify: (1) Execution log writes to /tmp only (2) Verification results write to /tmp only (3) The ONLY Slack interaction is posting escalations to stakeholder/owner threads."
  ```

- [AC-2.3] Escalations use post-and-exit pattern: posted to the owner's stakeholder thread, then Claude exits with "escalation_pending" JSON. No polling by Claude — orchestrator handles that | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md. Verify it specifies: (1) Escalations posted to the owner's stakeholder thread (identified by owner_handle in threads.stakeholders map) (2) Owner tagged with @handle (3) Claude immediately exits with JSON {status:'escalation_pending', thread_ts, escalation_summary} — does NOT poll or wait (4) When session is resumed with the owner's response, Claude continues execution"
  ```

### Deliverable 3: Update Plugin Structure

*Add scripts/ directory to manifest-dev-collab plugin.*

**Acceptance Criteria:**

- [AC-3.1] `scripts/` directory exists in manifest-dev-collab with the orchestrator script | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test -f claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py && echo PASS || echo FAIL"
  ```

- [AC-3.2] Plugin JSON still valid with correct metadata | Verify: covered by INV-G6

### Deliverable 4: Python Orchestrator Script

*The main deliverable: `claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py`*

**Acceptance Criteria:**

- [AC-4.1] Pre-flight phase: invokes Claude CLI to gather stakeholders, create Slack channel, create stakeholder threads. Writes initial state JSON with channel_id, thread_ids, stakeholders | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify pre-flight phase: (1) Invokes claude CLI with -p, --dangerously-skip-permissions, --output-format json, and --json-schema with the pre-flight schema (2) Prompt instructs Claude to: detect owner, gather stakeholders (names, handles, roles), ask about QA needs, create Slack channel, invite stakeholders, create per-stakeholder threads (3) Reads validated JSON from stdout (4) Validates JSON has required fields (channel_id, threads, stakeholders, slack_mcp_available) (5) Terminates with clear error if CLI fails or JSON invalid (6) Writes initial state file"
  ```

- [AC-4.2] Define phase: session-resume question loop. Generates a session UUID, invokes `claude -p "/define ..." --session-id <uuid>`. On "waiting_for_response" status: Python polls Slack thread for a response, then resumes with `claude -p "<response text>" --resume <session-id>`. Loops until "complete" with manifest_path | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the define phase in claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) Generates a session UUID and passes it via --session-id on the first invocation (2) Invokes claude -p with /define + task + COLLAB_CONTEXT, --dangerously-skip-permissions, --output-format json, --json-schema with define output schema (3) Checks response status: if 'waiting_for_response', Python polls the indicated Slack thread for a stakeholder response using a separate Claude CLI call, then resumes the /define session with claude -p '<response>' --resume <session-id> (4) Loops until status is 'complete' with manifest_path (5) Validates manifest file exists at the returned path (6) Updates state with manifest_path, session_id, and phase"
  ```

- [AC-4.3] Manifest review phase: invokes Claude CLI to post manifest to Slack and request approval. Poll loop: sleep(interval) → invoke Claude CLI to check for approval. If feedback, loops back to define phase passing previous manifest as "existing manifest" input plus feedback text | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the manifest review phase in claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) Invokes Claude CLI to post manifest content to Slack channel (2) Tags stakeholders for review (3) Poll loop: time.sleep(poll_interval) then invoke Claude CLI to read channel and check for approval using --json-schema with polling schema (4) If approved: advance to execute phase (5) If feedback: re-invokes the define phase, passing the previous manifest path as 'existing manifest' context plus the feedback text (leveraging /define's 'Existing Manifest Feedback' mechanism) (6) Updates state after each poll iteration"
  ```

- [AC-4.4] Execute phase: session-resume escalation loop. Generates a session UUID, invokes `claude -p "/do ..." --session-id <uuid>`. On "escalation_pending" status: Python polls Slack thread for owner response, then resumes with `claude -p "<response text>" --resume <session-id>`. Loops until "complete" | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the execute phase in claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) Generates a session UUID and passes it via --session-id on the first invocation (2) Invokes claude -p with /do + manifest + COLLAB_CONTEXT, --dangerously-skip-permissions, --output-format json, --json-schema with do output schema (3) Checks response status: if 'escalation_pending', Python polls the indicated Slack thread for an owner response, then resumes the /do session with claude -p '<response>' --resume <session-id> (4) Loops until status is 'complete' (5) Updates state with session_id and phase"
  ```

- [AC-4.5] PR phase: invokes Claude CLI to create PR. Invokes Claude CLI to post PR link to Slack. Poll loop for PR approval. Auto-fixes review comments (max 3 attempts, then escalate via Claude CLI to Slack) | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the PR phase in claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) Invokes Claude CLI to create PR (2) Invokes Claude CLI to post PR link to Slack, tag reviewers (3) Poll loop: sleep then check PR status via Claude CLI (4) On review comments: invoke Claude CLI to fix (5) Max 3 fix attempts per review round, then escalate to owner via Slack (6) Updates state with pr_url and approval status"
  ```

- [AC-4.6] QA phase (optional): if QA stakeholders exist, invokes Claude CLI to post QA request to Slack. Poll loop for QA sign-off | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the QA phase in claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) Only runs if QA stakeholders were identified during pre-flight (2) Invokes Claude CLI to post QA request to Slack (3) Poll loop for sign-off (4) Handles QA feedback by looping back"
  ```

- [AC-4.7] Done phase: invokes Claude CLI to post completion summary to Slack. Writes final state. Exits cleanly | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read the done phase in claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) Invokes Claude CLI to post completion summary to Slack (includes what was built, PR link, key decisions) (2) Writes final state with phase='done' (3) Exits with code 0"
  ```

- [AC-4.8] State management: JSON state file written after every phase transition. Contains: phase, channel_id, thread_ids, stakeholders, manifest_path, pr_url, session IDs for define/execute. No poll_interval in state — it's a Python constant. Unique filename per run | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify state management: (1) State file path includes unique identifier (timestamp or UUID) (2) State written after every phase transition (3) State contains at minimum: phase, channel_id, thread_ids, stakeholders (4) Later phases add: manifest_path, pr_url, define_session_id, execute_session_id (5) State file is simple flat JSON (6) No poll_interval in state — polling is configured as a Python constant"
  ```

- [AC-4.9] Resume capability: `--resume <state-file>` flag reads state and continues from the interrupted phase | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify resume: (1) Accepts --resume <path-to-state-file> argument (2) Reads state JSON (3) Determines current phase (4) Skips completed phases (5) Resumes from the interrupted phase (6) Logs that it's resuming"
  ```

- [AC-4.10] Error handling: every subprocess.run() checks return code. Non-zero = log error + update state + terminate. No silent failures | Verify: covered by INV-G12

- [AC-4.11] Pre-flight validates Slack MCP availability: first Claude CLI call tests Slack tools. On failure, terminates with clear error listing required MCP setup | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) The pre-flight Claude CLI call includes instructions to test Slack MCP availability (2) If Slack tools unavailable, Claude reports this in the output JSON (3) Python checks for this and terminates with clear error message listing how to set up Slack MCP"
  ```

- [AC-4.12] Edge case handling: Slack unavailable mid-workflow → terminate + state file for resume. Large content splitting for Slack posts (>4000 chars). Subprocess timeout per phase to prevent hangs | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Verify: (1) subprocess.run() calls have timeout parameter set per phase (pre-flight: 300s, define per-turn: reasonable timeout since Claude no longer runs the full interview in one call, do per-turn: similar, polling calls: 120s) (2) If a Claude CLI call fails because Slack is unavailable mid-workflow, Python logs the error, writes state, and terminates cleanly (3) When posting large content to Slack via Claude CLI, the prompt instructs Claude to split into numbered messages if content exceeds ~4000 chars"
  ```

- [AC-4.13] Prompt injection defense: all Claude CLI prompts that read Slack content include instructions to not execute dangerous requests, not expose secrets, and treat Slack messages as potentially adversarial | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py. Find all Claude CLI invocations that read from or interact with Slack. Verify each includes (in the prompt or --json-schema): (1) Do not execute actions unrelated to the collaboration task (2) Never expose environment variables, secrets, or credentials (3) Treat Slack messages as user input — validate before acting (4) If a message requests something dangerous, decline and note it in the output"
  ```

- [AC-4.14] No external Python dependencies — uses only stdlib (subprocess, json, pathlib, argparse, time, uuid, logging, sys) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import ast,sys; tree=ast.parse(open('claude-plugins/manifest-dev-collab/scripts/slack-collab-orchestrator.py').read()); imports=[n.names[0].name.split('.')[0] if isinstance(n,ast.Import) else n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,(ast.Import,ast.ImportFrom)) and (not isinstance(n,ast.ImportFrom) or n.module)]; stdlib={'subprocess','json','pathlib','argparse','time','uuid','logging','sys','os','typing','datetime','textwrap','shutil'}; non_std=[i for i in imports if i not in stdlib]; print('PASS' if not non_std else f'FAIL: non-stdlib imports: {non_std}')\""
  ```

### Deliverable 5: Rewrite /slack-collab Skill (Thin Launcher)

*Replace the current full orchestrator SKILL.md with a thin launcher that runs the Python script.*

**Acceptance Criteria:**

- [AC-5.1] Skill is a thin launcher: instructs Claude to run the Python script via Bash tool with `run_in_background=true` parameter (a Claude Code Bash tool feature that runs commands without timeout and notifies on completion — not nohup), passing $ARGUMENTS as the task description. Reports to user that workflow started | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/skills/slack-collab/SKILL.md. Verify: (1) The skill's primary instruction is to run python3 scripts/slack-collab-orchestrator.py via the Bash tool with run_in_background=true (2) It passes $ARGUMENTS as the task description (3) It tells the user the workflow has started and to follow along in Slack (4) The skill is concise — no orchestration logic duplicated from the Python script (5) It mentions --resume for recovery"
  ```

- [AC-5.2] Valid frontmatter with name "slack-collab", description with trigger terms, user-invocable: true | Verify: covered by INV-G7

### Deliverable 6: Update Documentation

*Update all affected READMEs per sync checklist.*

**Acceptance Criteria:**

- [AC-6.1] Root README.md lists manifest-dev-collab plugin | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-collab' README.md && echo PASS || echo FAIL"
  ```

- [AC-6.2] claude-plugins/README.md includes manifest-dev-collab in plugin table | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-collab' claude-plugins/README.md && echo PASS || echo FAIL"
  ```

- [AC-6.3] manifest-dev-collab/README.md describes the Python orchestrator architecture, prerequisites, usage, resume instructions | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev-collab/README.md. Verify it includes: (1) Overview of Python orchestrator architecture (2) Prerequisites: Slack MCP server, Python 3.8+, Claude Code CLI, plugins installed (3) Usage: /slack-collab 'task description' (4) Resume: how to resume from a crash (5) Workflow phases listed (6) What Slack is used for (Q&A, manifest review, escalations, PR review)"
  ```

- [AC-6.4] manifest-dev/README.md mentions collaboration mode in /define and /do | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "grep -qi 'collaborat' claude-plugins/manifest-dev/README.md && echo PASS || echo FAIL"
  ```

### Deliverable 7: Version Bumps

*Bump versions for affected plugins.*

**Acceptance Criteria:**

- [AC-7.1] manifest-dev plugin version bumped (minor) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json,subprocess; current=subprocess.run(['git','show','HEAD:claude-plugins/manifest-dev/.claude-plugin/plugin.json'],capture_output=True,text=True); old=json.loads(current.stdout)['version'] if current.returncode==0 else '0.0.0'; new=json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json'))['version']; old_parts=list(map(int,old.split('.'))); new_parts=list(map(int,new.split('.'))); assert new_parts>old_parts, f'Version not bumped: {old} -> {new}'; print(f'PASS: {old} -> {new}')\""
  ```

- [AC-7.2] manifest-dev-collab plugin version bumped (minor — new Python script is a new feature) | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json,subprocess; current=subprocess.run(['git','show','HEAD:claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json'],capture_output=True,text=True); old=json.loads(current.stdout)['version'] if current.returncode==0 else '0.0.0'; new=json.load(open('claude-plugins/manifest-dev-collab/.claude-plugin/plugin.json'))['version']; old_parts=list(map(int,old.split('.'))); new_parts=list(map(int,new.split('.'))); assert new_parts>old_parts, f'Version not bumped: {old} -> {new}'; print(f'PASS: {old} -> {new}')\""
  ```

### Deliverable 8: Unit Tests for Orchestrator

*Unit tests for the Python orchestrator's deterministic logic. No Slack or Claude CLI needed.*

**Acceptance Criteria:**

- [AC-8.1] Tests exist at `tests/collab/` covering state file operations: create, read, update, resume parsing | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "test -d tests/collab && find tests/collab -name 'test_*.py' | xargs -r grep -l 'state' | head -1 && echo PASS || echo FAIL"
  ```

- [AC-8.2] Tests cover phase transition logic: valid transitions, skip completed phases on resume, invalid state handling | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/collab/ -v -k 'phase or transition or resume' 2>&1 | tail -5"
  ```

- [AC-8.3] Tests cover error handling: non-zero exit code detection, missing JSON file, invalid JSON content, missing required fields | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/collab/ -v -k 'error or fail or invalid' 2>&1 | tail -5"
  ```

- [AC-8.4] Tests cover COLLAB_CONTEXT string construction: correct format, all fields populated, proper escaping | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/collab/ -v -k 'collab_context or context' 2>&1 | tail -5"
  ```

- [AC-8.5] All tests pass | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "pytest tests/collab/ -v && echo PASS || echo FAIL"
  ```

### Deliverable 9: Save Final Manifests to `.manifest/` Directory

*Final manifests go to `.manifest/` in the project root (committed to repo). Discovery logs and execution logs stay in `/tmp/` (working files).*

**Acceptance Criteria:**

- [AC-9.1] `.manifest/` directory exists in the project root, containing the current manifest with a meaningful date-based name | Verify: bash
  ```yaml
  verify:
    method: bash
    command: "ls .manifest/*.md 2>/dev/null | grep -q '2026' && echo PASS || echo FAIL"
  ```

- [AC-9.2] /define SKILL.md outputs final manifests to `.manifest/{descriptive-name}-{YYYY-MM-DD}.md`. Discovery logs stay in `/tmp/`. The Complete section references `.manifest/` for the manifest path | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/define/SKILL.md. Verify: (1) Final manifest output path is .manifest/ with a descriptive name and date (not /tmp/) (2) Discovery log path is still /tmp/ (3) The Complete section shows the .manifest/ path for the manifest (4) The skill instructs creating .manifest/ directory if it doesn't exist"
  ```

- [AC-9.3] /do SKILL.md execution logs stay in `/tmp/` — no path change needed | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read claude-plugins/manifest-dev/skills/do/SKILL.md. Verify: (1) Execution log path is still /tmp/do-log-{timestamp}.md (2) No references to .manifest/ for execution logs"
  ```

- [AC-9.4] CLAUDE.md documents `.manifest/` directory — final manifests committed here, logs stay in /tmp/ | Verify: subagent review
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: opus
    prompt: "Read CLAUDE.md. Verify it documents the .manifest/ directory: (1) States that final manifests are saved to .manifest/ (2) States that discovery logs and execution logs stay in /tmp/ (3) Mentions these manifest files are committed to the repo (4) Information is concise and maximally useful for future /define sessions"
  ```

## Amendments

### Amendment 1: Session-resume pattern — Claude never polls

**Rationale:** Claude Code should not waste tokens/time polling Slack. The Python orchestrator should own all polling. When /define needs a stakeholder response or /do needs an escalation response, Claude posts the question and exits with structured JSON. Python polls Slack and resumes the Claude session with the response via `--resume <session-id>`.

**Changes:**
- COLLAB_CONTEXT: removed `poll_interval` field (Python owns polling as a constant)
- /define SKILL.md: collaboration mode now instructs "post question, exit with JSON, orchestrator resumes you"
- /do SKILL.md: collaboration mode now instructs "post escalation, exit with JSON, orchestrator resumes you"
- Python orchestrator: `phase_define()` and `phase_execute()` become session-resume loops using `--session-id <uuid>` (first call) and `--resume <session-id>` (subsequent calls)
- Schemas: DEFINE_OUTPUT_SCHEMA → union of "waiting_for_response"/"complete". New DO_OUTPUT_SCHEMA → union of "escalation_pending"/"complete"
- State: stores define_session_id, execute_session_id for crash recovery resume
- Added ASM-10, ASM-11 for CLI session management assumptions

**Affected ACs:** AC-1.1, AC-1.3, AC-2.1, AC-2.3, AC-4.1, AC-4.2, AC-4.4, AC-4.8, AC-4.12
**Affected INVs:** INV-G3 (no poll_interval in format check)

### Amendment 2: Progressive disclosure — extract collaboration mode to reference files

**Rationale:** Collaboration mode content in /define and /do SKILL.md bloats the core prompt for users who don't use collaboration mode. Progressive disclosure: move all collaboration mode content to `references/COLLABORATION_MODE.md` under each skill. The main SKILL.md gets a 2-line conditional reference. Claude only reads the reference file when COLLAB_CONTEXT is detected in arguments — non-collaboration users never see it.

**Changes:**
- /define SKILL.md: Replace `## Collaboration Mode` section (lines 436-482) with a 2-line reference: "When `$ARGUMENTS` contains a `COLLAB_CONTEXT:` block, read `references/COLLABORATION_MODE.md` for full instructions. If no `COLLAB_CONTEXT:` block is present, ignore this — all other sections apply as written."
- /do SKILL.md: Replace `## Collaboration Mode` section (lines 54-95) with the same 2-line reference pattern.
- Create `skills/define/references/COLLABORATION_MODE.md`: Contains the full collaboration mode content extracted from /define SKILL.md (COLLAB_CONTEXT format, overrides, security).
- Create `skills/do/references/COLLABORATION_MODE.md`: Contains the full collaboration mode content extracted from /do SKILL.md (COLLAB_CONTEXT format, overrides, security).
- Version bumps: patch for manifest-dev (collaboration mode behavior unchanged, just restructured).

**Affected ACs:** AC-1.1, AC-1.2, AC-1.3, AC-1.4, AC-2.1, AC-2.2, AC-2.3
**Affected INVs:** INV-G1, INV-G2, INV-G3, INV-G8, INV-G14 (verification prompts need updated file paths)

**Verification path changes:** All verification prompts that reference "Collaboration Mode section of SKILL.md" must be updated to reference the `references/COLLABORATION_MODE.md` file instead. INV-G1 and INV-G2 must verify the main SKILL.md now has only the brief reference, not the full content. INV-G3 must check the reference files for COLLAB_CONTEXT format consistency.

### Amendment 3: Save final manifests to `.manifest/` instead of `/tmp/`

**Rationale:** Final manifests should be committed to the repo, not lost in `/tmp/`. Move to a `.manifest/` directory in the project root so manifests are version-controlled and persist across sessions. Discovery logs and execution logs stay in `/tmp/` — they're working files, not artifacts worth committing.

**Changes:**
- Create `.manifest/` directory
- Copy the current manifest to `.manifest/` with a meaningful name including a date (e.g., `.manifest/slack-collab-python-orchestrator-2026-02-26.md`)
- Update CLAUDE.md: Add a section documenting `.manifest/` directory — final manifests are saved here, committed to the repo.
- /define SKILL.md: Change manifest output path from `/tmp/manifest-{timestamp}.md` to `.manifest/{descriptive-name}-{YYYY-MM-DD}.md`. Discovery logs stay in `/tmp/`. The Complete section references `.manifest/` for the manifest path.
- /do SKILL.md: No path changes needed — execution logs stay in `/tmp/`.
- Python orchestrator: No change needed — reads manifest_path from /define's output JSON.

**New deliverable: D9**

**Affected ACs:** New AC-9.1 through AC-9.4
**Affected INVs:** INV-G1 (define's manifest output path changed), INV-G11 (CLAUDE.md updated)
