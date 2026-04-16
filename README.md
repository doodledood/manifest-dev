<p align="center">
  <picture>
    <img src="assets/logo.png" alt="Manifest Dev Logo" width="120" style="background: transparent;">
  </picture>
</p>

# Manifest-Driven Development

Stop iterating with the model after implementation. Define what you'd accept, run two commands, ship it.

## Quick Start

```bash
# Claude Code (primary)
/plugin marketplace add doodledood/manifest-dev
/plugin install manifest-dev@manifest-dev-marketplace

# Gemini CLI — everything (skills, agents, hooks)
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash

# OpenCode — everything (skills, agents, commands, plugin)
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash

# Codex CLI — everything (skills, TOML stubs, rules, config)
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash
```

Then use it:
```bash
# Define what to build, then execute
/define <what you want to build>
/do <manifest-path>

# Or go end-to-end autonomously:
/auto <what you want to build>

# Tend a PR through review:
/tend-pr <manifest-path-or-pr-url>

# Optional: figure something out before acting
/figure-out <topic or problem>
```

`/define` interviews you and builds a manifest. `/do` executes it. `/auto` chains both — define autonomously, auto-approve, execute — in a single command. `/figure-out` is optional — a truth-convergent thinking partner for when figuring it out IS the goal, or before `/define` when the problem space is foggy.

Control interview depth with `--interview minimal|autonomous|thorough` (default: thorough). Thorough asks everything. Minimal asks scope and high-impact items. Autonomous builds the manifest without asking, presents it for approval.

If you use zsh and want easy upgrade commands for the non-Claude distributions, add this to `~/.zshrc`:

```zsh
alias upgrade-manifest-dev-codex='curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash'
alias upgrade-manifest-dev-gemini='curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash'
alias upgrade-manifest-dev-opencode='curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash'
alias upgrade-manifest-dev-all='upgrade-manifest-dev-codex && upgrade-manifest-dev-gemini && upgrade-manifest-dev-opencode'
```

Then run `source ~/.zshrc` once. Future updates are just `upgrade-manifest-dev-codex`, `upgrade-manifest-dev-gemini`, `upgrade-manifest-dev-opencode`, or `upgrade-manifest-dev-all` for all three.

Uninstall uses the same entrypoints:

```bash
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/gemini/install.sh | bash -s -- uninstall
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/opencode/install.sh | bash -s -- uninstall
curl -fsSL https://raw.githubusercontent.com/doodledood/manifest-dev/main/dist/codex/install.sh | bash -s -- uninstall
```

## The Mindset Shift

Instead of telling the AI *how* to build something, you tell it what you'd accept.

Say you need a login page. The old way: "use React Hook Form, validate with Zod, show inline errors, disable the button while submitting." You've made every design decision upfront. The manifest way: "invalid credentials show an error without clearing the password field" and "the form can't be submitted twice." You define the bar. The AI picks how to clear it. Automated verification confirms it did.

## How It Works

```mermaid
flowchart TD
    A["/define 'task'"] --> B["Interview"]
    B --> C["Manifest file"]
    C --> D["/do manifest.md"]
    D --> E{"For each Deliverable"}
    E --> F["Satisfy ACs"]
    F --> G["/verify"]
    G -->|failures| H["Fix specific criterion"]
    H --> G
    G -->|all pass| I["/done"]
    E -->|risk detected| J["Consult trade-offs, adjust approach"]
    J -->|ACs achievable| E
    J -->|stuck| K["/escalate"]
```

`/define` interviews you to surface what you actually want. The stuff you'd reject in a PR but wouldn't think to specify upfront. Then `/do` implements toward those acceptance criteria, flexible on *how* but not on *what*.

After each deliverable, `/verify` runs automated checks against every criterion. Failing checks say exactly what's wrong. The AI fixes what failed, only what failed, and the loop continues until everything passes or a blocker needs your attention.

## What Changes

Your first pass lands closer to done. Issues get caught by verification before you see them, and the fix loop handles cleanup without your involvement. Every acceptance criterion has been verified, and you know what was checked.

