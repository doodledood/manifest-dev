# Manifest Schema

````markdown
# Definition: [Title]

## 1. Intent & Context
- **Goal:** [High-level purpose]
- **Mental Model:** [Key concepts to understand]
- **Medium:** local *(default and currently only supported)*

## 2. Approach (Complex Tasks Only)
*Initial direction, not rigid plan. Expect adjustment when reality diverges.*

- **Architecture:** [High-level HOW — starting direction]
- **Execution Order:**
  - D1 → D2 → D3
  - Rationale: [why this order]
- **Risk Areas:**
  - [R-1] [What could go wrong] | Detect: [how you'd know]
- **Trade-offs:**
  - [T-1] [Priority A] vs [Priority B] → Prefer [A] because [reason]

## 3. Global Invariants
*Rules that apply to the ENTIRE execution. If these fail, the task fails.*

- [INV-G1] Description: ... | Verify: [Method]
  ```yaml
  verify:
    method: bash | codebase | subagent | research | manual | deferred-auto
    phase: 1                       # optional integer, default 1; higher phases run after lower pass
    timeout: 30s | 5m | 6h | 1d    # optional wall-clock cap; integer + s|m|h|d suffix. Use for lifecycle ACs that legitimately wait (CI polling, approval, deploy). Absent → no cap.
    inner_method: subagent | bash | codebase | research   # REQUIRED when method: deferred-auto
    command: "[if bash, or deferred-auto with inner_method: bash]"
    agent: "[if subagent, or deferred-auto with inner_method: subagent]"
    model: "[optional, if subagent — defaults to inherit]"
    prompt: "[if subagent or research, or matching deferred-auto inner_method]"
  ```

*`deferred-auto`: user-triggered; runs only via `/verify --deferred`. Required `inner_method:` names the underlying verifier type. See `MULTI_REPO.md` §e for cross-repo semantics.*

*Auto-decided items carry `(auto)` after the ID, e.g. `[INV-G2] (auto) Description: ...`. Same convention applies to AC-* and PG-* that were auto-decided. Each auto-decided item also appears in Known Assumptions with reasoning.*

## 4. Process Guidance
*Constraints on HOW to work. Not gates — guidance for the implementer.*

- [PG-1] Description: ...

## 5. Known Assumptions
*Low-impact items where a reasonable default was chosen without explicit user confirmation. If wrong, amend.*

- [ASM-1] [What was assumed] | Default: [chosen value] | Impact if wrong: [consequence]

## 6. Deliverables
*Ordered by execution order from Approach, or by dependency then importance.*

### Deliverable 1: [Name]

**Acceptance Criteria:**
- [AC-1.1] Description: ... | Verify: ...
  ```yaml
  verify:
    method: ...
    phase: 1
    # ...same fields as INV-G verify
  ```
````

## Categories — what the Manifest captures

| Category | What | Examples |
|----------|------|----------|
| Global Invariants (INV-G*) | Negative constraints, ongoing, verifiable | "No breaking changes to public API"; "Don't edit /legacy" |
| Process Guidance (PG-*) | Non-verifiable HOW constraints | "Manual optimization only"; "No bullet points in summary" |
| Deliverables + ACs | Positive milestones (functional / non-functional / process) | "Section X explains Y"; "Document under 2000 words"; "Contains 'Executive Summary' section" |

## Encoding disciplines

- **Insights become criteria.** Every discovery encoded — INV-G*, AC-*, PG-*, R-*, T-*, or ASM-* — or explicitly scoped out with logged reasoning.
- **Automate verification.** Manual is last resort.
- **Verification phases.** Group by iteration speed — fast feedback first. Fast checks (bash, agent reviewers) in default phase 1. Slow checks (e2e, deploy-dependent) in later phases. Manual goes last. Omit `phase:` for phase 1; non-contiguous phases valid.
