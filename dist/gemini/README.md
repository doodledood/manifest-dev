# manifest-dev for Gemini CLI

Verification-first manifest workflows adapted for Gemini CLI. Define tasks, execute them, verify acceptance criteria, and complete with confidence.

## What's Included

| Component | Count | Status |
|-----------|-------|--------|
| Skills | 6 | Full compatibility (Agent Skills Open Standard) |
| Agents | 12 | Converted (frontmatter adapted, prompts unchanged) |
| Hooks | 3 | Adapted via Python adapter (gemini_adapter.py) |
| Extension manifest | 1 | gemini-extension.json |

### Skills (copied unchanged)
- **define** — Manifest builder with interview-driven scoping
- **do** — Manifest executor, iterates through deliverables
- **verify** — Spawns parallel verification agents
- **done** — Completion marker with execution summary
- **escalate** — Structured escalation with evidence
- **learn-define-patterns** — Extracts user preference patterns from /define sessions

### Agents (converted frontmatter)
All 12 agents converted with Gemini CLI tool names and required fields. Review agents are read-only verification subagents spawned by `/verify`.

### Hooks (adapted)
- **stop_do_hook** → AfterAgent: Blocks premature stops during /do workflows
- **pretool_verify_hook** → BeforeTool: Adds context reminder before /verify
- **post_compact_hook** → SessionStart: Recovers /do context after compaction

Hooks run through `gemini_adapter.py` which translates between Gemini and Claude Code hook protocols.

## Install / Update

### Everything (one command, no clone needed)
```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash
```

Installs skills, agents, hooks, context file, and extension manifest. Run again to update.

### Skills only
```bash
npx skills add doodledood/manifest-dev --all -a gemini-cli
```

### As Gemini Extension
```bash
gemini extensions install https://github.com/doodledood/manifest-dev/dist/gemini
```

### Required Configuration
Add to your Gemini CLI settings.json:
```json
{
  "experimental": {
    "enableAgents": true
  }
}
```

Merge `hooks/hooks.json` entries into your settings.json hooks section.

## Feature Parity

| Feature | Status | Notes |
|---------|--------|-------|
| Skills (define/do/verify/done/escalate) | Full | Agent Skills Open Standard |
| Verification agents | Full | Frontmatter converted, prompts unchanged |
| Stop enforcement hook | Full | Via AfterAgent + adapter |
| Verify context hook | Full | Via BeforeTool + adapter |
| Post-compact recovery | Full | Via SessionStart + adapter |
| $ARGUMENTS in skills | Missing | Not supported by Gemini CLI |
| SubagentStart/Stop hooks | Missing | No equivalent Gemini events |

## Source

This is a generated distribution from [manifest-dev](https://github.com/doodledood/manifest-dev) for Claude Code. The Claude Code plugin is the source of truth.
