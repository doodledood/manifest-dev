# Definition: Platform-Agnostic Collaboration Orchestration

## 1. Intent & Context
- **Goal:** Transform the hardcoded Slack+GitHub collaboration plugin (`manifest-dev-collab`) into a platform-agnostic orchestration plugin (`manifest-dev-orchestrate`) that supports any messaging medium (Slack, local/terminal, user-defined custom) and any review platform (GitHub, none, future others), with sensible defaults and independent configuration.
- **Mental Model:** The lead skill becomes an intent-based orchestrator that doesn't know or care about specific platforms. It sends high-level intent ("update stakeholders on Phase 2") and delegates platform-native translation to pluggable coordinators. Workers (define-worker, executor) are completely medium-blind — they message the lead, period. Local mode has no coordinator at all; the lead uses AskUserQuestion directly. The orchestration backend (currently Agent Teams) is referenced abstractly to prepare for future CMUX support.
- **Mode:** thorough

## 2. Approach

- **Architecture:**
  - `cp -r claude-plugins/manifest-dev-collab claude-plugins/manifest-dev-orchestrate` as starting point
  - Lead skill (`/orchestrate`) replaces `/slack-collab` — platform-agnostic, intent-based
  - Static medium mapping table: `slack` → slack-coordinator, `local` → no coordinator, `custom` → LLM-generated coordinator from `--medium-details`
  - Independent flags: `--medium <type>`, `--review-platform <type>`, `--medium-details "..."`, `--review-platform-details "..."`
  - Defaults: `--medium local` + `--review-platform github`
  - Workers are medium-blind: TEAM_CONTEXT `coordinator` field removed or made optional/internal
  - Orchestration ops abstracted: "spawn teammate", "message teammate" instead of TeamCreate/SendMessage
  - COLLABORATION_MODE.md files in manifest-dev core updated to remove Slack-specific references

- **Execution Order:**
  - D1 (Plugin scaffold) → D2 (Lead skill) → D3 (Agents) → D4 (COLLABORATION_MODE.md) → D5 (State schema) → D6 (Plugin registry + READMEs)
  - Rationale: Scaffold first (cp), then the core lead skill drives all other changes, agents adapt to the new lead, COLLABORATION_MODE depends on new TEAM_CONTEXT, state depends on all above, docs last.

- **Risk Areas:**
  - [R-1] Scope creep beyond abstraction+local | Detect: any work on Telegram/Discord coordinators, CMUX adapter code, or new features not in this manifest
  - [R-2] Regression in Slack mode behavior | Detect: prompt-reviewer or manual comparison shows missing phases/flow logic when --medium slack
  - [R-3] Orphaned cross-references | Detect: grep for "slack-collab" in new plugin files, grep for hardcoded "slack-coordinator" in lead skill or workers

- **Trade-offs:**
  - [T-1] Flexibility vs Simplicity → Prefer flexibility. Accept more complex lead skill for multi-medium support.
  - [T-2] Intent-based vs Interface-based coordination → Prefer intent-based. Lead sends natural language intent, coordinators translate. More LLM-native, less rigid.
  - [T-3] Brevity vs Explicitness in lead skill → Prefer explicitness. Medium-switching logic must be unambiguous.

## 3. Global Invariants (The Constitution)

- [INV-G1] No MEDIUM+ issues from prompt-reviewer on all changed skill and agent prompt files
  ```yaml
  verify:
    method: subagent
    agent: prompt-reviewer
    model: inherit
    prompt: "Review all changed .md files in claude-plugins/manifest-dev-orchestrate/ for prompt quality issues"
  ```

- [INV-G2] No MEDIUM+ issues from docs-reviewer — all READMEs synced with new plugin name, skill name, and component lists
  ```yaml
  verify:
    method: subagent
    agent: docs-reviewer
    model: inherit
    prompt: "Check README.md (root), claude-plugins/README.md, and claude-plugins/manifest-dev-orchestrate/README.md for accuracy against the new plugin structure"
  ```