While one manifest executes, you can define the next. The define phase is where your judgment matters; the do-verify-fix phase runs on its own. Writing acceptance criteria also forces you to stay engaged with your own code, which matters when heavy AI usage starts making your codebase feel foreign.

Resist the urge to intervene during `/do`. It won't nail everything on the first pass. That's expected. You invested in define; let the loop run.

## Who This Is For

If you've burned out on the weekly "game-changing AI coding tool" cycle and just want something that works, this is for you. Experienced developers who care more about output quality than execution speed. People who've learned the hard way that AI-generated code needs guardrails more than cheerleading.

We build around how LLMs actually work, not how we wish they worked. That means investing upfront for better results, not optimizing for token cost or raw speed. If you're counting every cent per token or want the fastest possible output regardless of quality, this probably isn't your thing.

---

Everything below is reference. You don't need any of it to get started.

---

## Going Deeper

<details>
<summary><strong>The problem this solves</strong></summary>

You plan a feature with the agent. It implements. The code looks reasonable. Then you review it and half the things aren't how you'd want them: wrong error handling patterns, conventions ignored, edge cases skipped. You send it back. It fixes some things, breaks others. Two or three rounds later you're satisfied, but you've spent more time reviewing and iterating than you saved.

The models can code. But we're throwing them into deep water without defining what "done" actually means. So the review-iterate loop eats the productivity gains.

Manifest-dev front-loads that review energy into `/define`. You spell out acceptance criteria and invariants before implementation starts. The do phase becomes mechanical, and the output lands closer to what you'd accept as a reviewer.

</details>

<details>
<summary><strong>Why this works (LLM first principles)</strong></summary>

LLMs are goal-oriented pattern matchers trained through reinforcement learning, not general reasoners. Clear acceptance criteria play to that strength. Rigid step-by-step plans fall apart because neither you nor the model can predict every detail upfront. Acceptance criteria focus on outcomes and leave implementation open.

There's also the drift problem. Long sessions cause the model to lose track of earlier instructions. The manifest compensates with external state and verification that catches drift before it ships. And since LLMs can't express genuine uncertainty (they'll confidently produce broken code), the verify-fix loop doesn't rely on the AI knowing it failed. It relies on automated checks catching failures.

These are design constraints, and the workflow treats them that way.

</details>

<details>
<summary><strong>Process Guidance and Approach</strong></summary>

The manifest also supports Process Guidance and an initial Approach (architecture, execution order). These are exactly what they sound like: recommendations, not requirements. Hints to help the model make better decisions while it's still not AGI. The acceptance criteria are the contract; the guidance is optimization on top.

This is spec-driven development adapted for LLM execution. The manifest is a spec, but ephemeral: it drives one task, then the code is the source of truth. No spec maintenance. No drift.

</details>

<details>
<summary><strong>Execution Modes</strong></summary>

`/do` supports `--mode efficient|balanced|thorough` to control verification intensity. Default is `thorough` (current behavior). Only pass `--mode` when you explicitly want to trade verification depth for quota savings.

| Mode | What changes | When to use |
|------|-------------|-------------|
| **thorough** (default) | Full verification: all quality gates, all models inherit from session, unlimited parallelism and fix loops | Most tasks. Don't change unless you have a reason. |
| **balanced** | Same models, but limits parallelism (max 4 concurrent verifiers) and fix loops (max 2) | Long-running tasks where you want to limit concurrent quota burn |
| **efficient** | Uses haiku for criteria-checker, skips quality gate reviewers, sequential verification, max 1 fix loop | Quick iterations where speed matters more than verification depth |

Set per-execution: `/do manifest.md --mode balanced`
Set in manifest: add `mode: balanced` to the Intent & Context section.

</details>

### Best Practice: One Manifest Per PR/Branch (or PR Set), Feedback Through It

The manifest is the canonical source of truth for the PR/branch — or, in multi-repo cases, the entire PR set / branch set. Not for a single task. Feedback flows through it: when something's off mid-`/do`, mid-`/verify`, or after `/done` (a missed edge case, a reviewer comment, a bug you didn't anticipate), just send the feedback in your active session. The system routes it through Self-Amendment automatically: `/escalate` → `/define --amend --from-do` → `/do` resumes with the updated manifest. No manual session-switching for the common case. Pure questions about the manifest are answered inline; everything else amends.

