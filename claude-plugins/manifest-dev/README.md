# manifest-dev

Tell Claude what "done" looks like. Let it work. Check the result.

## Quick Start

```
/define "add rate limiting to the API"
/do manifest.md
```

That's it. `/define` interviews you and builds a manifest. `/do` executes it. Two commands.

## The Mindset Shift

Stop thinking about *how* to build it. Start thinking about *what you'd accept*.

"What would make me accept this PR?" "What rules can't be broken?" "How would I know each piece is done?" That's what `/define` asks you. Architecture might come up too, but the pillar is acceptance, not implementation. What does good enough look like?

This works because LLMs are surprisingly good at execution when they know exactly what's expected. They're bad at reading your mind. The manifest closes that gap before a single line of code gets written. Compare that with plan mode, where you're thinking about *how* and still iterating with the model long after implementation starts.

The interview phase is slow. It catches the gaps that blow up after implementation.

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

---

Everything below is reference. You don't need any of it to get started.

---

## The Manifest

The manifest has three moving parts:

1. **Approach** (complex tasks) -- Validated implementation direction: architecture, execution order, risks, trade-offs
2. **Global Invariants** -- Rules that apply to the ENTIRE task (e.g., "tests must pass")
3. **Deliverables** -- Specific items to complete, each with **Acceptance Criteria**
   - ACs can be positive ("user can log in") or negative ("passwords are hashed")

### Schema

```markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts/architecture]

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW - starting direction]
- **Execution Order:** D1 → D2 → D3 | Rationale: [why]
- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
- **Trade-offs:**
  - [T-1] [A] vs [B] → Prefer [A] because [reason]

## 3. Global Invariants (The Constitution)
- [INV-G1] Description | Verify: [method]
- [INV-G2] Description | Verify: [method]
  - E2e tests encode as Global Invariants (one per test case), not deliverable ACs.
    They verify the whole system, not individual deliverables.

## 4. Deliverables (The Work)

### Deliverable 1: [Name]
- **Acceptance Criteria**:
  - [AC-1.1] Description | Verify: [method]
  - [AC-1.2] Description | Verify: [method]
```

### ID Scheme

| Type | Pattern | Purpose | Used By |
|------|---------|---------|---------|
| Global Invariant | INV-G{N} | Task-level rules | /verify (verified) |
| Process Guidance | PG-{N} | Non-verifiable HOW constraints | /do (followed) |
| Risk Area | R-{N} | Pre-mortem flags | /do (watched) |
| Trade-off | T-{N} | Decision criteria for adjustment | /do (consulted) |
| Acceptance Criteria | AC-{D}.{N} | Deliverable completion | /verify (verified) |

Criteria verify blocks support an optional `phase:` field (numeric, default 1). Lower phases run first; later phases (e2e, manual) only run after earlier phases pass.

## Skills

| Skill | Description |
|-------|-------------|
| `/define` | Interviews you, builds an executable manifest with verification criteria. `--interview minimal\|autonomous\|thorough` controls interview style (default: thorough). |
| `/do` | Works through the manifest autonomously, verifies everything passes |
| `/auto` | End-to-end autonomous: `/define --interview autonomous` → auto-approve → `/do` in one command. Supports `--mode` and `--tend-pr` pass-through. |
| `/tend-pr` | Sets up PR for review and starts a polling loop. Manifest-aware mode with scoped `/do`, or babysit mode without a manifest. |
| `/tend-pr-tick` | Single iteration of PR tending (classify comments, route fixes, tend CI). Called by `/loop` via `/tend-pr` — not user-invocable. |
| `/verify` | Runs verifiers phased by iteration speed — fast checks first, e2e/deploy-dependent later. Only advances to the next phase when the current one passes. (You rarely call this directly; `/do` handles it.) |
| `/done` | Prints what got done and what was verified |
| `/escalate` | When something's blocked, surfaces the issue for you to decide |
| `/learn-define-patterns` | Analyzes recent /define sessions, extracts user preference patterns, writes them to CLAUDE.md |

**Optional:** `/figure-out` — figure things out together on any topic. Truth-convergent thinking partner that investigates before claiming, surfaces gaps, and resists premature synthesis. Use when figuring it out IS the goal, or before `/define` when the problem space is foggy. End with `/figure-out-done`.

### Execution Modes

`/do` supports `--mode efficient|balanced|thorough` (default: thorough). Controls verification intensity — cheaper modes use less quota at the cost of verification depth. Only specify when you explicitly want to change it.

| Mode | Key Differences |
|------|----------------|
| **thorough** | Full verification, all quality gates, unlimited parallelism (default) |
| **balanced** | Same models, limited parallelism (max 4), limited fix loops (max 2) |
| **efficient** | Haiku for verification, skips reviewer agents, sequential, max 1 fix loop |