- [INV-G3] No MEDIUM+ issues from context-file-adherence-reviewer — CLAUDE.md compliance (kebab-case, version bumps, README sync checklist)
  ```yaml
  verify:
    method: subagent
    agent: context-file-adherence-reviewer
    model: inherit
    prompt: "Check all changes in claude-plugins/manifest-dev-orchestrate/ against CLAUDE.md rules"
  ```

- [INV-G4] No residual "slack-collab" references in the new plugin (except historical context or comparison notes)
  ```yaml
  verify:
    method: bash
    command: "! grep -r 'slack-collab' claude-plugins/manifest-dev-orchestrate/ --include='*.md' --include='*.json' | grep -v 'was slack-collab' | grep -v 'formerly' | grep -v 'replaced' | grep -q ."
  ```

- [INV-G5] Workers (manifest-define-worker, manifest-executor) contain NO medium-specific references — they are medium-blind
  ```yaml
  verify:
    method: bash
    command: "! grep -iE '(slack|telegram|discord|github-coordinator|review.platform)' claude-plugins/manifest-dev-orchestrate/agents/manifest-define-worker.md claude-plugins/manifest-dev-orchestrate/agents/manifest-executor.md | grep -v 'medium-blind' | grep -v 'agnostic' | grep -q ."
  ```

- [INV-G6] Scope guard — no Telegram/Discord coordinator implementations, no CMUX adapter code, no new coordinator agent files beyond what was copied from manifest-dev-collab
  ```yaml
  verify:
    method: bash
    command: "SCOPE_FAIL=0; if ls claude-plugins/manifest-dev-orchestrate/agents/ | grep -iE '(telegram|discord|cmux)'; then echo 'FAIL: out-of-scope coordinator found'; SCOPE_FAIL=1; fi; DIFF=$(diff <(ls claude-plugins/manifest-dev-collab/agents/ | sort) <(ls claude-plugins/manifest-dev-orchestrate/agents/ | sort)); if [ -n \"$DIFF\" ]; then echo \"FAIL: agent file mismatch:\"; echo \"$DIFF\"; SCOPE_FAIL=1; fi; [ $SCOPE_FAIL -eq 0 ] && echo 'PASS'"
  ```

- [INV-G7] `--medium-details` content is treated as configuration context only, never executed or passed to tools as commands
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify that --medium-details values are described as configuration context for coordinator prompts, not as executable content. The skill must NOT instruct the lead to execute, eval, or pass medium-details to shell commands."
  ```

- [INV-G8] Existing manifest-dev-collab plugin is completely untouched (no modifications to any file)
  ```yaml
  verify:
    method: bash
    command: "test -z \"$(git diff --name-only HEAD -- claude-plugins/manifest-dev-collab/)\" && echo 'PASS: collab untouched' || echo 'FAIL: collab files modified'"
  ```

- [INV-G9] Requirements traceability — every specified requirement (medium abstraction, review platform abstraction, local mode, dynamic mediums, orchestration abstraction, independent flags, defaults) maps to implementation in the lead skill
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify these requirements are implemented: (1) --medium flag with local|slack|custom values, (2) --review-platform flag with github|none|custom values, (3) --medium-details and --review-platform-details for custom configs, (4) defaults: medium=local, review-platform=github, (5) static medium mapping table, (6) local mode uses AskUserQuestion directly with no coordinator, (7) abstract orchestration ops (no direct TeamCreate/SendMessage references — uses intent-based language like 'spawn teammate', 'message teammate'), (8) intent-based coordination (lead sends intent, not verbatim messages)"
  ```