**Multi-repo:** by default — and recommended — a single manifest covers the whole multi-repo changeset (Intent declares `Repos:`, deliverables tag `repo:`). `/do` navigates absolute paths from the map natively — no filter logic. `/tend-pr` and `/drive` run per-repo against the shared canonical `/tmp` manifest. Cross-repo gates the user explicitly triggers (e.g., post-deploy verification across services) use `method: deferred-auto` + `/verify --deferred`. Splitting into independent per-repo manifests is also fine when the work is loosely coupled and you prefer to carry cross-PR coherence yourself. See `claude-plugins/manifest-dev/skills/define/references/MULTI_REPO.md` for the full convention.

After `/done`, the same default applies — the post-completion re-entry runs `/define --amend <manifest>` interactively (so you can shape the change), then `/do --scope <new-or-affected-deliverables>`. /done is unreachable until the full verification suite passes again.

**Two-session pattern is still useful** when you want to draft the next manifest while one is executing — `/define` in one session, watch `/do` in another. But you no longer have to ferry feedback manually between them; the autonomous Self-Amendment flow handles that within a single session.

**Example**: You ship a login feature. A reviewer flags that error messages leak whether an email exists in the system.

1. In the same session, send: "Auth errors should return a generic message regardless of whether the account exists."
2. The system amends the manifest with a new AC, then re-enters `/do --scope <auth-deliverable>` to implement it.
3. `/verify` confirms the fix in selective mode, then auto-triggers the full pass before `/done` is reachable again. Future regressions are caught by the new criterion.

Every round trip through the manifest grows your verification surface. Bug fixes and late requirements become checked criteria, accumulated cumulatively per the manifest's full-PR-state guarantee.

The do session doesn't need to remember the define conversation. The manifest is external state. Run `/do` in a fresh session after `/define`, or at minimum `/compact` before starting.

## What /define Produces

The interview classifies your task (Feature, Bug, Refactor, Prompting, Writing, Document, Blog, Research) and loads task-specific guidance. It probes for your latent criteria, the standards you hold but wouldn't think to spell out. A `manifest-verifier` agent validates the manifest for gaps before output.

<details>
<summary><strong>Example manifest</strong></summary>

````markdown
# Definition: User Authentication

## 1. Intent & Context
- **Goal:** Add password-based authentication to existing Express app
  with JWT sessions. Users can register, log in, and log out.
- **Mental Model:** Auth is a cross-cutting concern. Security invariants
  apply globally; endpoint behavior is per-deliverable.

## 2. Approach
- **Architecture:** Middleware-based auth with JWT stored in httpOnly cookies
- **Execution Order:** D1 (Model) → D2 (Endpoints) → D3 (Protected Routes)
- **Risk Areas:**
  - [R-1] Session fixation if tokens not rotated | Detect: security review
  - [R-2] Timing attacks on password comparison | Detect: constant-time check
- **Trade-offs:**
  - [T-1] Simplicity vs Security → Prefer security (use bcrypt, not md5)

## 3. Global Invariants (The Constitution)
- [INV-G1] Passwords never stored in plaintext
  ```yaml
  verify:
    method: bash
    command: "! grep -r 'password.*=' src/ | grep -v hash | grep -v test"
  ```
- [INV-G2] All auth endpoints rate-limited (max 5 attempts/minute)
  ```yaml
  verify:
    method: subagent
    agent: general-purpose
    model: inherit
    prompt: "Verify rate limiting exists on /login and /register endpoints"
  ```
- [INV-G3] JWT secrets from environment, never hardcoded
  ```yaml
  verify:
    method: bash
    command: "grep -r 'process.env.JWT' src/auth/"
  ```

## 4. Process Guidance (Non-Verifiable)
- [PG-1] Follow existing error handling patterns in the codebase
- [PG-2] Use established logging conventions