See `skills/do/references/execution-modes/` for per-mode behavioral details.

### Task-Specific Guidance

`/define` works for any task. Domain-specific guidance loads automatically when relevant:

| Task Type | File | When Loaded |
|-----------|------|-------------|
| Code | `skills/define/tasks/CODING.md` | APIs, features, fixes, refactors, tests |
| Writing | `skills/define/tasks/WRITING.md` | Prose, articles, marketing copy (base for Blog, Document) |
| Document | `skills/define/tasks/DOCUMENT.md` | Specs, proposals, formal docs (+ WRITING.md base) |
| Blog | `skills/define/tasks/BLOG.md` | Blog posts, tutorials (+ WRITING.md base) |
| Research | `skills/define/tasks/research/RESEARCH.md` + source files | Research, analysis, investigation. Source-specific guidance in `tasks/research/sources/` |
| Other | (none) | Doesn't fit above categories |

The universal flow works without any task file. Task files contain condensed domain knowledge that `/define` uses during probing. Full reference material for `/verify` agents lives in `skills/define/tasks/references/`.

## How the Interview Works

`/define` doesn't ask you to brainstorm from scratch. It proposes things, you react. It already knows a lot about common task shapes, so it generates candidates and you correct, approve, or reject them. Faster than staring at a blank prompt.

It walks through these in order, starting with whatever gives the most signal:

1. Intent & Context (what kind of task, how big, what could go wrong)
2. Deliverables (what are we building?)
3. Acceptance Criteria (how do we know each piece is done?)
4. Approach (for complex tasks: architecture, execution order, risks, trade-offs)
5. Global Invariants & Process Guidance (rules that apply everywhere, detected automatically)

## Agents

### Core Workflow

| Agent | Purpose |
|-------|---------|
| `criteria-checker` | Read-only verification agent. Validates a single criterion using commands, codebase analysis, file inspection, reasoning, or web research. Returns structured PASS/FAIL. |
| `manifest-verifier` | Reviews /define manifests for gaps and outputs actionable continuation steps. Returns specific questions to ask and areas to probe. |
| `define-session-analyzer` | Analyzes a single /define session transcript for user preference patterns. Spawned by `/learn-define-patterns`. |

### Code Reviewers

These run in parallel during `/verify`:

| Agent | Focus |
|-------|-------|
| `change-intent-reviewer` | Adversarial intent analysis: reconstructs what a change tries to achieve, finds where behavior diverges from intent |
| `contracts-reviewer` | Bidirectional API/interface contract verification with evidence from documentation and codebase |
| `code-bugs-reviewer` | Mechanical code defects: race conditions, data loss, edge cases, resource leaks, dangerous defaults |
| `code-coverage-reviewer` | Test coverage with proactive edge case enumeration — derives specific test scenarios from code logic |
| `code-maintainability-reviewer` | DRY violations, coupling, cohesion, consistency, dead code, architectural boundaries |
| `code-design-reviewer` | Design fitness: reinvented wheels, code vs configuration boundary, under-engineering, interface foresight |
| `code-simplicity-reviewer` | Unnecessary complexity, over-engineering, cognitive burden |
| `code-testability-reviewer` | Code that requires excessive mocking, business logic hard to verify in isolation |
| `type-safety-reviewer` | TypeScript type holes, opportunities to make invalid states unrepresentable |
| `context-file-adherence-reviewer` | Verifies code changes comply with CLAUDE.md instructions and project standards |
| `docs-reviewer` | Audits documentation accuracy against recent code changes |

## Medium Routing

`/define` supports `--medium <platform>` (default: local). Currently only `local` is supported — all interaction happens in the terminal via AskUserQuestion. The medium is encoded in the manifest's Intent section for downstream skills.

## Multi-CLI Distribution

Multi-CLI distributions under `dist/` for Gemini CLI, OpenCode, and Codex CLI are maintained at the repo level via `/sync-tools` (in `.claude/skills/`). The Claude Code plugin is the single source of truth; `/sync-tools` converts agents, adapts hooks into installable target-native payloads, wires additive installer config, and copies skills unchanged. See per-CLI READMEs in `dist/` for installation and feature parity.

## Hooks

Five hooks keep the workflow honest. `stop_do_hook.py` won't let you stop before verification runs. `post_compact_hook.py` restores `/do` context if the session gets compacted. `pretool_verify_hook.py` nudges agents to actually read the manifest before verifying anything. `posttool_log_hook.py` reminds the model to update the execution log after task progress during `/do`. And `prompt_submit_hook.py` reminds the model to check for manifest amendments when the user provides input during `/do` — enabling the autonomous Self-Amendment flow (`/escalate` → `/define --amend` → `/do` resume).