- [INV-G10] Behavior completeness — all use cases implemented (local solo, Slack team, custom medium, mixed modes like local+github, slack+no-review)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify these use cases are covered: (1) '/orchestrate task' — local+github default, (2) '/orchestrate task --medium slack --channel #dev' — Slack mode, (3) '/orchestrate task --medium custom --medium-details \"We use Mattermost\"' — dynamic medium, (4) '/orchestrate task --medium slack --review-platform none' — Slack without review, (5) '/orchestrate task --review-platform custom --review-platform-details \"GitLab at gitlab.example.com\"' — custom review platform, (6) resume with --resume preserving medium config"
  ```

- [INV-G11] Error experience — invalid flag values, missing required details for custom mediums, and incompatible combinations produce clear error messages
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify error handling for: (1) --medium custom without --medium-details, (2) --review-platform custom without --review-platform-details, (3) invalid --medium value not in mapping table (should suggest valid options or explain custom), (4) --medium slack without required Slack prerequisites"
  ```

## 4. Process Guidance (Non-Verifiable)

- [PG-1] Document load-bearing assumptions — identify what must remain true for each medium mode to work (e.g., Agent Teams availability, Slack MCP server configured, gh CLI authenticated)
- [PG-2] Verification plan — Slack mode behavior preserved by structural comparison with original /slack-collab skill; local mode verified by walkthrough
- [PG-3] Identify consumers — COLLABORATION_MODE.md files in manifest-dev core plugin are the primary consumers of TEAM_CONTEXT format changes; dist/ copies are secondary consumers
- [PG-4] Assess test coverage — hooks in manifest-dev have tests; new plugin has no hooks so no test gap. Prompt quality covered by prompt-reviewer gate.

## 5. Known Assumptions

- [ASM-1] Agent Teams API (TeamCreate, SendMessage) is available and works identically regardless of what coordinator agents are spawned | Default: true | Impact if wrong: orchestration backend abstraction would need immediate concrete adapter
- [ASM-2] The Slack coordinator agent file can be copied as-is into the new plugin without functional changes | Default: true | Impact if wrong: coordinator needs adaptation to work with the new lead skill's intent-based messages (though lead's Slack-specific instructions should handle this)
- [ASM-3] ~~No other plugins or tools reference `manifest-dev-collab` or `slack-collab` by name in a way that would break~~ **RESOLVED**: Grep confirmed cross-references exist in README.md, claude-plugins/README.md, .claude-plugin/marketplace.json, sync-tools/SKILL.md, and .manifest/slack-collab-full-spec.md. All are valid because the old plugin is preserved (INV-G8). No references break.
- [ASM-4] CMUX support is future-only — abstracting orchestration ops in the lead skill prompt is sufficient preparation | Default: true | Impact if wrong: would need concrete adapter pattern now

## 6. Deliverables (The Work)

### Deliverable 1: Plugin Scaffold
*Create new plugin directory by copying manifest-dev-collab*

**Acceptance Criteria:**
- [AC-1.1] `claude-plugins/manifest-dev-orchestrate/` exists with expected post-modification structure (plugin.json, agents/, skills/orchestrate/, README.md)
  ```yaml
  verify:
    method: bash
    command: "test -d claude-plugins/manifest-dev-orchestrate && test -f claude-plugins/manifest-dev-orchestrate/.claude-plugin/plugin.json && test -d claude-plugins/manifest-dev-orchestrate/agents && test -d claude-plugins/manifest-dev-orchestrate/skills/orchestrate && test -f claude-plugins/manifest-dev-orchestrate/README.md && echo 'PASS' || echo 'FAIL: missing expected structure'"
  ```

- [AC-1.2] `plugin.json` updated: name → `manifest-dev-orchestrate`, version reset to `1.0.0`, description updated to reflect platform-agnostic orchestration
  ```yaml
  verify:
    method: bash
    command: "cat claude-plugins/manifest-dev-orchestrate/.claude-plugin/plugin.json | python3 -c \"import sys,json; d=json.load(sys.stdin); assert 'orchestrate' in d.get('name','').lower(), f'name: {d.get(\\\"name\\\")}'; assert d.get('version','') == '1.0.0', f'version: {d.get(\\\"version\\\")}'; print('PASS')\""
  ```

