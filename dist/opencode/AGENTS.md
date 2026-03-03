# manifest-dev Workflow for OpenCode

Verification-first manifest workflows. Plan work thoroughly, execute against criteria, verify everything passes.

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
```

1. **/define** builds a Manifest: deliverables, acceptance criteria, global invariants, verification methods
2. **/do** executes the manifest: works through deliverables, logs progress, follows process guidance
3. **/verify** spawns parallel verification agents to check every criterion
4. **/done** outputs completion summary (called by /verify on success)
5. **/escalate** surfaces blocking issues with structured evidence (called when stuck)

## Agents (12)

### Verification Orchestration

**criteria-checker** -- Read-only verification agent. Validates a single criterion using any automated method: commands, codebase analysis, file inspection, reasoning, web research. Returns structured PASS/FAIL results. Spawned by /verify in parallel, one per criterion.

**manifest-verifier** -- Reviews /define manifests for gaps and outputs actionable continuation steps. Returns specific questions to ask and areas to probe so the interview can continue. Invoked at the end of /define before user approval.

### Code Review Suite (8 agents)

Specialized reviewers spawned by /verify for code quality criteria. Each covers an orthogonal domain with strict out-of-scope boundaries to prevent overlap.

**code-bugs-reviewer** -- Audit code changes for logical bugs. Covers race conditions, data loss, edge cases, logic errors, error handling, state inconsistencies, observable incorrect behavior, resource leaks, dangerous defaults, and fail-loudly violations.

**code-design-reviewer** -- Audit code for design fitness. Covers reinvented wheels, code vs configuration boundary, under-engineering, interface/contract foresight, concept purity/misuse, and PR-level coherence.

**code-simplicity-reviewer** -- Audit code for unnecessary complexity. Covers over-engineering, premature optimization, cognitive complexity, clarity over cleverness, and unnecessary indirection.

**code-maintainability-reviewer** -- Audit code for maintainability. Covers DRY violations, structural complexity, dead code, consistency, concept drift, boundary leakage, migration debt, coupling, cohesion, temporal coupling, linter suppression abuse, extensibility risk, and contract surface issues.

**code-coverage-reviewer** -- Verify code changes have adequate test coverage. Identifies missing test files, untested functions, untested branches, missing error path coverage, and missing edge case coverage.

**code-testability-reviewer** -- Audit code for testability issues. Identifies excessive mocking requirements, business logic buried in IO, non-deterministic inputs, and tight coupling that makes verification hard.

**type-safety-reviewer** -- Audit code for type safety across typed languages. Identifies any/unknown abuse, invalid states representable, type narrowing gaps, generic type issues, nullability problems, and discriminated union anti-patterns.

**docs-reviewer** -- Audit documentation and code comments for accuracy against recent code changes. Reports discrepancies between docs and code behavior.

### Project Standards

**claude-md-adherence-reviewer** -- Verify code changes comply with CLAUDE.md instructions and project standards. Audits against outcome-based rules defined in CLAUDE.md files.

### Learning

**define-session-analyzer** -- Analyze a single /define session transcript to extract user preference patterns. Spawned by /learn-define-patterns for parallel per-session analysis. Extracts probing hints, trade-off defaults, recurring invariants, and quality gate adjustments.