## 5. Known Assumptions
- [ASM-1] Express.js already configured | Default: true | Impact if wrong: Add setup step
- [ASM-2] PostgreSQL available | Default: true | Impact if wrong: Adjust migration

## 6. Deliverables (The Work)

### Deliverable 1: User Model & Migration
**Acceptance Criteria:**
- [AC-1.1] User model has id, email, hashedPassword, createdAt
  ```yaml
  verify:
    method: codebase
    pattern: "User.*id.*email.*hashedPassword.*createdAt"
  ```
- [AC-1.2] Email has unique constraint
- [AC-1.3] Migration creates users table with indexes

### Deliverable 2: Auth Endpoints
**Acceptance Criteria:**
- [AC-2.1] POST /register creates user, returns 201
- [AC-2.2] POST /login validates credentials, returns JWT
- [AC-2.3] Invalid credentials return 401, not 500
  ```yaml
  verify:
    method: subagent
    agent: code-bugs-reviewer
    model: inherit
    prompt: "Check auth routes return 401 for auth failures, not 500"
  ```
````

</details>

## The Manifest Schema

| Section | Purpose | ID Scheme |
|---------|---------|-----------|
| **Intent & Context** | Goal and mental model | -- |
| **Approach** | Architecture, execution order, risks, trade-offs | `R-{N}`, `T-{N}` |
| **Global Invariants** | Task-level rules (task fails if violated) | `INV-G{N}` |
| **Process Guidance** | Non-verifiable recommendations for how to work | `PG-{N}` |
| **Known Assumptions** | Low-impact items with defaults | `ASM-{N}` |
| **Deliverables** | Ordered work items with acceptance criteria | `AC-{D}.{N}` |

Approach section is added for complex tasks with dependencies, risks, or architectural decisions.

## Verification Methods

Every criterion can have an automated verification method:

| Method | When to Use | Example |
|--------|-------------|---------|
| `bash` | Commands with deterministic output | `npm run typecheck && npm run lint` |
| `codebase` | Code pattern checks | Check file exists, pattern matches |
| `subagent` | LLM-as-judge for subjective criteria | Code quality, security review |
| `research` | External information lookup | API compatibility, version checks |
| `manual` | Human verification required | UI review, deployment checks |

```yaml
# Bash verification
verify:
  method: bash
  command: "npm run test -- --coverage"

# Subagent verification with specialized reviewer
verify:
  method: subagent
  agent: code-maintainability-reviewer
  model: inherit
  prompt: "Review for DRY violations and coupling issues"

# Slow/expensive verification runs in a later phase
verify:
  method: bash
  phase: 2
  command: "curl -s https://staging.example.com/health"

# Manual verification
verify:
  method: manual
  instructions: "Verify the login flow works in staging"
```

Criteria support a `phase:` field (numeric, default 1). `/verify` runs phases in ascending order — faster checks first, slower/expensive ones only after earlier phases pass. This avoids wasting e2e deploy cycles when cheaper checks are still failing.

## Multi-CLI Support

The Claude Code plugin is the source of truth. Per-CLI distributions under `dist/` provide native packages for other AI coding CLIs. Each has a one-command remote installer — run again to update, or pass `uninstall` to remove only manifest-dev-managed files.

| CLI | Install | Skills | Agents | Hooks | Details |
|-----|---------|--------|--------|-------|---------|
| Claude Code | `/plugin install` | Full | Full | Full | Primary target |
| Gemini CLI | `curl .../gemini/install.sh \| bash` | Full | Full (converted) | Full (adapted) | [README](dist/gemini/README.md) |
| OpenCode | `curl .../opencode/install.sh \| bash` | Full | Full (converted) | Partial (adapted plugin) | [README](dist/opencode/README.md) |
| Codex CLI | `curl .../codex/install.sh \| bash` | Full | TOML stubs | Not available | [README](dist/codex/README.md) |