- [AC-1.3] Plugin registered in `.claude-plugin/marketplace.json` alongside existing entries
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('.claude-plugin/marketplace.json')); names=[p.get('name','') for p in d.get('plugins',[])]; assert 'manifest-dev-orchestrate' in names, f'not found in {names}'; print('PASS')\""
  ```

### Deliverable 2: Lead Skill — /orchestrate
*Platform-agnostic lead orchestrator replacing /slack-collab*

**Acceptance Criteria:**
- [AC-2.1] Skill file at `skills/orchestrate/SKILL.md` with correct frontmatter (name: orchestrate, description reflecting platform-agnostic orchestration)
  ```yaml
  verify:
    method: bash
    command: "head -10 claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md | grep -q 'name: orchestrate' && echo 'PASS' || echo 'FAIL: missing name: orchestrate in frontmatter'"
  ```

- [AC-2.2] CLI flag parsing: `--medium`, `--review-platform`, `--medium-details`, `--review-platform-details`, `--interview`, `--mode`, `--resume` all documented and handled
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify all these flags are documented with parsing instructions: --medium, --review-platform, --medium-details, --review-platform-details, --interview, --mode, --resume. Each must have valid values listed and default behavior specified."
  ```

- [AC-2.3] Static medium mapping table present: `local` → no coordinator (AskUserQuestion), `slack` → slack-coordinator agent, `custom` → LLM-adaptive from --medium-details
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify a medium mapping table exists with at least: local (no coordinator, AskUserQuestion), slack (slack-coordinator agent), custom (LLM-generated coordinator from --medium-details). Table must be clearly structured."
  ```

- [AC-2.4] Review platform mapping: `github` → github-coordinator agent, `none` → skip review phases, `custom` → LLM-adaptive from --review-platform-details
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify review platform mapping with: github (github-coordinator), none (skip review/PR phases), custom (LLM-generated from --review-platform-details)."
  ```

- [AC-2.5] Default behavior: no flags → `--medium local --review-platform github` (solo mode with GitHub review)
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify defaults are explicitly stated: medium defaults to 'local', review-platform defaults to 'github'."
  ```

- [AC-2.6] Local mode section: lead uses AskUserQuestion directly for all stakeholder Q&A, no messaging coordinator spawned, synchronous flow
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify local mode is documented: (1) no messaging coordinator spawned, (2) lead uses AskUserQuestion directly, (3) synchronous flow, (4) all phases still execute but interaction is local."
  ```

- [AC-2.7] Intent-based coordination: lead sends high-level intent to coordinators, not verbatim messages. Coordinators translate to platform-native patterns.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify intent-based coordination: (1) lead sends intent descriptions not verbatim messages, (2) coordinator translates intent to platform-native action, (3) no Slack-specific terminology in the generic orchestration logic (threading, channel, thread_ts etc. should only appear in Slack-specific sections)."
  ```

- [AC-2.8] Abstract orchestration ops: no direct TeamCreate/SendMessage tool references in generic flow. Uses intent-based language ("spawn teammate", "message teammate") with a note that Agent Teams is the default backend.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify: (1) generic orchestration sections use abstract language like 'spawn teammate', 'message teammate' instead of 'TeamCreate', 'SendMessage', (2) Agent Teams is documented as the default orchestration backend, (3) there is a note about future CMUX support or similar."
  ```

- [AC-2.9] Phase flow preserved: all 7 phases (Preflight, Define, Manifest Review, Execute, PR Review, QA, Done) present and functional, adapted for medium-agnosticism
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify all phases exist: Phase 0 (Preflight), Phase 1 (Define), Phase 2 (Manifest Review), Phase 3 (Execute), Phase 4 (PR Review), Phase 5 (QA), Phase 6 (Done). Each must be adapted for medium-agnosticism (no Slack-specific assumptions in generic flow). Phase 4 must adapt to --review-platform (skip if 'none')."
  ```

- [AC-2.10] Dynamic medium handling: when `--medium custom`, lead generates coordinator behavior from `--medium-details`, spawns an ad-hoc coordinator with LLM-composed instructions
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Verify custom medium handling: (1) --medium custom requires --medium-details, (2) lead generates coordinator instructions from the details description, (3) spawned coordinator follows same hub-and-spoke model, (4) error if --medium-details missing with --medium custom."
  ```

