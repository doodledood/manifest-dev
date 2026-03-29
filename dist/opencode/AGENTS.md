# manifest-dev Workflow for OpenCode

Verification-first manifest workflows. Plan work thoroughly, execute against criteria, verify everything passes.

Version: 0.74.0

## Workflow Overview

```
/define  -->  /do  -->  /verify  -->  /done
   |            |          |            |
   v            v          v            v
 Manifest    Execute    Check all    Summary
 builder     work       criteria     report
                           |
                           v
                       /escalate
                       (if blocked)

/auto  =  /define (autonomous) --> auto-approve --> /do
```

1. **/define** builds a Manifest: deliverables, acceptance criteria, global invariants, verification methods
2. **/do** executes the manifest: works through deliverables, logs progress, follows process guidance
3. **/verify** spawns parallel verification agents to check every criterion
4. **/done** outputs completion summary (called by /verify on success)
5. **/escalate** surfaces blocking issues with structured evidence (called when stuck)
6. **/auto** chains /define and /do into a single autonomous flow -- defines the task without user interview, auto-approves the manifest, and immediately executes

## Skills (7)

| Skill | User-Invocable | Purpose |
|-------|---------------|---------|
| `define` | Yes | Manifest builder -- interactive interview to plan work |
| `do` | Yes | Manifest executor -- implements deliverables against criteria |
| `verify` | No | Verification runner -- spawns parallel verifier agents |
| `auto` | Yes | End-to-end /define + /do in one command |
| `done` | No | Completion marker -- outputs summary after verification |
| `escalate` | No | Structured escalation during /do |
| `learn-define-patterns` | Yes | Analyze past sessions, extract preferences to AGENTS.md |

## Commands (4)

| Command | Skill |
|---------|-------|
| `/define` | define |
| `/do` | do |
| `/auto` | auto |
| `/learn-define-patterns` | learn-define-patterns |

## Agents (14)

### Verification Orchestration

**criteria-checker** -- Read-only verification agent. Validates a single criterion using any automated method: commands, codebase analysis, file inspection, reasoning, web research. Returns structured PASS/FAIL results. Spawned by /verify in parallel, one per criterion.

**manifest-verifier** -- Reviews /define manifests for gaps and outputs actionable continuation steps. Returns specific questions to ask and areas to probe so the interview can continue. Invoked at the end of /define before user approval.

### Code Review Suite (10 agents)

Specialized reviewers spawned by /verify for code quality criteria. Each covers an orthogonal domain with strict out-of-scope boundaries to prevent overlap.

**change-intent-reviewer** -- Adversarially analyze whether code, prompt, or config changes achieve their stated intent. Reconstructs change intent from diff context, then systematically attacks the logic to find behavioral divergences.

**code-bugs-reviewer** -- Audit code changes for mechanical defects -- runtime failures, resource issues, and structural code flaws. Focuses on defects detectable from code patterns (race conditions, resource leaks, edge cases, dangerous defaults) rather than intent-behavior analysis.

**code-design-reviewer** -- Audit code for design fitness. Covers reinvented wheels, code vs configuration boundary, under-engineering, interface/contract foresight, concept purity/misuse, and PR-level coherence.

**code-simplicity-reviewer** -- Audit code for unnecessary complexity. Covers over-engineering, premature optimization, cognitive complexity, clarity over cleverness, and unnecessary indirection.

**code-maintainability-reviewer** -- Audit code for maintainability. Covers DRY violations, structural complexity, dead code, consistency, concept drift, boundary leakage, migration debt, coupling, cohesion, temporal coupling, linter suppression abuse, extensibility risk, and contract surface issues.

**code-coverage-reviewer** -- Verify code changes have adequate test coverage by proactively enumerating edge cases from the code's logic. Derives specific test scenarios with concrete inputs and expected outputs, and reports coverage gaps.

**code-testability-reviewer** -- Audit code for testability issues. Identifies excessive mocking requirements, business logic buried in IO, non-deterministic inputs, and tight coupling that makes verification hard.

**contracts-reviewer** -- Verify API and interface contract correctness with evidence. Checks both outbound (code calls external/internal APIs correctly per documentation) and inbound (changes don't break consumers of your interfaces).

**type-safety-reviewer** -- Audit code for type safety across typed languages. Identifies any/unknown abuse, invalid states representable, type narrowing gaps, generic type issues, nullability problems, and discriminated union anti-patterns.

**docs-reviewer** -- Audit documentation and code comments for accuracy against recent code changes. Reports discrepancies between docs and code behavior.

### Project Standards

**context-file-adherence-reviewer** -- Verify code changes comply with context file instructions (CLAUDE.md, AGENTS.md, GEMINI.md) and project standards. Audits against outcome-based rules defined in the project's context files.

### Learning

**define-session-analyzer** -- Analyze a single /define session transcript to extract user preference patterns. Spawned by /learn-define-patterns for parallel per-session analysis. Extracts probing hints, trade-off defaults, recurring invariants, and quality gate adjustments.

## Hook Behaviors

The manifest-dev plugin (`plugins/manifest-dev.ts`) implements workflow enforcement hooks:

| Hook | Behavior | Can Block? |
|------|----------|------------|
| **Stop enforcement** | Re-engages agent when /do workflow exits without /done or /escalate | No (fire-and-forget) |
| **Verify context** | Injects reminder to read manifest/log before spawning verifiers | No (context injection) |
| **Post-compact recovery** | Restores /do workflow context after session compaction | No (context injection) |
| **Amendment check** | Reminds agent to check if user input changes the manifest scope | No (system message) |
| **Log reminder** | Nudges agent to update execution log after milestone tool calls | No (output mutation) |

### Limitations

- **Stop hook cannot block**: `session.idle` is fire-and-forget. The plugin attempts re-engagement via `ctx.client.session.prompt()` but this is fragile.
- **Subagent bypass**: `tool.execute.before`/`after` does NOT fire for tool calls within subagents (issue #5894). Hooks will not trigger for tools called by criteria-checker or other verification agents.
- **Experimental APIs**: `experimental.session.compacting` and `experimental.chat.system.transform` may change without notice.
- **Ephemeral state**: Plugin workflow state is in-memory. Lost on server restart.

See `plugins/HOOK_SPEC.md` for the complete behavioral specification.