**Keeping distributions in sync**: After changing plugin components, run `/sync-tools` in Claude Code to regenerate `dist/`. The sync skill reads reference files with per-CLI conversion rules and produces the full distribution for each target.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| `manifest-dev` | Core manifest workflows: `/define`, `/do`, `/verify`, `/tend-pr`, review agents, workflow hooks. The manifest is the canonical source of truth for the PR/branch — feedback during `/do`, `/verify`, or after `/done` defaults to amending it. Verification is selective during fix-loop (in-scope deliverables + globals) with a mandatory full final gate before `/done`. |
| `manifest-dev-tools` | Post-processing utilities for manifest workflows. `/adr` synthesizes Architecture Decision Records from session transcripts via multi-agent extraction pipeline. |
| `manifest-dev-experimental` | **Experimental.** Cron-driven, tick-based manifest runner (`/drive` + `/drive-tick`) with pluggable platform (`none`, `github`) and sink (`local`) adapters. Takes a manifest (or PR in babysit mode) to a terminal state via repeated stateless ticks; each tick delegates implement+verify+fix to `/do` (intra-tick convergence), with cross-tick boundaries handling CI triage, PR tending, and inbox routing. Coexists with `manifest-dev`; nothing deprecated. |

## Plugin Architecture

### Core Skills