- [AC-2.11] Old `/slack-collab` skill directory removed from new plugin (replaced by `/orchestrate`)
  ```yaml
  verify:
    method: bash
    command: "! test -d claude-plugins/manifest-dev-orchestrate/skills/slack-collab && echo 'PASS: old skill dir removed' || echo 'FAIL: slack-collab dir still exists'"
  ```

### Deliverable 3: Agent Updates
*Update copied agents for the new orchestration model*

**Acceptance Criteria:**
- [AC-3.1] `slack-coordinator.md` — functionally unchanged from original (receives intent from lead, translates to Slack-native actions). Only update: references to "slack-collab" → "orchestrate"
  ```yaml
  verify:
    method: bash
    command: "diff claude-plugins/manifest-dev-collab/agents/slack-coordinator.md claude-plugins/manifest-dev-orchestrate/agents/slack-coordinator.md | head -50"
  ```

- [AC-3.2] `github-coordinator.md` — functionally unchanged. Only update: references to "slack-collab" → "orchestrate"
  ```yaml
  verify:
    method: bash
    command: "diff claude-plugins/manifest-dev-collab/agents/github-coordinator.md claude-plugins/manifest-dev-orchestrate/agents/github-coordinator.md | head -50"
  ```

- [AC-3.3] `manifest-define-worker.md` — medium-blind. No references to Slack, Telegram, Discord, or any specific messaging platform. References lead only.
  ```yaml
  verify:
    method: bash
    command: "! grep -iE '(slack|telegram|discord)' claude-plugins/manifest-dev-orchestrate/agents/manifest-define-worker.md | grep -v 'agnostic' | grep -v 'medium-blind' | grep -q . && echo 'PASS' || echo 'FAIL: medium-specific references found'"
  ```

- [AC-3.4] `manifest-executor.md` — medium-blind. No references to Slack, Telegram, Discord, or any specific messaging platform. References lead only.
  ```yaml
  verify:
    method: bash
    command: "! grep -iE '(slack|telegram|discord)' claude-plugins/manifest-dev-orchestrate/agents/manifest-executor.md | grep -v 'agnostic' | grep -v 'medium-blind' | grep -q . && echo 'PASS' || echo 'FAIL: medium-specific references found'"
  ```

### Deliverable 4: COLLABORATION_MODE.md Updates
*Update the 3 core files + dist copies to be medium-agnostic*

**Acceptance Criteria:**
- [AC-4.1] `skills/define/references/COLLABORATION_MODE.md` — TEAM_CONTEXT `coordinator` field removed or made generic. No Slack-specific references. Worker messages lead only.
  ```yaml
  verify:
    method: bash
    command: "! grep -i 'slack' claude-plugins/manifest-dev/skills/define/references/COLLABORATION_MODE.md | grep -q . && echo 'PASS' || echo 'FAIL: Slack references remain'"
  ```

- [AC-4.2] `skills/do/references/COLLABORATION_MODE.md` — same treatment as AC-4.1
  ```yaml
  verify:
    method: bash
    command: "! grep -i 'slack' claude-plugins/manifest-dev/skills/do/references/COLLABORATION_MODE.md | grep -q . && echo 'PASS' || echo 'FAIL: Slack references remain'"
  ```

- [AC-4.3] `skills/verify/references/COLLABORATION_MODE.md` — same treatment as AC-4.1
  ```yaml
  verify:
    method: bash
    command: "! grep -i 'slack' claude-plugins/manifest-dev/skills/verify/references/COLLABORATION_MODE.md | grep -q . && echo 'PASS' || echo 'FAIL: Slack references remain'"
  ```