| Skill | Type | Description |
|-------|------|-------------|
| `/define` | User-invoked | Interviews you, classifies task type, probes for latent criteria, outputs manifest with verification methods. Defaults to amending a prior in-scope manifest (in-session, conversation-referenced, or branch-archived in `.manifest/`) so one change set keeps one constitution. On a fresh /define against a non-empty branch, seeds from the existing diff. |
| `/do` | User-invoked | Executes against manifest. Follows execution order, watches for risks, logs progress for disaster recovery. Any user feedback during execution defaults to a Self-Amendment cycle (pure questions answered inline). |
| `/auto` | User-invoked | End-to-end autonomous: `/define --interview autonomous` → auto-approve → `/do`. Supports `--mode` and `--tend-pr` pass-through |
| `/tend-pr` | User-invoked | Sets up PR for review and starts polling loop. Manifest-aware or babysit mode |
| `/tend-pr-tick` | User-invoked | Single iteration of PR tending (classify, route, fix). Called by `/loop` via `/tend-pr`; also user-invocable for single-tick runs. PR-comment routing follows the same default-to-amend reflex as in-session feedback. |
| `/verify` | Internal | Spawns verifiers for criteria in scope. Selective passes (in-scope deliverables' ACs + all globals) during fix-loop and after scoped /do; full pass auto-triggered before `/done` so completion always reflects an everything-green run. Phased by iteration speed (fast checks first, e2e/deploy-dependent later). Supports `--cache none\|manifest\|max` for prompt caching across verification agents.|
| `/done` | Internal | Prints hierarchical completion summary mirroring manifest structure. Reachable only after a full-mode green /verify pass. |
| `/escalate` | Internal | Structured escalation when blockers need human intervention. Requires evidence: 3+ attempts, failure reasons, hypothesis, resolution options |
| `/figure-out` | User-invoked | Collaborative thinking partner for any topic. Investigates before claiming, surfaces gaps, resists premature synthesis |
| `/learn-define-patterns` | User-invoked | Analyzes recent /define sessions, extracts user preference patterns, writes them to CLAUDE.md for future /define sessions |
| `thinking-disciplines` | Internal | Core thinking disciplines for rigorous collaborative reasoning. Invoked by `/figure-out` and `/define` |
| `/stop-thinking-disciplines` | User-invoked | Deactivates thinking disciplines mode |

### Review Agents

Built-in agents for quality verification via `subagent` method:

| Agent | Focus |
|-------|-------|
| `criteria-checker` | Core verifier: validates single criterion using bash/codebase/subagent/research methods |
| `cache-warmup` | Cache viability gauge: estimates shared context token footprint, recommends cache strategy. Spawned by `/verify` when `--cache` is active |
| `manifest-verifier` | Validates manifest completeness during `/define` |
| `change-intent-reviewer` | Adversarial intent analysis: reconstructs change intent, finds behavioral divergences across code, prompts, and config |
| `contracts-reviewer` | Bidirectional API/interface contract verification with evidence from docs and codebase |
| `code-bugs-reviewer` | Mechanical code defects: race conditions, data loss, edge cases, resource leaks, dangerous defaults |
| `code-maintainability-reviewer` | DRY violations, coupling, cohesion, dead code, consistency |
| `code-design-reviewer` | Design fitness: reinvented wheels, code vs configuration boundary, under-engineering, interface foresight, PR coherence |
| `code-simplicity-reviewer` | Over-engineering, premature optimization, cognitive complexity |
| `code-testability-reviewer` | Excessive mocking requirements, logic buried in IO, hidden dependencies |
| `code-coverage-reviewer` | Test coverage with proactive edge case enumeration — derives specific test scenarios from code logic |
| `type-safety-reviewer` | TypeScript type safety: `any` abuse, invalid states representable, narrowing issues |
| `docs-reviewer` | Documentation accuracy against code changes |
| `context-file-adherence-reviewer` | Compliance with context file (CLAUDE.md/AGENTS.md/GEMINI.md) project rules |
| `define-session-analyzer` | Analyzes a single /define session transcript for user preference patterns. Spawned by `/learn-define-patterns` |

Each reviewer returns structured output with severity levels (Critical, High, Medium, Low) and specific fix guidance.

### Workflow Enforcement Hooks

Hooks enforce workflow integrity. The AI can't skip steps:

| Hook | Event | Purpose |
|------|-------|---------|
| `stop_do_hook` | Stop command | Blocks premature stopping. Can't stop without verification passing or proper escalation. |
| `post_compact_hook` | Session compaction | Restores /do workflow context after compaction. Reminds to re-read manifest and log. |
| `pretool_verify_hook` | `/verify` invocation | Ensures manifest and log are in context before spawning verifiers. |
| `posttool_log_hook` | Task progress | Reminds to update execution log after task updates, task creation, or workflow skill calls during `/do`. |
| `prompt_submit_hook` | User input during `/do` | Detects manifest amendments when user provides input during `/do` — enables the autonomous Self-Amendment flow. |
| `thinking_disciplines_prompt_hook` | User input | Reinforces thinking disciplines on each user message when active (during `/figure-out` or `/define`). |
| `thinking_disciplines_pretool_hook` | AskUserQuestion | Reinforces thinking disciplines before asking user questions — the moment where sycophantic drift is most likely. |

### Task-Specific Guidance

`/define` loads guidance based on task classification:

| Task Type | Guidance | Quality Gates |
|-----------|----------|---------------|
| **Feature** | `tasks/FEATURE.md` + `CODING.md` | Bug detection, type safety, maintainability, simplicity, test coverage, testability, CLAUDE.md adherence |
| **Bug** | `tasks/BUG.md` + `CODING.md` | Bug fix verification, regression prevention, root cause analysis |
| **Refactor** | `tasks/REFACTOR.md` + `CODING.md` | Behavior preservation, maintainability, simplicity |
| **Prompting** | `tasks/PROMPTING.md` | Prompt quality criteria |
| **Writing** | `tasks/WRITING.md` | Prose quality, AI tells, vocabulary, anti-patterns, craft fundamentals (base for Blog, Document) |
| **Document** | `tasks/DOCUMENT.md` + `WRITING.md` | Structure completeness, consistency |
| **Blog** | `tasks/BLOG.md` + `WRITING.md` | Engagement, SEO |
| **Research** | `tasks/research/RESEARCH.md` + source files | Source-agnostic research methodology. Source-specific guidance in `tasks/research/sources/` |

## Development

```bash
# Setup (first time)
./scripts/setup.sh
source .venv/bin/activate

# Lint, format, typecheck
ruff check --fix claude-plugins/ && black claude-plugins/ && mypy

# Test hooks (run after ANY hook changes)
pytest tests/hooks/ -v

# Test plugin locally
/plugin marketplace add /path/to/manifest-dev
/plugin install manifest-dev@manifest-dev-marketplace
```

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for plugin development guidelines.

## License

MIT

---

*Built by developers who understand LLM limitations, and design around them.*

Follow along: [@aviramkofman](https://x.com/aviramkofman)