- [AC-4.4] All dist/ copies of COLLABORATION_MODE.md updated to match (codex, gemini, opencode)
  ```yaml
  verify:
    method: bash
    command: "for dist in dist/codex dist/gemini dist/opencode; do for skill in define do verify; do if [ -f \"$dist/skills/$skill/references/COLLABORATION_MODE.md\" ]; then grep -il 'slack' \"$dist/skills/$skill/references/COLLABORATION_MODE.md\" 2>/dev/null && echo \"FAIL: $dist/$skill has Slack refs\"; fi; done; done; echo 'CHECK COMPLETE'"
  ```

- [AC-4.5] TEAM_CONTEXT format updated: `coordinator` field either removed or made optional/internal. Workers don't reference it.

- [AC-4.6] `manifest-dev` plugin version bumped (patch) in `claude-plugins/manifest-dev/.claude-plugin/plugin.json` to reflect COLLABORATION_MODE.md changes
  ```yaml
  verify:
    method: bash
    command: "python3 -c \"import json; d=json.load(open('claude-plugins/manifest-dev/.claude-plugin/plugin.json')); v=d['version']; parts=v.split('.'); print('PASS: version ' + v) if int(parts[2]) > 0 or int(parts[1]) > 0 else print('FAIL: version not bumped')\""
  ```
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read all three COLLABORATION_MODE.md files in claude-plugins/manifest-dev/skills/{define,do,verify}/references/. Verify the TEAM_CONTEXT block either (a) has no 'coordinator' field, or (b) 'coordinator' is described as optional/internal. Workers should be instructed to message the lead only, with no awareness of which coordinator exists."
  ```

### Deliverable 5: State Schema Update
*New state file schema supporting medium-agnostic orchestration*

**Acceptance Criteria:**
- [AC-5.1] State schema in lead skill includes `medium` and `review_platform` fields that capture the configured values
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Find the state file JSON schema. Verify it includes: (1) 'medium' field (type + details), (2) 'review_platform' field (type + details). These must persist for --resume."
  ```

- [AC-5.2] State schema uses generic field names: no `channel_id` or `thread_ts` at the top level. Medium-specific state nested under a medium-specific key or abstracted.
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Find the state file JSON schema. Verify: (1) no top-level 'channel_id' field, (2) no top-level 'thread_ts' fields, (3) medium-specific state (channel_id, threads, etc.) is either nested under the medium config or abstracted to generic names."
  ```

- [AC-5.3] Resume works with new schema: `--resume` reads medium config from state file and spawns the right coordinator
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/skills/orchestrate/SKILL.md. Find the Resume section. Verify: (1) resume reads 'medium' and 'review_platform' from state file, (2) spawns the correct coordinator based on stored medium type, (3) handles medium=local correctly on resume (no coordinator)."
  ```

### Deliverable 6: Plugin Registry & Documentation
*Register new plugin and sync all READMEs*

**Acceptance Criteria:**
- [AC-6.1] Root `README.md` updated — mentions manifest-dev-orchestrate in Available Plugins section
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-orchestrate' README.md && echo 'PASS' || echo 'FAIL: not in root README'"
  ```

- [AC-6.2] `claude-plugins/README.md` updated — new plugin in plugin table
  ```yaml
  verify:
    method: bash
    command: "grep -q 'manifest-dev-orchestrate' claude-plugins/README.md && echo 'PASS' || echo 'FAIL: not in plugins README'"
  ```

- [AC-6.3] `claude-plugins/manifest-dev-orchestrate/README.md` — updated to describe platform-agnostic orchestration, lists supported mediums and review platforms, documents CLI flags
  ```yaml
  verify:
    method: subagent
    agent: criteria-checker
    model: inherit
    prompt: "Read claude-plugins/manifest-dev-orchestrate/README.md. Verify: (1) describes platform-agnostic orchestration (not Slack-specific), (2) lists supported mediums (local, slack, custom), (3) lists supported review platforms (github, none, custom), (4) documents CLI flags (--medium, --review-platform, --medium-details, --review-platform-details)."
  ```

## Amendments
*None yet.*
